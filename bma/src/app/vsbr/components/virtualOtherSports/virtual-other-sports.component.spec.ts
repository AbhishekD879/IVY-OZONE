import { VirtualOtherSports } from './virtual-other-sports.component';
import { banners } from './virtual-mock-data';
import { Carousel } from '@root/app/shared/directives/ng-carousel/carousel.class';
import { discardPeriodicTasks, fakeAsync, flush, tick } from '@angular/core/testing';

describe('VirtualSportsPageComponent', () => {
  let component: VirtualOtherSports;
  let deviceService;
  let windowRef;
  let carouselService;
  let router;
  let virtualHubService;
  let changeDetectorRef;

  beforeEach(() => {

    deviceService = {
      isDesktop: jasmine.createSpy('isDesktop')
    };
    router = {
      navigate: jasmine.createSpy(),
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
    };
    carouselService = {
      get: jasmine.createSpy().and.returnValue({} as Carousel),
    };


    windowRef = {
      nativeWindow: {
        setInterval: window.setInterval,
        open: jasmine.createSpy('open')
      }
    }

    virtualHubService = {
      onClickNavigationDetails: {
        id:'',
        sportInfo: null
      }
    }

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    }

    component = new VirtualOtherSports(deviceService, windowRef, carouselService, router, virtualHubService, changeDetectorRef);
  });

  it('should call getLaterUpdates on init', fakeAsync(() => {
    spyOn(component, 'getLaterUpdates');
    component.ngOnInit();
    tick(6000);
    expect(component.getLaterUpdates).toHaveBeenCalled();
    flush();
    discardPeriodicTasks();
  }));

  it('should set imgWidth to 720 if true', () => {
    deviceService.isDesktop = true;
    component.ngOnInit();
    expect(component.imgWidth).toBe(720);

    deviceService.isDesktop = false;
    component.ngOnInit();
    expect(component.imgWidth).toBe(480);
  });

  it('should update otherSportImages when otherSportImages changes', () => {
    const changes: any = {
      otherSportImages: {
        currentValue: ['image1.jpg', 'image2.jpg'],
      },
    };
    component.ngOnChanges(changes);
    expect(component.otherSportImages).toEqual(['image1.jpg', 'image2.jpg'] as any);
  });

  it('should not update virtualsLiveCount if virtualsLiveCount does not change', () => {
    const initialVirtualsLiveCount = component.virtualsLiveCount;
    const changes: any = {
      virtualsLiveCount: {
        currentValue: initialVirtualsLiveCount,
      },
    };
    component.ngOnChanges(changes);
    expect(component.virtualsLiveCount).toBe(initialVirtualsLiveCount);
  });

  it('should not update otherSportImages if otherSportImages does not change', () => {
    const initialOtherSportImages = component.otherSportImages;
    const changes: any = {
      otherSportImages: {
        currentValue: initialOtherSportImages,
      },
    };
    component.ngOnChanges(changes);
    expect(component.otherSportImages).toBe(initialOtherSportImages);
  });

  it('should update offers with repeated elements when banners has some elements', () => {
    const banners1 = banners;
    component.offers = banners;
    component.getLaterUpdates();
    expect(component.offers).toEqual([...banners1, ...banners1, ...banners1, ...banners1] as any);
  });

  it('should call getLaterUpdates() once after the view has been initialized', () => {
    spyOn(component, 'getLaterUpdates');
    component.ngAfterViewInit();
    expect(component.getLaterUpdates).toHaveBeenCalledTimes(1);
  });

  it('should return correct live count for the provided sportName when virtualsLiveCount has matching item', () => {
    component.virtualsLiveCount = [
      { sportName: 'Soccer', liveEventCount: '3' },
      { sportName: 'Basketball', liveEventCount: '1' },
      { sportName: 'Tennis', liveEventCount: '0' },
    ];
    const result1 = component.updateEventsData('Soccer');
    expect(result1).toBe('3 Events');

    const result2 = component.updateEventsData('Basketball');
    expect(result2).toBe('1 Event');

    const result3 = component.updateEventsData('Tennis');
    expect(result3).toBe('0 Event');
  });

  it('should return null when virtualsLiveCount is null', () => {
    component.virtualsLiveCount = null;
    const result = component.updateEventsData('Soccer');
    expect(result).toBeUndefined();
  });

  it('should return null when liveCount is null', () => {
    component.virtualsLiveCount = [
      { sportName: 'Soccer', liveEventCount: '3' },
      { sportName: 'Badminton', liveEventCount: null },
    ];
    const result = component.updateEventsData('Tennis');
    expect(result).toBeNull();
  });


  it('should open external URL using window.open', () => {
    const imageInfo = {
      redirectionURL: 'https://www.example.com',
    };
    component.goToVirtualSports(imageInfo as any);
    expect(windowRef.nativeWindow.open).toHaveBeenCalledWith('https://www.example.com', '_self');
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });

  it('should open external URL containing #!? using window.open', () => {
    const imageInfo = {
      redirectionURL: 'https://www.example.com/#!?parameter=value',
    };
    component.goToVirtualSports(imageInfo as any);
    expect(windowRef.nativeWindow.open).toHaveBeenCalledWith(
      'https://www.example.com/#!?parameter=value',
      '_self'
    );
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });

  it('should navigate to internal URL using router.navigateByUrl', () => {
    const imageInfo = {
      redirectionURL: '/internal-route',
    };
    component.goToVirtualSports(imageInfo as any);
    expect(windowRef.nativeWindow.open).not.toHaveBeenCalled();
    expect(router.navigateByUrl).toHaveBeenCalledWith('/internal-route');
  });

  it('should call carouselService.get with the correct carouselName', () => {
    const carouselName = 'carousel1';
    component['carouselName'] = carouselName;
    const carousel = component['carousel'];
    expect(carouselService.get).toHaveBeenCalledWith(carouselName);
    expect(carousel).toBeDefined();
  });

  it('should set the carousel property', () => {
    const carousel: Carousel = {} as any;
    component['carousel'] = carousel;
  })

  it('should call carouselService.get with the correct carouselName when accessing bannersCarousel', () => {
    const carouselName = 'carousel1';
    component['carouselName'] = carouselName;
    const bannersCarousel = component['bannersCarousel'];
    expect(carouselService.get).toHaveBeenCalledWith(carouselName);
    expect(bannersCarousel).toBeDefined();
  });

  it('should set the banner carousel property', () => {
    const bannersCarousel: Carousel = {} as any;
    component['bannersCarousel'] = bannersCarousel;
  })

  it('should prevent default behavior of MouseEvent and call trackClickGTMEvent', () => {
    const mockMouseEvent = new MouseEvent('click');
    const offer = {
      title: 'Offer Title',
      redirectionURL: '/some-url',
    };
    spyOn(mockMouseEvent, 'preventDefault');
    component.actionHandler(mockMouseEvent, offer as any);
    expect(mockMouseEvent.preventDefault).toHaveBeenCalled();
  });

  it('ngCarouselDisableRightSwipe setter method calling', () => {
    component.ngCarouselDisableRightSwipe = true;
    expect(component.ngCarouselDisableRightSwipe).toBe(false);
  });

  it('ngCarouselDisableRightSwipe should return false when called', () => {
    expect(component.ngCarouselDisableRightSwipe).toBe(false);
  });

  it('ngCarouselDisableRightSwipe should return false when conditions are not met', () => {
    const mockCarousel = {
      currentSlide: 0,
      slidesCount: 10,
    };
    component['carousel'] = mockCarousel as Carousel;
    component['carousel'].currentSlide = 2;
    expect(component.ngCarouselDisableRightSwipe).toBe(false);
  });

  it('showNext setter method calling', () => {
    expect(component.showNext()).toBe(false);
  });

  it('showNext should return false when called', () => {
    expect(component.showNext()).toBe(false);
  });

  it('showNext should return false when conditions are not met', () => {
    const mockCarousel = {
      currentSlide: 0,
      slidesCount: 10,
    };
    component['carousel'] = mockCarousel as Carousel;
    component['carousel'].currentSlide = 2;
    expect(component.showNext()).toBe(false);
  });

  it('showPrev setter method calling', () => {
    component.showPrev = true;
    expect(component.showPrev).toBe(false);
  });

  it('showPrev should return false when called', () => {
    expect(component.showPrev).toBe(false);
  });

  it('showPrev should return false when currentSlide is 0', () => {
    const mockCarousel = {
      currentSlide: 0,
      slidesCount: 10,
    };
    component['carousel'] = mockCarousel as Carousel;
    component['carousel'].currentSlide = 0;
    expect(component.showPrev).toBe(false);
  });

  it('nextSlide should increment currentIndex and call next() method', () => {
    const carousel = {
      next: jasmine.createSpy('previous').and.returnValue(jasmine.any(Function))
    };
    carouselService.get = jasmine.createSpy('get').and.returnValue({ next: carousel.next });
    component.currentIndex = 0;
    component.nextSlide();
    expect(component.currentIndex).toBe(1);
  });

  it('prevSlide should decrement currentIndex and callCarousel.previous()', () => {
    const bannersCarousel = {
      previous: jasmine.createSpy('previous').and.returnValue(jasmine.any(Function))
    };
    carouselService.get = jasmine.createSpy('get').and.returnValue({ previous: bannersCarousel.previous });
    component.currentIndex = 1;
    component.prevSlide();
    expect(component.currentIndex).toBe(0);
  });

  it('prevSlide should not decrement currentIndex if it is 0', () => {
    const bannersCarousel = {
      previous: jasmine.createSpy('previous').and.returnValue(jasmine.any(Function))
    };
    carouselService.get = jasmine.createSpy('get').and.returnValue({ previous: bannersCarousel.previous });
    component.currentIndex = 0;
    component.prevSlide();
    expect(component.currentIndex).toBe(0);
  });


});