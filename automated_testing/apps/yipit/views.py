#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests


def verify_if_deal_url_is_valid(request, deal_id):
    from django.http import HttpResponse
    from yipit.models import Deal

    # getting the deal from MySQL
    mydeal = Deal.objects.get(id=deal_id)
    # checking if its url is still valid
    response = requests.get(mydeal.url)

    # generating a json
    data = json.dumps({
        'succeeded': mydeal.title in response.text,
    })
    return HttpResponse(data, mimetype="application/json")
