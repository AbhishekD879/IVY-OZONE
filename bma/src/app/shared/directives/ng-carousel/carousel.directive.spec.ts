import { fakeAsync, tick } from '@angular/core/testing';

import { NgCarouselDirective } from '@shared/directives/ng-carousel/carousel.directive';

describe('NgCarouselDirective', () => {
  let directive: NgCarouselDirective;

  let domToolsService;
  let carouselService;
  let elementRef;
  let windowRef;
  let deviceService;
  let rendererService;
  let ngZone;

  beforeEach(() => {
    domToolsService = {
      css: jasmine.createSpy('css')
    } as any;

    carouselService = {
      remove: jasmine.createSpy(),
      get: jasmine.createSpy()
    } as any;
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector'),
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([])
      }
    } as any;
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout').and.callFake(val => val),
      },
      document: {
        createElement: jasmine.createSpy('createElement').and.returnValue({
          className: '',
          dataset: jasmine.createSpyObj('dataset', ['crlat', 'eventid'])
        })
      }
    } as any;
    deviceService = {} as any;

    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass'),
        listen: jasmine.createSpy('listen')
      }
    } as any;

    ngZone = {
      runOutsideAngular: jasmine.createSpy().and.callFake(fn => fn())
    } as any;

    spyOn<any>(global, 'requestAnimationFrame').and.callFake((fn: Function) => {
      fn();
    });
    directive = new NgCarouselDirective(domToolsService,
      carouselService, elementRef, windowRef, deviceService, rendererService, ngZone);

    directive.slides = [];
    directive['scrollWidth'] = 100;
  });

  describe('ngOnInit', () => {
    it('should init ngCarouselMoveThresholdPercentage', () => {
      directive.ngCarouselMoveThresholdPercentage = undefined;

      directive.ngOnInit();

      expect(directive.ngCarouselMoveThresholdPercentage).toEqual(directive['MOVE_TRESHOLD_PERCENTAGE']);
    });

    it('should not init ngCarouselMoveThresholdPercentage', () => {
      directive.ngCarouselMoveThresholdPercentage = 50;

      directive.ngOnInit();

      expect(directive.ngCarouselMoveThresholdPercentage).not.toEqual(directive['MOVE_TRESHOLD_PERCENTAGE']);
    });
  });

  describe('ngOnChanges', () => {
    let changes;
    beforeEach(() => {
      directive.refreshInteractionWithDom = jasmine.createSpy('refreshInteractionWithDom');
      changes = {
        ngCarouselWatch: true
      } as any;
    });

    it('should call refreshInteractionWithDom', () => {
      changes.ngCarouselWatch = true;

      directive.ngOnChanges(changes);

      expect(directive.refreshInteractionWithDom).toHaveBeenCalled();
    });

    it('should not call refreshInteractionWithDom', fakeAsync(() => {
      changes.ngCarouselWatch = false;

      directive.ngOnChanges(changes);
      tick();

      expect(directive.refreshInteractionWithDom).not.toHaveBeenCalled();
    }));
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  describe('ngAfterViewInit', () => {
    beforeEach(() => {
      directive.carouselPress = jasmine.createSpy('carouselPress');
      directive.carouselRelease = jasmine.createSpy('carouselRelease');
      directive.setNextSlideTimeout = jasmine.createSpy('setNextSlideTimeout');
      rendererService.renderer.listen.and.callFake((a, b, cb) => cb());
    });

    it('should init options', () => {
      directive.ngAfterViewInit();

      expect(directive.name).toEqual(directive.ngCarouselName);
      expect(directive.interval).toEqual(directive.ngCarouselTimer);
      expect(directive.random).toEqual(directive.ngCarouselRandom);
      expect(directive.looping).toEqual(directive.ngCarouselLoop);
      expect(directive.fluid).toEqual(directive.ngCarouselFluid);
      expect(directive.activeClass).toEqual(directive.ngCarouselActiveClass);
      expect(directive.centerMode).toEqual(directive.ngCenterMode);
      expect(directive.stopSlidesOnHover).toEqual(directive.ngStopSlideOnHover);
      expect(directive.amount).toEqual(typeof (directive.ngCarouselAmount) !== 'undefined' ? directive.ngCarouselAmount : 1);
    });

    it('should define mouse listeners', () => {
      directive.ngAfterViewInit();

      expect(directive.mouseListeners.length).toBeDefined();
      expect(directive.rendererService.renderer.listen).toHaveBeenCalledWith(
        directive.elementRef.nativeElement,
        jasmine.any(String),
        jasmine.any(Function));

      expect(directive.carouselPress).toHaveBeenCalled();
      expect(directive.carouselRelease).toHaveBeenCalled();
      expect(directive.setNextSlideTimeout).toHaveBeenCalled();
    });

    it('should clear timeout on mouseover', () => {
      directive.timeoutPromise = () => {
      };
      directive.ngStopSlideOnHover = true;
      directive.ngAfterViewInit();

      expect(directive.timeoutPromise).toBeDefined();
      expect(directive.windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(directive.timeoutPromise);
      expect(directive.stopSlidesOnHover).toBe(true);
      expect(directive.toggleSliding).toBe(false);
    });

    it('should not clear timeout on mouseover', () => {
      directive.timeoutPromise = undefined;

      directive.ngAfterViewInit();

      expect(directive.timeoutPromise).not.toBeDefined();
      expect(directive.windowRef.nativeWindow.clearTimeout).not.toHaveBeenCalledWith(directive.timeoutPromise);
    });

    it('should not pause on mouse leave', () => {
      directive.ngStopSlideOnHover = false;
      directive.ngAfterViewInit();
      expect(directive.stopSlidesOnHover).toBe(false);
      expect(directive.toggleSliding).toBe(false);
      expect(directive.setNextSlideTimeout).toHaveBeenCalled();
    });

    it('should set directive.amount 1', () => {
      directive.ngAfterViewInit();
      expect(directive.amount).toEqual(1);
    });

    it('should set directive.amount 1', () => {
      directive.ngCarouselAmount = 5;
      directive.ngAfterViewInit();
      expect(directive.amount).toEqual(5);
    });

  });

  it('setAttribute', () => {
    directive.amount = 5;
    directive.slideContainer = 'carousel-container' as any;
    spyOn(directive.activeSlideIndex, 'emit');
    directive.move(1, false);
    expect(domToolsService.css).toHaveBeenCalledWith('carousel-container',
      {
        '-ms-transform': 'translate3d(-20%, 0, 0)',
        '-webkit-transform': 'translate3d(-20%, 0, 0)',
        'transform': 'translate3d(-20%, 0, 0)'
      });
    expect(directive.activeSlideIndex.emit).toHaveBeenCalledWith(1);
  });

  describe('#touchHorizScroll', () => {
    let element;
    beforeEach(() => {
      element = {
        scrollLeft: 5,
        scrollTop: 0,
        addEventListener: () => {
        },
        removeEventListener: () => {
        },
      };
    });
    it('should call fromEvent', () => {
      directive.isTouchDevice = jasmine.createSpy('isTouchDevice').and.returnValue(false);
      directive.touchHorizScroll(element);
    });
  });

  describe('move', () => {
    beforeEach(() => {
      directive.slides = [1, 2, 3] as any;
      directive.slideContainer = document.createElement('div');
      spyOn<any>(directive.activeSlideIndex, 'emit');
      spyOn(directive, 'toggleActiveClass');
      directive.rendererService = {
        renderer: {
          addClass: jasmine.createSpy('addClass'),
          removeClass: jasmine.createSpy('removeClass'),
          listen: jasmine.createSpy('listen')
        }
      } as any;
    });

    it('should animate move and add callbacks', () => {
      directive.move(0, true, jasmine.createSpy('callbackFunction'));

      expect(requestAnimationFrame).toHaveBeenCalledWith(jasmine.any(Function));
      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(directive.slideContainer, 'carousel-animate');
      expect(directive.rendererService.renderer.removeClass).toHaveBeenCalledWith(directive.slideContainer, 'carousel-is-sliding');
      expect(directive.rendererService.renderer.listen).toHaveBeenCalledTimes(2);
      expect(directive.activeSlideIndex.emit).toHaveBeenCalledWith(0);
    });

    it('should animate move without adding callbacks', () => {
      directive.move(0, true);

      expect(requestAnimationFrame).toHaveBeenCalledWith(jasmine.any(Function));
      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(directive.slideContainer, 'carousel-animate');
      expect(directive.rendererService.renderer.removeClass).toHaveBeenCalledWith(directive.slideContainer, 'carousel-is-sliding');
      expect(directive.rendererService.renderer.listen).not.toHaveBeenCalled();
      expect(directive.activeSlideIndex.emit).toHaveBeenCalledWith(0);
    });

    it('should not animate', () => {
      directive.move(0, false);

      expect(requestAnimationFrame).toHaveBeenCalledWith(jasmine.any(Function));
      expect(directive.rendererService.renderer.addClass).not.toHaveBeenCalled();
      expect(directive.rendererService.renderer.removeClass)
        .not.toHaveBeenCalledWith(jasmine.any(Object), 'carousel-is-sliding');
      expect(directive.rendererService.renderer.listen).not.toHaveBeenCalled();
      expect(directive.activeSlideIndex.emit).toHaveBeenCalledWith(0);
    });

    it('should add event listener', () => {
      directive.move(0, true, jasmine.createSpy('callbackFunction'));

      expect(directive.animationListeners.length).toEqual(2);
      expect(directive.rendererService.renderer.listen).toHaveBeenCalledTimes(2);
    });

    it('should not add event listener', () => {
      directive.move(0, true);

      expect(directive.animationListeners.length).toEqual(0);
      expect(directive.rendererService.renderer.listen).not.toHaveBeenCalled();
    });

    describe(`should pass circle`, () => {
      it(`if wrap right`, () => {
        directive.move(4, true);
      });
      it(`if wrap left`, () => {
        directive.move(0, true);
      });

      afterEach(() => {
        expect(directive['isCirclePassed']).toBeTruthy();
        expect(directive.rendererService.renderer.removeClass)
          .toHaveBeenCalledWith(directive.slideContainer, 'circle-not-passed');
      });
    });

    describe(`should NOT pass circle`, () => {
      it(`if isCirclePassed`, () => {
        directive['isCirclePassed'] = true;

        directive.move(4, true);
      });
      it(`if not wrap`, () => {
        directive.move(1, false);
      });

      afterEach(() => {
        expect(directive.rendererService.renderer.removeClass)
          .not.toHaveBeenCalledWith(directive.slideContainer, 'circle-not-passed');
      });
    });

    it(`should add active class to first slide`, () => {
      directive['firstSlideCopy'] = { id: 'firstSlideCopy' } as any;
      directive.move(4, false);

      expect(directive['activeIndex']).toEqual(0);
      expect(directive.toggleActiveClass).toHaveBeenCalledWith(0, directive['firstSlideCopy']);
    });

    it(`should add active class to last slide`, () => {
      directive['lastSlideCopy'] = { id: 'lastSlideCopy' } as any;
      directive.move(0, false);

      expect(directive['activeIndex']).toEqual(2);
      expect(directive.toggleActiveClass).toHaveBeenCalledWith(2, directive['lastSlideCopy']);
    });

    it(`should Not set activeIndex and addActiveClass if slideIndex is Not integer`, () => {
      directive['activeIndex'] = null;
      directive.move(4.123, true);

      expect(directive['activeIndex']).toBeNull();
      expect(directive.toggleActiveClass).not.toHaveBeenCalled();
    });

    it(`should consider 2 slide copies for transform rules`, () => {
      const transform = 'translate3d(-300%, 0, 0)';
      directive.secondSlideCopy = { id: 1 } as any;
      directive['scrollWidth'] = 100;
      directive['amount'] = 1;

      directive.move(2, false);
      expect(domToolsService.css).toHaveBeenCalledWith(directive.slideContainer, jasmine.objectContaining({ transform }));
    });

    it(`should Not consider 2 slide copies for transform rules`, () => {
      const transform = 'translate3d(-200%, 0, 0)';
      directive['scrollWidth'] = 100;
      directive['amount'] = 1;

      directive.move(2, false);
      expect(domToolsService.css).toHaveBeenCalledWith(directive.slideContainer, jasmine.objectContaining({ transform }));
    });
  });

  describe('toggleActiveClass', () => {
    beforeEach(() => {
      directive.slides = [{ id: 1 }, { id: 2 }] as any;
      directive.activeIndex = 0;
      directive.activeClass = 'active';
    });
    describe('should Not add class', () => {
      it(`not activeClass`, () => {
        delete directive.activeClass;
        directive.toggleActiveClass(1, { id: 1 } as any);

        expect(directive.rendererService.renderer.addClass).not.toHaveBeenCalled();
      });

      it(`to slideCopy if it not exist`, () => {
        directive.toggleActiveClass(1);

        expect(directive.rendererService.renderer.addClass).toHaveBeenCalledTimes(1);
      });
    });

    describe('should add class', () => {
      it(`to slide copy`, () => {
        const slideCopy = { id: 11 } as any;

        directive.toggleActiveClass(1, slideCopy);

        expect(directive.rendererService.renderer.addClass)
          .toHaveBeenCalledWith(slideCopy, directive.activeClass);
      });

      it(`to active slide`, () => {
        const slideCopy = { id: 11 } as any;

        directive.toggleActiveClass(1, slideCopy);

        expect(directive.rendererService.renderer.addClass)
          .toHaveBeenCalledWith(directive.slides[1], directive.activeClass);
        expect(directive.rendererService.renderer.removeClass)
          .toHaveBeenCalledWith(directive.slides[0], directive.activeClass);
      });
    });
  });

  describe('carouselDrag', () => {
    beforeEach(() => {
      directive.currentCarousel = {
        currentSlide: 0
      } as any;
      directive.width = 50;
    });

    it('should calculate deltas', () => {
      directive.carouselDrag(100);

      expect(directive.deltaXFactor).toBeDefined();
    });

    it('should call rendererService.renderer.addClass', () => {
      directive.carouselDrag(100);

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.slideContainer, 'carousel-is-sliding');
    });

    it('should call move', () => {
      directive.move = jasmine.createSpy('move');

      directive.carouselDrag(100);

      expect(directive.move).toHaveBeenCalledWith(0, false);
    });
  });

  describe('refreshInteractionWithDom', () => {
    it('should initiate with "ng-carousel" class', () => {
      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.elementRef.nativeElement, 'ng-carousel');
    });

    it('should initiate with "ng-carousel" class', () => {
      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.slideContainer, 'circle-not-passed');
    });

    it('should Not add  "center-mode" class if not centerMode', () => {
      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).not.toHaveBeenCalledWith(
        directive.slideContainer, 'center-mode');
    });

    it('should add "center-mode" class if centerMode', () => {
      directive.centerMode = true;
      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.slideContainer, 'center-mode');
    });

    it('should add "activeClass" class if activeClass', () => {
      directive.activeClass = 'active';
      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.slides[0], directive.activeClass);
    });

    describe('scrollWidth === undefined', () => {
      beforeEach(() => {
        carouselService.add = jasmine.createSpy().and.returnValue({ onSlideChange: jasmine.createSpy() } as any);
        spyOn(directive, 'removeOldVirtualSlides');
        spyOn(directive, 'refreshVirtualSlides');
        spyOn(directive, 'onSlideChangeCallback');
        spyOn(directive, 'touchHorizScroll');

        elementRef.nativeElement.querySelectorAll.and.returnValue([{ offsetWidth: 600 }, {}] as any);
        elementRef.nativeElement.querySelector.and.returnValue({ offsetWidth: 1000 } as any);
        delete directive['scrollWidth'];
      });

      it(`should define scrollWidth as 100`, () => {
        directive.elementRef.nativeElement.querySelectorAll
          .and.returnValue([{ offsetWidth: 600 }] as any);
        directive.refreshInteractionWithDom();

        expect(directive['scrollWidth']).toEqual(100);
        expect(directive['isAdditionalCopies']).toBeFalsy();
      });

      it(`isAdditionalCopies should be truthy if more than 2 slides`, () => {
        directive.centerMode = true;
        elementRef.nativeElement.querySelectorAll.and.returnValue([{ offsetWidth: 600 }, {}, {}] as any);
        directive.refreshInteractionWithDom();

        expect(directive['isAdditionalCopies']).toBeTruthy();
      });

      it(`isAdditionalCopies should be truthy`, () => {
        directive.centerMode = true;
        directive.refreshInteractionWithDom();

        expect(directive['isAdditionalCopies']).toBeTruthy();
      });

      it(`should define scrollWidth as 60`, () => {
        directive.slidesToScroll = 1;
        directive.refreshInteractionWithDom();

        expect(directive['scrollWidth']).toEqual(60);
        expect(directive['isAdditionalCopies']).toBeTruthy();
      });
    });

    it('should initiate with "carousel-touch" class', () => {
      directive.isTouchDevice = jasmine.createSpy().and.callFake(() => true);

      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.elementRef.nativeElement, 'carousel-touch');
    });

    it('should initiate with "carousel-no-touch" class', () => {
      directive.isTouchDevice = jasmine.createSpy().and.callFake(() => false);

      directive.refreshInteractionWithDom();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.elementRef.nativeElement, 'carousel-no-touch');
    });

    it('should call remove', () => {
      carouselService.get = jasmine.createSpy().and.returnValue({
        currentSlide: 1,
        onSlideChangeCallbacks: []
      });
      directive.name = 'name';
      directive.refreshInteractionWithDom();
      expect(carouselService.remove).toHaveBeenCalled();
    });

    it('should create carousel', () => {
      const callback = jasmine.createSpy();

      carouselService.get = jasmine.createSpy().and.returnValue({
        currentSlide: 1,
        onSlideChangeCallbacks: [callback]
      });
      carouselService.add = jasmine.createSpy().and.returnValue({
        slidesCount: 5,
        onSlideChange: fn => fn(),
        unbindOnSlideChangeCallback: () => {},
        toIndex: () => {},
        next: () => {}
      });
      elementRef.nativeElement.querySelector = jasmine.createSpy().and.returnValue({
        appendChild: () => {}
      });
      elementRef.nativeElement.querySelectorAll = jasmine.createSpy().and.returnValue([{
        parentNode: {
          removeChild: jasmine.createSpy(),
          insertBefore: jasmine.createSpy()
        }
      }]);
      directive.name = 'name';
      directive.random = true;
      directive.interval = 1;
      directive.touchHorizScroll = jasmine.createSpy();

      directive.refreshInteractionWithDom();

      expect(carouselService.add).toHaveBeenCalled();
    });
  });

  describe('refreshVirtualSlides', () => {
    const classIgnore = 'carousel-ignore-first-slide';
    const classCopy = 'carousel-slide-copy';
    beforeEach(() => {
      directive.slideContainer = {
        appendChild: jasmine.createSpy('appendChild')
      } as any;
      elementRef.nativeElement.querySelectorAll = jasmine.createSpy().and.returnValue([{
        dataset: jasmine.createSpyObj('dataset', ['eventid']),
        parentNode: jasmine.createSpyObj('parentNode', ['insertBefore'])
      }]);
      directive.removeOldVirtualSlides = jasmine.createSpy();
      directive['cloneSlides'] = jasmine.createSpy('cloneSlides');
      directive['makeClonedSlidesEmpty'] = jasmine.createSpy('makeFirstAndLastSlideEmpty');

      directive.lastSlideCopy = { id: 'lastSlideCopy' } as any;
      directive.firstSlideCopy = { id: 'firstSlideCopy' } as any;
      directive.secondSlideCopy = { id: 'secondSlideCopy' } as any;
      directive.beforeLastSlideCopy = { id: 'beforeLastSlideCopy' } as any;
    });

    it(`should insert lastSlideCopy`, () => {
      directive.refreshVirtualSlides();

      expect(directive.slides[0].parentNode.insertBefore)
        .toHaveBeenCalledWith(directive.lastSlideCopy, directive.slides[0]);
    });

    it(`should add carousel-ignore-first-slide`, () => {
      directive.refreshVirtualSlides();

      expect(rendererService.renderer.addClass)
        .toHaveBeenCalledWith(directive.slideContainer, classIgnore);
      expect(directive.slideContainer.appendChild).not.toHaveBeenCalledWith(directive.secondSlideCopy);
      expect(directive.slides[0].parentNode.insertBefore)
        .not.toHaveBeenCalledWith(directive.beforeLastSlideCopy, directive.slides[0]);
    });

    it(`should add additional copies`, () => {
      directive['isAdditionalCopies'] = true;

      directive.refreshVirtualSlides();

      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(directive.secondSlideCopy, classCopy);
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(directive.beforeLastSlideCopy, classCopy);
      expect(directive.slideContainer.appendChild).toHaveBeenCalledWith(directive.secondSlideCopy);
      expect(directive.slides[0].parentNode.insertBefore)
        .toHaveBeenCalledWith(directive.beforeLastSlideCopy, directive.slides[0]);
      expect(rendererService.renderer.addClass)
        .not.toHaveBeenCalledWith(directive.slideContainer, classIgnore);
    });

    it('should call cloneSlides', () => {
      directive.looping = true;

      directive.refreshVirtualSlides();

      expect(directive['cloneSlides']).toHaveBeenCalled();
      expect(directive['makeClonedSlidesEmpty']).not.toHaveBeenCalled();
    });

    it('should call makeClonedSlidesEmpty', () => {
      directive.looping = false;

      directive.refreshVirtualSlides();

      expect(directive['makeClonedSlidesEmpty']).toHaveBeenCalled();
      expect(directive['cloneSlides']).not.toHaveBeenCalled();
    });

    it('should add "carousel-slide-copy" class', () => {
      directive.refreshVirtualSlides();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.firstSlideCopy, 'carousel-slide-copy');
      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.lastSlideCopy, 'carousel-slide-copy');
    });

    it('should add "carousel-ignore-first-slide" class', () => {
      directive.refreshVirtualSlides();

      expect(directive.rendererService.renderer.addClass).toHaveBeenCalledWith(
        directive.slideContainer, 'carousel-ignore-first-slide');
    });
  });

  describe('onSlideChangeCallback', () => {
    beforeEach(() => {
      directive.slideContainer = document.createElement('div');
      directive.slides = [{}, {}] as any;
      directive.currentCarousel = {} as any;

      directive.rendererService = {
        renderer: {
          addClass: jasmine.createSpy('addClass'),
          removeClass: jasmine.createSpy('removeClass')
        }
      } as any;

      spyOn(directive, 'setNextSlideTimeout');
      spyOn(directive, 'refreshVirtualSlides');
      spyOn(directive, 'move').and.callFake((slideIndex, animate, callback) => {
        if (typeof callback === 'function') {
          callback();
        }
      });
    });

    it('should remove carousel-animate class on callback if wrapping left', () => {
      directive.centerMode = true;
      directive.onSlideChangeCallback(0, 'left');

      expect(directive.rendererService.renderer.removeClass).toHaveBeenCalledWith(directive.slideContainer, 'carousel-animate');
      expect(directive.move).toHaveBeenCalledTimes(2);
      expect(directive.refreshVirtualSlides).toHaveBeenCalledTimes(1);
    });

    it('should remove carousel-animate class on callback if wrapping right', () => {
      directive.onSlideChangeCallback(0, 'right');

      expect(directive.rendererService.renderer.removeClass).toHaveBeenCalledWith(directive.slideContainer, 'carousel-animate');
      expect(directive.move).toHaveBeenCalledTimes(2);
      expect(directive.refreshVirtualSlides).toHaveBeenCalledTimes(1);
    });

    it('should not remove carousel-animate class on callback if wrapping not left or right', () => {
      directive.onSlideChangeCallback(0, 'any_other');

      expect(directive.rendererService.renderer.removeClass).not.toHaveBeenCalled();
      expect(directive.move).toHaveBeenCalledTimes(1);
    });
  });

  describe('ngOnDestroy', () => {
    it('should clear mouseListeners', () => {
      const callback = jasmine.createSpy();
      directive.mouseListeners.push(callback);
      directive.ngOnDestroy();
      expect(directive.mouseListeners.length).toEqual(0);
      expect(callback).toHaveBeenCalled();
    });
    it('should clear animationListeners', () => {
      directive.slideContainer = {} as any;
      directive.currentCarousel = {} as any;
      const callback = jasmine.createSpy();
      directive.animationListeners = [callback];
      directive.ngOnDestroy();
      expect(directive.animationListeners.length).toEqual(0);
      expect(callback).toHaveBeenCalled();
    });
  });

  describe('setNextSlideTimeout', () => {
    it('should clear timeoutPromise', () => {
      directive.interval = 1;
      directive.timeoutPromise = 999;
      directive.setNextSlideTimeout();
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(999);
    });
    it('should set timeoutPromise', () => {
      directive.interval = 1;
      directive.currentCarousel = {
        next: jasmine.createSpy('next'),
        slidesCount: 5
      } as any;
      directive.setNextSlideTimeout();
      expect(directive.currentCarousel.next).toHaveBeenCalled();
    });
    it('when toggleSliding is true', () => {
      directive.interval = 1;
      directive.timeoutPromise = 999;
      directive.toggleSliding = true;
      directive.setNextSlideTimeout();
      expect(directive.toggleSliding).toBe(true);
    });
    it('when toggleSliding is false', () => {
      directive.interval = 1;
      directive.timeoutPromise = 999;
      directive.toggleSliding = false;
      directive.setNextSlideTimeout();
      expect(directive.toggleSliding).toBe(false);
    });
  });

  describe('slideContainerTransitionAnimation', () => {
    let callback;
    let listener;
    beforeEach(() => {
      callback = jasmine.createSpy('callback');
      listener = jasmine.createSpy('listener');
      directive.animationListeners = [listener];
    });

    describe('should call callback', () => {
      it('if no event', () => {
        directive.slideContainerTransitionAnimation(callback)();
      });
      it('if event equal transitionProperty', () => {
        const event = { propertyName: directive['transitionProperty'] };
        directive.slideContainerTransitionAnimation(callback)(event);
      });

      afterEach(() => {
        expect(callback).toHaveBeenCalled();
        expect(listener).toHaveBeenCalled();
        expect(directive.animationListeners.length).toEqual(0);
      });
    });

    it('should Not call callback if event is not transition', () => {
      const event = { propertyName: 'min-height' };
      directive.slideContainerTransitionAnimation(callback)(event);
      expect(callback).not.toHaveBeenCalled();
      expect(listener).not.toHaveBeenCalled();
      expect(directive.animationListeners.length).toEqual(1);
    });
  });

  describe('carouselPress', () => {
    it('should set width', () => {
      directive.width = 0;
      directive.slideContainer = { offsetWidth: 1 } as any;
      directive.carouselPress();
      expect(directive.width).toEqual(1);
    });
  });

  describe('carouselRelease', () => {
    beforeEach(() => {
      directive.currentCarousel = {
        previous: jasmine.createSpy(),
        next: jasmine.createSpy()
      } as any;
    });
    it('should call previous', () => {
      directive.deltaXFactor = 0.5;
      directive.ngOnInit();
      directive.carouselRelease();
      expect(directive.currentCarousel.previous).toHaveBeenCalled();
    });
    it('should call next', () => {
      directive.deltaXFactor = -0.5;
      directive.ngOnInit();
      directive.carouselRelease();
      expect(directive.currentCarousel.next).toHaveBeenCalled();
    });
    it('should call next', () => {
      directive.deltaXFactor = -0.1;
      directive.move = jasmine.createSpy().and.callFake((x, y, fn) => fn());
      directive.ngOnInit();
      directive.carouselRelease();
      expect(directive.move).toHaveBeenCalled();
    });
  });

  describe('removeOldVirtualSlides', () => {
    it('should remove children', () => {
      const method = jasmine.createSpy();
      elementRef.nativeElement.querySelectorAll = jasmine.createSpy().and.returnValue([
        { parentNode: { removeChild: method } }
      ]);
      directive.removeOldVirtualSlides();
      expect(method).toHaveBeenCalled();
    });
  });

  describe('getPageX, getPageY', () => {
    let event;
    beforeEach(() => {
      event = { pageX: 1, pageY: 3, touches: [{ pageX: 2, pageY: 4 }] };
    });
    it('should return 2 and 4', () => {
      windowRef.nativeWindow.ontouchstart = {};
      expect(directive.getPageX(event)).toEqual(2);
      expect(directive.getPageY(event)).toEqual(4);
    });
    it('should return 1 and 3', () => {
      expect(directive.getPageX(event)).toEqual(1);
      expect(directive.getPageY(event)).toEqual(3);
    });
  });

  describe('isVerticalSwipe', () => {
    it('should return true', () => {
      expect(directive.isVerticalSwipe(0, 100, 0, 0)).toEqual(true);
    });
    it('should return false', () => {
      expect(directive.isVerticalSwipe(0, 100, 0, 50)).toEqual(false);
    });
    it('should return false too', () => {
      expect(directive.isVerticalSwipe(0, 10, 0, 0)).toEqual(false);
    });
  });

  describe('cloneSlides', () => {
    it('should create slides', () => {
      directive.slides = [{ dataset: {} }, { dataset: {} }] as any;
      directive['cloneSlides']();
      expect(directive.firstSlideCopy).toBeTruthy();
      expect(directive.lastSlideCopy).toBeTruthy();
      expect(directive.secondSlideCopy).toBeFalsy();
      expect(directive.beforeLastSlideCopy).toBeFalsy();
    });

    it(`should create additional copies`, () => {
      directive.slides = [{ dataset: {} }, { dataset: {} }] as any;
      directive['isAdditionalCopies'] = true;

      directive['cloneSlides']();

      expect(directive.secondSlideCopy).toBeTruthy();
      expect(directive.beforeLastSlideCopy).toBeTruthy();
    });
  });

  describe('makeClonedSlidesEmpty', () => {
    it('should create slides', () => {
      directive['makeClonedSlidesEmpty']();
      expect(directive.firstSlideCopy).toBeTruthy();
      expect(directive.lastSlideCopy).toBeTruthy();
      expect(directive.secondSlideCopy).toBeFalsy();
      expect(directive.beforeLastSlideCopy).toBeFalsy();
    });

    it('should create additional slides', () => {
      directive['isAdditionalCopies'] = true;

      directive['makeClonedSlidesEmpty']();

      expect(directive.firstSlideCopy).toBeTruthy();
      expect(directive.lastSlideCopy).toBeTruthy();
      expect(directive.secondSlideCopy).toBeTruthy();
      expect(directive.beforeLastSlideCopy).toBeTruthy();
    });
  });

  describe('touchHorizScroll', () => {
    it('should run event handlers', () => {
      const callback = [];
      const element = {
        scrollLeft: 0,
        scrollTop: 0,
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((e, h) => callback.push(h)),
        removeEventListener: jasmine.createSpy('removeEventListener')
      };
      directive.touchHorizScroll(element as any);
      callback.forEach(f => f({ pageX: 1 } as MouseEvent));
      expect(callback.length).toBeGreaterThan(0);
    });

    it('should run event handlers', () => {
      spyOn(directive, 'isVerticalSwipe'). and.returnValue(true)
      spyOn(directive, 'carouselDrag').and.callThrough();
      spyOn(directive, 'move').and.callThrough();
      directive.currentCarousel = {
        currentSlide: 0
      } as any;
      directive.ngDisableCarouselDragOnCenterMode = false
      const callback = [];
      const element = {
        scrollLeft: 0,
        scrollTop: 0,
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((e, h) => callback.push(h)),
        removeEventListener: jasmine.createSpy('removeEventListener')
      };
      directive.touchHorizScroll(element as any);
      callback.forEach(f => f({ pageX: 1 } as MouseEvent));
      expect(callback.length).toBeGreaterThan(0);
    });
  });
});
