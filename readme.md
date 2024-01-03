# Context
This is an academic project, with the intentions of learning and serving as a demonstration of my web development skills.
Going in to this project, I made the decision to utilize the opportunity to learn a technology stack that was completely new to me.
While I have significant experience in other languages, before this project I have not worked specifically 
with Python, Flask, or Pytest.
There are some additional challenges when working with a new tech stack, 
so if you notice some language or library features that are not being leveraged quite right, let me know, I'd love the feedback!

# Installation

## Docker
Docker compose can be used to get started quickly.
```bash
$ docker-compose up --build
```
This API is exposed on port `8000`.  An example call is shown below:
```bash
$ curl --request GET \
  --url http://localhost:8000/api/v1/views/top-day/Dawngate/2023/1
```
## Testing
Unit tests were implemented using pytest.  To run the entire test suite, simply use the `pytest` command.

For more granular control, tests for the page view api were split into two suites. 
The first suite is for integration tests which hits the wikipedia API directly.
The second is for unit tests, which utilize mock data instead.

```bash
# Run the unit tests only
pytest ./app/tests/test_views.py::TestPageViewMocked
# Run the integration tests only
pytest ./app/tests/test_views.py::TestPageViewIntegration
```

# API Documentation

## Response Codes and Errors
All provided endpoints will return json.

On a successful response, endpoints will return a status code: `200`

On api errors, endpoints will return a json response with more information in the `error` and `message` values.
The status code of an error response will be a `4XX` or `5XX`

Example error response:
```json
{
  "error": "bad request",
  "message": "Invalid year or month provided"
}
```

## Top viewed articles for week
Returns a list of the top 1000 most viewed articles for a given week.

`GET /api/v1/views/top-articles/week/{year}/{week}`

### Parameters
| Parameter | Description                                          |
|-----------|------------------------------------------------------|
| year      | The year of the date, in YYYY format.                |
| week      | The [Iso week number](#iso-week-number) of the date. |

### Example Response
```json
{
  "articles": [
    {
      "article": "Main_Page",
      "rank": 1,
      "views": 33951684
    },
    {
      "article": "Special:Search",
      "rank": 2,
      "views": 8984262
    },
    ...
  ]
}
```

## Top viewed articles for month

Returns a list of the top 1000 most viewed articles for a given month.

`GET /api/v1/views/top-articles/month/{year}/{month}`

### Parameters

| Parameter | Description                           |
|-----------|---------------------------------------|
| year      | The year of the date, in YYYY format. |
| month     | The month of the date, in MM format.  |

### Example response
```json
{
  "articles": [
    {
      "article": "Main_Page",
      "rank": 1,
      "views": 153563201
    },
    {
      "article": "Special:Search",
      "rank": 2,
      "views": 41184546
    },
    ...
  ]
}
```

## Highest view day of month for article

Returns the day of the month when an article got the most page views.

`GET /api/v1/views/top-day/{article}/{year}/{month}`

### Parameters

| Parameter | Description                                  |
|-----------|----------------------------------------------|
| article   | The [title of the article.](#article-titles) |
| year      | The year of the date, in YYYY format.        |
| month     | The month of the date, in MM format.         |

### Example response
```json
{
  "day": 4
}
```

## Article views for week 

Returns the view count of a specific article for a given week.

`GET /api/v1/views/article/week/{article}/{year}/{week}`

### Parameters

| Parameter | Description                                          |
|-----------|------------------------------------------------------|
| article   | The [title of the article.](#article-titles)         |
| year      | The year of the date, in YYYY format.                |
| week      | The [Iso week number](#iso-week-number) of the date. |

### Example response
```json
{
  "views": 129
}
```

## Article views for month

Returns the view count of a specific article for a given month.

`GET /api/v1/views/article/month/{article}/{year}/{month}`

### Parameters

| Parameter | Description                                  |
|-----------|----------------------------------------------|
| article   | The [title of the article.](#article-titles) |
| year      | The year of the date, in YYYY format.        |
| month     | The month of the date, in MM format.         |

### Example response
```json
{
  "views": 600
}
```

# Appendix
## Article titles
Article titles will use the same formatting as required from the dependent API.
 * Any spaces should be replaced with underscores.
 * Special characters should be URI-encoded, so that non-URI-safe characters like %, / or ? are accepted.

## ISO Week number
Week numbers in this service use the ISO formatting convention, as specified in the [python documentation](https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar).

_"The ISO year consists of 52 or 53 full weeks, and where a week starts on a Monday and ends on a Sunday. The first week of an ISO year is the first (Gregorian) calendar week of a year containing a Thursday. This is called week number 1, and the ISO year of that Thursday is the same as its Gregorian year."_

# Design Notes
I've recorded a few of my thoughts as I tackled this problem in the hopes that you gain a better understanding of how I think and approach problems.
## On the most viewed articles for a week
For the most viewed articles per week requirement, the wikipedia API has two relevant article-specific endpoints.
* `Get pageview counts for a page`
* `Get the most viewed articles for a project`

The first is less useful here, due to the sheer number of articles.
It would be expensive, and less practical to query all articles for their view counts.
The second endpoint has a limitation, where it only supports timespans of a month, or a day.
Using a month would not provide adequate granularity.
This leads to the conclusion of gathering the data from 7 calls to the most viewed articles API, one for each day in the week.
Once the data is gathered, it can be aggregated and sorted.
I don't love this from a performance standpoint, and it would be a likely early candidate for optimization.

There are corner cases with the threshold values that could make this approach not generate 100% accurate results.
Luckily, these corner cases are resolved with the listed assumption that any article not listed on a day should be considered to have no views.

## On the most viewed articles per month
The previous limitation with the wikipedia data granularity is not present with this use case.
This lets us get away with using the `Get the most viewed articles for a project` endpoint directly for the answer. 

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

## Assumptions

In the implemented wikipedia service, hardcoded defaults were chosen when retrieving information
The actual values to be used would depend on the use case,
and the code could be easily updated to reflect the desired behavior.

| Parameter | Default            | Rationale                                      |
|-----------|--------------------|------------------------------------------------|
| project   | `en.wikipedia.org` | English wikipedia is a commonly known project  |
| access    | `all-access`       | Include all access methods                     | 
| agent     | `user`             | Only include visits from users. (Exclude bots) |


## Project scope and next steps
When deciding the initial scope of the project, some topics were left as next steps.
Many of the decision factors for these topics would require more context.
I've included a few thoughts on some of these topics.
 * Authentication / Authorization

This API is permissive, and does not attempt to implement access control. 
 * Performance / Scalability

The API was designed in a passthrough manor such that all data is gathered from the wikipedia api in real time.
This does not attempt to optimize for performance, and would be most appropriate for small call volume.
In fact, this is a great time to talk about rate limits.
As the wikipedia API has a rate limit set, this service would eventually also be impacted by that limit.

Caching could also be employed to improve performance, depending on the composition of incoming calls.
Sparse calls to information about rare articles are unlikely to benefit much,
but there is likely more performance to be gained on caching for an endpoint
like the most viewed articles for a given month.

Another way of improving performance could be to add a form of persistence.
This would involve storing the view data after it has been retrieved from the Wikipedia API.
Future calls for that information could then use the data stores, reducing the load on the Wikipedia API, and
removing the overhead of the additional HTTP requests.

 * Observability

It's important to know when something goes wrong with your service.
This implementation does not have that covered.
To operate in a production environment, adding logging would be recommended at minimum.
More optimally, integrate with other observability tools such as Kibana, Datadog and PagerDuty. 