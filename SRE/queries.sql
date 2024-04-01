# Some queries you can run in monitoring

# searching for error messages
_sourceCategory=your_source_category "ERROR" OR "Exception"

# looking for http status code
_sourceCategory=your_source_category status>=400

#latency
_sourceCategory=your_source_category | parse "response_time=*ms" as response_time | where response_time > 1000
