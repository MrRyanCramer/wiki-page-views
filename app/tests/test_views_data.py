import pytest


@pytest.fixture
def daily_views_for_article_in_month():
    return {'items': [
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110100',
         'access': 'all-access', 'agent': 'user', 'views': 35},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110200',
         'access': 'all-access', 'agent': 'user', 'views': 50},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110300',
         'access': 'all-access', 'agent': 'user', 'views': 60},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110400',
         'access': 'all-access', 'agent': 'user', 'views': 62},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110500',
         'access': 'all-access', 'agent': 'user', 'views': 66},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110600',
         'access': 'all-access', 'agent': 'user', 'views': 143},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110700',
         'access': 'all-access', 'agent': 'user', 'views': 344},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110800',
         'access': 'all-access', 'agent': 'user', 'views': 748},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110900',
         'access': 'all-access', 'agent': 'user', 'views': 895},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111000',
         'access': 'all-access', 'agent': 'user', 'views': 899},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111100',
         'access': 'all-access', 'agent': 'user', 'views': 926},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111200',
         'access': 'all-access', 'agent': 'user', 'views': 1068},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111300',
         'access': 'all-access', 'agent': 'user', 'views': 941},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111400',
         'access': 'all-access', 'agent': 'user', 'views': 965},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111500',
         'access': 'all-access', 'agent': 'user', 'views': 931},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111600',
         'access': 'all-access', 'agent': 'user', 'views': 689},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111700',
         'access': 'all-access', 'agent': 'user', 'views': 670},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111800',
         'access': 'all-access', 'agent': 'user', 'views': 511},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111900',
         'access': 'all-access', 'agent': 'user', 'views': 597},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112000',
         'access': 'all-access', 'agent': 'user', 'views': 274},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112100',
         'access': 'all-access', 'agent': 'user', 'views': 146},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112200',
         'access': 'all-access', 'agent': 'user', 'views': 149},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112300',
         'access': 'all-access', 'agent': 'user', 'views': 131},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112400',
         'access': 'all-access', 'agent': 'user', 'views': 112},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112500',
         'access': 'all-access', 'agent': 'user', 'views': 99},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112600',
         'access': 'all-access', 'agent': 'user', 'views': 113},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112700',
         'access': 'all-access', 'agent': 'user', 'views': 139},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112800',
         'access': 'all-access', 'agent': 'user', 'views': 96},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023112900',
         'access': 'all-access', 'agent': 'user', 'views': 143},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023113000',
         'access': 'all-access', 'agent': 'user', 'views': 226}]}


@pytest.fixture
def daily_views_for_article_in_week():
    return {'items': [
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110600',
         'access': 'all-access', 'agent': 'user', 'views': 143},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110700',
         'access': 'all-access', 'agent': 'user', 'views': 344},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110800',
         'access': 'all-access', 'agent': 'user', 'views': 748},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023110900',
         'access': 'all-access', 'agent': 'user', 'views': 895},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111000',
         'access': 'all-access', 'agent': 'user', 'views': 899},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111100',
         'access': 'all-access', 'agent': 'user', 'views': 926},
        {'project': 'en.wikipedia', 'article': 'Dawngate', 'granularity': 'daily', 'timestamp': '2023111200',
         'access': 'all-access', 'agent': 'user', 'views': 1068}]}


@pytest.fixture
def top_articles():
    return {'items': [
        {'project': 'en.wikipedia', 'access': 'all-access', 'year': '2023', 'month': '01', 'day': '02',
         'articles': [
             {'article': 'Main_Page', 'views': 100, 'rank': 1},
             {'article': 'Special:Search', 'views': 10, 'rank': 2},
             {'article': 'Avatar:_The_Way_of_Water', 'views': 1, 'rank': 3}]}]}


@pytest.fixture
def monthly_views_for_article():
    return {'items': [
        {'access': 'all-access',
         'agent': 'user',
         'article': 'Dawngate',
         'granularity': 'monthly',
         'project': 'en.wikipedia',
         'timestamp': '2023010100', 'views': 600}]}
