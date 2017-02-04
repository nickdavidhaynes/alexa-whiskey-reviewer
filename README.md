# Alexa Whiskey Advisor

This project contains a sample project that shows how easy it is to use the Alexa service and AWS Lambda to create an Alexa skill. Basically, if you can write a Python function (or Node or C#, I guess), you can make a skill.

## Overview

The architecture of a skill looks something like this:

![](images/alexa_architecture.png)

The physical Echo/Dot device is really nothing more than a speaker, microphone, and wifi transmitter. The speaker listens constantly for the "Alexa" keyword. When it hears someone say "Alexa", it begins listening to what they say. A single statement is called an utterance. Each utterance should contain several parts:

- "Alexa" start word
- The invocation name of the skill you want to use
- The intent to pass to the skill
- "Slot" data that contextualizes the intent.

With the whiskey advisor, we will create a skill with the invocation name "whiskey advisor". We will then create a single intent, "get_review", that can be invoked by saying things like "tell me about {some whiskey}" or "how is {some whiskey}". Putting it all together, a sample utterance might be: "Alexa, ask whiskey advisor to tell me about Talisker 10." In this case, "whiskey advisor" is the invocation name, "tell me about" defines the intent of the question, and "Talisker 10" is a wildcard slot that is filled with the particular whiskey you want to hear about.

Once the devices captures an utterance, it sends the raw audio file to the Alexa cloud service. This is where much of the magic happens - the service translates the audio into text data, parses out the intent (if any valid one was provided), and extracts the values for the slot variables. In the case of the utterance above, the output from the Alexa service is json that looks like this:

```
{
  "session": {
    "sessionId": "XXXXXXXXXXXX",
    "application": {
      "applicationId": "XXXXXXXXXXXX"
    },
    "attributes": {},
    "user": {
      "userId": "XXXXXXXXXXXX"
    },
    "new": true
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "1234567890",
    "locale": "en-US",
    "timestamp": "2017-02-04T19:13:58Z",
    "intent": {
      "name": "GetReview",
      "slots": {
        "dram": {
          "name": "dram",
          "value": "talisker 10"
        }
      }
    }
  },
  "version": "1.0"
}
```

The skill creator then builds a custom web service that consumes this json data and spits out the text for Alexa to recite back. In this case, we would want the text to be: "The Talisker 10 is a respectable dram, with an average rating of 87. It's also an average-priced bottle at $59 for a fifth."

## Building the Lambda service

We'll use AWS Lambda to create the service that builds our output responses. Lambda AWS's serverless architecture platform - basically, you load a simple script into the service, and whenever the service endpoint is hit, your script is run against the input data. For small projects, this can be quite a bit cheaper and easier than managing a server. You also get a million free Lambda calls with the AWS free tier.

If you don't already have an AWS account, create a new one. Make sure you're in the Northern Virginia region - as of Feb 2017, this is the only region hosting the Alexa service.

From the AWS console, go to the Lambda dashboard. On the `Functions` tab, there should be a button for creating a new Lambda. Use the blank template, and select "Alexa Skills Kit" as the trigger. Give your Lambda a name and description and choose Python as the run time.

You'll then see an editor that allows you to type in code. Click the drop-down and choose "upload a .zip" instead. From this directory, zip together the `lambda_function.py` script with the `whiskey_data.json` file and upload this zip to the Lambda.

In the "Lambda function handler and role" box, make sure handler is set to "lambda_function.lambda_handler". This points the Lambda to the `lambda_handler` function contained in the `lambda_function.py` script you just uploaded. Choose to create a custom role for the Lambda, and click "Allow" on the default settings it assigns.

The rest of the settings can be left on their defaults for now, so confirm your work and create the function.

## Building the Alexa skill

Now that we have a Lambda to handle our Alexa requests, let's create the skill itself.
