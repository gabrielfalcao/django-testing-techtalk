#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mock import patch
from yipit.models import Deal


@patch('yipit.models.Deal.objects')
@patch('yipit.models.Redis')
def test_get_related_deals_from_redis(Redis, deal_queryset):
    (u"Get related deals should fetch data from redis")
    # Given an instance of Redis connection
    connection = Redis.return_value

    # And that by calling connection.zrange it returns a list of ids
    connection.zrange.return_value = [777]

    # And that by Deal.objects.get it returns a Fake deal
    deal_queryset.get.return_value = "Deal wannabe"

    # When I get related deals from a given deal
    deal = Deal()
    deal.id = 42
    related_deals = deal.get_related_deals()

    # Then related deals is a list of one faked deal
    related_deals.should.equal(["Deal wannabe"])

    # And zrange was called appropriately
    connection.zrange.assert_called_once_with(
        "yipit:related-deals:42", 0, -1,
    )


def test_deal_is_human_readable_when_wrapped_as_unicode():
    (u"A Deal should be human readable after wrapped in unicode")
    import requests
    from yipit.models import Deal

    # Given a deal with title, source and expiration date
    lunch = Deal()
    lunch.title = u"50% off at Shake Shack"
    lunch.source = u"KGB Deals"

    # When I wrap it was unicode
    representation = unicode(lunch)

    # Then it should look like this
    representation.should.equal(u"50% off at Shake Shack, by KGB Deals")
