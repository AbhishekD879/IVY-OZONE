import { fakeAsync, flush, tick } from '@angular/core/testing';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { from as observableFrom, of, throwError } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FreeBetsService } from '@core/services/freeBets/free-bets.service';
import { mockedFreeBets } from '@core/services/freeBets/free-bets.mock';

describe('FreeBetsService', () => {
  let service: FreeBetsService;
  let siteServer;
  let extensionsStorage;
  let user;
  let pubsub;
  let storage;
  let session;
  let time;
  let bpp;
  let nativeBridge;
  let dialog;
  let routingHelper;
  let filters;
  let locale;
  let sportsConfigHelperService;
  let device;
  let event;
  let initState;
  let now;
  let logoutCb;
  let pubsubStoreCb;
  let storeFreeebetsCallback;

  beforeEach(() => {
    now = new Date();
    siteServer = {
      getData: jasmine.createSpy('getData'),
      getCategories: jasmine.createSpy('getCategories')
    };
    extensionsStorage = {
      getList: jasmine.createSpy('getList')
    };

    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId').and.returnValue(of('americanfootball'))
    };

    user = {
      status: true,
      username: 'test',
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false),
      currencySymbol:'$'
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName, channel, channelFunction) => {
        if (channel === 'SESSION_LOGOUT') {
          logoutCb = channelFunction;
        } else if (channel === 'STORE_FREEBETS') {
          pubsubStoreCb = channelFunction;
        } else if (channel === pubSubApi.STORE_FREEBETS_ON_REFRESH) {
          storeFreeebetsCallback = channelFunction;
        }
      }),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    initState = JSON.stringify([{
      freebetTokenId: '12',
      freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
      freebetOfferName: 'testOffer',
      freebetTokenValue: 300,
      tokenPossibleBet: {
        betId: '12',
        betLevel: 'EVENT'
      }
    }]);
    storage = {
      get: jasmine.createSpy().and.returnValue(initState),
      set: jasmine.createSpy(),
      remove: jasmine.createSpy(),
      getCookie: jasmine.createSpy().and.returnValue(true)
    };
    session = {
      whenProxySession: jasmine.createSpy().and.returnValue(
        new Promise<void>(function(resolve) {
          resolve();
        }))
    };
    time = {
      compareDate: jasmine.createSpy('compareDate'),
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('time string'),
      parseDateTime: jasmine.createSpy('formatByPattern'),
      daysDifference: jasmine.createSpy('daysDifference'),
      isInNext24HoursRange: jasmine.createSpy('isInNext24HoursRange').and.returnValue(false),
      parseDateInLocalFormat: jasmine.createSpy('parseDateInLocalFormat').and.returnValue(now)
    };
    bpp = {
      send: jasmine.createSpy().and.returnValue(observableFrom([{
        response: {
          model: {
            freebetToken: [{
              freebetTokenExpiryDate: '1',
              freebetTokenId: '12',
              tokenPossibleBet: {
                betId: null,
                betLevel: 'EVENT'
              }
            }]
          }
        }
      }]))
    };
    nativeBridge = {
      onFreeBetUpdated: jasmine.createSpy()
    };
    dialog = {
      openDialog: jasmine.createSpy('openDialog').and.callFake((dialogName, component, closeOther, params) => {
        params.onBeforeClose();
      })
    };
    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('testUrl')
    };
    filters = {
      currencyPosition: jasmine.createSpy().and.returnValue('$300')
    };
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test')
    };
    device = {
      isDesktop: false
    };
    event = {
      cashoutAvail: 'test',
      categoryCode: 'test',
      categoryId: '12',
      categoryName: 'test',
      comments: {
        teams: {
          player_1: {
            id: '1'
          }
        }
      },
      displayOrder: 1,
      drilldownTagNames: 'test',
      eventIsLive: false,
      eventSortCode: 'test',
      eventStatusCode: '1',
      id: 12,
      isStarted: false,
      isUS: false,
      liveServChannels: 'ch.com',
      liveServChildrenChannels: 'ch.com',
      liveStreamAvailable: false,
      markets: [],
      marketsCount: 0,
      name: 'test',
      originalName: 'test',
      responseCreationTime: '0.04s',
      racingFormEvent: {
        class: ''
      },
      startTime: '12:00',
      streamProviders: {
        AtTheRaces: false,
        IMG: false,
        Perform: false,
        RPGTV: false,
        RacingUK: false,
        iGameMedia: false
      },
      svgId: '12',
      typeId: '4',
      typeName: 'event',
      outcomeId: 12
    };

    spyOn(console, 'info');

    service = new FreeBetsService(
      siteServer,
      extensionsStorage,
      user,
      pubsub,
      storage,
      session,
      time,
      bpp,
      nativeBridge,
      dialog,
      routingHelper,
      filters,
      locale,
      device,
      sportsConfigHelperService
    );

    spyOn(service, 'store').and.callThrough();
  });

  describe('constructor', () => {
    it('with free bets', () => {
      expect(service['freeBetsState']).toBeDefined();
      expect(pubsub.subscribe).toHaveBeenCalledWith('freeBetsFactory', pubsub.API.SESSION_LOGOUT, jasmine.any(Function));
      expect(service['freeBetsState'].available).toBeTruthy();
      expect(nativeBridge.onFreeBetUpdated).toHaveBeenCalledWith(true, jasmine.any(Array));
    });

    it('with callbacks', () => {
      const syncData = {
        data: [
          { tokenId: 1 },
        ],
        isPageRefresh: false
      };
      pubsubStoreCb(syncData);
      pubsub.subscribe.and.callFake((name, listeners, handler) => handler('someData'));
      expect(service['freeBetsState'].available).toBeTruthy();
      expect(nativeBridge.onFreeBetUpdated).toHaveBeenCalledTimes(2);
      expect(service.store).toHaveBeenCalledWith('test', syncData as any, false);
    });

    it('with callbacks and no data', () => {
      pubsubStoreCb();
      expect(service['freeBetsState'].available).toBeTruthy();
      expect(nativeBridge.onFreeBetUpdated).toHaveBeenCalledTimes(1);
      expect(service.store).not.toHaveBeenCalled();
    });
  });

  it('with SESSION_LOGOUT', () => {
    service['onFreeBetUpdated'] = jasmine.createSpy();
    logoutCb();
    expect(service['freeBetsState'].available).toBeFalsy();
    expect(service['freeBetsState'].data).toEqual([]);
    expect(service['onFreeBetUpdated']).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.NOTIFICATION_HIDE);
  });

  describe('store', () => {
    it('should store user free bets', () => {
      service.store('testUser', { data: [] });
      expect(nativeBridge.onFreeBetUpdated).toHaveBeenCalledTimes(2);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FREEBETS_UPDATED, jasmine.any(Object));
      expect(storage.set).toHaveBeenCalledTimes(1);
      expect(storage.remove).toHaveBeenCalledWith('hideFreeBetsFortestUser');
    });

    it('should store user free bets - sorted by freebetTokenExpiryDate', () => {
      locale['getString'] = jasmine.createSpy('getString').and.returnValue('FREEBET');
      time.compareDate.and.returnValue(1);
      const notSorted = {
        data: [
          { freebetTokenExpiryDate: '2025-06-25 12:16:10', freeBetType: 'FREEBET' },
          { freebetTokenExpiryDate: '2019-12-31 12:04:33', freeBetType: 'FREEBET' },
          { freebetTokenExpiryDate: '2019-06-25 15:16:10', freeBetType: 'FREEBET' }
        ]
      };
      const sorted = {
        data: [
          { freebetTokenExpiryDate: '2019-06-25 15:16:10', expires: '1 day', freeBetType: 'FREEBET' },
          { freebetTokenExpiryDate: '2019-12-31 12:04:33', expires: '1 day', freeBetType: 'FREEBET' },
          { freebetTokenExpiryDate: '2025-06-25 12:16:10', expires: '1 day', freeBetType: 'FREEBET' }
        ]
      };
      // @ts-ignore
      service.store('testUser', notSorted);
      // @ts-ignore
      expect(service['freeBetsState'].data).toEqual(sorted.data);
    });

    it('should handle params error', () => {
      service.store('testUser', { data: [], error: 'testError' });
      expect((console as any).info).toHaveBeenCalledWith('Freebets server error:', 'testError');
    });

    it('should clear stored free bets', () => {
      service.store('testUser', { data: undefined });
      expect(storage.remove).toHaveBeenCalledWith('freeBets-testUser');
    });

    it('should clear stored free bets', () => {
      storage.get.and.returnValues(
        false, mockedFreeBets.freeBetData
      );
      service.store('testUser', { data: undefined });
      expect(storage.remove).toHaveBeenCalledWith('freeBets-testUser');

    });

    it('should not call storage.remove if data has some value', () => {
      const mockData: IFreebetToken[] = mockedFreeBets.mockFreeBet;
      service.store('testUser', { data: mockData });
      expect(storage.remove).not.toHaveBeenCalledWith('freeBets-testUser');
    });

    it('should call setFreeBetsState with bet pack obj', () => {
      service['setFreeBetsState']([{name: 'fb1', freebetOfferCategories:{freebetOfferCategory:'Bet Pack'}}] as any)  
      expect(service.getFreeBetsState().available).toBe(true);
    });
    it('should call setFreeBetsState without  freebetOfferCategories obj', () => {
      service['setFreeBetsState']([{name: 'fb1',freebetOfferCategories:{freebetOfferCategory:'Acca Insurance'}}] as any) 
      expect(service.getFreeBetsState().available).toBe(true);
    });
    it('should store user free bets and sort', () => {
      const initState = [{
        freebetTokenId: '12',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '12',
          betLevel: 'EVENT'
        }
      },
      {
        freebetTokenId: '11',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '11',
          betLevel: 'EVENT'
        }
      },
      {
        freebetTokenId: '11',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '11',
          betLevel: 'EVENT'
        }
      },
      {
        freebetTokenId: '13',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '13',
          betLevel: 'EVENT'
        }
      }
    ];
      storage.get.and.returnValue(JSON.stringify(initState));
      service.store('testUser', { data: initState } as any);
      expect(service['freeBetsState'].available).toBeTrue();
    });    
    it('should call setFreeBetsState with bet pack obj', () => {
      service['setFreeBetsState']([{ name: 'fb1', freebetOfferCategories: { freebetOfferCategory: 'Fanzone' } }] as any)
      expect(service.getFreeBetsState().available).toBe(true);
    });
    it('should call setFreeBetsState without  freebetOfferCategories obj', () => {
      service['setFreeBetsState']([{ name: 'fb1', freebetOfferCategories: { freebetOfferCategory: 'Acca Insurance' } }] as any)
      expect(service.getFreeBetsState().available).toBe(true);
    });
    it('should call setFreeBetsState without  freebetOfferCategories obj', () => {
      service['setFreeBetsState']([{ name: 'fb1', freebetOfferCategories: {} }] as any)
      expect(service.getFreeBetsState().available).toBe(true);
    });
    it('should call setFreeBetsState without  freebetOfferCategories obj', () => {
      service['setFreeBetsState']([{ name: 'fb1', freebetOfferCategories: { freebetOfferCategory: '' } }] as any)
      expect(service.getFreeBetsState().available).toBe(true);
    });
    it('should store user free bets and sort', () => {
      const initState = [{
        freebetTokenId: '12',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '12',
          betLevel: 'EVENT'
        }
      },
      {
        freebetTokenId: '11',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '11',
          betLevel: 'EVENT'
        }
      },
      {
        freebetTokenId: '11',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '11',
          betLevel: 'EVENT'
        }
      },
      {
        freebetTokenId: '13',
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        freebetOfferName: 'testOffer',
        freebetTokenValue: 300,
        tokenPossibleBet: {
          betId: '13',
          betLevel: 'EVENT'
        }
      }
    ];
      storage.get.and.returnValue(JSON.stringify(initState));
      service.store('testUser', { data: initState } as any);
      expect(service['freeBetsState'].available).toBeTrue();
    });
  });
  it('should get free bet', () => {
    service.getFreeBet('12').subscribe(
      () => {
        expect(time.compareDate).toHaveBeenCalledTimes(2);
      });

    service.getFreeBet('1').subscribe(
      () => {
      },
      () => {
        expect((console as any).info).toHaveBeenCalledWith(
          'No freebet available by ID 1', undefined
        );
      });
  });

  it('should get free bet with different method for session refresh', () => {
    service['processFreebetsRequest'](true).subscribe(
      () => {
        expect(bpp.send).toHaveBeenCalledWith('allAccountFreebets', 'SPORTS');
      });

    service['processFreebetsRequest']().subscribe(
      () => {
        expect(bpp.send).toHaveBeenCalledWith('accountFreebets', 'SPORTS');
      });
  });

  it('should get free bet offers with different method for session refresh', () => {
    service['getAccLimitFreeBetReq']().subscribe(
      () => {
        expect(bpp.send).toHaveBeenCalledWith('accountFreebetsWithLimits', 'SPORTS');
      });
  });
  it('should get free bet offers with ANY_POOLS', () => {
    bpp.send = jasmine.createSpy().and.returnValue(observableFrom([{
        response: {
          model: {
            freebetToken: [{
              freebetOfferCategories: { freebetOfferCategory: 'Bet Pack'},
              freebetTokenExpiryDate: '1',
              freebetTokenId: '12',
              tokenPossibleBet: {
                betId: null,
                betLevel: 'ANY_POOLS'
              }
            }]
          }
        }
      }]));
    service['getAccLimitFreeBetReq']().subscribe(
      () => {
        expect(bpp.send).toHaveBeenCalledWith('accountFreebetsWithLimits', 'SPORTS');
      });
  });

  it('should get free bet offers with ANY', () => {
    bpp.send = jasmine.createSpy().and.returnValue(observableFrom([{
        response: {
          model: {
            freebetToken: [{
              freebetOfferCategories: { freebetOfferCategory: 'Bet Pack'},
              freebetTokenExpiryDate: '1',
              freebetTokenId: '12',
              tokenPossibleBet: {
                betId: null,
                betLevel: 'ANY_POOLS'
              }
            }]
          }
        }
      }]));
    service['getAccLimitFreeBetReq']().subscribe(
      () => {
        expect(bpp.send).toHaveBeenCalledWith('accountFreebetsWithLimits', 'SPORTS');
      });
  });
  it('should handle storefreebets on refrech connect event', () => {
    spyOn(service, 'getFreeBets').and.returnValue(of({} as any));

    storeFreeebetsCallback();

    expect(service.getFreeBets).toHaveBeenCalledWith(true);
  });

  describe('getFreeBets', () => {
    it('should get free bets and set usedBy', fakeAsync(() => {
      time.compareDate.and.returnValue(8);
      service.getFreeBets().subscribe(
        () => {
          expect(time.compareDate).toHaveBeenCalledTimes(2);
          expect(time.formatByPattern).toHaveBeenCalledTimes(2);
        });
      flush();
    }));
    it('should get free bets and set not usedBy', fakeAsync(() => {
      time.compareDate.and.returnValue(1);
      service.getFreeBets().subscribe(
        () => {
          expect(time.compareDate).toHaveBeenCalledTimes(2);
        });
      flush();
    }));

    it('should not call bpp service in case if user is in-shop', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      user.isInShopUser.and.returnValue(true);
      service.getFreeBets().subscribe(successHandler, errorHandler);
      tick();

      expect(session.whenProxySession).not.toHaveBeenCalled();
      expect(successHandler).toHaveBeenCalledWith([]);
      expect(errorHandler).not.toHaveBeenCalled();
    }));
  });

  it('getFreeBetsData should return free bets data', () => {
    const result: any[] = service.getFreeBetsData();

    expect(result).toEqual([{
      freebetTokenId: '12',
      freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
      freebetOfferName: 'testOffer',
      freebetTokenValue: 300,
      tokenPossibleBet: {
        betId: '12',
        betLevel: 'EVENT'
      }
    }]);
  });

  it('getFreeBetsData should return empty list', () => {
    storage.get.and.returnValue([]);
    const result: any[] = service.getFreeBetsData();

    expect(result).toEqual([]);
  });

  it('getBetNowLink no data', () => {
    expect(service['getBetNowLink']({} as any)).toEqual('/');
  });

  it('getBetNowLink ', () => {
    expect(service['getBetNowLink']({ categoryId: 12, eventData: {} } as any)).toEqual('/testUrl');
  });

  it('getBetNowLink no eventData', fakeAsync(() => {
    service['getSportlink'] = jasmine.createSpy('getSportlink').and.returnValue('sportLink');
    expect(service['getBetNowLink']({ categoryId: 12, eventData: null } as any)).toEqual('/sportLink');
    tick();
    expect(service['getSportlink']).toHaveBeenCalled();
  }));

  it('getSportlink', () => {
    expect(service['getSportlink']('horseracing', 'greyhound')).toEqual('sport/greyhound');
  });

  it('getSportlink', () => {
    expect(service['getSportlink']('21', 'def')).toEqual('def');
  });

  it('getFreeBetsSum should return string representing freebets sum', () => {
    storage.get.and.returnValue([]);
    const result: string = service.getFreeBetsSum();

    expect(filters.currencyPosition).toHaveBeenCalled();
    expect(result).toEqual('$300');
  });

  describe('@isFreeBetVisible', () => {
    it('should get free bet visibility (true)', () => {
      expect(service.isFreeBetVisible(event)).toBe(true);
    });

    it('should return false if user status is null', () => {
      user.status = null;
      expect(service.isFreeBetVisible(event)).toBe(false);
    });

    it('should get free bet visibility (false, no data)', () => {
      service['freeBetsState'] = {
        data: []
      } as any;
      expect(service.isFreeBetVisible(event)).toBe(false);
    });

    it('should get free bet visibility (false, no token)', () => {
      service['freeBetsState'] = {
        data: [
          { tokenPossibleBet: {} },
          {},
        ]
      } as any;
      expect(service.isFreeBetVisible(event)).toBe(false);
    });

    it('should get free bet visibility (false)', () => {
      service['freeBetsState'] = {
        data: [
          {
            tokenPossibleBet: {
              betId: '231',
              betLevel: 'MARKET'
            }
          }
        ]
      } as any;
      event.markets = [{ id: '231' }];
      expect(service.isFreeBetVisible(event)).toBe(true);
    });

    it('should get free bet visibility (false)', () => {
      service['freeBetsState'] = {
        data: [
          {
            tokenPossibleBet: {
              betId: '77',
              betLevel: 'SELECTION'
            }
          }
        ]
      } as any;
      event.markets = [{ id: '231', outcomes: [{ id: '77' }] }];
      expect(service.isFreeBetVisible(event)).toBe(true);
    });
  });

  it('should get free bets state', () => {
    expect(service.getFreeBetsState().available).toBe(true);
  });

  it('should get free bets in split format', () => {
    const state = {
      expiry: '2050-12-11T22:00:00.000Z.000Z',
      id: '12',
      offerName: 'testOffer ',
      value: 300
    };
    expect(JSON.stringify(service.getFreeBetInBetSlipFormat('12'))).toBe(JSON.stringify(state));
  });

  it('should not get free bets in split format', () => {
    expect(JSON.stringify(service.getFreeBetInBetSlipFormat('13'))).toBe(undefined);
  });

  it('should not get free bets in split format', () => {
    storage.get.and.returnValue(false);
    expect(JSON.stringify(service.getFreeBetInBetSlipFormat('13'))).toBe(undefined);
  });

  describe('@showFreeBetsInfo', () => {
    it('should show free bets info', () => {
      service.showFreeBetsInfo().subscribe(
        (result) => {
          expect(storage.get).toHaveBeenCalledTimes(4);
          expect(result).toEqual(null);
        });
    });

    it('should not update stored data ', () => {
      storage.get.and.returnValue(false);
      service.showFreeBetsInfo().subscribe((result) => {
        expect(storage.set).not.toHaveBeenCalled();
        expect(result).toEqual(null);
      });
    });

    it('should not update stored data (no token)', () => {
      storage.getCookie.and.returnValue(undefined);
      service.showFreeBetsInfo().subscribe((result) => {
        expect(storage.set).not.toHaveBeenCalled();
        expect(result).toEqual(null);
      });
    });

    it('should show dialog', () => {
      storage.getCookie.and.returnValue(true);
      storage.get.and.returnValues(
        false,
        '[{"tokenId":32,"freebetTokenExpiryDate":"11-11-2019"}]'
      );
      filters.currencyPosition.and.returnValue('10$');

      service.showFreeBetsInfo().subscribe((result) => {
        expect(dialog.openDialog).toHaveBeenCalledWith(
          'freeBetsDialog',
          jasmine.any(Function),
          false,
          {
            freeBetsSum: '10$',
            currencySymbol:'$',
            freeBetsData: [{ tokenId: 32, freebetTokenExpiryDate: 'time string' }],
            onBeforeClose: jasmine.any(Function)
          }
        );
        expect(storage.set).toHaveBeenCalledWith('hideFreeBetsFortest', true);
        expect(pubsub.publish).toHaveBeenCalledWith('USER_INTERACTION_REQUIRED');
        expect(result).toEqual(null);
      });
    });
  });

  describe('showFreeBetAvailableMessage', () => {
    it('should getFreeBetAvailableMessage', () => {
      expect(service.getFreeBetAvailableMessage()).toBe('test');
    });
  });

  describe('getHideFreeBetIDs', () => {
    it('should getHideFreeBetIDs', () => {
      const hideIDs = ['12', '13'];
      storage.get.and.returnValue(JSON.stringify(hideIDs));
      expect(service.getHideFreeBetIDs()).toEqual(hideIDs);
    });

    it('should getHideFreeBetIDs (empty)', () => {
      storage.get.and.returnValue(null);
      expect(service.getHideFreeBetIDs()).toEqual([]);
    });
  });

  describe('getBetLevelName', () => {
    it('should return empty string because of lack of data from SideSrev for event', fakeAsync(() => {
      siteServer.getData.and.returnValue([]);
      service.getBetLevelName('1', 'EVENT').subscribe(data => {
        expect(data).toBe('');
      });
      flush();
    }));

    it('should return freebetTokendisplayText', fakeAsync(() => {
      siteServer.getData.and.returnValue([]);
      service.getBetLevelName('1', 'EVENT','any').subscribe(data => {
        expect(data).toBe('any');
      });
      flush();
    }));

    it('should return event name', fakeAsync(() => {
      siteServer.getData.and.returnValue([{
        event: {
          name: 'eventName'
        }
      }]);
      service.getBetLevelName('1', 'EVENT').subscribe(data => {
        expect(data).toBe('eventName');
      });
      flush();
    }));

    it('should return type name', fakeAsync(() => {
      siteServer.getData.and.returnValue([{
        class: {
          children: [{
            type: {
              name: 'typeName'
            }
          }]
        }
      }]);
      service.getBetLevelName('1', 'TYPE').subscribe(data => {
        expect(data).toBe('typeName');
      });
      flush();
    }));

    it('should return class name', fakeAsync(() => {
      siteServer.getData.and.returnValue([{
        class: {
          name: 'className'
        }
      }]);
      service.getBetLevelName('1', 'CLASS').subscribe(data => {
        expect(data).toBe('className');
      });
      flush();
    }));

    it('should return empty string because of lack of data from SideSrev for category', fakeAsync(() => {
      siteServer.getCategories.and.returnValue([]);
      service.getBetLevelName('1', 'CATEGORY').subscribe(data => {
        expect(data).toBe('');
      });
      flush();
    }));

    it('should return category name', fakeAsync(() => {
      siteServer.getCategories.and.returnValue([[{ name: 'className' }]]);
      service.getBetLevelName('1', 'CATEGORY').subscribe(data => {
        expect(data).toBe('className');
      });
      flush();
    }));
    it('should call with ANY_POOLS', fakeAsync(() => {
      siteServer.getCategories.and.returnValue([[{ name: 'className' }]]);
      service.getBetLevelName('1', 'ANY_POOLS').subscribe(data => {
        expect(data).toBeUndefined();
      });
      flush();
    }));

    it('handle incorrect betLevel', fakeAsync(() => {
      service.getBetLevelName('', 'SOME').subscribe(data => {
        expect(data).toBe('');
      });
      flush();
    }));
  });

  describe('groupByName', ()=>{
    beforeEach(()=>{
      locale.getString.and.returnValue('All Sports');
    })
    it('should return grouped freebets of specific sport (HR , FB)', ()=> {
      const mockData = [
        {
        tokenPossibleBet: {
          name: 'Horse_Racing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '21',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Horse_Racing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '21',
          channels: ''
        }]
      },{
        tokenPossibleBet: {
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '22',
          channels: ''
        },
        tokenPossibleBets: [
          {
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '22',
          channels: ''
        }
      ]
      }] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of('Horse Racing'), of('Football'));
      service.groupByName(mockData,false).subscribe(data => {
        expect(data).toEqual({ 'Horse Racing': [mockData[1]], 'Football': [mockData[0]]});
      });
    });

    it('should return grouped freebets of specific sport (HR)', ()=> {
      const mockData = [
        {
        tokenPossibleBet: {
          name: 'Horse_Racing',
          betLevel: 'CLASS',
          betType: '',
          betId: '321',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Horse_Racing',
          betLevel: 'CLASS',
          betType: '',
          betId: '223',
          channels: ''
        },
        {
          name: 'Horse_Racing',
          betLevel: 'ANY_POOLS',
          betType: '',
          betId: '',
          channels: ''
        },
        {
          name: 'Horse_Racing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '21',
          channels: ''
        },{
          name: 'Horse_Racing',
          betLevel: 'CATEGORY1',
          betType: '',
          betId: '21',
          channels: ''
        }],
      }] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of('Horse Racing'));
      service.groupByName(mockData,false).subscribe(data => {
        expect(data).toEqual({ 'Horse Racing': [mockData[0]]});
      });
    });

    it('should return grouped freebets of specific sport (HR) with freebetTokenDisplayText', ()=> {
      const mockData = [
        {
        freebetTokenDisplayText: 'ANY_POOLS TEST',
        tokenPossibleBet: {
          name: 'Horse_Racing',
          betLevel: 'CLASS',
          betType: '',
          betId: '321',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Horse_Racing',
          betLevel: 'CLASS',
          betType: '',
          betId: '223',
          channels: ''
        },
        {
          name: 'Horse_Racing',
          betLevel: 'ANY_POOLS',
          betType: '',
          betId: '',
          channels: ''
        },
        {
          name: 'Horse_Racing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '21',
          channels: ''
        },{
          name: 'Horse_Racing',
          betLevel: 'CATEGORY1',
          betType: '',
          betId: '21',
          channels: ''
        }],
      }] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of('Horse Racing'));
      service.groupByName(mockData,false).subscribe(data => {
        expect(data).toEqual({ 'Horse Racing': [mockData[0]]});
      });
    });

    it('should return grouped freebets of specific freebet token display text', ()=> {
      const mockData = [
        {
        freebetTokenDisplayText:'any',
        tokenPossibleBet: {
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '22',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '22',
          channels: ''
        }]
      }] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of('any'));
      service.groupByName(mockData,true).subscribe(data => {
        expect(data).toEqual({ 'any': [mockData[0]]});
      });
    });
    it('should return grouped freebets of specific sport (Single sport)', () => {
      const  mockData = [
        {
          freebetTokenDisplayText:"Valid On FootBall Sport",
          tokenPossibleBet: {
            name: 'Football',
            betLevel: 'CATEGORY',
            betType: '',
            betId: '22',
            channels: ''
          },
          tokenPossibleBets: [{
            name: 'Football',
            betLevel: 'CATEGORY',
            betType: '',
            betId: '22',
            channels: ''
          }]
        },
        {
          freebetTokenDisplayText:"Valid On Tennis Sport",
          tokenPossibleBet: {
            name: 'Tennis',
            betLevel: 'CATEGORY',
            betType: '',
            betId: '23',
            channels: ''
          },
          tokenPossibleBets: [{
            name: 'Tennis',
            betLevel: 'CATEGORY',
            betType: '',
            betId: '23',
            channels: ''
          }]
        }
      ] as any;
      spyOn(service, 'getBetLevelName').and.returnValue(of('Football'));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({ 'Football': mockData });
      });
    });

    it('should return grouped freebets applicable on all sports', ()=> {
      const mockData = [
        {
        tokenPossibleBet: {
          name: 'HorseRacing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '45',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'HorseRacing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '45',
          channels: ''
        }]
      },
      {
        tokenPossibleBet: {
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '123',
          channels: ''
        }, 
        tokenPossibleBets: [{
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '123',
          channels: ''
        }]
      }
    ] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of(''), of(''));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({'All Sports': mockData});
      });
    });

    it('should return grouped freebets of All sports (without tokenPossibleBets)', ()=> {
      const mockData = [
        {
        tokenPossibleBet: {
          name: 'HorseRacing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '45',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '123',
          channels: ''
        }]
      }
    ] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of(''), of(''));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({'All Sports': mockData});
      });
    });

    it('should return grouped freebets of All sports (without tokenPossibleBets)', ()=> {
      const mockData = [
        {
        tokenPossibleBet: {
          name: 'HorseRacing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '45',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '123',
          channels: ''
        }]
      }
    ] as any;
      spyOn(service, 'getBetLevelName').and.returnValues(of(''), of(''));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({'All Sports': mockData});
      });
    });

    it('should return grouped freebets of All sports (without tokenPossibleBets)', ()=> {
      const mockData = [
        {
        tokenPossibleBet: {
          name: 'HorseRacing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Football',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '123',
          channels: ''
        }]
      }
    ] as any;
      spyOn(service, 'getBetLevelName').and.returnValue(of(''));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({'All Sports': mockData});
      });
    });

    it('should return grouped freebets of all sports when betlevel name is none', ()=> {
      const mockData = [{
        tokenPossibleBet: {
          name: 'Horse_Racing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '2122',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Horse_Racing',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '2122',
          channels: ''
        }]
      }] as any;
      spyOn(service, 'getBetLevelName').and.returnValue(of(''));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({ 'All Sports': mockData});
      });
    });

    it('should return freebets applicable to AllSports', () =>{
      const mockFreeBet = mockedFreeBets.mockFreeBet as any;
      service.groupByName(mockFreeBet).subscribe(data => {
        expect(data).toEqual({ 'All Sports': mockFreeBet});
      });
    });

   it('should return error', () =>{
      const mockFreeBet = mockedFreeBets.mockFreeBet as any;
      spyOn(service, 'getBetLevelName').and.returnValue(throwError('Not valid freebet'));
      service.groupByName(mockFreeBet).subscribe(null, error=>{
        expect(error).toBe('Not valid freebet');
      });
    });
    it('when the token possible bet object is empty', () =>{
      const mockData = [{
        tokenPossibleBet: {
          name: '',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '',
          channels: ''
        },
        tokenPossibleBets: [{
          name: '',
          betLevel: 'CATEGORY',
          betType: '',
          betId: '',
          channels: ''
        }]
      }] as any;
      spyOn(service, 'getBetLevelName').and.returnValue(of(''));
      service.groupByName(mockData);
      expect(service['getBetLevelName']).toHaveBeenCalledWith('', 'ANY','',true);
    });

    it('should not call getBetLevelName when the free bet list is empty', () =>{
      spyOn(service, 'getBetLevelName').and.returnValue(of(''));
      service.groupByName([]);
      expect(service['getBetLevelName']).not.toHaveBeenCalled();
    });


    it('should return grouped freebets of level ANY_POOLS', ()=> {
      const mockData = [
        {
          freebetTokenDisplayText: 'ANY_POOL',
        tokenPossibleBet: {
          name: 'HorseRacing',
          betLevel: 'ANY_POOLS',
          betType: '',
          betId: '',
          channels: ''
        },
        tokenPossibleBets: [{
          name: 'Football',
          betLevel: 'ANY_POOLS',
          betType: '',
          betId: '',
          channels: ''
        }]
      }
    ] as any;
      spyOn(service, 'getBetLevelName').and.returnValue(of(''));
      service.groupByName(mockData).subscribe(data => {
        expect(data).toEqual({'All Sports': mockData});
      });
    });
  });

  it('@enhanceFreeBetItem with less then 7', () => {
    const freeBetItem = mockedFreeBets.freeBetItem as any;
    time.compareDate.and.returnValue(1);
    service['enhanceFreeBetItem'](freeBetItem);

    expect(freeBetItem.expires).not.toBeNull();
  });

  it('@enhanceFreeBetItem with less then 7', () => {
    const freeBetItem = mockedFreeBets.freeBetItem as any;
    time.compareDate.and.returnValue(2);
    service['enhanceFreeBetItem'](freeBetItem);

    expect(freeBetItem.expires).not.toBeNull();
  });

  it('@enhanceFreeBetItem with more then 7', () => {
    const freeBetItem = mockedFreeBets.freeBetItem as any;
    time.compareDate.and.returnValue(8);
    service['enhanceFreeBetItem'](freeBetItem);

    expect(time.formatByPattern).toHaveBeenCalledWith(jasmine.any(Object), 'dd/MM/yyyy');
    expect(freeBetItem.usedBy).not.toBeNull();

  });

  describe('@getOddsBoostsWithCategories', () => {
    it('should ', () => {
      siteServer.getCategories.and.returnValue(Promise.resolve(mockedFreeBets.getCategoriesData));
      siteServer.getData.and.returnValue(Promise.resolve(mockedFreeBets.siteServerData));
      service['getCategoriesDataByIDs'] = jasmine.createSpy('getCategoriesDataByIDs').and.returnValue(
        of(mockedFreeBets.categoryData));

      service['getLevelEventsDataByIDs'] = jasmine.createSpy('getLevelEventsDataByIDs').and.returnValue(
        of(mockedFreeBets.categoryData));

      const tokens = mockedFreeBets.tokenSample as any;
      service['getBetNowLink'] = jasmine.createSpy('getBetNowLink');
      service['getCategoriesDataByIDs'] = jasmine.createSpy('getCategoriesDataByIDs');

      service.getOddsBoostsWithCategories(tokens).subscribe((freeBetTokes: IFreebetToken[]) => {
        expect(service['getBetNowLink']).not.toHaveBeenCalled();
      });
    });

    it('should test for level category ', () => {
      siteServer.getCategories.and.returnValue(Promise.resolve(mockedFreeBets.getCategoriesData));
      siteServer.getData.and.returnValue(Promise.resolve(mockedFreeBets.siteServerData));
      service['getCategoriesDataByIDs'] = jasmine.createSpy('getCategoriesDataByIDs').and.returnValue(
        of(mockedFreeBets.categoryDataSample));

      service['getLevelEventsDataByIDs'] = jasmine.createSpy('getLevelEventsDataByIDs').and.returnValue(
        of(mockedFreeBets.categoryDataSample));
      const tokens = mockedFreeBets.tokenCategorySample as any;
      const expectedTokens: IFreebetToken[] = mockedFreeBets.expectedTokenSample as any;
      service['getBetNowLink'] = jasmine.createSpy('getBetNowLink');
      service['getCategoriesDataByIDs'] = jasmine.createSpy('getCategoriesDataByIDs');

      service.getOddsBoostsWithCategories(tokens).subscribe((freeBetTokes: IFreebetToken[]) => {
        expect(service['getBetNowLink']).not.toHaveBeenCalled();
      });
    });

    it('should not consider if loop', () => {
      siteServer.getCategories.and.returnValue(Promise.resolve(mockedFreeBets.getCategoriesData));
      siteServer.getData.and.returnValue(Promise.resolve(mockedFreeBets.siteServerData));

      service['getBetNowLink'] = jasmine.createSpy('getBetNowLink');
      service['getCategoriesDataByIDs'] = jasmine.createSpy('getCategoriesDataByIDs').and.returnValue(
        of(mockedFreeBets.categoryDataSample2));
      service['getLevelEventsDataByIDs'] = jasmine.createSpy('getLevelEventsDataByIDs').and.returnValue(
        of(mockedFreeBets.categoryDataSample2));

      const tokens = [{ tokenId: '4' }] as any;

      service.getOddsBoostsWithCategories(tokens).subscribe((freeBetTokes: IFreebetToken[]) => {
        expect(service['getBetNowLink']).toHaveBeenCalled();

      });
    });
  });

  describe('@getFreeBetWithBetNowLink', () => {
    it('should handle token without tokenPossibleBet', () => {
      const token = {} as any;
      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(siteServer.getData).not.toHaveBeenCalled();
        expect(freeBet).toEqual({ betNowLink: '/' } as any);
      });
    });

    it('should handle token with betLevel = CATEGORY', () => {
      const token = mockedFreeBets.categoryToken as any;
      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(siteServer.getData).not.toHaveBeenCalled();
        expect(freeBet).toEqual({
          tokenPossibleBet: mockedFreeBets.categoryToken.tokenPossibleBet,
          betNowLink: '/sport/americanfootball'
        } as any);
      });
    });

    it('should handle token with betLevel = BET', () => {
      const token = mockedFreeBets.marketToken as any;
      siteServer.getData.and.returnValue(Promise.resolve({}));
      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(freeBet).toEqual({
          tokenPossibleBet: mockedFreeBets.marketToken.tokenPossibleBet,
          betNowLink: '/'
        } as any);
      });
    });

    it('should handle token with betLevel = ANY_POOLS', () => {
      const token = mockedFreeBets.horseRacingToken as any;
      siteServer.getData.and.returnValue(Promise.resolve({}));
      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(freeBet).toEqual({
          tokenPossibleBet: mockedFreeBets.horseRacingToken.tokenPossibleBet,
          betNowLink: '/horse-racing'
        } as any);
      });
    });

    it('should handle token with betLevel = ANY SPORTS + ANY_POOLS', () => {
      const token = mockedFreeBets.anySportsandanyPools as any;
      siteServer.getData.and.returnValue(Promise.resolve({}));
      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(freeBet).toEqual({
          tokenPossibleBets: mockedFreeBets.anySportsandanyPools.tokenPossibleBets,
          betNowLink: '/'
        } as any);
      });
    });

    it('should handle token with betLevel = BET', () => {
      const token = mockedFreeBets.marketToken as any;
      service['getBetNowLink'] = jasmine.createSpy('getBetNowLink');
      siteServer.getData.and.returnValue(Promise.resolve(null));
      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(service['getBetNowLink']).not.toHaveBeenCalled();
      });
    });
    

    it('should handle error', () => {
      const token = mockedFreeBets.marketToken as any;
      siteServer.getData.and.returnValue(throwError(`Can not fetch event 1}`));

      service.getFreeBetWithBetNowLink(token).subscribe((freeBet) => {
        expect(freeBet).toEqual({
          tokenPossibleBet: mockedFreeBets.marketToken.tokenPossibleBet,
          betNowLink: '/'
        } as any);
      });
    });
  });

  it('@getSelectionOutcomeIds should extract outcome ids', () => {
    const sportEvent = {
      event: {
        children: [
          { market: { children: [{ outcome: { id: '31' } }] } },
          { market: { children: [{ outcome: { id: '5' } }, { outcome: { id: '7' } }] } },
          { market: { children: [{ outcome: { id: '10' } }] } },
        ]
      }, class: {
        children: [{
          type: {
            id: '31',
            name: 'CATEGORY'
          }
        }]
      }
    } as any;
    const expectedResult = ['31', '5', '7', '10'];
    expect(service['getSelectionOutcomeIds'](sportEvent)).toEqual(expectedResult);
  });

  it('@getBetNowLink', () => {
    extensionsStorage.getList.and.returnValue([
      {
        name: 'extension-name',
        sportsConfig: { id: '6' },
        extendsModule: 'sb'
      }
    ]);
    routingHelper.formEdpUrl.and.returnValue('router-helper-link');
    const categoryId = '6';
    const eventData = {};
    expect(service['getBetNowLink']({ categoryId, eventData } as any)).toEqual('/router-helper-link');
  });
  describe('getFreeBetType', () => {
    it('should get  bets type as Fanzone', () => {
      service['isBetPack'] = jasmine.createSpy('isBetPack').and.returnValue(false);
      service['isFanzone'] = jasmine.createSpy('isFanzone').and.returnValue(true);
      service.getFreeBetType({ name: 'fb1', freebetOfferCategories: { freebetOfferCategory: 'Fanzone' } } as any);
      expect(locale.getString).toHaveBeenCalledWith('bma.fanZone');
    });
    it('should get  bets type as BetPack', () => {
      service['isBetPack'] = jasmine.createSpy('isBetPack').and.returnValue(true);
      service.getFreeBetType({ name: 'fb1', freebetOfferCategories: { freebetOfferCategory: 'Bet Token' } } as any);
      expect(locale.getString).toHaveBeenCalledWith('bma.betToken');
    });
    it('should get  bets type as BetPack', () => {
      service['isBetPack'] = jasmine.createSpy('isBetPack');
      service['isFanzone'] = jasmine.createSpy('isFanzone');
      service.getFreeBetType({ name: 'fb1', freebetOfferCategories: { freebetOfferCategory: 'test' } } as any);
      expect(locale.getString).toHaveBeenCalledWith('bma.freeBet');
    });
    it('should get  bets type as Freebet', () => {
      locale['getString'] = jasmine.createSpy('getString');
      service['isBetPack'] = jasmine.createSpy('isBetPack').and.returnValue(false);
      service['isFanzone'] = jasmine.createSpy('isFanzone').and.returnValue(false);
      service.getFreeBetType({ name: 'fb1' } as any);
      expect(locale.getString).toHaveBeenCalledWith('bma.freeBet');
    });
  });
  describe('@getLevelEventsDataByIDs', () => {
    it('should getLevelEventsDataByIDs for Betlevel MARKET', () => {
      const sportEvent = mockedFreeBets.sportEventMock as any;
      siteServer.getData.and.returnValue([{ sportEvent }]);
      service.getLevelEventsDataByIDs('MARKET', ['111', '112']).subscribe((freeBet) => {
        expect(service['getSelectionOutcomeIds']).not.toHaveBeenCalled();
      });
    });
    it('should getLevelEventsDataByIDs for Betlevel SELECTION', () => {
      const sportEvent = mockedFreeBets.sportEventMock as any;
      siteServer.getData.and.returnValue([{ sportEvent }]);
      service.getLevelEventsDataByIDs('SELECTION', ['111', '112']).subscribe((freeBet) => {
        expect(service['getSelectionOutcomeIds']).toHaveBeenCalled();
      });
    });
    it('should getLevelEventsDataByIDs for no Betlevel ', () => {
      const sportEvent = mockedFreeBets.sportEventMockWithClass as any;
      siteServer.getData.and.returnValue([{ sportEvent }]);
      service.getLevelEventsDataByIDs('abc', ['111', '112']).subscribe((freeBet) => {
        expect(service['getSelectionOutcomeIds']).not.toHaveBeenCalled();
      });
    });
    it('should getLevelEventsDataByIDs for no Betlevel ', () => {
      const sportEvent = mockedFreeBets.sportEventMockWithClass as any;
      siteServer.getData.and.returnValue([{ sportEvent }]);
      service.getLevelEventsDataByIDs('TYPE', ['111', '112']).subscribe((freeBet) => {
        expect(service['getSelectionOutcomeIds']).not.toHaveBeenCalled();
      });
    });
  });

  it('@getInitFreebetsState', () => {
    const hideIDs = ['12', '13'];
    storage.get.and.returnValue(hideIDs);

    service['getInitFreebetsState']();

    expect(nativeBridge.onFreeBetUpdated).toHaveBeenCalled();
  });

  it('@getCategoriesDataByIDs', () => {

    siteServer.getCategories.and.returnValue(Promise.resolve([{ id: '112', name: 'test' }]));
    service['getSportlink'] = jasmine.createSpy('getSportlink');
    service['getEventData'] = jasmine.createSpy('getEventData').and.returnValue(mockedFreeBets.getEventData);
    service['getCategoriesDataByIDs'](['112', '111, 114']).subscribe(data => {
      expect(siteServer.getCategories).toHaveBeenCalled();
      expect(service['getEventData']).toHaveBeenCalled();
    });

  });
  it('@isBetPack', () => {
    locale.getString.and.returnValue('BETPACK');
    expect(service.isBetPack()).toBeFalse();
    expect(service.isBetPack('Bet Pack')).toBeTrue();
  });
  it('@isFanzone', () => {
    locale.getString.and.returnValue('FANZONE');
    expect(service.isFanzone()).toBeFalse();
    expect(service.isFanzone('Fanzone')).toBeTrue();
  });
  });



