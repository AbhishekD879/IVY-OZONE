import { OptaScoreboardComponent } from './opta-scoreboard.component';
import { fakeAsync } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('OptaScoreboardComponent', () => {
  let component: OptaScoreboardComponent;
  let elementRef;
  let gtmService;
  let pubSubService;
  let ngZone;
  let elementMock;
  let windowRefService;
  let rendererService;
  let optaScoreboardOverlayService;

  beforeEach(fakeAsync(() => {
    elementRef = {
      nativeElement: {
        append: jasmine.createSpy('nativeElement'),
        appendChild: jasmine.createSpy('appendChild')
      }
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
      subscribe: jasmine.createSpy('publish')
    };
    ngZone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular')
    };

    elementMock = {
      elMap: [],
      create: (tagName, attributes = {}) => {
        const el = {
          tagName: tagName,
          _eventListenersMap: {},
          addEventListener: jasmine.createSpy('addEventListener').and.callFake((e, cb) => {
            el._eventListenersMap[e] = cb;
          }),
          attributes: attributes,
          querySelector: jasmine.createSpy(),
          appendChild: jasmine.createSpy('appendChild'),
          setAttribute: jasmine.createSpy('setAttribute').and.callFake((attrName, attrValue) => el.attributes[attrName] = attrValue),
          getAttribute: jasmine.createSpy('getAttribute').and.callFake(attrName => el.attributes[attrName]),
          remove: jasmine.createSpy('remove'),
        };
        elementMock.elMap.push(el);
        return el;
      }
    };

    windowRefService = {
      document: {
        querySelector: jasmine.createSpy(),
        createElement: jasmine.createSpy().and.callFake(tagName => elementMock.create(tagName)),
        body: {
          appendChild: jasmine.createSpy('appendChild'),
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      },
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('renderer.listen')
      }
    };
    optaScoreboardOverlayService = {
      hideOverlay: jasmine.createSpy('hideOverlay'),
      showOverlay: jasmine.createSpy('showOverlay'),
      initOverlay: jasmine.createSpy('initOverlay')
        .and.callFake(() => elementMock.create('scoreboard-overlay', { 'sb-data': '{ "matchId": 123 }' }))
    };

    component = new OptaScoreboardComponent(
      elementRef,
      gtmService,
      pubSubService,
      ngZone,
      windowRefService,
      rendererService,
      optaScoreboardOverlayService
    );
    component.event = { id: 123, categoryCode: 16 } as any;
  }));

  describe('setParameters', () => {
    let element;
    beforeEach(() => {
      (component as any).eventId = 123;
      element = elementMock.create('div');
    });

    it('should set stringified JSON to sb-data attribute of element', () => {
      (component as any).setParameters(element);
      expect(element.setAttribute).toHaveBeenCalledWith('sb-data',
        '{"matchId":123,"env":"prod","sport":16,"provider":"digital"}');
    });
    it('should set stringified JSON updated with optional properties to sb-data attribute of element', () => {
      (component as any).setParameters(element, { matchId: 456, property: 'value'});
      expect(element.setAttribute).toHaveBeenCalledWith('sb-data',
        '{"matchId":456,"env":"prod","sport":16,"provider":"digital","property":"value"}');
    });
  });

  describe('@getParameters', () => {
    let element;

    it('if element does not have sb-data attribute, should return empty object', () => {
      element = elementMock.create('div');
      const result = (component as any).getParameters(element);
      expect(result).toEqual({});
    });

    it('if element has JSON data in sb-data attribute, should return it contents parsed', () => {
      element = elementMock.create('div', {'sb-data': '{"foo":"bar"}'});
      const result = (component as any).getParameters(element);
      expect(result).toEqual({ foo: 'bar' });
    });

    it('if element has non-JSON string in sb-data attribute, should return empty object', () => {
      element = elementMock.create('div', {'sb-data': 'foobar'});
      const result = (component as any).getParameters(element);
      expect(result).toEqual({});
    });

    it('if element has non-object JSON data in sb-data attribute, should return empty object', () => {
      element = elementMock.create('div', {'sb-data': '"foobar"'});
      const result = (component as any).getParameters(element);
      expect(result).toEqual({});
    });
  });

  it('showScoreboardOverlayFn', () => {
    (component as any).scoreboardOverlay = elementMock.create('scoreboard-overlay');
    spyOn(component as any, 'setParameters').and.callThrough();
    (component as any).showScoreboardOverlayFn({ detail: { scoreboardKey: 'key' } } as any);
    expect((component as any).setParameters).toHaveBeenCalledWith((component as any).scoreboardOverlay, { overlayKey: 'key' });
    expect(optaScoreboardOverlayService.showOverlay).toHaveBeenCalled();
  });

  it('hideOptaScoreboardHandlerFn', () => {
    (component as any).hideOptaScoreboardHandlerFn();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.HIDE_OPTA_SCOREBOARD);
  });

  describe('initializeScoreboards', () => {
    beforeEach(() => {
      spyOn(component as any, 'setParameters').and.callThrough();
      spyOn(component as any, 'getParameters').and.callThrough();
      spyOn(component as any, 'createOverlayWrapper').and.returnValue({} as any);
      spyOn(component as any, 'getOverlayWrapper').and.returnValue({test: '123', querySelector: () =>  {return {addEventListener: ()=> 'sample2'};}} as any);
    });
    describe('for scoreboard-container', () => {
      beforeEach(() => {
        (component as any).initializeScoreboards();
      });
      it('should create element', () => {
        expect(windowRefService.document.createElement).toHaveBeenCalledWith('scoreboard-container');
        expect((component as any).scoreboardContainer).toBe(elementMock.elMap[0]);
        expect((component as any).scoreboardContainer.tagName).toEqual('scoreboard-container');
      });
      it('should set attributes to scoreboard-container', () => {
        expect((component as any).setParameters).toHaveBeenCalledWith(elementMock.elMap[0]);
      });
      it('should add scoreboard-container event listeners', () => {
        expect(elementMock.elMap[0].addEventListener)
          .toHaveBeenCalledWith('showScoreboardOverlay', (component as any).showScoreboardOverlayFn);
        expect(elementMock.elMap[0].addEventListener)
          .toHaveBeenCalledWith('hideScoreboardComponent', (component as any).hideOptaScoreboardHandlerFn);
        expect(elementMock.elMap[0].addEventListener)
          .toHaveBeenCalledWith('googleAnalyticsData', (component as any).gtmHandlerFn, true);
      });

      it('should append scoreboard-container to elementRef', () => {
        expect(elementRef.nativeElement.appendChild).toHaveBeenCalledWith(elementMock.elMap[0]);
      });
    });

    describe('for scoreboard-overlay', () => {
      it('should get element reference from OptaScoreboardOverlayService', () => {
        (component as any).initializeScoreboards();
        expect(optaScoreboardOverlayService.initOverlay).toHaveBeenCalled();
        expect((component as any).scoreboardOverlay).toBe(elementMock.elMap[1]);
        expect((component as any).scoreboardOverlay.tagName).toEqual('scoreboard-overlay');
      });
      it('should get parameters of its element', () => {
        (component as any).initializeScoreboards();
        expect((component as any).getParameters).toHaveBeenCalledWith(elementMock.elMap[1]);
      });
      it('should update parameters of its element if matchId does not equal current eventId', () => {
        (component as any).eventId = 456;
        (component as any).initializeScoreboards();
        expect((component as any).setParameters).toHaveBeenCalledWith(elementMock.elMap[1]);
      });
      it('should not update parameters of its element if matchId equals current eventId', () => {
        (component as any).eventId = 123;
        (component as any).initializeScoreboards();
        expect((component as any).setParameters).not.toHaveBeenCalledWith(elementMock.elMap[1]);
      });
    });
  });

  describe('gtmHandlerFn', () => {
    const event = { detail: '' };
    beforeEach(() => {
      spyOn(component.isLoaded, 'emit');
    });

    it('should track event', () => {
      (component as any).gtmHandlerFn(event);
      expect((component as any).gtmService.push).toHaveBeenCalledWith('trackEvent', event.detail);
    });

    it(`should emit 'isLoaded' if 'isLoadedValue' is Falthy`, () => {
      (component as any).isLoadedValue = false;
      (component as any).gtmHandlerFn(event);
      expect(component.isLoaded.emit).toHaveBeenCalledWith(true);
      expect((component as any).isLoadedValue).toBeTruthy();
    });

    it(`should Not emit 'isLoaded' if 'isLoadedValue' is Truthy`, () => {
      (component as any).isLoadedValue = true;
      (component as any).gtmHandlerFn(event);
      expect(component.isLoaded.emit).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from windowOrientationChangeListener if exists', () => {
      (component as any).windowOrientationChangeListener = jasmine.createSpy('windowOrientationChangeListener');
      component.ngOnDestroy();
      expect((component as any).windowOrientationChangeListener).toHaveBeenCalledTimes(1);
    });

    it('should remove scoreboardContainer if exists', () => {
      (component as any).scoreboardContainer = { remove: jasmine.createSpy('remove') } as any;
      component.ngOnDestroy();
      expect((component as any).scoreboardContainer.remove).toHaveBeenCalled();
    });

    it('should hide scoreboardOverlay', () => {
      component.ngOnDestroy();
      expect(optaScoreboardOverlayService.hideOverlay).toHaveBeenCalled();
    });

    it('should clear update carousel timeout', () => {
      (component as any).updateCarouselTimer = 100;
      component.ngOnDestroy();
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(100);
    });

    it('should pass', () => {
      (component as any).windowOrientationChangeListener = null;
      (component as any).scoreboardContainer = null;
      (component as any).updateCarouselTimer = null;
      component.ngOnDestroy();
      expect(windowRefService.nativeWindow.clearTimeout).not.toHaveBeenCalled();
    });

    it('should call removeEventListener if scoreboardOverlayWrapper is present and contains is true', () => {
      component['scoreboardOverlayWrapper'] = {
        classList: {
          add: jasmine.createSpy(),
          remove: jasmine.createSpy(),
          contains: jasmine.createSpy().and.returnValue(true)
        },
        className: 'x y z'
      } as any;
      component['scoreboardOverlay'] = { removeEventListener: jasmine.createSpy() } as any;
      (component as any).windowOrientationChangeListener = null;
      (component as any).scoreboardContainer = null;
      (component as any).updateCarouselTimer = null;
      component.ngOnDestroy();
      expect(component['scoreboardOverlayWrapper'].classList.remove).toHaveBeenCalled();
    });

    it('should call removeEventListener if scoreboardOverlayWrapper is present and contains is false', () => {
      component['scoreboardOverlayWrapper'] = {
        classList: {
          add: jasmine.createSpy(),
          remove: jasmine.createSpy(),
          contains: jasmine.createSpy().and.returnValue(false)
        },
        className: 'x y z'
      } as any;
      component['scoreboardOverlay'] = { removeEventListener: jasmine.createSpy() } as any;
      (component as any).windowOrientationChangeListener = null;
      (component as any).scoreboardContainer = null;
      (component as any).updateCarouselTimer = null;
      component.ngOnDestroy();
      expect(component['scoreboardOverlay'].removeEventListener).toHaveBeenCalled();
    });
  });

  describe('ngOnChanges', () => {
    let changes;

    describe('should not set timeout', () => {
      it('for update carousel when previous value is false', () => {
        changes = { toggleScoreboard: { previousValue: false, currentValue: true } };
      });
      it('if changes object do not contain toggleScoreboard item', () => {
        changes = {} as any;
      });
      it('for update carousel when current value is true', () => {
        changes = { toggleScoreboard: { previousValue: true, currentValue: true } };
      });

      afterEach(() => {
        component.ngOnChanges(changes);
        expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalled();
      });
    });

    describe('should set timeout ', () => {
      beforeEach(() => {
        changes = { toggleScoreboard: { previousValue: true, currentValue: false } };
      });
      it('for update carousel when values are met', () => {
        component.ngOnChanges(changes);
        expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 500);
      });

      it('and call function in callback', () => {
        const scoreboardContainer = { carousel: { updateCarousel: jasmine.createSpy('updateCarousel') } } as any;
        let setTimeoutCb = () => {};

        windowRefService.nativeWindow.setTimeout.and.callFake(c => setTimeoutCb = c);
        (component as any).scoreboardContainer = scoreboardContainer;
        component.ngOnChanges(changes);

        setTimeoutCb();
        expect(scoreboardContainer.carousel.updateCarousel).toHaveBeenCalled();
      });
    });
  });

  describe('ngAfterViewInit', () => {
    it(`should publish SCOREBOARD_VISUALIZATION_LOADED event`, () => {
      component.ngAfterViewInit();
      expect(pubSubService.publish).toHaveBeenCalled();
    });
  });

  describe('ngOnInit', () => {
    let ngZoneCb = () => {};
    beforeEach(() => {
      ngZone.runOutsideAngular.and.callFake(cb => ngZoneCb = cb);
      component.ngOnInit();
    });

    it('should set eventId', () => {
      expect((component as any).eventId).toEqual(123);
    });
    it('should execute runOutsideAngular with callback', () => {
      expect(ngZone.runOutsideAngular).toHaveBeenCalledWith(jasmine.any(Function));
    });

    describe('runOutsideAngular callback', () => {
      const unlistenFn = Symbol('unlistenFn');
      beforeEach(() => {
        rendererService.renderer.listen.and.returnValue(unlistenFn);
        component['initializeScoreboards'] = jasmine.createSpy('initializeScoreboards');
        ngZoneCb();
      });

      it('should listen to orientation change', () => {
        expect((component as any).windowOrientationChangeListener).toEqual(unlistenFn);
        expect(rendererService.renderer.listen).toHaveBeenCalledWith(
          windowRefService.nativeWindow, 'orientationchange', (component as any).updateCarousel);
      });

      it('should initialize scoreboards', () => {
        expect((component as any).initializeScoreboards).toHaveBeenCalled();
      });
    });
  });

  describe('#getOverlayWrapper', () => {
    it('should return el when windowRefService is not null', () => {
      windowRefService.document.querySelector.and.returnValue(windowRefService.document.createElement('scoreboard-container'));
      component['getOverlayWrapper'](12, '');
      expect(windowRefService.document.querySelector).toHaveBeenCalled();
    });

    it('should call createOverlayWrapper when windowRefService is null', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      component['getOverlayWrapper'](123, '');
      expect(windowRefService.document.createElement).toHaveBeenCalled();
    });
  });

  describe('#scoreboardHandlerFn', () => {
    it('should call setParameters method', () => {
      component['scoreboardOverlayWrapper'] = {
        classList: {
          add: jasmine.createSpy(),
          remove: jasmine.createSpy(),
          contains: jasmine.createSpy().and.returnValue(true)
        },
        className: 'x y z'
      } as any;
      component['setParameters'] = jasmine.createSpy('setParameters');
      component['scoreboardHandlerFn']({ detail: { scoreboardKey: '1f2' } });
      expect(component['setParameters']).toHaveBeenCalled();
    });
  });

  describe('#overlayHandlerFn', () => {
    it('should call pubsub publish', () => {
      component['scoreboardOverlayWrapper'] = {
        classList: {
          add: jasmine.createSpy(),
          remove: jasmine.createSpy(),
          contains: jasmine.createSpy().and.returnValue(true)
        },
        className: 'x y z'
      } as any;
      component['overlayHandlerFn']();
      expect(component['scoreboardOverlayWrapper'].classList.remove).toHaveBeenCalled();
    });
  });
});
