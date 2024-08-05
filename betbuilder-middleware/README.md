# Betbuilder-Middleware #

##  Quick summary ##

  This is a spring boot application which acts as a proxy between SportsBook and PricingGateway to fetch aggregated price for
  BYB selections while doing buildBet and placeBet transactions for BetBuilder bets.

## Prerequisites ##

    - JDK 17 installation
    - Redis installation

## How do I get set up? ##

    - Clone the project using below link
      git clone git@bitbucket.org:symphonydevelopers/betbuilder-middleware.git
    - Open the project in any IDE and run the Application.

## API's available in this microservice ##
  1. http://localhost:9090/price
     - This endpoint will be called internally from Betting-MS to fetch aggregated price from
       PricingGateway while doing buildBet transaction for Betbuilder bets.
     - Sample Request:
       {"batchId":"Timestamp: 1715163515451","combinations":[{"id":"f7ef1cc8-dc2c-5174-b792-c06666505396----2:9169149","sportId":4,"oEId":"14902400","selections":[{"fixtureId":"2:9169149","marketId":71999487,"optionId":325382158},{"fixtureId":"2:9169149","marketId":71998807,"optionId":325380123}]},{"id":"f7ef1cc8-dc2c-5174-b792-c06666505398----2:9184869","sportId":4,"oEId":"14918088","selections":[{"fixtureId":"2:9184869","marketId":72258012,"optionId":326492859},{"fixtureId":"2:9184869","marketId":72258017,"optionId":326492920}]},{"id":"f7ef1cc8-dc2c-5174-b792-c066665053960----2:9169149","sportId":4,"oEId":"14902400","selections":[{"fixtureId":"2:9169149","marketId":71999487,"optionId":325382160},{"fixtureId":"2:9169149","marketId":71998807,"optionId":325380123}]}]}
  2. http://localhost:9090/checkPrice
     - This endpoint is used by OpenBet for them to validate the price we are sending for betBuilder bets in placeBet requests.
     - Sample Request:
       {"transId":"123","combinations":[{"bbHash":"374443B4ABF98D75C95A9F374ABAD5CB560523E78B91C3BA069CF465CC6DE424"}]}
