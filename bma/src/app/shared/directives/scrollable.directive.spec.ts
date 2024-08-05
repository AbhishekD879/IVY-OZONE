import { ScrollableDirective } from '@shared/directives/scrollable.directive';

describe('ScrollableDirective', () => {
  let directive: ScrollableDirective,
    rendererService,
    device,
    windowRef,
    storage,
    elementMock,
    el;

  beforeEach(() => {
    rendererService = {
      _listenMap: {},
      _unlistenMap: {},
      renderer: {
        listen: jasmine.createSpy('listen').and.callFake((elm, event, cb) => {
          rendererService._listenMap[event] = cb;
          rendererService._unlistenMap[event] = jasmine.createSpy(`unlisten${event}`);
          return rendererService._unlistenMap[event];
        })
      }
    };
    device = {};
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        document: { body: { tagName: 'body'} }
      }
    };
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    elementMock = {
      offsetWidth: 0,
      scrollLeft: 0,
      querySelector: jasmine.createSpy('querySelector').and.returnValue({
        offsetLeft: 0,
        offsetWidth: 0
      })
    };

    el = { nativeElement: elementMock };

    directive = new ScrollableDirective(rendererService, device, windowRef, storage, el);
  });

  it('should initialize elementData property', () => {
    expect((directive as any).elementData).toEqual({ isMouseDown: false, clientX: 0, scrollLeft: 0 });
  });

  it('unlisteners should not be defined', () => {
    expect((directive as any).scrollListener).not.toBeDefined();
    expect((directive as any).mouseEnterListener).not.toBeDefined();
    expect((directive as any).mouseDownListener).not.toBeDefined();
    expect((directive as any).mouseMoveListener).not.toBeDefined();
    expect((directive as any).mouseLeaveListener).not.toBeDefined();
    expect((directive as any).mouseUpListener).not.toBeDefined();
    expect((directive as any).dragStartListener).not.toBeDefined();
  });

  describe('@ngAfterViewInit', () => {
    beforeEach(() => {
      spyOn(directive as any, 'setScrollable');
      spyOn(directive as any, 'scrollToSelected');
      directive.ngAfterViewInit();
    });
    it('should set element property', () => {
      expect((directive as any).element).toEqual(elementMock);
    });
    it('should init scrolls on ngAfterViewInit', () => {
      expect((directive as any).setScrollable).toHaveBeenCalled();
      expect((directive as any).scrollToSelected).toHaveBeenCalled();
    });
  });

  describe('ngOnChanges', () => {
    let changes;
    beforeEach(() => {
      changes = { rescrollOnChange: { firstChange: false, currentValue: true } };
      spyOn(directive as any, 'scrollToSelected');
    });
    it('should reinit scroll ngOnChanges', () => {
      let timeoutCb = () => {};
      windowRef.nativeWindow.setTimeout.and.callFake(cb => timeoutCb = cb);
      directive.ngOnChanges(changes);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function));
      timeoutCb();
      expect((directive as any).scrollToSelected).toHaveBeenCalled();
    });

    describe('should not reinit scroll ngOnChanges', () => {
      it('no rescrollOnChange in changes', () => {
        delete changes.rescrollOnChange;
      });

      it('not first changes without value', () => {
        changes.rescrollOnChange.firstChange = true;
      });

      it('rescrollOnChange.currentValue is null', () => {
        changes.rescrollOnChange.currentValue = null;
      });
      afterEach(() => {
        directive.ngOnChanges(changes);
        expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      });
    });
  });

  describe('ngOnDestroy', () => {
    it('should call event unlisteners if available', () => {
      (directive as any).scrollListener = jasmine.createSpy('scrollListener');
      (directive as any).dragStartListener = jasmine.createSpy('dragStartListener');
      (directive as any).mouseDownListener = jasmine.createSpy('mouseDownListener');
      directive.ngOnDestroy();
      expect((directive as any).scrollListener).toHaveBeenCalled();
      expect((directive as any).dragStartListener).toHaveBeenCalled();
      expect((directive as any).mouseDownListener).toHaveBeenCalled();
    });
    it('should not call event unlisteners if unavailable', () => {
      const scrollListener = jasmine.createSpy('scrollListener').and.returnValue(null),
        dragStartListener = jasmine.createSpy('dragStartListener').and.returnValue(null),
        mouseDownListener = jasmine.createSpy('mouseDownListener').and.returnValue(null);
      Object.defineProperties(directive, {
        'scrollListener': { get: scrollListener },
        'dragStartListener': { get: dragStartListener },
        'mouseDownListener': { get: mouseDownListener }
      });
      directive.ngOnDestroy();
      expect(scrollListener).toHaveBeenCalled();
      expect(dragStartListener).toHaveBeenCalled();
      expect(mouseDownListener).toHaveBeenCalled();
    });
  });

  describe('scrollHandler', () => {
    it('should set scrollLeft value to storage', () => {
      (directive as any).element = { scrollLeft: 100 };
      (directive as any).scrollHandler();
      expect(storage.set).toHaveBeenCalledWith('scrollLeft', 100);
    });
  });

  describe('mouseMoveHandler', () => {
    beforeEach(() => {
      (directive as any).element = {};
      (directive as any).elementData = { isMouseDown: true, scrollLeft: 100, clientX: 30 };
    });
    it('should set scrollLeft value of element if mousedown', () => {
      (directive as any).mouseMoveHandler({ clientX: 20 } as any);
      expect((directive as any).element.scrollLeft).toEqual(100 + 30 - 20);
    });
    it('should not set scrollLeft value of element if not mousedown', () => {
      (directive as any).elementData.isMouseDown = false;
      (directive as any).mouseMoveHandler({ clientX: 20 } as any);
      expect((directive as any).element.scrollLeft).toEqual(undefined);
    });
  });

  describe('mouseEnterHandler', () => {
    describe('should set elementData properties', () => {
      beforeEach(() => {
        (directive as any).element = { scrollLeft: 30 };
      });
      it('when event is available', () => {
        (directive as any).mouseEnterHandler({ clientX: 20 } as any);
        expect((directive as any).elementData.clientX).toEqual(20);
      });
      it('when event is not available', () => {
        (directive as any).mouseEnterHandler(null);
        expect((directive as any).elementData.clientX).toEqual(null);
      });
      afterEach(() => {
        expect((directive as any).elementData.scrollLeft).toEqual(30);
      });
    });
  });

  describe('mouseLeaveHandler', () => {
    beforeEach(() => {
      (directive as any).isMouseDown = undefined;
      spyOn(directive as any, 'scrollHandler');
      (directive as any).mouseEnterListener = jasmine.createSpy('mouseEnterListener');
      (directive as any).mouseMoveListener = jasmine.createSpy('mouseMoveListener');
      (directive as any).mouseLeaveListener = jasmine.createSpy('mouseLeaveListener');
      (directive as any).mouseUpListener = jasmine.createSpy('mouseUpListener');
      (directive as any).mouseLeaveHandler();
    });

    it('should set elementData.isMouseDown property', () => {
      expect((directive as any).elementData.isMouseDown).toEqual(false);
    });
    it('should call scrollHandler', () => {
      expect((directive as any).scrollHandler).toHaveBeenCalled();
    });
    it('should call event unsubscribers', () => {
      expect((directive as any).mouseEnterListener).toHaveBeenCalled();
      expect((directive as any).mouseMoveListener).toHaveBeenCalled();
      expect((directive as any).mouseLeaveListener).toHaveBeenCalled();
      expect((directive as any).mouseUpListener).toHaveBeenCalled();
    });
  });

  describe('mouseDownHandler', () => {
    const event = Symbol('event'),
      element = Symbol('element');

    beforeEach(() => {
      (directive as any).isMouseDown = undefined;
      (directive as any).element = element;
      spyOn(directive as any, 'mouseEnterHandler');
      spyOn(directive as any, 'mouseMoveHandler');
      spyOn(directive as any, 'mouseLeaveHandler');

      (directive as any).mouseDownHandler(event);
    });

    it('should set elementData.isMouseDown property', () => {
      expect((directive as any).elementData.isMouseDown).toEqual(true);
    });
    it('should call mouseEnterHandler', () => {
      expect((directive as any).mouseEnterHandler).toHaveBeenCalledWith(event);
    });

    it('should subscribe on events', () => {
      expect(rendererService.renderer.listen.calls.allArgs()).toEqual([
        [element, 'mouseenter', jasmine.any(Function)],
        [element, 'mousemove', jasmine.any(Function)],
        [element, 'mouseleave', jasmine.any(Function)],
        [{ tagName: 'body' }, 'mouseup', jasmine.any(Function)]
      ]);
    });

    describe('should set unlistener', () => {
      it('for mouseenter event', () => {
        (directive as any).mouseEnterListener();
        expect(rendererService._unlistenMap['mouseenter']).toHaveBeenCalled();
      });
      it('for mousemove event', () => {
        (directive as any).mouseMoveListener();
        expect(rendererService._unlistenMap['mousemove']).toHaveBeenCalled();
      });
      it('for mouseleave event', () => {
        (directive as any).mouseLeaveListener();
        expect(rendererService._unlistenMap['mouseleave']).toHaveBeenCalled();
      });
      it('for mouseup event', () => {
        (directive as any).mouseUpListener();
        expect(rendererService._unlistenMap['mouseup']).toHaveBeenCalled();
      });
    });

    describe('should execute event handler', () => {
      it('on mouseenter event', () => {
        (directive as any).mouseEnterHandler.calls.reset();
        rendererService._listenMap['mouseenter'](event);
        expect((directive as any).mouseEnterHandler).toHaveBeenCalledWith(event);
      });
      it('on mousemove event', () => {
        rendererService._listenMap['mousemove'](event);
        expect((directive as any).mouseMoveHandler).toHaveBeenCalledWith(event);
      });
      it('on mouseleave event', () => {
        rendererService._listenMap['mouseleave'](event);
        expect((directive as any).mouseLeaveHandler).toHaveBeenCalledWith();
      });
      it('on mouseup event', () => {
        rendererService._listenMap['mouseup'](event);
        expect((directive as any).mouseLeaveHandler).toHaveBeenCalledWith();
      });
    });
  });

  describe('setScrollable', () => {
    const element = Symbol('element');
    let event;
    beforeEach(() => {
      (directive as any).element = element;
      event = { preventDefault: jasmine.createSpy('preventDefault') };
      spyOn(directive as any, 'mouseDownHandler');
      spyOn(directive as any, 'scrollHandler');
    });

    describe('if device.isMobileOrigin', () => {
      beforeEach(() => {
        device.isMobileOrigin = true;
        (directive as any).setScrollable();
      });

      it('should create scroll listener', () => {
        expect(rendererService.renderer.listen).toHaveBeenCalledWith(element, 'scroll', jasmine.any(Function));
      });
      it('should set scroll unlistener', () => {
        (directive as any).scrollListener();
        expect(rendererService._unlistenMap['scroll']).toHaveBeenCalled();
      });
      it('should call scrollHandler on scroll event', () => {
        rendererService._listenMap['scroll'](event);
        expect((directive as any).scrollHandler).toHaveBeenCalledWith();
      });

      afterEach(() => { expect(Object.keys(rendererService._listenMap)).toEqual(['scroll']); });
    });

    describe('if not device.isMobileOrigin', () => {
      beforeEach(() => {
        device.isMobileOrigin = false;
        (directive as any).setScrollable();
      });

      it('should create dragstart and mousedown listeners', () => {
        expect(rendererService.renderer.listen.calls.allArgs()).toEqual([
          [element, 'dragstart', jasmine.any(Function)],
          [element, 'mousedown', jasmine.any(Function)]
        ]);
      });

      it('should set dragstart unlistener', () => {
        (directive as any).dragStartListener();
        expect(rendererService._unlistenMap['dragstart']).toHaveBeenCalled();
      });
      it('should set mousedown unlistener', () => {
        (directive as any).mouseDownListener();
        expect(rendererService._unlistenMap['mousedown']).toHaveBeenCalled();
      });

      it('should call event.preventDefault on dragstart event', () => {
        rendererService._listenMap['dragstart'](event);
        expect(event.preventDefault).toHaveBeenCalledWith();
      });
      it('should call event.preventDefault on mousedown event', () => {
        rendererService._listenMap['mousedown'](event);
        expect((directive as any).mouseDownHandler).toHaveBeenCalledWith(event);
      });

      afterEach(() => { expect(Object.keys(rendererService._listenMap)).toEqual(['dragstart', 'mousedown']); });
    });
  });

  describe('scrollToSelected', () => {
    let activeElement;
    beforeEach(() => {
      activeElement = {
        offsetLeft: 100,
        offsetWidth: 20
      };
      (directive as any).element = {
        offsetWidth: 150,
        querySelector: jasmine.createSpy('querySelector').and.returnValue(activeElement)
      };
      storage.get.and.returnValue('50');
    });

    it('should return immediately if no .active element found', () => {
      (directive as any).element.querySelector.and.returnValue(null);
      (directive as any).scrollToSelected();
      expect((directive as any).element.scrollLeft).not.toBeDefined();
    });

    describe('should set element.scrollLeft to 0', () => {
      it('sum of .active scrollLeft and offsetWidth values is less than directive offsetWidth', () => {
        (directive as any).scrollToSelected();
      });
      it('.active scrollLeft is less than directive offsetWidth by more than 50px (if .acive offsetWidth is zero)', () => {
        activeElement.offsetWidth = undefined;
        activeElement.offsetLeft = 99;
        (directive as any).scrollToSelected();
      });
      afterEach(() => {
        expect((directive as any).element.scrollLeft).toEqual(0);
      });
    });
    it('should set element.scrollLeft to value from local storage', () => {
      activeElement.offsetWidth = 50;
      activeElement.offsetLeft = 120;
      (directive as any).scrollToSelected();
      expect((directive as any).element.scrollLeft).toEqual(50);
    });
    it('should set element.scrollLeft to offsetLeft value of .active element', () => {
      // Wrong condition coverage case - should be removed when fixed
      storage.get.and.returnValue('180');
      activeElement.offsetWidth = 50;
      activeElement.offsetLeft = 120;
      (directive as any).scrollToSelected();
      expect((directive as any).element.scrollLeft).toEqual(120);
    });
    it('should set element.scrollLeft to offsetLeft value of .active element', () => {
      storage.get.and.returnValue(null);
      activeElement.offsetWidth = 50;
      activeElement.offsetLeft = 120;
      (directive as any).scrollToSelected();
      expect((directive as any).element.scrollLeft).toEqual(120);
    });

    afterEach(() => {
      expect((directive as any).element.querySelector).toHaveBeenCalledWith('.active');
    });
  });
});
