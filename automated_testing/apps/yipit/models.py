#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import Redis
from django.db import models


class Deal(models.Model):
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()
    url = models.URLField()

    def get_related_deals(self):
        db = Redis()
        key = "yipit:related-deals:{0}".format(self.id)

        deals = []
        for deal_id in db.zrange(key, 0, -1):
            deals.append(Deal.objects.get(id=deal_id))

        return deals

    def __unicode__(self):
        return u"{0}, by {1}".format(self.title, self.source)
