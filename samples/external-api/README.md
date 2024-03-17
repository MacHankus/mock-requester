# Info

This api is imitating some external api which could be used in production environment.
It has two endpoints:
- /save
- /request-history

First saves request to local history and second request returns request history. 

`/save` saves its body to fake DB along with created id for request. Body is optional.

Requesting `/request-history` help us see if there was a request made by mock-requester.