import { fakeAsync, tick } from '@angular/core/testing';
import { NavigationEnd } from '@angular/router';
import { Subject } from 'rxjs';

import { FootballTutorialOverlayComponent } from '@sb/components/footballTutorialOverlay/football-tutorial-overlay.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('FootballTutorialComponent', () => {
  let component: FootballTutorialOverlayComponent;
  let deviceService;
  let router;
  let userService;
  let storageService;
  let locationService;
  let pubSubService;
  let domToolsService;
  let windowRefService;
  let rendererService;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout')
      },
      document: {
        getElementById: jasmine.createSpy(),
        querySelector: jasmine.createSpy().and.returnValue({})
      }
    };
    domToolsService = {
      hasClass: jasmine.createSpy(),
      css: jasmine.createSpy(),
      addClass: jasmine.createSpy(),
      removeClass: jasmine.createSpy(),
      getOffset: jasmine.createSpy(),
      setTranslate: jasmine.createSpy(),
      scrollPageTop: jasmine.createSpy(),
      getPageScrollTop: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb({})),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy()
    };
    locationService = {
      path: jasmine.createSpy('path').and.returnValue('not-home')
    };
    storageService = {
      remove: jasmine.createSpy('remove'),
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue(null)
    };
    userService = {
      status: false
    };
    router = {
      events: new Subject(),
      navigate: jasmine.createSpy('navigate')
    };
    deviceService = {
      isMobile: jasmine.createSpy('isMobile').and.returnValue(true)
    };
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass'),
        setStyle: jasmine.createSpy('setStyle'),
        listen: jasmine.createSpy('listen').and.callFake((a, b, cb) => cb && cb({}))
      }
    };

    component = new FootballTutorialOverlayComponent(windowRefService, domToolsService, pubSubService, storageService,
      userService, deviceService, locationService, rendererService, router);
  });

  it('should check isHomeUrl true', fakeAsync(() => {
    component.ngOnInit();
    component.isActive = true;
    router.events.next(new NavigationEnd(1, '/football/matches/today', 'urlAfterRedirects'));
    tick();
    expect(pubSubService.unsubscribe).not.toHaveBeenCalled();
  }));

  it('should check isHomeUrl false', fakeAsync(() => {
    component.ngOnInit();
    component.isActive = true;
    router.events.next(new NavigationEnd(1, 'fake/url', 'urlAfterRedirects'));
    tick();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  }));

  it('should check isHomeUrl', fakeAsync(() => {
    component.ngOnInit();
    expect(component['isHomeUrl']('/fake/url')).toBeFalsy();
    expect(component['isHomeUrl']('/football/matches/today')).toBeTruthy();
  }));

  it('should show tutorial', () => {
    component['showTutorial'] = jasmine.createSpy('showTutorial');
    router.events.next(new NavigationEnd(1, 'fake/url', 'urlAfterRedirects'));
    component['storageService'].get = jasmine.createSpy('get').and.returnValue(null);
    component['userService'] = {status: true} as any;
    component.ngOnInit();

    expect(component['showTutorial']).toHaveBeenCalledTimes(2);
  });

  it('should update favorite star position', () => {
    component.ngOnInit();
    component.mainFavouriteStar = {} as any;
    component.homeBody = {} as any;
    deviceService.isMobile = true;
    windowRefService.nativeWindow.innerHeight = 200;
    windowRefService.nativeWindow.innerWidth = 100;

    domToolsService.getOffset = () => ({ top: 300, left: 0 });
    component['updatePositions']();
    component['cookieBanner'] = {get offsetHeight() { return 50; }} as any;
    component['updatePositions']();

    windowRefService.nativeWindow.innerHeight = 100;
    windowRefService.nativeWindow.innerWidth = 200;
    domToolsService.getOffset = () => ({ top: 100, left: 0 });
    component['updatePositions']();

    expect(domToolsService.scrollPageTop).toHaveBeenCalledTimes(3);
    expect(domToolsService.css).toHaveBeenCalledTimes(2);
  });

  it('should update favorite star position and call hideTutorial', () => {
    component.ngOnInit();
    component.mainFavouriteStar = {} as any;
    component.homeBody = {} as any;
    component['hideTutorial'] = jasmine.createSpy('hideTutorial');
    deviceService.isMobile = false;

    domToolsService.getOffset = () => ({ top: 300, left: 0 });
    component['updatePositions']();

    expect(domToolsService.css).toHaveBeenCalledTimes(1);
    expect(component['hideTutorial']).toHaveBeenCalledTimes(1);
  });

  it('should start animation', () => {
    component.topStar = {
      nativeElement: {
        getBoundingClientRect: jasmine.createSpy().and.returnValue({
          top: 100
        })
      }
    } as any;
    component.ngOnInit();
    component.footballOverlay = { querySelector: jasmine.createSpy() } as any;
    component.mainFavouriteStar = { querySelector: jasmine.createSpy() } as any;
    component.homeBody = {} as any;
    windowRefService.document.querySelector.and.returnValue({});
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());
    domToolsService.getOffset.and.returnValue({});
    component['animation']();

    windowRefService.document.querySelector = jasmine.createSpy().and.returnValue(null);
    component['animation']();

    expect(component.footballOverlay.querySelector).toHaveBeenCalledTimes(4);
    expect(component.mainFavouriteStar.querySelector).toHaveBeenCalledTimes(1);
    expect(windowRefService.document.querySelector).toHaveBeenCalledTimes(3);
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledTimes(4);
    expect(rendererService.renderer.addClass).toHaveBeenCalledTimes(3);
    expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(2);
    expect(domToolsService.setTranslate).toHaveBeenCalledTimes(2);
    expect(domToolsService.getPageScrollTop).toHaveBeenCalledTimes(1);
    expect(component.topStar.nativeElement.getBoundingClientRect).toHaveBeenCalled();
  });

  describe('ngOnDestroy', () => {
    it('should remove class from body if is homeBody', () => {
      const homeBody = {
        tagName: 'BODY'
      } as any;

      component.homeBody = homeBody;
      component.ngOnDestroy();

      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(homeBody, 'football-content-overlay');
    });

    it('should unsync from connect and pubsub events', () => {
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('footballTutorialOverlay');
    });

    it('should remove resize and orientation change listeners', () => {
      const windowResizeListener = jasmine.createSpy('windowResizeListener');
      const windowOrientationChangeListener = jasmine.createSpy('windowOrientationChangeListener');

      component['windowResizeListener'] = windowResizeListener;
      component['windowOrientationChangeListener'] = windowOrientationChangeListener;
      component.ngOnDestroy();

      expect(windowResizeListener).toHaveBeenCalled();
      expect(windowOrientationChangeListener).toHaveBeenCalled();
    });

    it('should unsubscribe from locationChange listener', () => {
      const locationChangeListener = {
        unsubscribe: jasmine.createSpy('locationChangeListener')
      } as any;

      component['locationChangeListener'] = locationChangeListener;
      component.ngOnDestroy();

      expect(locationChangeListener.unsubscribe).toHaveBeenCalled();
    });

    it('should clear timers', () => {
      const showTutorialTimer = 1;
      const runAnimationTimer = 2;
      const showBlockOverlayTimer = 3;
      const hideAnimatedElementTimer = 4;
      const showArr2Timer = 5;
      const textPanelAnimationTimer = 6;

      component['showTutorialTimer'] = showTutorialTimer;
      component['runAnimationTimer'] = runAnimationTimer;
      component['showBlockOverlayTimer'] = showBlockOverlayTimer;
      component['hideAnimatedElementTimer'] = hideAnimatedElementTimer;
      component['showArr2Timer'] = showArr2Timer;
      component['textPanelAnimationTimer'] = textPanelAnimationTimer;

      component.ngOnDestroy();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(showTutorialTimer);
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(runAnimationTimer);
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(showBlockOverlayTimer);
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(hideAnimatedElementTimer);
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(showArr2Timer);
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(textPanelAnimationTimer);
    });
  });

  describe('@hideTutorial', () => {
    it('should call destroyElement', () => {
      component.isActive = true;
      spyOn(component as any, 'destroyElement').and.callThrough();
      component['hideTutorial']();
      expect(component['destroyElement']).toHaveBeenCalled();
    });

    it('should not call destroyElement', () => {
      component.isActive = false;
      spyOn(component as any, 'destroyElement').and.callThrough();
      component['hideTutorial']();
      expect(component['destroyElement']).not.toHaveBeenCalled();
    });
  });

  describe('@showTutorial', () => {
    it('should call initElements', () => {
      spyOn(component as any, 'initElements').and.callThrough();
      spyOn(component as any, 'isHomeUrl').and.returnValue(true);
      spyOn(component as any, 'showAnimation');
      spyOn(component as any, 'updatePositions');
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => {
        cb(); // call setTimeout callback
      });
      const footballOverlay = {
        querySelector: jasmine.createSpy()
      };

      windowRefService.document = {
        querySelector: jasmine.createSpy(),
        getElementById: jasmine.createSpy('getElementById').and.returnValue(footballOverlay)
      };

      component['showTutorial']();

      expect(component['initElements']).toHaveBeenCalled();
      expect(component['showAnimation']).toHaveBeenCalledTimes(2);
      expect(component['updatePositions']).toHaveBeenCalledTimes(3);
    });

    it('should not call initElements', () => {
      component['location'] = { path: () => ('testUrl') } as any;
      spyOn(component as any, 'initElements').and.callThrough();
      component['showTutorial']();
      expect(component['initElements']).not.toHaveBeenCalled();
    });
  });

  describe('@showAnimation', () => {
    it('should call animation()', () => {
      component['animation'] = jasmine.createSpy();
      const footballOverlay = {
        querySelector: jasmine.createSpy()
      };
      windowRefService.document = {
        querySelectorAll: jasmine.createSpy().and.returnValue([{}, {}]),
        querySelector: jasmine.createSpy(),
        getElementById: jasmine.createSpy('getElementById').and.returnValue(footballOverlay)
      };
      component['showAnimation']({}, true);
      expect(component['animation']).toHaveBeenCalled();
    });

    it('should not call animation()', () => {
      component['animation'] = jasmine.createSpy();
      windowRefService.document = {
        querySelectorAll: jasmine.createSpy()
      };
      component['showAnimation']({});
      expect(component['animation']).not.toHaveBeenCalled();
    });
  });

});
