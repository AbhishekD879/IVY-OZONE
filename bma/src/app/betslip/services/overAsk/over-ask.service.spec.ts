import { of, Subject, throwError } from 'rxjs';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { discardPeriodicTasks, fakeAsync, tick } from '@angular/core/testing';
import { IBetslipBetData } from '@betslip/models/betslip-bet-data.model';
import Spy = jasmine.Spy;
import {
  offeredBetMock,
  requestedBetMock,
  betDataMock,
  confirmedBetMock,
  confirmedAndCancelledBetMock,
  notConfirmedAndNotCancelledBetMock
} from '@betslip/services/overAsk/over-ask-trader-response.mock';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ERROR_DICTIONARY } from '@core/constants/error-dictionary.constant';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { BetUtils } from '@app/bpp/services/bppProviders/bet.utils';

describe('#OverAskService', () => {
  let service: OverAskService, windowRefService, location, bppService,
    storageService, localeService,
    fracToDecService, dialogService, domToolsService, command, betslipStorageService, document, userService,
    sessionService, router,
    dynamicComponentLoader, authService, pubSubService, deviceService, logoutHandler;

  const legSP = [ { sportsLeg: { winPlaceRef: { id: 'E'}, price: { priceTypeRef: { id: 'SP' } } } } ],
        legLP = [ { sportsLeg: { winPlaceRef: { id: 'W'}, price: { priceTypeRef: { id: 'LP' } } } },
                  { sportsLeg: { winPlaceRef: { id: 'W'}, price: { priceTypeRef: { id: 'GP' } } } },
                  { sportsLeg: { winPlaceRef: { id: 'W'}, price: { priceTypeRef: { id: 'GUARANTEED' } } } }];

  const createService = () => {
    service = new OverAskService(
      windowRefService,
      location,
      bppService,
      storageService,
      localeService,
      fracToDecService,
      dialogService,
      domToolsService,
      command,
      betslipStorageService,
      document,
      userService,
      sessionService,
      router,
      dynamicComponentLoader,
      authService,
      pubSubService,
      deviceService
    );
  };

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        view: {
          mobile: true
        }
      }
    };

    location = {
      path: jasmine.createSpy()
    };

    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of({ redirectUrl: 'url' }))
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get'),
      remove: jasmine.createSpy('remove')
    };

    localeService = {
      getString: jasmine.createSpy().and.returnValue('someText')
    };

    fracToDecService = {
      getDecimal: jasmine.createSpy().and.returnValue(2.40)
    };

    dialogService = {
      openDialog: jasmine.createSpy()
    };

    domToolsService = {
      getOffset: jasmine.createSpy('getOffset').and.returnValue({})
    };

    command = {
      API: commandApi,
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve())
    };

    betslipStorageService = {
      setFreeBet: jasmine.createSpy('setFreeBet'),
      clean: jasmine.createSpy('clean'),
      cleanBetslip: jasmine.createSpy('cleanBetslip'),
      clearStateInStorage: jasmine.createSpy('clearStateInStorage')
    };

    document = {
      getElementById: jasmine.createSpy().and.returnValue({}),
      body: {
        scrollTop: 0
      }
    };

    userService = {
      username: 'name',
      status: true
    };

    sessionService = {
      whenProxySession: jasmine.createSpy('whenSession').and.returnValue(Promise.resolve())
    };

    router = {
      navigateByUrl: jasmine.createSpy()
    };

    dynamicComponentLoader = {
      loadModule: jasmine.createSpy('loadModule').and.returnValue({
        then: () => {
        }
      }),
      getDynamicComponent: jasmine.createSpy('getDynamicComponent').and.returnValue({})
    };

    authService = {
      sessionLoggedIn: of(null)
    };

    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, callback) => {
        if (method === 'SESSION_LOGOUT') {
          logoutHandler = callback;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publishSync: jasmine.createSpy('publishSync')
    };

    deviceService = {
      isOnline: jasmine.createSpy('isOnline'),
    };
    spyOn(console, 'warn');
    createService();
  });

  describe('constructor', () => {

    beforeEach(() => {
      service['restoreState'] = jasmine.createSpy();
      service['setState'] = jasmine.createSpy();
      service['readBetSubscribtion'] = {
        unsubscribe: jasmine.createSpy()
      } as any;
    });

    it('hasUserMadeDecision should be false', () => {
      expect(service['hasUserMadeDecision']).toBe(false);
    });

    it('progress flags should be false', () => {
      expect(service.isInProcess).toBe(false);
      expect(service.isInFinal).toBe(false);
    });

    it('connect syncs', () => {
      expect(service).toBeTruthy();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(service['tag'], pubSubService.API.SESSION_LOGOUT, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(service['tag'], pubSubService.API.RELOAD_COMPONENTS, jasmine.any(Function));
    });

    it('logoutHandler', (done) => {
      logoutHandler();
      expect(storageService.remove).not.toHaveBeenCalled();
      done();
    });

    it('logoutHandler (isInProcess)', (done) => {
      service.isInProcess = true;
      logoutHandler();
      expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
      expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith(false, false);
      done();
    });

    it('should subscribe to authService.sessionLoggedIn', () => {
      const sessionLoggedInSpy = spyOn(authService.sessionLoggedIn, 'subscribe');
      createService();

      expect(sessionLoggedInSpy).toHaveBeenCalled();
    });

    it('should handle error on authService.sessionLoggedIn',  fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.reject());
      createService();
      service['restoreState'] = jasmine.createSpy();
      tick();

      expect(service['restoreState']).not.toHaveBeenCalled();
    }));

    it('should call restoreState after components reload', fakeAsync(() => {
      pubSubService.subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback());
      createService();
      service['restoreState'] = jasmine.createSpy();
      tick();

      expect(service['restoreState']).toHaveBeenCalledTimes(2);
    }));
  });

  describe('ngOnDestroy', () => {
    it('should emit destroyed$', () => {
      const spyOnNext = spyOn(service['destroyed$'] as Subject<null>, 'next');
      const spyOnComplete = spyOn(service['destroyed$'] as Subject<null>, 'complete');

      service.ngOnDestroy();

      expect(spyOnNext).toHaveBeenCalled();
      expect(spyOnComplete).toHaveBeenCalled();
    });
  });

  it('clearBetsData', () => {
    service.clearBetsData();
    expect(service['betsData']).toBeDefined();
    expect(service['isBetsDataAssigned']).toBeFalsy();
  });

  it('showOveraskInProgressNotification', () => {
    windowRefService.nativeWindow.view.mobile = false;

    service.showOveraskInProgressNotification();
    expect(dynamicComponentLoader.loadModule).toHaveBeenCalledWith('@betslipModule/betslip.module#BetslipModule');
  });

  describe('setBetsData', () => {
    it('should setBetsData (!isInProcess)', () => {
      const betslipData = [{ error: 'OUTCOME_SUSPENDED' }, { error: 'SOME_ERROR' }];

      service.setBetsData(<any>betslipData);

      expect(betslipData[0].error).toEqual('OUTCOME_SUSPENDED');
    });

    it('should setBetsData (isInProcess)', () => {
      const betslipData = [
        { error: 'EVENT_STARTED' },
        { error: 'OUTCOME_SUSPENDED' },
        { error: 'SOME_ERROR' }, { errorMsg: 'msg' },
        { errorMsg: 'test' }
      ];
      service.isInProcess = true;
      localeService.getString.and.returnValue('test');

      service.setBetsData(<any>betslipData);

      expect(betslipData[0].error).toEqual('');
      expect(betslipData[1].error).toEqual('OUTCOME_SUSPENDED');
      expect(betslipData[2].error).toEqual('SOME_ERROR');
      expect(betslipData[3].errorMsg).toEqual('msg');
      expect(betslipData[4].errorMsg).toEqual('');
    });

    it('should setBetsData (hasTraderMadeDecision)', () => {
      const betslipData = [{ error: 'OUTCOME_SUSPENDED' }, { error: 'SOME_ERROR' }];

      service.hasTraderMadeDecision = true;
      service['updateBetsData'] = jasmine.createSpy('updateBetsData');
      service.setBetsData(<any>betslipData);
      expect(service['updateBetsData']).toHaveBeenCalled();
    });
  });

  describe('checkHasTraderMadeDecision', () => {
    let response;
    let result;

    beforeEach(() => {
      response = notConfirmedAndNotCancelledBetMock;
      service['getBetKey'] = jasmine.createSpy('getBetKey').and.returnValue(response);
    });

    it ('should return true and call getBetKey1', () => {
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it ('should return true and not call getBetKey2', () => {
      response = confirmedBetMock;
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).not.toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it ('should return false and call getBetKey3', () => {
      response = {
        bet: [ confirmedBetMock.bet[0], confirmedBetMock.bet[1], notConfirmedAndNotCancelledBetMock.bet[1] ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(false);
    });

    it ('should return true and not call getBetKey4', () => {
      response = confirmedAndCancelledBetMock;
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).not.toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it ('should return false and call getBetKey5', () => {
      response = {
        bet: [ notConfirmedAndNotCancelledBetMock.bet[0] ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(false);
    });

    it ('should return false and call getBetKey6', () => {
      response = {
        bet: [ notConfirmedAndNotCancelledBetMock.bet[0], confirmedBetMock.bet[0] ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(false);
    });
  });

  describe('isOverask', () => {
    it('should check if isOverask (true)', () => {
      const betData = {
        bets: [
          {
            isReferred: 'Y'
          },
          {
            isReferred: 'N'
          }
        ]
      };
      expect(service.isOverask(<any>betData)).toEqual(true);
    });

    it('should check if isOverask (false)', () => {
      const betData = {
        bets: [
          {
            isReferred: 'N'
          },
          {
            isReferred: 'N'
          }
        ]
      };
      expect(service.isOverask(<any>betData)).toEqual(false);
    });
  });

  describe('acceptOffer', () => {

    beforeEach(() => {
      service['hasUserMadeDecision'] = false;
    });

    it('should acceptOffer', fakeAsync(() => {
      service['getBetIds'] = jasmine.createSpy('getBetIds');

      const betData = { bets: [{ id: 1 }, { id: 2, isSelected: true, betId: 2 }] };
      const betslipData = [{ type: 'SGL' }, { error: 'SOME_ERROR' }];

      service.setBetsData(<any>betslipData);
      service.execute(<any>betData).subscribe(() => {
        expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
        discardPeriodicTasks();
      });

      service.acceptOffer();

      expect(service['getBetIds']).toHaveBeenCalled();
    }));

    it('should acceptOffer (fail)', fakeAsync(() => {
      const betData = { bets: [{ id: 1 }, { id: 2, isSelected: true, betId: 2 }] };
      const betslipData = [{ type: 'SGL' }, { error: 'SOME_ERROR' }];
      bppService.send.and.returnValue(of({ message: 'message' }));

      service.setBetsData(<any>betslipData);
      service.execute(<any>betData).subscribe(null, () => {
        expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
        discardPeriodicTasks();
      });

      service.acceptOffer();
    }));

    it('should acceptOffer (fail)', fakeAsync(() => {
      const betData = { bets: [{ id: 1 }, { id: 2, isSelected: true, betId: 2 }] };
      const betslipData = [{ type: 'SGL' }, { error: 'SOME_ERROR' }];
      bppService.send.and.returnValue(of({
        offerBetAction: [{
          status: 'ERROR'
        }]
      }));

      service.setBetsData(<any>betslipData);
      service.execute(<any>betData).subscribe(null, () => {
        expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
        discardPeriodicTasks();
      });

      service.acceptOffer();
    }));

    it('should acceptOffer(error)', fakeAsync(() => {
      const betData = { bets: [{ id: 1 }] };
      bppService.send.and.returnValue(of({ betError: 'error' }));
      service.execute(<any>betData).subscribe(null, () => {
        expect(storageService.remove).toHaveBeenCalledWith('overaskIsInProcess');
        expect(storageService.remove).toHaveBeenCalledWith('overaskUsername');
        expect(storageService.remove).toHaveBeenCalledWith('overaskPlaceBetsData');
        discardPeriodicTasks();
      });

      service.acceptOffer();
      tick();
    }));

    it('should do nothing if process is pending', () => {
      service['hasUserMadeDecision'] = true;
      service['clearOfferTimeout'] = jasmine.createSpy('clearOfferTimeout');
      service['getSelectedBetIds'] = jasmine.createSpy('getSelectedBetIds');
      service['acceptOrRejectOffer'] = jasmine.createSpy('acceptOrRejectOffer');

      service.acceptOffer();

      expect(service['clearOfferTimeout']).not.toHaveBeenCalled();
      expect(service['getSelectedBetIds']).not.toHaveBeenCalled();
      expect(service['acceptOrRejectOffer']).not.toHaveBeenCalled();
      expect(bppService.send).not.toHaveBeenCalled();
    });

    describe('PT_ERR_AUTH error', () => {
      const error = {
        error: {
          error: '9516 - PT_ERR_AUTH coral::bet::pre_place_bets_callback: funds reservation failed: PT_ERR_AUTH'
        }
      };
      const ecpextedError = {
        data: {
          status: 'PT_ERR_AUTH',
          message: jasmine.any(String)
        }
      } as any;

      beforeEach(() => {
        spyOn<any>(service, 'processOveraskFlow');
        spyOn<any>(service, 'finisWithFailure');
      });

      it('should check PT_ERR_AUTH error if failure response', fakeAsync(() => {
        spyOn<any>(service, 'acceptOrRejectOffer').and.returnValue(throwError(error));

        service.acceptOffer();
        tick();
        expect(service['processOveraskFlow']).not.toHaveBeenCalled();
        expect(service['finisWithFailure']).toHaveBeenCalledWith(ecpextedError as any);
      }));

      it('should check any error if failure response', fakeAsync(() => {
        const err = { mess: 'error', type: 'any' } as any;
        spyOn<any>(service, 'acceptOrRejectOffer').and.returnValue(throwError(err));

        service.acceptOffer();
        tick();
        expect(service['processOveraskFlow']).not.toHaveBeenCalled();
        expect(service['finisWithFailure']).toHaveBeenCalledWith(err as any);
      }));

      it('should check PT_ERR_AUTH error if success response', fakeAsync(() => {
        spyOn<any>(service, 'acceptOrRejectOffer').and.returnValue(of(error));

        service.acceptOffer();
        tick();
        expect(service['processOveraskFlow']).not.toHaveBeenCalled();
        expect(service['finisWithFailure']).toHaveBeenCalledWith(ecpextedError as any);
      }));
    });
  });

  describe('@rejectOffer', () => {
    let betData, betslipData;

    beforeEach(() => {
      betData = { bets: [{ id: 1, outcomeId: 10 }, {}] };
      betslipData = [{ type: 'SGL' }, { error: 'SOME_ERROR' }];

      service.setBetsData(<any>betslipData);
      service.execute(<any>betData).subscribe(null, () => { });
      spyOn(service as any, 'acceptOrRejectOffer').and.returnValue(of({}));
      spyOn(service as any, 'getSinglesOutcomesIds').and.callThrough();
    });

    it('should clean betslip', () => {
      service.rejectOffer().subscribe(() => {
        expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith(false, true);
      });
    });

    it('should rejectOffer(error)', () => {
      bppService.send.and.returnValue(throwError({}));

      service.rejectOffer().subscribe(() => {
        expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
      });
    });

    it('should call OVERASK_CLEAN_BETSLIP', () => {
      spyOn(service as any, 'finisWithFailure');

      service.rejectOffer().subscribe(() => {
        expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith(false, true);
      });
    });

    it('should reuse selections', () => {
      service.rejectOffer().subscribe(() => {
        expect(command.executeAsync).toHaveBeenCalledWith(jasmine.any(String), jasmine.any(Array));
        expect(pubSubService.publishSync).toHaveBeenCalledWith('REFRESH_BETSLIP');
      });
    });

    it('should NOT reuse selections', () => {
      service.rejectOffer(false).subscribe(() => {
        expect(command.executeAsync).not.toHaveBeenCalled();
        expect(pubSubService.publishSync).not.toHaveBeenCalledWith('REFRESH_BETSLIP');
      });
    });

    it('should call cancellOveraskProcess with cleanBetslip props', () => {
      const spy = spyOn(service, 'cancelOveraskProcess');
      service.rejectOffer(true, false).subscribe(() => {
        expect(spy).toHaveBeenCalledWith(false, true, false);
      });
    });

    it('should call cancellOveraskProcess with defoult props', () => {
      const spy = spyOn(service, 'cancelOveraskProcess');
      service.rejectOffer().subscribe(() => {
        expect(spy).toHaveBeenCalledWith(false, true, true);
      });
    });

    it('should be used default value of the argument if not passed', () => {
      const spy = spyOn(service, 'cancelOveraskProcess');
      service.rejectOffer().subscribe(() => {
        expect(spy).toHaveBeenCalled();
      });
    });
  });

  describe('@cancelOveraskProcess', () => {

    beforeEach(() => {
      userService.status = false;
    });

    it('should cancelOveraskProcess (true)', () => {
      service.cancelOveraskProcess(true, true);

      expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith( true, true );
    });

    it('should cancelOveraskProcess (true) not closing sidebar', () => {
      service.cancelOveraskProcess(undefined, true);

      expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith( false, true );
    });

    it('should use def params', () => {
      service.cancelOveraskProcess();

      expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith( false, false );
    });

    it(`should Not cleanBetslip if prop cleanBetslip is falthy`, () => {
      service.cancelOveraskProcess(undefined, undefined, false);

      expect(betslipStorageService.cleanBetslip).not.toHaveBeenCalled();
    });

    it(`should cleanBetslip if prop cleanBetslip is not defined`, () => {
      service.cancelOveraskProcess();

      expect(betslipStorageService.cleanBetslip).toHaveBeenCalled();
    });
  });

  describe('sortDeclinedBetsOnTop', () => {
    it('should sortDeclinedBetsOnTop (isTraderDeclined > 2)', () => {
      const betsData = [{ isTraderDeclined: false }, { isTraderDeclined: true }, { isTraderDeclined: true }];
      expect(service.sortDeclinedBetsOnTop(<any>betsData)[1].isTraderDeclined).toEqual(true);
    });

    it('should sortDeclinedBetsOnTop (isTraderDeclined < 2)', () => {
      const betsData = [{ isTraderDeclined: false }, { isTraderDeclined: false }, { isTraderDeclined: true }];
      expect(service.sortDeclinedBetsOnTop(<any>betsData)[1].isTraderDeclined).toEqual(false);
    });
  });

  describe('sortLinkedBets', () => {
    it('should sort bets in particular order', () => {
      const betsData = [
        { betId: 1 },
        { betId: 2, dependsOn: 1 },
        { betId: 3, dependsOn: 1 },
        { betId: 4, dependsOn: null }
      ] as IBetslipBetData[];
      service['defineIsRemovable'] = jasmine.createSpy('defineIsRemovable').and.returnValue(true);

      const result = service.sortLinkedBets(betsData);

      expect(result[0]).toEqual({ betId: 4, dependsOn: null} as IBetslipBetData);
      expect(result[1]).toEqual({ betId: 1, children: [2, 3]} as any);
      expect(result[2]).toEqual({ betId: 2, dependsOn: 1 } as any);
      expect(result[3]).toEqual({ betId: 3, dependsOn: 1 } as any);
      expect(service['defineIsRemovable']).toHaveBeenCalledTimes(6);
    });
  });

  describe('showOveraskInProgressNotification', () => {
    it('should showOveraskInProgressNotification', () => {
      windowRefService.nativeWindow.view.mobile = false;
      dynamicComponentLoader.loadModule = jasmine.createSpy('loadModule').and.returnValue(Promise.resolve(
        {
          componentFactoryResolver: {
            resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
          }
        }
      ));
      service.showOveraskInProgressNotification();
      expect(dynamicComponentLoader.loadModule).toHaveBeenCalled();
    });

    it('should showOveraskInProgressNotification (mobile)', () => {
      service.showOveraskInProgressNotification();
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', true);
    });
  });

  describe('@restoreState', () => {

    it('should restoreState', fakeAsync(() => {
      spyOn(service as any, 'executeInternal').and.returnValue(of({}));
      storageService.get.and.returnValue('name');
      service.isInProcess = false;
      service['restoreState']();
      tick();

      expect(service.isInProcess).toBeTruthy();
      expect(storageService.get).toHaveBeenCalledWith('overaskUsername');
      expect(storageService.get).toHaveBeenCalledWith('overaskPlaceBetsData');
      expect(pubSubService.publishSync).toHaveBeenCalledWith('OVERASK_STATE_RESTORED', jasmine.anything());
    }));

    it('should restoreState (error)', fakeAsync(() => {
      storageService.get.and.returnValue('name');
      bppService.send.and.returnValue(throwError('test'));
      service['restoreState']();
      tick();

      expect(pubSubService.publishSync).toHaveBeenCalledWith('OVERASK_STATE_RESTORE_FAILED', 'test');
    }));

    it('should restoreState (not isInProcess)', () => {
      storageService.get.and.callFake((param) => {
        return param !== 'overaskIsInProcess' ? 'name' : false;
      });
      service.isInProcess = true;
      service['restoreState']();

      expect(service.isInProcess).toBeFalsy();
      expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
    });
  });

  it('should clearOfferTimeout', () => {
    service['offerTimerSubscription'] = <any>{
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    service['clearOfferTimeout']();
    expect(service['offerTimerSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('should check if isNumbersDifferent', () => {
    expect(service['isNumbersDifferent']('f', 'f')).toEqual(false);
  });

  describe('updateBetData', () => {
    let betData, bet;

    beforeEach(() => {
      betData = {
        Bet: {
          stake: {
            amount: 12,
            stakePerLine: '12.0'
          },
          isEachWay: true,
          legs: [
            {
              firstOutcomeId: 10,
              price: {
                props: {
                  priceNum: 3,
                  priceDen: 3,
                  priceType: 'RP'
                }
              },
              parts: [
                {
                  outcome: {}
                }
              ]
            }
          ]
        },
        price: {
          priceNum: 3,
          priceDen: 3,
          priceType: 'LP'
        },
        isSP: false
      } as any;

      bet = {
        id: 10,
        isOffer: 'Y',
        offer: {
          stake: {
            amount: 12,
            stakePerLine: '12.0'
          },
          payout: [
            {
              potential: 10
            }
          ],
          leg: [
            {
              sportsLeg: {
                legPart: [
                  {
                    outcomeRef: {
                      id: 10
                    }
                  }
                ],
                price: {
                  priceTypeRef: {
                    id: 'SP'
                  },
                  priceNum: 3,
                  priceDen: 3
                },
                winPlaceRef: {
                  id: 'E'
                }
              }
            }
          ]
        }
      };
    });

    it('should updateBetData (isCancelled)', () => {
      betData = {};
      bet = { id: 10, isCancelled: 'Y' };

      service['updateBetData'](<any>{ betData, bet });
      expect(<any>betData).toEqual(jasmine.objectContaining({
        betId: 10,
        isTraderDeclined: true
      }));
    });

    it('should updateBetData (isConfirmed, isNoBetsOffered)', () => {
      betData = {};
      bet = { id: 10, isConfirmed: 'Y' };
      service.isNotDeletedFromTraderOffer = jasmine.createSpy('isNotDeletedFromTraderOffer').and.returnValue(true);

      service['updateBetData'](<any>{ betData, bet });

      expect(<any>betData).toEqual(jasmine.objectContaining({
        isTraderAccepted: true,
        isSelected: true,
        overaskMessage: 'someText'
      }));
    });

    it('should updateBetData (isConfirmed)', () => {
      betData = {};
      bet = { id: 10, isConfirmed: 'Y' };

      service.isNoBetsOffered = false;
      service['updateBetData'](<any>{ betData, bet });

      expect(<any>betData).toEqual(jasmine.objectContaining({
        isTraderAccepted: true,
        isSelected: true
      }));
    });

    it('should updateBetData and price (isConfirmed)', () => {
      betData = { price: {} };
      bet = {
        id: 10,
        isConfirmed: 'Y',
        leg: [{
          sportsLeg: {
            price: { priceNum: '1', priceDen: '2', priceTypeRef: { id: 'LP' } }
          }
        }]
      };

      service['updateBetData']({ betData, bet });

      expect(betData.price).toEqual(jasmine.objectContaining({ priceNum: '1', priceDen: '2' }));
    });

    it('should updateBetData (isOffer)', () => {
      betData.Bet.stake = {
        amount: 5
      };
      betData.Bet.legs = [
        {
          firstOutcomeId: 10,
          price: {
            props: {
              priceNum: 1,
              priceDen: 3,
              priceType: 'SP'
            }
          },
          parts: [
            {
              outcome: {}
            }
          ]
        },
        {
          firstOutcomeId: 7,
          price: {
            props: {
              priceNum: 1,
              priceDen: 3,
              priceType: 'SP'
            }
          },
          parts: [
            {
              outcome: {}
            }
          ]
        }];
      betData.Bet.leg = legSP;
      bet.offer.stake = {
        amount: 6,
        stakePerLine: 2
      };
      bet.offer.leg[0].sportsLeg.price.priceTypeRef.id = 'LP';
      bet.offer.leg[0].sportsLeg.winPlaceRef.id = 'W';
      bet.masterBetId = '000_03';
      service['originalPlacedBets'][bet.masterBetId] = betData.Bet;

      service['updateBetData'](<any>{ betData, bet });

      expect(<any>betData).toEqual(jasmine.objectContaining({
        isTraderOffered: true,
        potentialPayout: 10,
        isSP: false,
        isSPLP: false,
        traderChangedPriceType: true,
        tokenValue: 0
      }));

    });

    it('should updateBetData (isOffer)', () => {
      betData.Bet.stake = {
        amount: 5
      };
      betData.Bet.legs = [
        {
          firstOutcomeId: 10,
          price: {
            props: {
              priceNum: 3,
              priceDen: 3,
              priceType: 'SP'
            }
          },
          parts: [{ outcome: {} }]
        }];
      betData.Bet.leg = legSP;

      bet.offer.stake = {
        amount: 6,
        stakePerLine: 2
      };
      bet.offer.leg[0].sportsLeg.price.priceTypeRef.id = 'SP';
      bet.offer.leg[0].sportsLeg.winPlaceRef.id = 'E';
      bet.masterBetId = '000_03';
      service['originalPlacedBets'][bet.masterBetId] = betData.Bet;

      service['updateBetData'](<any>{ betData, bet });

      expect(betData).toEqual(jasmine.objectContaining({
        isTraderOffered: true,
        potentialPayout: 10,
        isSP: true
      }));
      expect(betData.isSPLP).toBeUndefined();
      expect(betData.traderChangedPriceType).toBeUndefined();
    });

    describe('tokenValue', () => {
      beforeEach(() => {
        spyOn<any>(service, 'updateBetPriceData');
        spyOn<any>(service, 'isPricesChanged');

        betData.Bet.stake = {
          amount: 5
        };
        betData.Bet.legs = [{
          firstOutcomeId: 10,
          price: {
            props: {
              priceNum: 3,
              priceDen: 3,
              priceType: 'SP'
            }
          },
          parts: [{ outcome: {} }]
        }];
        bet.offer.leg = legSP;
        bet.offer.stake = {
          amount: 6,
          stakePerLine: 2
        };
      });

      it('should set tokenValue by master bet', () => {
        bet.masterBetId = 100;
        service['originalPlacedBets'] = {100: {tokenValue: '1.50', stake: {}, leg: legSP}} as any;
        service['updateBetData'](<any>{ betData, bet });

        expect(betData.tokenValue).toEqual(1.5);
        expect(betData.potentialPayout).toEqual(10);
      });

      it('should set tokenValue 0 if master bet have no tokenValue', () => {
        bet.masterBetId = 100;
        service['originalPlacedBets'] = {100: {stake: {}, leg: legSP}} as any;
        service['updateBetData'](<any>{ betData, bet });

        expect(betData.tokenValue).toEqual(0);
        expect(betData.potentialPayout).toEqual(10);
      });

      it('should set tokenValue 0 if master bet tokenValue not proper', () => {
        bet.masterBetId = 100;
        service['originalPlacedBets'] = {100: {tokenValue: 'Some', stake: {}, leg: legSP}} as any;
        service['updateBetData'](<any>{ betData, bet });

        expect(betData.tokenValue).toEqual(0);
        expect(betData.potentialPayout).toEqual(10);
      });

      it('should set N/A', () => {
        bet.masterBetId = 100;
        bet.offer.payout = null;
        service['originalPlacedBets'] = {100: {tokenValue: '50.50', stake: {}, leg: legSP}} as any;
        service['updateBetData'](<any>{ betData, bet });

        expect(betData.potentialPayout).toEqual('N/A');
      });
    });

    it('should change price type to SP', () => {
      bet.masterBetId = '000_03';
      betData.Bet.leg = legLP;
      service['originalPlacedBets'][bet.masterBetId] = betData.Bet;
      service['updateBetData'](<any>{ betData, bet });

      expect(betData.isSP).toEqual(true);
      expect(betData.isSPLP).toEqual(false);
      expect(betData.traderChangedPriceType).toEqual(true);
    });

    it('should set price type if prise exists', () => {
      bet.masterBetId = '000_03';
      betData.Bet.leg = legSP;
      service['originalPlacedBets'][bet.masterBetId] = betData.Bet;
      service['updateBetData'](<any>{ betData, bet });

      expect(betData.price.priceType).toBe('SP');
    });

    it('should not set price type if no price were found', () => {
      bet.masterBetId = '000_03';
      betData.Bet.leg = legSP;
      service['originalPlacedBets'][bet.masterBetId] = betData.Bet;
      betData.price = undefined;
      service['updateBetData'](<any>{ betData, bet });

      expect(betData.price).not.toBeDefined();
    });

    it('should set isEachWay false for EXPLICIT_PLACES (tricast/forecast)', () => {
      betData.Bet.isEachWay = true;
      bet.masterBetId = 751693;
      bet.offer.leg[0].sportsLeg.winPlaceRef.id = 'EXPLICIT_PLACES';
      betData.Bet.leg = legSP;
      service['originalPlacedBets'] = {751693: requestedBetMock};
      service['updateBetData']({betData, bet});

      expect(betData.Bet.isEachWay).toBe(false);

      bet.offer.leg[0].sportsLeg.winPlaceRef.id = 'E';
    });

    it('Should isEachWay to be true', () => {
      betData.Bet.isEachWay = false;
      betData.Bet.leg = legSP;
      bet.masterBetId = 751693;
      service['originalPlacedBets'] = {751693: requestedBetMock};

      service['updateBetData']({betData, bet});

      expect(betData.Bet.isEachWay).toBe(true);
    });

    it('Should traderChangedLegType to be true', () => {
      betData.betId = 751693;
      betData.Bet.leg = legSP;
      bet.id = 751693;
      bet.masterBetId = '000_03';
      service['originalPlacedBets'][bet.masterBetId] = {stake: {}, leg: legLP};
      service['updateBetData']({betData, bet});

      expect(betData.traderChangedLegType).toBe(true);

    });

    it('Should traderChangedLegType to be false', () => {
      betData.Bet.leg = legSP;
      bet.offer.leg[0].sportsLeg.winPlaceRef.id = 'W';
      bet.masterBetId = 10;
      service['originalPlacedBets'] = {10: requestedBetMock};

      service['updateBetData']({betData, bet});

      expect(betData.traderChangedLegType).toBe(false);
    });

    it('should set isSP false for LP | GP | GUARANTEED price types', () => {
      bet.isOffer = 'Y';
      bet.offer.leg = [
        {sportsLeg: {price: {priceTypeRef: {id: 'LP'}}, winPlaceRef: {id: ''}}},
        {sportsLeg: {price: {priceTypeRef: {id: 'GP'}}, winPlaceRef: {id: ''}}},
        {sportsLeg: {price: {priceTypeRef: {id: 'GUARANTEED'}}, winPlaceRef: {id: ''}}}
      ] as any;
      bet.masterBetId = '000_03';
      service['originalPlacedBets'][bet.masterBetId] = {stake: {}, leg: legSP};

      service['updateBetPriceData'] = jasmine.createSpy('updateBetPriceData').and.returnValue({});
      service['isPricesChanged'] = jasmine.createSpy('isPricesChanged').and.returnValue(false);

      service['updateBetData']({betData, bet});

      expect(betData.isSP).toEqual(false);
    });

    describe('setting flag traderChangedStake', () => {
      const masterBetId = '000_00';

      beforeEach(() => {
        bet.masterBetId = masterBetId;
        service['originalPlacedBets'][bet.masterBetId] = {stake: {}};
      });

      it('should change stakePerLine when trader changed offer', () => {
        bet.masterBetId = '12345';
        service['originalPlacedBets'][bet.masterBetId] = { stake: { stakePerLine: '1.0' }, leg: legSP};

        bet.offer.stake.stakePerLine = '6.0';

        service['updateBetData'](<any>{ betData, bet });

        expect(betData.Bet.stake).toEqual(6);
        expect(betData.traderChangedStake).toBeTruthy();
      });

      it('should set flag traderChangedStake if multiple bet and stakePerLine is changed', () => {
        betData.traderChangedStake = false;
        betData.type = 'DBL';
        bet.masterBetId = '000_03';
        service['originalPlacedBets'][bet.masterBetId] = { stake: { stakePerLine: '23'}, leg: legSP };

        service['updateBetData'](<any>{ betData, bet });

        expect(betData.traderChangedStake).toBeTruthy();
      });
    });

    it('should update price anyway to get actual price (e.g. odds boosted) if betData has price', () => {
      const betDataOddsBoostMock = {
        Bet: {
          stake: {
            amount: 5
          },
          isEachWay: true,
          legs: [
            {
              firstOutcomeId: 10,
              price: {
                props: {
                  priceNum: 3,
                  priceDen: 3,
                  priceType: 'LP'
                }
              },
              parts: [
                {
                  outcome: {}
                }
              ]
            }
          ]
        },
        price: {
          priceNum: 3,
          priceDen: 3,
          priceType: 'LP'
        },
        isSP: false
      } as any;

      const betOddsBoostMock = {
        id: 10,
        isOffer: 'Y',
        offer: {
          stake: {
            amount: 6,
            stakePerLine: 2
          },
          payout: [
            {
              potential: 10
            }
          ],
          leg: [
            {
              sportsLeg: {
                legPart: [
                  {
                    outcomeRef: {
                      id: 10
                    }
                  }
                ],
                price: {
                  priceTypeRef: {
                    id: 'LP'
                  },
                  priceNum: 50,
                  priceDen: 1
                },
                winPlaceRef: {
                  id: 'E'
                }
              }
            }
          ]
        }
      } as any;
      service['isPricesChanged'] = jasmine.createSpy('isPricesChanged').and.returnValue(false);
      service['originalPlacedBets'][betOddsBoostMock.id] = {stake: {}, leg: legSP};

      service['updateBetData'](<any>{ betData: betDataOddsBoostMock, bet: betOddsBoostMock });

      expect(betDataOddsBoostMock.traderChangedOdds).toBeUndefined();
      expect(betDataOddsBoostMock.price.priceNum).toEqual(50);
      expect(betDataOddsBoostMock.price.priceDen).toEqual(1);
    });

    it('should not update price if betData does not have price', () => {
      spyOn<any>(service, 'isPricesChanged');

      const betDataOddsBoostMock = {
        Bet: {
          stake: {
            amount: 5
          },
          isEachWay: true,
          legs: [
            {
              firstOutcomeId: 10,
              price: {
                props: {
                  priceNum: 3,
                  priceDen: 3,
                  priceType: 'LP'
                }
              },
              parts: [
                {
                  outcome: {}
                }
              ]
            }
          ],
          leg: legLP
        },
        isSP: false
      } as any;

      const betOddsBoostMock = {
        id: 10,
        isOffer: 'Y',
        offer: {
          stake: {
            amount: 6,
            stakePerLine: 2
          },
          payout: [
            {
              potential: 10
            }
          ],
          leg: [
            {
              sportsLeg: {
                legPart: [
                  {
                    outcomeRef: {
                      id: 10
                    }
                  }
                ],
                price: {
                  priceTypeRef: {
                    id: 'LP'
                  },
                  priceNum: 50,
                  priceDen: 1
                },
                winPlaceRef: {
                  id: 'E'
                }
              }
            }
          ]
        }
      } as any;
      service['originalPlacedBets'][betOddsBoostMock.id] = {stake: {}, leg: legLP};

      service['updateBetData'](<any>{ betData: betDataOddsBoostMock, bet: betOddsBoostMock });

      expect(betOddsBoostMock.traderChangedOdds).toBeUndefined();
      expect(betOddsBoostMock.price).toBeUndefined();
    });

    it('should set Bet.stake as 0 if stake.stakePerline is undefined', () => {
      betData.traderChangedStake = false;
      bet.masterBetId = '000_03';
      service['originalPlacedBets'][bet.masterBetId] = { stake: { stakePerLine: '23'}, leg: legSP };
      bet.offer.stake.stakePerLine = null;

      service['updateBetData'](<any>{ betData, bet });

      expect(betData.Bet.stake).toBe(0);
    });
  });

  describe('isBetDataWithFreeBetAndChangedStake', () => {
    const masterBetId = '000_01';
    let betData, bet, betPairs;

    beforeEach(() => {
      service['originalPlacedBets'] = {
        '000_01': {stake: { stakePerLine: 5 }},
        '111_01': {stake: { stakePerLine: 100 }},
      } as any;
      betData = {
        Bet: {
          freeBet: { id: 'id' },
          leg: legSP
        }
      };
      bet = {
        id: '111_01',
        masterBetId: masterBetId,
        stake: {
          stakePerLine: 5
        },
        leg: legSP
      };
      betPairs = { betData, bet };

      spyOn<any>(BetslipBetDataUtils, 'isFreeBetUsed').and.returnValue(true);
      spyOn<any>(BetUtils, 'isOffer').and.returnValue(true);
      spyOn<any>(service, 'isNumbersDifferent').and.returnValue(true);
    });

    it('should return false if freeBet is not used', () => {
      (BetslipBetDataUtils.isFreeBetUsed as jasmine.Spy).and.returnValue(false);
      const result = service['isBetDataWithFreeBetAndChangedStake'](<any>betPairs);

      expect(result).toEqual(false);
    });

    it('should return false if freeBet is not offered', () => {
      (BetUtils.isOffer as jasmine.Spy).and.returnValue(false);
      const result = service['isBetDataWithFreeBetAndChangedStake'](<any>betPairs);

      expect(result).toEqual(false);
    });

    it('should return false if freeBet is not offered', () => {
      (service['isNumbersDifferent'] as jasmine.Spy).and.returnValue(false);
      const result = service['isBetDataWithFreeBetAndChangedStake'](<any>betPairs);

      expect(result).toEqual(false);
    });

    it('should return true and get original bet by bet.masterBetId', () => {
      const result = service['isBetDataWithFreeBetAndChangedStake'](<any>betPairs);

      expect(result).toEqual(true);
      expect(service['isNumbersDifferent']).toHaveBeenCalledWith(5, 5);
    });

    it('should return true and get original bet by bet.id', () => {
      bet.masterBetId = null;
      const result = service['isBetDataWithFreeBetAndChangedStake'](<any>betPairs);

      expect(result).toEqual(true);
      expect(service['isNumbersDifferent']).toHaveBeenCalledWith(100, 5);
    });
  });

  it('should check if isBetsDataWithFreeBetAndChangedStake', () => {
    const betData = {
      Bet: {
        freeBet: {
          id: 10
        }
      }
    };
    const bet = {
      isOffer: 'N'
    };
    const betPairs = [{ betData, bet }];
    expect(service['isBetsDataWithFreeBetAndChangedStake'](<any>betPairs)).toEqual(false);
  });

  describe('checkIsMatchBetsToBetsDataNotSuccess', () => {
    it('should checkIsMatchBetsToBetsDataNotSuccess (!isBetsDataAssigned)', () => {
      const betData = {};
      const bet = {};
      const betPairs = [{ betData, bet }];
      expect(service['checkIsMatchBetsToBetsDataNotSuccess'](<any>betPairs)).toEqual(false);
    });

    it('should checkIsMatchBetsToBetsDataNotSuccess', () => {
      const betData = {};
      const bet = {};
      const betPairs = [{ betData, bet }];
      service['isBetsDataAssigned'] = true;
      service['placeBetsData'] = <any>{
        bets: []
      };
      expect(service['checkIsMatchBetsToBetsDataNotSuccess'](<any>betPairs)).toEqual(true);
    });
  });

  describe('updateBetsData', () => {
    it('should updateBetsData (!checkIsMatchBetsToBetsDataNotSuccess)', () => {
      const betData = {};
      const bet = {};
      service['matchBetsToBetsData'] = jasmine.createSpy('matchBetsToBetsData').and.returnValue([{
        betData,
        bet
      }]);
      service['checkIsMatchBetsToBetsDataNotSuccess'] = jasmine.createSpy('checkIsMatchBetsToBetsDataNotSuccess')
        .and.returnValue(true);

      service['updateBetsData']();
      expect(betslipStorageService.setFreeBet).not.toHaveBeenCalled();
    });

    it('should updateBetsData (isBetsDataWithFreeBetAndChangedStake)', fakeAsync(() => {
      const betData = {
        Bet: {
          freebet: {}
        },
        stake: {
          freeBetAmount: '5'
        },
        id: 'SGL|10'
      };
      const bet = {};
      service['matchBetsToBetsData'] = jasmine.createSpy('matchBetsToBetsData').and.returnValue([{
        betData,
        bet
      }]);
      service['checkIsMatchBetsToBetsDataNotSuccess'] = jasmine.createSpy('checkIsMatchBetsToBetsDataNotSuccess')
        .and.returnValue(false);
      service['isBetsDataWithFreeBetAndChangedStake'] = jasmine.createSpy('isBetsDataWithFreeBetAndChangedStake')
        .and.returnValue(true);
      service['isBetDataWithFreeBetAndChangedStake'] = jasmine.createSpy('isBetDataWithFreeBetAndChangedStake')
        .and.returnValue(true);
      service.rejectOffer = jasmine.createSpy('rejectOffer').and.returnValue(of({}));

      service['updateBetsData']();
      tick();
      expect(betslipStorageService.setFreeBet).toHaveBeenCalledWith(betData);
      expect(localeService.getString).toHaveBeenCalledWith('bs.freeBetsAvalaible');
      expect(localeService.getString).toHaveBeenCalledWith('bs.overaskMessages.someBetsWithFreebet');
      expect(pubSubService.publish).toHaveBeenCalledWith('BETSLIP_CLEAR_STAKE', 'SGL|10');
    }));

    it('should updateBetsData (!checkIsMatchBetsToBetsDataNotSuccess && !isBetsDataWithFreeBetAndChangedStake)', () => {
      const betData = {};
      const bet = {};
      service['matchBetsToBetsData'] = jasmine.createSpy('matchBetsToBetsData').and.returnValue([{
        betData,
        bet
      }]);
      service['checkIsMatchBetsToBetsDataNotSuccess'] = jasmine.createSpy('checkIsMatchBetsToBetsDataNotSuccess')
        .and.returnValue(false);
      service['isBetsDataWithFreeBetAndChangedStake'] = jasmine.createSpy('isBetsDataWithFreeBetAndChangedStake')
        .and.returnValue(false);
      service['updateBetData'] = jasmine.createSpy('updateBetData');

      service['updateBetsData']();

      expect(service['updateBetData']).toHaveBeenCalledTimes(1);
    });
  });

  describe('isPriceTypeChange', () => {
    it('should check if isPriceTypeChange (true)', () => {
      const leg = {
        price: {
          priceType: 'SP'
        }
      };
      const offeredLeg = { priceType: 'LP' };

      expect(service['isPriceTypeChange'](<any>leg, <any>offeredLeg)).toEqual(true);
    });

    it('should check if isPriceTypeChange (false)', () => {
      const leg = {
        price: {
          priceType: 'SP'
        }
      };
      const offeredLeg = { priceType: 'SP' };

      expect(service['isPriceTypeChange'](<any>leg, <any>offeredLeg)).toEqual(false);
    });

    it('should detect price type change from GP to SP', () => {
      const leg = {
        price: {
          priceType: 'LP'
        }
      };
      const offeredLeg = { priceType: 'SP' };

      expect(service['isPriceTypeChange'](<any>leg, <any>offeredLeg)).toEqual(true);
    });

    it('should detect price type change from GUARANTEED to SP', () => {
      const leg = {
        price: {
          priceType: 'GUARANTEED'
        }
      };
      const offeredLeg = { priceType: 'SP' };

      expect(service['isPriceTypeChange'](<any>leg, <any>offeredLeg)).toEqual(true);
    });

    it('should not detect price type change from GUARANTEED to LP', () => {
      const leg = {
        price: {
          priceType: 'GUARANTEED'
        }
      };
      const offeredLeg = { priceType: 'LP' };

      expect(service['isPriceTypeChange'](<any>leg, <any>offeredLeg)).toEqual(false);
    });

    it('should not detect price type change from LP to GP', () => {
      const leg = {
        price: {
          priceType: 'LP'
        }
      };
      const offeredLeg = { priceType: 'GP' };

      expect(service['isPriceTypeChange'](<any>leg, <any>offeredLeg)).toEqual(false);
    });
  });

  it('should check if isPriceChange', () => {
    const leg = {
      price: {
        priceType: 'LP',
        priceDen: '2',
        priceNum: '4'
      }
    };
    const offeredLeg = {
      priceDen: '2',
      priceNum: '3'
    };

    expect(service['isPriceChange'](<any>leg, <any>offeredLeg)).toEqual(true);
  });

  describe('getTimeToOfferExpired', () => {
    it('should getTimeToOfferExpired', () => {
      const readBetResponse = {
        bet: [
          {
            offerExpiresAt: (new Date(Date.now() +1000)).toISOString()
          }
        ]
      };

      expect(service['getTimeToOfferExpired'](<any>readBetResponse) > 0).toEqual(true);
      expect(service.offerExpiresAt).toBe(readBetResponse.bet[0].offerExpiresAt);
    });

    it('should getTimeToOfferExpired (no expire date)', () => {
      const readBetResponse = {
        bet: [{}]
      };

      expect(service['getTimeToOfferExpired'](<any>readBetResponse)).toEqual(0);
      expect(service.offerExpiresAt).toBe('');
    });
  });

  it('should checkHasTraderMadeDecision', () => {
    const readBetResponse = {
      bet: [
        {
          betTypeRef: {
            id: 111
          },
          lines: 1,
          isConfirmed: 'N',
          isCancelled: 'N',
          tokenValue: '00.00',
          leg: [
            {
              sportsLeg: {
                outcomeCombiRef: {
                  id: 2
                },
                legPart: [{
                  outcomeRef: {
                    id: 13
                  }
                }]
              }
            },
            {
              sportsLeg: {
                outcomeCombiRef: {
                  id: 21
                },
                legPart: [{
                  outcomeRef: {
                    id: 14
                  }
                }]
              }
            }
          ]
        },
        {
          betTypeRef: {
            id: 110
          },
          lines: 2,
          isConfirmed: 'N',
          isCancelled: 'N',
          tokenValue: '10.00',
          leg: [
            {
              sportsLeg: {
                outcomeCombiRef: {},
                legPart: [{
                  outcomeRef: {
                    id: 14
                  }
                }]
              }
            }
          ]
        },
        {
          isConfirmed: 'Y',
          isCancelled: 'N'
        },
        {
          isConfirmed: 'N',
          isCancelled: 'Y'
        }
      ]
    };
    expect(service['checkHasTraderMadeDecision'](<any>readBetResponse)).toEqual(false);
  });

  it('should onOfferTimeout', () => {
    const subjectErrorSpy = jasmine.createSpy();
    service['betsData'] = <any>[{
      isSelected: true
    }];
    service['mainSubject'] = {
      error: subjectErrorSpy
    } as any;

    service['onOfferTimeout']();

    expect(service['betsData'][0].isSelected).toEqual(false);
    expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);

    expect(service['state']).toEqual(service['states'].off);
    expect(service.isNotInProcess).toBe(true);
    expect(service.isInProcess).toBe(false);
    expect(service.hasCustomerActionTimeExpired).toBe(false);
    expect(subjectErrorSpy).toHaveBeenCalledWith({ data: { offerTimeExpired: true } });
  });

  describe('matchBetsToBetsData', () => {
    it('should matchBetsToBetsData', () => {
      service['betsData'] = [{
        type: 'SGL',
        outcomeIds: ['1'],
        Bet: {
          lines: 1,
          clone: () => ({
            info: () => ({})
          })
        }
      }, {
        type: 'SGL',
        outcomeIds: ['2|3'],
        Bet: { lines: 1 },
        combiName: 'SCORECAST'
      }, {
        type: 'SGL',
        outcomeIds: ['4', '5'],
        Bet: { lines: 2 },
        combiName: 'FORECAST'
      }, {
        type: 'SGL',
        outcomeIds: ['6', '7'],
        Bet: { lines: 2 },
        combiName: 'FORECAST'
      }, {
        type: 'TBL',
        outcomeIds: ['8', '9'],
        Bet: { lines: 1 }
      }] as any;

      service['placeBetsData'] = {
        bets: [{
          betTypeRef: { id: 'SGL' },
          lines: { number: 1 },
          leg: [{
            sportsLeg: {
              outcomeCombiRef: {},
              legPart: [{ outcomeRef: { id: '1' } }]
            }
          }]
        }, {
          betTypeRef: { id: 'SGL' },
          lines: { number: 1 },
          masterBetId: '5',
          leg: [{
            sportsLeg: {
              outcomeCombiRef: {},
              legPart: [{ outcomeRef: { id: '1' } }]
            }
          }]
        }, {
          betTypeRef: { id: 'SGL' },
          lines: { number: 1 },
          leg: [{
            sportsLeg: {
              outcomeCombiRef: { id: 'SCORECAST' },
              legPart: [{ outcomeRef: { id: '2' } }, { outcomeRef: { id: '3' } }]
            }
          }]
        }, {
          betTypeRef: { id: 'SGL' },
          lines: { number: 2 },
          leg: [{
            sportsLeg: {
              outcomeCombiRef: { id: 'FORECAST' },
              legPart: [{ outcomeRef: { id: '4' } }, { outcomeRef: { id: '5' } }]
            }
          }]
        }, {
          betTypeRef: { id: 'SGL' },
          lines: { number: 2 },
          leg: [{
            sportsLeg: {
              outcomeCombiRef: { id: 'REVERSE_FORECAST' },
              legPart: [{ outcomeRef: { id: '6' } }, { outcomeRef: { id: '7' } }]
            }
          }]
        }, {
          betTypeRef: { id: 'TBL' },
          lines: { number: 1 },
          leg: [{
            sportsLeg: {
              outcomeCombiRef: {},
              legPart: [{ outcomeRef: { id: '8' } }, { outcomeRef: { id: '9' } }]
            }
          }]
        }, {
          betTypeRef: { id: 'UNKNOWN' },
          lines: {}, leg: []
        }]
      } as any;

      const result = service['matchBetsToBetsData']();

      expect(result.length).toEqual(6);
      expect(result[0]).toEqual(jasmine.objectContaining(<any>{
        betData: service['betsData'][0],
        bet: <any>service['placeBetsData'].bets[0]
      }));

      expect(result[1].betData.masterBetId).toEqual(5);
      expect(result[2].betData.masterBetId).toBeUndefined();
    });

    it('should matchBetsToBetsData (Can not find betData)', () => {
      service['placeBetsData'] = <any>{
        bets: [
          {
            betTypeRef: {
              id: 'SP'
            },
            lines: {
              number: 3
            },
            leg: [
              {
                sportsLeg: {
                  legPart: [],
                  outcomeCombiRef: {}
                }
              }
            ]
          }
        ]
      };

      service['betsData'] = <any>[
        {
          Bet: {
            lines: 1
          },
          outcomeIds: ['1', '2', '3']
        }
      ];

      expect(service['matchBetsToBetsData']().length).toEqual(0);
      expect(console.warn).toHaveBeenCalledWith('Overask', 'Can not find betData', 'SP_3');
    });
  });

  it('should buildReadBetRequest', () => {
    service['placeBetsData'] = <any>{
      bets: [{
        id: 12
      }]
    };

    expect(service['buildReadBetRequest']()).toEqual(jasmine.objectContaining({
      betRef: [{
        id: 12,
        provider: 'OpenBetSports'
      }]
    }));
  });

  describe('checkReadBetResponse', () => {
    let readBetResponse;

    beforeEach(() => {
      readBetResponse = {
        bet: [
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            betTypeRef: {
              id: 'SP'
            },
            lines: {
              number: 2
            },
            leg: []
          }
        ]
      };
      service.isInProcess = true;
      service['runReadBetPolling'] = jasmine.createSpy('runReadBetPolling').and.returnValue(of({}));
    });

    it('should checkReadBetResponse', () => {
      service['checkReadBetResponse'](<any>readBetResponse);
      expect(service['runReadBetPolling']).toHaveBeenCalledWith(5000);
    });

    it('should checkReadBetResponse (isBetsDataAssigned)', () => {
      service['checkIsMatchBetsToBetsDataNotSuccess'] = jasmine.createSpy().and.returnValue(false);
      service['isBetsDataAssigned'] = true;
      service['matchBetsToBetsData'] = jasmine.createSpy('matchBetsToBetsData');
      service['checkReadBetResponse'](<any>readBetResponse);
      expect(service['runReadBetPolling']).toHaveBeenCalledWith(5000);
    });

    it('should checkReadBetResponse (isBetsDataAssignedб checkIsMatchBetsToBetsDataNotSuccess)', () => {
      service['checkIsMatchBetsToBetsDataNotSuccess'] = jasmine.createSpy().and.returnValue(true);
      service['isBetsDataAssigned'] = true;
      service['matchBetsToBetsData'] = jasmine.createSpy('matchBetsToBetsData');
      service['checkReadBetResponse'](<any>readBetResponse);
      expect(service['runReadBetPolling']).not.toHaveBeenCalledWith(5000);
    });
  });

  describe('runReadBetPolling', () => {
    it('should finish with failure if bpp.send failed', fakeAsync(() => {
      const spy = spyOn(service as any, 'finisWithFailure');
      spyOn(service as any, 'sendReadBetRequest').and.returnValue(throwError({}));

      service['runReadBetPolling'](1).subscribe();
      tick(1);

      expect(spy).toHaveBeenCalled();
    }));

    it('should not finish with failure if device is offline', fakeAsync(() => {
      const spy = spyOn(service as any, 'finisWithFailure');
      spyOn(service as any, 'sendReadBetRequest').and.returnValue(throwError(ERROR_DICTIONARY.OFFLINE));
      deviceService.isOnline.and.returnValue(false);

      service['runReadBetPolling'](1).subscribe();
      tick(1);

      expect(spy).not.toHaveBeenCalled();
    }));
  });

  describe('applyBetsChanges', () => {

    beforeEach(() => {
      service['placeBetsData'] = <any>{
        bets: [{ id: 11 }]
      };
    });

    it('should applyBetsChanges (oldBet, isOffer)', () => {
      const readBetResponse = {
        bet: [{ id: 11, isOffer: 'Y' }]
      };

      service['applyBetsChanges'](<any>readBetResponse);
      expect(service['placeBetsData'].bets[0].isOffer).toEqual('Y');
      expect(service['originalPlacedBets']).toEqual({});
    });

    it('should applyBetsChanges (oldBet, !isOffer)', () => {
      const readBetResponse = {
        bet: [{ id: 11 }]
      };

      service['applyBetsChanges'](<any>readBetResponse);
      expect(service['placeBetsData'].bets[0].isOffer).toBeFalsy();
      expect(service['originalPlacedBets']).toEqual({});
    });

    it('should applyBetsChanges (oldBet, isConfirmed)', () => {
      const readBetResponse = {
        bet: [{ id: 11, isConfirmed: 'Y' }]
      };

      service['applyBetsChanges'](<any>readBetResponse);
      expect(service['placeBetsData'].bets[0]).toEqual(<any>readBetResponse.bet[0]);
      expect(service['originalPlacedBets']).toEqual({});
    });

    it('should not include referred bets, but return them', () => {
      const readBetResponse = {
        bet: [{ id: 11, isReferred: 'Y' }, { id: 11, isReferred: 'N'}]
      } as any;

      const result = service['applyBetsChanges'](readBetResponse);

      expect(service['placeBetsData'].bets.length).toEqual(1);
      expect(service['placeBetsData'].bets[0]).toEqual(<any>readBetResponse.bet[1]);
      expect(result.length).toBe(1);
      expect(result[0]).toEqual(readBetResponse.bet[0]);
      expect(service['originalPlacedBets'][11]).toEqual(readBetResponse.bet[0]);
    });

    it('should not left bet which isReferred=N if no referred bet with the same id', () => {
      const readBetResponse = {
        bet: [{ id: 11, isReferred: 'N' }]
      } as any;

      const result = service['applyBetsChanges'](readBetResponse);

      expect(service['placeBetsData'].bets.length).toEqual(1);
      expect(service['placeBetsData'].bets[0]).toEqual(<any>readBetResponse.bet[0]);
      expect(result).toBe(null);
      expect(service['originalPlacedBets']).toEqual({});
    });

    it('should define originalPlacedBets as empty object', () => {
      const readBetResponse = { bet: [] };
      service['originalPlacedBets'] = {'1': {}, 2: {}};

      service['applyBetsChanges'](<any>readBetResponse);

      expect(service['originalPlacedBets']).toEqual({});
    });
  });

  describe('applyTraderDecision', () => {
    const betsData = [{
      type: 'SGL',
      outcomeIds: ['1'],
      Bet: {
        lines: 1,
        clone: () => ({
          info: () => ({})
        })
      }
    }, {
      type: 'SGL',
      outcomeIds: ['2|3'],
      Bet: { lines: 1 },
      combiName: 'SCORECAST'
    }, {
      type: 'SGL',
      outcomeIds: ['4', '5'],
      Bet: { lines: 2 },
      combiName: 'FORECAST'
    }, {
      type: 'SGL',
      outcomeIds: ['6', '7'],
      Bet: { lines: 2 },
      combiName: 'FORECAST'
    }, {
      type: 'TBL',
      outcomeIds: ['8', '9'],
      Bet: { lines: 1 }
    }] as any;

    const placeBetsData = {
      bets: [{
        betTypeRef: { id: 'SGL' },
        lines: { number: 1 },
        leg: [{
          sportsLeg: {
            outcomeCombiRef: {},
            legPart: [{ outcomeRef: { id: '1' } }]
          }
        }]
      }, {
        betTypeRef: { id: 'SGL' },
        lines: { number: 1 },
        leg: [{
          sportsLeg: {
            outcomeCombiRef: {},
            legPart: [{ outcomeRef: { id: '1' } }]
          }
        }]
      }, {
        betTypeRef: { id: 'SGL' },
        lines: { number: 1 },
        leg: [{
          sportsLeg: {
            outcomeCombiRef: { id: 'SCORECAST' },
            legPart: [{ outcomeRef: { id: '2' } }, { outcomeRef: { id: '3' } }]
          }
        }]
      }, {
        betTypeRef: { id: 'SGL' },
        lines: { number: 2 },
        leg: [{
          sportsLeg: {
            outcomeCombiRef: { id: 'FORECAST' },
            legPart: [{ outcomeRef: { id: '4' } }, { outcomeRef: { id: '5' } }]
          }
        }]
      }, {
        betTypeRef: { id: 'SGL' },
        lines: { number: 2 },
        leg: [{
          sportsLeg: {
            outcomeCombiRef: { id: 'REVERSE_FORECAST' },
            legPart: [{ outcomeRef: { id: '6' } }, { outcomeRef: { id: '7' } }]
          }
        }]
      }, {
        betTypeRef: { id: 'TBL' },
        lines: { number: 1 },
        leg: [{
          sportsLeg: {
            outcomeCombiRef: {},
            legPart: [{ outcomeRef: { id: '8' } }, { outcomeRef: { id: '9' } }]
          }
        }]
      }, {
        betTypeRef: { id: 'UNKNOWN' },
        lines: {}, leg: []
      }]
    } as any;

    let readBetResponse;

    beforeEach(() => {
      readBetResponse = {
        bet: [{ id: 11, isConfirmed: 'Y', tokenValue: '10.00'}]
      } as any;

      service['state'] = service['states'].traderMadeDecision;

      spyOn(service as any, 'applyBetsChanges');
      spyOn(service as any, 'processOveraskFlow').and.callThrough();
      spyOn(service as any, 'saveStateToStorage').and.callThrough();
      service['mainSubject'] = new Subject();
    });

    it('should applyTraderDecision (isSomeBetsOffered)', () => {
      service['placeBetsData'] = <any>{
        bets: [{ id: 11, isOffer: 'Y' }]
      };
      service['onOfferTimeout'] = jasmine.createSpy('onOfferTimeout');

      service['applyTraderDecision'](readBetResponse);

      expect(pubSubService.publishSync).toHaveBeenCalledWith('OVERASK_BETS_DATA_UPDATED', '');
      expect(storageService.set).toHaveBeenCalledWith('overaskUsername', 'name');
      expect(service['processOveraskFlow']).not.toHaveBeenCalled();
      expect(service['applyBetsChanges']).toHaveBeenCalledWith(readBetResponse);
      expect(service['saveStateToStorage']).toHaveBeenCalledWith(undefined);
    });

    it('should save required bets to storage (isAllOffered, split bets)', () => {
      service['placeBetsData'] = <any>{
        bets: [{ id: 11, isOffer: 'Y' }]
      };
      const originals = [{id: 123}] as any;
      (service['applyBetsChanges'] as Spy).and.returnValue(originals);
      spyOn(service as any, 'setStateAndClearInStorage');
      spyOn(service as any, 'calculateBetsStates');
      service.isAllBetsOffered = true;

      service['applyTraderDecision'](readBetResponse);

      expect(service['saveStateToStorage']).toHaveBeenCalledWith(originals as any);
    });

    it('should applyTraderDecision (isAllBetsAccepted)', () => {
      service['placeBetsData'] = <any>{
        bets: [{ id: 12, isConfirmed: 'Y' }, { id: 13, isConfirmed: 'Y' }]
      };

      service['applyTraderDecision'](readBetResponse);

      expect(service['processOveraskFlow']).toHaveBeenCalled();
    });

    it('should applyTraderDecision (no bets offered)', () => {
      service['placeBetsData'] = <any>{
        bets: []
      };
      service.userHasChoice = true;
      service.isInProcess = true;
      service.isInFinal = false;

      service['applyTraderDecision'](readBetResponse);

      expect(pubSubService.publishSync).toHaveBeenCalledWith('OVERASK_BETS_DATA_UPDATED', '');
      expect(service['processOveraskFlow']).toHaveBeenCalled();
      expect(service.userHasChoice).toBe(false);
      expect(service.isInProcess).toBe(false);
      expect(service.isInFinal).toBe(true);
    });

    it('matchBetsToBetsData', () => {
      service['betsData'] = betsData;
      service['placeBetsData'] = placeBetsData;

      expect(service['matchBetsToBetsData']().length).toBe(6);
    });

    it('saveStateToStorage should use view\'s data', () => {
      service['placeBetsData'] = placeBetsData;

      service['saveStateToStorage']();

      expect(storageService.set.calls.argsFor(0)[0]).toBe('overaskPlaceBetsData');
      expect(storageService.set.calls.argsFor(0)[1]).toEqual(placeBetsData);
    });

    it('saveStateToStorage should use originals\' data', () => {
      const originals = [{id: 123}] as any;
      service['placeBetsData'] = placeBetsData;

      service['saveStateToStorage'](originals);

      const params = storageService.set.calls.argsFor(0);
      expect(params[0]).toBe('overaskPlaceBetsData');
      expect(params[1]).not.toEqual(placeBetsData);
      expect(params[1].bets).toEqual(originals);
    });
  });

  describe('processOveraskFlow', () => {

    beforeEach(() => {
      service['placeBetsData'] = {} as any;
      service['mainSubject'] = new Subject();
      spyOn(service as any, 'getBetIds');
    });

    it('should prepare bet ids for bet receipt', () => {
      service['processOveraskFlow']();

      expect(service['getBetIds']).toHaveBeenCalledWith(true);
    });

    it('should clear overask storage data', () => {
      service['processOveraskFlow']();

      expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
    });
  });

  it('clearStateFlags', () => {
    service.isAllBetsAccepted = undefined;
    service.isAllBetsDeclined = undefined;
    service.isAllBetsOffered = undefined;
    service.isNoBetsAccepted = undefined;
    service.isNoBetsDeclined = undefined;
    service.isNoBetsOffered = undefined;
    service.isSomeBetsAccepted = undefined;
    service.isSomeBetsDeclined = undefined;
    service.isSomeBetsOffered = undefined;
    service.userHasChoice = undefined;
    service['hasUserMadeDecision'] = undefined;
    service['suspendedIds'] = undefined;
    service['deletedBetIds'] = undefined;
    service['clearStateFlags']();

    expect(service.isAllBetsAccepted).toBe(false);
    expect(service.isAllBetsDeclined).toBe(false);
    expect(service.isAllBetsOffered).toBe(false);
    expect(service.isNoBetsAccepted).toBe(true);
    expect(service.isNoBetsDeclined).toBe(true);
    expect(service.isNoBetsOffered).toBe(true);
    expect(service.isSomeBetsAccepted).toBe(false);
    expect(service.isSomeBetsDeclined).toBe(false);
    expect(service.isSomeBetsOffered).toBe(false);
    expect(service.userHasChoice).toBe(false);
    expect(service['hasUserMadeDecision']).toBe(false);
    expect(service['suspendedIds']).toEqual([]);
    expect(service['deletedBetIds']).toEqual([]);
  });

  describe('calculateBetsStates userHasChoice flag', () => {
    beforeEach(() => {
      service['placeBetsData'] = {
        bets: [
          {
            isOffer: 'Y'
          }
        ]
      } as any;
    });

    it('should be true if trader counted some offer', () => {
      service.isInProcess = true;
      service.hasTraderMadeDecision = true;

      service['calculateBetsStates'](false);
    });

    it('should false if overask process not started', () => {
      service.isInProcess = false;
      service.hasTraderMadeDecision = true;

      service['calculateBetsStates'](true);
    });

    it('should false if offer is on review', () => {
      service.isInProcess = true;
      service.hasTraderMadeDecision = false;

      service['calculateBetsStates'](false);
    });

    it('should false if trader offered nothing', () => {
      service['placeBetsData'] = {
        bets: [
          {
            isConfirmed: 'Y'
          },
          {
            isCancelled: 'Y'
          }
        ]
      } as any;

      service.isInProcess = true;
      service.hasTraderMadeDecision = false;

      service['calculateBetsStates'](true);
    });
  });

  describe('isPricesChanged', () => {
    let betData;
    const childBet = {
      outcomeId: 111
    };

    beforeEach(() => {
      betData = {
        Bet: {
          legs: [{
            firstOutcomeId: 111,
            price: {
              props: {
                priceDec: 1.4,
                priceDen: 10,
                priceNum: 1,
                priceType: 'LP'
              }
            },
            parts: [{
              outcome: {}
            }]
          }]
        }
      } as any;

      service['betsData'] = [childBet] as any;
      betDataMock.oldLegs = undefined;
      service['originalPlacedBets'] = undefined;
    });

    it('betData for oldLegs should be undefined if no children', () => {
      service['isPricesChanged'](betData, [] as any);

      expect(betData.oldLegs[0].betData).toBeUndefined();
    });

    it('betData for oldLegs should be undefined children is empty', () => {
      spyOn<any>(service, 'isPriceChange').and.returnValue(false);
      spyOn<any>(service, 'isPriceTypeChange').and.returnValue(false);
      betData.outcomeIds = [];
      service['isPricesChanged'](betData, [] as any);

      expect(betData.oldLegs[0].betData).toBeUndefined();
    });

    it('betData should be ref to child element', () => {
      spyOn<any>(service, 'isPriceChange').and.returnValue(false);
      spyOn<any>(service, 'isPriceTypeChange').and.returnValue(false);
      betData.outcomeIds = [999];
      service['isPricesChanged'](betData, [] as any);

      expect(betData.oldLegs[0].betData).toBe(childBet);
    });

    it('should check if trader change prices', () => {
      service['isPricesChanged'](betData, {} as any);

      expect(betData.oldLegs[0]).toEqual({
        outcome: {},
        outcomeId: 111,
        price: {
          priceDen: 10,
          priceNum: 1,
          priceType: 'LP'
        }
      });
    });

    it('should check if trader change prices(priceType is undefined)', () => {
      betData.Bet.legs[0].price.props.priceType = null;
      service['isPricesChanged'](betData, {} as any);

      expect(betData.oldLegs[0]).toEqual({
        outcome: {},
        outcomeId: 111,
        price: {
          priceDen: 10,
          priceNum: 1,
          priceType: undefined
        }
      });
    });

    it('should check if trader change prices(priceType should be taken from priceTypeRef', () => {
      betData.Bet.legs[0].price.props.priceType = null;
      betData.Bet.legs[0].price.props.priceTypeRef = { id: 'SP' };
      service['isPricesChanged'](betData, {} as any);

      expect(betData.oldLegs[0]).toEqual({
        outcome: {},
        outcomeId: 111,
        price: {
          priceDen: 10,
          priceNum: 1,
          priceType: 'SP'
        }
      });
    });

    it('should detect price change (leg[0]: 1/2 -> 4/5) if originalRequestedBet is changed', () => {
      service['originalPlacedBets'] = {751693: requestedBetMock};

      expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
      expect(betDataMock.oldLegs[0].traderChangedPrice).toEqual(true);
      expect(betDataMock.oldLegs[0].changedPrice.priceNum).toEqual(4);
      expect(betDataMock.oldLegs[0].changedPrice.priceDen).toEqual(5);
      expect(betDataMock.oldLegs[1].traderChangedPrice).toEqual(undefined);
    });

    describe('for split bets', () => {
      it('should detect price change if base bet for linked changed', () => {
        service['originalPlacedBets'] = {555: requestedBetMock};
        (betDataMock as any).dependsOn = 555;
        (betDataMock as any).masterBetId = null;

        expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
      });

      it('should detect price change if base bet for not linked changed', () => {
        service['originalPlacedBets'] = {555: requestedBetMock};
        (betDataMock as any).dependsOn = null;
        (betDataMock as any).masterBetId = 555;

        expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
      });

      afterEach(() => {
        (betDataMock as any).dependsOn = null;
        (betDataMock as any).masterBetId = null;
      });
    });

    describe('if originalPlacedBets not proper', () => {
      beforeEach(() => {
        betDataMock.Bet.legs[0].price.priceNum = betDataMock.Bet.legs[0].price.props.priceNum = 100;
      });

      it('should detect price change 1/2 -> 4/5 by betData if no originalPlacedBets', () => {
        service['originalPlacedBets'] = null;

        expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
        expect(betDataMock.oldLegs[0].traderChangedPrice).toEqual(true);
        expect(betDataMock.oldLegs[0].changedPrice.priceNum).toEqual(4);
        expect(betDataMock.oldLegs[0].price.priceNum).toEqual(100);
        expect(betDataMock.oldLegs[1].traderChangedPrice).toEqual(undefined);
      });

      it('should detect price change by betData if no corresponding data', () => {
        service['originalPlacedBets'] = {751693: null};

        expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
        expect(betDataMock.oldLegs[0].traderChangedPrice).toEqual(true);
        expect(betDataMock.oldLegs[0].changedPrice.priceNum).toEqual(4);
        expect(betDataMock.oldLegs[0].price.priceNum).toEqual(100);
        expect(betDataMock.oldLegs[1].traderChangedPrice).toEqual(undefined);
      });

      it('should detect price change by betData if corresponding bet does not have legs', () => {
        service['originalPlacedBets'] = {751693: {leg: null}};

        expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
        expect(betDataMock.oldLegs[0].traderChangedPrice).toEqual(true);
        expect(betDataMock.oldLegs[0].changedPrice.priceNum).toEqual(4);
        expect(betDataMock.oldLegs[0].price.priceNum).toEqual(100);
        expect(betDataMock.oldLegs[1].traderChangedPrice).toEqual(undefined);
      });

      it('should detect price change by betData if corresponding bet legs do not much outcomeId', () => {
        service['originalPlacedBets'] = {751693: requestedBetMock};
        service['originalPlacedBets']['751693'].leg[0].sportsLeg.legPart[0].outcomeRef.id = 'Any other id # 1';
        service['originalPlacedBets']['751693'].leg[1].sportsLeg.legPart[0].outcomeRef.id = 'Any other id # 2';

        expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(true);
        expect(betDataMock.oldLegs[0].traderChangedPrice).toEqual(true);
        expect(betDataMock.oldLegs[0].changedPrice.priceNum).toEqual(4);
        expect(betDataMock.oldLegs[0].price.priceNum).toEqual(100);
        expect(betDataMock.oldLegs[1].traderChangedPrice).toEqual(undefined);
      });
    });

    it('should not detect price change if originalRequestedBet not changed', () => {
      service['originalPlacedBets'] = {751693: requestedBetMock};
      const mockPrice = betDataMock.Bet.legs[0];
      mockPrice.price = {...mockPrice.price};
      offeredBetMock.leg[0].sportsLeg.price = requestedBetMock.leg[0].sportsLeg.price;
      offeredBetMock.leg[1].sportsLeg.price = requestedBetMock.leg[1].sportsLeg.price;
      betDataMock.Bet.legs[0].price.priceNum = betDataMock.Bet.legs[0].price.props.priceNum = 100;
      service['originalPlacedBets']['751693'].leg[0].sportsLeg.legPart[0].outcomeRef.id = 553364979;
      service['originalPlacedBets']['751693'].leg[1].sportsLeg.legPart[0].outcomeRef.id = 553384143;

      expect(service['isPricesChanged'](betDataMock as any, offeredBetMock.leg as any)).toEqual(false);
      expect(betDataMock.oldLegs[0].traderChangedPrice).toEqual(undefined);
      expect(betDataMock.oldLegs[1].traderChangedPrice).toEqual(undefined);
    });
  });

  describe('defineIsRemovable', () => {
    it('should define true if bet accepted by trader', () => {
      const bet = {
        isTraderAccepted: true
      } as any;
      service['defineIsRemovable'](bet);

      expect(bet.isOfferRemovable).toEqual(true);
    });

    it('should define false if bet accepted by trader but has children', () => {
      const bet = {
        isTraderAccepted: false,
        isTraderOffered: true,
      } as any;
      service['defineIsRemovable'](bet);

      expect(bet.isOfferRemovable).toEqual(true);
    });

    it('should define false if bet not accepted by trader and not offered', () => {
      const bet = {
        isTraderAccepted: false,
        isTraderOffered: false
      } as any;
      service['defineIsRemovable'](bet);

      expect(bet.isOfferRemovable).toEqual(false);
    });

    it('should define false if bet offered but has children', () => {
      const bet = {
        isTraderOffered: true,
        children: [{}]
      } as any;
      service['defineIsRemovable'](bet);

      expect(bet.isOfferRemovable).toEqual(false);
    });
  });

  describe('clearBetFlags', () => {
    it('should clear bet state flags', () => {
      const betData = {} as any;
      service['clearBetFlags'](betData);

      expect(betData.isTraderAccepted).toBe(false);
      expect(betData.isTraderDeclined).toBe(false);
      expect(betData.isTraderOffered).toBe(false);
      expect(betData.isSelected).toBe(false);
      expect(betData.isTraderChanged).toBe(false);
      expect(betData.isOfferRemovable).toBe(false);

      expect(betData.traderChangedPriceType).toBe(false);
      expect(betData.traderChangedLegType).toBe(false);
      expect(betData.traderChangedOdds).toBe(false);
      expect(betData.traderChangedStake).toBe(false);

      expect(betData.overaskMessage).toBe('');
    });

    it('should not clear isSuspended flag for single bet', () => {
      const betData = {
        disabled: true,
        type: 'SGL'
      } as any;
      service['clearBetFlags'](betData);

      expect(betData.disabled).toBe(true);
    });

    it('should clear isSuspended flag if not single bet', () => {
      const betData = {
        disabled: true,
        type: 'DBL'
      } as any;
      service['clearBetFlags'](betData);

      expect(betData.disabled).toBe(false);
    });
  });

  describe('setStateAndClearInStorage', () => {
    it('should setState and clear state in storage', () => {
      const state = 'off';
      service['setState'] = jasmine.createSpy('setState');
      service.setStateAndClearInStorage(state);

      expect(service['setState']).toHaveBeenCalledWith(state);
      expect(betslipStorageService.clearStateInStorage).toHaveBeenCalledTimes(1);
    });

    describe('setState', () => {

      it('should setState for isInProcess', () => {
        service.setStateAndClearInStorage('off');

        expect(service.isInProcess).toBeFalsy();
      });

      it('should setState for isInFinal (not receipt)', () => {
        service.bsMode = 'foo';
        service.setStateAndClearInStorage('traderMadeDecision');

        expect(service.isInProcess).toBeTruthy();
        expect(service.isInFinal).toBeFalsy();
      });

      it('should setState for isInFinal (receipt) (not real case)', () => {
        service.bsMode = 'Bet Receipt';
        service.setStateAndClearInStorage('traderMadeDecision');

        expect(service.isInProcess).toBeTruthy();
        expect(service.isInFinal).toBeTruthy();
      });
    });
  });

  describe('getBetIds', () => {
    it('should return betId for all selected bets', () => {
      service['betsData'] = [
        { betId: 1, isSelected: true },
        { betId: 2, isSelected: true },
        { betId: 3, isSelected: false },
        { isSelected: true },
        { betId: 5, isSelected: true, disabled: true },
        { betId: 6, isSelected: false, disabled: true },
        { betId: 7, isSelected: false, disabled: true, isTraderDeclined: true },
        { betId: 8, isSelected: true, disabled: true, isTraderDeclined: true }
      ] as any;
      const result = service['getBetIds']();

      expect(result).toEqual([1, 2, 5, 8]);
    });

    it('should return betId for all selected and declined by traders bets', () => {
      service['betsData'] = [
        { betId: 1, isSelected: true },
        { betId: 2, isSelected: true },
        { betId: 3, isSelected: false },
        { betId: 4, isSelected: false, isTraderDeclined: true },
        { isSelected: true },
        { betId: 5, isSelected: true, disabled: true },
        { betId: 6, isSelected: false, disabled: true },
        { betId: 7, isSelected: false, disabled: true, isTraderDeclined: true },
        { betId: 8, isSelected: true, disabled: true, isTraderDeclined: true }
      ] as any;
      const result = service['getBetIds'](true);

      expect(result).toEqual([1, 2, 4, 5, 7, 8]);
    });
  });

  it('processOveraskFlow should call getBetIds with option true', () => {
    service['getBetIds'] = jasmine.createSpy('getBetIds').and.returnValue([]);
    service['placeBetsData'] = {
      bets: [],
      ids: []
    } as any;
    service['mainSubject'] = new Subject();
    service['processOveraskFlow']();

    expect(service['getBetIds']).toHaveBeenCalledWith(true);
  });

  describe('acceptOrRejectOffer', () => {
    it('should set hasUserMadeDecision as true', () => {
      service['hasUserMadeDecision'] = false;
      service['acceptOrRejectOffer']([] as any, 'accept');
      bppService.send.and.returnValue(of({ message: 'message' }));

      expect(service['hasUserMadeDecision']).toEqual(true);
    });
  });

  describe('setSuspended', () => {
    it('should update suspended bets', () => {
      const suspended = [1, 2, 3];
      service.setSuspended(suspended);

      expect(service['suspendedIds']).toBe(suspended);
    });
  });

  describe('isOveraskCanBePlaced', () => {
    it('should return false if no placeBetsData', () => {
      service['placeBetsData'] = null;

      expect(service.isOveraskCanBePlaced()).toEqual(false);
    });

    it('should return false if no bets', () => {
      service['placeBetsData'] = {
        bets: null
      } as any;

      expect(service.isOveraskCanBePlaced()).toEqual(false);
    });

    it('should return false if array of bets is empty', () => {
      service['placeBetsData'] = {
        bets: []
      } as any;

      expect(service.isOveraskCanBePlaced()).toEqual(false);
    });

    it('should return false if no active bets', () => {
      service['suspendedIds'] = [2, 3];
      service['placeBetsData'] = {
        bets: [
          {id : 1, isCancelled: 'Y'},
          {id : 2, isCancelled: 'Y'},
          {id : 3, isCancelled: 'N'}
        ]
      } as any;

      expect(service.isOveraskCanBePlaced()).toEqual(false);
    });

    it('should return true', () => {
      service['suspendedIds'] = [3];
      service['placeBetsData'] = {
        bets: [
          {id : 1, isCancelled: 'Y'},
          {id : 2, isCancelled: 'N'},
          {id : 3, isCancelled: 'N'}
        ]
      } as any;

      expect(service.isOveraskCanBePlaced()).toEqual(true);
    });
  });

  describe('isBetPlaced', () => {
    it('should return false if no placeBetsData', () => {
      service['placeBetsData'] = null;

      expect(service.isBetPlaced(null)).toEqual(false);
    });

    it('should return false if no bets', () => {
      service['placeBetsData'] = {
        bets: null
      } as any;

      expect(service.isBetPlaced(null)).toEqual(false);
    });

    it('should return false if array of bets is empty', () => {
      service['placeBetsData'] = {
        bets: []
      } as any;

      expect(service.isBetPlaced(null)).toEqual(false);
    });

    it('should return false if bet is not placed', () => {
      service['placeBetsData'] = {
        bets: [
          {id : 1, isCancelled: 'Y'},
          {id : 2, isCancelled: 'N'}
        ]
      } as any;

      expect(service.isBetPlaced({betId: 5} as any)).toEqual(false);
    });

    it('should return true if bet is placed', () => {
      service['suspendedIds'] = [3];
      service['placeBetsData'] = {
        bets: [
          {id : 1, isCancelled: 'Y'},
          {id : 3, isCancelled: 'N'}
        ]
      } as any;

      expect(service.isBetPlaced({betId: 3} as any)).toEqual(true);
    });
  });

  describe('isNotDeletedFromTraderOffer', () => {
    it('Should return false if there is id in a deletedBetID array', () => {
      const id = 'id';
      service['deletedBetIds'] = [id];
      expect(service.isNotDeletedFromTraderOffer(id)).toBe(false);
    });

    it('Should return true if there is no id in a deletedBetID array', () => {
      const id = 'id';
      service['deletedBetIds'] = [''];
      expect(service.isNotDeletedFromTraderOffer(id)).toBe(true);
    });
  });

  describe('collectDeletedBetID', () => {
    it('Should add "id" to the deletedBetID array', () => {
      service['deletedBetIds'] = [];
      const id = 'id';

      service.collectDeletedBetID(id);

      expect(service['deletedBetIds'][0]).toBe(id);
    });
  });

  describe('removeDeletedBetID', () => {
    it('Should remove "id" from the deletedBetID array', () => {
      const id1 = 'id1';
      const id2 = 'id2';
      service['deletedBetIds'] = [id1, id2];

      service.removeDeletedBetID(id1);

      expect(service['deletedBetIds'][0]).toBe('id2');
    });
  });

  describe('calculateStateMessage', () => {
    beforeEach(() => {
      service.stateMessage = 'stateMessage';
      service.errorMessage = 'errorMessage';
    });

    it('should clear states and do not define stateMessage if no state', () => {
      service['state'] = null;

      service['calculateStateMessage']();

      expect(service.stateMessage).toEqual('');
      expect(service.errorMessage).toEqual('');
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should clear states and do not define stateMessage if no state is not customerActionTimeExpired', () => {
      service['state'] = 'off';

      service['calculateStateMessage']();

      expect(service.stateMessage).toEqual('');
      expect(service.errorMessage).toEqual('');
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should clear states and define stateMessage if no state is customerActionTimeExpired', () => {
      service['state'] = 'customerActionTimeExpired';

      service['calculateStateMessage']();

      expect(service.stateMessage).toEqual('someText');
      expect(service.errorMessage).toEqual('');
      expect(localeService.getString).toHaveBeenCalledWith('bs.overaskMessages.customerActionTimeExpired');
    });
  });

  describe('checkHasTraderMadeDecision', () => {
    let response;
    let result;

    beforeEach(() => {
      response = {
        bet: [
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          }
        ]
      };
      service['getBetKey'] = jasmine.createSpy('getBetKey').and.returnValue(response);
    });

    it ('should return true and call getBetKey', () => {
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it ('should return true and not call getBetKey', () => {
      response = {
        bet: [
          {
            isConfirmed: 'Y',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'Y',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'Y',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          }
        ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).not.toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it ('should return false and call getBetKey', () => {
      response = {
        bet: [
          {
            isConfirmed: 'Y',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'Y',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          }
        ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(false);
    });

    it ('should return true and not call getBetKey', () => {
      response = {
        bet: [
          {
            isConfirmed: 'Y',
            isCancelled: 'Y',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'Y',
            isCancelled: 'Y',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'Y',
            isCancelled: 'Y',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          }
        ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).not.toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it ('should return false and call getBetKey', () => {
      response = {
        bet: [
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          }
        ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(false);
    });

    it ('should return false and call getBetKey', () => {
      response = {
        bet: [
          {
            isConfirmed: 'N',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          },
          {
            isConfirmed: 'Y',
            isCancelled: 'N',
            leg: {
              sportsLeg: { outcomeCombiRef: { id: '10' } },
              legPart: { outcomeRef: { id: '123' } }
            },
            lines: '1'
          }
        ]
      };
      result = service['checkHasTraderMadeDecision'](response as any);

      expect(service['getBetKey']).toHaveBeenCalled();
      expect(result).toEqual(false);
    });
  });

  describe('finisWithFailure', () => {
    beforeEach(() => {
      userService.status = true;
      service.errorMessage = undefined;
      service['mainSubject'] = {
        error: jasmine.createSpy()
      } as any;
    });

    describe('PT_ERR_AUTH error', () => {
      it ('should not define errorMessage if no error', () => {
        service['finisWithFailure']();

        expect(service.errorMessage).toBe('');
      });

      it ('should not define errorMessage if no error data', () => {
        service['finisWithFailure']({ data: null });

        expect(service.errorMessage).toBe('');
      });

      it ('should not define errorMessage if not PT_ERR_AUTH error', () => {
        service['finisWithFailure']({ data: { status: ''} });

        expect(service.errorMessage).toBe('');
      });

      it ('should define if for PT_ERR_AUTH error', () => {
        const error = {
          data: {
            status: 'PT_ERR_AUTH',
            message: 'bs.overaskMessages.PT_ERR_AUTH'
          }
        };

        service['finisWithFailure'](error);

        expect(service.errorMessage).toBe(error.data.message);
      });
    });
  });

  describe('checkError', () => {
    it('should not return error if no error object', () => {
      expect(service['checkError'](null)).toBeUndefined();
    });

    it('should not return error if no error field is not string', () => {
      expect(service['checkError']({ error: {} })).toBeUndefined();
    });

    it('should not return error if not PT_ERR_AUTH', () => {
      expect(service['checkError']({ error: {error: 'error'} })).toBeUndefined();
    });

    it('should return error for PT_ERR_AUTH status', () => {
      const error = {
        error: {
          code: 2500,
          status: 'SERVICE_ERROR',
          error: '9516 - PT_ERR_AUTH coral::bet::pre_place_bets_callback: funds reservation failed: PT_ERR_AUTH',
          message: 'Service error'
        }
      };

      expect(service['checkError'](error)).toEqual({
        data: {
          status: 'PT_ERR_AUTH',
          message: jasmine.any(String)
        }
      } as any);
      expect(localeService.getString).toHaveBeenCalledWith('bs.overaskMessages.PT_ERR_AUTH');
    });

    it('should return error for PT_ERR_AUTH status', () => {
      const error = {
        error: {
          code: 2500,
          status: 'SERVICE_ERROR',
          error: '9516 - LOW_FUNDS There was an error while attempting to place your bet, please try and place this bet again: LOW_FUNDS',
          message: 'Service error'
        }
      };

      expect(service['checkError'](error)).toEqual({
        data: {
          status: 'LOW_FUNDS',
          message: jasmine.any(String)
        }
      } as any);
      expect(localeService.getString).toHaveBeenCalledWith('bs.overaskMessages.LOW_FUNDS');
    });
  });

  afterEach(() => {
    service = null;
  });
});
