import { PromotionDetailsComponent } from './promotion-details.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of, throwError, BehaviorSubject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { EVENTS_DATA } from '@app/promotions/constants/promotion-mock';
import { dialogIdentifierDictionary } from '@app/core/constants/dialog-identifier-dictionary.constant';
import {  bpmpReponseReturnOffers_one, bpmpReponseReturnOffers_two,bpmpReponseReturnOffers_three } from '../../constants/promotion-details.mock';

describe('PromotionDetailsComponent', () => {
  let promotionDetailsComponent,
    userService,
    msgDetails,
    router,
    route,
    cmsService,
    promotionsService,
    pubSubService,
    dynamicComponentsService,
    rendererService,
    promotionData,
    changeDetectorRef,
    siteServerService,
    eventsData,
    fakeConnection,
    ChannelService,
    CacheEventsService,
    UpdateEventService,
    componentFactoryResolver,
    resolvedDialogComponent,
    dialogService,
    promotionsNavigationService,
    gtmService,
    freeRideHelperService,
    bonusSuppressionService,
    deviceService,
    bppService;

  beforeEach(() => {
    eventsData = EVENTS_DATA;
    promotionsService = {
      isUserLoggedIn: jasmine.createSpy('isUserLoggedIn')
    };
    dialogService = <any>{
      API: dialogIdentifierDictionary,
      openDialog: jasmine.createSpy('openDialog').and.callFake((p1, p2, p3, opt) => {
        opt.data.callConfirm();
      }),
      closeDialog: jasmine.createSpy('closeDialog')
    };
    resolvedDialogComponent = {
      name: dialogService.API.howItWorksDialog
    };
    componentFactoryResolver = <any>{
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
    };
    dynamicComponentsService = {
      addComponent: jasmine.createSpy()
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    route = {
      params: of({ typeName: 'typeName', promoKey: 'promoKey' })
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((p1, p2, callback) => {
        callback();
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.callFake((p1, p2) => {
        return of(['sysConfig']);
      }),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };
    promotionData = {
      marketLevelFlag: 'marketLevelFlag',
      eventLevelFlag: 'eventLevelFlag',
      useDirectFileUrl: 'sport/football/matches/today',
      directFileUrl: 'sport/football/matches/today',
      overlayBetNowUrl: 'url',
      flagName: 'flags',
      iconId: 'icon/122'
    };
    promotionsNavigationService = {
      isNavGroup: jasmine.createSpy('isNavGroup'),
      getNavigationGroups: jasmine.createSpy('getNavigationGroups').and.returnValue(of([{}])),
      setNavGroupData: jasmine.createSpy('setNavGroupData'),
      getLeaderBoards:jasmine.createSpy('getLeaderBoards').and.returnValue(of([{}])),
    };
    promotionsService = {
      isUserLoggedIn: jasmine.createSpy('isUserLoggedIn'),
      disableOptInButton: jasmine.createSpy('disableOptInButton'),
      decorateLinkAndTrust: jasmine.createSpy('decorateLinkAndTrust'),
      enableOptInButton: jasmine.createSpy('enableOptInButton'),
      changeBtnLabel: jasmine.createSpy('changeBtnLabel'),
      sendGTM: jasmine.createSpy('sendGTM'),
      preparePromotions: jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return p1;
      }),
      storeId: jasmine.createSpy('storeId').and.callFake((p1) => {
        return of({ fired: false });
      }),
      getPromotionsFromSiteCore: jasmine.createSpy('getPromotionsFromSiteCore').and.returnValue(of({}))
    };
    dynamicComponentsService = {
      addComponent: jasmine.createSpy('addComponent')
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen')
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    siteServerService = {
      getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(Promise.resolve(eventsData))
    };
    fakeConnection = {
      connected: true,
      id: 10
    };
    ChannelService = {
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue('1234'),
    };
    CacheEventsService = {
      store: jasmine.createSpy('getLSChannelsFromArray').and.callThrough(),
      clearByName: jasmine.createSpy('clearByName').and.callThrough()
    };
    UpdateEventService = {
      init: jasmine.createSpy('init').and.callThrough()
    };
    userService = {
      vipLevel: jasmine.createSpy('vipLevel').and.returnValue('1234')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    bonusSuppressionService = {
      navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false)
    };

    freeRideHelperService = {
      showFreeRide:  jasmine.createSpy('showFreeRide')
    }
    promotionDetailsComponent = new PromotionDetailsComponent(
      userService,
      promotionsService,
      promotionsNavigationService,
      pubSubService,
      rendererService,
      {} as any,
      {} as any,
      cmsService,
      dynamicComponentsService,
      router,
      route,
      changeDetectorRef,
      siteServerService,
      ChannelService,
      CacheEventsService,
      UpdateEventService,
      dialogService,
      freeRideHelperService,
      deviceService,
      componentFactoryResolver,
      gtmService,
      bonusSuppressionService,
      bppService
    );

    promotionDetailsComponent['sysConfig'] = {
      OptInMessagging: {
        alreadyOptedInMessage: 'successMessage',
        errorMessage: 'ffs',
        successMessage: 'successMessage',
      }
    };
    promotionDetailsComponent['elementRef'] = {
      nativeElement: {
        querySelectorAll: () => { },
        querySelector: () => { },
      }
    };
    bppService={
      send: jasmine.createSpy('send')
    }
  });

  describe('@infoPanelWarningMessage', () => {
    beforeEach(() => {
      promotionDetailsComponent.sysConfig = { OptInMessagging: { errorMessage: 'ffs' } };
      msgDetails = { type: 'warning', message: 'ffs', align: 'center' };
    });

    it('should run infoPanelWarningMessage function first time', () => {
      promotionDetailsComponent['infoPanelComponent'] = null;
      promotionDetailsComponent['optInButton'] = { parentNode: 'who cares' };
      const optInButton = promotionDetailsComponent['optInButton'];

      promotionDetailsComponent['infoPanelWarningMessage']();

      expect(dynamicComponentsService.addComponent)
        .toHaveBeenCalledWith(jasmine.any(Function), msgDetails, optInButton.parentNode, optInButton);
    });

    it('should run infoPanelWarningMessage function rest times with other params', () => {
      promotionDetailsComponent['infoPanelComponent'] = { instance: { showInfoPanel() { } } };
      const ifoPanelInstance = promotionDetailsComponent['infoPanelComponent'].instance;
      spyOn(ifoPanelInstance, 'showInfoPanel');

      promotionDetailsComponent['infoPanelWarningMessage']();

      expect(ifoPanelInstance.showInfoPanel)
        .toHaveBeenCalledWith(msgDetails.message, msgDetails.type);
    });
  });


  describe('init', () => {
    beforeEach(() => {
      promotionDetailsComponent.sysConfig = { OptInMessagging: { errorMessage: 'ffs' } };
      msgDetails = { type: 'warning', message: 'ffs', align: 'center' };
    });

    it('should call disableOptInButton', () => {
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((p1, p2, callback) => {
        callback('status');
      });
      spyOn(promotionDetailsComponent, 'disableOptInButton');
      spyOn(promotionDetailsComponent, 'getOptInStatus');

      promotionDetailsComponent['infoPanelComponent'] = null;
      promotionDetailsComponent['optInButton'] = { parentNode: 'who cares' };
      promotionDetailsComponent['validPromotion'] = true;
      promotionDetailsComponent['init']();
      expect(promotionDetailsComponent['disableOptInButton']).toHaveBeenCalled();
    });

    it('should not call disableOptInButton', () => {
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((p1, p2, callback) => {
        callback();
      });
      spyOn(promotionDetailsComponent, 'disableOptInButton');
      spyOn(promotionDetailsComponent, 'getOptInStatus');
      promotionDetailsComponent['infoPanelComponent'] = null;
      promotionDetailsComponent['optInButton'] = { parentNode: 'who cares' };
      promotionDetailsComponent['validPromotion'] = true;
      promotionDetailsComponent['init']();
      expect(promotionDetailsComponent['disableOptInButton']).not.toHaveBeenCalled();
    });

    it('should call enableOptInButton', () => {
      spyOn(promotionDetailsComponent, 'enableOptInButton');
      spyOn(promotionDetailsComponent, 'getOptInStatus');
      promotionDetailsComponent['infoPanelComponent'] = null;
      promotionDetailsComponent['optInButton'] = { parentNode: 'who cares' };
      promotionDetailsComponent['validPromotion'] = true;
      promotionDetailsComponent['init']();
      expect(promotionDetailsComponent['enableOptInButton']).toHaveBeenCalled();
    });

    it('should call initPromo', () => {
      spyOn(promotionDetailsComponent, 'initPromo');
      let status = true;
      promotionsService.isUserLoggedIn = jasmine.createSpy('isUserLoggedIn').and.callFake(() => {
        status = !status;
        return status;
      });
      promotionDetailsComponent['infoPanelComponent'] = null;
      promotionDetailsComponent['optInButton'] = { parentNode: 'who cares' };
      promotionDetailsComponent['lastLoginStatus'] = 'lastLoginStatus';
      promotionDetailsComponent['init']();

      expect(promotionDetailsComponent['initPromo']).toHaveBeenCalled();
    });

  });


  describe('OnInit', () => {

    it('should call onInit', () => {
      promotionDetailsComponent['elementRef'] = {
        nativeElement: {
          querySelector: jasmine.createSpy().and.returnValue('handle-opt-in'),
          querySelectorAll: jasmine.createSpy().and.returnValue('#promo-descr a')
        }
      };
      promotionDetailsComponent['rendererService'] = {
        renderer: {
          listen: jasmine.createSpy('listen').and.callFake((p1, p2, p3) => {
            return { listener: true };
          })
        }
      };
      promotionsService.promotionData = jasmine.createSpy().and.returnValue(Promise.resolve(
        promotionData
      ));
      spyOn(promotionDetailsComponent, 'showSpinner');
      spyOn(promotionDetailsComponent, 'hideSpinner');      
      spyOn(promotionDetailsComponent, 'populatePromoData');
      promotionDetailsComponent.ngOnInit();

      expect(promotionDetailsComponent.sysConfig).toEqual(['sysConfig']);
    });

    it('should call onInit', () => {
      const response = [{
        teasers: []
      }];
      promotionsService.promotionData = jasmine.createSpy().and.returnValue(throwError(null));
      spyOn(promotionDetailsComponent, 'showError');
      spyOn(promotionDetailsComponent, 'hideSpinner');
      (promotionsService['getPromotionsFromSiteCore'] as any).and.returnValue(of(response));
      promotionDetailsComponent.ngOnInit();

      expect(promotionDetailsComponent.showError).toHaveBeenCalled();
      expect(promotionDetailsComponent.hideSpinner).toHaveBeenCalled();
    });

    it('should call onInit with RGYellow true user', () => {
      bonusSuppressionService.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
      const response = [{
        teasers: []
      }];
      promotionsService.promotionData = jasmine.createSpy().and.returnValue(throwError(null));
      spyOn(promotionDetailsComponent, 'showError');
      spyOn(promotionDetailsComponent, 'hideSpinner');
      (promotionsService['getPromotionsFromSiteCore'] as any).and.returnValue(of(response));
      promotionDetailsComponent.ngOnInit();

      expect(promotionDetailsComponent.showError).toHaveBeenCalled();
      expect(promotionDetailsComponent.hideSpinner).toHaveBeenCalled();
    });


  });

  describe('disable Option button', () => {

    it('should not have been called ', () => {
      promotionDetailsComponent['optInButton'] = false;
      promotionDetailsComponent.disableOptInButton();

      expect(promotionsService.disableOptInButton).not.toHaveBeenCalled();
    });

    it('should have been called ', () => {
      promotionDetailsComponent['optInButton'] = true;
      promotionDetailsComponent['optInButtonListeners'] = [true];
      promotionDetailsComponent.disableOptInButton();

      expect(promotionsService.disableOptInButton)
        .toHaveBeenCalledWith(promotionDetailsComponent['optInButton'], promotionDetailsComponent['optInButtonListeners']);
    });

  });
  describe('enabled Option button', () => {

    it('should not been enabled option button ', () => {
      promotionDetailsComponent['optInButton'] = false;
      promotionDetailsComponent['optInButtonHandler'] = false;
      promotionDetailsComponent.enableOptInButton();

      expect(promotionsService.enableOptInButton).not.toHaveBeenCalled();
    });
    it('should not been enabled option button ', () => {
      promotionDetailsComponent['optInButton'] = true;
      promotionDetailsComponent['optInButtonHandler'] = false;
      promotionDetailsComponent.enableOptInButton();

      expect(promotionsService.enableOptInButton).not.toHaveBeenCalled();
    });

    it('should have been option enabled ', () => {
      promotionDetailsComponent['optInButton'] = true;
      promotionDetailsComponent['optInButtonHandler'] = true;
      promotionDetailsComponent.enableOptInButton();

      const result = [];
      result.push(promotionsService.enableOptInButton
        (promotionDetailsComponent['optInButton'], promotionDetailsComponent['optInButtonHandler']));

      expect(promotionDetailsComponent.optInButtonListeners).toEqual(result);
    });

  });

  describe('#changeAccordionState', () => {
    it('should call changeAccordionState method', () => {
      expect(promotionDetailsComponent.isExpanded).toEqual([true, true]);

      promotionDetailsComponent.changeAccordionState(1, false);

      expect(promotionDetailsComponent.isExpanded).toEqual([true, false]);
    });
  });

  describe('promoNotFired', () => {

    it('should call enableOptInButton', () => {

      spyOn(promotionDetailsComponent, 'enableOptInButton');
      promotionDetailsComponent['optInButtonClicked'] = false;
      promotionDetailsComponent.promoNotFired();

      expect(promotionDetailsComponent.enableOptInButton).toHaveBeenCalled();
    });
    it('should call enableOptInButton', () => {

      spyOn(promotionDetailsComponent, 'startOptIn');
      promotionDetailsComponent['optInButtonClicked'] = true;
      promotionDetailsComponent.promoNotFired();

      expect(promotionDetailsComponent['optInButtonClicked']).toBe(false);
      expect(promotionDetailsComponent.startOptIn).toHaveBeenCalled();
    });

  });

  describe('promoFired', () => {

    it('should call enableOptInButton', () => {

      promotionDetailsComponent['sysConfig'] = {
        OptInMessagging: {
          alreadyOptedInMessage: 'successMessage'
        }
      };
      promotionDetailsComponent.optInButton = true;
      promotionDetailsComponent.promoFired();

      expect(promotionsService.changeBtnLabel).toHaveBeenCalledWith
        (promotionDetailsComponent.sysConfig.OptInMessagging.alreadyOptedInMessage, promotionDetailsComponent.optInButton);
    });
  });
  describe('initPromotionButton', () => {

    beforeEach(() => {
      promotionDetailsComponent['elementRef'] = {
        nativeElement: {
          querySelector: jasmine.createSpy().and.returnValue('handle-opt-in')
        }
      };
      promotionsService['isUserLoggedIn'] = jasmine.createSpy().and.callFake(() => {
        return true;
      });

      promotionDetailsComponent.optInButton = true;
      promotionDetailsComponent['domToolsService'] = {
        removeClass: jasmine.createSpy('removeClass')
      };
      promotionDetailsComponent['rendererService'] = {
        renderer: {
          listen: jasmine.createSpy('listen').and.callFake((p1, p2, p3) => {
            return { listener: true };
          })
        }
      };

      spyOn(window, 'clearTimeout');
    });

    it('should call domToolsService', fakeAsync(() => {
      promotionDetailsComponent['COMPILATION_DELAY'] = '1000';
      promotionDetailsComponent['timeoutInstance'] = '1000';
      promotionsService['isUserLoggedIn'] = jasmine.createSpy().and.callFake(() => {
        return true;
      });
      promotionDetailsComponent.validPromotion={
        requestId:'12345'
      }
      spyOn(promotionDetailsComponent,'getOptInStatus');
      promotionDetailsComponent.initPromotionButton();
      tick(1000);
      expect(promotionDetailsComponent['optInButton']).toEqual('handle-opt-in');
      expect(promotionDetailsComponent['domToolsService'].removeClass).toHaveBeenCalled();
    }));

    it('should not been called domToolsService', fakeAsync(() => {
      promotionsService['isUserLoggedIn'] = jasmine.createSpy().and.callFake(() => {
        return true;
      });
      spyOn(promotionDetailsComponent,'getOptInStatus');
      promotionDetailsComponent.validPromotion={
        requestId:'12345'
      }
      promotionDetailsComponent['elementRef'] = {
        nativeElement: {
          querySelector: jasmine.createSpy().and.returnValue(null)
        }
      };
      promotionDetailsComponent['COMPILATION_DELAY'] = '1000';
      promotionDetailsComponent.initPromotionButton();
      tick(1000);
      expect(promotionDetailsComponent['optInButton']).toEqual(null);
      expect(promotionDetailsComponent['domToolsService'].removeClass).not.toHaveBeenCalled();
    }));

    it('should add new eventListener', fakeAsync(() => {
      promotionDetailsComponent['COMPILATION_DELAY'] = '1000';
      spyOn(promotionDetailsComponent,'getOptInStatus');
      promotionDetailsComponent.validPromotion={
        requestId:'12345'
      }
      promotionDetailsComponent.validPromotion.requestId='1000'
      promotionDetailsComponent.initPromotionButton();

      tick(1000);
      expect(promotionDetailsComponent['optInButtonListeners']).toEqual([{ listener: true }]);
      expect(promotionDetailsComponent['eventListeners']).toEqual([{ listener: true }]);
    }));
  });

  describe('sendGTM', () => {
    it('send should be call', () => {
      const clickEvent = {
        target: {
          dataset: {}
        }
      };
      promotionDetailsComponent['validPromotion'] = true;
      promotionDetailsComponent.sendGTM(clickEvent);

      expect(promotionsService['sendGTM']).toHaveBeenCalled();
    });
  });


  describe('initPromo', () => {
    beforeEach(() => {
      spyOn(promotionDetailsComponent, 'initPromotionButton');
    });

    it('should call initPromo', () => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup'
        }];
      });
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();

      expect(promotionDetailsComponent['initPromotionButton']).toHaveBeenCalled();
    });

    it('should not call initPromo', () => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => []);
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();

      expect(promotionDetailsComponent['initPromotionButton']).not.toHaveBeenCalled();
    });

    it('should call isNavGroup', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      spyOn(promotionDetailsComponent,'clickNavItem');
      spyOn(promotionDetailsComponent, 'getNavGroup').and.returnValue([{id:'test',navItems:[{name:'xyz'}]}]);
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();
      tick();

    expect(promotionDetailsComponent.getNavGroup).toHaveBeenCalled();
    }));

    it('should get data for selected nav item', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      spyOn(promotionDetailsComponent,'clickNavItem');
      spyOn(promotionDetailsComponent, 'getNavGroup').and.returnValue([{id:'123',navItems:[{name:'leaderboard'}]}]);
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();

      tick();
     expect(promotionDetailsComponent.initPromotionButton).toHaveBeenCalled();
    }));

    it('should set navGroupItem as blank array' , fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      promotionDetailsComponent.navGroups = [{id:'hjkshkjd'},{id:'dfsf'}];
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      spyOn(promotionDetailsComponent,'clickNavItem');
      promotionDetailsComponent.getNavGroup('test_blank');
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();

      tick();

    expect(promotionDetailsComponent.navGroupItem).toEqual([]);
    }));

    it('should  get data for selected nav item if item name is description', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      spyOn(promotionDetailsComponent, 'getNavGroup').and.returnValue([{id:'123',navItems:[{name:'description'}]}]);
      spyOn(promotionDetailsComponent,'clickNavItem');
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();

      tick();

    expect(promotionDetailsComponent.initPromotionButton).toHaveBeenCalled();
    }));

    it('should call preventdefault if event passed', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      promotionDetailsComponent.navGroupItem = [{id:'123',navItems:[{name:'Leaderboard'}],navType:'Leaderboard'}];
      promotionDetailsComponent['promotion'] = true;
      const clickEvent = {
        preventDefault: jasmine.createSpy().and.returnValue(true),
      } as any;
      spyOn(promotionDetailsComponent,'filterLeaderBoardById')
      promotionDetailsComponent.clickNavItem(promotionDetailsComponent.navGroupItem[0],clickEvent);

      tick();

     expect(promotionDetailsComponent.filterLeaderBoardById).toHaveBeenCalled();
    }));

    it('should call preventdefault if event passed with descriptionTxt', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      promotionDetailsComponent.navGroupItem = [{id:'123',navItems:[{name:'Leaderboard'}],navType:'Leaderboard',descriptionTxt:'text'}];
      promotionDetailsComponent['promotion'] = true;
      const clickEvent = {
        preventDefault: jasmine.createSpy().and.returnValue(true),
      } as any;
      spyOn(promotionDetailsComponent,'filterLeaderBoardById')
      promotionDetailsComponent.clickNavItem(promotionDetailsComponent.navGroupItem[0],clickEvent);

      tick();

     expect(promotionDetailsComponent.filterLeaderBoardById).toHaveBeenCalled();
    }));

    it('should call getLeaderBoards ', fakeAsync(() => {
      spyOn(promotionDetailsComponent,'clickNavItem');
      promotionDetailsComponent.getLeaderBoards();
      expect(promotionDetailsComponent.clickNavItem).toHaveBeenCalled();

    }));
 
    it('should call filterLeaderBoardById ', fakeAsync(() => {
      promotionDetailsComponent.leaderBoardList = [
        {
          id: '1',
          name: 'leaderboard'
        },
        {
          id: '2',
          name: 'leader'
        }
      ] 
       promotionDetailsComponent.filterLeaderBoardById('1');
       expect(promotionDetailsComponent.lbConfigData).toEqual({id: '1',name: 'leaderboard'});

    }));

    it('should call preventdefault if event passed', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      promotionDetailsComponent.navGroupItem = [{id:'123',navItems:[{name:'leaderboard'}],navType:[{name:'leaderboard'}]}];
      promotionDetailsComponent['promotion'] = true;
      const clickEvent = {
        preventDefault: jasmine.createSpy()
      } as any;
      spyOn(promotionDetailsComponent,'filterLeaderBoardById')
      promotionDetailsComponent.clickNavItem(promotionDetailsComponent.navGroupItem[0],clickEvent);

      tick();

     expect(promotionDetailsComponent.filterLeaderBoardById).not.toHaveBeenCalled();
    }));

    it('should call isNavGroup and set navGroupItem empty', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{id:'test'}])
      spyOn(promotionDetailsComponent, 'getNavGroup').and.returnValue([{id:'testid',navItems:[{name:'xyz'}]}]);
      spyOn(promotionDetailsComponent,'clickNavItem');
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();
      tick();

    expect(promotionDetailsComponent.getNavGroup).toHaveBeenCalled();
    }));

    it('should call isNavGroup and set navGroupItem empty', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      promotionDetailsComponent.navGroups = [];
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([])
      spyOn(promotionDetailsComponent, 'getNavGroup').and.returnValue([{id:'testid',navItems:[{name:'xyz'}]}]);
      spyOn(console, 'warn')
      spyOn(promotionDetailsComponent, 'getLeaderBoards')
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();
      tick();

    expect(promotionDetailsComponent.getNavGroup).toHaveBeenCalled();
    }));

    it('should call isNavGroup and getNavigationGroups', fakeAsync(() => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup',
          navigationGroupId: '123'
        }];
      });
      (promotionsNavigationService['isNavGroup']as any) = new BehaviorSubject([{}]);
      spyOn(promotionDetailsComponent,'clickNavItem');
      spyOn(promotionDetailsComponent, 'getNavGroup').and.returnValue([{id:'testid',navItems:[{name:'xyz'}],navType:'description'}]);
      promotionDetailsComponent['promotion'] = true;
      promotionDetailsComponent.initPromo();
      tick();

    expect(promotionDetailsComponent.getNavGroup).toHaveBeenCalled();
    }));
  });

  describe('optInButtonHandler', () => {

    it('disableOptInButton to have not been called', () => {
      const event = {
        preventDefault: () => { },
        stopPropagation: () => { },
      };
      spyOn(promotionDetailsComponent, 'disableOptInButton');
      spyOn(promotionDetailsComponent, 'startOptIn');

      promotionDetailsComponent['validPromotion'] = true;
      promotionDetailsComponent['infoPanelComponent'] = {
        instance: {
          hideInfoPanel: () => { }
        }
      };
      promotionDetailsComponent.optInButtonHandler(event);

      expect(pubSubService['publish']).toHaveBeenCalled();
      expect(promotionDetailsComponent['disableOptInButton']).not.toHaveBeenCalled();
      expect(promotionDetailsComponent['startOptIn']).not.toHaveBeenCalled();
    });

    it('disableOptInButton to have been called', () => {
      const event = {
        preventDefault: () => { },
        stopPropagation: () => { },
      };

      promotionsService['isUserLoggedIn'] = jasmine.createSpy().and.callFake(() => {
        return true;
      });

      spyOn(promotionDetailsComponent, 'disableOptInButton');
      spyOn(promotionDetailsComponent, 'startOptIn');

      promotionDetailsComponent['validPromotion'] = true;
      promotionDetailsComponent.optInButtonHandler(event);

      expect(pubSubService['publish']).not.toHaveBeenCalled();
      expect(promotionDetailsComponent['disableOptInButton']).toHaveBeenCalled();
      expect(promotionDetailsComponent['startOptIn']).toHaveBeenCalled();
    });
  });

  describe('checkPromotionStatus', () => {
    it('notFiredCallBack should be call', () => {

      promotionsService.checkStatus = jasmine.createSpy().and.callFake((p1) => {
        return of({ fired: false });
      });

      promotionDetailsComponent.validPromotion = {
        requestId: 123
      };
      const firedCallBack = spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      const notFiredCallBack = spyOn(promotionDetailsComponent, 'enableOptInButton');
      promotionDetailsComponent.checkPromotionStatus(firedCallBack, notFiredCallBack);

      expect(notFiredCallBack).toHaveBeenCalled();
    });

    it('FiredCallBack should be call', () => {

      promotionsService.checkStatus = jasmine.createSpy().and.callFake((p1) => {
        return of({ fired: true });
      });

      promotionDetailsComponent.validPromotion = {
        requestId: 123
      };
      const firedCallBack = spyOn(promotionDetailsComponent, 'enableOptInButton');
      const notFiredCallBack = spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      promotionDetailsComponent.checkPromotionStatus(firedCallBack, notFiredCallBack);

      expect(firedCallBack).toHaveBeenCalled();
    });

    it('should return error should', () => {
      promotionsService.checkStatus = jasmine.createSpy().and.returnValue(throwError(null));
      promotionDetailsComponent.validPromotion = {
        requestId: 123
      };
      const firedCallBack = spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      const notFiredCallBack = spyOn(promotionDetailsComponent, 'enableOptInButton');
      promotionDetailsComponent.checkPromotionStatus(firedCallBack, notFiredCallBack);

      expect(notFiredCallBack).toHaveBeenCalled();
    });
  });

  describe('startOptIn', () => {

    it('should be true', () => {

      spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      spyOn(promotionDetailsComponent, 'enableOptInButton');
      promotionDetailsComponent['validPromotion'] = {
        requestId: 123
      };
      promotionDetailsComponent.startOptIn();

      expect(promotionDetailsComponent.infoPanelWarningMessage).toHaveBeenCalled();
      expect(promotionDetailsComponent.enableOptInButton).toHaveBeenCalled();
    });

    it('changeBtnLabel should be called', () => {
      promotionsService['storeId'] = jasmine.createSpy('storeId').and.callFake((p1) => {
        return of({ fired: true });
      });
      spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      spyOn(promotionDetailsComponent, 'enableOptInButton');
      promotionDetailsComponent['validPromotion'] = {
        requestId: 123
      };
      promotionDetailsComponent.startOptIn();

      expect(promotionDetailsComponent.infoPanelWarningMessage).not.toHaveBeenCalled();
      expect(promotionDetailsComponent.enableOptInButton).not.toHaveBeenCalled();
    });

    it('should be false ', () => {

      spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      spyOn(promotionDetailsComponent, 'enableOptInButton');
      promotionDetailsComponent['validPromotion'] = {
        requestId: 123
      };
      promotionDetailsComponent.startOptIn();

      expect(promotionDetailsComponent.infoPanelWarningMessage).toHaveBeenCalled();
      expect(promotionDetailsComponent.enableOptInButton).toHaveBeenCalled();
    });

    it('should return error ', () => {

      spyOn(promotionDetailsComponent, 'infoPanelWarningMessage');
      spyOn(promotionDetailsComponent, 'enableOptInButton');

      promotionsService.storeId = jasmine.createSpy().and.returnValue(throwError(null));
      promotionDetailsComponent['validPromotion'] = {
        requestId: 123
      };
      promotionDetailsComponent.startOptIn();

      expect(promotionDetailsComponent.infoPanelWarningMessage).toHaveBeenCalled();
      expect(promotionDetailsComponent.enableOptInButton).toHaveBeenCalled();
    });

  });


  describe('@checkRedirect', () => {
    it('should navigate using route if attr "routerlink" is exist', () => {
      const clickEvent = {
        target: {
          dataset: {
            routerlink: 'sport/football/matches/today'
          }
        },
        path: []
      };
      promotionDetailsComponent.checkRedirect(clickEvent);
      expect(router.navigateByUrl).toHaveBeenCalledWith('sport/football/matches/today');
    });

    it('should handle error using catch', fakeAsync(() => {
      const clickEvent = {
        target: {
          dataset: {
            routerlink: 'sport/football/matches/today'
          }
        },
      };
      spyOn(console, 'warn');
      promotionDetailsComponent.checkRedirect(clickEvent);
      
      tick();
      expect(console.warn).toHaveBeenCalled();
    }));


    it('should not navigate if attr "routerlink" is not exist', () => {
      const clickEvent = {
        target: {
          dataset: {}
        },
        path: []
      };
      promotionDetailsComponent.checkRedirect(clickEvent);
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });

    describe('ngOnDestroy', () => {
      it('ngOnDestroy, init', () => {
        spyOn(window, 'clearTimeout');

        promotionDetailsComponent['timeoutInstance'] = '100';
        promotionDetailsComponent['init']();
        promotionDetailsComponent.ngOnDestroy();
        expect(pubSubService.subscribe).toHaveBeenCalledTimes(4);
        expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
      });

      it('should remove all listeners', () => {
        const listener = jasmine.createSpy('listener');

        promotionDetailsComponent.eventListeners.push(listener);

        promotionDetailsComponent.ngOnDestroy();
        expect(listener).toHaveBeenCalled();
      });
    });
  });

  describe('@handleGtmTracking', () => {
    it('handleGtmTracking (sendGTM)', () => {
      const event = <any>{
        target: {
          nodeName: 'A'
        },
        path: [
          {
            id: 'q'
          },
          {
            id: 'terms-and-cond'
          }
        ]
      };
      promotionDetailsComponent['handleGtmTracking'](event);
      expect(promotionsService.sendGTM).toHaveBeenCalled();
    });

    it('handleGtmTracking (sendGTM)', () => {
      const event = <any>{
        target: {
          nodeName: 'A'
        },
        path: [
          {
            id: 'q'
          },
          {
            id: 'promo-descr'
          }
        ]
      };
      promotionDetailsComponent['handleGtmTracking'](event);
      expect(promotionsService.sendGTM).toHaveBeenCalled();
    });

    it('handleGtmTracking', () => {
      const event = <any>{
        target: {
          nodeName: 'A'
        },
        path: [
          {
            id: 'q'
          },
          {
            id: 'p'
          }
        ]
      };
      promotionDetailsComponent['handleGtmTracking'](event);
      expect(promotionsService.sendGTM).not.toHaveBeenCalled();
    });

    it('handleGtmTracking', () => {
      const event = <any>{
        target: {
          nodeName: 'B'
        },
        path: [
          {
            id: 'q'
          },
          {
            id: 'terms-and-cond'
          }
        ]
      };

      promotionDetailsComponent['handleGtmTracking'](event);
      expect(promotionsService.sendGTM).not.toHaveBeenCalled();
    });
  });
  describe('ngOnInit', () => {
    it('should call getSystemConfig with false param', () => {
      promotionDetailsComponent.ngOnInit();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });
  });

  describe('dynamic_promo', () => {
    it('should call getDynamicButtonDetails', () => {
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');

      promotionDetailsComponent['populatePromoData']('data');
      expect(promotionDetailsComponent['getDynamicButtonDetails']).toHaveBeenCalled();
    });

    it('populate is called', () => {
      promotionsService.preparePromotions = jasmine.createSpy('preparePromotions').and.callFake((p1) => {
        return [{
          requestId: 'requestId',
          safeDescription: 'safeDescription',
          safeHtmlMarkup: 'safeHtmlMarkup',
          description: 'description',
          htmlMarkup: 'htmlMarkup'
        }];
      });
      promotionDetailsComponent['promotion'] = true;
      spyOn(promotionDetailsComponent, 'populatePromoData');
      promotionDetailsComponent.initPromo();

      expect(promotionDetailsComponent['populatePromoData']).toHaveBeenCalled();
    });

    it('populate test cases is called', () => {
      const str = '<button id="dynamic-btn"> dasdasdadasdadads </button>';
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      promotionDetailsComponent.populatePromoData(str);
      expect(promotionDetailsComponent['getDynamicButtonDetails']).toHaveBeenCalled();
    });

    it('populate test cases is called with dynamicbtn', () => {
      const str = '<button id="dynamicbtn"> dasdasdadasdadads </button>';
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      promotionDetailsComponent.populatePromoData(str);
      expect(promotionDetailsComponent['getDynamicButtonDetails']).toHaveBeenCalled();
    });

    it('getDynamicButtonDetails is called', () => {
      const data = ['1234'];
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }];
      spyOn(promotionDetailsComponent, 'liveConnection');
      promotionDetailsComponent.getDynamicButtonDetails(data);
      expect(promotionDetailsComponent.promoDescriptionContentArr).not.toBeUndefined();
    });
    it('populate test cases is called with getChannels', () => {
      const data = [{
        htmlCont: 'content', selection: '1234', eventInfo: {
          outcome: { liveServChannels: 'SeleCN1234' },
          market: { liveServChannels: 'MARKET1234' }, event: { liveServChannels: 'EVENT1234' }
        }
      }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      const retVal = promotionDetailsComponent.getChannels(data);
      expect(retVal.length).not.toBe(0);
    });

    it('populate test cases is not called with getChannels', () => {
      const data = [{ htmlCont: 'content', selection: '1234', eventInfo: '' }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      const retVal = promotionDetailsComponent.getChannels(data);
      expect(retVal.length).toBe(0);
    });

    xit('populate test cases not to be called', () => {
      const str = '<bbbutton id="dynamic-btn"> dasdasdadasdadads </bbbutton>';
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      promotionDetailsComponent.populatePromoData(str);
      expect(promotionDetailsComponent['getDynamicButtonDetails']).toHaveBeenCalled();
    });

    xit('promoDescriptionContentArrection and sel.id doesnt match', () => {
      const data = ['123234'];
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '123234', eventInfo: '' as any }];
      spyOn(promotionDetailsComponent, 'liveConnection');
      promotionDetailsComponent.getDynamicButtonDetails(data);
      expect(promotionDetailsComponent.promoDescriptionContentArr).not.toBeUndefined();
    });

    it('subscribe to be called', () => {
      promotionDetailsComponent.promoDescriptionContentArr = [{
        htmlCont: 'content', selection: '1234', eventInfo: { event: { outcome: { id: '123' } } }
      }];
      spyOn(promotionDetailsComponent, 'getChannels');
      promotionDetailsComponent.liveConnection();

      expect(pubSubService.publish).toHaveBeenCalled();
    });

    it('rerendering should not be done', () => {
      promotionDetailsComponent.promoDescriptionContentArr = [{
        htmlCont: 'content', selection: '1234', eventInfo: { event: { outcome: { id: '123' } } }
      }];
      promotionDetailsComponent.promotion = true;
      promotionDetailsComponent.validPromotion = true;
      spyOn(promotionDetailsComponent, 'populatePromoData');
      promotionDetailsComponent.initPromo();

      expect(promotionDetailsComponent.populatePromoData).not.toHaveBeenCalled();
    });

    it('should check if its horse racing event', () => {
      const eventInfo = {
        categoryId: '21'
      };
      const output = promotionDetailsComponent.isRacingEvent(eventInfo);
      expect(output).toBe(true);
    });

    it('should check if its greyhound racing event', () => {
      const eventInfo = {
        categoryId: '19'
      };
      const output = promotionDetailsComponent.isRacingEvent(eventInfo);
      expect(output).toBe(true);
    });

    it('should check if its not racing event', () => {
      const eventInfo = {
        categoryId: '20'
      };
      const output = promotionDetailsComponent.isRacingEvent(eventInfo);
      expect(output).toBe(false);
    });
  });

  describe('checkPromotionType', () => {
    it('should call customPromotion emitter', () => {
      promotionDetailsComponent.promotion = { useCustomPromotionName: true, customPromotionName: 'Qwerty' };
      spyOn(promotionDetailsComponent.customPromotion, 'emit');
      promotionDetailsComponent.checkPromotionType();
      expect(promotionDetailsComponent.customPromotion.emit).toHaveBeenCalled();
    });
    it('should not call customPromotion emitter', () => {
      promotionDetailsComponent.promotion = { useCustomPromotionName: false, customPromotionName: 'Qwerty' };
      spyOn(promotionDetailsComponent.customPromotion, 'emit');
      promotionDetailsComponent.checkPromotionType();
      expect(promotionDetailsComponent.customPromotion.emit).not.toHaveBeenCalled();
    });
    it('should not call customPromotion emitter for empty customPromotionName', () => {
      promotionDetailsComponent.promotion = { useCustomPromotionName: true, customPromotionName: '' };
      spyOn(promotionDetailsComponent.customPromotion, 'emit');
      promotionDetailsComponent.checkPromotionType();
      expect(promotionDetailsComponent.customPromotion.emit).not.toHaveBeenCalled();
    });
  });
  describe('initBetpack', () => {
    it('populate test cases is called with dynamicbtn', () => {
      const str = '<button id="bet-pack-btn"> dasdasdadasdadads </button>';
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      spyOn(promotionDetailsComponent, 'initBetpack');
      promotionDetailsComponent.populatePromoData(str);
      expect(promotionDetailsComponent['getDynamicButtonDetails']).toHaveBeenCalled();
      expect(promotionDetailsComponent['initBetpack']).toHaveBeenCalled();
    });
    it('populate test cases not to be called', () => {
      const str = '<bbbutton id="notbetpackbtn"> dasdasdadasdadads </bbbutton>';
      promotionDetailsComponent.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' }];
      spyOn(promotionDetailsComponent, 'getDynamicButtonDetails');
      spyOn(promotionDetailsComponent, 'initBetpack');
      promotionDetailsComponent.populatePromoData(str);
      expect(promotionDetailsComponent['getDynamicButtonDetails']).toHaveBeenCalled();
      expect(promotionDetailsComponent['initBetpack']).not.toHaveBeenCalled();
    });
    it('call initBetpack', fakeAsync(() => {
      promotionDetailsComponent['elementRef'] = {
        nativeElement: {
          querySelector: jasmine.createSpy().and.returnValue({addEventListener : () => {}})
        }
      };
      promotionDetailsComponent.validPromotion = {
        title :  'test',
        vipLevel : 10,
        promotionId : '123',
        betPack:{
          offerId:'123'
        }
      };

      spyOn(window, 'clearTimeout');
      promotionDetailsComponent.timeoutInstance = jasmine.createSpy().and.returnValue(1);
      promotionDetailsComponent['COMPILATION_DELAY'] = '1000';
      promotionDetailsComponent['timeoutInstance'] = '1000';
      promotionDetailsComponent.initBetpack();
      tick(1000);
      spyOn(promotionDetailsComponent, 'onClick');
      expect(clearTimeout).toHaveBeenCalled();
      expect(promotionDetailsComponent.elementRef.nativeElement.querySelector).toHaveBeenCalled();
      expect(promotionDetailsComponent.elementRef.nativeElement.querySelector.and.returnValue({addEventListener : () => {}})).toHaveBeenCalled();
    }));
    it('should not call addEventListener if el has not set', fakeAsync(() => {
      promotionDetailsComponent['elementRef'] = {
        nativeElement: {
          querySelector: jasmine.createSpy().and.returnValue(null)
        }
      };
      spyOn(window, 'clearTimeout');
      promotionDetailsComponent.timeoutInstance = jasmine.createSpy().and.returnValue(1);
      promotionDetailsComponent['COMPILATION_DELAY'] = '1000';
      promotionDetailsComponent['timeoutInstance'] = '1000';
      promotionDetailsComponent.initBetpack();
      tick(1000);
      spyOn(promotionDetailsComponent, 'onClick');
      expect(clearTimeout).toHaveBeenCalled();
      expect(promotionDetailsComponent.elementRef.nativeElement.querySelector).toHaveBeenCalled();
      expect(promotionDetailsComponent.onClick).not.toHaveBeenCalled();
    }));
    it('should callDialog', () => {
      promotionDetailsComponent.validPromotion = {
        title :  'test',
        vipLevel : 10,
        promotionId : '123',
        betPack:{
          offerId:'123'
        }
      };

      const event = {
        preventDefault: () => { },
        stopPropagation: () => { },
        target : { innerHTML : 'test'}
      };
      spyOn(promotionDetailsComponent, 'callDialog');
      promotionDetailsComponent.onClick(event);
      expect(promotionDetailsComponent['callDialog']).toHaveBeenCalled();
    });
    it('should call through callDialog ', fakeAsync(() => {
      spyOn(promotionDetailsComponent, 'confirm');
      promotionDetailsComponent.callDialog();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalled();
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'promotionDialog', undefined, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('promotionDialog');
      expect(promotionDetailsComponent['confirm']).toHaveBeenCalled();
    }));
    it('call confirm',()=>{
      promotionDetailsComponent.validPromotion = {
        htmlMarkup: 'abc',
        description: 'def',
        safeCongratsMsg : ''
      };
      promotionDetailsComponent.promotion ={
        betPack : {
          congratsMsg : 'test'
        }
      };
      promotionDetailsComponent.confirm();
      expect(promotionDetailsComponent.validPromotion.htmlMarkup).toBeNull();
      expect(promotionDetailsComponent.validPromotion.description).toBeNull();
      expect(promotionDetailsComponent.validPromotion.safeCongratsMsg).not.toBeNull();
    });
  });

  it('openLoginDialog',()=>{
    promotionDetailsComponent.openLoginDialog();

    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('checkFreeRide, if showFreeRide returns true',()=>{
    // promotionDetailsComponent.freeRideErrorFlag = false;
    freeRideHelperService.showFreeRide.and.returnValue(true);

    promotionDetailsComponent['checkFreeRide']();

    expect(promotionDetailsComponent.freeRideFlag).toEqual(true);
  });

  it('checkFreeRide, if showFreeRide returns false',()=>{
    // promotionDetailsComponent.freeRideErrorFlag = false;
    freeRideHelperService.showFreeRide.and.returnValue(false);

    promotionDetailsComponent['checkFreeRide']();

    expect(promotionDetailsComponent.freeRideErrorFlag).toEqual(true);
  });

  it('closeDialogClick, if showFreeRide returns false',()=>{
    const eventInfo = {value : true}
    promotionDetailsComponent.closeDialogClick(eventInfo);

    expect(promotionDetailsComponent.freeRideFlag).toEqual(true);
  });
  it('getNavGroup', () => {
    spyOn(promotionDetailsComponent, 'initBetpack');
    promotionDetailsComponent.navGroups = [{id:'mockId'},{id:'mockId2'}]
    promotionDetailsComponent.getNavGroup('mockId');
     expect(promotionDetailsComponent['initBetpack']).not.toHaveBeenCalled();
  });

  it('getLbClassName', () => {
    promotionDetailsComponent.BRAND = 'ladbrokes'
    promotionDetailsComponent.activeNav = 'active'
    const navGroup = {
      name: 'active'
    }
    promotionDetailsComponent.getLbClassName(navGroup);
  });

  it('getLbClassName for coral', () => {
    promotionDetailsComponent.BRAND = 'bma'
    promotionDetailsComponent.activeNav = 'active'
    const navGroup = {
      name: 'active'
    }
    promotionDetailsComponent.getLbClassName(navGroup);
  });
  describe('getOptInStatus', () => {
    it('getOptInStatus should be call', () => {
      const disableOptInButton =spyOn(promotionDetailsComponent,'disableOptInButton')
      promotionDetailsComponent.bppService={
        send:jasmine.createSpy('send').and.returnValue(of(bpmpReponseReturnOffers_one))
      }
      promotionDetailsComponent.getOptInStatus('118095');

       expect(disableOptInButton).toHaveBeenCalled();
    });
    it('getOptInStatus should be call', () => {
      const disableOptInButton =spyOn(promotionDetailsComponent,'disableOptInButton')
      promotionDetailsComponent.bppService={
        send:jasmine.createSpy('send').and.returnValue(of(bpmpReponseReturnOffers_two))
      }
      promotionDetailsComponent.getOptInStatus('118095');

       expect(disableOptInButton).toHaveBeenCalled();
    });
    it('getOptInStatus should be call', () => {
      const disableOptInButton =spyOn(promotionDetailsComponent,'disableOptInButton')
      promotionDetailsComponent.bppService={
        send:jasmine.createSpy('send').and.returnValue(of(bpmpReponseReturnOffers_three))
      }
      promotionDetailsComponent.getOptInStatus('118095');

       expect(disableOptInButton).toHaveBeenCalled();
    });
    it('getOptInStatus should be call negative scenarios', () => {
      promotionDetailsComponent.bppService={
        send:jasmine.createSpy('send').and.returnValue(of(bpmpReponseReturnOffers_two))
      }
      promotionDetailsComponent.CheckInClaimedOffers('11800');
       expect(true).toEqual(true);
    });
  });
});
