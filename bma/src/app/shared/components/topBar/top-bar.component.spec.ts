import { TopBarComponent } from './top-bar.component';

describe('TopBarComponent', () => {
  let component: TopBarComponent;
  let localeService;
  let changeDetectorRef;
  let pubSubService;
  let domToolsService;
  let iObserverMock;
  let IntersectionObserverSpy;
  let elementRef;
  let seoDataService;

  beforeEach(() => {
    function setupIntersectionObserverMock({
      root = null,
      rootMargin = '',
      thresholds = [],
      callback = (...args) => {},
      disconnect = () => null,
      observe = () => null,
      takeRecords = () => [],
      unobserve = () => null,
    } = {}): void {
      class MockIntersectionObserver implements IntersectionObserver {
        readonly root: Element | null = root;
        readonly rootMargin: string = rootMargin;
        readonly thresholds: ReadonlyArray < number > = thresholds;
        callback: (...args) => {};
        disconnect: () => void = disconnect;
        observe: (target: Element) => void = observe;
        takeRecords: () => IntersectionObserverEntry[] = takeRecords;
        unobserve: (target: Element) => void = unobserve;
      }

      Object.defineProperty(
        window,
        'IntersectionObserver', {
          writable: true,
          configurable: true,
          value: MockIntersectionObserver
        }
      );

      Object.defineProperty(
        global,
        'IntersectionObserver', {
          writable: true,
          configurable: true,
          value: MockIntersectionObserver
        }
      );
    }
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('localizedString')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    pubSubService = {
      cbMap: {},
      subscribe: jasmine.createSpy('subscribe').and.callFake(function(name, method, cb) {pubSubService.cbMap[method] = cb}),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        PIN_TOP_BAR: 'PIN_TOP_BAR'
      }
    };
    seoDataService = {
      seoSubjObservable: {
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb && cb(true))
      }
    } as any;
    domToolsService = {
      getHeight: jasmine.createSpy('getHeight').and.callFake(el => el.height),
      HeaderEl: { height: 50 },
      ContentEl: { id: 'content' }
    };
    elementRef = {
      nativeElement: {
        height: 40,
        style: {},
        parentElement: {
          style: {}
        }
      }
    };
    iObserverMock = {
      callback: (...args) => {},
      observe: jasmine.createSpy('observe'),
      disconnect: jasmine.createSpy('disconnect')
    };
    setupIntersectionObserverMock();
    IntersectionObserverSpy = spyOn(window as any, 'IntersectionObserver').and.callFake(function(cb, options) {
      iObserverMock.callback = cb;
      return iObserverMock;
    });
    window.IntersectionObserver;

    component = new TopBarComponent(localeService, changeDetectorRef, pubSubService, domToolsService, elementRef, seoDataService);
    component.title = 'sb.title';
    component.path = '/pathMock';
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.ngOnInit();
    });
    it('should init properties and call detectChanges', () => {
      expect(component.linkPath).toEqual(component.path);
      expect(component.titleText).toEqual('localizedString');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should subscribe to PIN_TOP_BAR pubsub message', () => {
      expect(pubSubService.subscribe).toHaveBeenCalledWith('TopBarComponent', 'PIN_TOP_BAR', jasmine.any(Function));
    });
    it('should update true when observable returns true', () => {
      seoDataService.seoSubjObservable.subscribe.and.callFake(cb => cb & cb(true));
      expect(component.seoEnabledInCms).toBeTruthy();
    });
    it('should update true when observable returns false', () => {
      seoDataService.seoSubjObservable.subscribe.and.callFake(cb => cb & cb(false));
      component.ngOnInit();
      expect(component.seoEnabledInCms).toBeFalsy();
    });

    describe('on PIN_TOP_BAR pubsub message', () => {
      beforeEach(() => {
        spyOn(component as any, 'pinTopBar').and.callThrough();
        spyOn(component as any, 'unpinTopBar').and.callThrough();
      });
      it('should call pinTopBar if received true', () => {
        pubSubService.cbMap['PIN_TOP_BAR'](true);
        expect((component as any).pinTopBar).toHaveBeenCalled();
        expect((component as any).unpinTopBar).not.toHaveBeenCalled();
      });
      it('should call unpinTopBar if received false', () => {
        pubSubService.cbMap['PIN_TOP_BAR'](false);
        expect((component as any).unpinTopBar).toHaveBeenCalled();
        expect((component as any).pinTopBar).not.toHaveBeenCalled();
      });
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from pubsub PIN_TOP_BAR message and disconnect existing intersection observer', () => {
      spyOn(component as any, 'disconnectObserver').and.callThrough();
      (component as any).disconnectObserver();
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('TopBarComponent');
      expect((component as any).disconnectObserver).toHaveBeenCalled();
    });
  });

  describe('getPath', () => {
    it('should return set path', () => {
      expect(component.getPath()).toEqual('/pathMock');
    });

    it('should return empty path if no set', () => {
      component.path = undefined;

      expect(component.getPath()).toEqual('');
    });
  });

  describe('getText', () => {
    it('should localise title', () => {
      expect(component.getText()).toEqual('localizedString');
      expect(localeService.getString).toHaveBeenCalledWith('sb.title');
    });

    it('should bind title', () => {
      const title = 'some title';
      component.title = title;

      expect(component.getText()).toEqual(title);
      expect(localeService.getString).not.toHaveBeenCalledWith(title);
    });
  });

  it('titleClickHandler should handle title click', () => {
    component.titleFunc.emit = jasmine.createSpy('titleFunc.emit');

    expect(component.titleClickHandler()).toBeFalsy();
    expect(component.titleFunc.emit).toHaveBeenCalled();
  });

  it('backClickHandler should handle back button click', () => {
    component.backFunc.emit = jasmine.createSpy('backFunc.emit');

    component.backClickHandler();
    expect(component.backFunc.emit).toHaveBeenCalled();
  });

  describe('pinTopBar', () => {
    beforeEach(() => {
      spyOn(component as any, 'disconnectObserver').and.callThrough();
      (component as any).disconnectObserver();
      spyOn(component as any, 'createObserver').and.callThrough();
      (component as any).createObserver();
      (component as any).pinTopBar();
    });
    it('should get height of app header', () => {
      expect(domToolsService.getHeight.calls.allArgs()).toEqual([
        [{ height: 50 }], [elementRef.nativeElement]
      ]);
    });
    it('should disconnect old observer', () => {
      expect((component as any).disconnectObserver).toHaveBeenCalled();
    });
    it('should create new intersection observer and use the content element as target', () => {
      expect((component as any).createObserver).toHaveBeenCalledWith({ root: null, rootMargin: '-130px 0px 0px 0px', threshold: 0 });
      expect((component as any).iObserver).toEqual(iObserverMock);
      expect(iObserverMock.observe).toHaveBeenCalledWith({ id: 'content' });
    });
  });

  describe('unpinTopBar', () => {
    beforeEach(() => {
      spyOn(component as any, 'fixPosition').and.callThrough();
      (component as any).fixPosition();
      spyOn(component as any, 'disconnectObserver').and.callThrough();
      (component as any).disconnectObserver();
      (component as any).unpinTopBar();
    });
    it('should clear pinned state and disconnect observer', () => {
      expect((component as any).fixPosition).toHaveBeenCalledWith(false);
      expect((component as any).disconnectObserver).toHaveBeenCalled();
    });
  });

  describe('fixPosition', () => {
    it('should set fixed position and add padding-top to the parent', () => {
      (component as any).fixPosition(true);
      expect(elementRef.nativeElement.style.position).toEqual('fixed');
      expect(elementRef.nativeElement.parentElement.style.paddingTop).toEqual('40px');
    });
    describe('should reset position and padding-top of the parent', () => {
      it('(false provided)', () => {
        (component as any).fixPosition(false);
      });
      it('(by default)', () => {
        (component as any).fixPosition();
      });
      afterEach(() => {
        expect(elementRef.nativeElement.style.position).toEqual(null);
        expect(elementRef.nativeElement.parentElement.style.paddingTop).toEqual(null);
      });
    });
    afterEach(() => {
      expect(domToolsService.getHeight).toHaveBeenCalledWith(elementRef.nativeElement);
    });
  });

  describe('createObserver', () => {
    let result;
    beforeEach(() => {
      spyOn(component as any, 'fixPosition').and.callThrough();
      (component as any).fixPosition();
      result = (component as any).createObserver({ root: null });
    });
    it('should create Intersection Observer instance', () => {
      expect(IntersectionObserverSpy).toHaveBeenCalledWith(jasmine.any(Function), { root: null });
      expect(result).toEqual(iObserverMock);
    });
    it('on intersection event should fix position if isIntersecting', () => {
      iObserverMock.callback([{ isIntersecting: true }]);
      expect((component as any).fixPosition).toHaveBeenCalledWith(false);
    });
    describe('on intersection event should not fix position', () => {
      it('if not isIntersecting', () => {
        iObserverMock.callback([{ isIntersecting: false }]);
        expect((component as any).fixPosition).toHaveBeenCalledWith(true);
      });
      describe('(fallback values)', () => {
        it('intersection entries are empty', () => {
          iObserverMock.callback([]);
        });
        it('intersection entries are not defined', () => {
          iObserverMock.callback(undefined);
        });
        afterEach(() => {
          expect((component as any).fixPosition).toHaveBeenCalledWith(undefined);
        });
      });
    });
  });

  describe('disconnectObserver', () => {
    it('should disconnect existent observer', () => {
      (component as any).iObserver = iObserverMock;
      (component as any).disconnectObserver();
      expect(iObserverMock.disconnect).toHaveBeenCalled();
    });
    it('should do nothing if there is no existent observer', () => {
      (component as any).iObserver = null;
      (component as any).disconnectObserver();
    });
  });
});
