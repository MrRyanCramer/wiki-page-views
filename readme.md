# Context





# Installation

# API Documentation

## Top viewed articles for week
Returns a list of the most viewed articles for a given week.

`GET /views/top-articles/week/{year}/{week}`

### Parameters
| Parameter | Description                                          |
|-----------|------------------------------------------------------|
| year      | The year of the date, in YYYY format.                |
| week      | The [Iso week number](#iso-week-number) of the date. |

### Response

## Top viewed articles for month

Returns a list of the most viewed articles for a given month.

`GET /views/top-articles/month/{year}/{month}`

### Parameters

| Parameter | Description                           |
|-----------|---------------------------------------|
| year      | The year of the date, in YYYY format. |
| month     | The month of the date, in MM format.  |

## Highest view day of month for article

Returns the day of the month when an article got the most page views.

`GET /views/top-day/{article}/{year}/{month}`

### Parameters

| Parameter | Description                           |
|-----------|---------------------------------------|
| article   | The title of the article.             |
| year      | The year of the date, in YYYY format. |
| month     | The month of the date, in MM format.  |

## Article views for week 

Returns the view count of a specific article for a given week.

`GET /views/article/week/{article}/{year}/{week}`

### Parameters

| Parameter | Description                                          |
|-----------|------------------------------------------------------|
| article   | The title of the article.                            |
| year      | The year of the date, in YYYY format.                |
| week      | The [Iso week number](#iso-week-number) of the date. |

## Article views for month

Returns the view count of a specific article for a given month.

`GET /views/article/month/{article}/{year}/{month}`

### Parameters

| Parameter | Description                           |
|-----------|---------------------------------------|
| article   | The title of the article.             |
| year      | The year of the date, in YYYY format. |
| month     | The month of the date, in MM format.  |



# Appendix
## ISO Week number
Week numbers in this service use the ISO formatting convention, as specified in the [python documentation](https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar).

_"The ISO year consists of 52 or 53 full weeks, and where a week starts on a Monday and ends on a Sunday. The first week of an ISO year is the first (Gregorian) calendar week of a year containing a Thursday. This is called week number 1, and the ISO year of that Thursday is the same as its Gregorian year."_

# Design Notes
I've recorded a few of my thoughts as I tackled this problem in the hopes that you gain a better understanding of how I think and approach problems.
## On the most viewed articles for a week
For the most viewed articles per week requirement, the wikipedia API has two relevant article-specific endpoints.
* Get pageview counts for a page.
* Get the most viewed articles for a project.

The first is less useful here, due to the sheer number of articles.
It would be expensive, and less practical to query all articles for their view counts.
The second endpoint has a limitation, where it only supports timespans of a month, or a day.
Using a month would not provide adequate granularity.
This leads to the conclusion of gathering the data from 7 calls to the most viewed articles API, one for each day in the week.
Once the data is gathered, it can be aggregated and sorted.

There are corner cases with the threshold values that could make this approach not generate 100% accurate results.
Luckily, these corner cases are resolved with the listed assumption that any article not listed on a day has 0 views.

## On the most viewed articles per month
The previous limitation with the wikipedia data granularity is not present with this use case.
This lets us get away with using the API directly for the answer. 

## On the view count of a specific article for a week or month
Here the `Get pageview counts for a page` wikipedia endpoint helps out a great deal.
It has both daily and monthly granularity with a specifiable date range.
For the month requirement, set the range to the whole month, and set the granularity to monthly.
This gets the view data directly.
For the week requirement, set the range to the specific week, and set the granularity to daily.
This gets an array of views per day, that can be aggregated for the final answer.

## On the day of the month when an article got the most page views
Again we are helped out by the `Get pageview counts for a page` wikipedia endpoint.
We can set the range to the target month, and the granularity to daily.
The resulting array can be searched for the maximum view number, and the day that it corresponds to.

## Next Steps
Depends on context, and needs.  Seek feedback.
 * Authentication
 * Caching
 * Observability
 * Scalability
 * Convenience methods
 * Internationalization
 * Improved routing