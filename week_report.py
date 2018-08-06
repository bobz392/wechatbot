#! /usr/bin/env python2.7
#coding=utf-8

import logging
from gensim import corpora, models, similarities
from model import Message

class WeekReport(object):


    def preview(self, name):
        notes = Message.query_weekly_message(name)