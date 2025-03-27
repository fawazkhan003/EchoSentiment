# EchoSentiment

**Twitter API requirements**

To query the twitter API you must first obtain and allocate a bearer token to the environment variable "TWITTER_BEARER_TOKEN". 

A bearer token can be obtained via the x development portal after creating a developer account at https://developer.x.com/en/portal/dashboard.

To assign an environment variable globally:

On Mac/Linux, open a terminal and run:

export TWITTER_BEARER_TOKEN="your_bearer_token_here"

On Windows (PowerShell):

$env:TWITTER_BEARER_TOKEN="your_bearer_token_here"

OR

To assign an environment variable in PyCharm: 

Go to Run → Edit Configurations

Under Environment Variables, add:

TWITTER_BEARER_TOKEN=your_bearer_token_here

