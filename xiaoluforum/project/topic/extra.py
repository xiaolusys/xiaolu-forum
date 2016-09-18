# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from spirit.comment.models import Comment
from spirit.topic.models import Topic
from django.db.models import Sum


#获得一个topic的所有点击喜欢的数目
def get_likes_count_by_topic(topic):
    comments = Comment.objects \
        .for_topic(topic=topic)
    sum = comments.aggregate(Sum('likes_count'))
    return sum['likes_count__sum']

#获取一个帖子的第一个评论
def get_first_comment_by_topic(topic):
    comments = Comment.objects \
        .for_topic(topic=topic) \
        .order_by('date')
    comments = comments.first().comment
    if comments.find('http') != -1:
        comments = comments[0:20]+"......"
    if len(comments)>50:
        comments = comments[0:50]+"......"
    if comments.find('7xogkj')!= -1:
        comments = '......'
    return comments

#获得所有topic喜欢的数目
def get_likes_count_by_topics(topics):
    for topic in topics:
        topic.like_counts = get_likes_count_by_topic(topic)

#获取所有帖子的第一个评论
def get_first_comment_by_topics(topics):
    for topic in topics:
        topic.first_comment = get_first_comment_by_topic(topic)


def get_topic_by_mysort(*categories):
    cat = []
    cat.append(categories[2])
    cat.append(categories[1])
    cat.append(categories[0])
    return cat