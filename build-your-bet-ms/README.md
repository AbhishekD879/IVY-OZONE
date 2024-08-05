BuildYourBet (BYB) proxies some of the banach calls using **banach-api** library.
Documentation is available on <byb-host>/docs/index.html, for example:
https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/docs/index.html

Documentation is being generated during test run using Spring Rest Docs tool.

Project uses Spring Boot 2.x WebFlux to implement rest interfaces.
It's desired to use only non-blocking and async operations in this microservice.
Banach-api library, for example, uses Spring's async WebClient to call Banach apis.

More info on banach integration: https://confluence.egalacoral.com/display/SPI/Banach+Integration
