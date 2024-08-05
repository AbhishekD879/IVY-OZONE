
**Running:**

./gradlew bootRun

**Endpoints:**

DEV2 Featured:
- https://coral-featuredms-dev2.symphony-solutions.eu:8446/health
- wss://coral-featuredms-dev2.symphony-solutions.eu
DEV2 Inplay:
- https://coral-inplay-publisher-dev2.symphony-solutions.eu:8443/health
- wss://coral-inplay-publisher-dev2.symphony-solutions.eu

###DEV0 Inplay:
- https://coral-inplay-publisher-dev0.symphony-solutions.eu:8443/health
- wss://coral-inplay-publisher-dev0.symphony-solutions.eu

###DEV0 Featured:
- https://oxyms-dev.symphony-solutions.eu:8446/health
- wss://oxyms-dev.symphony-solutions.eu

###InPlay Ping
`curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: coral-inplay-publisher-dev2.symphony-solutions.eu" -H "Origin: 127.0.0.1" https://coral-inplay-publisher-dev2.symphony-solutions.eu/websocket/?transport=websocket&EIO=3`

###Featured Ping
`curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: oxyms-dev.symphony-solutions.eu" -H "Origin: 127.0.0.1" https://oxyms-dev.symphony-solutions.eu/socket.io/?module=featured\&EIO=3\&transport=websocket`
