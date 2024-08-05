import {
  FeaturedHighlightsCarouselComponent
} from '@featured/components/featured-highlights-carousel/featured-highlights-carousel.component';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('FeatureHighlightCarouselComponent', () => {
  let component: FeaturedHighlightsCarouselComponent;
  let windowRefService;
  let device;
  let router;
  let carouselService;
  let routingHelperService;
  let elementRef;
  let domToolsService;
  let rendererService;
  let pubSubService;
  let changeDetectorRef;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy().and.returnValue(100)
      }
    };
    windowRefService = {
      nativeWindow: {
        location: { origin: 'loc' },
        setTimeout: jasmine.createSpy().and.callFake((cb, sec) => {
          cb();
        })
      }
    };

    device = {
      isTouch: jasmine.createSpy().and.returnValue(false)
    };

    router = {
      navigate: jasmine.createSpy(),
      url:'football'
    };
    domToolsService = {
      getWidth: (w) => w
    };
    carouselService = {
      carousel: {
        currentSlide: 5,
        slidesCount: 10,
        next: jasmine.createSpy(),
        previous: jasmine.createSpy(),
        onSlideChangeCallbacks: jasmine.createSpy()
      },
      remove: jasmine.createSpy(),
      get: (name: string): Carousel => carouselService.carousel as Carousel
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy().and.callFake((target, event, cb) => {
          cb();
          return () => {};
        })
      }
    };
    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy().and.returnValue('some-link')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new FeaturedHighlightsCarouselComponent(
      elementRef,
      windowRefService,
      router,
      domToolsService,
      carouselService,
      rendererService,
      routingHelperService,
      device,
      pubSubService,
      changeDetectorRef
    );
    component.highlightsCarousel = { data: [], _id: '456' } as any;
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });
  it('childComponentLoaded', () => {
    component.initialised = false;
    component.childComponentLoaded();
    expect(component.initialised).toBe(true);
  });
  it('#ngOnInit should not initShowCarouselButtons for touch devices', () => {
    // touch device
    device.isTouch.and.returnValue(true);
    component['resizeListener'] = null;
    component.ngOnInit();
    expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalled();
    expect(component['resizeListener'] as any).toBeNull();
  });

  describe('ngOnInit should handle event update', () => {
    beforeEach(() => {
      component.highlightsCarousel.eventIds = [1];
    });

    it('and detect changes', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => { if (channel === 'WS_EVENT_UPDATED') {cb({ id: 1 });}});
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('and do not detect changes', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => { if (channel === 'WS_EVENT_UPDATED') {cb({ id: 2 });}});
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });
    it(`should subscribe on WS_EVENT_UPDATE`, () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => { if (channel === 'WS_EVENT_UPDATE') {cb();}});
      component.pageId = 'featuredHighlightsCarousel_1';
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('featuredHighlightsCarousel_1', 'WS_EVENT_UPDATE', jasmine.any(Function));
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('isFanzonePage should return true if page is fanzone', () => {
      const isFanzone = component.isFanzonePage();

      expect(isFanzone).toBeTrue;
    });
    it('isFanzonePage should return false if page is fanzone', () => {
      router.url = 'fanzone'
  
      const isFanzone = component.isFanzonePage();
      expect(isFanzone).toBeFalse;
    });
  });

  describe('ngOnDestroy', () => {
    it('should not remove carousel', () => {
      component.highlightsCarousel = null;
      component.ngOnDestroy();
      expect(carouselService.remove).not.toHaveBeenCalled();
    });

    it('should remove carouse and call resize listener', () => {
      device.isTouch.and.returnValue(false);
      component['resizeListener'] = jasmine.createSpy('resizeListener');
      component.ngOnDestroy();
      expect(carouselService.remove).toHaveBeenCalled();
      expect(component['resizeListener']).toHaveBeenCalled();
    });

    it('should not call resize listener', () => {
      device.isTouch.and.returnValue(true);
      component['resizeListener'] = jasmine.createSpy('resizeListener');
      component.ngOnDestroy();
      expect(component['resizeListener']).not.toHaveBeenCalled();
    });
  });

  describe('#isValidCarousel cases:', () => {
    it('no highlight carousel', () => {
      component.highlightsCarousel = undefined as any;
      expect(component.isValidCarousel).toBe(false);
    });

    it('no data', () => {
      component.highlightsCarousel = {} as any;
      expect(component.isValidCarousel).toBe(false);
    });

    it('has data', () => {
      component.highlightsCarousel = { data: [] } as any;
      expect(component.isValidCarousel).toBe(false);
    });

    it('has data', () => {
      component.highlightsCarousel = {
        data: [{ id: 2, markets: [{}] }, { id: 5, markets: [] }]
      } as any;
      expect(component.isValidCarousel).toBe(true);
    });
  });

  it('#trackByCard should generate id', () => {
    expect(component.trackByCard(87, { id: '7888' })).toEqual('7888');
  });

  it('#competitionsNavigate should navigate to competition page', () => {
    component.highlightsCarousel.data = [
      { categoryName: 'TENNIS', typeName: 'tennis', className: 'name1' }
    ] as any;
    component.competitionsNavigate();
    expect(routingHelperService.formCompetitionUrl).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['some-link']);
  });

  it('#nextSlide should scroll carousel', () => {
    component.nextSlide();
    expect(carouselService.carousel.next).toHaveBeenCalled();
  });

  it('#prevSlide should scroll carousel', () => {
    component.prevSlide();
    expect(carouselService.carousel.previous).toHaveBeenCalled();
  });

  it('#showNext checks if arrow-next is shown', () => {
    expect(component.showNext).toBe(true);
    carouselService.carousel.currentSlide = 10;
    expect(component.showNext).toBe(false);
  });

  it('#showPrev checks if arrow-prev is shown', () => {
    expect(component.showPrev).toBe(true);
    carouselService.carousel.currentSlide = 0;
    expect(component.showPrev).toBe(false);
  });

  it('#carousel should get the carousel', () => {
    expect(component['carousel'].currentSlide).toBe(5);
    expect(component['carousel'].slidesCount).toBe(10);
    component.highlightsCarousel = null;
    expect(component['carousel']).toBeNull();
  });

  it('#initShowCarouselButtons checks if carousel prev next controls is visible', () => {
    component['elementRef'] = elementRef;
    carouselService.carousel.slidesCount = 1;
    component.highlightsCarousel.data = [{
      categoryCode: 'Football'
    }] as any;
    component['initShowCarouselButtons']();
    expect(component.showCarouselButtons).toBe(false);

    carouselService.carousel.slidesCount = 2;
    component.highlightsCarousel.data = [{}, {}] as any;
    component['initShowCarouselButtons']();
    expect(component.showCarouselButtons).toBe(true);
  });

  it('#isOneCard should check carousel', () => {
    component.highlightsCarousel = {} as any;
    expect(component['isOneCard']).toBeFalsy();

    component.highlightsCarousel = {
      data: []
    } as any;
    expect(component['isOneCard']).toBeFalsy();

    component.highlightsCarousel = {
      inPlay: true,
      data: [{ id: 2, markets: [{}] }]
    } as any;
    expect(component['isOneCard']).toBeTruthy();

    component.highlightsCarousel = {
      inPlay: true,
      data: [{ id: 2, markets: [{}] }, { id: 5, markets: [] }]
    } as any;
    expect(component['isOneCard']).toBeFalsy();
  });

  it('should use OnPush strategy', () => {
    expect(FeaturedHighlightsCarouselComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
