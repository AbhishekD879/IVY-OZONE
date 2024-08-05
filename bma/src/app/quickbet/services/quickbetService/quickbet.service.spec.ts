import { throwError, of as observableOf } from 'rxjs';
import { tick, fakeAsync } from '@angular/core/testing';
import { QuickbetService } from './quickbet.service';
import { quickbet } from '@localeModule/translations/en-US/quickbet.lang';
import { HttpHeaders } from '@angular/common/http';

describe('QuickbetService', () => {
  let pubSubService;
  let userService;
  let localeService;
  let deviceService;
  let quickbetSelectionBuilder;
  let quickbetUpdateService;
  let sessionStorageService;
  let commandService;
  let remoteBetslipService;
  let infoDialogService;
  let cmsService;
  let awsService;
  let windowRefService;
  let templateService;
  let service;
  let storageService;
  let http;

  const betData = {
    'startTime': '2020-12-28T09:13:09Z',
    'username': 'user',
    'eventId': '12345',
    'categoryId': '21'
  };

  const mock = {
    location: 'Bet Receipt',
    module: 'RP Tip',
    dimension86: 0,
    dimension87: 0,
    dimension88: null
  } as any;

  beforeEach(() => {
    pubSubService = {
      API: {
        ADD_TO_QUICKBET: 'ADD_TO_QUICKBET',
        RENDER_QUICKBET_COMPONENT: 'RENDER_QUICKBET_COMPONENT',
        REMOVE_FROM_QUICKBET: 'REMOVE_FROM_QUICKBET'
      },
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      publishSync: jasmine.createSpy('publishSync')
    };

    userService = {
      status: true,
      oddsFormat: 'dec',
      bppToken: 'BPP_TOKEN',
      set: jasmine.createSpy(),
      currencySymbol: '$',
      username: 'test'
    };

    localeService = {
      getString: jasmine.createSpy('getString')
    };

    deviceService = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true)
    };

    quickbetSelectionBuilder = {
      build: jasmine.createSpy('build').and.returnValue({})
    };
    quickbetUpdateService = {
      saveSelectionData: jasmine.createSpy('saveSelectionData').and.returnValue({}),
      getOdds: jasmine.createSpy('getOdds').and.returnValue('1'),
      updateOutcomePrice: jasmine.createSpy('updateOutcomePrice')
    };
    sessionStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue({}),
      remove: jasmine.createSpy('remove')
    };

    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      register: jasmine.createSpy('register'),
      API: {
        BPP_AUTH_SEQUENCE: 'BPP_AUTH_SEQUENCE'
      }
    };

    remoteBetslipService = {
      placeBet: jasmine.createSpy('placeBet').and.returnValue(
        observableOf({
          data: {
            receipt: [],
            error: {}
          }
        })
      ),
      removeSelection: jasmine.createSpy('removeSelection'),
      addSelection: jasmine.createSpy('addSelection').and.returnValue(
        observableOf({
          data: {
            event: {},
            request: {},
            selectionPrice: {}
          }
        })
      )
    };

    infoDialogService = {
      openInfoDialog: jasmine.createSpy(),
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup')
    };

    cmsService = {
      getOddsBoost: jasmine.createSpy()
    };

    awsService = {
      addAction: jasmine.createSpy()
    };

    windowRefService = {
      nativeWindow: jasmine.createSpyObj('nativeWindow', ['setTimeout', 'clearTimeout'])
    };

    templateService = {
      genEachWayPlaces: jasmine.createSpy('genEachWayPlaces').and.returnValue('1-2-3-4')
    };

    storageService = {
      get: jasmine.createSpy('storageService.get').and.returnValue(undefined),
      set: jasmine.createSpy('storageService.set')
    };

    http = {
      post: jasmine.createSpy().and.returnValue(observableOf({ body: {} }))
    };

    service = new QuickbetService(
      pubSubService,
      userService,
      localeService,
      deviceService,
      quickbetSelectionBuilder,
      quickbetUpdateService,
      sessionStorageService,
      commandService,
      remoteBetslipService,
      infoDialogService,
      cmsService,
      awsService,
      windowRefService,
      templateService,
      storageService,
      http
    );
  });

  it('get racingPostTip', () => {
    service['_racingPostTip'] = betData;
    expect(service.racingPostTip).toEqual(betData);
  });

  it('set racingPostTip', () => {
    service.racingPostTip = betData as any;
    expect(service['_racingPostTip']).toBe(betData);
  });



  it('handlePriceErrorMessage (doUpdate: true)', () => {
    const error = {
      price: {
        priceNum: '11',
        priceDen: '55',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const selection = {
      oldPrice: {
        priceNum: '1',
        priceDen: '4',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      },
      price: {
        priceNum: '1',
        priceDen: '2',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const doUpdate = true;
    quickbetUpdateService.updateOutcomePrice = jasmine.createSpy();

    service.handlePriceErrorMessage(error, selection, doUpdate);

    expect(localeService.getString).toHaveBeenCalledWith(
      'quickbet.betPlacementErrors.PRICE_CHANGED',
      [jasmine.any(String), jasmine.any(String)]
    );
  });

  it('handlePriceErrorMessage (getOdds call, selection: oldPrice)', () => {
    const error = {
      price: {
        priceNum: '11',
        priceDen: '55',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const selection = {
      oldPrice: {
        priceNum: '1',
        priceDen: '4',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      },
      price: {
        priceNum: '1',
        priceDen: '2',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const doUpdate = true;

    service.getOdds = jasmine.createSpy();
    quickbetUpdateService.updateOutcomePrice = jasmine.createSpy();

    service.handlePriceErrorMessage(error, selection, doUpdate);

    expect(service.getOdds).toHaveBeenCalledTimes(2);
    expect(service.getOdds).toHaveBeenCalledWith(selection.oldPrice);
  });
  it('handlePriceErrorMessage (getOdds call, selection: price)', () => {
    const error = {
      price: {
        priceNum: '11',
        priceDen: '55',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const selection = {
      price: {
        priceNum: '1',
        priceDen: '2',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const doUpdate = true;

    service.getOdds = jasmine.createSpy();
    quickbetUpdateService.updateOutcomePrice = jasmine.createSpy();

    service.handlePriceErrorMessage(error, selection, doUpdate);

    expect(service.getOdds).toHaveBeenCalledTimes(2);
    expect(service.getOdds).toHaveBeenCalledWith(selection.price);
  });

  it('handlePriceErrorMessage (doUpdate: false)', () => {
    const error = {
      price: {
        priceNum: '11',
        priceDen: '55',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const selection = {
      oldPrice: {
        priceNum: '1',
        priceDen: '4',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      },
      price: {
        priceNum: '1',
        priceDen: '2',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const doUpdate = false;
    quickbetUpdateService.updateOutcomePrice = jasmine.createSpy();
    service.handlePriceErrorMessage(error, selection, doUpdate);

    expect(localeService.getString).toHaveBeenCalledWith(
      'quickbet.betPlacementErrors.PRICE_CHANGED',
      [jasmine.any(String), jasmine.any(String)]
    );
    expect(quickbetUpdateService.updateOutcomePrice).not.toHaveBeenCalled();
  });

  it('should execute pubsub with ADD_TO_QUICKBET', fakeAsync(() => {
    service.showQuickbet({ test: 'obj' });
    tick(501);
    expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.ADD_TO_QUICKBET, {
      test: 'obj'
    });
    expect(infoDialogService.openConnectionLostPopup).not.toHaveBeenCalled();
  }));

  it('should open connection lost popup', fakeAsync(() => {
    deviceService.isOnline.and.returnValue(false);
    service.showQuickbet({ test: 'obj' }).catch(() => { });
    tick(501);
    expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
  }));

  it('should pass dynamic tagging for quickbet', () => {
    const iGtmOrigin = {
      location: 'dummyLocation',
      module: 'dummyModule'
    }
    service.showQuickbet({ test: 'obj' }, iGtmOrigin);
    expect(service.dynamicGtmObj).toBeTruthy();
    expect(service.dynamicGtmObj).toBe(iGtmOrigin);
  })

  it('should return build and save selection', fakeAsync(() => {
    const requestParams = {
      additional: {
        scorecastMarketId: 10
      },
      outcomeIds: [1, 2],
      selectionType: ''
    };
    service.makeAddSelectionRequest(requestParams).subscribe(result => {
      expect(quickbetSelectionBuilder.build).toHaveBeenCalled();
      expect(quickbetUpdateService.saveSelectionData).toHaveBeenCalled();
      expect(result).toEqual({});
    });
    tick();
  }));

  it('should return build and save selection with original price', fakeAsync(() => {
    const requestParams = {
      additional: {
        scorecastMarketId: 10
      },
      outcomeIds: [1, 2],
      selectionType: ''
    };
    const originalPrice = {
      priceType: 'LP',
      priceDen: 1,
      priceNum: 2
    };
    const selectionPrice = {
      priceType: 'LP',
      priceDen: 3,
      priceNum: 5
    };
    const successHandler = jasmine.createSpy('success');

    remoteBetslipService.addSelection.and.returnValue(
      observableOf({
        data: {
          event: {},
          request: {},
          selectionPrice
        }
      })
    );

    service.makeAddSelectionRequest(requestParams, originalPrice).subscribe(successHandler);
    tick();

    expect(quickbetSelectionBuilder.build).toHaveBeenCalledWith(jasmine.objectContaining({
      selectionPrice: originalPrice
    }), {});
    expect(successHandler).toHaveBeenCalledWith({});
    expect(quickbetUpdateService.updateOutcomePrice).toHaveBeenCalledWith(selectionPrice);
  }));

  it('should return selection with error key', fakeAsync(() => {
    const requestParams = {
      additional: {
        scorecastMarketId: 10
      },
      outcomeIds: [1, 2],
      selectionType: ''
    };

    remoteBetslipService.addSelection = jasmine.createSpy().and.returnValue(
      observableOf({
        data: {
          error: { test: 123 }
        }
      })
    );

    service = new QuickbetService(
      pubSubService,
      userService,
      localeService,
      deviceService,
      quickbetSelectionBuilder,
      quickbetUpdateService,
      sessionStorageService,
      commandService,
      remoteBetslipService,
      infoDialogService,
      cmsService,
      awsService,
      windowRefService,
      templateService,
      storageService,
      http
    );

    service.makeAddSelectionRequest(requestParams).subscribe(res => {
      expect(quickbetSelectionBuilder.build).not.toHaveBeenCalled();
      expect(quickbetUpdateService.saveSelectionData).not.toHaveBeenCalled();
      expect(res).toEqual({ data: { error: { test: 123 } } });
    });
    tick();
  }));

  it('makeAddSelectionRequest', fakeAsync(() => {
    const requestParams = {
      additional: {
        scorecastMarketId: 10
      },
      outcomeIds: [1, 2],
      selectionType: ''
    };

    remoteBetslipService.addSelection = jasmine.createSpy().and.returnValue(observableOf(undefined));

    service = new QuickbetService(
      pubSubService,
      userService,
      localeService,
      deviceService,
      quickbetSelectionBuilder,
      quickbetUpdateService,
      sessionStorageService,
      commandService,
      remoteBetslipService,
      infoDialogService,
      cmsService,
      awsService,
      windowRefService,
      templateService,
      storageService,
      http
    );

    service.makeAddSelectionRequest(requestParams).subscribe(res => {
      expect(quickbetSelectionBuilder.build).toHaveBeenCalled();
      expect(quickbetUpdateService.saveSelectionData).toHaveBeenCalled();
    });
    tick();
  }));

  it('makeAddSelectionRequest data: { test: "test" }', fakeAsync(() => {
    const requestParams = {
      additional: {
        scorecastMarketId: 10
      },
      outcomeIds: [1, 2],
      selectionType: ''
    };

    remoteBetslipService.addSelection = jasmine
      .createSpy()
      .and.returnValue(observableOf({ test: 'test' }));

    service = new QuickbetService(
      pubSubService,
      userService,
      localeService,
      deviceService,
      quickbetSelectionBuilder,
      quickbetUpdateService,
      sessionStorageService,
      commandService,
      remoteBetslipService,
      infoDialogService,
      cmsService,
      awsService,
      windowRefService,
      templateService,
      storageService,
      http
    );

    service.makeAddSelectionRequest(requestParams).subscribe(res => {
      expect(quickbetSelectionBuilder.build).toHaveBeenCalled();
      expect(quickbetUpdateService.saveSelectionData).toHaveBeenCalled();
    });
    tick();
  }));

  it('should remove bets', () => {
    const selectionData = {
      requestData: { outcomeIds: ['13241'] }
    };
    service.removeSelection(selectionData);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.REMOVE_FROM_QUICKBET, {
      outcomeId: '13241',
      isAddToBetslip: false
    });
    expect(service.selectionData).toBe(null);
    expect(remoteBetslipService.removeSelection).toHaveBeenCalled();
  });

  it('should remove bets without pubsub', () => {
    service.removeSelection();
    expect(pubSubService.publish).not.toHaveBeenCalled();
    expect(service.selectionData).toBe(null);
    expect(remoteBetslipService.removeSelection).toHaveBeenCalled();
  });

  it('should restore selection and render component', () => {
    const selection = {
      data: {
        event: {
          markets: [{
            drilldownTagNames: 'MKTFLAG_LP'
          }]
        },
        request: {},
        selectionPrice: {}
      }
    } as any;
    spyOn(service, 'getStoredSelectionState');
    spyOn(service, 'renderComponent');
    service.restoreSelection(selection);
    expect(quickbetSelectionBuilder.build).toHaveBeenCalled();
    expect(quickbetUpdateService.saveSelectionData).toHaveBeenCalled();
    expect(service.renderComponent).toHaveBeenCalled();
  });

  it('should do nothing if selection have an error', () => {
    const selection = {
      data: {
        event: {
          markets: [{
            drilldownTagNames: 'MKTFLAG_LD'
          }]
        },
        request: {},
        selectionPrice: {},
        error: {}
      }
    };
    spyOn(service, 'renderComponent');
    service.restoreSelection(selection);
    expect(quickbetSelectionBuilder.build).not.toHaveBeenCalled();
    expect(quickbetUpdateService.saveSelectionData).not.toHaveBeenCalled();
    expect(service.renderComponent).not.toHaveBeenCalled();
  });

  it('restoreSelection no data', () => {
    const selection = {
      data: {
        event: {
          markets: [{
            drilldownTagNames: 'MKTFLAG_LP'
          }]
        },
        request: {},
        selectionPrice: {},
        error: {}
      }
    };
    spyOn(service, 'renderComponent');
    service.restoreSelection(selection);
    expect(quickbetSelectionBuilder.build).not.toHaveBeenCalled();
    expect(quickbetUpdateService.saveSelectionData).not.toHaveBeenCalled();
    expect(service.renderComponent).not.toHaveBeenCalled();
  });

  it('should return restored selection', () => {
    expect(service.restoredSelection).toBeDefined();
    const response = service.getRestoredSelection();
    expect(response).toBe(null);
  });

  it('should save quick bet into storage', fakeAsync(() => {
    windowRefService.nativeWindow.setTimeout.and.callFake(window.setTimeout);

    service.saveQBStateInStorage();
    tick(501);
    expect(sessionStorageService.set).toHaveBeenCalled();
    expect(service.sessionStrUpdateTimeout).toBeNull();
  }));

  it('should not save quick bet into storage if timeout not reached', fakeAsync(() => {
    windowRefService.nativeWindow.setTimeout.and.callFake(window.setTimeout);

    service.saveQBStateInStorage();

    tick(250);
    expect(sessionStorageService.set).not.toHaveBeenCalled();
    expect(service.sessionStrUpdateTimeout).toEqual(jasmine.any(Number));

    tick(500);
    expect(service.sessionStrUpdateTimeout).toBeNull();
  }));

  it('saveQBStateInStorage with data', fakeAsync(() => {
    windowRefService.nativeWindow.setTimeout.and.callFake(window.setTimeout);

    service.saveQBStateInStorage({ userEachWay: false, userStake: false });

    tick(250);
    expect(sessionStorageService.set).not.toHaveBeenCalled();
    expect(service.sessionStrUpdateTimeout).toEqual(jasmine.any(Number));

    tick(500);
    expect(service.sessionStrUpdateTimeout).toBeNull();
  }));

  it('saveQBStateInStorage(sessionStrUpdateTimeout: false)', fakeAsync(() => {
    service.sessionStrUpdateTimeout = 20;
    service.saveQBStateInStorage();

    tick(250);
    expect(sessionStorageService.set).not.toHaveBeenCalled();
    expect(service.sessionStrUpdateTimeout).toEqual(jasmine.any(Number));
  }));

  it('should remove quick bet from storage', () => {
    service.removeQBStateFromStorage();
    expect(sessionStorageService.remove).toHaveBeenCalledWith('quickbetSelection');
    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
  });

  it('should not save selection to storage if removeQBStateFromStorage called', fakeAsync(() => {
    windowRefService.nativeWindow.setTimeout.and.callFake(window.setTimeout);
    windowRefService.nativeWindow.clearTimeout.and.callFake(window.clearTimeout);

    service.saveQBStateInStorage();
    expect(service.sessionStrUpdateTimeout).toEqual(jasmine.any(Number));

    service.removeQBStateFromStorage();
    tick(501);

    expect(sessionStorageService.set).not.toHaveBeenCalled();
    expect(service.sessionStrUpdateTimeout).toBeNull();
  }));

  it('should call getOdds method', () => {
    service.getOdds();
    expect();
  });

  it('acceptChangedBoost', () => {
    service['reboost'] = true;

    expect(service.acceptChangedBoost()).toBeTruthy();
    expect(service['reboost']).toBeFalsy();
  });

  it('acceptChangedBoost reboost false', () => {
    expect(service.acceptChangedBoost()).toBeFalsy();
  });

  it('activateReboost', () => {
    service.activateReboost();
    expect(service.reboost).toBeTruthy();
  });

  it('should return SP for SP price type', () => {
    const price = {
      id: 2312323,
      priceDec: '2.75',
      priceDen: 7,
      priceNum: 4,
      priceType: 'SP',
      isPriceChanged: false,
      isPriceUp: false,
      isPriceDown: false,
      priceTypeRef: { id: '' },
      handicapValueDec: ''
    };

    quickbetUpdateService.getOdds.and.returnValue('SP');
    expect(service.getOdds(price)).toBe('SP');
  });

  it('should return price in fractional format', () => {
    const price = {
      id: 2312323,
      priceDec: '2.75',
      priceDen: 7,
      priceNum: 4,
      priceType: 'LP',
      isPriceChanged: false,
      isPriceUp: false,
      isPriceDown: false,
      priceTypeRef: { id: '' },
      handicapValueDec: ''
    };

    service.userService.oddsFormat = 'frac';
    quickbetUpdateService.getOdds.and.returnValue('4/7');
    expect(service.getOdds(price)).toBe('4/7');
  });
  it('isVirtualSport (true)', () => {
    expect(service.isVirtualSport('Virtual Sports')).toBeTruthy();
  });
  it('isVirtualSport (false)', () => {
    expect(service.isVirtualSport('test')).toBeFalsy();
  });
  it('handleStakeTooLowErrorMessage', () => {
    const error = {
      stake: {
        minAllowed: '5.00'
      }
    };
    service.localeService.getString = jasmine.createSpy().and.returnValue('Minimum stake is £5.00');
    expect(service.handleStakeTooLowErrorMessage(error)).toEqual('Minimum stake is £5.00');
    expect(service.localeService.getString).toHaveBeenCalled();
  });
  it('handleStakeTooHighErrorMessage', () => {
    const error = {
      stake: {
        maxAllowed: '20.00'
      }
    };
    service.localeService.getString = jasmine.createSpy().and.returnValue('Maximum stake is £20.00');
    expect(service.handleStakeTooHighErrorMessage(error)).toEqual('Maximum stake is £20.00');
    expect(service.localeService.getString).toHaveBeenCalled();
  });

  describe('Handle bet placement error', () => {
    it('should return error DEFAULT_PLACEBET_ERROR', () => {
      const error = {
        code: 'DEFAULT_PLACEBET_ERROR',
        description: '',
        subErrorCode: ''
      };

      service.localeService.getString.and.returnValue(
        quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR
      );
      const response = service.getBetPlacementErrorMessage(error, {});
      expect(service.localeService.getString).toHaveBeenCalledWith(
        'quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR'
      );
      expect(response).toBe(quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR);
    });

    it('should return error DEFAULT_PLACEBET_ERROR if got a SERVICE_ERROR', () => {
      const error = {
        code: 'SERVICE_ERROR',
        description: '',
        subErrorCode: ''
      };
      service.localeService.getString.and.returnValues(
        'KEY_NOT_FOUND',
        'KEY_NOT_FOUND',
        quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR
      );
      const response = service.getBetPlacementErrorMessage(error, {});
      expect(service.localeService.getString).toHaveBeenCalledWith('quickbet.betPlacementErrors.');
      expect(service.localeService.getString).toHaveBeenCalledWith(
        'quickbet.betPlacementErrors.SERVICE_ERROR'
      );
      expect(service.localeService.getString).toHaveBeenCalledWith(
        'quickbet.betPlacementErrors.TIMEOUT_ERROR'
      );
      expect(response).toBe(quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR);
    });

    it('should call specific error handler for BAD_FREEBET_TOKEN error', () => {
      service.getBetPlacementErrorMessage(
        { subErrorCode: 'BAD_FREEBET_TOKEN' },
        { isBoostActive: true }
      );
      expect(localeService.getString).toHaveBeenCalledWith('quickbet.oddsBoostExpiredOrRedeemed');

      service.getBetPlacementErrorMessage(
        { subErrorCode: 'BAD_FREEBET_TOKEN' },
        { isBoostActive: false }
      );
      expect(localeService.getString).toHaveBeenCalledWith(
        'quickbet.betPlacementErrors.BAD_FREEBET_TOKEN'
      );
    });
    it('getBetPlacementErrorMessage (error.description === undefined', () => {
      const error = {
        code: 'CONNECTION_TIMEOUT',
        subErrorCode: ''
      };
      localeService.getString = jasmine.createSpy('getString').and.returnValue('KEY_NOT_FOUND');
      awsService.addAction = jasmine.createSpy();
      service.getBetPlacementErrorMessage(error, {});
      expect(awsService.addAction).toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith(
        'quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR'
      );
    });
    it('getBetPlacementErrorMessage (error.description === "Connection timeout"', () => {
      const error = {
        code: 'CONNECTION_TIMEOUT',
        description: 'Connection timeout',
        subErrorCode: ''
      };
      localeService.getString = jasmine.createSpy('getString').and.returnValue('test_error');
      expect(service.getBetPlacementErrorMessage(error, {})).toEqual('test_error');
    });

    it('should (doUpdate:true)', () => {
      const error = {
        code: 'SERVICE_ERROR',
        description: '',
        subErrorCode: ''
      };
      service.handleTimeoutErrorMessage = jasmine.createSpy();
      service.getBetPlacementErrorMessage(error, {}, true);
      expect(service.handleTimeoutErrorMessage).toHaveBeenCalledWith(error, {}, true);
    });

    it('should handle INTERNAL_PLACE_BET_PROCESSING as TimeoutErrorMessage (doUpdate:true)', () => {
      const error = {
        code: 'INTERNAL_PLACE_BET_PROCESSING',
        description: '',
        subErrorCode: ''
      };
      service.handleTimeoutErrorMessage = jasmine.createSpy();
      service.getBetPlacementErrorMessage(error, {}, true);
      expect(service.handleTimeoutErrorMessage).toHaveBeenCalledWith(error, {}, true);
    });

    it('bet not permitted', () => {
      service.getBetPlacementErrorMessage({ description: 'This bet is not permitted for your account' }, {});
      expect(localeService.getString).toHaveBeenCalledWith('quickbet.betPlacementErrors.BET_NOT_PERMITTED');
    });
  });

  it('placeBetRequest', fakeAsync(() => {
    service.placeBetRequest({}).subscribe(response => {
      expect(remoteBetslipService.placeBet).toHaveBeenCalled();
    });
    tick();
  }));

  it('placeBetRequest error', fakeAsync(() => {
    remoteBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(
      observableOf({
        data: {
          error: 'error'
        }
      })
    );
    service.placeBetRequest({}).subscribe(null, response => {
      expect(remoteBetslipService.placeBet).toHaveBeenCalled();
    });
    tick();
  }));

  it('placeBetRequest throw error', fakeAsync(() => {
    remoteBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(
      throwError({
        data: {
          error: {
            code: 'UNAUTHORIZED_ACCESS',
            description: '',
            subErrorCode: 'UNAUTHORIZED_ACCESS'
          }
        }
      })
    );
    service.placeBetRequest({}).subscribe(null, response => {
      expect(remoteBetslipService.placeBet).toHaveBeenCalled();
    });
    tick();
  }));

  it('should render component', () => {
    service.renderComponent();
    expect(pubSubService.publishSync).toHaveBeenCalledWith(
      'RENDER_QUICKBET_COMPONENT', undefined
    );
  });

  it('should render component and add to quickbet', () => {
    service.renderComponent({});
    expect(pubSubService.publishSync).toHaveBeenCalledWith('RENDER_QUICKBET_COMPONENT', {});
    expect(pubSubService.publishSync).toHaveBeenCalledWith('ADD_TO_QUICKBET', {});
  });

  it('should return session key', () => {
    service.getStoredSelectionState();
    expect(sessionStorageService.get).toHaveBeenCalledWith('quickbetSelection');
  });

  it('should return {}', () => {
    sessionStorageService.get = jasmine.createSpy().and.returnValue(false);
    service.getStoredSelectionState();
    expect(service.getStoredSelectionState()).toEqual({});
  });

  it('should handle handicap error', () => {
    const error = {
      price: {
        priceNum: '11',
        priceDen: '55',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const selection = {
      oldHandicapValue: '1',
      handicapValue: 2,
      formatHandicap: jasmine.createSpy('formatHandicap'),
      oldPrice: {
        priceNum: '1',
        priceDen: '4',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      },
      price: {
        priceNum: '1',
        priceDen: '2',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    service.handleHandicapErrorMessage(error, selection, false);
    expect(localeService.getString).toHaveBeenCalledWith(
      'quickbet.betPlacementErrors.HANDICAP_CHANGED',
      [selection.oldHandicapValue, selection.handicapValue]
    );
  });

  it('should update new handle handicap', () => {
    const error = {
      price: {
        priceNum: '11',
        priceDen: '55',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    const selection = {
      oldHandicapValue: '1',
      handicapValue: 2,
      updateHandicapValue: jasmine.createSpy('updateHandicapValue'),
      formatHandicap: jasmine.createSpy('formatHandicap'),
      oldPrice: {
        priceNum: '1',
        priceDen: '4',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      },
      price: {
        priceNum: '1',
        priceDen: '2',
        priceType: 'qwe',
        priceTypeRef: { id: 10 }
      }
    };
    service.handleHandicapErrorMessage(error, selection, true);
    expect(selection.updateHandicapValue).toHaveBeenCalled();
  });

  it('should get error text string', () => {
    service.handleTimeoutErrorMessage();
    expect(localeService.getString).toHaveBeenCalledWith(
      'quickbet.betPlacementErrors.TIMEOUT_ERROR'
    );
  });

  it('should place a bet', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };

    spyOn(service, 'placeBetRequest').and.returnValue(
      throwError({
        code: 'UNAUTHORIZED_ACCESS'
      })
    );
    awsService.addAction = jasmine.createSpy('addAction');

    service.placeBet(betObject).subscribe(
      results => { },
      err => {
        expect(awsService.addAction).toHaveBeenCalled();
        commandService.executeAsync().then(response => {
          expect(err).toEqual({
            code: 'UNAUTHORIZED_ACCESS'
          });
          expect(commandService.executeAsync).toHaveBeenCalledWith('BPP_AUTH_SEQUENCE');
        });
      }
    );
    tick(50);
  }));

  it('placeBet', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    awsService.addAction = jasmine.createSpy('addAction');
    service.placeBet(betObject).subscribe(
      results => {
        expect(awsService.addAction).toHaveBeenCalled();
        expect(storageService.set).toHaveBeenCalledWith('tooltipsSeen', { 'receiptViewsCounter-test': 1 });
      },
      err => { }
    );
    tick(50);
  }));

  it('placeBet with higher views counter', fakeAsync(() => {
    storageService.get = jasmine.createSpy().and.returnValue({ 'receiptViewsCounter-test': 2 });
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    awsService.addAction = jasmine.createSpy('addAction');
    service.placeBet(betObject).subscribe(
      results => {
        expect(awsService.addAction).toHaveBeenCalled();
        expect(storageService.set).toHaveBeenCalledWith('tooltipsSeen', { 'receiptViewsCounter-test': 3 });
      },
      err => { }
    );
    tick(50);
  }));

  it('placeBet subErrorCode: "EXTERNAL_FUNDS_UNAVAILABLE"', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    service.placeBetRequest = jasmine.createSpy('placeBetRequest').and.returnValue(
      throwError({
        subErrorCode: 'EXTERNAL_FUNDS_UNAVAILABLE'
      })
    );
    awsService.addAction = jasmine.createSpy('addAction');
    service.getStoredSelectionState = jasmine
      .createSpy('getStoredSelectionState')
      .and.returnValue({});
    service.placeBet(betObject).subscribe(
      results => { },
      err => {
        expect(awsService.addAction).toHaveBeenCalledTimes(2);
        expect(service.getStoredSelectionState).toHaveBeenCalled();
      }
    );
    tick(50);
  }));

  it('placeBet subErrorCode: "test"', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    service.placeBetRequest = jasmine.createSpy('placeBetRequest').and.returnValue(
      throwError({
        subErrorCode: 'test'
      })
    );
    awsService.addAction = jasmine.createSpy('addAction');
    service.placeBet(betObject).subscribe(
      results => { },
      err => {
        expect(awsService.addAction).toHaveBeenCalledTimes(2);
      }
    );
    tick(50);
  }));

  it('placeBet getStoredSelectionState: not_empty', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    service.placeBetRequest = jasmine.createSpy('placeBetRequest').and.returnValue(
      throwError({
        subErrorCode: 'EXTERNAL_FUNDS_UNAVAILABLE'
      })
    );
    awsService.addAction = jasmine.createSpy('addAction');
    service.getStoredSelectionState = jasmine
      .createSpy('getStoredSelectionState')
      .and.returnValue({ test: 'test' });
    commandService.executeAsync = jasmine.createSpy().and.returnValue(Promise.resolve({}));
    service.placeBet(betObject).subscribe(
      results => { },
      err => {
        expect(awsService.addAction).toHaveBeenCalledTimes(4);
        expect(service.getStoredSelectionState).toHaveBeenCalled();
        expect(commandService.executeAsync).toHaveBeenCalled();
      }
    );
    tick(50);
  }));

  it('placeBet commandService.executeAsync throw error', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    service.placeBetRequest = jasmine.createSpy('placeBetRequest').and.returnValue(
      throwError({
        subErrorCode: 'EXTERNAL_FUNDS_UNAVAILABLE'
      })
    );
    awsService.addAction = jasmine.createSpy('addAction');
    service.getStoredSelectionState = jasmine
      .createSpy('getStoredSelectionState')
      .and.returnValue({ test: 'test' });
    commandService.executeAsync = jasmine.createSpy().and.returnValue(Promise.reject());
    service.placeBet(betObject).subscribe(
      results => { },
      err => {
        expect(awsService.addAction).toHaveBeenCalledTimes(3);
        expect(service.getStoredSelectionState).toHaveBeenCalled();
        expect(commandService.executeAsync).toHaveBeenCalled();
      }
    );
    tick(50);
  }));

  it('placeBet placebetRequest not empty', fakeAsync(() => {
    const betObject = {
      id: '',
      receipt: {
        id: ''
      },
      stake: {
        amount: '1'
      },
      payout: {
        potential: '1'
      },
      price: {
        priceNum: '1',
        priceDen: '1'
      }
    };
    let alreadyCalled = false;
    service.placeBetRequest = jasmine.createSpy('placeBetRequest').and.callFake(() => {
      if (alreadyCalled) {
        return observableOf({
          data: 'data'
        });
      }
      alreadyCalled = true;
      return throwError({
        subErrorCode: 'EXTERNAL_FUNDS_UNAVAILABLE'
      });
    });

    awsService.addAction = jasmine.createSpy('addAction');
    service.getStoredSelectionState = jasmine
      .createSpy('getStoredSelectionState')
      .and.returnValue({ test: 'test' });
    commandService.executeAsync = jasmine.createSpy().and.returnValue(Promise.resolve({}));
    service.placeBet(betObject).subscribe(
      results => { },
      err => {
        expect(awsService.addAction).toHaveBeenCalledTimes(4);
        expect(service.getStoredSelectionState).toHaveBeenCalled();
        expect(commandService.executeAsync).toHaveBeenCalled();
      }
    );
    tick(50);
  }));

  it('addSelection', fakeAsync(() => {
    service.makeAddSelectionRequest = jasmine.createSpy().and.returnValue(observableOf(null));

    service.canUseOddsBoost = () => observableOf(false);
    service.addSelection({}).subscribe();
    tick();
    expect(service.makeAddSelectionRequest).toHaveBeenCalledWith(jasmine.any(Object), undefined, false);

    const originalPrice = { priceType: 'LP' };
    service.canUseOddsBoost = () => observableOf(true);
    service.addSelection({}, originalPrice).subscribe();
    tick();
    expect(service.makeAddSelectionRequest).toHaveBeenCalledWith(
      jasmine.objectContaining({ oddsBoost: true, token: jasmine.any(String) }), originalPrice, false
    );

    service.addSelection({}, originalPrice, true).subscribe();
    tick();
    expect(service.makeAddSelectionRequest).toHaveBeenCalledWith(
    jasmine.objectContaining({ oddsBoost: true, token: jasmine.any(String) }), originalPrice, false
   );
  }));

  describe('canUseOddsBoost', () => {
    it('should return false (user logged out)', fakeAsync(() => {
      userService.status = false;
      service.canUseOddsBoost().subscribe(res => {
        tick();
        expect(res).toBeFalsy();
      });
    }));

    it('should return false (bpp token not existed)', fakeAsync(() => {
      userService.bppToken = null;
      service.canUseOddsBoost().subscribe(res => {
        tick();
        expect(res).toBeFalsy();
      });
    }));

    it('should return false (odds boost disabled in cms)', fakeAsync(() => {
      userService.status = true;
      cmsService.getOddsBoost = () => observableOf({ enabled: false });
      service.canUseOddsBoost().subscribe(res => {
        tick();
        expect(res).toBeFalsy();
      });
    }));

    it('should return true', fakeAsync(() => {
      userService.status = true;
      cmsService.getOddsBoost = () => observableOf({ enabled: true });
      service.canUseOddsBoost().subscribe(res => {
        tick();
        expect(res).toBeTruthy();
      });
    }));
  });

  describe('#getEWTerms', () => {
    it('should call getEWTerms method', () => {
      const legPart = {
        eachWayNum: '1',
        eachWayDen: '2'
      } as any;
      service.getEWTerms(legPart);

      expect(localeService.getString).toHaveBeenCalledWith('quickbet.oddsAPlaces', {
        num: '1',
        den: '2',
        arr: '1-2-3-4'
      });
      expect(templateService.genEachWayPlaces).toHaveBeenCalledWith(legPart, true);
    });

    it('should call getEWTerms method', () => {
      const legPart = {
        eachWayNum: '',
        eachWayDen: '2'
      } as any;

      expect(service.getEWTerms(legPart)).toEqual('');
      expect(localeService.getString).not.toHaveBeenCalled();
      expect(templateService.genEachWayPlaces).not.toHaveBeenCalled();
    });
  });

  describe('#getLinesPerStake', () => {
    it('should call getLinesPerStake method', () => {
      const receipt = {
        numLines: '1',
        amount: '4',
        stakePerLine: '2'
      } as any;
      service.getLinesPerStake(receipt);

      expect(localeService.getString).toHaveBeenCalledWith('quickbet.linesPerStake', {
        lines: 2,
        stake: '$2.00'
      });
    });
  });

  describe('getBybSelectionType', () => {
    it('should get five 5 side type', () => {
      service.getBybSelectionType('f');
      expect(localeService.getString).toHaveBeenCalledWith('quickbet.bybType.fiveASide');
    });

    it('should get build your bet type', () => {
      service.getBybSelectionType('e');
      expect(localeService.getString).toHaveBeenCalledWith('quickbet.bybType.byb');
    });

    it('should not get any type', () => {
      service.getBybSelectionType('');
      expect(localeService.getString).not.toHaveBeenCalled();
    });
  });

  describe('readUpCellData', () => {
    it('should call upcell api call', () => {
      service.readUpCellBets('/v2/placeBet', {});
      const body = {};
      expect(http.post).toHaveBeenCalledWith(`/v2/placeBet`, body,
        jasmine.objectContaining({
          headers: jasmine.any(HttpHeaders)
        })
      );
    });
  });
});
