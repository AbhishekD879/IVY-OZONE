import { of as observableOf, throwError, of } from 'rxjs';
import { YourcallBetslipService } from './yourcall-betslip.service';
import { tick, fakeAsync } from '@angular/core/testing';

describe('YourcallBetslipService', () => {
  let service: YourcallBetslipService;
  let coreTools;
  let yourcallProviderService;
  let remoteBetslipService;
  let userService;
  let fracToDecService;
  let commandService;
  let pubsubService;
  let gtmService;
  let localeService;
  let awsService;
  let FiveASideService;
  let location;
  let observer;
  let bybSelectedSelectionsService;
  let callbackHandler

  const testingObj = {
    eventCategory: 'quickbet',
    eventAction: 'place bet',
    eventLabel: 'success',
    betID: 'teststr',
    betType: 'Single',
    ecommerce: {
      purchase: {
        actionField: {
          id: 'teststr',
          revenue: '1.2'
        },
        products: [{
          price: '1.2',
          category: '16',
          variant: 442,
          brand: 'Bet builder',
          metric1: 0,
          dimension60: 776939,
          dimension62: '0',
          dimension63: '0',
          dimension64: 'EDP',
          dimension65: 'Bet builder',
          dimension66: 1,
          dimension67: '29.00',
          dimension89: undefined,
          dimension90: 77918,
          quantity: 1
        }]
      }
    },
  };

  beforeEach(() => {
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy().and.returnValue(true),
      getOwnDeepProperty: jasmine.createSpy().and.returnValue('BYB'),
      deepClone: jasmine.createSpy().and.callFake((data) => data),
      uuid: jasmine.createSpy('uuid').and.returnValue(1)
    };
    yourcallProviderService = {
      API: 'BYB',
      use: jasmine.createSpy(),
      helper: {
        getPlaceBetErrorMsg: jasmine.createSpy('getPlaceBetErrorMsg'),
        createSelectionData: jasmine.createSpy('createSelectionData').and.returnValue({}),
        createBet: jasmine.createSpy('createBet')
      }
    };
    remoteBetslipService = {
      placeBet: jasmine.createSpy().and.returnValue(observableOf([])),
      removeSelection: jasmine.createSpy('removeSelection'),
      addSelection: jasmine.createSpy('addSelection').and.returnValue(observableOf({
        data: {
          odds: '10',
          priceNum: '1',
          priceDen: '10',
        }
      })),
      configs: {
        general: {},
        sgl: {},
        ds: {},
        byb: {
          add: {
            request: '50001',
            success: '51001',
            error: '51002',
            change: ''
          },
          remove: {
            request: '30002',
            success: '30003'
          },
          placeBet: {
            request: '50011',
            success: '51101',
            error: '51102'
          }
        }
      }
    };
    userService = {
      currencySymbol: 'UAH',
      currency: 'UAH',
      bppToken: 'bppToken',
      oddsFormat: 'frac'
    };
    fracToDecService = {
      decToFrac: jasmine.createSpy(),
      getDecimal: jasmine.createSpy()
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync'),
      API: {
        BPP_AUTH_SEQUENCE: 'BPP_AUTH_SEQUENCE'
      }
    };
    callbackHandler = (ctrlName: string, eventName: string, callback) => {
      if(eventName === 'LUCKY_DIP_KEYPAD_PRESSED'){
        tick(1000)
        callback(true);
      }
      else{
        callback();
        
      }
  }

    pubsubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe').and.callFake(callbackHandler),
      API: {
        YOURCALL_SELECTION_UPDATE: 'YOURCALL_SELECTION_UPDATE',
        QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD: 'QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD',
      }
    } as any;

    gtmService = {
      push: jasmine.createSpy()
    };
    localeService = {
      getString: jasmine.createSpy()
    };
    awsService = {
      addAction: jasmine.createSpy()
    };
    FiveASideService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    location = {
      path: jasmine.createSpy().and.returnValue('Bet builder')
    };
    observer = {
      error: jasmine.createSpy('error'),
      complete: jasmine.createSpy('complete'),
      next: jasmine.createSpy('next')
    };
    bybSelectedSelectionsService = {
        placeBet: jasmine.createSpy('placeBet').and.returnValue(true),
        duplicateIdd: new Set(),
        betPlacementSucess: jasmine.createSpy('betPlacementSucess').and.returnValue(true),
    };

    service = new YourcallBetslipService(
      remoteBetslipService,
      userService,
      fracToDecService,
      coreTools,
      commandService,
      pubsubService,
      localeService,
      gtmService,
      yourcallProviderService,
      awsService,
      FiveASideService,
      location,
      bybSelectedSelectionsService
    );

    service.placeData = {
      bet: {},
      eventEntity: {
        sportId: '16',
        typeId: '1',
        id: '1',
      },
      selection: {
        stake: 'stake',
        betOdds: 'betOdds'
      }
    };
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });
  it('updateKeyboardStatus pubsub', () => {
    service['digitKeyBoardStatus']=true
    service['isBetPlaceClicked']=false
    service.updateKeyboardStatus()
    expect(service).toBeTruthy();
  });
  it('updateKeyboardStatus pubsub isBetPlaceClicked true', () => {
    service['digitKeyBoardStatus']=true
    service['isBetPlaceClicked']=true;
    service.updateKeyboardStatus()
    expect(service).toBeTruthy();
  });

  describe('#addSelection', () => {
    it('should call addSelection for Five A Side', fakeAsync(() => {
      location['path'].and.returnValue('/5-a-side');
      service.addSelection({} as any).then();

      tick();

      expect(yourcallProviderService.helper.createBet).toHaveBeenCalledWith({
        currencySymbol: 'UAH',
        currency: 'UAH',
        token: 'bppToken',
        oddsFormat: 'frac',
        dashboardData: {},
        oddsFract: undefined,
        odds: '10',
        channel: 'f'
      });
    }));

    it('should call addSelection for Build Your Bet', fakeAsync(() => {
      location['path'].and.returnValue('/build-your-bat');
      service.addSelection({} as any).then();

      tick();

      expect(yourcallProviderService.helper.createBet).toHaveBeenCalledWith({
        currencySymbol: 'UAH',
        currency: 'UAH',
        token: 'bppToken',
        oddsFormat: 'frac',
        dashboardData: {},
        oddsFract: undefined,
        odds: '10',
        channel: 'e'
      });
    }));

    it('should call reject', () => {
      yourcallProviderService.API = 'byb1';
      service.addSelection(null as any).then(() => {}, error => {
        expect(error).toEqual('Remote betslip config not found');
      });

      expect(yourcallProviderService.helper.createSelectionData).toHaveBeenCalledWith([]);
    });
  });

  describe('placeBet', () => {
    let bet, event, selection;

    beforeEach(() => {
      bet = {
        currency: 'UAH',
        price: '1/2',
        stake: '10',
        token: 'token',
        winType: 'yes',
        clientUserAgent: 'S|W|A0000000'
      } as any;
      event = {
        id: '13213'
      } as any;
      selection = {
        id: '12'
      } as any;
    });

    it('should trigger place bet request wrapper and return Connection timeout error', () => {
      remoteBetslipService.placeBet.and.returnValue(throwError({
        data: {
          error: {
            code: 'Error',
            description: 'Connection timeout',
            subErrorCode: 'SERVICE_ERROR'
          }
        }
      }));
      service['handleTimeoutErrorMessage'] = jasmine.createSpy().and.returnValue('Connection timeout');

      service.placeBet(bet, event, selection).subscribe(null, error => {
        expect(error).toEqual('Connection timeout');
      });
      expect(service['handleTimeoutErrorMessage']).toHaveBeenCalled();
    });

    it('should trigger place bet request wrapper and return UNAUTHORIZED_ACCESS error', () => {
      remoteBetslipService.placeBet.and.returnValue(throwError({
        data: {
          error: {
            code: 'UNAUTHORIZED_ACCESS',
            description: '',
            subErrorCode: 'UNAUTHORIZED_ACCESS'
          }
        }
      }));
      service['authorizeAndPlaceBet'] = jasmine.createSpy().and.returnValue(observableOf([]));

      service.placeBet(bet, event, selection).subscribe(null, () => {});
      expect(service['authorizeAndPlaceBet']).toHaveBeenCalled();
    });

    it('should track to NR (happy-flow)', () => {
      spyOn(service as any, 'betPlacementSuccess').and.returnValue(observableOf(null));
      service.placeBet(bet, event, selection).subscribe(() => {
        expect(awsService.addAction).toHaveBeenCalledWith('yourcallBetslipService=>placeBet=>Start', jasmine.any(Object));
        expect(awsService.addAction).toHaveBeenCalledWith('yourcallBetslipService=>placeBet=>Done', jasmine.any(Object));
        expect(service['betPlacementSuccess']).toHaveBeenCalledWith([] as any);
      });
    });

    it('should handle error from excluded from betting user', () => {
      const successHandlerFn = jasmine.createSpy('successHandler');
      const errorHandlerFn = jasmine.createSpy('errorHandler');
      const placeBetResponse = {
        data: {
          betFailure: {
            betNo: 0,
            betError: [{
              betFailureCode: 500,
              betFailureDesc: 'bet.miscError',
              betFailureReason: 'system error: unknown bet placement error'
            }]
          },
          betPlacement: [],
          responseCode: '6'
        }
      };

      coreTools.hasOwnDeepProperty.and.returnValue(false);
      localeService.getString.and.callFake(v => v);
      remoteBetslipService.placeBet.and.returnValue(observableOf(placeBetResponse));

      service.placeBet(bet, event, selection).subscribe(successHandlerFn, errorHandlerFn);

      expect(errorHandlerFn).toHaveBeenCalledWith('yourCall.generalPlaceBetError');
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.generalPlaceBetError');
      expect(pubsubService.publish).not.toHaveBeenCalledWith(pubsubService.API.YOURCALL_SELECTION_UPDATE);
    });

    it('should handle general place bet error of price change', () => {
      const successHandlerFn = jasmine.createSpy('successHandler');
      const errorHandlerFn = jasmine.createSpy('errorHandler');
      const placeBetResponse = {
        data: {
          error: {
            code: 'BET_ERROR',
            description: 'price change',
            message: 'Sorry price has changed',
            subErrorCode: 'PRICE_CHANGED',
            price: {
              priceNum: '1',
              priceDen: '2'
            }
          },
          betPlacement: [],
          responseCode: '6'
        }
      };

      coreTools.hasOwnDeepProperty.and.returnValue(true);
      localeService.getString.and.callFake(v => v);
      remoteBetslipService.placeBet.and.returnValue(throwError(placeBetResponse));

      service.placeBet(bet, event, selection).subscribe(successHandlerFn, errorHandlerFn);

      expect(errorHandlerFn).toHaveBeenCalledWith('yourCall.generalPlaceBetError');
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.generalPlaceBetError');
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.YOURCALL_SELECTION_UPDATE,
        jasmine.objectContaining({ skipMessage: true }));
      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(placeBetResponse.data.error.price.priceNum,
        placeBetResponse.data.error.price.priceDen);
    });

    it('should remove currency symbol from free bet value', () => {
      const freeBet = {
        currency: 'UAH',
        price: '1/2',
        stake: '10',
        token: 'token',
        winType: 'yes',
        clientUserAgent: 'S|W|A0000000',
        freeBet: {
          stake: '$12.02'
        }
      } as any;
      service.placeBet(freeBet, event, selection);
      expect(freeBet.freeBet.stake).toBe('12.02');
    });

    it('should call observer.error', fakeAsync(() => {
      const successHandlerFn = jasmine.createSpy('successHandler');

      const placeBetResponse = {
        data: {
          error: {
            code: 'UNAUTHORIZED_ACCESS',
            description: 'price change',
            message: 'Sorry price has changed',
            subErrorCode: 'PRICE_CHANGED',
            price: {
              priceNum: '1',
              priceDen: '2'
            }
          },
          betPlacement: [],
          responseCode: '6'
        }
      };
      coreTools.hasOwnDeepProperty.and.returnValue(true);
      localeService.getString.and.callFake(v => v);
      remoteBetslipService.placeBet.and.returnValue(throwError(placeBetResponse));
      service['authorizeAndPlaceBet'] = jasmine.createSpy().and.returnValue(throwError('error'));

      service.placeBet(bet, event, selection).subscribe(successHandlerFn, (error) => {
        expect(error).toEqual('error');
      });
    }));
  });

  describe('#authorizeAndPlaceBet', () => {
    it('should catch error', () => {
      commandService.executeAsync.and.returnValue(Promise.resolve());
      service['betPlacementError'] = jasmine.createSpy('betPlacementError').and.returnValue('authError');
      remoteBetslipService.placeBet.and.returnValue({
        data: {
          betError: 'Error'
        }
      });
      service['authorizeAndPlaceBet']('ERROR').subscribe(() => {}, (err) => {
        expect(err).toEqual('authError');
        expect(service.placeData.bet.token).toEqual('bppToken');
        expect(remoteBetslipService.placeBet).toHaveBeenCalledWith({
          token: 'bppToken'
        }, jasmine.any(Object));
      });
    });

    it('should catch error after call placeBet', () => {
      service['betPlacementError'] = jasmine.createSpy('betPlacementError').and.returnValue('Error');
      commandService.executeAsync.and.returnValue(Promise.resolve());
      remoteBetslipService.placeBet.and.returnValue(throwError({
        data: {
          error: 'error'
        }
      }));
      service['authorizeAndPlaceBet']('ERROR').subscribe(() => {}, (err) => {
        expect(err).toEqual('Error');
        expect(remoteBetslipService.placeBet).toHaveBeenCalledWith({
          token: 'bppToken'
        }, jasmine.any(Object));
        expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledWith({
          data: {
            error: 'error'
          }
        }, 'data.error');
      });
    });

    it('should catch error after call placeBet with errorResponse', () => {
      service['betPlacementError'] = jasmine.createSpy('betPlacementError').and.returnValue('Error');
      commandService.executeAsync.and.returnValue(Promise.resolve());
      remoteBetslipService.placeBet.and.returnValue(throwError({
        data: {
          error: 'error'
        }
      }));
      coreTools.hasOwnDeepProperty.and.returnValue(false);
      service['authorizeAndPlaceBet']('ERROR').subscribe(() => {}, (err) => {
        expect(err).toEqual('Error');
        expect(remoteBetslipService.placeBet).toHaveBeenCalledWith({
          token: 'bppToken'
        }, jasmine.any(Object));
      });
    });

    it('should  call betPlacementSuccessHandler', () => {
      commandService.executeAsync.and.returnValue(Promise.resolve());
      remoteBetslipService.placeBet.and.returnValue(of({
        data: {}
      }));
      service['betPlacementSuccessHandler'] = jasmine.createSpy('betPlacementSuccessHandler');

      service['authorizeAndPlaceBet']('ERROR').subscribe(() => {}, () => {
        expect(service['betPlacementSuccessHandler']).toHaveBeenCalled();
      });
    });
  });

  describe('trackPlaceBetError', () => {
    it('should track to GA and NR with betType = Multiple', () => {
      const bet = {
        events: [{
          name: 'events1'
        }, {
          name: 'events2'
        }]
      };
      service['trackPlaceBetError']({code: '12345'} as any, bet as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'quickbet',
        eventAction: 'place bet',
        eventLabel: 'failure',
        errorMessage: undefined,
        errorCode: '12345',
        betType: 'Multiple',
        location: 'yourcall'
      });
      expect(awsService.addAction).toHaveBeenCalledWith(
        'yourcallBetslipService=>placeBet=>Error',
        {date: jasmine.any(Number), errCode: '12345'}
      );
    });
    it('should track to GA and NR', () => {
      service['trackPlaceBetError']({code: '12345'} as any, {} as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.any(Object));
      expect(awsService.addAction).toHaveBeenCalledWith(
        'yourcallBetslipService=>placeBet=>Error',
        {date: jasmine.any(Number), errCode: '12345'}
      );
    });

  });

  describe('#removeSelection', () => {
    it('should call remoteBetslipService.removeSelection', () => {
      service.removeSelection();

      expect(remoteBetslipService.removeSelection).toHaveBeenCalledWith({
        add: {
          request: '50001',
          success: '51001',
          error: '51002',
          change: ''
        },
        remove: {
          request: '30002',
          success: '30003'
        },
        placeBet: {
          request: '50011',
          success: '51101',
          error: '51102'
        }
      });
    });
  });

  describe('#getOdds', () => {
    it('should return odds without oddsData.odds', () => {
      const betOdds = {
        data: {
          priceDen: 1,
          priceNum: 10
        }
      };
      fracToDecService.getDecimal.and.returnValue('decimal');

      const result = service['getOdds'](betOdds);

      expect(result).toEqual({
        dec: 'decimal',
        frac: '10/1'
      });
    });

    it('should return odds as {}', () => {
      const betOdds = {
        data: {
          priceDen: 1
        }
      };
      fracToDecService.getDecimal.and.returnValue('decimal');

      const result = service['getOdds'](betOdds as any);

      expect(result).toEqual({});
    });
  });

  describe('#betPlacementSuccess', () => {
    it('should return receiptData data', () => {
      const response = {
        data: {
          betPlacement: [],
          token: 'token'
        }
      };
      service['trackPlaceBetSuccess'] = jasmine.createSpy('trackPlaceBetSuccess');
      service['betPlacementSuccess'](response).subscribe(data => {
        expect(data).toEqual({
          data: {
            betPlacement: [],
            token: 'token'
          }
        } as any);
      });
    });
    it('should return receiptData data with betPlacement object', () => {
      const response = {
        data: {
          betPlacement: [{
            obBetId: '1'
          }],
          token: 'token'
        }
      };
      service['trackPlaceBetSuccess'] = jasmine.createSpy('trackPlaceBetSuccess');
      service['betPlacementSuccess'](response as any).subscribe(data => {
        expect(data).toEqual({
          data: {
            obBetId: '1'
          }
        } as any);
      });
      expect(service.placeData).toEqual(null);
    });
  });

  describe('#getErrorMsg', () => {
    it('should return providerErrorMsg', () => {
      const error = {
        code: 'Error',
        description: 'Connection timeout',
        subErrorCode: 'SERVICE_ERROR'
      };
      yourcallProviderService.helper.getPlaceBetErrorMsg.and.returnValue('error');

      const result = service['getErrorMsg'](error);

      expect(result).toEqual('error');
    });

    it('should return serverError', () => {
      const error = {
        code: 'INTERNAL_PLACE_BET_PROCESSING',
        description: 'Connection timeout',
        subErrorCode: 'SERVICE_ERROR'
      };
      yourcallProviderService.helper.getPlaceBetErrorMsg.and.returnValue(null);
      localeService.getString.and.returnValue('serverError');

      const result = service['getErrorMsg'](error);

      expect(result).toEqual('serverError');
    });

    it('should return generalPlaceBetError', () => {
      const error = {
        code: 'error',
        description: 'Connection timeout',
        subErrorCode: 'SERVICE_ERROR'
      };
      yourcallProviderService.helper.getPlaceBetErrorMsg.and.returnValue(null);
      localeService.getString.and.returnValue('generalPlaceBetError');

      const result = service['getErrorMsg'](error);

      expect(result).toEqual('generalPlaceBetError');
    });
  });

  describe('#betPlacementSuccessHandler', () => {
    it('should return error', () => {
      service['betPlacementSuccess'] = jasmine.createSpy('betPlacementSuccess').and.returnValue(throwError('error'));
      service['betPlacementSuccessHandler']({} as any, observer);

      expect(observer.error).toHaveBeenCalledWith('error');
      expect(observer.complete).toHaveBeenCalled();
    });

    it('should call observer.next()', () => {
      const response = {
        data: {
          betPlacement: [],
          token: 'token'
        }
      };

      service['betPlacementSuccessHandler'](response as any, observer);

      expect(observer.next).toHaveBeenCalledWith({ data: { betPlacement: [], token: 'token' } });
      expect(observer.complete).toHaveBeenCalled();
    });
  });

  describe('#handleTimeoutErrorMessage', () => {
    it('should getString', () => {
      localeService.getString.and.returnValue('TIMEOUT_ERROR');
      const result = service['handleTimeoutErrorMessage']();

      expect(result).toEqual('TIMEOUT_ERROR');
    });
  });

  describe('trackPlaceBetSuccess', () => {
    it('(events === 1 and 5-a-side and not eventIsLive and not isYourCallBet)', () => {
      testingObj.ecommerce.purchase.products[0].dimension62 = '0';
      testingObj.ecommerce.purchase.products[0].dimension63 = '0';
      testingObj.ecommerce.purchase.products[0].metric1 = 2.05;
      location['path'].and.returnValue('/5-a-side');
      testingObj.ecommerce.purchase.products[0].brand = '5-A-Side';
      testingObj.ecommerce.purchase.products[0].dimension65 = '5-A-Side';
      service['trackPlaceBetSuccess']({
          receipt: 'teststr',
          totalStake: '1.2',
          events: [{}],
          numLines: 1,
          betId: 77918,
        } as any, {} as any,
        { eventIsLive: false,
          sportId: '16',
          typeId: 442,
          id: 776939
        },
        { isYourCallBet: false,
          potentialPayout: '1.2',
          stake: '1.2',
          betOdds: '29.00',
          freebetValue: 2.05} as any);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', testingObj);
      expect(awsService.addAction).toHaveBeenCalledWith('yourcallBetslipService=>placeBet=>Success',
        {
          date: jasmine.any(Number),
          betID: testingObj.betID
        });
    });

    it('(events > 2 and 5-a-side)', () => {
      testingObj.betType = 'Multiple';
      location['path'].and.returnValue('/5-a-side');
      testingObj.ecommerce.purchase.products[0].brand = '5-A-Side';
      testingObj.ecommerce.purchase.products[0].dimension65 = '5-A-Side';
      testingObj.ecommerce.purchase.products[0].metric1 = 0;
      service['trackPlaceBetSuccess']({
        receiptData: ['1', '2'],
        receipt: 'teststr',
        events: [{}, {}],
        numLines: 1,
        betId: 77918,
        totalStake: '1.2'
        } as any, {} as any,
        { eventIsLive: false,
          sportId: '16',
          typeId: 442,
          id: 776939
        },
        { isYourCallBet: false,
          potentialPayout: '1.2',
          stake: '1.2',
          betOdds: '29.00'} as any);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', testingObj);
    });

    it('(events > 2 and 5-a-side and eventIsLive and isYourCallBet)', () => {
      testingObj.ecommerce.purchase.products[0].dimension62 = '1';
      testingObj.ecommerce.purchase.products[0].dimension63 = '1';
      testingObj.ecommerce.purchase.products[0].metric1 = 0;
      testingObj.betType = 'Multiple';
      location['path'].and.returnValue('/5-a-side');
      testingObj.ecommerce.purchase.products[0].brand = '5-A-Side';
      testingObj.ecommerce.purchase.products[0].dimension65 = '5-A-Side';
      testingObj.ecommerce.purchase.products[0]['dimension181']  = 'predefined stake'
      service['stakeFromQb'] = 1;
      service['digitKeyBoardStatus'] = false;
      service['trackPlaceBetSuccess']({
          receipt: 'teststr',
          events: [{}, {}],
          numLines: 1,
          betId: 77918,
          totalStake: '1.2'
        } as any, {} as any,
        { eventIsLive: true,
          sportId: '16',
          typeId: 442,
          id: 776939
        },
        { isYourCallBet: true,
          potentialPayout: '1.2',
          stake: '1.2',
          betOdds: '29.00'} as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining(
        { eventCategory: 'quickbet', eventAction: 'place bet', eventLabel: 'success', betID: 'teststr', betType: 'Multiple' }));
    });

    it('(events > 2 and 5-a-side and not eventIsLive and not isYourCallBet)', () => {
      testingObj.ecommerce.purchase.products[0].dimension62 = '0';
      testingObj.ecommerce.purchase.products[0].dimension63 = '0';
      testingObj.ecommerce.purchase.products[0].metric1 = 0;
      testingObj.betType = 'Multiple';
      location['path'].and.returnValue('/5-a-side');
      testingObj.ecommerce.purchase.products[0].brand = '5-A-Side';
      testingObj.ecommerce.purchase.products[0].dimension65 = '5-A-Side';
      testingObj.ecommerce.purchase.products[0]['dimension181']  = 'keypad predefined stake'
      service['stakeFromQb'] = 2;
      service['digitKeyBoardStatus'] = true;
      service['trackPlaceBetSuccess']({
          receipt: 'teststr',
          events: [{}, {}],
          numLines: 1,
          betId: 77918,
          totalStake: '1.2'
        } as any, {} as any,
        { eventIsLive: false,
          sportId: '16',
          typeId: 442,
          id: 776939
        },
        { isYourCallBet: false,
          potentialPayout: '1.2',
          stake: '1.2',
          betOdds: '29.00'} as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', testingObj);
    });
  });

  describe('getErrorMsg', () => {
    it('bet not allowed error', () => {
      service['getErrorMsg']([{ betFailureDesc: 'CUST_RULES_EXCLUDE' }] as any);
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.betNotAllowedError');
    });

    it('generic error', () => {
      service['getErrorMsg'](null);
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.generalPlaceBetError');
    });
  });
});
