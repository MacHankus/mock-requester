# Info

This samples show how mock-requester works. Examples are prepared in such way that you can observe how mock-requester is able to call external apis during handling own request and how it works with given configuration file.

Here you can find three applications:
- **external-api** exposes two endpoints: 
    - /save
    - /request-history.
  
  Basically `/save` endpoint saves some data to request history and `/request-history` provides that history. So if you call `/save` 2 times you will see 2 requests in history.
- **external-api-second** - same as **external-api** , just another instance
- **client** makes request to mock-requester
- **mock-requester** actual application that we want to test

# How to use it
There are different scenarios available and reqdy to use. Each scenario has its own configuration file, and docker-compose file.

Before running sample project you can choose scenario you want to run. Then you just need to run it like a normal docker-compose file.

```
cd samples && docker-compose -f docker-compose.${docker-compose-scenario-name}.yaml up
```

# Scernarios

All scenarios are placed in `samples` folder to show you how the tool works. Every scenario has own configuration file and docker-compose file.
Here is a description for few scenarios you can create with mock-requester.

### Simple request

#### Description

`Client` is an appication that makes request to mock-requester. Mock-requester is configured such way that it calls some external api during `Client's` call.

`Cient` makes request under `/request-history` to show there is nothing in history yet. Then it calls mock-requester and after that it makes another call to `request-history` to show there was a call made by mock-requester to external-api. We can see that a request was made by mock-requester.

#### Config
File: `simple-request.yaml`

[config file](../samples/simple-request.yaml)

[compose file](../samples/docker-compose.simple-request.yaml)

```
simple-request:
  incoming: 
    type: http
    path: collect
  side_effects:
    type: http
    url: "http://external-api:8000/save"
    method: post
    headers: 
      Content-Type: application/json
```

This config force mock-requester to :
   - catch requests to endpoint `/collect`
   - while handling the request mock-requester calls `http://external-api:8000/save` with given headers with `POST` method

### Simple request with placeholder pointing to request's body that client has sent

#### Description

`Client` makes request to mock-requester. Mock-requester is configured such way that it calls some external api during `Client's` call.

Firstly it makes request under `/request-history` to show there is nothing in history yet. Then it calls mock-requester with payload :
```
   {
      "givenKey": "GIVEN_KEY_VALUE"
   }
``` 
After that it makes another call to `request-history` to show there was a call made by mock-requester to external-api. We can see that a request was made by mock-requester to external api with payload `{"sent-key": "GIVEN_KEY_VALUE"}`. 

#### Config
File: `simple-request-with-placeholder.yaml`

[config file](../samples/simple-request-with-placeholder.yaml)

[compose file](../samples/docker-compose.simple-request-with-placeholder.yaml)


```
simple-request-with-placeholder:
  incoming: 
    type: http
    path: collect
  side_effects:
    type: http
    url: "http://external-api:8000/save"
    method: post
    payload:
      sentKey: ${BODY.givenKey}
    headers: 
      Content-Type: application/json
```

This config force mock-requester to :
   - catch requests to endpoint `/collect`
   - while handling the request mock-requester calls `http://external-api:8000/save` with given headers with `POST` method and given payload `{"sentKey": "${BODY.givenKey}"}`. `${BODY.givenKey}` placeholder will be replaced by value given in payload of client's call to mock-requester.
  

### Request chain with values from previous side effects

#### Description

`Client` makes request to mock-requester. Mock-requester is configured such way that it calls two separate external apis. Second call is based on first calls' response.

`Client` firstly makes request under `/request-history` to both external apis to show there is nothing in history yet. Then it calls mock-requester under `/collect` endpoint. Mock requester knows from configuration that it should make two request to `external-api` and `external-api-second`. You can see that second call will use response of first call. Inside second's call payload you can see placeholder `{ idReturnedByFirstSideEffectWas: ${SIDE_EFFECT[0].payload.request_id} }`. It means that second call expects key `request_id` from first's call response payload and placeholder will be replaced by its value.

#### Config
File: `request-chain-with-values-from-side-effects.yaml`

[config file](../samples/request-chain-with-values-from-side-effects.yaml)

[compose file](../samples/docker-compose.request-chain-with-values-from-side-effects.yaml)
```
request-chain-with-values-from-side-effects:
  incoming: 
    type: http
    path: collect
  side_effects:
    -
      type: http
      url: "http://external-api:8000/save"
      method: post
      headers: 
        Content-Type: application/json
    -
      type: http
      url: "http://external-api-second:8000/save"
      method: post
      payload:
        idReturnedByFirstSideEffectWas: ${SIDE_EFFECT[0].payload.request_id}
      headers: 
        Content-Type: application/json
```

This config force mock-requester to :
   - catch requests to endpoint `/collect`
   - while handling the request mock-requester it calls `http://external-api:8000/save` with given headers with `POST`
   - after first request to external-api was made mock-requester makes another request to second external-api with paylaod `{ idReturnedByFirstSideEffectWas: ${SIDE_EFFECT[0]} }` but the placeholder will be replaced by value returned by first external-api. Request will be made with same method and headers as first request according to config