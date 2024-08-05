import { ModuleRibbonComponent } from '@shared/components/moduleRibbon/module-ribbon.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { GA_TRACKING } from '@shared/constants/channel.constant';
import environment from '@environment/oxygenEnvConfig';

describe('ModuleRibbonComponent', () => {
  const title = 'ModuleRibbonComponent';

  let moduleRibbonComponent,
    location,
    ribbonService,
    user,
    pubSubService,
    router,
    sessionService,
    cmsService,
    deviceService,
    sessionStorageService,
    bonusSuppressionService;

  const navPoints = [{
    homeTabs: ['/home/eventhub/2', '/home/featured'],
    ctaAlignment: 'center'
  }, {
    homeTabs: ['/home/eventhub/2', '/home/other'],
    ctaAlignment: 'right'
  }, {
    homeTabs: []
  }] as any;

  const gtmData = {
    isHomePage: true,
    event: GA_TRACKING.event,
    GATracking: {
      eventAction: GA_TRACKING.eventAction,
      eventCategory: GA_TRACKING.moduleRibbon.eventCategory,
      eventLabel: ""
    }
  }

  beforeEach(() => {
    location = {
      isCurrentPathEqualTo: jasmine.createSpy('isCurrentPathEqualTo'),
      path: jasmine.createSpy('path')
    };
    ribbonService = {
      moduleList: [{}],
      removeTab: jasmine.createSpy('removeTab'),
      isPrivateMarketsTab: jasmine.createSpy('isPrivateMarketsTab'),
      getPrivateMarketTab: jasmine.createSpy('getPrivateMarketTab').and.returnValue(of([])),
      filterTabs: jasmine.createSpy('isPrivateMarketsTab')
    };
    user = {};
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true),
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((place, key, callback) => {
        callback();
      }),
      unsubscribe: jasmine.createSpy()
    };
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue({
          unsubscribe: jasmine.createSpy()
        })
      },
      navigate: jasmine.createSpy('navigate'),
      url: '/'
    };
    sessionService = {
      whenUserSession: jasmine.createSpy('whenUserSession').and.returnValue(of({}))
    };
    cmsService = {
      getNavigationPoints: jasmine.createSpy('getNavigationPoints').and.returnValue(of(navPoints)),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };

    deviceService = {
      requestPlatform: 'mobile'
    };

    sessionStorageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'firstBetTutorial') { return null }
          else if(n === 'initialTabLoaded')  {return null }
      }),
      set: jasmine.createSpy('set')
    }

    moduleRibbonComponent = new ModuleRibbonComponent(
      location, ribbonService, user, pubSubService, router, sessionService, cmsService, deviceService, sessionStorageService,
      bonusSuppressionService
    );
    moduleRibbonComponent.moduleRibbon = null;
  });

  describe('@ngOnInit', () => {
    beforeEach(() => {
      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
    });

    it('ngOnInit success', fakeAsync(() => {
      moduleRibbonComponent.user.status= true;
      moduleRibbonComponent.ngOnInit();
      tick();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, ['SUCCESSFUL_LOGIN'], jasmine.any(Function));
      expect(ribbonService.getPrivateMarketTab).toHaveBeenCalledTimes(1);
    }));
    it('ngOnInit success', fakeAsync(() => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent.superButtonAvailable = false;
      moduleRibbonComponent.ngOnInit();
      tick();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, ['SEGMENTED_INIT_FE_REFRESH'], jasmine.any(Function));
      expect(ribbonService.getPrivateMarketTab).toHaveBeenCalledTimes(1);
    }));

    it('ngOnInit success', fakeAsync(() => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent.superButtonAvailable = true;
      moduleRibbonComponent.ngOnInit();
      tick();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, ['SEGMENTED_INIT_FE_REFRESH'], jasmine.any(Function));
      expect(ribbonService.getPrivateMarketTab).toHaveBeenCalledTimes(1);
    }));
    it('ngOnInit - user status = false', fakeAsync(() => {
      moduleRibbonComponent.user.status = false;
      moduleRibbonComponent.ngOnInit();
      tick();

      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, ['SUCCESSFUL_LOGIN'], jasmine.any(Function));
      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
      cmsService.getNavigationPoints().subscribe(() => {
        expect(moduleRibbonComponent.hasNavPointForHome.length>0).toBe(true);
      });
    }));

    it('ngOnInit error', () => {
      cmsService.getNavigationPoints.and.returnValue(of([]));
      moduleRibbonComponent.user.status = true;
      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(throwError(null));
      moduleRibbonComponent.ngOnInit();
      expect(ribbonService.getPrivateMarketTab).toHaveBeenCalledTimes(1);
      cmsService.getNavigationPoints().subscribe(() => {
        expect(moduleRibbonComponent.hasNavPointForHome.length>0).toBe(false);
      });
    });

    it('ngOnInit - redirect to private-markets page if "private markets" tab is available and user is' +
      'currently on Home Page', fakeAsync(() => {
        moduleRibbonComponent.user.status = true;
        sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));

        moduleRibbonComponent.router.url = '/';
        ribbonService.isPrivateMarketsTab.and.returnValue(true);

        moduleRibbonComponent.ngOnInit();
        tick();

        expect(router.navigate).toHaveBeenCalledWith(['home', 'private-markets']);
      }));

    it('ngOnInit - do NOT redirect to home page if "private markets" tab is NOT available and user is' +
      'currently NOT on PRivate markets Tab', fakeAsync(() => {
        moduleRibbonComponent.user.status = true;
        sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));

        location.isCurrentPathEqualTo.and.callFake(param => param === '/home/next-races');
        ribbonService.isPrivateMarketsTab.and.returnValue(false);

        moduleRibbonComponent.ngOnInit();
        tick();

        expect(router.navigate).not.toHaveBeenCalledWith(['/']);
      }));

    it('ngOnInit - do NOT redirect to private-markets page if user is currently NOT on Home page', fakeAsync(() => {
      moduleRibbonComponent.user.status = true;
      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));
      moduleRibbonComponent.router.url = '/home/private-markets';

      moduleRibbonComponent.ngOnInit();
      tick();

      expect(router.navigate).not.toHaveBeenCalledWith(['home', 'private-markets']);
    }));

    it('ngOnInit - do NOT redirect to private-markets page if "private markets" tab is NOT available and user is' +
      'currently on Home page', fakeAsync(() => {
        moduleRibbonComponent.user.status = true;
        sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));
        location.isCurrentPathEqualTo.and.callFake(param => param === '/' ? true : undefined);
        ribbonService.isPrivateMarketsTab.and.returnValue(false);

        moduleRibbonComponent.ngOnInit();
        tick();

        expect(router.navigate).not.toHaveBeenCalledWith(['home', 'private-markets']);
      }));

    it('isFirstBetAvailable should be true when no session data', fakeAsync(() => {
      sessionStorageService.get = jasmine.createSpy()
      .withArgs('firstBetTutorial').and.returnValue(null)
      .withArgs('initialTabLoaded').and.returnValue({id: 'featured-tab', url: '/home/featured'});

      moduleRibbonComponent.ngOnInit();
      expect(moduleRibbonComponent.initialTabLoaded).toEqual('featured-tab');
      expect(moduleRibbonComponent.isFirstBetAvailable).toBe(true);
    }))

    it('should set the initialTabLoaded when active tab is available', () => {
      sessionStorageService.get = jasmine.createSpy()
      .withArgs('firstBetTutorial').and.returnValue(null)
      .withArgs('initialTabLoaded').and.returnValue(null);

      moduleRibbonComponent.ngOnInit();
      expect(moduleRibbonComponent.isFirstBetAvailable).toBe(true);
    })
  });
  describe('ngOnchnages', () => {
    it('modulelist contains the baseurl case', () => {
      ribbonService.filterTabs.and.returnValue([{ 'url': 'test', 'title': 'test' }, { 'url': 'test2', 'title': 'test2' }]);
      router = {
        navigate: jasmine.createSpy('navigate'),
        url: '/'
      };
      location = {
        path: jasmine.createSpy('path').and.returnValue('test')
      };
      moduleRibbonComponent = new ModuleRibbonComponent(
        location, ribbonService, user, pubSubService, router, sessionService, cmsService, deviceService, sessionStorageService,
        bonusSuppressionService
      );
      moduleRibbonComponent['ngOnChanges']();
      expect(router.navigate).not.toHaveBeenCalled();
    });
    it('modulelist contains the baseurl case having Query params', () => {
      ribbonService.filterTabs.and.returnValue([{ 'url': 'test', 'title': 'test' }, { 'url': 'test2', 'title': 'test2' }]);
      router = {
        navigate: jasmine.createSpy('navigate'),
        url: '/'
      };
      location = {
        path: jasmine.createSpy('path').and.returnValue('test?q=1')
      };
      moduleRibbonComponent = new ModuleRibbonComponent(
        location, ribbonService, user, pubSubService, router, sessionService, cmsService, deviceService, sessionStorageService,
        bonusSuppressionService
      );
      moduleRibbonComponent['ngOnChanges']();
      expect(router.navigate).not.toHaveBeenCalled();
    });
    it('modulelist contains the doesnot contain baseurl case', () => {
      ribbonService.filterTabs.and.returnValue([{ 'url': 'test', 'title': 'test' }, { 'url': 'test2', 'title': 'test2' }]);
      router = {
        navigate: jasmine.createSpy('navigate'),
        url: '/'
      };
      location = {
        path: jasmine.createSpy('path').and.returnValue('testq?q=1')
      };
      moduleRibbonComponent = new ModuleRibbonComponent(
        location, ribbonService, user, pubSubService, router, sessionService, cmsService, deviceService, sessionStorageService,
        bonusSuppressionService
      );
      moduleRibbonComponent['ngOnChanges']();
      expect(router.navigate).toHaveBeenCalled();
    });
  });
  describe('setActiveTab', () => {
    it('set constants by negative condition', () => {
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
      moduleRibbonComponent.location.isCurrentPathEqualTo = jasmine.createSpy('isCurrentPathEqualTo').and.returnValue(true);
      moduleRibbonComponent.activeTab = { id: 'test' };
      moduleRibbonComponent['setActiveTab']();
      expect(moduleRibbonComponent.homeTabUrl).toEqual('/home/featured');
    });

    it('set constants by positive condition', () => {
      moduleRibbonComponent.location.isCurrentPathEqualTo = jasmine.createSpy('isCurrentPathEqualTo').and.returnValue(false);
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('test');
      moduleRibbonComponent.router.url = 'test';
      moduleRibbonComponent.activeTab = null;
      moduleRibbonComponent['setActiveTab']();
      expect(moduleRibbonComponent.homeTabUrl).toEqual('test');
    });
    it('set constants by positive condition to get call getHomeTabNavigationPoints', () => {
      moduleRibbonComponent.location.isCurrentPathEqualTo = jasmine.createSpy('isCurrentPathEqualTo').and.returnValue(false);
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/home/featured?q=1');
      moduleRibbonComponent.router.url = '/';
      moduleRibbonComponent.activeTab = null;
      moduleRibbonComponent['getHomeTabNavigationPoints'] = jasmine.createSpy('getHomeTabNavigationPoints');
      moduleRibbonComponent['setActiveTab']();
      expect(moduleRibbonComponent.homeTabUrl).toEqual('/home/featured');
      expect(moduleRibbonComponent['getHomeTabNavigationPoints']).toHaveBeenCalled();
    });
  });

  describe('getPlaceholderCls', () => {
    it('should return alignment class', () => {
      moduleRibbonComponent.sbAlignment = 'center';
      expect(moduleRibbonComponent.getPlaceholderCls()).toEqual('cta-center');
      expect(moduleRibbonComponent).toBeTruthy();
      moduleRibbonComponent.sbAlignment = 'right';
      expect(moduleRibbonComponent.getPlaceholderCls()).toEqual('cta-right');
    });
    
    it('should return no-cta',() => {
      moduleRibbonComponent.superButtonAvailable = true;
      spyOn(moduleRibbonComponent, 'isActiveTabHome').and.returnValue(true);
      moduleRibbonComponent.sbAlignment = '';
      expect(moduleRibbonComponent.getPlaceholderCls()).toEqual('no-cta');
    });
  });

  describe('getHomeTabNavigationPoints', () => {
    it('getHomeTabNavigationPoints', () => {
      moduleRibbonComponent.router.url = '/';
      moduleRibbonComponent['getHomeTabNavigationPoints']();
      expect(moduleRibbonComponent.hasNavPointForHome.length>0).toBe(true);
    });
    it('getHomeTabNavigationPoints', () => {
      moduleRibbonComponent.router.url = '/';
      cmsService.getNavigationPoints.and.returnValue(of([navPoints[1]]));
      moduleRibbonComponent['getHomeTabNavigationPoints']();
      expect(moduleRibbonComponent.hasNavPointForHome.length>0).toBe(false);
    });
  });
  describe('setGATrackingData', () => {
    it('set Ga Tracking Data with homepage true', () => {
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('');
      moduleRibbonComponent['setGATrackingData']();
      expect(moduleRibbonComponent.GTMTrackingObj).toEqual(gtmData);
    });
    it('set Ga Tracking Data with homepage false', () => {
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/next-races');
      moduleRibbonComponent['setGATrackingData']();
      expect(moduleRibbonComponent.GTMTrackingObj).not.toEqual(gtmData);
    });
  });
  describe('isCurrentPathEmpty', () => {
    it('should check that current path is empty', () => {
      moduleRibbonComponent.router.url = '/';
      const result = moduleRibbonComponent['isCurrentPathEmpty']();
      expect(result).toBeTruthy();
    });

    it('should check that current path is not empty', () => {
      moduleRibbonComponent.router.url = '/test';
      const result = moduleRibbonComponent['isCurrentPathEmpty']();
      expect(result).toBeFalsy();
    });

    it('should current path with query params in url', () => {
      moduleRibbonComponent.router.url = '/?id=2';
      const result = moduleRibbonComponent['isCurrentPathEmpty']();
      expect(result).toBeTruthy();
    });
  });

  describe('addPrivateMarketTab', () => {
    beforeEach(() => {
      moduleRibbonComponent['setLocation'] = jasmine.createSpy('setLocation');
    });

    it('should check for user session', (done: DoneFn) => {
      moduleRibbonComponent.user.status =true;
      moduleRibbonComponent['addPrivateMarketTab'](true);

      setTimeout(() => {
        expect(moduleRibbonComponent['setLocation']).toHaveBeenCalled();
        done();
      });
    });

    it('should not check for user session', (done: DoneFn) => {
      moduleRibbonComponent.user.status = false;
      moduleRibbonComponent['addPrivateMarketTab']();

      setTimeout(() => {
        expect(sessionService.whenUserSession).not.toHaveBeenCalled();
        expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
        expect(moduleRibbonComponent['setLocation']).not.toHaveBeenCalled();
        done();
      });
    });
  });

  describe('setLocation', () => {
    it('should navigate to home/private-markets page', () => {
      location.isCurrentPathEqualTo.and.callFake((path) => path === '/');
      ribbonService.isPrivateMarketsTab.and.returnValue(true);

      moduleRibbonComponent['setLocation']();

      expect(router.navigate).toHaveBeenCalledWith(['home', 'private-markets']);
    });

    it('should navigate to home page when it is not private market', () => {
      location.isCurrentPathEqualTo.and.returnValue(true);
      ribbonService.isPrivateMarketsTab.and.returnValue(false);

      moduleRibbonComponent['setLocation']();

      expect(location.isCurrentPathEqualTo).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    afterEach(() => {
      expect(ribbonService.isPrivateMarketsTab).toHaveBeenCalled();
    });
  });

  it('ngOnDestroy should unsubscribe', () => {
    moduleRibbonComponent.routeListener = jasmine.createSpyObj(['unsubscribe']);

    moduleRibbonComponent.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
    expect(moduleRibbonComponent.routeListener.unsubscribe).toHaveBeenCalled();
  });

  describe('addPrivateMarketTab', () => {
    it('should set privateMarketTabCreated to true, call ribbonService.getPrivateMarketTab, fill moduleList and call setLocation',
      fakeAsync(() => {
        moduleRibbonComponent['privateMarketTabCreated'] = false;
        moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
        moduleRibbonComponent['setLocation'] = jasmine.createSpy('setLocation');
        ribbonService.getPrivateMarketTab.and.returnValue(of([1]));
        moduleRibbonComponent.user.status = true;
        moduleRibbonComponent['addPrivateMarketTab']();
        tick();

        expect(moduleRibbonComponent['privateMarketTabCreated']).toBe(true);
        expect(moduleRibbonComponent['setLocation']).toHaveBeenCalled();
        expect(moduleRibbonComponent.moduleList).toEqual([1]);
      }));

    it('should set privateMarketTabCreated to false when getPrivateMarketTab promise fails', fakeAsync(() => {
      moduleRibbonComponent['privateMarketTabCreated'] = false;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['setLocation'] = jasmine.createSpy('setLocation');
      ribbonService.getPrivateMarketTab.and.returnValue(throwError(''));
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent['addPrivateMarketTab']();
      tick();

      expect(moduleRibbonComponent['privateMarketTabCreated']).toBe(false);
      expect(moduleRibbonComponent['setLocation']).not.toHaveBeenCalled();
      expect(moduleRibbonComponent.moduleList).toEqual(undefined);
    }));

    it('should NOT go into if statement body if user is not defined', () => {
      moduleRibbonComponent.user = null;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['privateMarketTabCreated'] = false;

      moduleRibbonComponent['addPrivateMarketTab']();

      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
    });

    it('should NOT go into if statement body if isOnPrivateMarketTab returns true', () => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(true);
      moduleRibbonComponent['privateMarketTabCreated'] = false;

      moduleRibbonComponent['addPrivateMarketTab']();

      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
    });

    it('should NOT go into if statement body if privateMarketTabCreated is set to true', () => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['privateMarketTabCreated'] = true;

      moduleRibbonComponent['addPrivateMarketTab']();

      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
    });
  });

  it('isActiveTabHome', () => {
    moduleRibbonComponent.activeTab = {
      url: '/home/featured'
    };
    expect(moduleRibbonComponent['isActiveTabHome']()).toBe(true);
    moduleRibbonComponent.activeTab = {
      url: ''
    };
    expect(moduleRibbonComponent['isActiveTabHome']()).toBe(true);
    moduleRibbonComponent.activeTab = {
      url: 'other'
    };
    expect(moduleRibbonComponent['isActiveTabHome']()).toBe(false);
  });

  it('superButtonAvailable in setActiveTab', () => {
    moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
    moduleRibbonComponent['getHomeTabNavigationPoints'] = jasmine.createSpy('getHomeTabNavigationPoints');
    moduleRibbonComponent['isActiveTabHome'] = jasmine.createSpy('isActiveTabHome').and.returnValue(true);
    moduleRibbonComponent.hasNavPointForHome = navPoints[0];
    cmsService.hasExtraNavPoints = true;
    moduleRibbonComponent['setActiveTab']();
    expect(moduleRibbonComponent.superButtonAvailable).toBe(true);

    moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
    moduleRibbonComponent['isActiveTabHome'].and.returnValue(false);
    moduleRibbonComponent.hasNavPointForHome = navPoints[0];
    cmsService.hasExtraNavPoints = true;
    moduleRibbonComponent['setActiveTab']();
    expect(moduleRibbonComponent.superButtonAvailable).toBe(true);

    moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
    moduleRibbonComponent['isActiveTabHome'].and.returnValue(true);
    moduleRibbonComponent.hasNavPointForHome = [];
    cmsService.hasExtraNavPoints = true;
    moduleRibbonComponent['setActiveTab']();
    expect(moduleRibbonComponent.superButtonAvailable).toBe(true);

    moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
    moduleRibbonComponent['isActiveTabHome'].and.returnValue(true);
    moduleRibbonComponent.hasNavPointForHome = [];
    cmsService.hasExtraNavPoints = false;
    moduleRibbonComponent['setActiveTab']();
    expect(moduleRibbonComponent.superButtonAvailable).toBe(false);
  });

  describe('#filterModulesBasedOnRgyellow, should filterout headerlinks based on rgYellow status',() =>{
    it('filterModulesBasedOnRgyellow should filter out links with rgYellow true', () =>{
      moduleRibbonComponent.user.rgYellow = false;
      environment.brand = 'bma';
      moduleRibbonComponent.moduleList = [{ title: '1-2-Free' }, { title: 'restricted'}];
      moduleRibbonComponent['filterModulesBasedOnRgyellow']();
      expect(moduleRibbonComponent.moduleList.length).toEqual(2);
    })
  });

  it('isFirstBetAvailable should be false on onStartTutorialClick', () => {
    moduleRibbonComponent['onStartTutorialClick']();
    expect(moduleRibbonComponent.isFirstBetAvailable).toBe(false);
  })
});