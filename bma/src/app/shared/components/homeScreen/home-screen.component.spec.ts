import { fakeAsync, tick } from '@angular/core/testing';
import { HomeScreenComponent } from '@shared/components/homeScreen/home-screen.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('HomeScreenComponent', () => {
  let component,
      rendererService,
      pubsub,
      windowRef,
      device,
      domTools,
      nativeBridgeService,
      sessionstorageService;

  beforeEach(() => {
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(() => {
        }),
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass')
      }
    };
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((location, action, fn) => {
        fn();
      }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    windowRef = {
      nativeWindow: {
        innerWidth: 10,
        innerHeight: 5,
        orientation: 90,
        setTimeout: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        document: {
          activeElement: {
            blur: jasmine.createSpy('blur')
          },
          querySelector: jasmine.createSpy('querySelector').and.returnValue('querySelector_result'),
        }
      },
      document: {
        getElementById: jasmine.createSpy('getElementById').and.returnValue({
          style: {
            display: ''
          }
        }),
      }
    };
    device = {
      isWrapper: false,
      mobileWidth: 20,
      isTallMobile: true
    };
    domTools = {
      removeClass: jasmine.createSpy('removeClass')
    };
    nativeBridgeService = {
      pageLoaded: jasmine.createSpy('pageLoaded')
    };
    sessionstorageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    }

    component = new HomeScreenComponent(
      rendererService,
      pubsub,
      windowRef,
      device,
      domTools,
      nativeBridgeService,
      sessionstorageService
    );
    component.listeners = [];
    component.events = ['click', 'touchstart', 'touchend', 'touchmove'];
  });

  describe('#ngOnInit', () => {
    it('should call replayEvents() & pageLoaded()', fakeAsync(() => {
      pubsub.subscribe.and.callFake((location, action, fn) => {
        if (action === 'APP_IS_LOADED') {
          fn(true);
          expect(windowRef.document.getElementById('home-screen').style.display).toBe('none');
        }
      });
      component.ngOnInit();
      tick();
      expect(pubsub.subscribe).toHaveBeenCalledWith('HomeScreenComponent', 'APP_IS_LOADED', jasmine.any(Function));
    }));

    it('should call onWindowResize if device is mobile', () => {
      component['device'].isMobile = true;

      spyOn(component, 'onWindowResize');

      component.ngOnInit();

      expect(component.onWindowResize).toHaveBeenCalledTimes(1);
    });

    it('should call onWindowResize if device is mobile', () => {
      component['device'].isMobile = true;

      spyOn(component, 'onWindowResize');

      component.ngOnInit();
      expect(component.onWindowResize).toHaveBeenCalledTimes(1);
    });

    describe('on orientation change', () => {
      const callbackMethods = {};
      beforeEach(() => {
        component['device'].isWrapper = true;
        component['device'].isAndroid = true;
        spyOn(component, 'onWindowResize');

        pubsub.subscribe.and.callFake((name, channel, fn) => {
          callbackMethods[channel] = fn;
        });
      });

      it('should subscribe on ORIENTATION_CHANGED pubsub event for Native App', () => {
        component['device'].isMobile = true;

        component.ngOnInit();

        expect(pubsub.subscribe.calls.allArgs()[1]).toEqual(
          ['HomeScreenComponent', 'ORIENTATION_CHANGED', jasmine.any(Function)]
        );
      });

      it(`should call callback if ORIENTATION_CHANGED`, () => {
        component['device'].isMobile = true;

        component.ngOnInit();

        callbackMethods['ORIENTATION_CHANGED']({ isLandscape: true });

        expect(component.onWindowResize).toHaveBeenCalledTimes(2);
      });

      it(`should Not subscribe on ORIENTATION_CHANGED pubsub event for Native App`, () => {
        component['device'].isMobile = false;

        component.ngOnInit();

        callbackMethods['ORIENTATION_CHANGED']({
          orientation: {
            isLandscape: true
          }
        });
        expect(pubsub.subscribe.calls.allArgs()[2]).toBeUndefined();
        expect(component.onWindowResize).not.toHaveBeenCalled();
      });
    });

    describe('resize & orientationchange', () => {
      const callbacks = {};

      beforeEach(() => {
        component['device'].isMobile = true;

        spyOn(component, 'onWindowResize');
        rendererService.renderer.listen.and.callFake((el, event, cb) => callbacks[event] = cb);
      });

      it(`should run onWindowResize if resize`, () => {
        component.ngOnInit();

        callbacks['resize']();
        expect(component.onWindowResize).toHaveBeenCalledTimes(2);
      });

      it(`should run onWindowResize if orientationchange`, () => {
        component.ngOnInit();

        callbacks['orientationchange']();
        expect(component.onWindowResize).toHaveBeenCalledTimes(2);
      });
    });

    it(`should Not add resize listener if is Not Mobile`, () => {
      component.ngOnInit();

      expect(component.orientationChangeListener).toBeUndefined();
      expect(rendererService.renderer.listen.calls.allArgs()[component['events'].lengths]).toBeUndefined();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should remove listeners', () => {
      component.ngOnInit();
      component.ngOnDestroy();
      expect(pubsub.unsubscribe).toHaveBeenCalledWith('HomeScreenComponent');
      expect(component.listeners).toEqual([]);
    });

    it(`should remove orientationChangeListener`, () => {
      component['device'].isMobile = true;
      component.ngOnInit();

      spyOn(component, 'orientationChangeListener');

      component.ngOnDestroy();

      expect(component['orientationChangeListener']).toHaveBeenCalled();
    });
  });

  describe('#isLandscape', () => {
    it('should check if it is Landscape - isWrapper', () => {
      component['device'].isWrapper = true;
      component['device'].isAndroid = true;
      expect(component['isLandscape']).toBe(true);
    });

    it('should check if it is Landscape (orientation = 0)', () => {
      component['device'].isWrapper = false;
      component['device'].isAndroid = false;
      component['windowRef'].nativeWindow.orientation = 0;
      expect(component['isLandscape']).toBe(false);
    });

    it('should check if it is Landscape (orientation = 90)', () => {
      component['device'].isWrapper = false;
      component['device'].isAndroid = false;
      component['windowRef'].nativeWindow.orientation = 90;
      expect(component['isLandscape']).toBe(true);
    });
  });

  describe('#onWindowResize', () => {
    it('should call with addClass', () => {
      windowRef.nativeWindow.document.querySelector.and.callFake((selector: string) => {        
        if (selector === '.landscape-mobile-overlay') return 'querySelector_result';
        if (selector === '.snb-video-container') return false;
      });
      component['onWindowResize']();
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith('querySelector_result', 'landscape-mode');
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(windowRef.document.body, 'mobile-overlay-active');
      expect(windowRef.nativeWindow.document.activeElement.blur).toHaveBeenCalled();
    });

    it('should call with removeClass', () => {
      windowRef.nativeWindow.orientation = 0;
      component['onWindowResize']();
      expect(domTools.removeClass).toHaveBeenCalledWith('querySelector_result', 'landscape-mode');
      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(windowRef.document.body, 'mobile-overlay-active');
    });

    it('should call with removeClass when isLandscape = false and ither conditions=true', () => {
      windowRef.nativeWindow.orientation = 228;
      component['onWindowResize']();
      expect(domTools.removeClass).toHaveBeenCalledWith('querySelector_result', 'landscape-mode');
    });
  });
});
