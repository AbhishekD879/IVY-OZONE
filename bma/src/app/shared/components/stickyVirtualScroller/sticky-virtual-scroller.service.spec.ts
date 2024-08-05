import { StickyVirtualScrollerService } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.service';
import { IScrollInfo } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.model';
import { fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';

describe('#StickyVirtualScrollerService', () => {
  let service: StickyVirtualScrollerService, windowRef, renderService, pubSubService, domToolsService, zone, deviceService,
    carouselMenuStateService, scrollInfoMock: IScrollInfo;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        scrollBy: jasmine.createSpy('scrollBy'),
        addEventListener: jasmine.createSpy('addEventListener'),
        scroll: jasmine.createSpy('scroll'),
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue('querySelector')
        },
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb, time) => {
          cb();
        })
      }
    };
    renderService = {
      renderer: {
        listen: jasmine.createSpy('listen')
      }
    };
    pubSubService = {
      API: {
        FIXED_CONTENT_REDRAW: 'FIXED_CONTENT_REDRAW',
        WS_EVENT_DELETE: 'WS_EVENT_DELETE',
        INPLAY_COMPETITION_REMOVED: 'INPLAY_COMPETITION_REMOVED'
      },
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    domToolsService = {
      toggleClass: jasmine.createSpy('toggleClass'),
      css: jasmine.createSpy('css'),
      getWidth: jasmine.createSpy('getWidth'),
      getHeight: jasmine.createSpy('getHeight').and.returnValue(10),
      getOuterHeight: jasmine.createSpy('getOuterHeight').and.returnValue(5),
      getElementTopPosition: jasmine.createSpy('getElementTopPosition').and.returnValue(10),
      getElementBottomPosition: jasmine.createSpy('getElementBottomPosition').and.returnValue(10),
      getOffset: jasmine.createSpy('getOffset').and.returnValue({
        top: 10
      }),
      scrollStop: jasmine.createSpy('scrollStop').and.callFake(cb => {
        cb();
      })
    };
    zone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular')
    };
    deviceService = {};
    carouselMenuStateService = {
      carouselStick$: {
        next: jasmine.createSpy('next')
      }
    };

    service = new StickyVirtualScrollerService(
      windowRef,
      renderService,
      pubSubService,
      domToolsService,
      zone,
      deviceService,
      carouselMenuStateService);

    scrollInfoMock = {
      uuid: 'scrollUniqueId',
      dimensions: {
        documentHeight: 0,
        footerMenuHeight: 0,
        headerHeight: 0,
        scrollableHeaderHeight: 0,
        scrollableHeight: 0,
        scrollableMaxPosition: 20,
        stickyElementHeight: 0,
        stickyMaxPosition: 0,
        topBarHeight: 0,
        viewPortHeight: 0
      },
      firstScrollableElement: {} as any,
      lastScrollableElement: {} as any,
      scrollableElement: {} as any,
      stickyElement: {
        style: {
          removeProperty: jasmine.createSpy('style.removeProperty').and.returnValue(true),
        }
      } as any,
      stickyElementPlaceholder: {
        style: {
          removeProperty: jasmine.createSpy('style.removeProperty').and.returnValue(true),
        }
      } as any,
      isFirstStickyElement: false,
      isVirtualScroll: false,
      scrollDebounceTime: 1000,
      calculateScrollDimensions: jasmine.createSpy('calculateScrollDimensions'),
      preFetchNext: jasmine.createSpyObj('EventEmitter', ['emit']),
      toogleStickyVisiblity: jasmine.createSpyObj('EventEmitter', ['emit']),
      lastScrollableHeight: 10
    };
  });

  describe('init', () => {
    beforeEach(() => {
      service['attachEventListeners'] = jasmine.createSpy('attachEventListeners');
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        cb();
      });
    });

    it('should create StickyVirtualScrollerService instance', () => {
      expect(service).toBeTruthy();
    });

    it('should subscribe on FIXED_CONTENT_REDRAW', () => {
      service['handleCookieBannerPosition'] = jasmine.createSpy('handleCookieBannerPosition');
      service['init']();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('stickyVirtualScroll',
        pubSubService.API.FIXED_CONTENT_REDRAW, jasmine.any(Function));
      expect(service['handleCookieBannerPosition']).toHaveBeenCalled();
    });

    it('should subscribe on WS_EVENT_DELETE', () => {
      service['updateScrollVisibility'] = jasmine.createSpy('updateScrollVisibility');
      service['init']();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('stickyVirtualScroll',
        pubSubService.API.WS_EVENT_DELETE, jasmine.any(Function));
      expect(service['updateScrollVisibility']).toHaveBeenCalled();
    });

    it('should subscribe on INPLAY_COMPETITION_ADDED, INPLAY_COMPETITION_UPDATED, INPLAY_COMPETITION_REMOVED', () => {
      service['updateScrollVisibility'] = jasmine.createSpy('updateScrollVisibility');
      service['init']();
      expect(pubSubService.subscribe.calls.argsFor(2)).toEqual(['stickyVirtualScroll',
        ['INPLAY_COMPETITION_ADDED'], jasmine.any(Function)]);
      expect(pubSubService.subscribe.calls.argsFor(3)).toEqual(['stickyVirtualScroll',
        ['INPLAY_COMPETITION_UPDATED'], jasmine.any(Function)]);
      expect(pubSubService.subscribe.calls.argsFor(4)).toEqual(['stickyVirtualScroll',
        ['INPLAY_COMPETITION_REMOVED'], jasmine.any(Function)]);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 200);
      expect(service['updateScrollVisibility']).toHaveBeenCalled();
    });
  });

  describe('#destroyEvents', () => {
    beforeEach(() => {
      service['keepStickyHeader'] = true;
    });

    it('should destroyEvents', () => {
      service['orientationChange'] = jasmine.createSpy('orientationChange');
      service['resize'] = jasmine.createSpy('resize');
      service['touchEnd'] = jasmine.createSpy('touchEnd');
      service['scrollHandler'] = jasmine.createSpy('scrollHandler');

      service.destroyEvents();
      expect(service['orientationChange']).toHaveBeenCalled();
      expect(service['resize']).toHaveBeenCalled();
      expect(service['scrollHandler']).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('stickyVirtualScroll');
      expect(carouselMenuStateService.carouselStick$.next).toHaveBeenCalledWith({ stick: false, forceVisibility: false });
      expect(service['keepStickyHeader']).toEqual(false);
    });

    it('should not call destroyEvents', () => {
      service.destroyEvents();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('stickyVirtualScroll');
      expect(carouselMenuStateService.carouselStick$.next).toHaveBeenCalledWith({ stick: false, forceVisibility: false });
      expect(service['keepStickyHeader']).toEqual(false);
    });
  });

  describe('#handleStickyPosition', () => {
    beforeEach(() => {
      service.stick = jasmine.createSpy('stick');
      service['handleExternalStickyPositions'] = jasmine.createSpy('handleExternalStickyPositions');
      service['handleStickHeaderPosition'] = jasmine.createSpy('handleStickHeaderPosition');
    });
    it('should call handleStickyPosition when scroll suspended and no scrollInfo', () => {
      service['isSuspended'] = true;

      service.handleStickyPosition(undefined);
      expect(service['handleExternalStickyPositions']).not.toHaveBeenCalled();
      expect(service['handleStickHeaderPosition']).not.toHaveBeenCalled();
    });

    it('should call handleStickyPosition when scroll suspended', () => {
      service['isSuspended'] = true;

      service.handleStickyPosition(scrollInfoMock as any);
      expect(service['handleExternalStickyPositions']).not.toHaveBeenCalled();
      expect(service['handleStickHeaderPosition']).not.toHaveBeenCalled();
    });

    it('should call handleStickyPosition when scroll is not suspended', () => {
      service['isSuspended'] = false;

      service.handleStickyPosition(scrollInfoMock as any);
      expect(service['handleExternalStickyPositions']).toHaveBeenCalledWith(scrollInfoMock);
      expect(service['handleStickHeaderPosition']).toHaveBeenCalledWith(scrollInfoMock);
    });

  });

  describe('#keepScrollPositions', () => {
    beforeEach(() => {
      service.stick = jasmine.createSpy('stick');
      service['scrollBy'] = jasmine.createSpy('scrollBy');
    });
    it('should call keepScrollPositions when scroll suspended and no scrollInfo', () => {
      service['isSuspended'] = true;

      service.keepScrollPositions(undefined);
      expect(domToolsService.getElementTopPosition).not.toHaveBeenCalled();
      expect(service['scrollBy']).not.toHaveBeenCalled();
    });

    it('should call keepScrollPositions when scroll suspended', () => {
      service['isSuspended'] = true;

      service.keepScrollPositions(scrollInfoMock as any);
      expect(domToolsService.getElementTopPosition).not.toHaveBeenCalled();
      expect(service['scrollBy']).not.toHaveBeenCalled();
    });

    it('should call keepScrollPositions whit diff uuid', () => {
      service['serviceScrollInfo'] = {
        uuid: 'scrollUniqueId_diff'
      } as any;
      service.keepScrollPositions(scrollInfoMock as any);
      expect(domToolsService.getElementTopPosition).toHaveBeenCalledWith({});
      expect(service.stick).toHaveBeenCalledWith(false, false, { uuid: 'scrollUniqueId_diff' } as any);
    });

    it('should call keepScrollPositions whit same uuid', () => {
      service['serviceScrollInfo'] = {
        uuid: 'scrollUniqueId'
      } as any;
      service.keepScrollPositions(scrollInfoMock as any);
      expect(domToolsService.getElementTopPosition).not.toHaveBeenCalled();
      expect(service.stick).not.toHaveBeenCalled();
    });

    it('should call keepScrollPositions isSticky = false and isFirstTopAboveSticky = true', () => {
      domToolsService.getElementTopPosition.and.returnValue(10);
      service['serviceScrollInfo'] = {
        uuid: 'scrollUniqueId_diff'
      } as any;
      service['isSticky'] = false;
      service.keepScrollPositions({
        uuid: 'scrollUniqueId',
        dimensions: {
          scrollableMaxPosition: 20
        },
        stickyElement: 'stickyElement',
        isFirstStickyElement: true,
        firstScrollableElement: 'firstScrollableElement',
        lastScrollableElement: 'lastScrollableElement',
        lastScrollableHeight: 1
      } as any);
      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
      expect(service.stick).toHaveBeenCalledWith(false, false, { uuid: 'scrollUniqueId_diff' } as any);
      expect(service['scrollBy']).toHaveBeenCalledTimes(2);
    });

    it('should call keepScrollPositions isSticky = true and isFirstTopAboveSticky = false', () => {
      domToolsService.getElementTopPosition.and.returnValue(30);
      service['serviceScrollInfo'] = {
        uuid: 'scrollUniqueId_diff'
      } as any;
      service['isSticky'] = true;
      service.keepScrollPositions({
        uuid: 'scrollUniqueId',
        dimensions: {
          scrollableMaxPosition: 20
        },
        stickyElement: 'stickyElement',
        isFirstStickyElement: true,
        firstScrollableElement: 'firstScrollableElement',
        lastScrollableElement: 'lastScrollableElement',
        lastScrollableHeight: 1
      } as any);
      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
      expect(service.stick).toHaveBeenCalledWith(false, false, { uuid: 'scrollUniqueId_diff' } as any);
      expect(service['scrollBy']).toHaveBeenCalledTimes(2);
    });
    it('should call keepScrollPositions isSticky = true and isFirstTopAboveSticky = true', () => {
      domToolsService.getElementTopPosition.and.returnValue(10);
      service['serviceScrollInfo'] = {
        uuid: 'scrollUniqueId_diff'
      } as any;
      service['isSticky'] = true;
      service.keepScrollPositions({
        uuid: 'scrollUniqueId',
        dimensions: {
          scrollableMaxPosition: 20
        },
        stickyElement: 'stickyElement',
        isFirstStickyElement: true,
        firstScrollableElement: 'firstScrollableElement',
        lastScrollableElement: 'lastScrollableElement',
        lastScrollableHeight: 1
      } as any);
      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
      expect(service.stick).toHaveBeenCalledWith(false, false, { uuid: 'scrollUniqueId_diff' } as any);
      expect(service['scrollBy']).not.toHaveBeenCalled();
    });
    it('should call keepScrollPositions isSticky = false and isFirstTopAboveSticky = false', () => {
      domToolsService.getElementTopPosition.and.returnValue(30);
      service['serviceScrollInfo'] = {
        uuid: 'scrollUniqueId_diff'
      } as any;
      service['isSticky'] = false;
      service.keepScrollPositions({
        uuid: 'scrollUniqueId',
        dimensions: {
          scrollableMaxPosition: 20
        },
        stickyElement: 'stickyElement',
        isFirstStickyElement: true,
        firstScrollableElement: 'firstScrollableElement',
        lastScrollableElement: 'lastScrollableElement',
        lastScrollableHeight: 1
      } as any);
      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
      expect(service.stick).toHaveBeenCalledWith(false, false, { uuid: 'scrollUniqueId_diff' } as any);
      expect(service['scrollBy']).not.toHaveBeenCalled();
    });
  });

  describe('setScrollInfo', () => {
    let incomingScrollInfo;
    beforeEach(() => {
      service.keepScrollPositions = jasmine.createSpy('keepScrollPositions');
      incomingScrollInfo = { ...scrollInfoMock, uuid: 'incomingScrollInfo' };
    });

    it('should setScrollInfo', () => {
      service.setScrollInfo(incomingScrollInfo);
      expect(service.keepScrollPositions).toHaveBeenCalledWith(incomingScrollInfo);
      expect(service['serviceScrollInfo']).toEqual(incomingScrollInfo);
    });

    it('lastScrollInfo should be null if isFirstStickyElement', () => {
      service['lastScrollInfo'] = undefined;
      incomingScrollInfo.isFirstStickyElement = true;
      service.setScrollInfo(incomingScrollInfo);
      expect(service['lastScrollInfo']).toBeNull();
    });

    it('should set lastScrollInfo if lastScrollInfo is undefined', () => {
      service['lastScrollInfo'] = undefined;
      incomingScrollInfo.isFirstStickyElement = false;
      const serviceScrollInfo = service['serviceScrollInfo'];
      service.setScrollInfo(incomingScrollInfo);
      expect(service['lastScrollInfo']).toEqual(serviceScrollInfo);
    });

    it('should set lastScrollInfo if lastScrollInfo is defined and not equal to current one', () => {
      service['lastScrollInfo'] = { ...scrollInfoMock, uuid: 'lastScrollInfo' };
      incomingScrollInfo.isFirstStickyElement = false;
      service['serviceScrollInfo'] = { ...scrollInfoMock, uuid: 'serviceScrollInfo' };
      const serviceScrollInfo = service['serviceScrollInfo'];
      service.setScrollInfo(incomingScrollInfo);
      expect(service['lastScrollInfo']).toEqual(serviceScrollInfo);
    });

    it('should not set lastScrollInfo if serviceScrollInfo is not defined', () => {
      service['lastScrollInfo'] = { ...scrollInfoMock, uuid: 'lastScrollInfo' };
      incomingScrollInfo.isFirstStickyElement = false;
      service['serviceScrollInfo'] = undefined;
      service.setScrollInfo(incomingScrollInfo);
      expect(service['lastScrollInfo']).toEqual(service['lastScrollInfo']);
    });
  });

  describe('#handleStickHeaderPosition', () => {
    beforeEach(() => {
      service.stick = jasmine.createSpy('stick');
      service['stickCarousel'] = jasmine.createSpy('stickCarousel');
      domToolsService.getElementTopPosition.and.returnValue(20);
      service['scrollBy'] = jasmine.createSpy('scrollBy');
    });
    it('should call handleStickHeaderPosition when scroll isSticky = true and no scrollInfo', () => {
      service['isSticky'] = true;

      service.handleStickHeaderPosition(scrollInfoMock as any);
      expect(service['stickCarousel']).not.toHaveBeenCalled();
    });

    it('should call handleStickHeaderPosition when isSticky false', () => {
      service['isSticky'] = false;

      service.handleStickHeaderPosition(scrollInfoMock as any);
      expect(service['stickCarousel']).toHaveBeenCalledWith(true);
      expect(service['stick']).toHaveBeenCalledWith(true, false, scrollInfoMock);
    });

    it('should call handleStickHeaderPosition when isSticky false', () => {
      service['isSticky'] = false;
      service['lastScrollInfo'] = {
        toogleStickyVisiblity: {
          emit: jasmine.createSpy('toogleStickyVisiblity.emit')
        }
      } as any;

      service.handleStickHeaderPosition(scrollInfoMock as any);
      expect(service['stickCarousel']).toHaveBeenCalledWith(true);
      expect(service['lastScrollInfo'].toogleStickyVisiblity.emit).toHaveBeenCalledWith(true);
      expect(service['stick']).toHaveBeenCalledWith(true, false, scrollInfoMock);
    });

    it(`should call handleStickHeaderPosition with scrollInfo
      when isSticky true case (isFirstBelowSticky || isLastBottomAboveSticky)`, () => {
        service['isSticky'] = true;
        scrollInfoMock.dimensions.scrollableMaxPosition = 10;

        service.handleStickHeaderPosition(scrollInfoMock as any);
        expect(service['stick']).toHaveBeenCalledWith(false, false, scrollInfoMock);
      });

    it(`should call handleStickHeaderPosition without scrollInfo
      when isSticky true case (isFirstBelowSticky || isLastBottomAboveSticky)`, () => {
        service['isSticky'] = true;
        service['serviceScrollInfo'] = scrollInfoMock;
        scrollInfoMock.dimensions.scrollableMaxPosition = 10;

        service.handleStickHeaderPosition();
        expect(service['stick']).toHaveBeenCalledWith(false, false, scrollInfoMock);
      });

    it(`should not call handleStickHeaderPosition when (isFirstBelowSticky = false || isLastBottomAboveSticky is false)`, () => {
      service['isSticky'] = true;
      service['serviceScrollInfo'] = scrollInfoMock;
      scrollInfoMock.dimensions.scrollableMaxPosition = 10;
      domToolsService.getElementTopPosition.and.returnValue(0);

      service.handleStickHeaderPosition();
      expect(service['stick']).not.toHaveBeenCalled();
    });
  });

  describe('#stick', () => {
    let requestAnimationFrameCb = () => {};

    beforeEach(() => {
      service['isSticky'] = true;
      service['updateStickyHeaderWidth'] = jasmine.createSpy('updateStickyHeaderWidth');
      service['updateStickyHeaderTop'] = jasmine.createSpy('updateStickyHeaderTop');
      service.initialScrollDimensions = {
        headerHeight: 20,
        topBarHeight: 10
      } as any;
      spyOn(global as any, 'requestAnimationFrame').and.callFake(cb => requestAnimationFrameCb = cb);
      service['keepStickyHeaderPosition'] = jasmine.createSpy('keepStickyHeaderPosition');
      service['keepStickyHeader'] = true;
      zone.runOutsideAngular.and.callFake((fn: Function) => fn());
    });

    it('should call stick when no scrollInfo', () => {
      service.stick(true, true, undefined);

      expect(zone.runOutsideAngular).toHaveBeenCalled();
    });

    it('should call keepStickyHeaderPosition', () => {
      service.stick(true, true, scrollInfoMock as any);
      requestAnimationFrameCb();

      expect(service['keepStickyHeaderPosition']).toHaveBeenCalled();
    });

    it('should not call keepStickyHeaderPosition', () => {
      service['keepStickyHeader'] = false;

      service.stick(true, true, scrollInfoMock as any);
      requestAnimationFrameCb();

      expect(service['keepStickyHeaderPosition']).not.toHaveBeenCalled();
    });

    it('should not call keepStickyHeaderPosition', () => {
      service['keepStickyHeader'] = false;

      service.stick(true, false, scrollInfoMock as any);
      requestAnimationFrameCb();

      expect(service['keepStickyHeaderPosition']).not.toHaveBeenCalled();
    });

    it('should call stick when isSticky false', () => {
      jasmine.clock().install();
      service['isSticky'] = false;
      service['lastScrollInfo'] = {
        toogleStickyVisiblity: {
          emit: jasmine.createSpy('toogleStickyVisiblity.emit')
        }
      } as any;

      service.stick(false, true, scrollInfoMock as any);

      jasmine.clock().tick(2000);

      expect(domToolsService.toggleClass).not.toHaveBeenCalledWith();
      expect(domToolsService.css).not.toHaveBeenCalledWith();
      expect(windowRef.nativeWindow.scroll).not.toHaveBeenCalledWith();
      expect(carouselMenuStateService.carouselStick$.next).not.toHaveBeenCalledWith();

      jasmine.clock().uninstall();
    });
  });

  describe('#handleExternalStickyPositions', () => {
    beforeEach(() => {
      zone.runOutsideAngular.and.callFake((fn: Function) => fn());
      service['stickCarousel'] = jasmine.createSpy('stickCarousel');
    });
    it('should call handleExternalStickyPositions (isCarouselStick = false)', () => {
      service['isCarouselStick'] = false;
      service['firstStickyElement'] = 'firstStickyElement' as any;
      scrollInfoMock.dimensions.stickyMaxPosition = 20;
      service.handleExternalStickyPositions(scrollInfoMock as any);

      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
    });

    it('should call handleExternalStickyPositions (isCarouselStick = true && firstStickyElement = true)', () => {
      service['isCarouselStick'] = true;
      service['firstStickyElement'] = 'firstStickyElement' as any;
      scrollInfoMock.dimensions.stickyMaxPosition = 5;
      service.handleExternalStickyPositions(scrollInfoMock as any);

      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
    });

    it('should call handleExternalStickyPositions (isCarouselStick = false)', () => {
      service['isCarouselStick'] = false;
      service['firstStickyElement'] = 'firstStickyElement' as any;
      scrollInfoMock.dimensions.stickyMaxPosition = 5;
      service.handleExternalStickyPositions(scrollInfoMock as any);

      expect(domToolsService.getElementTopPosition).toHaveBeenCalled();
    });

    it('should call handleExternalStickyPositions (firstStickyElement = true)', () => {
      service['firstStickyElement'] = null;
      service.handleExternalStickyPositions(scrollInfoMock as any);

      expect(domToolsService.getElementTopPosition).not.toHaveBeenCalled();
    });
  });

  describe('#updateScrollVisibility', () => {
    it('should call updateScrollVisibility', () => {
      service['updateScrollVisibility$'].next = jasmine.createSpy('updateScrollVisibility$.next');
      service.updateScrollVisibility();

      expect(service['updateScrollVisibility$'].next).toHaveBeenCalled();
    });
  });

  describe('#calculateInitialScrollDimensions', () => {
    it('should call calculateInitialScrollDimensions with reset', () => {
      Object.defineProperty(service['domToolsService'], 'HeaderEl', { value: 'HeaderEl' });
      Object.defineProperty(service['domToolsService'], 'FooterEl', { value: 'FooterEl' });
      service.calculateInitialScrollDimensions(true);

      expect(domToolsService.getHeight).toHaveBeenCalledTimes(1);
      expect(domToolsService.getOuterHeight).toHaveBeenCalledTimes(4);
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalledTimes(2);
    });

    it('should call calculateInitialScrollDimensions with resetm and querySelector = null', () => {
      windowRef.nativeWindow.document.querySelector.and.returnValue(null);
      Object.defineProperty(service['domToolsService'], 'HeaderEl', { value: null });
      Object.defineProperty(service['domToolsService'], 'FooterEl', { value: null });
      service.calculateInitialScrollDimensions(true);

      expect(domToolsService.getHeight).toHaveBeenCalledTimes(1);
      expect(domToolsService.getOuterHeight).not.toHaveBeenCalledTimes(4);
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalledTimes(2);
    });

    it('should call calculateInitialScrollDimensions with reset = false initialScrollDimensions = undefined', () => {
      Object.defineProperty(service['domToolsService'], 'HeaderEl', { value: 'HeaderEl' });
      Object.defineProperty(service['domToolsService'], 'FooterEl', { value: 'FooterEl' });
      service.calculateInitialScrollDimensions();

      expect(domToolsService.getHeight).toHaveBeenCalledTimes(1);
      expect(domToolsService.getOuterHeight).toHaveBeenCalledTimes(4);
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalledTimes(2);
    });

    it('should call calculateInitialScrollDimensions with reset = false', () => {
      Object.defineProperty(service['domToolsService'], 'HeaderEl', { value: 'HeaderEl' });
      Object.defineProperty(service['domToolsService'], 'FooterEl', { value: 'FooterEl' });
      service['initialScrollDimensions'] = {} as any;
      service.calculateInitialScrollDimensions();

      expect(domToolsService.getHeight).not.toHaveBeenCalled();
      expect(domToolsService.getOuterHeight).not.toHaveBeenCalled();
      expect(windowRef.nativeWindow.document.querySelector).not.toHaveBeenCalled();
    });
  });

  describe('#init', () => {
    it('should call init', () => {
      pubSubService.subscribe.and.callFake((a, b, callback) => {
        callback();
      });
      service['attachEventListeners'] = jasmine.createSpy('attachEventListeners');
      service['init']();

      expect(service['attachEventListeners']).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });
  });

  describe('#attachEventListeners', () => {
    it('should call attachEventListeners', () => {
      Object.defineProperty(deviceService, 'isMobileOrigin', { value: true });
      service['attachEventListeners']();

      expect(renderService.renderer.listen).toHaveBeenCalled();
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalled();
    });

    it('should call attachEventListeners when isMobileOrigin = false', () => {
      Object.defineProperty(deviceService, 'isMobileOrigin', { value: false });
      service['attachEventListeners']();

      expect(renderService.renderer.listen).toHaveBeenCalled();
      expect(windowRef.nativeWindow.addEventListener).not.toHaveBeenCalled();
    });

    it('should handle renderer callbacks', () => {
      spyOn(service, 'handleStickyPosition');
      service['redrawScrollableElements'] = jasmine.createSpy('redrawScrollableElements');
      Object.defineProperty(deviceService, 'isMobileOrigin', { value: true });
      renderService.renderer.listen.and.callFake((a, b, cb) => {
        cb();
      });
      service['windowRef'].nativeWindow.addEventListener = jasmine.createSpy().and.callFake((a, cb) => {
        cb();
      });
      service['attachEventListeners']();
      expect(service['redrawScrollableElements']).toHaveBeenCalledTimes(2);
    });

    it('should call handleStickyPosition', fakeAsync(() => {
      service.handleStickyPosition = jasmine.createSpy('handleStickyPosition');
      zone.runOutsideAngular.and.callFake((fn: Function) => fn());

      renderService.renderer.listen.and.callFake((a, b, cb) => {
        if (b === 'scroll') {
          cb();
        }
      });
      service['attachEventListeners']();
      tick(100);
      expect(service.handleStickyPosition).toHaveBeenCalledTimes(1);
      tick(500);
      expect(service.handleStickyPosition).toHaveBeenCalledTimes(2);
      discardPeriodicTasks();
    }));

    it('should call initDebouncedFunctions', () => {
      service['attachEventListeners']();
      expect(service['stickCarousel']).toBeDefined();
      service['stickCarousel']();
      expect(carouselMenuStateService.carouselStick$.next).toHaveBeenCalled();
    });
  });

  describe('#redrawScrollableElements', () => {
    beforeEach(() => {
      service['updateScrollDimensions$'].next = jasmine.createSpy('updateScrollDimensions$.next');
      service['calculateInitialScrollDimensions'] = jasmine.createSpy('calculateInitialScrollDimensions');
      service['updateStickyHeaderWidth'] = jasmine.createSpy('updateStickyHeaderWidth');
    });
    it('should call redrawScrollableElements with serviceScrollInfo', () => {
      service['serviceScrollInfo'] = scrollInfoMock;
      service['redrawScrollableElements']();

      expect(service['updateScrollDimensions$'].next).toHaveBeenCalled();
      expect(service['calculateInitialScrollDimensions']).toHaveBeenCalledWith(true);
      expect(service['updateStickyHeaderWidth']).toHaveBeenCalledWith(scrollInfoMock);
    });

    it('should call redrawScrollableElements without serviceScrollInfo', () => {
      service['redrawScrollableElements']();

      expect(service['updateScrollDimensions$'].next).toHaveBeenCalled();
      expect(service['calculateInitialScrollDimensions']).toHaveBeenCalledWith(true);
      expect(service['updateStickyHeaderWidth']).not.toHaveBeenCalled();
    });
  });

  describe('#handleCookieBannerPosition', () => {
    beforeEach(() => {
      service['updateScrollDimensions$'].next = jasmine.createSpy('updateScrollDimensions$.next');
      service['calculateInitialScrollDimensions'] = jasmine.createSpy('calculateInitialScrollDimensions');
      service['updateStickyHeaderTop'] = jasmine.createSpy('updateStickyHeaderTop');
    });
    it('should call handleCookieBannerPosition with serviceScrollInfo, isSticky = false', () => {
      service['serviceScrollInfo'] = scrollInfoMock;
      service['handleCookieBannerPosition']();

      expect(service['updateScrollDimensions$'].next).toHaveBeenCalled();
      expect(service['calculateInitialScrollDimensions']).toHaveBeenCalledWith(true);
      expect(service['updateStickyHeaderTop']).not.toHaveBeenCalled();
    });

    it('should call handleCookieBannerPosition with serviceScrollInfo, isSticky = true', () => {
      service['serviceScrollInfo'] = scrollInfoMock;
      service['isSticky'] = true;
      service['handleCookieBannerPosition']();

      expect(service['updateScrollDimensions$'].next).toHaveBeenCalled();
      expect(service['calculateInitialScrollDimensions']).toHaveBeenCalledWith(true);
      expect(service['updateStickyHeaderTop']).toHaveBeenCalledWith(scrollInfoMock);
    });

    it('should call handleCookieBannerPosition without serviceScrollInfo', () => {
      service['handleCookieBannerPosition']();

      expect(service['updateScrollDimensions$'].next).toHaveBeenCalled();
      expect(service['calculateInitialScrollDimensions']).toHaveBeenCalledWith(true);
      expect(service['updateStickyHeaderTop']).not.toHaveBeenCalled();
    });
  });

  describe('#updateStickyHeaderWidth', () => {
    it('should call updateStickyHeaderWidth', () => {
      service['updateScrollVisibility$'].next = jasmine.createSpy('updateScrollVisibility$.next');
      service['updateStickyHeaderWidth'](scrollInfoMock as any);

      expect(domToolsService.getWidth).toHaveBeenCalledWith({});
      expect(domToolsService.css).toHaveBeenCalledWith(jasmine.any(Object), 'width', undefined);
    });
  });

  describe('#updateStickyHeaderTop', () => {
    it('should call updateStickyHeaderTop', () => {
      service['updateStickyHeaderTop'](scrollInfoMock as any);

      expect(domToolsService.css).toHaveBeenCalledWith(jasmine.any(Object), 'top', 0);
    });
  });

  it('should call scrollBy', () => {
    service['scrollBy'](10);

    expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, 10);
  });

  describe('keepStickyHeaderPosition', () => {
    it('wasSticked', () => {
      service.wasSticked = true;
      service.initialScrollDimensions = scrollInfoMock.dimensions;
      service['keepStickyHeaderPosition'](scrollInfoMock);

      expect(domToolsService.getOffset).toHaveBeenCalled();
      expect(service['serviceScrollInfo']).toBeNull();
      expect(windowRef.nativeWindow.scroll).toHaveBeenCalledWith(0, 10);
      expect(carouselMenuStateService.carouselStick$.next).toHaveBeenCalledWith({ stick: true, forceVisibility: false });
      expect(service.wasSticked).toBeFalsy();
    });
  });
});
