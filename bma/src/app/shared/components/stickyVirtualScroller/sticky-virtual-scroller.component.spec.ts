import { of as observableOf } from 'rxjs';
import { fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';
import { StickyVirtualScrollerComponent } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.component';

describe('#StickyVirtualScrollerComponent', () => {
  let component: StickyVirtualScrollerComponent;
  let stickyScrollService,
    domToolsService,
    windowRef,
    rendererService,
    element,
    cmsService,
    deviceService;

  beforeEach(fakeAsync(() => {
    stickyScrollService = {
      updateScrollDimensions$: observableOf(null),
      updateScrollVisibility$: observableOf(null),
      scrollInfo: {},
      initialScrollDimensions: {},
      handleStickHeaderPosition: jasmine.createSpy('handleStickHeaderPosition'),
      setScrollInfo: jasmine.createSpy('setScrollInfo'),
      scrollBy: jasmine.createSpy('scrollBy'),
      calculateInitialScrollDimensions: jasmine.createSpy('calculateInitialScrollDimensions'),
      isSuspended: true
    };

    domToolsService = {
      getOuterHeight: jasmine.createSpy('getOuterHe ight').and.returnValue(0),
      css: jasmine.createSpy('css'),
      getElementTopPosition: jasmine.createSpy('getElementTopPosition').and.returnValue(100),
      getElementBottomPosition: jasmine.createSpy('getElementBottomPosition').and.returnValue(200),
      getParentByLevel: jasmine.createSpy('getParentByLevel').and.returnValue({
        previousSibling: {
          nodeName: 'nodeName'
        },
        parentElement: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue('parentElement_querySelector')
        }
      })
    };

    windowRef = {
      nativeWindow: {
        scrollBy: jasmine.createSpy('scrollBy'),
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb, time) => {
          cb();
        })
      }
    };

    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue('listener'),
      }
    };

    element = {
      nativeElement: {
        tagName: 'tagName',
        querySelector: jasmine.createSpy('querySelector'),
        parentNode: {
          querySelector: jasmine.createSpy('querySelector')
        }
      }
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))
    };

    deviceService = {};

    component = new StickyVirtualScrollerComponent(
      stickyScrollService,
      domToolsService,
      windowRef,
      rendererService,
      element,
      cmsService,
      deviceService
    );
    component['scrollableContaierElementRef'] = {
      nativeElement: {}
    };
  }));

  it('constructor', fakeAsync(() => {
    expect(component).toBeTruthy();
    component['toggleVisibility'].emit = jasmine.createSpy('toggleVisibility.emit');
    component['setScrollInfo'] = jasmine.createSpy('setScrollInfo');
    component['toggleVisibilityDebounced'](true, false);
    tick(2000);
    expect(component['toggleVisibility'].emit).toHaveBeenCalledWith({ visible: true, reloadData: false });
    discardPeriodicTasks();
  }));

  it('#ngOnInit', fakeAsync(() => {
    cmsService.getSystemConfig.and.returnValue(observableOf({
      VirtualScrollConfig: {
        enabled: false,
        iOSInnerScrollEnabled: false,
        androidInnerScrollEnabled: false
      }
    }));
    component['calculateScrollDimensions'] = jasmine.createSpy('calculateScrollDimensions');
    component.ngOnInit();
    tick(200);
    expect(component['updateScrollDimensionsSubscription']).toBeDefined();
    expect(component['updateScrollVisibilitySubscription']).toBeDefined();
    discardPeriodicTasks();
  }));

  it('#ngOnInit if no scroll info', fakeAsync(() => {
    cmsService.getSystemConfig.and.returnValue(observableOf({
      VirtualScrollConfig: {
        enabled: false,
        iOSInnerScrollEnabled: false,
        androidInnerScrollEnabled: false
      }
    }));
    component['calculateScrollDimensions'] = jasmine.createSpy('calculateScrollDimensions');
    component['setScrollInfo'] = jasmine.createSpy('setScrollInfo');
    stickyScrollService.scrollInfo = undefined;
    component.ngOnInit();
    tick(200);
    expect(component['setScrollInfo']).toHaveBeenCalled();
    expect(component['calculateScrollDimensions']).toHaveBeenCalled();
    expect(stickyScrollService.handleStickHeaderPosition).toHaveBeenCalled();
    discardPeriodicTasks();
  }));

  describe('#ngOnInit get VirtualScrollConfig', () => {
    it('virtual scroll disabled', fakeAsync(() => {
      Object.defineProperty(deviceService, 'isIos', { value: false });
      Object.defineProperty(deviceService, 'isAndroid', { value: false });
      cmsService.getSystemConfig.and.returnValue(observableOf({
        VirtualScrollConfig: {
          enabled: false,
          iOSInnerScrollEnabled: false,
          androidInnerScrollEnabled: false
        }
      }));
      component.ngOnInit();
      tick(200);
      expect(component['isIOsEnabled']).toBeFalsy();
      expect(component['isAndroidEnabled']).toBeFalsy();
      discardPeriodicTasks();
    }));

    it('virtual scroll enabled', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        VirtualScrollConfig: {
          enabled: true,
          iOSInnerScrollEnabled: false,
          androidInnerScrollEnabled: false
        }
      }));
      component.ngOnInit();
      tick(200);
      expect(component['isIOsEnabled']).toBeFalsy();
      expect(component['isAndroidEnabled']).toBeFalsy();
      discardPeriodicTasks();
    }));

    it('virtual scroll enabled and device scroll disabled', fakeAsync(() => {
      Object.defineProperty(deviceService, 'isIos', { value: false });
      Object.defineProperty(deviceService, 'isAndroid', { value: false });

      cmsService.getSystemConfig.and.returnValue(observableOf({
        VirtualScrollConfig: {
          enabled: true,
          iOSInnerScrollEnabled: true,
          androidInnerScrollEnabled: true
        }
      }));
      component.ngOnInit();
      tick(200);
      expect(component['isIOsEnabled']).toBeFalsy();
      expect(component['isAndroidEnabled']).toBeFalsy();
      discardPeriodicTasks();
    }));

    it('virtual scroll enabled and device scroll enabled', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        VirtualScrollConfig: {
          enabled: true,
          iOSInnerScrollEnabled: true,
          androidInnerScrollEnabled: true
        }
      }));
      Object.defineProperty(deviceService, 'isIos', { value: true });
      Object.defineProperty(deviceService, 'isAndroid', { value: true });
      component.ngOnInit();
      tick(200);
      expect(component['isIOsEnabled']).toBeTruthy();
      expect(component['isAndroidEnabled']).toBeTruthy();
      discardPeriodicTasks();
    }));
  });

  describe('ngOnDestroy', () => {
    beforeEach(() => {
      component['calculateScrollDimensions'] = jasmine.createSpy('calculateScrollDimensions');
      component['updateScrollDimensionsSubscription'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
      component['updateScrollVisibilitySubscription'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
    });

    it('ngOnDestroy when no listeners', fakeAsync(() => {
      component.ngOnDestroy();
      tick(200);
      expect(component['updateScrollDimensionsSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['updateScrollVisibilitySubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['visible']).toEqual(false);
      discardPeriodicTasks();
    }));

    it('ngOnDestroy when listeners are present', fakeAsync(() => {
      component['windowScroll'] = jasmine.createSpy('windowScroll');
      component['touchStart'] = jasmine.createSpy('touchStart');
      component['touchEnd'] = jasmine.createSpy('touchEnd');
      component['updateScrollDimensionsSubscription'].unsubscribe = jasmine.createSpy('unsubscribe');
      component['updateScrollVisibilitySubscription'].unsubscribe = jasmine.createSpy('unsubscribe');
      component.ngOnDestroy();
      tick(200);
      expect(component['updateScrollDimensionsSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['updateScrollVisibilitySubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['windowScroll']).toHaveBeenCalled();
      expect(component['touchStart']).toHaveBeenCalled();
      expect(component['touchEnd']).toHaveBeenCalled();
      expect(component['visible']).toEqual(false);
      discardPeriodicTasks();
    }));

    it('wasSticked when isSticked', fakeAsync(() => {
      component['scrollInfo'] = {
        isSticked: true
      } as any;
      component.ngOnDestroy();
      tick(200);

      expect(stickyScrollService.wasSticked).toBeTruthy();
      discardPeriodicTasks();
    }));

    it('when isSticked', fakeAsync(() => {
      component['scrollInfo'] = {
        isSticked: false
      } as any;
      component.ngOnDestroy();
      tick(200);

      expect(stickyScrollService.wasSticked).toBeFalsy();
      discardPeriodicTasks();
    }));

    it('when isSticked', fakeAsync(() => {
      component['scrollInfo'] = null;
      component.ngOnDestroy();
      tick(200);

      expect(stickyScrollService.wasSticked).toBeFalsy();
      discardPeriodicTasks();
    }));
  });

  describe('#scrollVisibilityHandler', () => {
    it('sholud call scrollVisibilityHandler when scroll is suspended', () => {
      component['visible'] = true;
      stickyScrollService.isSuspended = false;
      component['scrollDimensions'] = {
        documentHeight: 200,
        footerMenuHeight: 100
      } as any;
      component['toggleVisibilityDebounced'] = jasmine.createSpy('toggleVisibilityDebounced');
      component.scrollVisibilityHandler(true);

      expect(component['visible']).toEqual(false);
      expect(component['toggleVisibilityDebounced']).toHaveBeenCalledWith(false, true);
    });

    it('sholud call scrollVisibilityHandler method with reload data', () => {
      component['visible'] = true;
      component['toggleVisibilityDebounced'] = jasmine.createSpy('toggleVisibilityDebounced');
      component.scrollVisibilityHandler(true);

      expect(component['visible']).toEqual(true);
      expect(component['toggleVisibilityDebounced']).not.toHaveBeenCalled();
    });

    it('sholud call scrollVisibilityHandler method with reload data', () => {
      component['scrollDimensions'] = {
        scrollableMaxPosition: 0,
        footerMenuHeight: 0
      } as any;
      component['visible'] = false;
      stickyScrollService.isSuspended = false;

      component['toggleVisibilityDebounced'] = jasmine.createSpy('toggleVisibilityDebounced');
      component.scrollVisibilityHandler(true);

      expect(component['toggleVisibilityDebounced']).not.toHaveBeenCalled();
    });

    it('sholud call scrollVisibilityHandler method without reload data', () => {
      component['visible'] = false;
      stickyScrollService.isSuspended = false;
      component['toggleVisibilityDebounced'] = jasmine.createSpy('toggleVisibilityDebounced');
      component['scrollDimensions'] = {
        scrollableHeight: 100,
        scrollableMaxPosition: 100,
        documentHeight: 1000,
        footerMenuHeight: 100
      } as any;
      component.scrollVisibilityHandler(false);

      expect(component['visible']).toEqual(true);
      expect(component['toggleVisibilityDebounced']).toHaveBeenCalledWith(true, false);
    });

    describe('#should call prefetchNext', () => {
      beforeEach(() => {
        component['visible'] = false;
        stickyScrollService.isSuspended = false;
        component['scrollDimensions'] = {
          scrollableHeight: 100,
          scrollableMaxPosition: 100,
          documentHeight: 1000,
          footerMenuHeight: 100
        } as any;
        component['preFetchNext'].emit = jasmine.createSpy('preFetchNext.emit');
      });

      it('should call prefetchNext when scrolling up', () => {
        component['scrollEnabled'] = true;
        component['lastScrollableTopPosition'] = 200;
        component.scrollVisibilityHandler(true);

        expect(component.preFetchNext.emit).toHaveBeenCalledWith(true);
      });

      it('should call prefetchNext when scrolling up or forcePrefetch', () => {
        component['scrollEnabled'] = true;
        component['lastScrollableTopPosition'] = 200;
        component.scrollVisibilityHandler(true, true);

        expect(component.preFetchNext.emit).toHaveBeenCalledWith(true);
      });

      it('should not call prefetchNext when scrolling down', () => {
        component['scrollEnabled'] = true;
        component['lastScrollableTopPosition'] = 50;
        component.scrollVisibilityHandler(true);

        expect(component.preFetchNext.emit).not.toHaveBeenCalled();
      });

      it('should call prefetchNext when forcePrefetch', () => {
        component['scrollEnabled'] = true;
        component['lastScrollableTopPosition'] = 50;
        component.scrollVisibilityHandler(true, true);

        expect(component.preFetchNext.emit).toHaveBeenCalled();
      });

      it('should not call prefetchNext when scrollEnabled = false and scrolling up', () => {
        component['scrollEnabled'] = false;
        component['lastScrollableTopPosition'] = 200;
        component.scrollVisibilityHandler(true);

        expect(component.preFetchNext.emit).not.toHaveBeenCalled();
      });

      it('should not call prefetchNext when scrollEnabled = false and scrolling down', () => {
        component['scrollEnabled'] = false;
        component['lastScrollableTopPosition'] = 50;
        component.scrollVisibilityHandler(true);

        expect(component.preFetchNext.emit).not.toHaveBeenCalled();
      });
    });
  });

  describe('#touchEndHandler', () => {
    it('should call touchEndHandler when scroll is suspended', () => {
      stickyScrollService.isSuspended = true;
      component.touchEndHandler({} as any);

      expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalled();
    });

    it('should call touchEndHandler when scroll is not enabled', () => {
      stickyScrollService.isSuspended = false;
      component['scrollEnabled'] = false;
      component['scrollableElement'] = {} as any;
      component.touchEndHandler({
        changedTouches: [{
          clientY: 1
        }]
      } as any);

      expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalledWith({});
      expect(domToolsService.getElementTopPosition).not.toHaveBeenCalled();
    });

    it('should call touchEndHandler when not scrolled', () => {
      domToolsService.getElementTopPosition.and.returnValue(0);
      stickyScrollService.isSuspended = false;
      component['scrollEnabled'] = true;
      component['scrollableElement'] = {} as any;
      component['touchStartPosition'] = 10;
      component['scrollDimensions'] = {
        scrollableMaxPosition: 110
      } as any;
      component.touchEndHandler({
        changedTouches: [{
          clientY: 20
        }]
      } as any);

      expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalled();
      expect(domToolsService.getElementTopPosition).toHaveBeenCalledWith({});
    });

    describe('#inner scroll (isBelowSticky && isScrollingUp)', () => {
      beforeEach(() => {
        stickyScrollService.isSuspended = false;
        component['scrollEnabled'] = true;
        component['scrollableElement'] = {} as any;
        component['touchStartPosition'] = 20;
        component['scrollDimensions'] = {
          scrollableMaxPosition: 10
        } as any;
      });

      it('should not scroll', () => {
        domToolsService.getElementTopPosition.and.returnValue(0);
        component.touchEndHandler({
          changedTouches: [{
            clientY: 30
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalled();
      });

      it('should scroll when isIOsEnabled', () => {
        component['isIOsEnabled'] = true;
        component['isAndroidEnabled'] = false;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 10
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, 90);
      });
      it('should scroll when isAndroidEnabled', () => {
        component['isIOsEnabled'] = false;
        component['isAndroidEnabled'] = true;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 10
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, 90);
      });
      it('should scroll when isAndroidEnabled or isIOsEnabled', () => {
        component['isIOsEnabled'] = true;
        component['isAndroidEnabled'] = true;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 10
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, 90);
      });
      it('should not scroll when inner scroll disabled', () => {
        component['isIOsEnabled'] = false;
        component['isAndroidEnabled'] = false;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 10
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalledWith(0, 90);
      });
    });

    describe('#inner scroll (isAboveSticky && isScrollingDown)', () => {
      beforeEach(() => {
        stickyScrollService.isSuspended = false;
        component['scrollEnabled'] = true;
        component['scrollableElement'] = {} as any;
        component['touchStartPosition'] = 10;
        component['scrollDimensions'] = {
          scrollableMaxPosition: 110
        } as any;
      });
      it('should scroll when isIOsEnabled', () => {
        component['isIOsEnabled'] = true;
        component['isAndroidEnabled'] = false;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 20
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, -10);
      });
      it('should scroll when isAndroidEnabled', () => {
        component['isIOsEnabled'] = false;
        component['isAndroidEnabled'] = true;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 20
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, -10);
      });
      it('should scroll when isAndroidEnabled or isIOsEnabled', () => {
        component['isIOsEnabled'] = true;
        component['isAndroidEnabled'] = true;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 20
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, -10);
      });
      it('should not scroll when inner scroll disabled', () => {
        component['isIOsEnabled'] = false;
        component['isAndroidEnabled'] = false;
        component.touchEndHandler({
          changedTouches: [{
            clientY: 20
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalledWith(0, -10);
      });


      it('should not scroll', () => {
        domToolsService.getElementTopPosition.and.returnValue(140);
        component.touchEndHandler({
          changedTouches: [{
            clientY: 30
          }]
        } as any);

        expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalled();
      });
    });
  });

  describe('#attachEventListeneres', () => {
    it('should call attachEventListeneres when scrollableElement present', () => {
      expect(component['windowScroll']).toBeUndefined();
      expect(component['touchStart']).toBeUndefined();
      expect(component['touchEnd']).toBeUndefined();
      component['scrollableElement'] = 'scrollableElement' as any;
      component['attachEventListeneres']();

      expect(component['windowScroll']).toBeDefined();
      expect(component['touchStart']).toBeDefined();
      expect(component['touchEnd']).toBeDefined();
    });

    it('should call attachEventListeneres when scrollableElement not present', () => {
      component['attachEventListeneres']();

      expect(component['windowScroll']).toBeUndefined();
      expect(component['touchStart']).toBeUndefined();
      expect(component['touchEnd']).toBeUndefined();
    });

    it('should call attachEventListeneres when scrollableElement present', () => {
      rendererService.renderer.listen.and.callFake((a, b, cb) => {
        cb({
          touches: [{
            clientY: 100
          }]
        });
      });
      expect(component['windowScroll']).toBeUndefined();
      expect(component['touchStart']).toBeUndefined();
      expect(component['touchEnd']).toBeUndefined();

      component['scrollableElement'] = 'scrollableElement' as any;
      component['scrollVisibilityHandler'] = jasmine.createSpy('scrollVisibilityHandler');
      component['setScrollInfo'] = jasmine.createSpy('setScrollInfo');
      component['touchEndHandler'] = jasmine.createSpy('touchEndHandler');

      component['attachEventListeneres']();

      expect(component['scrollVisibilityHandler']).toHaveBeenCalled();
      expect(component['setScrollInfo']).toHaveBeenCalled();
      expect(component['touchEndHandler']).toHaveBeenCalled();

      expect(component['touchStartPosition']).toEqual(100);
    });
  });

  describe('#ngAfterContentInit', () => {
    beforeEach(() => {
      component['calculateScrollDimensions'] = jasmine.createSpy('calculateScrollDimensions');
      component['scrollVisibilityHandler'] = jasmine.createSpy('scrollVisibilityHandler');
      component['attachEventListeneres'] = jasmine.createSpy('attachEventListeneres');
      component['preFetchNext'].emit = jasmine.createSpy('preFetchNext.emit');
    });
    it('should call ngAfterContentInit with items', fakeAsync(() => {
      component.items = [1, 2];
      component['scrollDimensions'] = {
        viewPortHeight: 700
      } as any;
      component['ngAfterContentInit']();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 200);
      tick(200);
      expect(stickyScrollService.calculateInitialScrollDimensions).toHaveBeenCalled();
      expect(component['preFetchNext'].emit).toHaveBeenCalledWith(true);
      expect(component['scrollVisibilityHandler']).toHaveBeenCalledWith(false, true);
      expect(component['calculateScrollDimensions']).toHaveBeenCalled();
      expect(component['attachEventListeneres']).toHaveBeenCalled();
    }));

    it('should call ngAfterContentInit without items', fakeAsync(() => {
      component['scrollDimensions'] = {
        viewPortHeight: 100
      } as any;
      component['ngAfterContentInit']();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 200);
      tick(200);
      expect(stickyScrollService.calculateInitialScrollDimensions).toHaveBeenCalled();
      expect(component['scrollVisibilityHandler']).toHaveBeenCalledWith(false, true);
      expect(component['calculateScrollDimensions']).toHaveBeenCalled();
      expect(component['attachEventListeneres']).toHaveBeenCalled();
    }));

    it('should call ngAfterContentInit when scrollDimensions false', fakeAsync(() => {
      component['scrollDimensions'] = undefined;
      component['ngAfterContentInit']();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 200);
      tick(200);
      expect(stickyScrollService.calculateInitialScrollDimensions).toHaveBeenCalled();
      expect(component['preFetchNext'].emit).not.toHaveBeenCalled();
      expect(component['scrollVisibilityHandler']).toHaveBeenCalledWith(false, true);
      expect(component['calculateScrollDimensions']).toHaveBeenCalled();
      expect(component['attachEventListeneres']).toHaveBeenCalled();
    }));

    it('should call ngAfterContentInit preFetchNext emit not to haveBeenCalled', fakeAsync(() => {
      component.items = [1, 2];
      component['scrollDimensions'] = {
        viewPortHeight: 100
      } as any;
      component['ngAfterContentInit']();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 200);
      tick(200);
      expect(stickyScrollService.calculateInitialScrollDimensions).toHaveBeenCalled();
      expect(component['preFetchNext'].emit).not.toHaveBeenCalled();
      expect(component['scrollVisibilityHandler']).toHaveBeenCalledWith(false, true);
      expect(component['calculateScrollDimensions']).toHaveBeenCalled();
      expect(component['attachEventListeneres']).toHaveBeenCalled();
    }));
  });

  describe('#setScrollInfo', () => {
    beforeEach(() => {
      component['scrollUniqueId'] = 'scrollUniqueId';
      component['scrollDimensions'] = 'scrollDimensions' as any;
      component['stickyElement'] = 'stickyElement' as any;
      component['stickyElementPlaceholder'] = 'stickyElementPlaceholder' as any;
      component['isFirstStickyElement'] = true;
      component['firstScrollableElement'] = 'firstScrollableElement' as any;
      component['scrollableElement'] = {
        parentElement: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue('lastScrollableElement')
        }
      } as any;
      component['scrollEnabled'] = true;
      component['scrollDebounceTime'] = 20;
      component['calculateScrollDimensions'] = (() => { }) as any;
    });

    it('should call setScrollInfo when OuterHeight 0', () => {
      component['setScrollInfo']();

      expect(stickyScrollService.setScrollInfo).toHaveBeenCalledWith(jasmine.objectContaining({
        uuid: 'scrollUniqueId',
        dimensions: 'scrollDimensions',
        stickyElement: 'stickyElement',
        stickyElementPlaceholder: 'stickyElementPlaceholder',
        isFirstStickyElement: true,
        firstScrollableElement: 'firstScrollableElement',
        lastScrollableElement: 'lastScrollableElement',
        lastScrollableHeight: 1,
        scrollableElement: jasmine.any(Object),
        isVirtualScroll: true,
        scrollDebounceTime: 20,
        calculateScrollDimensions: jasmine.any(Function)
      }));
    });

    it('should call setScrollInfo when OuterHeight 2', () => {
      domToolsService.getOuterHeight.and.returnValue(2);
      component['setScrollInfo']();

      expect(stickyScrollService.setScrollInfo).toHaveBeenCalledWith(jasmine.objectContaining({
        uuid: 'scrollUniqueId',
        dimensions: 'scrollDimensions',
        stickyElement: 'stickyElement',
        stickyElementPlaceholder: 'stickyElementPlaceholder',
        isFirstStickyElement: true,
        firstScrollableElement: 'firstScrollableElement',
        lastScrollableElement: 'lastScrollableElement',
        lastScrollableHeight: 2,
        scrollableElement: jasmine.any(Object),
        isVirtualScroll: true,
        scrollDebounceTime: 20,
        calculateScrollDimensions: jasmine.any(Function)
      }));
    });
  });

  describe('#calculateScrollDimensions', () => {
    beforeEach(() => {
      stickyScrollService.initialScrollDimensions = {
        stickyMaxPosition: 10,
        documentHeight: 600,
        footerMenuHeight: 100
      };
    });
    it('should call calculateScrollDimensions with scrollableElementLevel, scrollableElementLevel, items', fakeAsync(() => {
      domToolsService.getParentByLevel.and.callFake((a, b, c) => {
        if (b === 1) {
          return {
            viewPortHeight: 700
          };
        } else {
          return {
            previousSibling: {
              nodeName: 'nodeName'
            }
          };
        }
      });
      component.scrollableElementLevel = 2;
      component.stickyHeaderLevel = 1;
      component.items = [1, 2];
      const result = component['calculateScrollDimensions']();

      tick(300);

      expect(result).toEqual({
        stickyElementHeight: 0,
        scrollableHeaderHeight: 0,
        scrollableHeight: 0,
        scrollableMaxPosition: 10,
        viewPortHeight: 490,
        stickyMaxPosition: 10,
        documentHeight: 600,
        footerMenuHeight: 100
      } as any);
    }));

    it('should call ScrollDimensions with undefined value', fakeAsync(() => {
      domToolsService.getParentByLevel.and.callFake((a, b, c) => {
        if (b === 1) {
          return '';
        } else {
          return {
            previousSibling: {
              nodeName: 'nodeName'
            }
          };
        }
      });
      component.scrollableElementLevel = 2;
      component.stickyHeaderLevel = 1;
      component.items = [1, 2];
      const result = component['calculateScrollDimensions']();

      tick(300);

      expect(result).toBeUndefined();
    }));

    it('should call calculateScrollDimensions when firstScrollableElement = false lastScrollableElement = true', fakeAsync(() => {
      domToolsService.getParentByLevel.and.returnValue({
        previousSibling: {
          nodeName: 'nodeName'
        },
        tagName: 'tagName',
        parentElement: {
          querySelector: jasmine.createSpy('querySelector').and.callFake((a) => {
            if (a === 'tagName:first-of-type') {
              return false;
            }
            if (a === 'tagName:last-of-type') {
              return true;
            }
          })
        }
      });
      element.nativeElement.parentNode.querySelector.and.returnValue('nativeElement.parentNode');

      component.scrollableElementLevel = 2;
      component.stickyHeaderLevel = 1;
      component.items = [1, 2];
      const result = component['calculateScrollDimensions']();

      tick(300);

      expect(result).toEqual({
        stickyElementHeight: 0,
        scrollableHeaderHeight: 0,
        scrollableHeight: 0,
        scrollableMaxPosition: 10,
        viewPortHeight: 490,
        stickyMaxPosition: 10,
        documentHeight: 600,
        footerMenuHeight: 100
      } as any);
    }));

    it('should call calculateScrollDimensions when firstScrollableElement = false lastScrollableElement = false', fakeAsync(() => {
      component.scrollableHeaderSelector = 'scrollableHeaderSelector' as any;
      domToolsService.getParentByLevel.and.returnValue({
        previousSibling: {
          nodeName: 'nodeName'
        },
        tagName: 'tagName',
        parentElement: {
          querySelector: jasmine.createSpy('querySelector').and.callFake((a) => {
            if (a === 'tagName:first-of-type') {
              return false;
            }
            if (a === 'tagName:last-of-type') {
              return false;
            }
          })
        }
      });
      element.nativeElement.parentNode.querySelector.and.returnValue('nativeElement.parentNode');

      component.scrollableElementLevel = 2;
      component.stickyHeaderLevel = 1;
      component.items = [1, 2];
      const result = component['calculateScrollDimensions']();

      tick(300);

      expect(result).toEqual({
        stickyElementHeight: 0,
        scrollableHeaderHeight: 0,
        scrollableHeight: 0,
        scrollableMaxPosition: 10,
        viewPortHeight: 490,
        stickyMaxPosition: 10,
        documentHeight: 600,
        footerMenuHeight: 100
      } as any);
    }));

    it('should call calculateScrollDimensions without scrollableElementLevel, scrollableElementLevel, items', () => {
      element.nativeElement.parentNode.querySelector.and.returnValue('nativeElement.parentNode');
      const result = component['calculateScrollDimensions']();

      expect(result).toEqual({
        stickyElementHeight: 0,
        scrollableHeaderHeight: 0,
        scrollableHeight: 0,
        scrollableMaxPosition: 10,
        viewPortHeight: 490,
        stickyMaxPosition: 10,
        documentHeight: 600,
        footerMenuHeight: 100
      } as any);
      expect(component['firstScrollableElement']).toEqual('parentElement_querySelector' as any);
      expect(component['lastScrollableElement']).toEqual('parentElement_querySelector' as any);
    });

    it('should call calculateScrollDimensions when device scroll enabled', () => {
      element.nativeElement.parentNode.querySelector.and.returnValue('nativeElement.parentNode');
      component['isIOsEnabled'] = true;
      component['isAndroidEnabled'] = true;
      component['calculateScrollDimensions']();
    });

    it('should call calculateScrollDimensions when device scroll disabled', () => {
      component['isIOsEnabled'] = false;
      component['isAndroidEnabled'] = false;
      element.nativeElement.parentNode.querySelector.and.returnValue('nativeElement.parentNode');
      component['calculateScrollDimensions']();
    });

    describe('#scrollableHeight', () => {
      beforeEach(() => {
        component.scrollableElementLevel = 2;
        component.stickyHeaderLevel = 1;
        component.items = [1, 2];
      });
      it('should return 0', fakeAsync(() => {
        domToolsService.getParentByLevel.and.callFake((a, b, c) => {
          if (b === 2) {
            return null;
          } else {
            return {
              previousSibling: {
                nodeName: 'nodeName'
              }
            };
          }
        });
        const result = component['calculateScrollDimensions']();

        tick(300);

        expect(result).toEqual({
          stickyElementHeight: 0,
          scrollableHeaderHeight: 0,
          scrollableHeight: 0,
          scrollableMaxPosition: 10,
          viewPortHeight: 490,
          stickyMaxPosition: 10,
          documentHeight: 600,
          footerMenuHeight: 100
        } as any);
      }));
    });
    it('should return 10', fakeAsync(() => {
      domToolsService.getOuterHeight.and.returnValue(10);
      const result = component['calculateScrollDimensions']();

      tick(300);

      expect(result).toEqual({
        stickyElementHeight: 10,
        scrollableHeaderHeight: 0,
        scrollableHeight: 10,
        scrollableMaxPosition: 20,
        viewPortHeight: 480,
        stickyMaxPosition: 10,
        documentHeight: 600,
        footerMenuHeight: 100
      } as any);
    }));

    describe('when scrollable height is greater viewportport height', () => {
      beforeEach(() => {
        domToolsService.getOuterHeight.and.returnValue(420);
      });

      it('should scroll when isIOsEnabled', fakeAsync(() => {
        component['isIOsEnabled'] = true;
        component['isAndroidEnabled'] = false;

        const result = component['calculateScrollDimensions']();

        tick(300);

        expect(result).toEqual({
          stickyElementHeight: 420,
          scrollableHeaderHeight: 0,
          scrollableHeight: 70,
          scrollableMaxPosition: 430,
          viewPortHeight: 70,
          stickyMaxPosition: 10,
          documentHeight: 600,
          footerMenuHeight: 100
        } as any);
      }));
      it('should scroll when isAndroidEnabled', fakeAsync(() => {
        component['isIOsEnabled'] = false;
        component['isAndroidEnabled'] = true;

        const result = component['calculateScrollDimensions']();

        tick(300);

        expect(result).toEqual({
          stickyElementHeight: 420,
          scrollableHeaderHeight: 0,
          scrollableHeight: 70,
          scrollableMaxPosition: 430,
          viewPortHeight: 70,
          stickyMaxPosition: 10,
          documentHeight: 600,
          footerMenuHeight: 100
        } as any);
      }));
      it('should scroll when isAndroidEnabled or isIOsEnabled', fakeAsync(() => {
        component['isIOsEnabled'] = true;
        component['isAndroidEnabled'] = true;

        const result = component['calculateScrollDimensions']();

        tick(300);

        expect(result).toEqual({
          stickyElementHeight: 420,
          scrollableHeaderHeight: 0,
          scrollableHeight: 70,
          scrollableMaxPosition: 430,
          viewPortHeight: 70,
          stickyMaxPosition: 10,
          documentHeight: 600,
          footerMenuHeight: 100
        } as any);
      }));
      it('should not scroll when inner scroll disabled', fakeAsync(() => {
        component['isIOsEnabled'] = false;
        component['isAndroidEnabled'] = false;

        const result = component['calculateScrollDimensions']();

        tick(300);

        expect(result).toEqual({
          stickyElementHeight: 420,
          scrollableHeaderHeight: 0,
          scrollableHeight: 420,
          scrollableMaxPosition: 430,
          viewPortHeight: 70,
          stickyMaxPosition: 10,
          documentHeight: 600,
          footerMenuHeight: 100
        } as any);
      }));
    });

    describe('isFirstStickyElement', () => {
      beforeEach(() => {
        component.stickyContainerLevel = 7;
        component.stickyContainerTag = 'ACCORDION';
      });

      it('should be false for accordion', () => {
        domToolsService.getParentByLevel.and.callFake((a, b, c) => {
          if (b === 7) {
            return {
              previousSibling: {
                nodeName: 'ACCORDION'
              }
            };
          } else {
            return {
              previousSibling: {
                nodeName: 'nodeName'
              }
            };
          }
        });
        component['calculateScrollDimensions']();
        expect(component['isFirstStickyElement']).toBeFalsy();
      });

      it('should be true for non accordion', () => {
        domToolsService.getParentByLevel.and.callFake((a, b, c) => {
          if (b === 7) {
            return {
              previousSibling: {
                nodeName: 'nonAccordion'
              }
            };
          } else {
            return {
              previousSibling: {
                nodeName: 'nodeName'
              }
            };
          }
        });
        component['calculateScrollDimensions']();
        expect(component['isFirstStickyElement']).toBeTruthy();
      });

      it('should be false for nothing', () => {
        domToolsService.getParentByLevel.and.callFake((a, b, c) => {
          if (b === 7) {
            return null;
          } else {
            return {
              previousSibling: {
                nodeName: 'nodeName'
              }
            };
          }
        });
        component['calculateScrollDimensions']();
        expect(component['isFirstStickyElement']).toBeFalsy();
      });
    });

    describe('stickyElementPlaceholder', () => {
      beforeEach(() => {
        component.stickyHeaderTag = 'header';
        component.stickyHeaderLevel = 6;
      });

      it('should be defined', () => {
        domToolsService.getParentByLevel.and.callFake((a, b, c) => {
          if (b === 6) {
            return {
              nextElementSibling: {
                nodeName: 'nodeName'
              }
            };
          } else {
            return {
              previousSibling: {
                nodeName: 'nodeName'
              }
            };
          }
        });
        component['calculateScrollDimensions']();
        expect(component['stickyElementPlaceholder']).toBeDefined();
      });

      it('should be null', () => {
        domToolsService.getParentByLevel.and.callFake((a, b, c) => {
          if (b === 6) {
            return null;
          } else {
            return {
              previousSibling: {
                nodeName: 'nodeName'
              }
            };
          }
        });
        component['calculateScrollDimensions']();
        expect(component['stickyElementPlaceholder']).toBeNull();
      });
    });
  });
});
