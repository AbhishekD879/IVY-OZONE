# QuickBet (RemoteBetslip) microservice
QuickBet microservice (QB) allow Front End (FE) clients to place single bets in one go, without adding them to traditional betslip. All communication are done using socket.io (built on top of websockets, supports long polling as backup option)

## Establishing new session
Any communication between FE and QB is done in session scope.
Establishing new connection between FE and QB will create new session in QB for that particular client.

On new client connection event, QB will send back message '30000' with data: {id: string}, where id is session id.

To reconnect to the same session (after loosing connection, for example), FE client should add single query parameter to connection url: ?id=string, where id is the session id.

Every connection request without 'id' in query parameter will create a new session.

QB will return error message on any action requested by client that has not established session yet.

## YourCall Bets workflow
### Adding YourCall Selection
Adding YourCall selection starts off continious polling of DigitalSport's (DS) odds/calculate API, that returns odds for given selection. Whenever odds change is detected, new odds will be broadcasted to clients subscribed to the same YourCall selection. In case of any error (timeout, DS error), client will be notified about it and polling will be stopped.

![](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgUUIgQWRkIFlvdXJDYWxsIFNlbGVjdGlvbgpGRS0-UUI6IHsnNDAwMDEnLCB7Li4ufX0KbG9vcCAKICAgIG5vdGUgb3ZlciBRQixEUzogaW4gdGhyZWFkIHBvb2wAHwVRQi0-K0RTOiBvZGRzL2FjY3VtdWxhdG9yLWNhbGN1bGF0ZQBHBURTLT4tUUIAIgYKZW5kCgphbHQgc3VjY2VzcwBCCUZFAIENBTEAgQYMIAoAgQkFb3B0IGlmAGMFIGNoYW5nZWQAgSEFACkSMwCBQwogICAgZW4AIwZvcHQgZXJyb3IAgT4KAIE-CQBuEjQAMxJlbHNlADwGAIEdEzIAgjgKAIFZBQ&s=rose)

**Messages:**

* '40001' (add yourcall selection):

~~~
{
  "events": [
    {
      "betType": 1,
      "conditionType": 2,
      "conditionValue": 3,
      "game1Id": 321,
      ..
      "game4Id": 786,
      "player1Id": 123,
      ..
      "player4Id": 456,
      "statisticId": 41
    }
  ]
}
~~~

It's possible to add more than one selection to **events** array - in that case, FE will receive odds for the whole accumulator

* '41001' (response after adding yourcall selection):

~~~
  {
    "roomName":"b515823f1c92d89e9c9c2e05c1bf42e3f4c62d38",
    "data": {
      "odds": "50"
      }
  }
~~~
**roomName** - is the socket.io room name where QB will send broadcast message about odds change. It is also uniquely indentifies YourCall selection

**data** - contains initial odds calculated by QB

* '41002' (error on initial request to DS's odds/change)

  * DS Error:

  ~~~
  {
      code: 5xx, // where xx is DS error code
      message: <message_from_DS>
  }
  ~~~

  * Time out to DS:

  ~~~
  {
      code: 402,
      message: "Timeout on calculating YourCall initial odds"
  }
  ~~~

  * Any other error:

  ~~~
  {
      code: 4,
      message: "Internal error while adding YourCall selection"
  }
  ~~~

  * Validation error (missing required field or similiar):

  ~~~
  {
      code: 4,
      message: "Should be at least one player market selection"
  }
  ~~~

* '41003' (odds change message)

~~~
  {
    "odds": "2.5"
  }
~~~

* '41004' (error in odds/change polling routine)

  * DS error:

  ~~~
      {
          code: 401,
          message: "Error returned in YourCall live odds calculation"
      }
  ~~~

  * Time out to DS:

  ~~~
      {
          code: 403,
          message: "DS timed out in YourCall live odds calculation"
      }
  ~~~

### Placing YourCall Bet (SGL only)
When YourCall place bet is issued, QB will fetch oxiToken and sprotbookUser from BetPlacement Proxy (BPP).
Then it will call DigitalSport's (DS) /bets/create api for bet creation. In turn, DS will place manual bet to OpenBet (OB) and will return raw OB response to QB (be it success or error) along with the rest of the data.

NOTE: If OpenBet returns bet error, it will be returned to FE with succesful message, but json will contain 'betError' array with OB's errors.

![](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgUUIgUGxhY2UgWW91ckNhbGwgQmV0CgpGRS0-UUI6IHsnNDAwMTEnLCB7Li4ufX0KUUItPitCUFA6IC9Qcm94eS9hdXRoL3VzZXJkYXRhIHticHBUb2tlbn0KQlBQLT4tAEAFb3hpABAFLCBzcG9ydHNib29rVXNlcn0KYWx0IGJwcCBlcnJvcgogICAgUUItPkZFAHUFMTEwMgBwCmVuZAB4BkRTOiBiZXRzL2NyZWF0ZQpEUwBgCC4uLgBNBnN1Y2Nlc3MAPhMAgUALICAgIG5vdGUgcmlnaHQgb2YgRkUAfgUgICAgSWYgT3BlbkJldCByZXR1cm5lZCBiZXQAgSMGLAAeCWl0IHdpbGwgYmUgcHJlc2VudGVkIHRvIGNsaWVudCBpbiAiYmV0RXJyb3IiIGZpZWxkADEKbiBtZXNzYWdlIACBEwcgKACBMQcpAIIFBWVuZACBGwUKZWxzZQCBeigK&s=rose)

**Messages:**

* '40011' (Place YourCall Bet):

~~~
{
    "amount": 123,
    "freebet": {
      "id": 123,
      "stake": "2.25"
    },
    "token": "xxx",
    "currency": "USD",
    "odds": "2.5",
    "events": [
        {
            "conditionType": 3,
            "conditionValue": 2,
            "game1Id": 123,
            "game2Id": 123,
            "game3Id": 123,
            "game4Id": 123,
            "player1Id": 123,
            "player2Id": 123,
            "player3Id": 123,
            "player4Id": 123,
            "statisticId": 41,
            "betType": 1
        }
    ]
}
~~~

* '41101' (Message about successfull bet placement):
  * Success:

  ~~~
  {
      "data": {
          "dsBetId": 123,
          "obBetId": 123,
          "receipt": "123",
          "numLines": 1,
          "totalStake": "10",
          "currency": "USD",
          "odds": "2.5",
          "isAccumulator": false,
          "dateCreated": "2017-11-04 12:30:00",
          "event": [
                  {
                      "id": 163449,
                      "type": 1,
                      "statistic": {
                        "id": 41,
                        "title": "Assists",
                        "phraseTitle": [
                          "assist",
                          "assists"
                        ],
                        "value": 2,
                        "condition": 3
                      },
                      "settlement": {
                        "result": "Pending",
                        "voidReason": null,
                        "value": [
                          0
                        ]
                      },
                      "player1": {
                        "id": 141300,
                        "name": "Ryan Shawcross"
                      },
                      "team1": {
                        "id": 4633,
                        "title": "Stoke City",
                        "abbreviation": "STK"
                      },
                      "game1": {
                        "id": 84409,
                        "date": "2017-11-04 12:30:00",
                        "status": 1,
                        "sportId": 1,
                        "homeTeam": {
                          "id": 4633,
                          "title": "Stoke City",
                          "abbreviation": "STK"
                        },
                        "visitingTeam": {
                          "id": 4626,
                          "title": "Leicester City",
                          "abbreviation": "LEI"
                        }
                      },
                      "odds": "50"
              }
          ],
          betError: []
      }
  }
  ~~~

  * When OB returned bet error:

  ~~~
  {
      data: {
          betError: [
              {
                  betFailureCode: 554,
                  betFailureKey: "bet.invalidChannel",
                  betFailureReason: "invalid channel specified",
                  betFailureDebug: "source should only be 1 character long",
              }
          ]
      }
  }
  ~~~

* '41102' (Message about error during bet placement to DS/OB):

  * In case of DS errors (see DigitalSports documentation for codes description):

  ~~~
  {
      code: 5xx, // where xx is DS error code
      message: <message_from_DS>
  }
  ~~~

  * In case of authentication problems (on BPP or OB sides):

  ~~~
  {
      code: “UNAUTHORIZED_ACCESS”,
      description: “Token expired or user does not exist”
  }
  ~~~

  * In case of timeouts, connectivity issues or other unexpected errors with BPP, DS or OB:

  ~~~
  {
      code: "INTERNAL_PLACE_BET_PROCESSING",
      description: <some basic error decription, typicall exception message>
  }
  ~~~

## QA Endpoints (not available on prod and HL)
* **/qa/attachedSessions** - shows active sessions (where client is connected). Key is socket.io client id, value is session itself.
* /qa/sessions - shows all sessions in redis
* **/qa/yc/liveOdds** - show current subscriptions to odds changes from DS
* **/qa/yc/triggerOddsChange/[session_id]?odds=1.5** - makes QB send clients the same message as like it was odds change (altough it is not real odds change from DS). If **odds** query parameter is omiited, QB will generate random value. **session_id** is the QB's session id (no socket.io client id)

**NOTE:** APIs marked as bold are node-specific. Because QB Microservice can have multiple instance, request can route to one or another, resulting in different output. Altough triigerOddsChange api takes session_id, which shared across all instances, subscription to DS's odds changes still can be done in different instance. That's why it's also instance-dependent.
