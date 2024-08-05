import { PrivateMarketsService } from './private-markets.service';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('PrivateMarketsService', () => {
  let service: PrivateMarketsService;

  let eventService;
  let templateService;
  let pubSubService;
  let liveServConnectionService;
  let nativeBridgeService;
  let bppService;
  let userService;
  let siteServerRequestHelperService;

  const accountFreebetsResponse = {
    response: {
      model: {
        currency: '$',
        freebetToken: [{
          freebetTokenRestrictedSet: {
            id: '123456'
          }
        }],
        token: '',
      },
      version: '1.0'
    }
  };

  const ssMarkets = {
    SSResponse: {
      children: []
    }
  };
  beforeEach(() => {
    eventService = {
      cachedEventsByFn: (callback: Function) => {
        return () => of(callback());
      }
    };
    templateService = {
      filterBetInRunMarkets: jasmine.createSpy().and.returnValue([])
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    liveServConnectionService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({})),
      disconnect: jasmine.createSpy('disconnect'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    nativeBridgeService = {
      arePrivateMarketsAvailable: jasmine.createSpy()
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of(accountFreebetsResponse))
    };
    userService = {};
    siteServerRequestHelperService = {
      getEventsByMarkets: jasmine.createSpy().and.returnValue(Promise.resolve(ssMarkets))
    };
    service = new PrivateMarketsService(
      eventService,
      templateService,
      pubSubService,
      liveServConnectionService,
      nativeBridgeService,
      bppService,
      userService,
      siteServerRequestHelperService,
    );
  });

  function createService() {
    service = new PrivateMarketsService(
      eventService,
      templateService,
      pubSubService,
      liveServConnectionService,
      nativeBridgeService,
      bppService,
      userService,
      siteServerRequestHelperService,
    );
  }

  describe('cache markets', () => {
    it('should subscribe to store markets', () => {
      pubSubService.subscribe.and.callFake((file, method, cb) => {
        if (method === 'STORE_PRIVATE_MARKETS') {
          const privateMarketsMock = [];
          cb(privateMarketsMock);
        }
      });

      createService();

      expect(service.storedPrivateMarkets).toBeDefined();
    });


    it('should subscribe and remove store markets on logout', () => {
      pubSubService.subscribe.and.callFake((file, method, cb) => {
        if (method === 'STORE_PRIVATE_MARKETS') {
          const privateMarketsMock = [];
          cb(privateMarketsMock);
        }
        if (method === pubSubService.API.SESSION_LOGOUT || method === pubSubService.API.BETS_COUNTER_PLACEBET) {
          service.storedPrivateMarkets = [];
          cb();
        }
      });

      createService();

      expect(service.storedPrivateMarkets).not.toBeDefined();
    });
  });

  it('disconnect', () => {
    service.disconnect();

    expect(liveServConnectionService.disconnect).toHaveBeenCalledTimes(1);
  });

  it('subscribe', fakeAsync(() => {
    const events = <any>[{
      liveServChannels: 'sEVMKT0141932894'
    }];
    service.subscribe(events);

    tick();
    expect(liveServConnectionService.subscribe).toHaveBeenCalledTimes(1);
  }));

  it('unsubscribe', () => {
    const events = <any>[{
      liveServChannels: 'sEVMKT0141932894'
    }];
    service.unsubscribe(events);

    expect(liveServConnectionService.unsubscribe).toHaveBeenCalledTimes(1);
  });

  it('privateMarketsUpdateHandler', () => {
    const update = <any>{
      type: 'MESSAGE',
      channel: {
        name: 'channel',
        id: 2
      },
      event: {
        id: 1
      },
      subChannel: {
        type: 'a'
      }
    };
    service['privateMarketsUpdateHandler'](update);

    expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_SERVE_MS_UPDATE', jasmine.any(Object));
  });

  it('normalizeData', () => {
    const freebets = <any>[
      {
        freebetOfferName: 'freebetOfferName1',
        freebetTokenId: 1,
        freebetTokenRestrictedSet: {
          id: 2
        }
      }
    ];
    const markets = <any>{
      SSResponse: {
        children: [
          {
            event: {
              children: [
                {
                  market: {
                    name: 'market1',
                    id: 2,
                    children: [
                      {
                        outcome: {}
                      }
                    ]
                  }
                },
                {
                  market: {
                    name: 'market1',
                    id: 1,
                    children: [
                      {
                        outcome: {}
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    };

    expect(service['normalizeData'](freebets, markets)[0].markets[0]['freebetTokenId']).toEqual(1);
  });

  it('get markets when we have cache defined', fakeAsync(() => {
    service.storedPrivateMarkets = [{
      freebetTokenRestrictedSet: {
        id: 123456
      }
    }] as any;

    service.markets();
    expect(bppService.send).not.toHaveBeenCalled();
    tick();
    expect(siteServerRequestHelperService.getEventsByMarkets).toHaveBeenCalledWith({
      marketIds: [
        123456
      ],
      simpleFilters: 'includeRestricted=true&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A'
    });
  }));

  it('markets', () => {
    service.markets().subscribe(() => {
      expect(bppService.send).toHaveBeenCalledTimes(1);
      expect(bppService.send).toHaveBeenCalledWith('privateMarkets');
      expect(siteServerRequestHelperService.getEventsByMarkets).toHaveBeenCalledWith({
        marketIds: [
          123456
        ],
        simpleFilters: 'includeRestricted=true&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A'
      });
    });
  });

  it('getPrivateMarkets catch', fakeAsync(() => {
    bppService.send = jasmine.createSpy('privateMarkets').and.returnValue(throwError(''));

    createService();
    service.markets().subscribe(
      () => {},
      () => {
        expect(nativeBridgeService.arePrivateMarketsAvailable).toHaveBeenCalledWith(false);

      }
    );

    flush();
  }));

  it('getPrivateMarkets should not request events if no tokens come from BPP', fakeAsync(() => {
    bppService.send = jasmine.createSpy('privateMarkets').and.returnValue(of({
      response: {
        model: {}
      }
    }));

    createService();
    spyOn(service, 'getPrivateMarketsEvents' as any).and.callThrough();

    service.markets().subscribe(() => {
      expect(service['getPrivateMarketsEvents']).not.toHaveBeenCalled();
    });

    flush();
  }));

  it('getPrivateMarketsEvents send native event without events', fakeAsync(() => {
    eventService.cachedEventsByFn = (callback: Function) => {
      return () => Promise.resolve(null);
    };

    createService();
    service.markets().subscribe(() => {
      expect(nativeBridgeService.arePrivateMarketsAvailable).toHaveBeenCalledWith(false);
    });

    flush();
  }));

  it('getPrivateMarketsEvents send native event', fakeAsync(() => {
    eventService.cachedEventsByFn = (callback: Function) => {
      return () => Promise.resolve([]);
    };

    createService();
    service.markets().subscribe(() => {
      expect(nativeBridgeService.arePrivateMarketsAvailable).toHaveBeenCalledWith(false);
    });

    flush();
  }));

  it('getDetailedPrivateBets negative condition', fakeAsync(() => {
    siteServerRequestHelperService.getEventsByMarkets = jasmine.createSpy('getEventsByMarkets').and.returnValue(throwError({}));
    createService();
    service['getTokensIds'] = jasmine.createSpy().and.returnValue([1]);
    service['getDetailedPrivateBets']([]);

    tick();
    expect(siteServerRequestHelperService.getEventsByMarkets).toHaveBeenCalled();
  }));
});
