import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

import { InitBetslipService } from './init-betslip.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';

describe('InitBetslipService', () => {
  let service: InitBetslipService;
  let dialogService;
  let windowRef;
  let cmsService;
  let addToBetslipService;
  let overaskService;
  let gtmService;
  let pubsub;
  let command;
  let deviceService;
  let userService;
  let nativeBridgeService;
  let location;
  let toteBetslipService;
  let betslipService;
  let betslipDataService;
  let betslipStorageService;
  let dynamicComponentLoader;
  let addSelectionCallback;
  let infoDialogService;
  let localeService;
  let sessionStorage;
  let arcUserService;
  let eventVideoStreamProviderService;
  let storageService;
  let scorecastDataService

  beforeEach(() => {
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    windowRef = {
      nativeWindow: {
        view: {}
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };
    addToBetslipService = {
      syncProcess: {},
      syncToBetslip: jasmine.createSpy('syncToBetslip').and.returnValue(of(null)),
      addToBetSlip: jasmine.createSpy('addToBetSlip').and.returnValue(of(null)),
      getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(of(null)),
      isAddToBetslipInProcess: jasmine.createSpy('isAddToBetslipInProcess')
    };
    overaskService = {
      showOveraskInProgressNotification: jasmine.createSpy('showOveraskInProgressNotification')
    };
    gtmService = {
      push: jasmine.createSpy(),
      setSBTrackingData: jasmine.createSpy('setSBTrackingData')
    };
    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string | string[], cb: Function) => {
        if (method === 'SELECTION_ADDED') {
          addSelectionCallback = cb;
        }
      }),
      publishSync: jasmine.createSpy('publishSync'),
    };
    command = {
      API: commandApi,
      register: jasmine.createSpy(),
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve({ streamActive: true, streamID: 12 })),
    };
    deviceService = {};
    userService = {
      isInShopUser: jasmine.createSpy('isInShopUser')
    };
    nativeBridgeService = {
      onClosePopup: jasmine.createSpy('onClosePopup'),
      onOpenPopup: jasmine.createSpy('onOpenPopup')
    };
    location = {
      path: jasmine.createSpy().and.returnValue('/')
    };
    toteBetslipService = {
      addToteBet: jasmine.createSpy('addToteBet'),
      isToteBetPresent: jasmine.createSpy().and.returnValue(false)
    };
    betslipService = {
      toggleSelection: jasmine.createSpy('toggleSelection').and.returnValue(of(null)),
      count: jasmine.createSpy('count'),
      betSlipReady: of(null),
      showBetslipLimitationPopup: jasmine.createSpy('bsService.showLimitationsPopup'),
      showLottoBetWithIdExistsPopup: jasmine.createSpy('bsService.showLimitationsPopup')
    };
    betslipDataService = {
      betslipData: { bets: [] },
      containsRegularBets: jasmine.createSpy('containsRegularBets')
    };
    betslipStorageService = {
      getOutcomesIds: jasmine.createSpy('getOutcomesIds')
    };
    storageService = {
      get: jasmine.createSpy('betSelections').and.returnValue([
        {
          isLotto: true, 
          details:{
            selections:'22|23|24',
            draws: [{id: 1}]
          }
        }
      ])
    };
    
    dynamicComponentLoader = {
      loadModule: jasmine.createSpy('loadModule').and.returnValue(Promise.resolve({
        componentFactoryResolver: {
          resolveComponentFactory: () => ({})
        }
      }))
    };

    infoDialogService = {
      openInfoDialog: jasmine.createSpy()
    };
    localeService = {
      getString: jasmine.createSpy()
    };

    sessionStorage = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue('LuckyDip'),
      remove: jasmine.createSpy('remove')
    };
    arcUserService = {
      quickbet: true
    };
    eventVideoStreamProviderService = {
      isStreamAndBet: true
    };
    scorecastDataService = {
      setScorecastData: (data)=> { return data},
      getScorecastData: ()=> { return {
        name: 'name',
        eventLocation: 'scorecast',
        teamname: 'teamname',
        playerName: 'playerName',
        result: '24',
        dimension64: '64',
        dimension60: '60',
        dimension61: '61',
        dimension62: '62'
      }},
    }
    service = new InitBetslipService(
      dialogService,
      windowRef,
      cmsService,
      addToBetslipService,
      overaskService,
      gtmService,
      pubsub,
      command,
      deviceService,
      userService,
      nativeBridgeService,
      location,
      toteBetslipService,
      betslipService,
      betslipDataService,
      betslipStorageService,
      dynamicComponentLoader,
      infoDialogService,
      localeService,
      sessionStorage,
      arcUserService,
      eventVideoStreamProviderService,
      storageService,
      scorecastDataService
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should track add selection events', fakeAsync(() => {
    const selection = {
      params: {
        eventIsLive: true,
        isYourCallBet: true,
        GTMObject: {}
      }
    };

    service.init();
    addSelectionCallback(selection);
    tick();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.any(Object));
  }));

  it('shouldUseQuickBet', () => {
    userService.isInShopUser = () => false;
    userService.quickBetNotification = true;
    deviceService.isMobile = true;
    deviceService.isDesktop = false;
    betslipDataService.betslipData = { bets: [] };
    addToBetslipService.syncProcess = { inProgress: false };

    expect(service['shouldUseQuickBet']({} as any)).toBeTruthy();
    expect(service['shouldUseQuickBet']({ isFCTC: true } as any)).toBeFalsy();
  });

  describe('toggleBetslipSelection', () => {
    it('tote present', () => {
      toteBetslipService.isToteBetPresent.and.returnValue(true);
      service['showBetslipLimitationPopup'] = jasmine.createSpy();
      service['toggleBetslipSelection']({} as any);
      expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalledTimes(1);
    });

    it('toggle selection', fakeAsync(() => {
      windowRef.nativeWindow.view.mobile = true;

      service['toggleBetslipSelection']({
        GTMObject: {
          selectionID: '1'
        }, goToBetslip: true
      } as any);
      tick();

      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledTimes(2);
      expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED', { selectionId: '1' });
      expect(betslipService.count).toHaveBeenCalledTimes(1);
    }));

    it('toggle selection without GTM', fakeAsync(() => {
      service['toggleBetslipSelection']({} as any);
      tick();

      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
      expect(pubsub.publishSync).toHaveBeenCalledTimes(2);
      expect(betslipService.count).toHaveBeenCalledTimes(1);
    }));

    it('toggle error', fakeAsync(() => {
      betslipService.toggleSelection.and.returnValue(throwError(null));
      service['toggleBetslipSelection']({} as any);
      tick();

      betslipService.toggleSelection.and.returnValue(throwError(1));
      service['toggleBetslipSelection']({} as any);
      tick();

      expect(dynamicComponentLoader.loadModule).toHaveBeenCalledTimes(1);
      expect(dialogService.openDialog).toHaveBeenCalledTimes(1);
    }));
  });

  it('bindEvents', () => {
    command.register.and.callFake((p1, cb) => cb());
    pubsub.subscribe.and.callFake((p1, p2, cb) => {
      cb({ params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}, GTMObject: { selectionID:'123'} });
    });

    service['bindEvents']();

    expect(command.register).toHaveBeenCalledTimes(5);
    expect(pubsub.subscribe).toHaveBeenCalledTimes(7);
  });

  describe('#toggleSelection', () => {
    it('toggleSelection if luckyDip', () => {
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      userService.quickBetNotification = {};
      deviceService.isMobile = true;
      deviceService.isDesktop = false;
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(2);
    });
    it('toggleSelection if luckyDip', () => {
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [{id: '123', isDisplayed: true}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      userService.quickBetNotification = {};
      deviceService.isMobile = true;
      deviceService.isDesktop = false;
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(1);
    });
    it('toggleSelection if not luckyDip', () => {
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      userService.quickBetNotification = {};
      deviceService.isMobile = true;
      deviceService.isDesktop = false;
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(2);
    });
    it('when quickBet is blocked', () => {
      service['shouldUseQuickBet'] = jasmine.createSpy().and.returnValue(true);
      service['toggleQuickbetSelection'] = jasmine.createSpy();
      service['isQuickBetBlocked'] = true;
      service['toggleSelection']({GTMObject: { selectionID:'123'}, params: {}, outcomes: [],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any, true);
      expect(service['toggleQuickbetSelection']).not.toHaveBeenCalled();
    });
  });

  describe('addToBetslipListener', () => {
    it('overask in progress', () => {
      overaskService.isInProcess = true;
      service['addToBetslipListener']({outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any);
      expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalledTimes(1);
    });

    it('add tote bet (regular bets present in betslip)', fakeAsync(() => {
      betslipDataService.containsRegularBets.and.returnValue(true);
      service['addToBetslipListener']({ isTote: true, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'} } as any);
      tick();
      expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalled();
    }));

    it('add tote bet (tote bet present in betslip)', fakeAsync(() => {
      toteBetslipService.isToteBetPresent.and.returnValue(true);
      service['addToBetslipListener']({ isTote: true, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'} } as any);
      tick();
      expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalled();
    }));

    it('add tote bet and clear bet builder', () => {
      storageService.get.and.returnValue(false);
      service['addToBetslipListener']({ isTote: true, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'} } as any);
      expect(toteBetslipService.addToteBet).toHaveBeenCalledTimes(1);
      expect(pubsub.publish).toHaveBeenCalledWith('CLEAR_BET_BUILDER');
      expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
    });

    it('toggle selection', () => {
      storageService.get.and.returnValue(false);
      service['addToBetslipListener']({GTMObject: { selectionID:'123'}, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any);
      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(1);
    });

    it('should save to session storage', () => {
      service['addToBetslipListener']({ GTMObject: { selectionID:'123'} ,test: 1, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'} } as any);

      expect(sessionStorage.set).toHaveBeenCalledWith(RemoteBetslipService.STORAGE_KEY, {
        GTMObject: { selectionID:'123'},test: 1, outcomes:[{id:'234234'}],
        details : {marketDrilldownTagNames : 'MKTFLAG_LD'}
      });
    });
    it('should save to session storage1', () => {
      sessionStorage.get.and.returnValue(null);
      service['addToBetslipListener']({ GTMObject: { selectionID:'123'} ,test: 1, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'} } as any);

      expect(sessionStorage.set).toHaveBeenCalledWith(RemoteBetslipService.STORAGE_KEY, {
        GTMObject: { selectionID:'123'},test: 1, outcomes:[{id:'234234'}],
        details : {marketDrilldownTagNames : 'MKTFLAG_LD'}
      });
    });
    it('should save to session storage1', () => {
      sessionStorage.get.and.returnValue(null);
      service['addToBetslipListener']({ GTMObject: { selectionID:'123'} ,test: 1, outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'} } as any);

      expect(sessionStorage.set).toHaveBeenCalledWith(RemoteBetslipService.STORAGE_KEY, {
        GTMObject: { selectionID:'123'},test: 1, outcomes:[{id:'234234'}],
        details : {marketDrilldownTagNames : 'MKTFLAG_LD'}
      });
    });

    it('isLotto bet Data', () => {
      const lottoData = {
          isLotto: true, 
          data:{
            selections:'22|23|24',
            draws: [{id: 1}]
          }
        };
        betslipDataService.containsRegularBets.and.returnValue(true);
        storageService.get.and.returnValue(false);
      service['addToBetslipListener'](lottoData as any);
      expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalled();
    });

    it('isLotto bet Data', () => {
      const lottoData = {
          isLotto: true, 
          data:{
            selections:'22|23|24',
            draws: [{id: 1}]
          }
        };
        betslipDataService.containsRegularBets.and.returnValue(false);
        storageService.get.and.returnValue(false);
        toteBetslipService.isToteBetPresent.and.returnValue(true);
      service['addToBetslipListener'](lottoData as any);
      expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalled();
    });

    it('addSingleOrMultipleBetsListener trigger toggleSelection', () => {
      const lottoData = [{
        isLotto: true, 
        data:{
          selections:'22|23',
          draws: [{id: 1}]
        }
      }];
      betslipDataService.containsRegularBets.and.returnValue(false);
      // storageService.get.and.returnValue(false);
      toteBetslipService.isToteBetPresent.and.returnValue(false);
      service['addSingleOrMultipleBetsListener'](lottoData as any);
      expect(betslipService.toggleSelection).toHaveBeenCalled();
    });

    it('addSingleOrMultipleBetsListener', () => {
      const lottoData = [{
        isLotto: true, 
        data:{
          selections:'22|23|24',
          draws: [{id: 1}]
        }
      }];
      betslipDataService.containsRegularBets.and.returnValue(false);
      // storageService.get.and.returnValue(false);
      toteBetslipService.isToteBetPresent.and.returnValue(false);
      service['addSingleOrMultipleBetsListener'](lottoData as any);
      expect(betslipService.showBetslipLimitationPopup).not.toHaveBeenCalled();
    })
  });

  describe('selectionAddedListener', () => {
    it('no GTM config', () => {
      service['selectionAddedListener']({ params: {} } as any);
      expect(command.executeAsync).not.toHaveBeenCalled();
    });

    it('no bet data', () => {
      service['selectionAddedListener']({
        params: {
          GTMObject: {
            tracking: {}
          }
        }
      } as any);
      expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('prepare tracking data', fakeAsync(() => {
      service['selectionAddedListener']({
        params: {
          GTMObject: {
            tracking: {},
            betData: {
              smth: '1'
            }
          }
        }
      } as any);
      tick();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
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

    it('prepare tracking data (if cases for streamData)', fakeAsync(() => {
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve({ streamActive: false }));
      service['selectionAddedListener']({
        params: {
          GTMObject: {
            tracking: {},
            betData: {
              smth: '1'
            }
          }
        }
      } as any);
      tick();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
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

    it('prepare data with no tracking property but stream possible', fakeAsync(() => {
      service['selectionAddedListener']({
        params: {
          GTMObject: {},
          eventIsLive: true,
        }
      } as any);
      tick();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        inPlayStatus: 'In Play',
        location: '/',
        customerBuilt: 'No',
        streamActive: 1,
        streamID: 12,
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

    it('prepare data with no tracking property but stream possible (if cases)', fakeAsync(() => {
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve({ streamActive: false }));
      service['selectionAddedListener']({
        params: {
          GTMObject: {},
          eventIsLive: false
        },
        isYourCallBet: true
      } as any);
      tick();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'add to betslip',
        eventLabel: 'success',
        inPlayStatus: 'Pre Event',
        location: '/',
        customerBuilt: 'Yes',
        streamActive: 0,
        streamID: null,
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
  });

  it('toggleLoadingOverlay', () => {
    service['toggleLoadingOverlay'](true);
    service['toggleLoadingOverlay'](false);
    expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledTimes(1);
    expect(nativeBridgeService.onClosePopup).toHaveBeenCalledTimes(1);
    expect(pubsub.publish).toHaveBeenCalledWith(
      pubSubApi.TOGGLE_LOADING_OVERLAY, jasmine.any(Object)
    );
  });

  describe('toggleQuickbetSelection', () => {
    beforeEach(() => {
      spyOn<any>(service, 'checkArcUser');
    });
    it('quick bet disabled', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        quickBet: null
      }));
      service['toggleQuickbetSelection']({} as any);
      tick();
      expect(betslipService.toggleSelection).toHaveBeenCalledTimes(1);
    }));

    it('show quickbet', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        quickBet: { EnableQuickBet: true }
      }));
      service['toggleQuickbetSelection']({} as any);
      tick();
      expect(command.executeAsync).toHaveBeenCalledWith(
        commandApi.SHOW_QUICKBET, jasmine.any(Array), 'error'
      );
    }));

    it('toggle loading overlay if error returned', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        quickBet: { EnableQuickBet: true }
      }));
      command.executeAsync.and.returnValue(Promise.resolve('error'));

      service['toggleQuickbetSelection']({} as any);
      tick();

      expect(pubsub.publish).toHaveBeenCalledWith(
        pubSubApi.TOGGLE_LOADING_OVERLAY, jasmine.any(Object)
      );
    }));

    it('toggle loading overlay if error thrown', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        quickBet: { EnableQuickBet: true }
      }));
      command.executeAsync.and.returnValue(Promise.reject('error'));

      service['toggleQuickbetSelection']({} as any);
      tick();

      expect(pubsub.publish).toHaveBeenCalledWith(
        pubSubApi.TOGGLE_LOADING_OVERLAY, jasmine.any(Object)
      );
    }));
  });

  describe('addToQuickbetFromNative', () => {
    it('overask in process', () => {
      overaskService.isInProcess = true;
      service['addToQuickbetFromNative']('1');
      expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalledTimes(1);
    });

    it('show quickbet', fakeAsync(() => {
      service['addToQuickbetFromNative']('1');
      tick();
      expect(command.executeAsync).toHaveBeenCalledWith(
        commandApi.SHOW_QUICKBET, jasmine.any(Array), jasmine.any(String)
      );
    }));

    it('toggle loading overlay if error returned', fakeAsync(() => {
      command.executeAsync.and.returnValue(Promise.resolve('error'));
      service['addToQuickbetFromNative']('1');
      tick();
      expect(pubsub.publish).toHaveBeenCalledWith(
        pubSubApi.TOGGLE_LOADING_OVERLAY, jasmine.any(Object)
      );
    }));

    it('toggle loading overlay if error thrown', fakeAsync(() => {
      command.executeAsync.and.returnValue(Promise.reject());
      service['addToQuickbetFromNative']('1');
      tick();
      expect(pubsub.publish).toHaveBeenCalledWith(
        pubSubApi.TOGGLE_LOADING_OVERLAY, jasmine.any(Object)
      );
    }));
  });
  describe('saveSelectionData', () => {
    it('should remove event and market property before storing to local storage', () => {
      const outcomes = [
        {
          id: 1,
          event: {},
          market: {}
        } as any
      ] as any[], selectionData = {
        outcomes
      } as any;
      service['saveSelectionData'](selectionData);
      expect(outcomes[0].event).toBeTruthy();
      expect(outcomes[0].market).toBeTruthy();
      expect(selectionData.outcomes[0].event).toBeTruthy();
      expect(selectionData.outcomes[0].market).toBeTruthy();
      expect(sessionStorage.set).toHaveBeenCalledWith('RemoteBS', {
        outcomes: [
          {
            id: 1
          } as any
        ]
      });
    });
  });
  describe('checkArcUser',() => {
    it('quickbet is disabled', () => {
      spyOn<any>(service,'toggleLoadingOverlay');
      service['checkArcUser']();
      expect(service['toggleLoadingOverlay']).toHaveBeenCalledWith(false);
    });
    it('quickbet is enabled', () => {
      spyOn<any>(service,'toggleLoadingOverlay');
      arcUserService.quickbet = false;
      service['checkArcUser']();
      expect(service['toggleLoadingOverlay']).toHaveBeenCalledWith(true);
    })
  });

  describe('addToStreamBetQuickBetListener',() => {
    it('overask in progress', () => {
      overaskService.isInProcess = true;
      service['addToStreamBetQuickBetListener']({outcomes:[{id:'234234'}],details : {marketDrilldownTagNames : 'MKTFLAG_LD'}} as any);
      expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalledTimes(1);
    });
    it('overask not in progress', () => {
      const selectionData = [{
        isLotto: true, 
        data:{
          selections:'22|23',
          draws: [{id: 1}]
        }
      }];
      overaskService.isInProcess = false;
      service['addSingleOrMultipleBetsListener'](selectionData as any);
      expect(betslipService.toggleSelection).toHaveBeenCalled();
    });
  });
});