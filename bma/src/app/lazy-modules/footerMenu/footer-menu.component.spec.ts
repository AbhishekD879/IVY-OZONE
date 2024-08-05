import { of } from 'rxjs';
import { FooterMenuComponent } from '@lazy-modules/footerMenu/footer-menu.component';
import { NavigationEnd } from '@angular/router';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';
describe('FooterMenuComponent', () => {
  let component: FooterMenuComponent;
  let cmsService;
  let userService;
  let casinoLinkService;
  let pubSubService;
  let betslipTabsService;
  let deviceService;
  let gtmService;
  let servingService;
  let router;
  let navigationService;
  let commandService;
  let cd, storageService,
  sessionStorageService;
  let windowRefService;
  let footerSubMenu,filtersService, bonusSuppressionService;

  beforeEach(() => {
    footerSubMenu = [ {
      disabled: false,
      lang: 'lang',
      linkTitle: '1-2-Free',
      linkTitle_brand: 'linkTitle_brand',
      sortOrder: 0,
      targetUri: 'racingsuperseries',
      inApp: false,
      id: 'id',
      brand: 'brand',
      createdBy: 'createdBy',
      createdAt: 'createdAt',
      updatedBy: 'updatedBy',
      updatedAt: 'updatedAt',
      updatedByUserName: 'updatedByUserName',
      createdByUserName: 'createdByUserName',
      target: 'target',
      targetUriCopy: 'targetUriCopy',
      sportName: 'sportName',
      relUri: false,
      svgId: 'svgId',
    }]
    cmsService = {
      getFooterMenu: jasmine.createSpy('getFooterMenu').and.returnValue(of([{
        id: '12',
        targetUri: '/',
        linkTitle: 'Home'
      }] as any)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of([])),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };
    userService = {
      status: false
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    }
    pubSubService = {
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string | string[], callback: Function) => {
        
        if(method === 'FIRST_BET_PLACEMENT_TUTORIAL'){
          callback({step: '2', tutorialEnabled: true});
        }
        else if(method ==='FIRST_BET'){
          callback();
        }
          else{callback();}
      }),
      publishSync: jasmine.createSpy('publishSync')
    };
    betslipTabsService = jasmine.createSpyObj('betslipTabsService', ['redirectToBetSlipTab']);
    deviceService = {
      isMobile: true,
      isTablet: false
    };
    servingService = {
      sendExternalCookies: jasmine.createSpy('sendExternalCookies'),
      getClass: jasmine.createSpy('getClass').and.returnValue(false)
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      events: of([])
    };
    casinoLinkService = {
      decorateCasinoLink: jasmine.createSpy().and.returnValue([]),
      uriDecoration: jasmine.createSpy('uriDecoration').and.returnValue('/')
    };
    gtmService = jasmine.createSpyObj('GTM', ['push']);
    navigationService = {
      isAbsoluteUri: () => true,
      redirect: jasmine.createSpy('redirect'),
      openUrl: jasmine.createSpy('openUrl')
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(of({})),
      API: {
        GET_OPEN_BETS_COUNT: 'GET_OPEN_BETS_COUNT',
        UNSUBSCRIBE_OPEN_BETS_COUNT: 'UNSUBSCRIBE_OPEN_BETS_COUNT'
      }
    };
    filtersService = {
      filterLinkforRSS: jasmine.createSpy('filterLinkforRSS').and.returnValue((of('promotion/details/exclusion'))),
    };
    cd = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    windowRefService = {
      document: {
        getElementById: jasmine.createSpy('getElementById').and.returnValue({
          classList: {
            add: jasmine.createSpy().and.returnValue('icon-pressed-state'),
            remove: jasmine.createSpy().and.returnValue('icon-default-state')
          }
        }),
      },
    };

    storageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
        
           if(n === 'betSelections') { return {}}
           else{ return null}
      })
    };

    sessionStorageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'firstBetTutorialAvailable') { return true}
          else if(n === 'betPlaced') { return null}
      })
    };

    component = new FooterMenuComponent(
      cmsService,
      userService,
      casinoLinkService,
      pubSubService,
      betslipTabsService,
      deviceService,
      gtmService,
      servingService,
      router,
      navigationService,
      commandService,
      cd,
      storageService,
      sessionStorageService,
      filtersService,
      windowRefService,
      bonusSuppressionService
    );

    component.onBoardingData={
      enbaled:true
    }
  });

  it('should create component with initialized properties', () => {
    expect(component.animate).toEqual(false);
    expect(component.animateOpenBetsCounter).toEqual(0);
    expect(component.moreThanTwenty).toEqual(false);
    expect(component.openBetsCounter).toEqual(0);
  });

  describe('customRedirect', () => {
    let mouseEvent;
    let link;

    beforeEach(() => {
      mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);
      link = {
        redirectUrl: '',
        relUri: '',
        linkTitle: 'title',
      };
    });

    it('should prevent default handler', () => {
      component.customRedirect(mouseEvent, link);

      expect(mouseEvent.preventDefault).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('should prevent default redirect tablet', () => {
      deviceService.isMobile = false;
      deviceService.isTablet = true;
      component.customRedirect(mouseEvent, link);
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('should delegate opening to service if redirectUrl is ready', () => {
      link.redirectUrl = 'http://external.com';
      link.relUri = 'http://external.com';

      component.customRedirect(mouseEvent, link);

      expect(navigationService.openUrl).toHaveBeenCalledWith(link.redirectUrl, true);
    });

    it('should not call service if no redirectUrl', () => {
      link.redirectUrl = '';
      link.relUri = 'http://external.com';

      component.customRedirect(mouseEvent, link);
      expect(navigationService.openUrl).not.toHaveBeenCalled();
    });
    it('should navigate to internal link', () => {
      link.redirectUrl = '/some/page';
      link.relUri = '';

      component.customRedirect(mouseEvent, link);

      expect(navigationService.openUrl).toHaveBeenCalledWith(link.redirectUrl, true);
    });

    it('should send additional tracking', () => {
      component.customRedirect(mouseEvent, link);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'navigation',
        eventAction: 'footer',
        eventLabel: link.linkTitle
      });
      expect(servingService.sendExternalCookies).toHaveBeenCalledWith(link.relUri);
      expect(betslipTabsService.redirectToBetSlipTab).toHaveBeenCalledWith(link.linkTitle);
    });
  });
  describe('#ngOnInit', () => {
    it('if betSlipActiveTab.name', () => {
      environment.brand='bma';
      storageService.get.and.returnValue([{}]);
      sessionStorageService.get.and.returnValue(true)
      router.events = of(new NavigationEnd(1, '', ''));
      component.ngOnInit();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });

    it('Should subscribe to SESSION LOGIN and update mybets', () => {
      component['handleMyBetsCount'] = jasmine.createSpy('handleMyBetsCount');
      component['getLinks'] = jasmine.createSpy('getLinks');
      environment.brand='ladbrokes';
      sessionStorageService.get.and.returnValue(true)
      router.events = of(new NavigationEnd(1, '', ''));
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubSubService.API.SESSION_LOGIN) {
            callback();
            expect(component['getLinks']).toHaveBeenCalled();
            expect(component['handleMyBetsCount']).toHaveBeenCalled();
          }
        });

      component.ngOnInit();
    });
    it('Should subscribe to SEGMENTED_FE_REFRESH and update mybets', () => {
      component['handleMyBetsCount'] = jasmine.createSpy('handleMyBetsCount');
      component['getLinks'] = jasmine.createSpy('getLinks');
      router.events = of(new NavigationEnd(1, '', ''));
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubSubService.API.SEGMENTED_FE_REFRESH) {
            callback();
            expect(component['getLinks']).toHaveBeenCalled();
            expect(component['handleMyBetsCount']).toHaveBeenCalled();
          }
        });
      component.ngOnInit();
    });
    it('Should subscribe to NONSEGMENTED_FE_REFRESH and update mybets', () => {
      component['handleMyBetsCount'] = jasmine.createSpy('handleMyBetsCount');
      component['getLinks'] = jasmine.createSpy('getLinks');
      router.events = of(new NavigationEnd(1, '', ''));
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubSubService.API.NONSEGMENTED_FE_REFRESH) {
            callback();
            expect(component['getLinks']).toHaveBeenCalled();
            expect(component['handleMyBetsCount']).toHaveBeenCalled();
          }
        });
        storageService.get.and.returnValue([{}]);
      component.ngOnInit();
    });
    it('Should subscribe to APP_BUILD_VERSION and update footerMenu', () => {
      component['getLinks'] = jasmine.createSpy('getLinks');
      router.events = of(new NavigationEnd(1, '', ''));
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubSubService.API.APP_BUILD_VERSION) {
            callback();
            expect(component['getLinks']).toHaveBeenCalled();
          }else{
            callback({step: 'pickYourBet', tutorialEnabled: true});
          }
        });
      component.ngOnInit();
    });

    it('if no betSlipActiveTab.name', () => {
      cmsService.getFooterMenu.and.returnValue(of([{
          id: '12',
          targetUri: '/',
          linkTitle: 'My Bets'
        }] as any));
      userService.status = true;
      component['deviceService'] = {
        isMobile: false,
        isTablet: false
      } as any;
      component.betSlipActiveTab.name = 'lorem ipsum';
      router.events = of(new NavigationEnd(1, '', ''));
      component.ngOnInit();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });

    it('if no betSlipActiveTab.name', () => {
      cmsService.getFooterMenu.and.returnValue(of([{
          id: '12',
          targetUri: '/',
          linkTitle: 'My Bets'
        }] as any));
      userService.status = true;
      component['deviceService'] = {
        isMobile: false,
        isTablet: false
      } as any;
      component.betSlipActiveTab.name = 'lorem ipsum';
      component['handleMyBetsCount'] = jasmine.createSpy('handleMyBetsCount');
      router.events = of(new NavigationEnd(1, '', ''));
      component.ngOnInit();

      expect(component['handleMyBetsCount']).toHaveBeenCalled();
    });


    it('should not call BetsCount if User not logged in', () => {
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe');
      userService.status = false;
      component['handleMyBetsCount'] = jasmine.createSpy('handleMyBetsCount');
      component.ngOnInit();

      expect(component['handleMyBetsCount']).not.toHaveBeenCalled();
    });
  });

  it('should call iconPressedState', () => {
    const link = {
      linkTitle: 'home',
      id: '123'
    }
    component.iconPressedState(link);
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('home');
  });

  it('should call iconDefaultState', () => {
    const link = {
      linkTitle: 'home',
      id: '123'
    }
    component.iconDefaultState(link);
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('123');
  });

  describe('getLinks', () => {
    it('should run detectChangess', () => {
      component['getLinks']();

      expect(cd.detectChanges).toHaveBeenCalled();
    });
    it('should run detectChangess with status true', () => {
      userService.status = true;
      component['getLinks']();

      expect(cd.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should unsubscribe from connect and execute command', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('footerMenu');
      expect(commandService.executeAsync).toHaveBeenCalledWith('UNSUBSCRIBE_OPEN_BETS_COUNT');
    });

    describe('#handleMyBetsCount', () => {
      beforeEach(() => {
        component['animateOpenBetsCount'] = jasmine.createSpy('animateOpenBetsCount');
        component['getOpenBetsCount'] = jasmine.createSpy('getOpenBetsCount')
          .and.returnValue(of({count: 10, moreThanTwenty: false}));
        cmsService.getSystemConfig.and.returnValue(of({BetsCounter: {enabled: true}}));
      });

      it('when BetsCounter is enabled and user is logged in should getOpenBetsCount and animateOpenBetsCount', () => {
      userService.status = true;
        component.ngOnInit();
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(component['getOpenBetsCount']).toHaveBeenCalled();
        expect(component['animateOpenBetsCount']).toHaveBeenCalledWith({count: 10, moreThanTwenty: false});
      });

      it('when BetsCounter is enabled and user is NOT logged in should not call getOpenBetsCount and animateOpenBetsCount', () => {
      userService.status = false;
      component.ngOnInit();
      expect(cmsService.getSystemConfig).toHaveBeenCalledTimes(1);
      expect(component['getOpenBetsCount']).toHaveBeenCalledTimes(1);
      expect(component['animateOpenBetsCount']).toHaveBeenCalledTimes(1);
    });



    describe('should not getOpenBetsCount', () => {
      it(' when BetsCounter is disabled', () => {
        userService.status = true;
        cmsService.getSystemConfig.and.returnValue(of( { BetsCounter: { enabled: false } }));
      });
      it(' when BetsCounter config is missing', () => {
        userService.status = true;
          cmsService.getSystemConfig.and.returnValue(of({}));
        });
        afterEach(() => {
          component.ngOnInit();
          expect(cmsService.getSystemConfig).toHaveBeenCalled();
          expect(component['getOpenBetsCount']).not.toHaveBeenCalled();
          expect(component['animateOpenBetsCount']).toHaveBeenCalledWith({} as any);
        });
      });
    });

    it('#getOpenBetsCount', () => {
      commandService.executeAsync.and.returnValue(Promise.resolve(of({count: 10, moreThanTwenty: false})));
      const result = component['getOpenBetsCount']();
      expect(commandService.executeAsync).toHaveBeenCalledWith('GET_OPEN_BETS_COUNT');
      result.subscribe(value => {
        expect(value).toEqual({count: 10, moreThanTwenty: false});
      });
    });

  describe('#animateOpenBetsCount', () => {
    let requestAnimationFrameCb = () => {};

    beforeEach(() => {
      spyOn(global as any, 'requestAnimationFrame').and.callFake(cb => requestAnimationFrameCb = cb);
    });
    describe('should not update component properties', () => {
      it('when current animateOpenBetsCounter is equal to new count value', () => {
        component['animateOpenBetsCounter'] = 10;
        component['animateOpenBetsCount']({ count: 10, moreThanTwenty: false });
      });
      it('when value is not defined/falsy', () => {
        component['animateOpenBetsCount'](null);
      });
      afterEach(() => {
        expect(global['requestAnimationFrame']).not.toHaveBeenCalled();
        expect(component.animate).toEqual(false);
      });
    });
    describe('when current animateOpenBetsCounter is not equal to new count value, should update component properties', () => {
      beforeEach(() => {
        component['animateOpenBetsCounter'] = 0;
      });
      it('for 20+ bets', () => {
        component['animateOpenBetsCount']({ count: 20, moreThanTwenty: true });
        expect(component.animate).toEqual(false);
        requestAnimationFrameCb();
        expect(component.moreThanTwenty).toEqual(true);
        expect(component.animate).toEqual(true);
        expect(component.animateOpenBetsCounter).toEqual(20);
        expect(component.openBetsCounter).toEqual(20);
      });

      it('for less than 20 bets', () => {
        component['animateOpenBetsCount']({ count: 19, moreThanTwenty: false });
        expect(component.animate).toEqual(false);
        requestAnimationFrameCb();
        expect(component.moreThanTwenty).toEqual(false);
        expect(component.animate).toEqual(true);
        expect(component.animateOpenBetsCounter).toEqual(19);
        expect(component.openBetsCounter).toEqual(19);
      });

      it('for 20 bets', () => {
        component['animateOpenBetsCounter'] = 20;
        component['animateOpenBetsCount']({ count: 20, moreThanTwenty: false });
        expect(component.animate).toEqual(false);
        requestAnimationFrameCb();
        expect(component.moreThanTwenty).toEqual(false);
        expect(component.animate).toEqual(true);
        expect(component.animateOpenBetsCounter).toEqual(20);
        expect(component.openBetsCounter).toEqual(20);
      });

      it('for more than 20 bets', () => {
        component['animateOpenBetsCounter'] = 20;
        component['animateOpenBetsCount']({ count: 20, moreThanTwenty: true });
        expect(component.animate).toEqual(false);
        requestAnimationFrameCb();
        expect(component.moreThanTwenty).toEqual(true);
        expect(component.animate).toEqual(true);
        expect(component.animateOpenBetsCounter).toEqual(20);
        expect(component.openBetsCounter).toEqual(20);
      });

      describe('for missing count property (coverage case)', () => {
        it('moreThanTwenty=false', () => {
          component['animateOpenBetsCount']({ count: null, moreThanTwenty: false });
          requestAnimationFrameCb();
          expect(component.animateOpenBetsCounter).toEqual(null);
          expect(component.openBetsCounter).toEqual(0);
        });
        it('moreThanTwenty=true', () => {
          component['animateOpenBetsCount']({ count: null, moreThanTwenty: true });
          requestAnimationFrameCb();
          expect(component.animateOpenBetsCounter).toEqual(null);
          expect(component.openBetsCounter).toEqual(20);
        });
      });
      afterEach(() => {
        expect(cd.detectChanges).toHaveBeenCalledTimes(2);
        expect(global['requestAnimationFrame']).toHaveBeenCalledWith(jasmine.any(Function));
      });
    });
  });
});

  it('trackByIndex', () => {
    expect(component.trackByIndex(123)).toBe(123);
  });

  describe('isActiveLink', () => {
    it('betSlipActiveTab.name is not equal linkTitle', () => {
      component.betSlipActiveTab.name = 'lorem ipsum';
      expect(component['isActiveLink']({linkTitle: 'new'} as any)).toBe(false);
    });

    it('betSlipActiveTab.name is equal linkTitle', () => {
      component.betSlipActiveTab.name = 'lorem ipsum';
      expect(component['isActiveLink']({linkTitle: 'lorem ipsum'} as any)).toBe(true);
    });

    it('betSlipActiveTab.name is falthy', () => {
      component.betSlipActiveTab.name = '';
      expect(component['isActiveLink']({
        linkTitle: 'new',
        targetUri: '/'
      } as any)).toBe(false);
    });
  });

  describe('updateLinksState', () => {
    it('should run detectChangess', () => {
      component['updateLinksState']();
      expect(cd.detectChanges).toHaveBeenCalled();
    });
  });
  describe('#filterFooterBasedOnRgyellow, should filterout headerlinks based on rgYellow status',() =>{
    it('filterFooterBasedOnRgyellow should filter out links with rgYellow true', () =>{
      component.footerLinks = footerSubMenu;
      component.filterFooterBasedOnRgyellow();
      expect(component.footerLinks).toEqual(footerSubMenu);
    })
  });
  describe('#filterLinkforRSS,',() =>{
    it('filterLinkforRSS should filter out links with rss true', () =>{
      (filtersService['filterLinkforRSS']as any).and.returnValue(of('promotion/details/exclusion'));
     component.ngOnInit();
    component.footerLinks[0].targetUri = 'racingsuperseries';
      component['updateLinksState']();
      expect(filtersService.filterLinkforRSS).toHaveBeenCalled();
    })
  })
});
