# **EchoSentiment**

###Discaimer: These instructions have been revised with the assistance of AI for clarity.###

## **Twitter API Requirements**  

To query the **Twitter API**, you must first obtain and allocate a **Bearer Token** to the environment variable `TWITTER_BEARER_TOKEN`.  

A bearer token can be obtained via the **X Development Portal** after creating a developer account at [https://developer.x.com/en/portal/dashboard](https://developer.x.com/en/portal/dashboard).  

### **Setting Up the Bearer Token (select one method)**  

#### **Globally (System-Wide)**  
On **Mac/Linux**, open a terminal and run:

export TWITTER_BEARER_TOKEN="your_bearer_token_here"

On Windows (PowerShell):
$env:TWITTER_BEARER_TOKEN="your_bearer_token_here"

#### ##In PyCharm##
Go to Run → Edit Configurations.
Under Environment Variables, add:

TWITTER_BEARER_TOKEN=your_bearer_token_here

Click OK and Apply.

## **META API Requirements**  
To query the Meta API, you must first obtain and allocate an **Access Token** to the environment variable 'META_ACCESS_TOKEN'.

An access token can be obtained via the Meta Development Portal after creating a developer account at [https://developers.facebook.com/](https://developers.facebook.com/).

You will then need to create an empty/example application to generate an access token. After that, navigate to the Graph API Explorer and select the following permissions (not yet determined), then generate an API key.

To assign an environment variable, follow the same steps as in Twitter API Requirements above, replacing TWITTER_BEARER_TOKEN with META_ACCESS_TOKEN.

