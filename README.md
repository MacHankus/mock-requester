# Why
Idea for the project was simple. 
If you have test environment that relys on external api and you dont want to write your own mock-api to imitate external api on test environment you can use this project as your mock-api. 

Sometimes external apis are more complex; for example external api needs to call an endpoint from your application and then it return some result or even external api needs to call few other external or internal apis to collect some data and return some data based on it. Mock-requester is able to collect every response and every next call is able to use data returned by previous calls.

# Flowchart

![flowchart](docs/images/mock-requester-flowchart.jpg?raw=true)

# Instrukcja użycia 
Main object inside mock-requester application is configuration file called **config.yaml**. Application use this file to get knowladge about what to do when something is calling mock-requester.
This file is directly maintained by the user of mock-requester.

Confugiration file is built from segments:
```
mock-external-weight-api: # Block name for readability
  incoming: 
    type: http
    path: do/something/under/this/path # endpoint path that will be used by mock-requester as an entry. In given example mock-requester will listen to every request under this path : [POST] http://localhost:8000/do/something/under/this/path
  side_effects: # list (or single item) of side effects. This side effects represents calls to some external applications.
    type: http
    url: "http://external-api:9006/start/doing/external/things" # url that will be used 
    method: post # for now allowed methods are POST, GET, PUT, DELETE, PATCH 
    payload: # optional dict with values
      id_route: ${BODY.idRoute} # you can use placeholders like ${BODY.some_key_from_body}, ${SIDE_EFFECT[1].key_from_payload_returned_from_second_call}
      type_route: ${typeRoute}
      result: 1
      weight: 4
    headers: 
      Content-Type: application/json

```

Important details:
- side_effects could be array or single object
- payload section of every side_effect can hold placeholders that refferences to body of client's request or responses from previous calls (if side_effects is array)

# Samples
There are scenarios prepared to see how mock-requester works. Scenarios are placed in [this direction](samples) and there is [readme file](samples/README.md) that describes every scenario and how it works.