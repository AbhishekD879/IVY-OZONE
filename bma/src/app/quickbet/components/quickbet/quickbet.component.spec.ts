import { of, Subject, throwError } from 'rxjs';
import { fakeAsync, tick, flush } from '@angular/core/testing';
import { QuickbetComponent } from '@app/quickbet/components/quickbet/quickbet.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { IGtmEventModel } from '@app/quickbet/models/quickbet-gtm-event.model';
import { BETSLIP } from '@app/core/services/remoteBetslip/remote-betslip.constant';

describe('QuickbetComponent', () => {
  let component;
  let locale;
  let pubsub;
  let gtm;
  let quickbetService;
  let remoteBsService;
  let quickbetOverAskService;
  let command;
  let dialogService;
  let infoDialogService;
  let device;
  let nativeBridgeService;
  let location;
  let quickbetDataProviderService;
  let rendererService;
  let windowRef;
  let gtmTrackingService;
  let gtmOrigin;
  let quickbetDepositService;
  let quickbetNotificationService;
  let awsService;
  let userService;
  let changeDetectorRef;
  let sessionStorage, racingPostTipService;
  let arcUserService;
  let storageService;
  let betslipService;
  let scorecastDataService;
  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    locale = jasmine.createSpyObj('localeService', ['getString']);
    pubsub = jasmine.createSpyObj('pubsub', ['subscribe', 'publish', 'publishSync', 'unsubscribe']);
    pubsub.API = pubSubApi;
    // gtm = jasmine.createSpyObj('gtmService', ['push']);
    gtm = {
      push: jasmine.createSpy('push'),
      setSBTrackingData: jasmine.createSpy('setSBTrackingData')
    };
    remoteBsService = jasmine.createSpyObj('remoteBsService', ['connect', 'disconnect']);
    quickbetOverAskService = jasmine.createSpyObj('quickbetOverAskService', ['execute']);
    command = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve())
    };
    command.API = commandApi;
    dialogService = jasmine.createSpyObj('dialogService', ['closeDialogs']);
    infoDialogService = jasmine.createSpyObj('infoDialogService', ['openConnectionLostPopup']);
    device = jasmine.createSpyObj('device', ['isOnline']);
    nativeBridgeService = jasmine.createSpyObj('nativeBridgeService', [
      'onClosePopup',
      'onOpenPopup'
    ]);
    location = jasmine.createSpyObj('locationService', ['path']);
    rendererService = {
      renderer: jasmine.createSpyObj('renderer2', ['removeClass'])
    };
    windowRef = {
      document: jasmine.createSpyObj('document', ['querySelector'])
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}])
    };
    quickbetDataProviderService = {
      quickbetPlaceBetListener: new Subject(),
      quickbetReceiptListener: {
        next: jasmine.createSpy()
      }
    };
    quickbetService = {
      selectionData: null,
      getRestoredSelection: jasmine.createSpy(),
      removeSelection: jasmine.createSpy(),
      removeQBStateFromStorage: jasmine.createSpy(),
      addSelection: jasmine.createSpy('addSelection').and.returnValue(of({})),
      activateReboost: jasmine.createSpy('activateReboost'),
      placeBet: jasmine.createSpy().and.returnValue(
        of([
          {
            receipt: {}
          }
        ])
      ),
      getBetPlacementErrorMessage: jasmine.createSpy().and.returnValue(''),
      getOdds: jasmine.createSpy('getOdds'),
      isVirtualSport: jasmine.createSpy('isVirtualSport'),
      isBetNotPermittedError: jasmine.createSpy('isBetNotPermittedError'),
      getBetNorPermittedError: jasmine.createSpy('getBetNotPermittedError'),
      quickBetOnOverlayCloseSubj: new Subject<string>()
    };
    gtmTrackingService = jasmine.createSpyObj('gtmTrackingService', ['getTracking']);
    gtmOrigin = {
      location: 'location',
      module: 'module'
    };
    quickbetDepositService = {
      update: jasmine.createSpy('update')
    };
    quickbetNotificationService = {
      clear: jasmine.createSpy('clear')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    userService = {
      bppToken: 'bppToken'
    };

    sessionStorage =  {
      get: jasmine.createSpy('get'),
      remove: jasmine.createSpy('remove')
    };
    racingPostTipService = {
      racingPostGTM: undefined
    };
    arcUserService = {
      quickbet: true
    };
    betslipService={
      betKeyboardData:''
    };
    scorecastDataService = {
      setScorecastData: (data)=> { return data},
      getScorecastData: ()=> { 
        return {
          name: 'name',
          eventLocation: 'scorecast',
          teamname: 'teamname',
          playerName: 'playerName',
          result: '24',
          dimension64: '64',
          dimension60: '60',
          dimension61: '61',
          dimension62: '62'
        }
      },
    }
    component = new QuickbetComponent(
      locale,
      pubsub,
      gtm,
      quickbetService,
      remoteBsService,
      quickbetOverAskService,
      command,
      dialogService,
      infoDialogService,
      device,
      nativeBridgeService,
      location,
      quickbetDataProviderService,
      rendererService,
      windowRef,
      gtmTrackingService,
      quickbetDepositService,
      quickbetNotificationService,
      awsService,
      changeDetectorRef,
      userService,
      sessionStorage,
      racingPostTipService,
      arcUserService,
      storageService,
      betslipService,
      scorecastDataService
    );
    component.selection = {};
  });

  describe('addSelectionHandler', () => {
    it('shold call addSelection method with properly argument', () => {
      const params = {
        outcomes: [{id: 'string'}],
        type: 'string',
        additional: {
          scorecastMarketId: 1
        },
        GTMObject: {
          tracking: {}
        },
        details: {
          marketDrilldownTagNames : 'MKTFLAG_LD'
        }
      };
      spyOn(component, 'getSelectionType');
      spyOn(component, 'addSelection');
      component.addSelectionHandler(params);
      expect(component.addSelection).toHaveBeenCalled();
    });

    it('shold call addSelection method with properly argument if selection data dont have details', () => {
      const params = {
        outcomes: [{id: 'string'}],
        type: 'string',
        additional: {
          scorecastMarketId: 1
        },
        GTMObject: {
          tracking: {}
        },
        details: {
        }
      };
      spyOn(component, 'getSelectionType');
      spyOn(component, 'addSelection');
      component.addSelectionHandler(params);
      expect(component.addSelection).toHaveBeenCalled();
    });
    it('shold call addSelection method with properly argument if selection data dont have details', () => {
      const params = {
        outcomes: [{id: 'string'}],
        type: 'string',
        additional: {
          scorecastMarketId: 1
        },
        GTMObject: {
          tracking: {}
        },
        details: {
          marketDrilldownTagNames : 'MKTFLAG_SP'
        }
      };
      spyOn(component, 'getSelectionType');
      spyOn(component, 'addSelection');
      component.addSelectionHandler(params);
      expect(component.addSelection).toHaveBeenCalled();
    });
    it('shold call addSelection method with properly argument if selection data dont have details', () => {
      const params = {
        outcomes: [{id: 'string'}],
        type: 'string',
        additional: {
          scorecastMarketId: 1
        },
        GTMObject: {
          tracking: {}
        },
      };
      spyOn(component, 'getSelectionType');
      spyOn(component, 'addSelection');
      component.addSelectionHandler(params);
      expect(component.addSelection).toHaveBeenCalled();
    });
  });

  describe('closePanel', () => {
    beforeEach(() => {
      spyOn(component as any, 'toggleLoadingOverlay');
      spyOn(component as any, 'removeSubscribers');
      component.selection = null;
    });

    it('should close panel', () => {
      component.isLuckyDip=true;
      component.closePanel();
      expect(quickbetService.removeSelection).toHaveBeenCalled();
      expect(component.toggleLoadingOverlay).toHaveBeenCalledWith({spinner: false, overlay: false});
      expect(pubsub.publish).toHaveBeenCalled();
      expect(quickbetService.removeQBStateFromStorage).toHaveBeenCalled();
      expect(component.removeSubscribers).toHaveBeenCalled();
    });

    it('should close panel, isStreamBet is true', () => {
      component.isLuckyDip=true;
      component.selection = {isStreamBet: true};
      component.closePanel();
      // expect(quickbetService.removeSelection).toHaveBeenCalled();
      expect(component.toggleLoadingOverlay).toHaveBeenCalledWith({spinner: false, overlay: false});
      expect(pubsub.publish).toHaveBeenCalled();
      expect(quickbetService.removeQBStateFromStorage).toHaveBeenCalled();
      expect(component.removeSubscribers).toHaveBeenCalled();
    });

    it('should close panel and skip on reconnect', () => {
      component.selection = {};
      component.closePanel(false);
      expect(quickbetService.removeSelection).toHaveBeenCalled();
      expect(component.toggleLoadingOverlay).toHaveBeenCalledWith({spinner: false, overlay: false});
      expect(pubsub.publish).toHaveBeenCalled();
      expect(quickbetService.removeQBStateFromStorage).toHaveBeenCalled();
      expect(component.removeSubscribers).toHaveBeenCalled();
      expect(component.selection.skipOnReconnect).toBeTruthy();
    });
  });

  describe('addToBetslip', () => {
    it('should open popup if is not connected', () => {
      device.isOnline.and.returnValue(false);
      component.addToBetslip();
      expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    });
    it('should open popup if is digitKeyBoardStatus true', () => {
      device.isOnline.and.returnValue(false);
      component.addToBetslip();
      expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    });

    it('should add to betslip if is connected (manual adding)', () => {
      device.isOnline.and.returnValue(true);  
      component['trackAddBetToQB'] = jasmine.createSpy();
      component['closePanel'] = jasmine.createSpy();
      component['formBetslipSelection'] = jasmine.createSpy().and.returnValue({
        outcomeId: [],
        userEachWay: undefined,
        userStake: undefined,
        type: 'simple',
        price: {priceType: 'SP'},
        isVirtual: false,
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: null
      })
      component.selectionData = {disabled: false} as any;
      component.addToBetslip();

      expect(component.command.executeAsync).toHaveBeenCalled();
      expect(component.trackAddBetToQB).toHaveBeenCalledWith(component.selectionData, true);
      expect(component.closePanel).toHaveBeenCalledWith(true);
    });

    it('should add selection to BS if not receipt', () => {
      device.isOnline.and.returnValue(true);
      spyOn(component, 'trackAddBetToQB');
      spyOn(component, 'closePanel');
      component['formBetslipSelection'] = jasmine.createSpy().and.returnValue({
        outcomeId: [],
        userEachWay: undefined,
        userStake: undefined,
        type: 'simple',
        price: {priceType: 'SP'},
        isVirtual: false,
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: null
      })
      component.stakeFromQb = 1
      component.selectionData = {disabled: false} as any;
      component.addToBetslip(false);

      expect(component.command.executeAsync).toHaveBeenCalled();
      expect(component.closePanel).toHaveBeenCalledWith(true);
    });
    

    it('should not add selection to BS if not receipt but selection is disabled', () => {
      device.isOnline.and.returnValue(true);
      spyOn(component, 'trackAddBetToQB');
      spyOn(component, 'closePanel');
      component['formBetslipSelection'] = jasmine.createSpy().and.returnValue({
        outcomeId: [],
        userEachWay: undefined,
        userStake: undefined,
        type: 'simple',
        price: {priceType: 'SP'},
        isVirtual: false,
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: null
      })
      component.stakeFromQb = 0
      component.selectionData = {
        disabled: true
      } as any;
      component.addToBetslip(false);

      expect(component.command.executeAsync).not.toHaveBeenCalled();
      expect(component.closePanel).toHaveBeenCalledWith(false);
    });

    it('should not add selection to BS if no data (undisplayed)', () => {
      device.isOnline.and.returnValue(true);
      spyOn(component, 'trackAddBetToQB');
      spyOn(component, 'closePanel');
      spyOn(component, 'formBetslipSelection');
      component.selectionData = {} as any;
      component.addToBetslip(false);

      expect(component.command.executeAsync).not.toHaveBeenCalled();
      expect(component.closePanel).toHaveBeenCalledWith(false);
    });

    it('should not add selection to BS if receipt state', () => {
      device.isOnline.and.returnValue(true);
      spyOn(component, 'trackAddBetToQB');
      spyOn(component, 'closePanel');
      spyOn(component, 'formBetslipSelection');
      component.selectionData = {} as any;
      component.addToBetslip(true);

      expect(component.command.executeAsync).not.toHaveBeenCalled();
      expect(component.closePanel).toHaveBeenCalledWith(false);
    });
  });

  it('getSelectionType', () => {
    expect(component.getSelectionType('ab')).toBe('ab');
    expect(component.getSelectionType(1)).toBe('simple');
  });

  describe('restoreSelection', () => {
    it('isRestoreSelection', () => {
      quickbetService.getRestoredSelection.and.returnValue(true);

      spyOn(component, 'toggleLoadingOverlay');
      component.restoreSelection();
      expect(component['toggleLoadingOverlay']).toHaveBeenCalledWith({overlay: true, spinner: false});
      expect(pubsub.publish).toHaveBeenCalled();
    });

    it('noRestoreSelection', () => {
      quickbetService.getRestoredSelection.and.returnValue(false);

      spyOn(component, 'toggleLoadingOverlay');
      component.restoreSelection();
      expect(component['toggleLoadingOverlay']).not.toHaveBeenCalled();
      expect(pubsub.publish).not.toHaveBeenCalled();
    });
  });

  it('get custom error description', () => {
    locale.getString.and.returnValue('str');
    expect(component.getErrorDescription('smth')).toBe('str');
  });

  it('get custom error description with negative case', () => {
    locale.getString = jasmine.createSpy();
    component.getErrorDescription(null);
    expect(locale.getString).toHaveBeenCalledWith('quickbet.SERVER_ERROR');
  });

  describe('toggleLoadingOverlay', () => {
    it('should call last pubsub method', () => {
      component.toggleLoadingOverlay({});
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.TOGGLE_LOADING_OVERLAY, {});
    });

    it('should open popup if state overlay exist', () => {
      component.toggleLoadingOverlay({overlay: {}});
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith('QuickBet');
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.TOGGLE_LOADING_OVERLAY, {
        overlay: {}
      });
    });

    it('should call onClosePopup method', () => {
      component.toggleLoadingOverlay({});
      expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('QuickBet', {});
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.TOGGLE_LOADING_OVERLAY, {});
    });

    it('should update loading state of selection to falsy value', () => {
      component['loadingSelection'] = true;
      component['toggleLoadingOverlay'](null);

      expect(component['loadingSelection']).toBeFalsy();
    });

    it('should update loading state of selection to truthy value', () => {
      component['loadingSelection'] = false;
      component['toggleLoadingOverlay']({ spinner: true });

      expect(component['loadingSelection']).toBeTruthy();
    });
  });

  describe('addSelection', () => {
    beforeEach(() => {
      component['removeSubscribers'] = jasmine.createSpy();
      component['placeBetListener'] = jasmine.createSpy();
      component['toggleLoadingOverlay'] = jasmine.createSpy();
      component['checkArcUser'] = jasmine.createSpy();
      component.selection = {
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: { betData: { dimension94: 1 }},
      } as any;
    });

    it('handle observable error', fakeAsync(() => {
      quickbetService.addSelection.and.returnValue(throwError('error'));
      component['addSelectionErrorHandler'] = jasmine.createSpy();
      component.addSelection({} as any);
      tick();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(component['placeBetListener']).toHaveBeenCalled();
      expect(component['addSelectionErrorHandler']).toHaveBeenCalledWith('error', {});
      expect(component['toggleLoadingOverlay']).toHaveBeenCalledWith({spinner: false, overlay: true});
    }));

    it('should call subscription when are errors', fakeAsync(() => {
      const obsResponse = {data: {error: 'some error'}};
      quickbetService.addSelection.and.returnValue(of(obsResponse));
      component['addSelectionErrorHandler'] = jasmine.createSpy();
      component.addSelection({} as any);
      tick();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(component['placeBetListener']).toHaveBeenCalled();
      expect(component['addSelectionErrorHandler']).toHaveBeenCalledWith(obsResponse, {});
    }));

    it('should call subscription when selection is fanzone selection', fakeAsync(() => {
      const obsResponse = { markets: [{
        "drilldownTagNames":"MKTFLAG_FZ",
        children:[]
      }]};
      quickbetService.addSelection.and.returnValue(of(obsResponse));
      component['addSelectionErrorHandler'] = jasmine.createSpy();
      component.addSelection({} as any);
      tick();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(component['placeBetListener']).toHaveBeenCalled();
      expect(component['addSelectionErrorHandler']).toHaveBeenCalledWith(obsResponse, {});
    }));

    it('should call subscription when no errors', fakeAsync(() => {
      const reqData = { isOutright: true } as any;
      quickbetService.addSelection.and.returnValue(of({}));
      component['trackAddBetToQB'] = jasmine.createSpy();
      component.addSelection({} as any);
      tick();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(component['placeBetListener']).toHaveBeenCalled();
      expect(component.selectionData).toEqual(reqData);
      expect(component['trackAddBetToQB']).toHaveBeenCalledWith(reqData);
    }));

    it('should call subscription when no errors and selectionData present for restore', fakeAsync(() => {
      component.selectionData = {
        freebet: {
          name: 'freebet',
          freebetValue: '0.5'
        },
        isOutright: true
      } as any;
      quickbetService.addSelection.and.returnValue(of({}));
      component['trackAddBetToQB'] = jasmine.createSpy();
      component.addSelection({} as any);
      tick();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(component['placeBetListener']).toHaveBeenCalled();
      expect(component.selectionData).toEqual({
        freebet: {
          name: 'freebet',
          freebetValue: '0.5'
        },
        isOutright: true
      });
      expect(component['trackAddBetToQB']).toHaveBeenCalledWith({
        freebet: {
          name: 'freebet',
          freebetValue: '0.5'
        },
        isOutright: true
      });
    }));

    it('should call luckydip', fakeAsync(() => {
      component.isLuckyDip = true;
      component.selection = {
        selectionInfo:  {
          potentialOdds: '1',
          eventName: 'event',
          outcomeName: 'outcomeName',
          newOdds: 'newOdds',
        },
        outcomes : [{id: '123'}]
      }
      component.selectionData = {
        freebet: {
          name: 'freebet',
          freebetValue: '0.5'
        }
      } as any;
      quickbetService.addSelection.and.returnValue(of({}));
      // component['trackAddBetToQB'] = jasmine.createSpy();
      component.addSelection({} as any);
      tick();
      expect(component.isWSdisabled).toBeFalsy();
    }));

    it('should call luckydip without outcomes', fakeAsync(() => {
      component.isLuckyDip = true;
      component.selection = {
        selectionInfo:  {
          potentialOdds: '1',
          eventName: 'event',
          outcomeName: 'outcomeName',
          newOdds: 'newOdds',
        }
      }
      component.selectionData = {
        freebet: {
          name: 'freebet',
          freebetValue: '0.5'
        }
      } as any;
      quickbetService.addSelection.and.returnValue(of({}));
      component.addSelection({} as any);
      tick();
      expect(component.isWSdisabled).toBeFalsy();
    }));
  });

  it('extendSelectionDataWithError', () => {
    const code = 'code',
      requestData = {},
      status = 'test';

    component['extendSelectionDataWithError'](code, requestData, status);

    expect(component.selectionData.requestData).toBe(requestData);
    expect(component.selectionData.error).toEqual({ code, selectionUndisplayed: status });
  });

  describe('addSelectionErrorHandler', () => {
    it('reset instances where data comes', () => {
      const errorData = {
          data: {
            error: {
              code: 'some_code',
              description: 'quickbet.some_code'
            }
          }
        },
        requestData = {
          additional: {},
          outcomeIds: 2
        };
      component['getErrorDescription'] = jasmine
        .createSpy('getErrorDescription')
        .and.returnValue('quickbet.server_error');
      component['sendEventToGTM'] = jasmine.createSpy();
      component.addSelectionErrorHandler(errorData, requestData);
      expect(component['sendEventToGTM']).toHaveBeenCalledWith({
        eventAction: 'add to betslip',
        eventLabel: 'failure',
        errorMessage: 'quickbet.some_code',
        errorCode: 'some_code'
      });
      expect(component['selectionData']).toEqual({
        error: { code: 'some_code', selectionUndisplayed: 'SERVER_ERROR' }, requestData
      });
    });

    it('reset instances where is no data', () => {
      component['getErrorDescription'] = jasmine
        .createSpy('getErrorDescription')
        .and.returnValue('quickbet.test_code');
      component['sendEventToGTM'] = jasmine.createSpy();
      component.addSelectionErrorHandler({}, {});
      expect(component['sendEventToGTM']).toHaveBeenCalledWith({
        eventAction: 'add to betslip',
        eventLabel: 'failure',
        errorMessage: 'quickbet.test_code',
        errorCode: 'server_error'
      });
      expect(component['selectionData']).toEqual({
        error: { code: 'SERVER_ERROR', selectionUndisplayed: 'SERVER_ERROR' },
        requestData: {}
      });
    });

    it('bet not permitted case', () => {
      const requestData = {},
        code = 'SERVER_ERROR';
      component['extendSelectionDataWithError'] = jasmine.createSpy();
      quickbetService.isBetNotPermittedError.and.returnValue(true);
      component.addSelectionErrorHandler({
        data: {
          error: { description: 'err' }
        }
      }, {});
      expect(component['extendSelectionDataWithError']).toHaveBeenCalledWith(code, requestData, 'BET_NOT_PERMITTED');
    });

    it('error handling when error code "UNAUTHORIZED_ACCESS" only first time', fakeAsync(() => {
      const errorData = {
        data: {
          error: {
            code: 'UNAUTHORIZED_ACCESS',
            description: 'description'
          }
        }
      };
      const extendSelectionDataWithErrorSpy = spyOn(component, 'extendSelectionDataWithError');
      const sendEventToGTMSpy = spyOn(component, 'sendEventToGTM');
      const addSelectionSpy = spyOn(component, 'addSelection');

      component.addSelectionErrorHandler(errorData, {});
      tick(100);

      expect(awsService.addAction).toHaveBeenCalledTimes(3);
      expect(command.executeAsync).toHaveBeenCalledWith('auth/bppAuthSequence');
      expect(component['addSelection']).toHaveBeenCalledWith({
        token: 'bppToken'
      });
      expect(component.extendSelectionDataWithError).not.toHaveBeenCalled();

      sendEventToGTMSpy.calls.reset();
      addSelectionSpy.calls.reset();
      extendSelectionDataWithErrorSpy.calls.reset();
      awsService.addAction.calls.reset();

      component.addSelectionErrorHandler(errorData, {});
      tick(100);

      expect(awsService.addAction).toHaveBeenCalledTimes(1);
      expect(command.executeAsync).not.toHaveBeenCalledWith();
      expect(component['addSelection']).not.toHaveBeenCalledWith();
      expect(component.extendSelectionDataWithError).toHaveBeenCalledWith('UNAUTHORIZED_ACCESS', {}, '');
    }));
  });

  describe('formBetslipSelection for selection and GTMObject data', () => {
    
    beforeEach(() => {
      component.selection = {
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: { betData: { dimension94: 1, dimension177: 'No Show'}}
      } as any;
     });

    it('formbetslipselection for selection and GTMObject data', () => {
      component.selectionData = {
        selectionData: { requestData: { outcomeIds: '23' } },
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        isEachWay: true,
        isLP: true,
        hasSP: true,
        GTMObject: {},
        stake: '1',
        selectionType: 'type'
      };
      gtmTrackingService.getTracking.and.returnValue({});
      const formData = component['formBetslipSelection']();
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(quickbetService.isVirtualSport).toHaveBeenCalledWith(component.selectionData.categoryName);
    });
  });

  describe('formBetslipSelection', () => {

    beforeEach(() => {
      component.selection = {
        eventId: 123,
        isOutright: true,
        isSpecial: false        
      } as any;
    });

    it('slip selection without data', () => {
      component.selectionData = {
        eventId: 123
      };
      quickbetService.isVirtualSport.and.returnValue(false);
      expect(component.formBetslipSelection()).toEqual({
        outcomeId: [],
        userEachWay: undefined,
        userStake: undefined,
        type: 'simple',
        price: {priceType: 'SP'},
        isVirtual: false,
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: null
      });
    });

    it('slip selection with incoming data', () => {
      component.selectionData = {
        isLP: true,
        hasSP: true,
        price: {},
        requestData: {outcomeIds: [1]},
        isEachWay: true,
        stake: 'stake',
        selectionType: 'selectionType',
        categoryName: 'categoryName',
        eventId: 123
      };
      gtmTrackingService.getTracking.and.returnValue({});
      quickbetService.isVirtualSport.and.returnValue(true);
      expect(component.formBetslipSelection()).toEqual({
        outcomeId: [1],
        userEachWay: true,
        userStake: 'stake',
        type: 'selectiontype',
        price: {priceType: 'SP'},
        isVirtual: true,
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: {tracking: {}}
      });
    });

    it('slip selection with incoming data negative case', () => {
      component.selectionData = {
        eventId: 123,
        isLP: true,
        hasSP: false,
        price: {},
        requestData: {outcomeIds: [1]},
        isEachWay: true,
        stake: 'stake',
        selectionType: 'selectionType',
        categoryName: 'categoryName'
      };
      gtmTrackingService.getTracking.and.returnValue({});
      quickbetService.isVirtualSport.and.returnValue(true);
      expect(component.formBetslipSelection()).toEqual({
        outcomeId: [1],
        userEachWay: true,
        userStake: 'stake',
        type: 'selectiontype',
        price: {priceType: 'LP'},
        isVirtual: true,
        eventId: 123,
        isOutright: true,
        isSpecial: false,
        GTMObject: {tracking: {}}
      });
    });

    it('@formBetslipSelection', () => {
      component.selectionData = {
        selectionData: {requestData: {outcomeIds: '23'}},
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        isEachWay: true,
        isLP: true,
        hasSP: true,
        GTMObject: {},
        stake: '1',
        selectionType: 'type'
      };

      expect(component['formBetslipSelection']()).toEqual(jasmine.objectContaining({
        userEachWay: component.selectionData.isEachWay,
        userStake: component.selectionData.stake,
        type: component.selectionData.selectionType
      }));
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(quickbetService.isVirtualSport).toHaveBeenCalledWith(component.selectionData.categoryName);
    });

    it('@formBetslipSelection else cases', () => {
      gtmTrackingService.getTracking.and.returnValue({key: 'value'} as any);
      component.selection = null;
      component.selectionData = {
        selectionData: {requestData: {key: '23'}},
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        isEachWay: true,
        isLP: true,
        hasSP: false,
        GTMObject: {},
        stake: '1',
        selectionType: 'type'
      };

      expect(component['formBetslipSelection']()).toEqual(jasmine.objectContaining({
        userEachWay: component.selectionData.isEachWay,
        userStake: component.selectionData.stake,
        type: component.selectionData.selectionType,
        isOutright: undefined,
        isSpecial: undefined,
      }));
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(quickbetService.isVirtualSport).toHaveBeenCalledWith(component.selectionData.categoryName);
    });

    it('should get data from session storage', () => {
      component.selection = null;
      const data = {
        selectionData: {
          eventId: 1,
          isOutright: true,
          isSpecial: false
        }};
      component.selectionData = {
        isLP: true
      };

      sessionStorage.get.and.returnValue(data);

       expect(component['formBetslipSelection']()).toEqual(jasmine.objectContaining({
         eventId: 1,
         isOutright: true,
         isSpecial: false
         }));
    });

    it('should not get data from session storage',  () => {
      component.selection = null;
      sessionStorage.get.and.returnValue(undefined);
      component.selectionData = {
        isLP: true
      };

      expect(component['formBetslipSelection']()).toEqual(jasmine.objectContaining({
        eventId: undefined,
        isOutright: undefined,
        isSpecial: undefined,
      }));

    });

    it('should not get data from session storage',  () => {
      component.selection = null;
      sessionStorage.get.and.returnValue({});
      component.selectionData = {
        isLP: true
      };

      expect(component['formBetslipSelection']()).toEqual(jasmine.objectContaining({
        eventId: undefined,
        isOutright: undefined,
        isSpecial: undefined,
      }));

    });

  });

  describe('trackPlaceBetError', () => {
    it('should create new instance of error object', () => {
      const error = {
        code: '1_1'
      } as any;
      component['sendEventToGTM'] = jasmine.createSpy();
      component.trackPlaceBetError(error, {} as any, '');
      expect(component['sendEventToGTM']).toHaveBeenCalledWith({
        eventLabel: 'failure',
        errorMessage: '',
        errorCode: '1 1'
      });
    });

    it('trackPlaceBetError negative case', () => {
      component.trackPlaceBetError(null, {} as any, '');
      component['sendEventToGTM'] = jasmine.createSpy();
      expect(component['sendEventToGTM']).not.toHaveBeenCalled();
    });
    it('trackPlaceBetError isStreamBet true', () => {
      spyOn(component, 'sendEventToGTM').and.callThrough();
      component.selection.isStreamBet = true;
      component.selectionData = {
        eventName: 'e1',
        outcomeName: 'o1'
      };
      const trackingInfo = {ecommerce: {purchase: {products: [1]}}};
      component.trackPlaceBetError({code: ''}, trackingInfo as any, '');
      expect(component['sendEventToGTM']).toHaveBeenCalled();
    });
  });

  describe('@placeBet', () => {
    it('should not extend track object with stream data', fakeAsync(() => {
      const streamData = {
        streamID: null,
        streamActive: true
      };

      gtmTrackingService.getTracking.and.returnValue(null);
      component.selectionData = {
        isStarted: true,
        categoryName: 'Football',
        GTMObject: {}
      };
      component.trackObj = null;
      location.path.and.returnValue('/page');
      command.executeAsync.and.returnValue(Promise.resolve(streamData));
      component.placeBet();
      tick();

      expect(component.trackObj).toEqual({
        eventAction: 'place bet',
        betType: 'single',
        betCategory: 'football',
        betInPlay: 'yes',
        bonusBet: 'false',
        location: '/page',
        customerBuilt: 'No'
      });
    }));

    it('should extend track object with stream data', fakeAsync(() => {
      const streamData = {
        streamID: '123',
        streamActive: true
      };

      component.selectionData = {
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        GTMObject: {}
      };
      component.trackObj = null;
      location.path.and.returnValue('/page');
      command.executeAsync.and.returnValue(Promise.resolve(streamData));

      component.placeBet();
      tick();

      expect(component.trackObj).toEqual({
        eventAction: 'place bet',
        betType: 'single',
        betCategory: 'football',
        betInPlay: 'no',
        bonusBet: 'true',
        location: '/page',
        customerBuilt: 'Yes',
        streamActive: streamData.streamActive,
        streamID: streamData.streamID
      });
    }));

    it('should extend track object with ecommerce data', fakeAsync(() => {
      const streamData = {
        streamID: '123',
        streamActive: true
      };

      gtmTrackingService.getTracking.and.returnValue(gtmOrigin);
      component.selectionData = {
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2
      };
      component.trackObj = null;
      location.path.and.returnValue('/page');
      command.executeAsync.and.returnValue(Promise.resolve(streamData));

      component.placeBet();
      tick();

      expect(component.trackObj).toEqual({
        eventAction: 'place bet',
        ecommerce: {
          purchase: {
            actionField: {},
            products: [{
              dimension64: gtmOrigin.location,
              dimension65: gtmOrigin.module
            }]
          }
        },
        streamActive: streamData.streamActive,
        streamID: streamData.streamID
      });
    }));
    it('should extend track object with ecommerce and racingpost data', fakeAsync(() => {
      const streamData = {
        streamID: '123',
        streamActive: true
      };

      gtmTrackingService.getTracking.and.returnValue(gtmOrigin);
      component.selectionData = {
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2
      };
      component.trackObj = null;
      location.path.and.returnValue('/page');
      racingPostTipService.racingPostGTM = {
        location: 'Bet Receipt',
        module: 'RP Tip',
        dimension86: 0,
        dimension87: 0,
        dimension88: null
      };
      command.executeAsync.and.returnValue(Promise.resolve(streamData));

      component.placeBet();
      tick();

      expect(component.trackObj).toEqual({
        eventAction: 'place bet',
        ecommerce: {
          purchase: {
            actionField: {},
            products: [{
              dimension64: gtmOrigin.location,
              dimension65: gtmOrigin.module
            }]
          }
        },
        streamActive: streamData.streamActive,
        streamID: streamData.streamID
      });
    }));

    it('should subscribe to placeBetListener when err has occurred during bet placement', fakeAsync(() => {
      spyOn(component, 'placeBetListener');
      component.betIsPlaced = true;
      component.selectionData = {
        isStarted: true,
        categoryName: 'Football'
      };
      component.trackObj = null;
      command.executeAsync.and.returnValue(Promise.resolve([]));

      component.placeBet();
      tick();
      expect(component.placeBetListener).toHaveBeenCalled();
      expect(component.betIsPlaced).toBe(false);
    }));

    it('should not subscribe to placeBetListener when err has occurred during bet placement', fakeAsync(() => {
      spyOn(component, 'placeBetListener');
      component.betIsPlaced = false;
      component.selectionData = {
        isStarted: true,
        categoryName: 'Football',
        GTMObject: {}
      };
      component.trackObj = null;
      command.executeAsync.and.returnValue(Promise.resolve([]));

      component.placeBet();
      tick();
      expect(component.placeBetListener).not.toHaveBeenCalled();
    }));
    it('should  subscribe to placeBetListener with dynamicGtmObj', fakeAsync(() => {
      spyOn(component, 'placeBetListener');
      component.betIsPlaced = false;
      component.selectionData = {
        isStarted: true,
        categoryName: 'Football',
        GTMObject: {}
      };
      component.trackObj = null;
      command.executeAsync.and.returnValue(Promise.resolve([]));
      component.quickbetService.dynamicGtmObj='test';
      component.placeBet();
      tick();
      expect(component.placeBetListener).not.toHaveBeenCalled();
    }));
    it('should  subscribe to placeBetListener with dynamicGtmObj else case', fakeAsync(() => {
      spyOn(component, 'placeBetListener');
      component.betIsPlaced = false;
      component.selectionData = {
        isStarted: true,
        categoryName: 'Football',
        GTMObject: {}
      };
      component.trackObj = null;
      command.executeAsync.and.returnValue(Promise.resolve([]));
      component.quickbetService.dynamicGtmObj='test';
      component.gtmTrackingService={
        getTracking:jasmine.createSpy('getTracking').and.returnValue({location:'window',
        module: 'surface bets'})};
      component.placeBet();
      tick();
      expect(component.placeBetListener).not.toHaveBeenCalled();
    }));
  });

  it('isPlaceBetSubscribetExist', () => {
    component.quickbetPlaceBetSubscriber = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    component.isPlaceBetSubscribetExist();
    expect(component.quickbetPlaceBetSubscriber.unsubscribe).toHaveBeenCalled();
  });

  describe('placeBetListener', () => {
    it('unsubscribe if subscription exists', () => {
      component.isPlaceBetSubscribetExist = jasmine.createSpy();
      component.placeBetListener();
      expect(component.isPlaceBetSubscribetExist).toHaveBeenCalled();
    });

    it('subscription error without error obj', fakeAsync(() => {
      component.trackPlaceBetError = jasmine.createSpy().and.returnValue({});
      component.removeSubscribers = jasmine.createSpy();
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(throwError({} as any));
      quickbetDataProviderService.quickbetPlaceBetListener.error({} as any);
      component.placeBetListener();
      tick();
      expect(component.removeSubscribers).toHaveBeenCalled();
    }));

    it('success case', fakeAsync(() => {
      component['removeSubscribers'] = jasmine.createSpy();
      component['trackPlaceBetSuccess'] = jasmine.createSpy();
      component.selectionData = {};
      component.selection = null;
      component.isLuckyDip = false;
      const receiptDetailsModel = {receipt: {}, bet: {isquickbet: false}};
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      component.placeBetListener();
      tick();
      quickbetDataProviderService.quickbetPlaceBetListener.next([{}]);
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubsub.API.BET_PLACED, BETSLIP.QUICKBET);
      expect(pubsub.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET');
      tick();
      expect(pubsub.publish).not.toHaveBeenCalledWith('STORE_FREEBETS');
      expect(pubsub.publish).toHaveBeenCalledWith('PRIVATE_MARKETS_TAB');
      expect(component['quickbetNotificationService'].clear).toHaveBeenCalled();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(component['trackPlaceBetSuccess']).toHaveBeenCalled();
    }));

    it('success case if luckydip market', fakeAsync(() => {
      component['removeSubscribers'] = jasmine.createSpy();
      component['trackPlaceBetSuccess'] = jasmine.createSpy();
      component.selectionData = {};
      component.selection = null;
      component.isLuckyDip = true;
      const receiptDetailsModel = {receipt: {}, bet: {isquickbet: false}};
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      component.placeBetListener();
      tick();
      quickbetDataProviderService.quickbetPlaceBetListener.next([{}]);
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubsub.API.BET_PLACED, BETSLIP.QUICKBET);
      expect(pubsub.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET');
      tick();
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubsub.API.MY_BET_PLACED_LD, { isquickbet: true });
    }));

    it('success case, should store freebets if BIR is true', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: true,
        bet: {isquickbet: false}
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      component['trackPlaceBetSuccess'] = jasmine.createSpy('trackPlaceBetSuccess');
      component.selectionData = {};
      component.selection = null;

      component.placeBetListener();
      tick();
      quickbetDataProviderService.quickbetPlaceBetListener.next([{}]);

      expect(pubsub.publish).toHaveBeenCalledWith('STORE_FREEBETS');
    }));

    it('success case, should store freebets if BIR is false and there are claimed offers', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        claimedOffers: [{ status: 'claimed' }],
        bet: {isquickbet: false}
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      component['trackPlaceBetSuccess'] = jasmine.createSpy('trackPlaceBetSuccess');
      component.selectionData = {};
      component.selection = null;

      component.placeBetListener();
      tick();
      quickbetDataProviderService.quickbetPlaceBetListener.next([{}]);

      expect(pubsub.publish).toHaveBeenCalledWith('STORE_FREEBETS');
    }));

    it('failed case, should NOT store freebets if BIR is false and there are NO claimed offers', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false}
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      component['trackPlaceBetSuccess'] = jasmine.createSpy('trackPlaceBetSuccess');
      component.selectionData = {};
      component.selection = null;

      component.placeBetListener();
      tick();
      quickbetDataProviderService.quickbetPlaceBetListener.next([{}]);

      expect(pubsub.publish).not.toHaveBeenCalledWith('STORE_FREEBETS');
      flush();
    }));

    it('should set skipOnRecconect after bet placed', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false},
        receipt: {id: '1'}
      };
      component.selectionData = {
        eventId: 123
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));

    it('should call local strg when event it matched', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false},
        receipt: {id: '1'}
      };
      component.selectionData = {
        eventId: 11
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      storageService.get = jasmine.createSpy().and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));

    it('should call local strg when event id and bet id Matched', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false,id: 3},
        receipt: {id: '1'}
      };
      component.selectionData = {
        eventId: 11
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      storageService.get = jasmine.createSpy().and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));

    it('should call local strg when freebetId', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false,id: 3},
        receipt: {id: '1'},
        freebetId: 12
      };
      component.selectionData = {
        eventId: 11
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      storageService.get = (key) => {
        if(key === 'toteFreeBets') {
          return [
            {freebetTokenId: 12}
          ]
        } else {
          return [
            {freebetTokenId: 12}
          ]
          }
      };
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));

    it('should call if local storage does not exist', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false},
        receipt: {id: '1'}
      };
      component.selectionData = {
        eventId: 123
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      storageService.get = jasmine.createSpy().and.returnValue(false);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));
    it('should call if local storage when data is null', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false},
        receipt: {id: '1'}
      };
      component.selectionData = {
        eventId: 11
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      storageService.get = jasmine.createSpy().and.returnValue(null);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));

    it('should call if local storage when data is empty', fakeAsync(() => {
      const receiptDetailsModel = {
        isBir: false,
        bet: {isquickbet: false},
        receipt: {id: '1'}
      };
      component.selectionData = {
        eventId: 11
      };
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      quickbetService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of([receiptDetailsModel]));
      
      quickbetDataProviderService.quickbetPlaceBetListener = of(null);
      storageService.get = jasmine.createSpy().and.returnValue([]);
      component.selection = {};
      component['trackObj'] = {};
      component.placeBetListener();
      tick(2000);
      expect(component.selection.skipOnReconnect).toBeTruthy();
    }));

    it('error ODDS_BOOST_PRICE_INVALID', fakeAsync(() => {
      component['trackPlaceBetError'] = jasmine.createSpy();
      component.selectionData = {};
      component.reuseSelection = jasmine.createSpy();
      quickbetDataProviderService.quickbetPlaceBetListener.error({
        subErrorCode: 'ODDS_BOOST_PRICE_INVALID'
      });
      component.placeBetListener();
      tick();
      expect(component.betIsPlaced).toBeTruthy();
      expect(quickbetService.activateReboost).toHaveBeenCalled();
    }));

    it('error ODDS_BOOST_PRICE_INVALID negative case', fakeAsync(() => {
      component['trackPlaceBetError'] = jasmine.createSpy();
      component.selectionData = {};
      component.reuseSelection = jasmine.createSpy();
      quickbetDataProviderService.quickbetPlaceBetListener.error({
        subErrorCode: null
      });
      component.placeBetListener();
      tick();
      expect(quickbetService.activateReboost).not.toHaveBeenCalled();
    }));

    it('error UNHANDLED', fakeAsync(() => {
      component.selectionData = {};
      component.trackPlaceBetError = jasmine.createSpy();
      quickbetDataProviderService.quickbetPlaceBetListener.error({
        subErrorCode: 'ANY',
        code: 'ANY'
      });

      component.placeBetListener();
      tick();

      expect(component.betIsPlaced).toBeTruthy();
      expect(quickbetService.getBetPlacementErrorMessage).toHaveBeenCalled();
      expect(quickbetDataProviderService.quickbetReceiptListener.next).toHaveBeenCalled();
    }));

    it('error OVERASK', fakeAsync(() => {
      component['trackPlaceBetError'] = jasmine.createSpy();
      component.selectionData = {};
      quickbetDataProviderService.quickbetPlaceBetListener.error({
        code: 'OVERASK'
      });

      component.placeBetListener();
      tick();

      expect(component.betIsPlaced).toBeTruthy();
      expect(quickbetService.activateReboost).not.toHaveBeenCalled();
    }));

    it('error 4016', fakeAsync(() => {
      component['trackPlaceBetError'] = jasmine.createSpy();
      component.selectionData = {};
      quickbetDataProviderService.quickbetPlaceBetListener.error({
        code: '4016'
      });

      component.placeBetListener();
      tick();

      expect(component.betIsPlaced).toBeTruthy();
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SHOW_LOCATION_RESTRICTED_BETS_DIALOG);
    }));

    it('error STAKE_TOO_LOW', fakeAsync(() => {
      component.selectionData = {};
      component.trackPlaceBetError = jasmine.createSpy();
      component['removeSubscribers'] = jasmine.createSpy();
      quickbetDataProviderService.quickbetPlaceBetListener.error({
        error: '',
        subErrorCode: 'STAKE_TOO_LOW',
        code: 'TEST'
      });

      component.placeBetListener();
      tick();

      expect(component.betIsPlaced).toBeTruthy();
      expect(component['removeSubscribers']).toHaveBeenCalled();
      expect(quickbetService.getBetPlacementErrorMessage).toHaveBeenCalled();
      expect(quickbetDataProviderService.quickbetReceiptListener.next).toHaveBeenCalledWith([{error: '', errorCode: 'STAKE_TOO_LOW'}]);
    }));
  });

  describe('trackAddBetToQB', () => {
    it('toBetslip arg, live, byb, boost active, streamed', fakeAsync(() => {
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'betslip'
      });
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamID: '12',
        streamActive: true
      }));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      };

      component['trackAddBetToQB'](eventData, true);
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '1',
              variant: '11',
              brand: 'mname',
              metric1: 3,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 1,
              dimension63: 1,
              dimension64: '/',
              dimension65: 'betslip',
              dimension86: 1,
              dimension87: 1,
              dimension88: '12',
              dimension166: 'normal',
              dimension180: 'normal'
            }]
          }
        }
      });
    }));

    it('toBetslip arg, live, byb, boost active, streamed - stream and bet true', fakeAsync(() => {
      component.selection.isStreamBet = true;
      component.categoryName = 'test';
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'betslip'
      });
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamID: '12',
        streamActive: true
      }));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3',
        outcomeName: 'outcome name',
        categoryName: 'test'
      };

      component['trackAddBetToQB'](eventData, true);
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name - outcome name',
              category: '1',
              variant: '11',
              brand: 'mname',
              metric1: 3,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 1,
              dimension63: 1,
              dimension64: 'test',
              dimension65: 'stream and bet',
              dimension86: 1,
              dimension87: 1,
              dimension88: '12',
              dimension166: 'normal',
              dimension180: 'normal'
            }]
          }
        }
      });
    }));

    it('toBetslip arg, live, byb, boost active, for virtuals', fakeAsync(() => {
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'next races'
      });
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamID: '12',
        streamActive: true
      }));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 39,
        freebetValue: '3'
      };

      component['trackAddBetToQB'](eventData, true);
      component.stakeFromQb = 1;
      component.digitKeyBoardStatus = false;
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '39',
              variant: '11',
              brand: 'mname',
              metric1: 3,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 1,
              dimension63: 1,
              dimension64: '/',
              dimension65: 'next races',
              dimension86: 1,
              dimension87: 1,
              dimension88: '12',
              dimension166: 'normal',
              dimension180: 'virtual',
              dimension181: 'predefined stake'
            }]
          }
        }
      });
    }));

    it('toBetslip arg, live, byb, boost active, for virtuals', fakeAsync(() => {
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'next races'
      });
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamID: '12',
        streamActive: true
      }));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 39,
        freebetValue: '3'
      };

      component['trackAddBetToQB'](eventData, true);
      component.stakeFromQb = 2;
      component.digitKeyBoardStatus = true;
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '39',
              variant: '11',
              brand: 'mname',
              metric1: 3,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 1,
              dimension63: 1,
              dimension64: '/',
              dimension65: 'next races',
              dimension86: 1,
              dimension87: 1,
              dimension88: '12',
              dimension166: 'normal',
              dimension180: 'virtual',
              dimension181: 'keypad predefined stake'
            }]
          }
        }
      });
    }));

    it('toQuickbet arg, not live, not byb, not boost active, not streamed', fakeAsync(() => {
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'quickbet'
      });
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {}));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '4'
      };

      component['trackAddBetToQB'](eventData);
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to quickbet',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '1',
              variant: '11',
              brand: 'mname',
              metric1: 4,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 0,
              dimension63: 0,
              dimension64: '/',
              dimension65: 'quickbet',
              dimension86: 0,
              dimension87: 0,
              dimension88: null,
              dimension166: 'normal',
              dimension180: 'normal'
            }]
          }
        }
      });
    }));

    it('toQuickbet add dimension94 if module is surface bets', fakeAsync(() => {
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'surface bets'
      });
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {}));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '4'
      };
      component.selection = {GTMObject: {betData:{dimension94:1, dimension177: 'No Show'}}}
      component['trackAddBetToQB'](eventData);
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to quickbet',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '1',
              variant: '11',
              brand: 'mname',
              metric1: 4,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 0,
              dimension63: 0,
              dimension64: '/',
              dimension65: 'surface bets',
              dimension86: 0,
              dimension87: 0,
              dimension88: null,
              dimension94:1,
              dimension177: 'No Show',
              dimension166: 'normal',
              dimension180: 'normal'
            }]
          }
        }
      });
    }));

    it('no gtmObject', fakeAsync(() => {
      gtmTrackingService.getTracking.and.returnValue(null);
      const eventData = {};
      const streamData = {};
      command.executeAsync.and.returnValue(Promise.resolve(streamData));

      component['trackAddBetToQB'](eventData, true);
      tick();

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              dimension86: 0, 
              dimension87: 0, 
              dimension88: null, 
              quantity: 1, 
              name: 'name', 
              category: 16, 
              variant: 1935, 
              brand: 'Match Betting', 
              dimension60: '60', 
              dimension61: '61', 
              dimension62: '62', 
              dimension63: 0, 
              dimension64: '64', 
              dimension65: 'edp', 
              dimension66: 1, 
              dimension67: 81, 
              dimension180: 'scorecast;teamname;playerName;24',
              metric1: 0
            }]
          }
        }
      });
    }));

    it('It should get the tracking', fakeAsync(() => {
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      };
      component['trackAddBetToQB'](eventData, true);
      tick();
      gtmTrackingService.getTracking.and.returnValue(gtmOrigin);
      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'quickbet'
      });
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
    }));

    it('It should call dynamicGtmObj', fakeAsync(() => {
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      };

      const dummyObj = {
        location: '/',
        module: 'quickbet'
      }

      component['trackAddBetToQB'](eventData, true);
      tick();
      expect(gtmTrackingService.dynamicGtmObj).toBe(undefined);
    }));

    it('has tracking obj and It should call dynamicGtmObj', fakeAsync(() => {
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      };

      gtmTrackingService.getTracking.and.returnValue({
        location: '/',
        module: 'surface bets'
      });

      quickbetService.dynamicGtmObj = {
        location: '/',
        module: 'quickbet'
      }

      component['trackAddBetToQB'](eventData, true);
      tick();
      expect(quickbetService.dynamicGtmObj).toBeTruthy();
    }));

    it('tracking obj is undefined and It should call dynamicGtmObj', fakeAsync(() => {
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      };

      gtmTrackingService.getTracking.and.returnValue(undefined);

      quickbetService.dynamicGtmObj = {
        location: '/',
        module: 'quickbet'
      }

      component['trackAddBetToQB'](eventData, true);
      tick();
      expect(quickbetService.dynamicGtmObj).toBeTruthy();
    }));
   });

  it('reuseSelection should restore gtmTracking for selection', fakeAsync(() => {
    spyOn<any>(component, 'addSelection');
    component.reuseSelection({} as any);
    tick();
    expect(gtmTrackingService.getTracking).toHaveBeenCalled();
  }));

  describe('trackPlaceBetSuccess should track ecommerce:', () => {
    let price;
    let selectionData;
    let receipt;
    let trackingInfo;

    beforeEach(() => {
      price = {
        id: '10001',
        priceDec: '1',
        priceDen: '4',
        priceNum: '5'
      };

      receipt = {
        receipt: {
          id: '999999'
        },
        legParts: [{outcomeId: 1}, {outcomeId: 4}],
        price
      };

      selectionData = {
        categoryId: '555',
        typeId: '666',
        marketName: 'Market Name',
        eventId: '777',
        outcomeId: '888',
        isStarted: true,
        isYourCallBet: true,
        stake: '5',
        freebetValue: 15,
        GTMObject: {}
      } as any;

      trackingInfo = {
        ecommerce: {
          purchase: {
            actionField: {},
            products: [{}]
          }
        }
      };
    });

    it('negative case', () => {
      component['trackPlaceBetSuccess'](null, null);
      expect(quickbetService.getOdds).not.toHaveBeenCalled();
    });

    it('number odds value with stake / bonus / isYourCallBet / isStarted / boosted / streamed', fakeAsync(() => {
      quickbetService.getOdds.and.returnValue('4.20');
      command.executeAsync.and.returnValue(Promise.resolve({
        streamActive: true,
        streamID: '12'
      }));
      component.selectionData = selectionData;
      const selections = {...component.selection};
      component.selection = {selections, ...{GTMObject: {betData:{dimension94:1}}} };
      receipt.bet={id:1102103};
      receipt.oddsBoost = true;
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      component['trackPlaceBetSuccess']([receipt], trackingInfo);
      component.stakeFromQb = 1;
      component.digitKeyBoardStatus = true;
      tick(2000);

      expect(quickbetService.getOdds).toHaveBeenCalledWith(receipt.price, 'dec');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        ecommerce: {
          purchase: {
            actionField: {
              id: receipt.receipt.id,
              revenue: 20
            },
            products: [{
              name: 'single',
              id: '999999',
              price: 20,
              category: '555',
              variant: '666',
              brand: 'Market Name',
              dimension60: '777',
              dimension61: '888',
              dimension62: 1,
              dimension63: 1,
              dimension66: 2,
              dimension67: 4.2,
              dimension86: 1,
              dimension87: 1,
              dimension88: '12',
              dimension90: 1102103,
              dimension94:1,
              metric1: 15,
              dimension166: 'normal',
              dimension180: 'normal',
              dimension181: 'predefined stake'
            }]
          }
        },
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'quickbet'
      });
    }));

    it('number odds value with stake / bonus / isYourCallBet / isStarted / boosted / streamed -  stream and bet', fakeAsync(() => {
      quickbetService.getOdds.and.returnValue('4.20');
      command.executeAsync.and.returnValue(Promise.resolve({
        streamActive: true,
        streamID: '12'
      }));
      component.categoryName = 'test';
      component.selectionData = {...selectionData, isStreamBet: true, eventName: 'event Name', outcomeName: 'outcome Name'};
      const selections = {...component.selection};
      component.selection = {selections, ...{GTMObject: {betData:{dimension94:1}}}, isStreamBet: true, eventName: 'event Name', outcomeName: 'outcome Name' };
      receipt.bet={id:1102103};
      receipt.oddsBoost = true;
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      component['trackPlaceBetSuccess']([receipt], trackingInfo);
      tick(2000);

      expect(quickbetService.getOdds).toHaveBeenCalledWith(receipt.price, 'dec');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent', eventCategory: 'quickbet',
        ecommerce: {
          purchase: {
            actionField: { id: '999999', revenue: 20 },
            products: [
              {
                name: 'event Name - outcome Name', id: '999999', price: 20, category: '555', variant: '666',
                brand: 'Market Name', dimension60: '777', dimension61: '888', dimension62: 1, dimension63:
                  1, dimension66: 2, dimension67: 4.2, dimension86: 1, dimension87: 1, dimension88: '12',
                  dimension166: 'normal', dimension180: 'normal', metric1: 15, dimension65: 'stream and bet', dimension90: 1102103,
                dimension94: 1, dimension64: 'test'
              }]
          }
        }, eventLabel: 'success'
      });
    }));

    it('SP odds value with !stake / !bonus / !isYourCallBet / !isStarted / !numLegs/ !boost / !stream', fakeAsync(() => {
      quickbetService.getOdds.and.returnValue('SP');
      command.executeAsync.and.returnValue(Promise.resolve({}));
      selectionData.stake = null;
      selectionData.freebetValue = null;
      selectionData.isStarted = false;
      selectionData.isYourCallBet = false;
      component.selectionData = selectionData;
      receipt.legParts = [];
      const selections = {...component.selection};
      component.selection = {selections, ...{GTMObject: {betData:{dimension94:1}}} };
      receipt.bet={id:1102103};
      component.stakeFromQb = 2;
      component.digitKeyBoardStatus = false;
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      component['trackPlaceBetSuccess']([receipt], trackingInfo);
      tick(2000);

      expect(quickbetService.getOdds).toHaveBeenCalledWith(receipt.price, 'dec');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        ecommerce: {
          purchase: {
            actionField: {
              id: receipt.receipt.id,
              revenue: 0
            },
            products: [{
              name: 'single',
              id: '999999',
              price: 0,
              category: '555',
              variant: '666',
              brand: 'Market Name',
              dimension60: '777',
              dimension61: '888',
              dimension62: 0,
              dimension63: 0,
              dimension66: 0,
              dimension67: 'SP',
              dimension86: 0,
              dimension87: 0,
              dimension88: null,
              dimension90: 1102103,
              dimension94:1,
              metric1: 0,
              dimension166: 'normal',
              dimension180: 'normal',
              dimension181: 'keypad predefined stake'
            }]
          }
        },
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'quickbet'
      });
    }));

    it('SP odds value with !stake / !bonus / !isYourCallBet / !isStarted / !numLegs/ !boost / !stream', fakeAsync(() => {
      quickbetService.getOdds.and.returnValue('SP');
      command.executeAsync.and.returnValue(Promise.resolve({}));
      selectionData.stake = null;
      selectionData.freebetValue = null;
      selectionData.isStarted = false;
      selectionData.isYourCallBet = false;
      selectionData.categoryId = '39'
      component.selectionData = selectionData;
      receipt.legParts = [];
      const selections = {...component.selection};
      component.selection = {selections, ...{GTMObject: {betData:{dimension94:1}}} };
      receipt.bet={id:1102103};
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      component['trackPlaceBetSuccess']([receipt], trackingInfo);
      tick(2000);

      expect(quickbetService.getOdds).toHaveBeenCalledWith(receipt.price, 'dec');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        ecommerce: {
          purchase: {
            actionField: {
              id: receipt.receipt.id,
              revenue: 0
            },
            products: [{
              name: 'single',
              id: '999999',
              price: 0,
              category: '39',
              variant: '666',
              brand: 'Market Name',
              dimension60: '777',
              dimension61: '888',
              dimension62: 0,
              dimension63: 0,
              dimension66: 0,
              dimension67: 'SP',
              dimension86: 0,
              dimension87: 0,
              dimension88: null,
              dimension90: 1102103,
              dimension94:1,
              metric1: 0,
              dimension166: 'normal',
              dimension180: 'virtual'
            }]
          }
        },
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'quickbet'
      });
    }));

    it('trackPlaceBetSucces without receipt', () => {
      receipt = undefined;
      component['trackPlaceBetSuccess']([receipt], trackingInfo);

      expect(gtm.push).not.toHaveBeenCalled();
    });

    it('trackPlaceBetSucces without ecommerce', fakeAsync(() => {
      trackingInfo = {};
      component.scorecastData = {
        eventLocation: 'scorecast'
      };
      component['trackPlaceBetSuccess']([receipt], trackingInfo);
      tick(2000);

      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventLabel: 'success',
        betID: '999999'
      });
    }));
  });

  it('ngOnInit should subscribe on change selection status', () => {
    
    component.ngOnInit();

    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'Quickbet',
      pubSubApi.GET_QUICKBET_SELECTION_STATUS,
      jasmine.any(Function)
    );
  });

  it('ngOnInit should subscribe on quickBetOnOverlayCloseSubj ', () => {
   
    component.selection = {isStreamBet: true} as any;
    const closePanelSpy = spyOn(component, 'closePanel');
    component.ngOnInit();
    quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
    expect(closePanelSpy).toHaveBeenCalled();
  });

  it('ngOnInit should add selection if component initiated with selection', () => {
    component.selection = {
      outcomes: [{
        id: '123'
      }]
    };
   
    component.ngOnInit();

    expect(quickbetService.addSelection).toHaveBeenCalledWith(jasmine.objectContaining({
      outcomeIds: ['123']
    }), null, undefined, false);

  });
  it('ngOnInit LUCKY_DIP_KEYPAD_PRESSED isBetPlaceClicked true ', () => {
    const pubsub:any={
      API:{
          QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD: 'QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD',
          DIGIT_KEYBOARD_KEY_PRESSED: 'DIGIT_KEYBOARD_KEY_PRESSED',
          LUCKY_DIP_KEYPAD_PRESSED:"LUCKY_DIP_KEYPAD_PRESSED"
      },
      subscribe:jasmine.createSpy('pubsub.subscribe')
        .and.callFake((filename: string, eventName: string, callback: Function) => {
      if(eventName === 'LUCKY_DIP_KEYPAD_PRESSED'){
          callback(true)
      }
      else callback()
  })} 
    component = new QuickbetComponent(
      locale,
      pubsub,
      gtm,
      quickbetService,
      remoteBsService,
      quickbetOverAskService,
      command,
      dialogService,
      infoDialogService,
      device,
      nativeBridgeService,
      location,
      quickbetDataProviderService,
      rendererService,
      windowRef,
      gtmTrackingService,
      quickbetDepositService,
      quickbetNotificationService,
      awsService,
      changeDetectorRef,
      userService,
      sessionStorage,
      racingPostTipService,
      arcUserService,
      storageService,
      betslipService,
      scorecastDataService
    );
    component.selection = {isStreamBet: true} as any;
    const closePanelSpy = spyOn(component, 'closePanel');
    const reuseSelection = spyOn(component, 'reuseSelection');

    component.isBetPlaceClicked=true;
    component.ngOnInit();
    quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
    expect(closePanelSpy).toHaveBeenCalled();
  });

  describe('subscribe on change status should', () => {
    const data = ['A', true];
    let selectionData;

    function initComponent(error?, addToBetslipSpec?) {
      quickbetService.selectionData = selectionData;
      !addToBetslipSpec && pubsub.subscribe.and.callFake((a, b, fn) => {
        fn(data[0], data[1]);
      });
      remoteBsService.connect.and.returnValue(error ? throwError('error') : of({}));
      spyOn<any>(component, 'addSelection');
      spyOn<any>(component, 'reuseSelection');
      spyOn<any>(component, 'restoreSelection');
      spyOn<any>(component, 'placeBetListener');
      spyOn<any>(component, 'closePanel');
      component.selectionData = selectionData;
      component.ngOnInit();
    }

    beforeEach(() => {
      selectionData = {
        isStarted: true,
        categoryName: 'Football',
        disabled: false,
        stake: 5,
        setStatus: jasmine.createSpy('setStatus'),
        GTMObject: {}
      } as any;
    });

    it('should remove class from element', () => {
      const testObj = {someAttr: 'tra-ta-ta'};
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(testObj);
      initComponent();
      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(testObj, 'dk-active-input');
    });

    it('invoke add to betslip when is sync', () => {
      pubsub.subscribe = jasmine.createSpy('subscribe').and.callFake((a, b, cb) => {
        b === 'DEVICE_VIEW_TYPE_CHANGED_NEW' && cb && cb('device');
      });
      component.addToBetslip = jasmine.createSpy('addToBetslip');
      initComponent(false, true);
      expect(component.addToBetslip).toHaveBeenCalled();
    });

    

    it('should not invoke add to betslip', () => {
      pubsub.subscribe = jasmine.createSpy('subscribe').and.callFake((a, b, cb) => {
        b === 'DEVICE_VIEW_TYPE_CHANGED_NEW' && cb && cb(component.selectionData = null);
      });
      component.addToBetslip = jasmine.createSpy('addToBetslip');
      initComponent(false, true);
      expect(component.addToBetslip).not.toHaveBeenCalled();
    });

    it('close panel if no selection data', () => {
      selectionData = null;
      initComponent();
      expect(component.closePanel).toHaveBeenCalled();
    });

    it('REMOTE_BS_RECONNECT callback', () => {
      component.addSelectionHandler = jasmine.createSpy('addSelectionHandler');
      component.selection = {
        skipOnReconnect: true
      };
      initComponent();
      expect(component.addSelectionHandler.calls.count()).toBe(2);
    });

    it('pubsub Quickbet should handle error', fakeAsync(() => {
      initComponent(true);
      tick();
      expect(component.selectionData).toEqual({
        error: {code: 'SERVER_ERROR'},
        requestData: undefined
      });
    }));

    it('not trigger setStatus', () => {
      quickbetService.selectionData = null;
      initComponent();

      expect(component.selectionData.setStatus).not.toHaveBeenCalledWith();
    });

    it('trigger setStatus', () => {
      initComponent();

      expect(component.selectionData.setStatus).toHaveBeenCalledWith(data[0], data[1]);
    });

    it('not trigger update', () => {
      selectionData.disabled = true;
      initComponent();

      expect(quickbetDepositService.update).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('trigger update', () => {
      selectionData.disabled = false;
      initComponent();

      expect(quickbetDepositService.update).toHaveBeenCalledWith(component.selectionData.stake);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    
    it('trigger update for qucikbet_digit_status', () => {
      component.digitKeyBoardStatus = true
      selectionData.disabled = false;
      initComponent();

      expect(quickbetDepositService.update).toHaveBeenCalledWith(component.selectionData.stake);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });


    it('not trigger timeout error on reconnect and betplacement', () => {
      component['extendSelectionDataWithError'] = jasmine.createSpy();
      selectionData.disabled = false;
      component.betplacementProcess = true;
      initComponent();
      expect(component['extendSelectionDataWithError'])
        .toHaveBeenCalledWith('SERVER_ERROR', component.selectionData.requestData, 'TIMEOUT_ERROR');

      expect(component['betplacementProcess']).toBeFalsy();
    });

    it('should restoreSelection', () => {
      selectionData.disabled = true;
      component.selection = undefined;
      component.ngOnInit();

      expect(quickbetService.getRestoredSelection).toHaveBeenCalled();
    });
  });

  describe('isPlacedBetBoosted', () => {
    it('should return true if receipt exists', () => {
      expect(component['isPlacedBetBoosted']({oddsBoost: true} as any)).toBe(true);
    });

    it('should return false if receipt not exists', () => {
      expect(component['isPlacedBetBoosted']({} as any)).toBe(false);
    });
  });

  it('ngOnDestroy', () => {
    component['removeSubscribers'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('Quickbet');
    expect(component['removeSubscribers']).toHaveBeenCalled();
  });

  describe('getOriginalPrice', () => {
    it('should return null if selection does not have price', () => {
      expect(component['getOriginalPrice']({})).toBeNull();
    });

    it('should return null if selection has SP price', () => {
      expect(component['getOriginalPrice']({
        price: {
          priceType: 'SP'
        }
      })).toBeNull();
    });

    it('should return extended price if selection has LP price', () => {
      const price = {
        priceType: 'LP',
        priceDen: 2,
        priceNum: 1
      };
      const selection = { price };

      expect(component['getOriginalPrice'](selection)).toEqual(price);
    });
  });

  afterEach(() => {
    component = null;
  });

  it('@trackPlaceBetError', () => {
    const trackingsInfo = {eventID: 'id'} as IGtmEventModel;
    const errorMessage = 'message';
    const error = {code: 'code'} as any;

    component['trackPlaceBetError'](error, trackingsInfo, errorMessage);
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining(
      {eventLabel: 'failure', errorMessage: errorMessage, errorCode: error.code, eventID: 'id'}));
  });

  it('@addSelectionErrorHandler', () => {
    component['extendSelectionDataWithError'] = jasmine.createSpy();
    component.selectionData = {};
    const errorData = {data: {error: {code: 'code', description: 'description'}}};
    const requestData = {};
    component['addSelectionErrorHandler'](errorData, requestData);

    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining(
      {
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'add to betslip',
        eventLabel: 'failure',
        errorMessage: errorData.data.error.description,
        errorCode: errorData.data.error.code
      }
    ));
    expect(component['extendSelectionDataWithError']).toHaveBeenCalled();
  });

  it('@addSelectionErrorHandler bpp reject case', fakeAsync(() => {
    const code = 'UNAUTHORIZED_ACCESS';
    command.executeAsync.and.returnValue(Promise.reject(null));
    component.selectionData = {};
    const errorData = {data: {error: {code, description: 'desc'}}};
    const requestData = {};
    component['addSelectionErrorHandler'](errorData, requestData);

    tick();

    expect(component.selectionData).toEqual({
      error: {
        code,
        selectionUndisplayed: 'SERVER_ERROR'
      },
      requestData
    });
  }));

  it('addSelectionErrorHandler (event undisplayed)', () => {
    const code = 'EVENT_NOT_FOUND';
    component.addSelectionErrorHandler({
      data: {
        error: { code: 'EVENT_NOT_FOUND', description: 'err' }
      }
    }, {});
    const requestData = {};

    expect(component.selectionData).toEqual({
      error: {
        code,
        selectionUndisplayed: 'EVENT_NOT_FOUND'
      },
      requestData
    });
  });

  it('@addSelectionErrorHandler when UNAUTHORIZED_ACCESS', () => {
    component.selectionData = {};
    const errorData = {data: {error: {code: 'UNAUTHORIZED_ACCESS', description: 'description'}}};
    const requestData = {};
    component.userService.bppToken = false;
    component['addSelectionErrorHandler'](errorData, requestData);

    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining(
      {
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'add to betslip',
        eventLabel: 'failure',
        errorMessage: errorData.data.error.description,
        errorCode: errorData.data.error.code.toLowerCase()
      }
    ));
    expect(awsService.addAction).toHaveBeenCalledTimes(2);
  });

  it('@addSelectionErrorHandler else cases', () => {
    component.selectionData = {};
    const errorData = {data: null};
    const requestData = {};
    const testDescription = 'testdescription';
    locale.getString.and.returnValue(testDescription);
    component['addSelectionErrorHandler'](errorData, requestData);

    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining(
      {
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'add to betslip',
        eventLabel: 'failure',
        errorMessage: testDescription,
        errorCode: 'server_error'
      }
    ));
  });

  it('@addSelection', fakeAsync(() => {
    const data = {
      outcomeIds: ['123', '1234']
    } as any;
    const errorData = {data: {error: {code: 'code', description: 'description'}}};

    quickbetService.addSelection.and.returnValue(throwError(errorData));
    component['addSelection'](data);
    tick();

    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining(
      {
        errorMessage: errorData.data.error.description,
        errorCode: errorData.data.error.code
      }
    ));
    expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {spinner: false, overlay: true});
  }));
  describe('toggleLoadingOverlay', () => {
    it('@toggleLoadingOverlay true', fakeAsync(() => {
      component['toggleLoadingOverlay']({overlay: true});
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith('QuickBet');
      expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {overlay: true});
    }));

    it('@toggleLoadingOverlay false', fakeAsync(() => {
      component['toggleLoadingOverlay']({overlay: false});
      expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('QuickBet', {});
      expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {overlay: false});
    }));

    it('@toggleLoadingOverlay false', fakeAsync(() => {
      component['toggleLoadingOverlay']({});
      expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {});
    }));
  });

  it('@getErrorDescription from locale', () => {
    locale.getString.and.returnValue('errorCode');
    expect(component['getErrorDescription']()).toEqual('errorCode');
  });

  it('@restoreSelection ', fakeAsync(() => {
    const selectionData = {
      selectionData: {requestData: {key: '23'}},
      isStarted: false,
      categoryName: 'Football',
      isYourCallBet: true,
      freebetValue: 2,
      isEachWay: true,
      isLP: true,
      hasSP: false,
      GTMObject: {},
      stake: '1',
      selectionType: 'type'
    };

    quickbetService.getRestoredSelection.and.returnValue(selectionData);
    component['restoreSelection']();
    tick();

    expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {overlay: true, spinner: false});
    expect(pubsub.publish).toHaveBeenCalledWith('QUICKBET_OPENED', component.selectionData);
  }));

  it('@restoreSelection ', fakeAsync(() => {
    const selectionData = {
      markets: [{
        "drilldownTagNames":"MKTFLAG_FZ",
        children:[]
      }]
    };
    userService.status = false;

    quickbetService.getRestoredSelection.and.returnValue(selectionData);
    component['restoreSelection']();
    tick();
    expect(sessionStorage.remove).toHaveBeenCalled();
    expect(pubsub.publish).not.toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {overlay: true, spinner: false});
    expect(pubsub.publish).not.toHaveBeenCalledWith('QUICKBET_OPENED', component.selectionData);
  }));

  it('@restoreSelection ', fakeAsync(() => {
    quickbetService.getRestoredSelection.and.returnValue('');
    component['restoreSelection']();
    tick();

    expect(pubsub.publish).not.toHaveBeenCalled();
  }));

  it('@addToBetslip ', fakeAsync(() => {
    component.selection = {} as any;
    component.selectionData = {
      selectionData: {requestData: {key: '23'}},
      disabled: false,
      isStarted: false,
      categoryName: 'Football',
      isYourCallBet: true,
      freebetValue: 2,
      isEachWay: true,
      isLP: true,
      hasSP: false,
      GTMObject: {},
      stake: '1',
      selectionType: 'type'
    };
    device.isOnline.and.returnValue(true);
    component['addToBetslip']();
    tick();

    expect(command.executeAsync).toHaveBeenCalledTimes(2);
    expect(gtmTrackingService.getTracking).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith('QUICKBET_PANEL_CLOSE', true);
  }));

  it('@addToBetslip if OnLine false', fakeAsync(() => {
    component.selection = {} as any;
    device.isOnline.and.returnValue(false);
    component['addToBetslip']();
    tick();

    expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
  }));

  it('@closePanel', () => {
    component['closePanel'](true);

    expect(quickbetService.removeSelection).toHaveBeenCalledWith(null, true);
    expect(quickbetService.removeQBStateFromStorage).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {spinner: false, overlay: false});
    expect(pubsub.publish).toHaveBeenCalledWith('QUICKBET_PANEL_CLOSE', true);
  });

  it('@closePanel with default args', () => {
    component['closePanel']();

    expect(quickbetService.removeSelection).toHaveBeenCalledWith(null, false);
    expect(quickbetService.removeQBStateFromStorage).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith('TOGGLE_LOADING_OVERLAY', {spinner: false, overlay: false});
    expect(pubsub.publish).toHaveBeenCalledWith('QUICKBET_PANEL_CLOSE', false);
  });

  describe('selectionVisible', () => {
    it('should be falsy if selectionData is not available', () => {
      component.selectionData = null;
      expect(component.selectionVisible).toBeFalsy();
    });

    it('should be falsy if selectionData is available and loading in progress', () => {
      component.selectionData = {} as any;
      component['loadingSelection'] = true;
      expect(component.selectionVisible).toBeFalsy();
    });

    it('should be truthy if selectionData is available and loading is not in progress', () => {
      component.selectionData = {} as any;
      component['loadingSelection'] = false;
      expect(component.selectionVisible).toBeTruthy();
    });
  });

  describe('hasClaimedOffers', () => {
    it('should return true if status is claimed', () => {
      const receiptDetails = {
        claimedOffers: [{ status: 'claimed' }],
      };
      expect(component['hasClaimedOffers'](receiptDetails)).toBeTruthy();
    });

    it('should return false if status is NOT claimed', () => {
      const receiptDetails = {
        claimedOffers: [{ status: 'not_claimed_or_what_ever' }],
      };
      expect(component['hasClaimedOffers'](receiptDetails)).toBeFalsy();
    });

    it('should return false if there are NO claimed offers', () => {
      const receiptDetails = {};
      expect(component['hasClaimedOffers'](receiptDetails)).toBeFalsy();
    });
  });
  describe('checkArcUser', () => {
    it('should not allow quickbet', () => {
      arcUserService.quickbet = true;
      spyOn(component,'addToBetslip');
      component['checkArcUser']();
      expect(component.addToBetslip).toHaveBeenCalled();
    })
    it('should allow quickbet', () => {
      arcUserService.quickbet = false;
      component['toggleLoadingOverlay'] = jasmine.createSpy();
      component['checkArcUser']();
      expect(pubsub.publish).toHaveBeenCalled();
      expect(component['toggleLoadingOverlay']).toHaveBeenCalledWith({ spinner: false, overlay: true });
    })
  });

  it('setTagforLd', () => {
    component.isLuckyDip = true;
    component['setTagforLd']('mobile');
    expect(component.tag).toEqual('luckydip');
  });

  it('setTagforLd ,to set  Quickbet if luckyDip is not available', () => {
    component.isLuckyDip = false;
    component['setTagforLd']();
    expect(component.tag).toEqual('Quickbet');
  });
});
