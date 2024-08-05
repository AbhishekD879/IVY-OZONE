import { ToteBetslipService } from './tote-betslip.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('ToteBetslipService', () => {
  let service: ToteBetslipService;
  let bppService;
  let commandService;
  let deviceService;
  let filterService;
  let localeService;
  let pubSubService;
  let siteServerEventToOutcomeService;
  let storageService;
  let clientUserAgentService;
  let coreToolsService;
  let userService;
  let currencyCalculatorService;
  let currencyCalculator;
  let authService;
  let freeBetsService;

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe')
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get'),
      remove: jasmine.createSpy('remove')
    };
    deviceService = {
      channel: { channelRef: { id: 'M' } }
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of({}))
    };
    clientUserAgentService = {
      getId: jasmine.createSpy('getId')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    commandService = {
      API: commandApi,
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve())
    };
    filterService = {
      numberWithCurrency: jasmine.createSpy('numberWithCurrency')
    };
    siteServerEventToOutcomeService = {
      getEventToOutcomeForOutcome: jasmine.createSpy('getEventToOutcomeForOutcome').and.callFake(() => of([]).toPromise())
    };
    coreToolsService = {
      getCurrencySymbolFromISO: jasmine.createSpy('getCurrencySymbolFromISO')
    };
    currencyCalculator = {
      currencyExchange: jasmine.createSpy('currencyExchange').and.callFake(() => 1.59)
    };
    userService = {
      currency: 'USD'
    };
    currencyCalculatorService = {
      getCurrencyCalculator: jasmine.createSpy('getCurrencyCalculator').and.returnValue(of(currencyCalculator))
    };
    freeBetsService = {
      getFreeBets: jasmine.createSpy().and.returnValue(of(null))
    };
    authService = {
      drillDownToteFreebets: jasmine.createSpy('drillDownToteFreebets')
    };

    service = new ToteBetslipService(
      bppService,
      commandService,
      deviceService,
      filterService,
      localeService,
      pubSubService,
      siteServerEventToOutcomeService,
      storageService,
      clientUserAgentService,
      coreToolsService,
      userService,
      currencyCalculatorService,
      freeBetsService,
      authService
    );

    service.currencyCalculator = currencyCalculator;
    service.stakeRestrictions = {} as any;
  });

  it('constructor', () => {
    expect(service.userCurrencyCode).toBe(userService.currency);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'ToteBetslipService',
      [pubSubApi.SUCCESSFUL_LOGIN, pubSubApi.SESSION_LOGOUT],
      jasmine.any(Function)
    );
  });

  describe('addToteBet', () => {
    it('should initialize bet details', fakeAsync(() => {
      const data: any = {
        toteBetDetails: {},
        outcomes: [{}]
      };
      service.addToteBet(data);
      tick();

      expect(storageService.set).toHaveBeenCalledWith('toteBet', data);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.BETSLIP_COUNTER_UPDATE, 1);
      expect(coreToolsService.getCurrencySymbolFromISO).toHaveBeenCalledTimes(1);
      expect(currencyCalculatorService.getCurrencyCalculator).toHaveBeenCalledTimes(1);
      expect(siteServerEventToOutcomeService.getEventToOutcomeForOutcome).toHaveBeenCalledTimes(1);
    }));

    it('should initialize bet details with toteBetDetails', fakeAsync(() => {
      const data: any = {
        toteBetDetails: {orderedOutcomes: [{}]},
        outcomes: [{}]
      };
      service.addToteBet(data);
      tick();

      expect(storageService.set).toHaveBeenCalledWith('toteBet', data);
    }));
    it('should set pot bet title', fakeAsync(() => {
      service.addToteBet({
        toteBetDetails: { orderedLegs: [{}], numberOfLines: 1 }
      } as any);
      tick();
      expect(localeService.getString).toHaveBeenCalledWith('bs.potBetTitle', [1]);
    }));

    it('should set pot bet title with poolData', fakeAsync(() => {
      service.addToteBet({
        toteBetDetails: { orderedLegs: [{}], numberOfLines: 1 }
      } as any, {
        toteBetDetails: { orderedLegs: [{}], numberOfLines: 1 }
      } as any);
      tick();
      expect(localeService.getString).toHaveBeenCalledWith('bs.potBetTitle', [1]);
    }));

    it('should set total stake title from poolBet', fakeAsync(() => {
      service.addToteBet({
        toteBetDetails: {},
        poolBet: { stakePerLine: 1 }
      } as any);
      tick();
      expect(filterService.numberWithCurrency).toHaveBeenCalledWith(1, '£');
      expect(localeService.getString).toHaveBeenCalledWith(
        'bs.totalStakeTitle', jasmine.any(Object)
      );
    }));

    it('test filter the value if token is FRRIDE', fakeAsync(() => {
      const mockData: IFreebetToken[] = [{
        tokenPossibleBetTags: {
          tagName: 'FRRIDE'
        }
      },
      {
        tokenPossibleBetTags: {
          tagName: 'FRRIDE1'
        }
      }] as any;
      freeBetsService.getFreeBets = jasmine.createSpy().and.returnValue(of(mockData));
      storageService.get = jasmine.createSpy().and.returnValue(JSON.stringify(mockData));
        service.addToteBet({
          toteBetDetails: {},
          poolBet: { stakePerLine: 1 }
        } as any);
        tick();
        expect(authService.drillDownToteFreebets).toHaveBeenCalled();
      })); 

      it('test filter the value if no tokenPossibleBetTags', fakeAsync(() => {
        const mockData: IFreebetToken[] = [{
          tokenPossibleBetTags: undefined
        }] as any;
        freeBetsService.getFreeBets = jasmine.createSpy().and.returnValue(of(mockData));
        storageService.get = jasmine.createSpy().and.returnValue(JSON.stringify(mockData));
          service.addToteBet({
            toteBetDetails: {},
            poolBet: { stakePerLine: 1 }
          } as any);
          tick();
          expect(authService.drillDownToteFreebets).toHaveBeenCalled();
        })); 
    it('test filter the value if data null', fakeAsync(() => {
        
        freeBetsService.getFreeBets = jasmine.createSpy().and.returnValue(of(null));
        storageService.getFreeBets = jasmine.createSpy().and.returnValue(of(null));
        service.addToteBet({
          toteBetDetails: {},
          poolBet: { stakePerLine: 1 }
        } as any);
        tick();
        expect(authService.drillDownToteFreebets).toHaveBeenCalled();
      }));
  });

  describe('clear', () => {
    it('should publish betslip liveupdate unsubscribe', () => {
      service.toteBet = { channelIds: '1' } as any;
      service.clear();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.BETSLIP_LIVEUPDATE_UNSUBSCRIBE, ['1']);
    });

    it('should not publish betslip liveupdate unsubscribe', () => {
      service.toteBet = null;
      service.clear();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  it('getLegTitle', () => {
    expect(
      service.getLegTitle({ name: 'leg1', eventTitle: 'abc' } as any)
    ).toBe('leg1: abc');
  });

  it('getSelectionName', () => {
    expect(
      service.getSelectionName({ isFavourite: false, runnerNumber: '1', name: 'name1' } as any)
    ).toBe('1. name1');
    expect(
      service.getSelectionName({ isFavourite: true, name: 'name1' } as any)
    ).toBe('name1');
  });

  describe('getTotalStake', () => {
    beforeEach(() => {
      service.toteBet = {
        poolBet: { stakePerLine: '10.123' }
      } as any;
      service.isPotBet = true;
      service.numberOfLines = 1;
      service.poolCurrencyCode = '$';
      service.userCurrencyCode = '$';
    });

    it('should return total stake', () => {
      expect(service.getTotalStake()).toBe('10.12');
    });

    it('should calculate total stake via currencyCalculator', () => {
      service.userCurrencyCode = '£';
      service.getTotalStake();
      expect(currencyCalculator.currencyExchange).toHaveBeenCalledWith(
        service.poolCurrencyCode, service.userCurrencyCode, 10.123
      );
    });

    it('shoudl return null if currencyCalculator is not available', () => {
      service.currencyCalculator = null;
      service.userCurrencyCode = '£';
      expect(service.getTotalStake()).toBeNull();
    });
  });

  describe('handleErrors', () => {
    it('should handle large stake', () => {
      service.handleErrors({
        betError: [{ betFailureKey: 'LARGE_STAKE' }]
      });
      expect(localeService.getString).toHaveBeenCalledWith(
        'bs.TOTE_BET_ERRORS.LARGE_STAKE', jasmine.any(Array)
      );
    });

    it('should handle small stake', () => {
      service.handleErrors({
        betError: [{ betFailureKey: 'SMALL_STAKE' }]
      });
      expect(localeService.getString).toHaveBeenCalledWith(
        'bs.TOTE_BET_ERRORS.SMALL_STAKE', jasmine.any(Array)
      );
    });

    it('should handle stake increment', () => {
      service.handleErrors({
        betError: [{ betFailureKey: 'STAKE_INCREMENT' }]
      });
      expect(localeService.getString).toHaveBeenCalledWith(
        'bs.TOTE_BET_ERRORS.STAKE_INCREMENT', jasmine.any(Array)
      );
    });

    it('should handle unknown error', () => {
      service.handleErrors({
        betError: [{ betFailureDesc: 'UNKNOWN_ERROR' }]
      });
      expect(localeService.getString).toHaveBeenCalledWith('bs.TOTE_BET_ERRORS.UNKNOWN_ERROR');
    });

    it('should handle unknown error (key not found)', () => {
      localeService.getString.and.returnValue('KEY_NOT_FOUND');
      service.handleErrors({
        betError: [{ betFailureDesc: 'TRADER_DRUNK', betFailureReason: 'Trader is drunk' }]
      });
      expect(service.toteError).toBe('Trader is drunk');
    });
  });

  it('isToteBetPresent', () => {
    service.toteBet = {} as any;
    expect(service.isToteBetPresent()).toBeTruthy();
    service.toteBet = null;
    expect(service.isToteBetPresent()).toBeFalsy();
  });

  it('isToteBetWithProperStake', () => {
    service.toteBet = null;
    expect(service.isToteBetWithProperStake()).toBeFalsy();

    service.toteBet = {
      poolBet: { stakePerLine: '123' }
    } as any;
    service.isPotBet = true;
    expect(service.isToteBetWithProperStake()).toBeFalsy();
  });

  describe('placeBet', () => {
    it('should not place bet', () => {
      service.toteBet = null;
      service.placeBet(1);
      expect(bppService.send).not.toHaveBeenCalled();
    });

    it('should place bet', fakeAsync(() => {
      storageService.get.and.returnValue({
        poolBet: {
          stakePerLine: '',
          freebetTokenId: '1'
        }
      } as any);
      service.toteBet = {
        poolBet: {
          stakePerLine: '',
          freebetTokenId: '1'
        }
      } as any;
      service['calculateStakePerLine'] = (data) => { return 1;}
      service.placeBet(1);
      tick();
      expect(bppService.send).toHaveBeenCalledWith('placePoolBet', jasmine.any(Object));
      expect(clientUserAgentService.getId).toHaveBeenCalled();
    }));

    it('should place bet', fakeAsync(() => {
      storageService.get.and.returnValue('');
      service.toteBet = {
        poolBet: {
          stakePerLine: '',
          freebetTokenId: '1',
          freebetTokenValue: '1'
        }
      } as any;
      service['calculateStakePerLine'] = (data) => { return 1;}
      service.placeBet(1);
      tick();
      expect(bppService.send).toHaveBeenCalledWith('placePoolBet', jasmine.any(Object));
      expect(clientUserAgentService.getId).toHaveBeenCalled();
    }));

    it('should handle place bet error', fakeAsync(() => {
      service.toteBet = {
        toteBetDetails: {
          numberOfLines: 2
        },
        poolBet: {
          stakePerLine: '',
          freebetTokenId: '',
          freebetTokenValue: 27
        }
      } as any;
      storageService.get.and.returnValue({
        toteBetDetails: {
          numberOfLines: 2
        },
        poolBet: {
          stakePerLine: '',
          freebetTokenId: '',
          freebetTokenValue: 27
        }
      } as any);
      bppService.send.and.returnValue(of({
        betFailure: [{
          betError: [{}]
        }]
      }));
      service.placeBet(1);
      tick();
      expect(bppService.send).toHaveBeenCalledWith('placePoolBet', jasmine.any(Object));
    }));
  });

  describe('reload', () => {
    it('should initialize bet', () => {
      storageService.get.and.returnValue({ toteBetDetails: {} });
      service.reload();
      expect(coreToolsService.getCurrencySymbolFromISO).toHaveBeenCalledTimes(1);
    });

    it('should not initialize bet', () => {
      storageService.get.and.returnValue(null);
      service.reload();
      expect(coreToolsService.getCurrencySymbolFromISO).not.toHaveBeenCalled();
    });
  });

  describe('removeToteBet', () => {
    it('should remove bet and refresh betslip', () => {
      service.removeToteBet(true, true);
      expect(pubSubService.publishSync).toHaveBeenCalledWith(
        pubSubApi.BETSLIP_COUNTER_UPDATE, 0
      );
      expect(storageService.remove).toHaveBeenCalledWith('toteBet');
      expect(storageService.remove).toHaveBeenCalledWith('toteSuspended');
      expect(pubSubService.publish).toHaveBeenCalledWith('REFRESH_BETSLIP');
    });

    it('should remove bet and close betslip', () => {
      service.removeToteBet(false);
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });

    it('should handle default params', () => {
      service.removeToteBet();

      expect(pubSubService.publish).toHaveBeenCalledWith('REFRESH_BETSLIP');
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });
  });

  it('setStakePerLine', () => {
    service.toteBet = { poolBet: { stakePerLine: '5' } } as any;
    service.setStakePerLine();

    service.toteBet = null;
    service.setStakePerLine();

    expect(filterService.numberWithCurrency).toHaveBeenCalledWith(5, '£');
    expect(filterService.numberWithCurrency).toHaveBeenCalledWith(0, '£');
    expect(localeService.getString).toHaveBeenCalledTimes(2);
  });

  describe('getNotPotBetTotalStake', () => {
    beforeEach(() => {
      service.betName = '';
      service.toteBet = {
        poolBet: {
          stakePerLine: 2,
          poolItem: [{}, {}],
          poolType: 'Test'
        }
      } as any;
    });

    it('should return stake for exacta/trifecta', () => {
      localeService.getString.and.returnValue('exacta');
      service.betName = 'exacta';
      expect(service['getNotPotBetTotalStake']()).toBe(2);
    });

    it('should return stake for win/place', () => {
      service.toteBet.poolBet.poolType = 'WN';
      expect(service['getNotPotBetTotalStake']()).toBe(4);
    });

    it('should return stake for exacta', () => {
      service.toteBet.poolBet.poolType = 'EX';
      expect(service['getNotPotBetTotalStake']()).toBe(4);
    });

    it('should return stake for trifecta', () => {
      service.toteBet.poolBet.poolType = 'TR';
      expect(service['getNotPotBetTotalStake']()).toBe(0);
    });

    it('missed bet type', () => {
      spyOn(console, 'error');
      service['getNotPotBetTotalStake']();
      expect(console.error).toHaveBeenCalledWith('Missed formula for bet type ', 'Test');
    });
  });

  describe('getTotalStakeValue', () => {
    it('no bet', () => {
      expect(service['getTotalStakeValue']()).toBe(0);
    });

    it('placepot/jackpot', () => {
      service.isPotBet = true;
      service.numberOfLines = 2;
      service.toteBet = {
        poolBet: { stakePerLine: 1 }
      } as any;
      expect(service['getTotalStakeValue']()).toBe(2);
    });

    it('exacta/trifecta', () => {
      service.toteBet = {
        poolBet: { stakePerLine: 1, poolItem: [] }
      } as any;
      service['getTotalStakeValue']();
      expect(localeService.getString).toHaveBeenCalledWith('uktote.strightExactaBet');
      expect(localeService.getString).toHaveBeenCalledWith('uktote.strightTrifectaBet');
    });
  });


  describe('calculateStakePerLine', () => {
    it('no bet', () => {
      service.toteBet = null;
      expect(service['getTotalStakeValue']()).toBe(0);
      service.toteBet = {
        poolBet: null
      } as any;
      expect(service['getTotalStakeValue']()).toBe(0);
      service.toteBet = {
        poolBet: {
          stakePerLine: ''
        }
      } as any;
      expect(service['getTotalStakeValue']()).toBe(0);
    });

    it('poolbet', () => {
      service.toteBet = {
        poolBet: {
          stakePerLine: 3
        }
      } as any;
      service.isPotBet = true;
      service['getNotPotBetTotalStake'] = () => { return 1 };
      service.numberOfLines = 2;
      expect(service['getTotalStakeValue'](1)).toBe(5);
      expect(service['getTotalStakeValue']()).toBe(6);
      service.isPotBet = false;
      expect(service['getTotalStakeValue']()).toBe(1);
      service['getNotPotBetTotalStake'] = () => { return 1 };
      expect(service['getTotalStakeValue']()).toBe(1);
      service['getNotPotBetTotalStake'] = () => { return 2 };
      expect(service['getTotalStakeValue'](1)).toBe(1);
      service['getNotPotBetTotalStake'] = () => { return 0 };
      expect(service['getTotalStakeValue']()).toBe(0);
    });

    it('getstring', () => {
      service.toteBet = {
        poolBet: { stakePerLine: 1, poolItem: [] }
      } as any;
      service['getTotalStakeValue']();
      expect(localeService.getString).toHaveBeenCalledWith('uktote.strightExactaBet');
      expect(localeService.getString).toHaveBeenCalledWith('uktote.strightTrifectaBet');
    });


    it('should call calculateStakePerLine with stakePerLine null' , () => {
      spyOn(service, 'calculateNumOfLines').and.returnValue(2);
      service.toteBet = {
        poolBet: { stakePerLine: null, poolItem: [] }
      } as any;
        const totePoolBet = {
          poolBet : {
            freebetTokenValue: 5
          }
        } as any;
        expect(service['calculateStakePerLine'](totePoolBet)).toEqual(2.50);
    });
    it('should call calculateStakePerLine with stakePerLine > 2' , () => {
      spyOn(service, 'calculateNumOfLines').and.returnValue(2);
      service.toteBet = {
        poolBet: { stakePerLine: 2, poolItem: [] }
      } as any;
        let totePoolBet = {
          poolBet : {
            freebetTokenValue: 5
          }
        } as any;
        expect(service['calculateStakePerLine'](totePoolBet)).toEqual(2.50);
        totePoolBet = {
          poolBet : {
          }
        } as any;
        expect(service['calculateStakePerLine'](totePoolBet)).toEqual(2.00); 
    });
  });


  describe('getToteBetSuspendedError', () => {
    it('no tote events', () => {
      expect(service['getToteBetSuspendedError']()).toBe('');
    });

    it('no suspended events', () => {
      service.toteBet = {
        outcomes: [{ id: '1' }],
        events: [{
          markets: [{
            outcomes: [{ id: '1' }]
          }]
        }]
      } as any;
      service['getToteBetSuspendedError']();
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('event suspended', () => {
      service.toteBet = {
        outcomes: [{ id: '1' }],
        events: [{
          eventStatusCode: 'S',
          markets: [{
            outcomes: [{ id: '1' }]
          }]
        }]
      } as any;
      service['getToteBetSuspendedError']();
      expect(localeService.getString).toHaveBeenCalledWith('bs.EVENT_SUSPENDED');
    });
  });

  describe('liveUpdateHandler', () => {
    it('no events', () => {
      service['liveUpdateHandler']({} as any);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    it('events updated', () => {
      service.toteBet = {
        events: [{
          linkedEventId: 1
        }]
      } as any;
      service['liveUpdateHandler']({
        event: { id : 1 },
        channel: {}
      } as any);
      expect(commandService.executeAsync).toHaveBeenCalledWith(
        commandApi.UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE, jasmine.any(Array)
      );
    });
  });

  describe('subscribeForUpdates', () => {
    it('no tote bet', () => {
      service['subscribeForUpdates']();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('subscribe for updates', () => {
      pubSubService.publish.and.callFake((p1, p2) => p2[1]());
      service.toteBet = { channelIds: [] } as any;
      service['subscribeForUpdates']();
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubApi.BETSLIP_LIVEUPDATE_SUBSCRIBE_FOR_TOTE_BETS, jasmine.any(Array)
      );
    });
  });

  describe('updateToteEventsStatuses', () => {
    it('should update event, market and outcomes', () => {
      const toteEvent: any = {
        linkedEventId: '1',
        eventStatusCode: 'A',
        markets: [{
          outcomes: [{
            linkedOutcomeId: '1',
            outcomeStatusCode: 'A'
          }]
        }]
      };

      const fixedOddsEvent: any = {
        id: '1',
        eventStatusCode: 'S',
        markets: [{
          marketStatusCode: 'S',
          outcomes: [{
            id: '1',
            outcomeStatusCode: 'S'
          }, {
            id: '2',
            outcomeStatusCode: 'S'
          }]
        }]
      };


      service.toteBet = { events: [toteEvent] } as any;

      service['updateToteEventsStatuses']([fixedOddsEvent]);

      expect(toteEvent.eventStatusCode).toBe(fixedOddsEvent.eventStatusCode);
      expect(toteEvent.markets[0].marketStatusCode).toBe(fixedOddsEvent.markets[0].marketStatusCode);
      expect(toteEvent.markets[0].outcomes[0].outcomeStatusCode).toBe(
        fixedOddsEvent.markets[0].outcomes[0].outcomeStatusCode
      );
    });

    it('no events', () => {
      service['updateToteEventsStatuses']([]);
      expect(service.toteBet).toBeFalsy();
    });

    it('should not update event', () => {
      service.toteBet = {} as any;
      service['updateToteEventsStatuses']([{}] as any);
      expect(service.toteBet.events).toBeUndefined();
    });

    it('should not update event market', () => {
      service.toteBet = {
        events: [{}]
      } as any;
      service['updateToteEventsStatuses']([{}] as any);
      expect(service.toteBet.events[0].markets).toBeUndefined();
    });

    it('should not update event market outcomes', () => {
      service.toteBet = {
        events: [{
          markets: [{}]
        }]
      } as any;
      service['updateToteEventsStatuses']([{
        markets: [{}]
      }] as any);
      expect(service.toteBet.events[0].markets[0].outcomes).toBeUndefined();
    });
  });

  it('addListeners should update currency on login/logout', () => {
    pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
    service['addListeners']();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'ToteBetslipService', [pubSubApi.SUCCESSFUL_LOGIN, pubSubApi.SESSION_LOGOUT], jasmine.any(Function)
    );
    expect(service.userCurrencyCode).toBe(userService.currency);
  });


  describe('getRoundedValue', () => {
    it('convert number ', () => {
      expect(service.getRoundedValue(2.4378)).toEqual(2.43);
    });
    it('convert string', () => {
      expect(service.getRoundedValue('2.4378')).toEqual(2.43);
    });
  });
  describe('calculateNumOfLines', () => {
    it('call calculateNumOfLines ', () => {
      let totePoolBet = {
        poolBet: {
          poolType: 'UTRI'
        },
        toteBetDetails: {
          betName: '2 bet'
        }
      }
      expect(service.calculateNumOfLines(totePoolBet)).toEqual(2);
      totePoolBet = {
        poolBet: {
          poolType: 'UEXA'
        },
        toteBetDetails: {
          betName: '1 REVERSE'
        }
      }
      expect(service.calculateNumOfLines(totePoolBet)).toEqual(2);
      totePoolBet = {
        poolBet: {
          poolType: 'UEXA'
        },
        toteBetDetails: {
          betName: '1 REVERSE1'
        }
      }
      expect(service.calculateNumOfLines(totePoolBet)).toEqual(1);
      totePoolBet = {
        poolBet: {
          poolType: 'UEXA1'
        },
        toteBetDetails: {
          betName: '1 REVERSE'
        }
      }
      service.toteBet = {
        toteBetDetails: {
          numberOfLines: 2
        }
      } as any;
      expect(service.calculateNumOfLines(totePoolBet)).toEqual(2);
      service.toteBet = {
        toteBetDetails: {
          orderedOutcomes: [{}]
        }
      } as any;
      expect(service.calculateNumOfLines(totePoolBet)).toEqual(1);
    });
    
  });
  it('should call setFreeBetsConfig', ()=> {
    service.setFreeBetsConfig(undefined);
    expect(service.freeBetsConfigData).toBeUndefined();
    expect(service.getFreeBetsConfig()).toBeUndefined();
  });
  it('should call setTokenValue', ()=> {
    service.setTokenValue('undefined');
    expect(service.tokenValue).toEqual('undefined');
    expect(service.getTokenValue()).toEqual('undefined');
  });
  it('should call setToteFreeBetText', ()=> {
    service.setToteFreeBetText('undefined');
    expect(service.freeBetText).toEqual('undefined');
    expect(service.getToteFreeBetText()).toEqual('undefined');
  });
});
