import { ElementRef } from '@angular/core';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import {
  DesktopSurfaceBetsCarouselComponent
} from '@ladbrokesDesktop/shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SurfaceBetsCarouselComponent } from '@shared/components/surfaceBetsCarousel/surface-bets-carousel.component';

describe('DesktopSurfaceBetsCarouselComponent', () => {
  let component: DesktopSurfaceBetsCarouselComponent;
  let elementRef,
    domTools,
    windowRef,
    renderer,
    carouselService,
    changeDetRef,
    pubsub;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue(100)
      }
    };
    windowRef = {
      nativeWindow: {
        location: { origin: 'loc' },
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    domTools = {
      getWidth: (w) => w
    };
    carouselService = {
      carousel: {
        currentSlide: 5,
        slidesCount: 10,
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous'),
        onSlideChangeCallbacks: jasmine.createSpy('onSlideChangeCallbacks')
      },
      remove: jasmine.createSpy('remove'),
      get: (name: string): Carousel => carouselService.carousel as Carousel
    };

    renderer = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(() => {
        })
      }
    };

    changeDetRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };

    pubsub = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    component = new DesktopSurfaceBetsCarouselComponent(
      elementRef as ElementRef,
      domTools as DomToolsService,
      windowRef as WindowRefService,
      renderer as RendererService,
      carouselService as CarouselService,
      changeDetRef,
      pubsub
    );

    component.module = { data: [], _id: '456' } as any;
  });

  it('#ngOnInit should set initial values', () => {
    const superNgOnInitSpy = spyOn<any>(SurfaceBetsCarouselComponent.prototype, 'ngOnInit');
    component['initShowCarouselButtons'] = jasmine.createSpy('initShowCarouselButtons');
    windowRef.nativeWindow.setTimeout.and.callFake(() => {
      component['initShowCarouselButtons']();
    });
    component.ngOnInit();
    expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
    expect(component['initShowCarouselButtons']).toHaveBeenCalled();
    expect(component['resizeListener']).toEqual(jasmine.any(Function));
    expect(renderer.renderer.listen).toHaveBeenCalled();
    expect(superNgOnInitSpy).toHaveBeenCalled();
  });

  it('#ngOnDestroy should call resizeListener', () => {
    const superNgOnDestroySpy = spyOn<any>(SurfaceBetsCarouselComponent.prototype, 'ngOnDestroy');
    component['resizeListener'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(component['resizeListener']).toHaveBeenCalled();
    expect(carouselService.remove).toHaveBeenCalledWith(component.carouselName);
    expect(superNgOnDestroySpy).toHaveBeenCalled();
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
    component.module = null;
    expect(component['carousel']).toBeNull();
  });

  it('#initShowCarouselButtons checks if carousel prev next controls is visible', () => {
    component['elementRef'] = elementRef;
    carouselService.carousel.slidesCount = 1;
    component.module.data = [{
      categoryCode: 'Football'
    }] as any;
    component['initShowCarouselButtons']();
    expect(component.showCarouselButtons).toBe(false);

    carouselService.carousel.slidesCount = 2;
    component.module.data = [{}, {}] as any;
    component['initShowCarouselButtons']();
    expect(component.showCarouselButtons).toBe(true);
  });
  describe('ngOnChanges', () => {
    beforeEach(() => {
      spyOn<any>(component, 'initShowCarouselButtons');
    });
    it('should call initShowCarouselButtons', () => {
      const changes: any = {
        module: {}
      };
      component.ngOnChanges(changes);
      expect(component['initShowCarouselButtons']).toHaveBeenCalledTimes(1);
    });

    it('should not call initShowCarouselButtons', () => {
      const changes: any = {
      };
      component.ngOnChanges(changes);
      expect(component['initShowCarouselButtons']).not.toHaveBeenCalledTimes(1);
    });
  });
});
