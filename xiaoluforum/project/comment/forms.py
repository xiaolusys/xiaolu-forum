# -*- coding: utf-8 -*-

# from __future__ import unicode_literals

import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_bytes

from spirit.core import utils
from spirit.core.utils.markdown import Markdown
from spirit.topic.models import Topic
from spirit.comment.poll.models import CommentPoll, CommentPollChoice
from spirit.comment.models import Comment

from qiniu import Auth, put_file, put_data, etag, urlsafe_base64_encode
import qiniu.config
import hashlib
from django.utils import six
import Image

class CommentForm(forms.ModelForm):

    comment = forms.CharField(
        max_length=settings.ST_COMMENT_MAX_LEN,
        widget=forms.Textarea)
    comment_hash = forms.CharField(
        max_length=32,
        widget=forms.HiddenInput,
        required=False)

    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, user=None, topic=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user
        self.topic = topic
        self.mentions = None  # {username: User, }
        self.polls = None  # {polls: [], choices: []}
        self.fields['comment'].widget.attrs['placeholder'] = _("Write comment...")

    def get_comment_hash(self):
        assert self.topic

        # This gets saved into
        # User.last_post_hash,
        # it does not matter whether
        # is a safe string or not
        comment_hash = self.cleaned_data.get('comment_hash', None)

        if comment_hash:
            return comment_hash

        return utils.get_hash((
            smart_bytes(self.cleaned_data['comment']),
            smart_bytes('thread-{}'.format(self.topic.pk))
        ))

    def _get_comment_html(self):
        user = self.user or self.instance.user
        markdown = Markdown(no_follow=not user.st.is_moderator)
        comment_html = markdown.render(self.cleaned_data['comment'])
        self.mentions = markdown.get_mentions()
        self.polls = markdown.get_polls()
        return comment_html

    def _save_polls(self):
        assert self.instance.pk
        assert self.polls is not None

        polls = self.polls['polls']
        choices = self.polls['choices']

        CommentPoll.update_or_create_many(comment=self.instance, polls_raw=polls)
        CommentPollChoice.update_or_create_many(comment=self.instance, choices_raw=choices)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.topic = self.topic

        self.instance.comment_html = self._get_comment_html()
        comment = super(CommentForm, self).save(commit)

        if commit:
            self._save_polls()

        return comment


class CommentMoveForm(forms.Form):

    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.TextInput)

    def __init__(self, topic, *args, **kwargs):
        super(CommentMoveForm, self).__init__(*args, **kwargs)
        self.fields['comments'] = forms.ModelMultipleChoiceField(
            queryset=Comment.objects.filter(topic=topic),
            widget=forms.CheckboxSelectMultiple
        )

    def save(self):
        comments = self.cleaned_data['comments']
        comments_list = list(comments)
        topic = self.cleaned_data['topic']
        comments.update(topic=topic)

        # Update topic in comment instance
        for c in comments_list:
            c.topic = topic

        return comments_list

def generate_public_url(filepath):
    bucket_domain = settings.QINIU_PUBLIC_DOMAIN
    # 有两种方式构造base_url的形式
    base_url = 'http://%s/%s' % (bucket_domain, filepath)

    return base_url


def upload_public_to_remote(filepath, iostream):
    """ 上传公开文件到第三方 """
    # 需要填写你的 Access Key 和 Secret Key
    access_key = "M7M4hlQTLlz_wa5-rGKaQ2sh8zzTrdY8JNKNtvKN"
    secret_key = "8MkzPO_X7KhYQjINrnxsJ2eq5bsxKU1XmE8oMi4x"

    # 要上传的空间
    bucket_name = 'xiaolumm'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filepath)
    ret, info = put_file(token, filepath, iostream)

    return info


def get_hash(bytes_iter):
    assert not isinstance(
        bytes_iter,
        (six.text_type, six.binary_type))  # Avoid gotcha

    # todo: test!
    md5 = hashlib.md5()

    for b in bytes_iter:
        md5.update(b)

    return md5.hexdigest()

class CommentImageForm(forms.Form):

    image = forms.ImageField()

    def __init__(self, user=None, *args, **kwargs):
        super(CommentImageForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_image(self):
        file = self.cleaned_data['image']

        if file.image.format.lower() not in settings.ST_ALLOWED_UPLOAD_IMAGE_FORMAT:
            raise forms.ValidationError(
                _("Unsupported file format. Supported formats are %s."
                  % ", ".join(settings.ST_ALLOWED_UPLOAD_IMAGE_FORMAT))
            )

        return file


    def save(self):
        # todo: use DEFAULT_FILE_STORAGE and MEDIA_URL

        file = self.cleaned_data['image']
        file_hash = get_hash(file.chunks())
        file.name = ''.join((file_hash, '.', file.image.format.lower()))
        upload_to = os.path.join('spirit', 'images', str(self.user.pk))
        file.url = os.path.join(settings.MEDIA_URL, upload_to, file.name).replace("\\", "/")
        media_path = os.path.join(settings.MEDIA_ROOT, upload_to)
        utils.mkdir_p(media_path)
        with open(os.path.join(media_path, file.name), 'wb') as fh:
            for c in file.chunks():
                fh.write(c)

            file.close()

        return file
