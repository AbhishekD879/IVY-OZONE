import { Subject } from 'rxjs';
import { NavigationEnd } from '@angular/router';
import { fakeAsync, tick, flush } from '@angular/core/testing';

import { SidebarComponent } from '@app/lazy-modules/sidebar/components/sidebar.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('SidebarComponent', () => {
  let component: SidebarComponent;
  let stopListener;
  let device;
  let cms;
  let nativeBridgeService;
  let windowRefService;
  let rendererService;
  let domToolsService;
  let elementRef;
  let userService;
  let locationService;
  let router;
  let pubSubService;
  let route;
  let routingState;
  let sessionStorage;

  beforeEach(() => {
    stopListener = jasmine.createSpy('stopListener');
    userService = {
      oddsFormat: 'testOddsFormat',
      loginPending: false
    };
    device = {
      isNativeAndroid: true,
      isWrapper: true,
      isMobile: true
    };
    cms = {
      triggerSystemConfigUpdate: () => {
      }
    };
    nativeBridgeService = {
      onRightMenuClick: jasmine.createSpy(),
      onCloseBetSlip: jasmine.createSpy(),
      onOpenBetSlip: jasmine.createSpy(),
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy().and.returnValue({innerHTML:true})},
      nativeWindow: {
        document: {
          querySelectorAll: jasmine.createSpy(),
          body: {},
          documentElement: {}
        },
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn: Function, time: Number) => fn())
      }
    };
    rendererService = {
      renderer: {
        listen: stopListener
      } as any
    };
    domToolsService = {
      toggleClass: jasmine.createSpy(),
      css: jasmine.createSpy()
    };
    locationService = {
      path: jasmine.createSpy('path').and.returnValue('/home/private-markets')
    };
    elementRef = {
      nativeElement: {
        querySelectorAll: jasmine.createSpy('querySelectorAll'),
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          children: [{
            tag: 'A'
          }]
        }),
        children: [{
          tag: 'DIV'
        }]
      }
    };
    router = {
      events: new Subject()
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb({
        open: false,
        preventBridgeFn: {}
      })),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    route = {};
    routingState = jasmine.createSpyObj('routingState', ['getRouteParam']);

    sessionStorage = {
        get: jasmine.createSpy('get').and.callFake(
          n => {
            if(n === 'cashOutAvail') { return true } 
            else if(n === 'tutorialCompleted')  {return false}
            else {return true}
        }), 
      set: jasmine.createSpy('set')
    };

    component = new SidebarComponent(device, cms, nativeBridgeService, windowRefService, rendererService,
      domToolsService, elementRef, userService, locationService, router, pubSubService, route, routingState, sessionStorage);
    component['resizeListerner'] = () => {}; // fake function
    component['orientationChangeListerner'] = () => {}; // fake function
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should subscribe/unsubscribe renderer events', () => {
    spyOn<any>(component, 'showSidebar');
    component.ngOnInit();

    expect(rendererService.renderer.listen).toHaveBeenCalledTimes(2);
    expect(pubSubService.subscribe).toHaveBeenCalled();

    component.ngOnDestroy();
    expect(stopListener).toHaveBeenCalledTimes(2);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('sidebar');
  });

  it('should test betslip/right menu connect open/close event', () => {
    const data = {
      open: true
    };

    component.sideClass = 'test';

    const callbacks = {};
    pubSubService.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    spyOn<any>(component, 'showSidebar');

    component.ngOnInit();
    callbacks['show-test'](true);
    expect(component['showSidebar']).toHaveBeenCalledWith(true);

    callbacks['show-test']('someString');
    expect(component['showSidebar']).toHaveBeenCalledWith(true);

    callbacks['show-test'](false);
    expect(component['showSidebar']).toHaveBeenCalledWith(false);

    callbacks['show-test'](data);
    expect(component['showSidebar']).toHaveBeenCalledWith(true);
  });

  it('should call #showSidebar inside onDestroy function with correct params', () => {
    spyOn<any>(component, 'showSidebar');
    component.ngOnDestroy();

    expect(component['showSidebar']).toHaveBeenCalledWith(false, false);
  });

  describe('@showSidebar', () => {
    beforeEach(() => {
      spyOn<any>(component, 'updateSidebarState');
    });

    it('should publish only if bs', () => {
      component['showSidebar'](false);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should publish only if bs close action', () => {
      component.sideClass = 'slide-out-betslip';
      component['showSidebar'](true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenBetSlip).toHaveBeenCalled();
    });

    it('should not open slide out betSlip for nativeApp', () => {
      component.sideClass = 'sidebar-right-menu';
      component['showSidebar'](true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenBetSlip).not.toHaveBeenCalled();
    });

    it('should not open slide out betSlip for nativeApp', () => {
      component.sideClass = 'slide-out-betslip';
      device.isWrapper = false;
      component['showSidebar'](true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenBetSlip).not.toHaveBeenCalled();
    });

    it('should publish bs closing', () => {
      component.sideClass = 'slide-out-betslip';
      component['showSidebar'](false);

      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(nativeBridgeService.onCloseBetSlip).toHaveBeenCalled();
    });

    it('should publish bs closing', fakeAsync(() => {
      component.sideClass = 'slide-out-betslip';
      device.isWrapper = true;

      component['showSidebar'](false);
      tick();

      expect(component['updateSidebarState']).toHaveBeenCalledWith(false, true, true, false);
    }));
  });

  describe('handleRouteChange', () => {

    it('should not handle route change if it is the same prev and current url', fakeAsync(() => {
      const url = '/sport/football';

      component.ngOnInit();
      router.events.next(new NavigationEnd(0, url, url));
      router.events.next(new NavigationEnd(1, url, url));
      flush();

      expect(locationService.path).not.toHaveBeenCalled();
    }));

    it('should not handle route change if prevPage with market is same as current page', fakeAsync(() => {
      const previousUrl = '/event/football/england/premierLeague/123';
      const market = 'all-markets';
      const currentUrl = `/event/football/england/premierLeague/123/${market}`;

      routingState.getRouteParam.and.returnValue(market);
      component.ngOnInit();
      router.events.next(new NavigationEnd(0, previousUrl, previousUrl));
      router.events.next(new NavigationEnd(1, currentUrl, currentUrl));
      flush();

      expect(locationService.path).not.toHaveBeenCalled();
    }));

    it('should not handle route change if prevPage with market and market type is same as current page', fakeAsync(() => {
      const previousUrl = '/event/football/england/premierLeague/123';
      const market = 'all-markets';
      const currentUrl = `/event/football/england/premierLeague/123/${market}/${market}`;

      routingState.getRouteParam.and.returnValue(market);

      component.ngOnInit();
      router.events.next(new NavigationEnd(0, previousUrl, previousUrl));
      router.events.next(new NavigationEnd(1, currentUrl, currentUrl));
      flush();

      expect(locationService.path).not.toHaveBeenCalled();
    }));

    it('should not handle route change if prevPage and current are same racing pages', fakeAsync(() => {
      const previousUrl = '/horse-racing/horse-racing-live/catterick/15-15-catterick/9989282/totepool/quadpot';
      const market = '';
      const currentUrl = `/horse-racing/horse-racing-live/catterick/15-15-catterick/9989282/totepool/win`;

      routingState.getRouteParam.and.returnValue(market);

      component.ngOnInit();
      router.events.next(new NavigationEnd(0, previousUrl, previousUrl));
      router.events.next(new NavigationEnd(1, currentUrl, currentUrl));
      flush();

      expect(locationService.path).not.toHaveBeenCalled();
    }));

    it('should NOT hide sideBar if Football BetFilter page is shown during loginAndPlace a bet', () => {
      spyOn<any>(component, 'showSidebar');
      component.sidebarShown = true;
      locationService.path = jasmine.createSpy('path').and.returnValue('/bet-filter/results/all?today%27s-matches');

      component['handleRouteChange']({} as any);

      expect(component.sidebarShown).toBeTruthy();
      expect(component['showSidebar']).not.toHaveBeenCalled();
    });

    it('should hide sideBar if not Football BetFilter page is shown during loginAndPlace a bet', () => {
      spyOn<any>(component, 'showSidebar');
      component.sidebarShown = true;
      locationService.path = jasmine.createSpy('path').and.returnValue('/some/other/path');

      component['handleRouteChange']({} as any);

      expect(component['showSidebar']).toHaveBeenCalledWith(false, true);
    });

    it('should not hide sideBar if previous url was private markets', () => {
      spyOn<any>(component, 'showSidebar');
      component.sidebarShown = true;
      component['handleRouteChange']({ url: '/home/private-markets' } as any);
      expect(component['showSidebar']).not.toHaveBeenCalled();
    });

    it('should handle route change if prevPage and current are different racing pages', fakeAsync(() => {
      const previousUrl = '/horse-racing/horse-racing-live/catterick/15-15-catterick/9989282/totepool/quadpot';
      const market = '';
      const currentUrl = `/horse-racing/horse-racing-live/catterick/15-15-catterick/9989285/totepool/win`;

      routingState.getRouteParam.and.returnValue(market);

      component.ngOnInit();
      router.events.next(new NavigationEnd(0, previousUrl, previousUrl));
      router.events.next(new NavigationEnd(1, currentUrl, currentUrl));
      flush();

      expect(locationService.path).toHaveBeenCalled();
    }));
  });

  describe('@updateSidebarState', () => {
    beforeEach(() => {
      component['document'] = {
        documentElement: {
          scrollTop: 0
        },
        body: {
          scrollTop: 0
        }
      } as any;
    });

    it('should publish event about sidebar status', () => {
      component.sideClass = 'lorem';
      component['updateSidebarState'](true, true, true, true);

      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 220, false);
      expect(pubSubService.publish).toHaveBeenCalledWith('show-lorem-true', 'prevent');

      component['updateSidebarState'](true, false, true, true);
      expect(pubSubService.publish).toHaveBeenCalledWith('show-lorem-true', '');
      expect(nativeBridgeService.onRightMenuClick).toHaveBeenCalled();
    });

    it('should remove focus from active element', () => {
      component['document'] = {
        activeElement: {
          blur: jasmine.createSpy('blur').and.callThrough()
        }
      } as any;
      component.sideClass = '';
      component['updateSidebarState'](false, true, true, true);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.HOME_BETSLIP);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 220, false);
      expect(pubSubService.publish).toHaveBeenCalledWith('show--false', 'prevent');
    });

    it('should updates state of the sidebar', () => {
      component['windowScrollY'] = 10;
      component.sideClass = '';
      component['updateSidebarState'](false, true, true, false);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.HOME_BETSLIP);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 220, false);
      expect(pubSubService.publish).toHaveBeenCalledWith('show--false', 'prevent');
      expect(document.documentElement.scrollTop).toEqual(0);
      expect(document.body.scrollTop).toEqual(0);
    });

    it('should updates state for Mobile', () => {
      component.sideClass = '';
      component['updateSidebarState'](false, true, true, false);
      device.isMobile = false;

      expect(nativeBridgeService.onRightMenuClick).not.toHaveBeenCalled();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 220, false);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
  });

  describe('@onKeyDown', () => {
    let keyCode;

    beforeEach(() => {
      keyCode = 4;
      component['hideSidebar'] = jasmine.createSpy('hideSidebar').and.callThrough();
    });

    it('should not call hideSidebar', () => {
      component.onKeyDown(keyCode);

      expect(component['hideSidebar']).not.toHaveBeenCalled();
    });

    it('should call hideSidebar', () => {
      keyCode = 27;
      component.onKeyDown(keyCode);

      expect(component['hideSidebar']).toHaveBeenCalled();
    });
  });

  describe('@handleOuterClick', () => {
    let event;

    beforeEach(() => {
      event = {
        target: {
          classList: {
            contains: (className) => true
          },
          className: 'sidebar'
        }
      } as any;
      component['showSidebar'] = jasmine.createSpy('showSidebar').and.callThrough();
    });

    it('should close sidebar by clicking on overlay', () => {
      component.handleOuterClick(event);

      expect(component['showSidebar']).toHaveBeenCalledWith(false);
    });

    it('should close sidebar by clicking on close button', () => {
      event = {
        target: {
          classList: {
            contains: (className) => true
          },
          className: 'sidebar-close'
        }
      } as any;
      sessionStorage.get = jasmine.createSpy()
      .withArgs('cashOutAvail').and.returnValue(false)
      .withArgs('betPlaced').and.returnValue(true);
      component.handleOuterClick(event);

      expect(pubSubService.publish).toHaveBeenCalledWith('FIRST_BET_PLACEMENT_TUTORIAL', { step: 'betDetails', tutorialEnabled: true, type: 'defaultContent' });
      expect(component['showSidebar']).toHaveBeenCalledWith(false);
    });

    it('check if cashout is avilable on clicking of close button', () => {
      event = {
        target: {
          classList: {
            contains: (className) => true
          },
          className: 'sidebar-close'
        }
      } as any;
      component.handleOuterClick(event);

      expect(pubSubService.publish).toHaveBeenCalledWith('FIRST_BET_PLACEMENT_TUTORIAL', { step: 'betDetails', tutorialEnabled: true, type: 'cashOut' });
      expect(component['showSidebar']).toHaveBeenCalledWith(false);
    });
  });

  describe('@formClassList', () => {
    let result;

    beforeEach(() => {
      component.sidePosition = 'left';
      component.sideClass = 'sideClass';
    });

    it('should add left sidebar class', () => {
      result = component['formClassList']();

      expect(result).toEqual('sidebar-android left-side sideClass');
    });

    it('should add right sidebar class', () => {
      device.isNativeAndroid = false;
      component.sidePosition = '';
      result = component['formClassList']();

      expect(result).toEqual(' right-side sideClass');
    });
  });

  describe('@hideSidebar', () => {
    beforeEach(() => {
      component.sidebarShown = true;
      component['showSidebar'] = jasmine.createSpy('showSidebar').and.callThrough();
    });

    it('should hide sidebar', () => {
      component['hideSidebar'](true);

      expect(component['showSidebar']).toHaveBeenCalledWith(false, true);
    });

    it('should hide sidebar', () => {
      component['hideSidebar']();

      expect(component['showSidebar']).toHaveBeenCalledWith(false, false);
    });

    it('should not hide sidebar', () => {
      component.sidebarShown = false;
      component['hideSidebar']();

      expect(component['showSidebar']).not.toHaveBeenCalled();
    });
  });

  describe('@resizeSidebar', () => {
    beforeEach(() => {
      component.sidebarShown = true;
      component['updateSidebarWidth'] = jasmine.createSpy('updateSidebarWidth').and.callThrough();
    });

    it('should update sidebar width on resize', () => {
      component['resizeSidebar']();

      expect(component['updateSidebarWidth']).toHaveBeenCalled();
    });

    it('should update sidebar width on resize', () => {
      component.sideWidth = 0;
      component['resizeSidebar']();

      expect(component['updateSidebarWidth']).toHaveBeenCalled();
    });

    it('should not update sidebar width on resize', () => {
      component.sideWidth = 1;
      component['resizeSidebar']();

      expect(component['updateSidebarWidth']).not.toHaveBeenCalled();
    });

    it('should not update sidebar width on resize', () => {
      component.sidebarShown = false;
      component['resizeSidebar']();

      expect(component['updateSidebarWidth']).not.toHaveBeenCalled();
    });
  });

  describe('@updateSidebarWidth', () => {
    beforeEach(() => {
      component['sideHideClose'] = 'sideHideClose';
      component.sideWidth = 1;
      elementRef.nativeElement.querySelectorAll = jasmine.createSpy('querySelectorAll').and.returnValue([{}]);
    });

    it('should update sidebar', () => {
      component['updateSidebarWidth']();

      expect(domToolsService.css).toHaveBeenCalledWith({ tag: 'A' }, { width: 1 });
      expect(domToolsService.css).toHaveBeenCalledWith({}, { width: 1 });
    });
  });
});
