import { NgCarouselExtendedDirective } from '@shared/directives/ng-carousel-extended/carousel.directive';

describe('NgCarouselExtendedDirective', () => {
  let directive: NgCarouselExtendedDirective,
    domToolsService,
    carouselService,
    elementRef,
    windowRef,
    deviceService,
    rendererService,
    ngZone;

  beforeEach(() => {
    domToolsService = {
      css: jasmine.createSpy()
    };
    carouselService = {
      get: jasmine.createSpy('carouselService.get'),
      remove: jasmine.createSpy('carouselService.remove'),
      add: jasmine.createSpy('carouselService.add')
    };
    elementRef = {};
    windowRef = {
      nativeWindow: {
        document: {
          createElement: jasmine.createSpy('createElement')
        },
        MaxTouchPoints: jasmine.createSpy('MaxTouchPoints'),
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        innerWidth: 500
      }
    };
    deviceService = {};
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass'),
        listen: jasmine.createSpy('listen')
      }
    };
    ngZone = {
      runOutsideAngular: jasmine.createSpy()
    };

    spyOn(console, 'log');

    directive = new NgCarouselExtendedDirective(
      domToolsService,
      carouselService,
      elementRef,
      windowRef,
      deviceService,
      rendererService,
      ngZone
    );
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  describe('ngAfterViewInit', () => {
    beforeEach(() => {
      directive.refreshInteractionWithDom = jasmine.createSpy('refreshInteractionWithDom');
    });

    it('should set default value', () => {
      directive.ngCarouselAmount = 20;

      directive.ngAfterViewInit();

      expect(directive.amount).toEqual(20);
    });

    it('should call refreshInteractionWithDom and set defined values', () => {
      directive.ngCarouselName = 'ngCarouselName';
      directive.ngCarouselTimer = 200;
      directive.ngCarouselLoop = true;
      directive.ngCarouselFluid = true;

      directive.ngAfterViewInit();

      expect(directive.name).toEqual('ngCarouselName');
      expect(directive.interval).toEqual(200);
      expect(directive.looping).toEqual(true);
      expect(directive.fluid).toEqual(true);
      expect(directive.amount).toEqual(1);
      expect(directive.refreshInteractionWithDom).toHaveBeenCalled();
    });
  });

  describe('carouselDrag', () => {
    beforeEach(() => {
      directive.slideContainer = {} as any;
      directive.startPosition = 10;
      directive.width = 10;
      directive['touchScroll'] = jasmine.createSpy('touchScroll');
    });

    it('should set deltaXFactor to 1 when delta > 1', () => {
      directive.carouselDrag(20);

      expect(directive.deltaXFactor).toEqual(1);
      expect(directive['touchScroll']).toHaveBeenCalledWith(30);
    });

    it('should set deltaXFactor to -1 when delta < -1', () => {
      directive.carouselDrag(-20);

      expect(directive.deltaXFactor).toEqual(-1);
      expect(directive['touchScroll']).toHaveBeenCalledWith(-10);
    });

    it('should use deltaXFactor when  -1 < delta < 1', () => {
      directive.carouselDrag(5);

      expect(directive.deltaXFactor).toEqual(0.5);
      expect(directive['touchScroll']).toHaveBeenCalledWith(15);
    });

    afterEach(() => {
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith({}, 'carousel-is-sliding');
    });
  });

  describe('slideContainerTransitionAnimation', () => {
    const transitionEndCallback = jasmine.createSpy('transitionEndCallback');
    let result;

    beforeEach(() => {
      directive.currentCarousel = {
        currentSlide: 0
      } as any;
      directive['animate'] = jasmine.createSpy('animate');
      result = directive.slideContainerTransitionAnimation(transitionEndCallback);
    });

    it('should call transitionEndCallback', () => {
      result();

      expect(transitionEndCallback).toHaveBeenCalled();
    });

    it('should call each animationListener', () => {
      const animationListener = jasmine.createSpy('animationListeners');

      directive.animationListeners.push(animationListener);

      result();

      expect(animationListener).toHaveBeenCalled();
      expect(directive.animationListeners).toEqual([]);
    });

    afterEach(() => {
      expect(directive['animate']).toHaveBeenCalledWith(1);
    });
  });

  describe('carouselRelease', () => {
    beforeEach(() => {
      directive.currentCarousel = {
        previous: jasmine.createSpy('currentCarousel.previous'),
        next: jasmine.createSpy('currentCarousel.next'),
        currentSlide: 0
      } as any;
      directive['animate'] = jasmine.createSpy('animate').and.callFake(() => {
        directive.deltaXFactor = 0;
      });
    });

    it('should go to previous slide when user dragged right', () => {
      directive.ngCarouselMoveThresholdPercentage = 10;
      directive.deltaXFactor = 10;

      directive.carouselRelease();

      expect(directive.currentCarousel.previous).toHaveBeenCalled();
      expect(directive.deltaXFactor).toEqual(0);
    });

    it('should go to next slide when user dragged left', () => {
      directive.ngCarouselMoveThresholdPercentage = -1000;
      directive.deltaXFactor = -1;

      directive.carouselRelease();

      expect(directive.currentCarousel.next).toHaveBeenCalled();
      expect(directive.deltaXFactor).toEqual(0);
    });

    it('should animate to next slide if deltaXFactor gt 0', () => {
      directive.ngCarouselMoveThresholdPercentage = 1000;
      directive.deltaXFactor = 1;

      directive.carouselRelease();

      expect(directive['animate']).toHaveBeenCalledWith(1, jasmine.any(Function));
    });

    it('should animate to next slide if deltaXFactor lt 0', () => {
      directive.ngCarouselMoveThresholdPercentage = 1000;
      directive.deltaXFactor = -1;

      directive.carouselRelease();

      expect(directive['animate']).toHaveBeenCalledWith(1, jasmine.any(Function));
      expect(directive.deltaXFactor).toEqual(0);
    });
  });

  describe('refreshInteractionWithDom', () => {
    beforeEach(() => {
      directive.name = undefined;
      directive.isCarouselInit.emit = jasmine.createSpy('emit');
      directive.elementRef = {
        nativeElement: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue(undefined),
          querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([])
        }
      };
      directive.removeOldVirtualSlides = jasmine.createSpy('removeOldVirtualSlides');
    });

    describe('should check device type and', () => {
      it('add class for touch device', () => {
        directive.isTouchDevice = jasmine.createSpy('isTouchDevice').and.returnValue(true);

        directive.refreshInteractionWithDom();

        expect(rendererService.renderer.addClass)
          .toHaveBeenCalledWith(directive.elementRef.nativeElement, 'carousel-touch');
      });

      it('add class for non-touch device', () => {
        directive.isTouchDevice = jasmine.createSpy('isTouchDevice').and.returnValue(false);

        directive.refreshInteractionWithDom();

        expect(rendererService.renderer.addClass)
          .toHaveBeenCalledWith(directive.elementRef.nativeElement, 'carousel-no-touch');
      });
    });

    it('should notify about ng-carousel error', () => {
      directive.refreshInteractionWithDom();

      expect((console as any).log).toHaveBeenCalledWith('ng-carousel error: No slides found');
      expect((console as any).log).toHaveBeenCalledWith('ng-carousel error: No slidecontainer found');
    });

    it('should Initialize left right logic', () => {
      directive['touchHorizScroll'] = jasmine.createSpy('touchHorizScroll');
      directive.elementRef.nativeElement.querySelector.and.returnValue({});

      directive.refreshInteractionWithDom();

      expect(directive['touchHorizScroll']).toHaveBeenCalled();
    });

    it('should process carousel name with carouselService', () => {
      directive.name = 'carouselName';
      carouselService.get.and.returnValue({});

      directive.refreshInteractionWithDom();

      expect(carouselService.get).toHaveBeenCalledTimes(3);
      expect(carouselService.get).toHaveBeenCalledWith('carouselName');
      expect(carouselService.remove).toHaveBeenCalledWith('carouselName');
    });

    describe('should process slides: ', () => {
      beforeEach(() => {
        directive.name = 'carouselName';
        directive.looping = true;
        directive.elementRef.nativeElement.querySelectorAll.and.returnValue([{}, {}]);
        directive.refreshVirtualSlides = jasmine.createSpy('refreshVirtualSlides');
        directive.amount = 10;
      });

      it('change slide and unbindOnSlideChangeCallback', () => {
        carouselService.get.and.returnValue({
          currentSlide: 2,
          onSlideChangeCallbacks: [jasmine.any(Function)]
        });
        carouselService.add.and.returnValue({
          getSlidesQuantity: jasmine.createSpy('getSlidesQuantity').and.returnValue(2),
          onSlideChange: jasmine.createSpy('onSlideChange'),
          unbindOnSlideChangeCallback: jasmine.createSpy('unbindOnSlideChangeCallback'),
          currentSlide: 2,
          toIndex: jasmine.createSpy('toIndex')
        });
        directive.fluid = true;

        directive.refreshInteractionWithDom();

        expect(directive.currentCarousel.amount).toEqual(10);
        expect(directive.currentCarousel.fluid).toBeTruthy();
        expect(directive.currentCarousel.quantity).toEqual(2);
        expect(directive.currentCarousel.onSlideChange).toHaveBeenCalledWith(jasmine.any(Function));
        expect(directive.currentCarousel.onSlideChange).toHaveBeenCalledTimes(2);
        expect(directive.currentCarousel.unbindOnSlideChangeCallback).toHaveBeenCalledWith(0);
        expect(directive.currentCarousel.unbindOnSlideChangeCallback).toHaveBeenCalledTimes(1);
        expect(directive.currentCarousel.getSlidesQuantity)
          .toHaveBeenCalledWith(directive.elementRef.nativeElement);
      });

      it('If new slide was out of range, move to the new assigned one', () => {
        carouselService.get.and.returnValue({ currentSlide: 1 });
        carouselService.add.and.returnValue({
          getSlidesQuantity: jasmine.createSpy('getSlidesQuantity').and.returnValue(2),
          onSlideChange: jasmine.createSpy('onSlideChange').and.callFake((cb) => {
            cb && cb(1, 'wrapping');
          }),
          currentSlide: 2,
          toIndex: jasmine.createSpy('toIndex')
        });
        directive.onSlideChangeCallback = jasmine.createSpy('onSlideChangeCallback');

        directive.refreshInteractionWithDom();

        expect(directive.onSlideChangeCallback).toHaveBeenCalledWith(2, 'false');
        expect(directive.onSlideChangeCallback).toHaveBeenCalledWith(1, 'wrapping');
        expect(directive.currentCarousel.onSlideChange).toHaveBeenCalledWith(jasmine.any(Function));
        expect(directive.currentCarousel.toIndex).toHaveBeenCalledWith(1);
        expect(directive.currentCarousel.getSlidesQuantity).not.toHaveBeenCalled();
      });

      it('set interval', () => {
        directive.interval = 100;
        directive.setNextSlideTimeout = jasmine.createSpy('setNextSlideTimeout');
        carouselService.get.and.returnValue({ currentSlide: 1 });
        carouselService.add.and.returnValue({
          slidesCount: 2,
          currentSlide: 1,
          onSlideChange: jasmine.createSpy('onSlideChange')
        });

        directive.refreshInteractionWithDom();

        expect(directive.setNextSlideTimeout).toHaveBeenCalled();
      });

      afterEach(() => {
        expect(directive.refreshVirtualSlides).toHaveBeenCalled();
        expect(carouselService.add)
          .toHaveBeenCalledWith(2, 'carouselName', { looping: true }, directive.elementRef.nativeElement);
      });
    });

    afterEach(() => {
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(directive.elementRef.nativeElement, 'ng-carousel');
      expect(directive.removeOldVirtualSlides).toHaveBeenCalled();
      expect(directive.isCarouselInit.emit).toHaveBeenCalledWith(true);
      expect(directive.elementRef.nativeElement.querySelector).toHaveBeenCalledWith('slidecontainer');
      expect(directive.elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('slide');
    });
  });

  describe('onSlideChangeCallback', () => {
    beforeEach(() => {
      directive.setNextSlideTimeout = jasmine.createSpy('setNextSlideTimeout');
      directive.refreshVirtualSlides = jasmine.createSpy('refreshVirtualSlides');
      directive['animate'] = jasmine.createSpy('animate');
    });

    it('should move to the first slide', () => {
      directive.onSlideChangeCallback(0, 'left');

      expect(directive['animate']).toHaveBeenCalledWith(0, jasmine.any(Function));
    });

    it('should move to the last slide', () => {
      directive.slides = [];
      directive.onSlideChangeCallback(0, 'right');

      expect(directive['animate']).toHaveBeenCalledWith(1, jasmine.any(Function));
    });

    describe('should call animate callback', () => {
      let callback;

      beforeEach(() => {
        directive.slides = [];
        directive['animate'] = jasmine.createSpy('animate').and.callFake((index, cb) => {
          callback = cb;
        });
      });

      it('for left wrapping', () => {
        directive.onSlideChangeCallback(0, 'left');

        callback();

        expect(directive['animate']).toHaveBeenCalledWith(0);
      });

      it('for roght wrapping', () => {
        directive.onSlideChangeCallback(0, 'right');

        callback();

        expect(directive['animate']).toHaveBeenCalledWith(1);
      });
    });

    afterEach(() => {
      expect(directive.setNextSlideTimeout).toHaveBeenCalled();
      expect(directive.refreshVirtualSlides).toHaveBeenCalled();
    });
  });

  describe('touchHorizScroll', () => {
    let event;

    beforeEach(() => {
      event = {
        preventDefault: jasmine.createSpy('preventDefault')
      };

      rendererService.renderer.listen.and.callFake((element: any, eventName: string, cb) => {
        cb && cb();
      });

      directive.mouseListeners = [];
      directive.elementRef.nativeElement = {} as any;
      directive.carouselDrag = jasmine.createSpy('carouselDrag');
      directive.carouselPress = jasmine.createSpy('carouselPress');
      directive.carouselRelease = jasmine.createSpy('carouselRelease');
      directive.setNextSlideTimeout = jasmine.createSpy('setNextSlideTimeout');
      directive.getPageX = jasmine.createSpy('getPageX').and.returnValue(0);
      directive.getPageY = jasmine.createSpy('getPageY').and.returnValue(0);
      directive.isVerticalSwipe = jasmine.createSpy('isTouchDevice').and.returnValue(true);
      directive['animate'] = jasmine.createSpy('animate');
      directive['getContainerTRansformPosition'] = jasmine.createSpy('getContainerTRansformPosition');

      directive.slideContainer = {
        scrollLeft: 10,
        scrollTop: 10,
        addEventListener: jasmine.createSpy('slideContainer.addEventListener').and.callFake((eventName: string, cb, options) => {
          cb && cb(event);
        })
      } as any;
    });

    it('should add event listeners for touch device', () => {
      directive.isTouchDevice = jasmine.createSpy('isTouchDevice').and.returnValue(true);
      deviceService.isTablet = true;

      directive.touchHorizScroll();

      expect(directive.isTouchDevice).toHaveBeenCalledTimes(5);

      // mouseListeners
      expect(directive.mouseListeners.length).toEqual(3);

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'touchstart', jasmine.any(Function));
      expect(directive.carouselPress).toHaveBeenCalled();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'touchend', jasmine.any(Function));
      expect(directive.carouselRelease).toHaveBeenCalled();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'mouseover', jasmine.any(Function));
      expect(directive.setNextSlideTimeout).toHaveBeenCalled();

      // slideContainer listeners
      expect(directive.slideContainer.addEventListener).toHaveBeenCalledWith('touchstart', jasmine.any(Function), false);
      expect(directive['getContainerTRansformPosition']).toHaveBeenCalled();
      expect(directive.getPageX).toHaveBeenCalledWith(event);
      expect(directive.getPageY).toHaveBeenCalledWith(event);

      expect(directive.slideContainer.addEventListener).toHaveBeenCalledWith('touchmove', jasmine.any(Function), false);
      expect(directive.getPageX).toHaveBeenCalledWith(event);
      expect(directive.getPageY).toHaveBeenCalledWith(event);
      expect(directive.isVerticalSwipe).toHaveBeenCalledWith(10, 0, 10, 0);
      expect(directive.carouselDrag).toHaveBeenCalledWith(10);
      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should add event listeners for non-touch device', () => {
      directive.isTouchDevice = jasmine.createSpy('isTouchDevice').and.returnValue(false);
      deviceService.isTablet = false;
      directive.timeoutPromise = new Promise(() => {
      });
      directive.slideContainer.addEventListener =
        jasmine.createSpy('slideContainer.addEventListener').and.callFake((eventName: string, cb) => {
          if (['mouseup', 'mousedown', 'touchmove', 'mousemove'].indexOf(eventName) > -1 && !directive.isTouchDevice()) {
            return; // simulate events.isDown === false;
          }

          cb && cb(event);
        });

      directive.touchHorizScroll();

      // mouseListeners
      expect(directive.mouseListeners.length).toEqual(3);

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'mousedown', jasmine.any(Function));
      expect(directive.carouselPress).toHaveBeenCalled();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'mouseup', jasmine.any(Function));
      expect(directive.carouselRelease).toHaveBeenCalled();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'mouseover', jasmine.any(Function));
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(directive.timeoutPromise);

      // slideContainer listeners
      expect(directive.slideContainer.addEventListener).toHaveBeenCalledWith('mouseup', jasmine.any(Function));
      expect(directive.slideContainer.addEventListener).toHaveBeenCalledWith('mouseout', jasmine.any(Function));
      expect(directive.isVerticalSwipe).not.toHaveBeenCalled();
      expect(directive.carouselDrag).not.toHaveBeenCalled();
      expect(event.preventDefault).not.toHaveBeenCalled();
      expect(directive['animate']).not.toHaveBeenCalled();
    });

    it('should add event listeners for non-touch device without isDown option', () => {
      directive.isTouchDevice = jasmine.createSpy('isTouchDevice').and.returnValue(false);
      directive.currentCarousel = {
        currentSlide: 1
      } as any;
      directive.slideContainer.addEventListener =
        jasmine.createSpy('slideContainer.addEventListener').and.callFake((eventName: string, cb) => {
          if (eventName === 'mouseup' && !directive.isTouchDevice()) {
            return; // simulate events.isDown === true;
          }

          cb && cb(event);
        });

      directive.touchHorizScroll();

      //  moveToSlide
      expect(directive.getPageX).toHaveBeenCalledWith(event);
      expect(directive['animate']).toHaveBeenCalledWith(0);
    });
  });

  describe('animate', () => {
    const formStyle = (rule: string): void => {
        style = {
          '-webkit-transform': rule,
          '-moz-transform': rule,
          '-ms-transform': rule,
          '-o-transform': rule,
          'transform': rule
        };
      },
      slideContainerEvents = ['transitionend', 'oTransitionEnd', 'webkitTransitionEnd'];
    let style;

    beforeEach(() => {
      directive.animationListeners = [];
      directive.slideContainer = {} as any;
      rendererService.renderer.listen = jasmine.createSpy('listen');
      directive['getSlidePosition'] = jasmine.createSpy('getSlidePosition').and.returnValue(1000);
    });

    it('should set animation for non-desktop', () => {
      directive['slideContainerTransitionAnimation'] = jasmine.createSpy('slideContainerTransitionAnimation');

      formStyle(`translate(-${ 1000 - windowRef.nativeWindow.innerWidth }px, 0)`);

      directive['animate'](10);

      expect(directive['getSlidePosition']).toHaveBeenCalledWith(10);

      expect(domToolsService.css).toHaveBeenCalledWith({}, style);
      expect(directive['slideContainerTransitionAnimation']).toHaveBeenCalledTimes(3);
      expect(directive['slideContainerTransitionAnimation']).toHaveBeenCalledWith(undefined);
    });

    it('should set animation for desktop', () => {
      deviceService.isDesktop = true;

      formStyle(`translate3d(-${ 1000 - windowRef.nativeWindow.innerWidth }px, 0)`);

      directive['animate'](10);

      expect(domToolsService.css).toHaveBeenCalledWith({}, style);

      slideContainerEvents.forEach((event: string) => {
        expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, event, jasmine.any(Function));
      });
    });

    afterEach(() => {
      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith({}, 'carousel-is-sliding');
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith({}, 'carousel-animate');
      expect(directive.animationListeners.length).toEqual(3);
    });
  });

  describe('touchScroll', () => {
    const position = 10,
      formStyle = (rule: string): void => {
        style = {
          '-webkit-transform': rule,
          '-moz-transform': rule,
          '-ms-transform': rule,
          '-o-transform': rule,
          'transform': rule
        };
      };
    let style;

    beforeEach(() => {
      directive.slideContainer = {} as any;
    });

    it('should animate in all 3 axis if desktop', () => {
      deviceService.isDesktop = true;

      formStyle(`translate3d(${ Math.ceil(position) }px, 0, 0)`);

      directive['touchScroll'](position);

      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith({}, 'carousel-animate');
      expect(domToolsService.css).toHaveBeenCalledWith({}, style);
    });

    it('should animate in all 2 axis if not desktop', () => {
      deviceService.isDesktop = false;

      formStyle(`translate(${ Math.ceil(position) }px, 0)`);

      directive['touchScroll'](position);

      expect(domToolsService.css).toHaveBeenCalledWith({}, style);
    });

    afterEach(() => {
      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith({}, 'carousel-animate');
    });
  });

  describe('#getSlidePosition', () => {
    it('should get slide position for 1-st slide', () => {
      directive.slideContainer = {
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{
          offsetLeft: 0
        }, {
          offsetLeft: 100
        }])
      } as any;
      const result = directive['getSlidePosition'](1);
      expect(result).toBe(100 + 500);
    });

    it('should get slide position for 2-st slide', () => {
      directive.slideContainer = {
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{
          offsetLeft: 0
        }, {
          offsetLeft: 100
        }, {
          offsetLeft: 200
        }])
      } as any;
      const result = directive['getSlidePosition'](2);
      expect(result).toBe(200 + 500 - 15);
    });
  });

  describe('getContainerTRansformPosition', () => {
    it('should getComputedStyle and return negative value', () => {
      directive.slideContainer = {} as any;
      window.getComputedStyle = jasmine.createSpy('window.getComputedStyle').and.returnValue({ transform: '1 2 3 4 5' });

      expect(directive['getContainerTRansformPosition']()).toEqual(-5);
    });

    it('should return zero negative value', () => {
      directive.slideContainer = {} as any;
      window.getComputedStyle = jasmine.createSpy('window.getComputedStyle').and.returnValue({ transform: '' });

      expect(directive['getContainerTRansformPosition']()).toEqual(-0);

      expect(window.getComputedStyle).toHaveBeenCalledWith({} as any);
    });
  });
});
