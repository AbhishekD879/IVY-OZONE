import { BehaviorSubject, of, throwError } from 'rxjs';
import { discardPeriodicTasks, fakeAsync, tick } from '@angular/core/testing';
import { BannersSectionComponent } from './banners-section.component';
import Utils from '@core/services/aemBanners/utils';
import environment from '@environment/oxygenEnvConfig';
import { singleOfferFromLibrary } from '@app/core/services/aemBanners/test/data/singleOfferFromLibrary.mock';

const offersJson = require('./test/data/mockedOffersToCarousel.json');
const { allOffersMock } = singleOfferFromLibrary;

describe('BannersSectionComponent', () => {
  let component: BannersSectionComponent;
  let windowRefService;
  let pubSubService;
  let deviceService;
  let carouselMockService;
  let carouselInstanceMock;
  let gtmServiceMock;
  let cmsService;
  let elementRef;
  let domTools;
  let storageService;
  let userService;
  let bannerSectionService;
  let bannerClickServiceMock;
  let rendererService;
  let configFromCms;
  let changeDetectorRef, location;

  const imagesMock = ['1', '2', '3'];

  beforeEach(() => {
    configFromCms = {
      DynamicBanners: {
        enabled: true,
        timePerSlide: 5,
        maxOffers: 123
      }
    };
    windowRefService = {
      document: {
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.callFake(() => imagesMock),
        cookie: ''
      },
      nativeWindow: jasmine.createSpyObj('nativeWindow', ['open', 'setTimeout', 'clearTimeout', 'clearInterval', 'setInterval'])
    };
    windowRefService.nativeWindow.location = {pathname: 'stubpath'};
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: {
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS',
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };
    deviceService = {
      viewType: 'mobile',
      isWrapper: false
    };
    carouselMockService = {
      get: jasmine.createSpy('get').and.callFake(() => carouselInstanceMock)
    } as any;
    gtmServiceMock = {
      push: jasmine.createSpy('push')
    };
    carouselInstanceMock = {
      next: jasmine.createSpy('next'),
      previous: jasmine.createSpy('previous'),
      toIndex: jasmine.createSpy('toIndex')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(configFromCms))
    };
    elementRef = { nativeElement: {} };
    domTools = {
      css: () => {},
      getWidth: () => {}
    };
    storageService = {
      get: jasmine.createSpy('getItem').and.callFake((key) => {
        if (key === 'existingUser') {
          return JSON.parse('1');
        }
        if (key === 'vipLevel') {
          return JSON.parse('22');
        }
        if (key === 'countryCode') {
          return JSON.parse('IE');
        }
      }),
      set: jasmine.createSpy('setItem'),
      setCookie: jasmine.createSpy('setCookie'),
      getCookie: jasmine.createSpy('getCookie').and.returnValue('')
    };
    userService = {
      isRetailUser: jasmine.createSpy('isRetailUser').and.returnValue(true),
      accountBusinessPhase: 'in-shop'
    };
    bannerSectionService = {
      fetchOffersFromAEM: jasmine.createSpy('fetchOffersFromAEM').and.callFake(() => of(offersJson)),
      updateData: jasmine.createSpy('updateData'),
      getOdds: jasmine.createSpy('getOdds').and.returnValue(allOffersMock[0]),
      offersLatestOdds$: {
        subscribe: jasmine.createSpy('subscribe'),
        complete: jasmine.createSpy('complete')
      }
    };
    bannerClickServiceMock = {
      handleBannerClick: jasmine.createSpy('handleBannerClick')
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen')
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy()
    };
    location = {
      path: jasmine.createSpy().and.returnValue('')
    };

    createComponent();
  });

  function createComponent () {
    component = new BannersSectionComponent(
      windowRefService,
      pubSubService,
      deviceService,
      storageService,
      gtmServiceMock,
      userService,
      bannerSectionService,
      rendererService,
      carouselMockService,
      cmsService,
      elementRef,
      domTools,
      bannerClickServiceMock,
      changeDetectorRef, location
    );
    component.page = 'samplePage';
  }

  it('should use vanilla brand',  () => {
    const curBrand = environment.brand;
    environment.brand = 'ladbrokes';
    deviceService.isDesktop = true;
    const cmp = new BannersSectionComponent(
      windowRefService,
      pubSubService,
      deviceService,
      storageService,
      gtmServiceMock,
      userService,
      bannerSectionService,
      rendererService,
      carouselMockService,
      cmsService,
      elementRef,
      domTools,
      bannerClickServiceMock,
      changeDetectorRef, location
    );
    expect(cmp.brand).toBe('ladbrokes');
    expect(cmp.imgWidth).toBe('720');
    environment.brand = curBrand; // restore brand value
  });

  it('check detecting gifs called', () => {
    const nonAnimatedUrl = 'https://banners.com/is/image/stageladbrokescoral/duck1?&$ladbrokes-mobile-tablet-width$';
    const findGifsSpy = spyOn(component, 'findGifsAndLoadInBackground');

    component.resetSwiper([{imgUrl: nonAnimatedUrl,bannerStatus: true}]);

    expect(findGifsSpy).toHaveBeenCalled();
  });

  it('Based on device type image width param needs to be added', () => {
    component.imgWidth = '720';
    const imgUrl: string = "https://scmedia.cms.test.env.works/$-$/1d927088bad34f71a0ed2e839318680b.jpg";
    const img: string = component.addImageWidth(imgUrl);
    expect(img).toBe(imgUrl+'?w=720');
  });
  
  it('Based on device type image width param needs to be changed', () => {
    component.imgWidth = '480';
    const imgUrl: string = "https://scmedia.cms.test.env.works/$-$/1d927088bad34f71a0ed2e839318680b.jpg";
    const img: string = component.addImageWidth(imgUrl);
    expect(img).toBe(imgUrl+'?w=480');
  });

  it('check transform animated images to not animated', () => {
    const animatedUrl = 'https://banners.com/is/content/stageladbrokescoral/duck1?&$ladbrokes-mobile-tablet-width$';
    const nonAnimatedUrl = 'https://banners.com/is/image/stageladbrokescoral/duck1?&$ladbrokes-mobile-tablet-width$';
    const offersWithGifs = [
      {
        imgUrl: animatedUrl
      }, {
        imgUrl: nonAnimatedUrl
      }];

    component.findGifsAndLoadInBackground(offersWithGifs);

    expect(offersWithGifs[0].imgUrl).toEqual(nonAnimatedUrl);
    expect(offersWithGifs[1].imgUrl).toEqual(nonAnimatedUrl);
  });

  it('check setting loaded attribute', () => {
    spyOn(component as any, 'unSetBannerSectionHeight');
    const animatedUrl = 'https://banners.com/is/content/stageladbrokescoral/duck1?&$ladbrokes-mobile-tablet-width$';
    const nonAnimatedUrl = 'https://banners.com/is/image/stageladbrokescoral/duck1?&$ladbrokes-mobile-tablet-width$';
    component.offers = [
      {
        imgUrl: animatedUrl
      }, {
        imgUrl: nonAnimatedUrl
      }];

    component.onFirstImageLoaded();

    expect(component.firstImageLoaded).toEqual(true);
    expect(component['unSetBannerSectionHeight']).toHaveBeenCalled();
  });

  it('when config empty banners won\'t be displayed', () => {
    component.isBannersEnabled = false;
    cmsService.getSystemConfig.and.returnValue(of({}));

    component.ngOnInit = jasmine.createSpy();

    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(component.isBannersEnabled).toBeFalsy();
  });
  it('check carousel instance for previous navigation', () => {
    component.prevSlide();
    expect(carouselMockService.get).toHaveBeenCalledWith('aem-banners-carousel');
    expect(carouselInstanceMock.previous).toHaveBeenCalled();
  });

  it('check carousel instance for next navigation', () => {
    component.nextSlide();
    expect(carouselMockService.get).toHaveBeenCalledWith('aem-banners-carousel');
    expect(carouselInstanceMock.next).toHaveBeenCalled();
  });

  describe('getUserType', () => {
    it('new ladbrokes user', () => {
      storageService.get.and.returnValue(null);
      component.brand = 'ladbrokes';
      expect(component['getUserType']()).toBe('new');
    });

    it('existing ladbrokes user', () => {
      storageService.get.and.returnValue({});
      expect(component['getUserType']()).toBe('in-shop');
    });

    it('existing coral user', () => {
      storageService.get.and.returnValue({});
      userService.isRetailUser.and.returnValue(false);
      expect(component['getUserType']()).toBe('existing');
    });

    it('anonymous coral user', () => {
      storageService.get.and.returnValue(null);
      component.brand = 'coral';
      expect(component['getUserType']()).toBe('anonymous');
    });
  });

  it('check brand to be used in component and in request to AEM', () => {
    expect(Utils.resolveBrandOrDefault('ladbrokes')).toBe('ladbrokes');
    expect(Utils.resolveBrandOrDefault('coral')).toBe('coral');
  });

  it('check default brand to be used in component and in request to AEM', () => {
    expect(Utils.resolveBrandOrDefault('someOtherEnvBrand')).toBe('coral');
  });

  describe('getAppType', () => {
    it('retail', () => { // TODO: rename to retail after changes in cms.
      component['page'] = 'retail';

      expect(component['getAppType']()).toEqual('connect');
    });

    it('isWrapper', () => {
      component['deviceService'].isWrapper = true;

      expect(component['getAppType']()).toEqual('app');
    });

    describe('isWrapper false', () => {
      beforeEach(() => {
        component['deviceService'].isWrapper = false;
      });

      it('isMobile', () => {
        component['deviceService'].isMobile = true;

        expect(component['getAppType']()).toEqual('mobile');
      });

      it('isTablet', () => {
        component['deviceService'].isTablet = true;

        expect(component['getAppType']()).toEqual('mobile');
      });

      it('isDesktop', () => {
        component['deviceService'].isDesktop = true;

        expect(component['getAppType']()).toEqual('mobile');
      });

      it('empty', () => {
        component['deviceService'].isMobile = false;
        component['deviceService'].isTablet = false;
        component['deviceService'].isDesktop = false;

        expect(component['getAppType']()).toEqual('');
      });
    });
  });

  describe('@actionHandler', () => {
    let mouseEvent;
    let offer;
    beforeEach(() => {
      offer = {
        link : 'some/link',
        target: '_blank'
      };
      mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);
    });

    it('should prevent default click and call banner click service', () => {
      offer.link = 'http://external.com';
      offer.target = '_self';
      component.offers = [];
      spyOn<any>(component, 'trackClickGTMEvent').and.callThrough();
      component.actionHandler(mouseEvent, offer);

      expect(mouseEvent.preventDefault).toHaveBeenCalled();
      expect(component['trackClickGTMEvent']).toHaveBeenCalledWith(mouseEvent);
      expect(bannerClickServiceMock.handleBannerClick).toHaveBeenCalled();
    });
  });

  describe('trackClickGTMEvent', () => {
    it('should not set property and not run gtm function', () => {
      const event = jasmine.createSpy('MouseEvent') as any;
      component.offers = [];
      component.trackClickGTMEvent(event);

      expect(gtmServiceMock.push).not.toHaveBeenCalled();
      expect(component['isGTMSuccess']).toBeFalsy();
    });

    it('should set property and run gtm function', () => {
      const event  = jasmine.createSpy('MouseEvent') as any;
      component.offers = offersJson.offers;
      component.trackClickGTMEvent(event);

      expect(gtmServiceMock.push).toHaveBeenCalledWith('aemBannerClick', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'banner',
        eventAction: 'click',
        eventLabel: component.offers[0].itemName,
        personalised: component.offers[0].personalised,
        location: windowRefService.nativeWindow.location.pathname,
        position: component.offers[0].position
      }));
      expect(component['isGTMSuccess']).toBeTruthy();
    });

    it('should send gtm event with vip level', () => {
      userService.vipLevel = 'vip';
      component.activeSlideIndex = 0;
      component.offers = [{}];
      component.trackClickGTMEvent({} as any);
      expect(gtmServiceMock.push).toHaveBeenCalledWith(
        'aemBannerClick', jasmine.objectContaining({ vipLevel: 'vip' }) );
    });
  });

  describe('#getTeasersData', () => {
    it('should get cms config', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({EagerLoadImagesNumber:{SiteCoreBannerDesktop:3,SiteCoreBannerMobile:2}}));
      createComponent();
      const offers = [{
        bannerStatus: true
      }];
      bannerSectionService.offersLatestOdds$ = new BehaviorSubject(offers);
      component['getTeasersData'] = jasmine.createSpy();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });
    it('should get cms config and use maxOffer and timePerSlide', () => {
      component['getTeasersData']();
      storageService.get.and.callFake((key) => {
        return null;
      });
      component['getAppType'] = jasmine.createSpy('getAppType').and.returnValue({});
      component['getUserType'] = jasmine.createSpy('getUserType').and.returnValue({});
      component['initOrientationChangeListener'] = jasmine.createSpy('initOrientationChangeListener');
      component.requestOffersAndCarouselInit = jasmine.createSpy('initOrientationChangeListener')
        .and.returnValue(of([1, 2]));
      component.initPubSubAndSubscriptions = jasmine.createSpy('initPubSubAndSubscriptions');
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component.timePerSlide).toBe(configFromCms.DynamicBanners.timePerSlide * 1000);
    });
    it('should Not setBannerSectionHeight when firstImageLoaded is true', () => {
      component.firstImageLoaded = true;
      component['getTeasersData']();
      storageService.get.and.callFake((key) => {
        return null;
      });
      component['getAppType'] = jasmine.createSpy('getAppType').and.returnValue({});
      component['getUserType'] = jasmine.createSpy('getUserType').and.returnValue({});
      component['initOrientationChangeListener'] = jasmine.createSpy('initOrientationChangeListener');
      component.requestOffersAndCarouselInit = jasmine.createSpy('initOrientationChangeListener')
        .and.returnValue(of([1, 2]));
      component.initPubSubAndSubscriptions = jasmine.createSpy('initPubSubAndSubscriptions');
      expect(component['setBannerSectionHeight']).not.toHaveBeenCalledTimes(1);
    });
    beforeEach(() => {
      spyOn(component as any, 'initOrientationChangeListener');
      spyOn(component as any, 'setBannerSectionHeight');
      spyOn(component as any, 'initPubSubAndSubscriptions');
      spyOn(component, 'requestOffersAndCarouselInit').and.returnValue(of([1, 2]));
      spyOn(component as any, 'getBannerDynamicParams').and.returnValue({});
    });

    it('when banners enabled', () => {
      component['getTeasersData']();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component.isBannersEnabled).toBeTruthy();
      expect(component['getBannerDynamicParams']).toHaveBeenCalled();
      expect(component['setBannerSectionHeight']).toHaveBeenCalledTimes(1);
      expect(component['initOrientationChangeListener']).toHaveBeenCalled();
      expect(component.requestOffersAndCarouselInit).toHaveBeenCalled();
      expect(component.initPubSubAndSubscriptions).toHaveBeenCalled();
    });
    it('when banners enabled and requestOffersAndCarouselInit throw error', () => {
      component['requestOffersAndCarouselInit'] = jasmine.createSpy('requestOffersAndCarouselInit').and.returnValue(throwError('error'));
      component['getBannerDynamicParams'] = jasmine.createSpy('getBannerDynamicParams').and.returnValue({});
      component['initOrientationChangeListener'] = jasmine.createSpy('initOrientationChangeListener');
      component['setBannerSectionHeight'] = jasmine.createSpy();
      component['initPubSubAndSubscriptions'] = jasmine.createSpy();
      component.requestOffersAndCarouselInit = jasmine.createSpy('initOrientationChangeListener')
        .and.returnValue(of([1, 2]));
        component['getTeasersData']();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component.isBannersEnabled).toBeTruthy();
      expect(component['getBannerDynamicParams']).toHaveBeenCalled();
      expect(component['setBannerSectionHeight']).toHaveBeenCalledTimes(1);
      expect(component['initOrientationChangeListener']).toHaveBeenCalled();
      expect(component.requestOffersAndCarouselInit).toHaveBeenCalled();
      expect(component.initPubSubAndSubscriptions).toHaveBeenCalled();
    });
    describe('when banners enabled', () => {
      it(`should Not setBannerSectionHeight`, () => {
        component.firstImageLoaded = true;

        component['getTeasersData'] = jasmine.createSpy();

        expect(component['setBannerSectionHeight']).not.toHaveBeenCalledTimes(1);
      });
    });
    it('when banners disabled', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        DynamicBanners: {
          enabled: false
        }}));
        component['getTeasersData']();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component.isBannersEnabled).toBeFalsy();
    });
  });
  describe('#ngOnInit', () => {
    it('live odds banners', fakeAsync(() => {
      deviceService.isDesktop = true;
      const cmp = new BannersSectionComponent(
        windowRefService,
        pubSubService,
        deviceService,
        storageService,
        gtmServiceMock,
        userService,
        bannerSectionService,
        rendererService,
        carouselMockService,
        cmsService,
        elementRef,
        domTools,
        bannerClickServiceMock,
        changeDetectorRef, location
      );
      cmp.allOffers = allOffersMock;
      cmp['ngOnInit']();
      tick(10000);
      expect(cmp.imgWidth).toBe('720');
      expect(cmp.allOffers.length).not.toBe(0);
      discardPeriodicTasks();
    }));
    it('live odds banners when offers is empty',fakeAsync(() => {
      component.allOffers= [];
      component.offers = [];
      component['ngOnInit']();
      tick(10000);
      expect(component.offers.length).toBe(0);
      discardPeriodicTasks();
    }));
    it(`should detectListener on 10000ms` , () => {
      component['getLaterUpdates'] = jasmine.createSpy('getLaterUpdates');
      windowRefService.nativeWindow.setInterval.and.callFake(cb => cb());
      component['ngOnInit']();
      expect(windowRefService.nativeWindow.setInterval).toHaveBeenCalledWith(
        jasmine.any(Function), component['LIVE_ODDS_INTERVAL']);
      expect(component['getLaterUpdates']).toHaveBeenCalledTimes(1);
    });
});

  describe('ngAfterViewInit', () => {
    it(`should call getLaterUpdates method`, () => {
      component.allOffers= allOffersMock;
      component.ngAfterViewInit();
      component['getLaterUpdates']();
      expect(component.allOffers.length).not.toBe(0);
    });
    it(`should call getLaterUpdates method with empty offers`, () => {
      component.allOffers= [];
      component.offers = [];
      component.ngAfterViewInit();
      component['getLaterUpdates']();
      expect(component.offers.length).toBe(0);
    });
  });

  describe('gotToSlide', () => {
    it(`should slide`, () => {
      component.gotToSlide(3);

      expect(carouselInstanceMock.toIndex).toHaveBeenCalledWith(3);
    });
  });

  describe('#setBannerSectionHeight', () => {
    beforeEach(() => {
      component['element'] = <any>{ nodeName: 'banner-section' };
      component['domTools'].css = jasmine.createSpy();
      component['domTools'].getWidth = jasmine.createSpy().and.returnValue(500);
    });

   it('should set temporary height for mobile when view port width 1100', () => {
      component['deviceService'].isDesktop = false;
      component['windowRef'].nativeWindow.innerWidth = 1100;
      component['setBannerSectionHeight']();

      expect(component['domTools'].css).toHaveBeenCalledTimes(2);
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'display', 'block');
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'height', '227px');
    });

    it('should set temporary height for mobile when view port width 1000', () => {
      component['deviceService'].isDesktop = false;
      component['windowRef'].nativeWindow.innerWidth = 1000;
      component['setBannerSectionHeight']();

      expect(component['domTools'].css).toHaveBeenCalledTimes(2);
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'display', 'block');
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'height', '227px');
    });

    it('should set temporary height for NOT mobile when view port width 1100', () => {
      component['deviceService'].isDesktop = true;
      component['windowRef'].nativeWindow.innerWidth = 1100;
      component['setBannerSectionHeight']();

      expect(component['domTools'].css).toHaveBeenCalledTimes(2);
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'display', 'block');
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'height', '122.35955056179776px');
    });

    it('should set temporary height for NOT mobile when view port width 1000', () => {
      component['deviceService'].isDesktop = true;
      component['windowRef'].nativeWindow.innerWidth = 1000;
      component['setBannerSectionHeight']();

      expect(component['domTools'].css).toHaveBeenCalledTimes(2);
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'display', 'block');
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'height', '237px');
    });
  });

  it('#unSetBannerSectionHeight should', () => {
    component['element'] = <any>{ nodeName: 'banner-section' };
    component['domTools'].css = jasmine.createSpy();
    component['unSetBannerSectionHeight']();

    expect(component['domTools'].css).toHaveBeenCalledTimes(2);
    expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'display', '');
    expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'height', '');
  });

  describe('requestOffersAndCarouselInit', () => {
    beforeEach(() => {
      component['unSetBannerSectionHeight'] = jasmine.createSpy();
      component.carousel = {
        settings: {} ,
        _options: {}
      };
      component['element'] = <any>{ nodeName: 'banner-section' };
      component['domTools'].css = jasmine.createSpy();
    });

    it('should resetSwiper if has offers', () => {
      spyOn(component, 'resetSwiper');

      component['requestOffersAndCarouselInit']().subscribe();

      expect(component.resetSwiper).toHaveBeenCalled();
      expect(component.isLoaded).toBeTruthy();
    });

    it('should unSetBannerSectionHeight if has No offers', () => {
      (component['bannerService'].fetchOffersFromAEM as any).and.returnValue(of({ offers: [] }));

      component['requestOffersAndCarouselInit']().subscribe();

      expect(component['domTools'].css).toHaveBeenCalledTimes(2);
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'display', 'none');
      expect(component['domTools'].css).toHaveBeenCalledWith({ nodeName: 'banner-section' } as any, 'height', '0');
    });

    it('error case', () => {
      component['unSetBannerSectionHeight'] = jasmine.createSpy();
      component['bannerService'].fetchOffersFromAEM = jasmine.createSpy().and.returnValue(throwError('error'));
      component['requestOffersAndCarouselInit']().subscribe(() => {}, () => {});

      expect(component['unSetBannerSectionHeight']).toHaveBeenCalled();
      expect(component['showBanners']).toBe(false);
      expect(component.isLoaded).toBeTruthy();
    });
  });

  describe('#initPubSubAndSubscriptions', () => {
    it('should subscribe on RELOAD_COMPONENTS', () => {
      component['pubsub'].subscribe = jasmine.createSpy();
      component.initPubSubAndSubscriptions();

      expect(component['pubsub'].subscribe).toHaveBeenCalledWith('dynamicBanners', 'RELOAD_COMPONENTS', jasmine.any(Function));
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
    it('should reload component on RELOAD_COMPONENTS', () => {
      component.ngOnInit = jasmine.createSpy();
      component.ngOnDestroy = jasmine.createSpy();
      component['pubsub'].subscribe = jasmine.createSpy().and.callFake((a, b, cb) => {
        if (b === 'RELOAD_COMPONENTS') {
          cb();
        }
      });
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());
      component.initPubSubAndSubscriptions();

      expect(component.ngOnInit).toHaveBeenCalled();
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
    });
  });

  describe('handleActiveSlide', () => {
    beforeEach(() => {
      component.offers = [{}, {}];
    });
    it('should set active offer index', () => {
      component.handleActiveSlide(1);
      expect(component.offers[0].active).toBeTruthy();
      expect(component.offers[1].active).toBeFalsy();
      expect(component.activeSlideIndex).toBe(0);
      expect(component.isSlided).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it(`should Not detectChanges if no offers by index`, () => {
      component.handleActiveSlide(3);

      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });

    it('should send gtm track event', () => {
      userService.vipLevel = 'VIP';
      component.offers = [{ itemName: 'offer1' }];
      component.isSlided = true;
      component.handleActiveSlide(0);
      expect(gtmServiceMock.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'banner',
        eventAction: 'view',
        eventLabel: 'offer1',
        vipLevel: 'VIP'
      }));
      expect(component.isSlided).toBeTruthy();
    });

    it('should not send gtm track event if offer already tracked', () => {
      component.offers = [{ tracked: true }];
      component.handleActiveSlide(0);
      expect(gtmServiceMock.push).not.toHaveBeenCalled();
    });

    it(`should return if  slideIndex id Not integer`, () => {
      component.handleActiveSlide(1.123);
      expect(component.activeSlideIndex).toEqual(0);
      expect(gtmServiceMock.push).not.toHaveBeenCalled();
    });
  });

  describe('removeSlideOnError', () => {
    it('should remove offer from the list by index', () => {
      component.offers = [{ Id: 'i1'}, { Id: 'i2' }, { Id: 'i3' }, { Id: 'i4' }];
      component.removeSlideOnError(1);

      expect(component.offers).toEqual([{ Id: 'i1'}, { Id: 'i3' }, { Id: 'i4' }]);
    });
  });

  it('ngOnDestroy', () => {
    component['orientationChangeListener'] = jasmine.createSpy('orientationChangeListener');
    component.ngOnDestroy();
    expect(component['orientationChangeListener']).toHaveBeenCalledTimes(1);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('dynamicBanners');
    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledTimes(1);
    expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
  });

  it('handleReload', () => {
    spyOn(component, 'ngOnDestroy');
    spyOn(component, 'ngOnInit');
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());

    component['handleReload']();

    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledTimes(1);
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledTimes(1);
    expect(component.ngOnInit).toHaveBeenCalledTimes(1);
    expect(component.ngOnDestroy).toHaveBeenCalledTimes(1);
  });

  it('loadImageInBackgroundForOffer', () => {
    const offer: any = {};
    const img: any = component.loadImageInBackgroundForOffer(offer, 'img');
    img.onload();
    expect(offer.imgUrl).toBe('img');
  });

  it('trackByPosition', () => {
    expect(component.trackByPosition({ position: 1 })).toBe(1);
  });

  it('updateDynamicBanners', () => {
    spyOn(component, 'requestOffersAndCarouselInit').and.returnValue(of(null));
    component.carousel = { _options: {}, settings: {} } as any;
    component.updateDynamicBanners();
    expect(component.carousel._options).toEqual(jasmine.objectContaining({
      userType: 'in-shop', imsLevel: 22
    }));
    expect(component.carousel.settings).toEqual(jasmine.objectContaining({
      userType: 'in-shop', imsLevel: 22
    }));
    expect(component.requestOffersAndCarouselInit).toHaveBeenCalledTimes(1);
  });

  it('should not set imsLevel into options', () => {
    spyOn(component, 'requestOffersAndCarouselInit').and.returnValue(of(null));
    component.carousel = { _options: {}, settings: {} } as any;
    storageService.get.and.returnValue(null);
    component.updateDynamicBanners();
    expect(component.carousel._options['imsLevel']).toBeUndefined();
    expect(component.carousel.settings['imsLevel']).toBeUndefined();
  });

  it('initOrientationChangeListener', () => {
    rendererService.renderer.listen.and.callFake((p1, p2, cb) => cb());
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());
    component.offers = [{bannerStatus: true}];

    component['initOrientationChangeListener']();

    expect(rendererService.renderer.listen).toHaveBeenCalledWith(
      windowRefService.nativeWindow, 'orientationchange', jasmine.any(Function) );
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
      jasmine.any(Function), component.SWIPER_RESET_TIMEOUT);
  });

  describe('getBannerDynamicParams', () => {
    it('should return params with: imsLevel, device, maxOffers', () => {
      storageService.get.and.returnValue('vip');
      deviceService.viewType = 'mobile';
      component.page = 'home';
      component.brand='coral';
      component['cmsBannerConfig'] = { maxOffers: 1 } as any;
      expect(component['getBannerDynamicParams']()).toEqual({
        locale: 'en-gb',
        brand: 'coral',
        channel: '',
        userType: 'in-shop',
        page: 'homepage',
        imsLevel: 'vip',
        device: 'mobile',
        maxOffers: 1
      });
    });

    it('should return params without: imsLevel, device, maxOffers', () => {
      storageService.get.and.returnValue('');
      deviceService.viewType = 'desktop';
      component.brand='coral';
      component.page = '';
      component.brand='coral';
      component['cmsBannerConfig'] = {} as any;
      expect(component['getBannerDynamicParams']()).toEqual({
        locale: 'en-gb',
        brand: 'coral',
        channel: '',
        userType: 'anonymous',
        page: ''
      });
    });
    it('should set locale to en-ie if user is from Ireland', () => {
      storageService.get.and.returnValue('');
      deviceService.viewType = 'desktop';
      component.page = '';
      component.brand = 'ladbrokes';
      userService.countryCode = 'IE';
      component['cmsBannerConfig'] = {} as any;
      expect(component['getBannerDynamicParams']()).toEqual({
        locale: 'en-ie',
        brand: 'ladbrokes',
        channel: '',
        userType: 'new',
        page: ''
      });
    });
  });

  describe('subscribeForEvents', () => {
    beforeEach(() => {
      pubSubService.subscribe.and.callFake((s, c, cb) => cb());
      spyOn(component, 'updateDynamicBanners');
    });

    it('should update dynamic banners', () => {
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());
      component.carousel = {} as any;

      component['subscribeForEvents']();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'dynamicBanners', 'SESSION_LOGIN', jasmine.any(Function) );
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
        jasmine.any(Function), component.SWIPER_RESET_TIMEOUT );
      expect(component.updateDynamicBanners).toHaveBeenCalledTimes(1);
    });

    it('should not update dynamic banners', () => {
      component.carousel = null;
      component['subscribeForEvents']();
      expect(component.updateDynamicBanners).not.toHaveBeenCalled();
    });
  });
  describe('#checkForFiveASideUrl', () => {
    it('should check for valid five aside url', () => {
      const mockLocation = '5-a-side/pre-leader-board/';
      location.path.and.returnValue(mockLocation);
      expect(component.checkForFiveASideUrl()).toBeTruthy();
    });
    it('should check for invalid  five aside url', () => {
      const mockLocation = 'inplay';
      location.path.and.returnValue(mockLocation);
      expect(component.checkForFiveASideUrl()).toBeFalsy();
    });
  });

  it('Based on query params', () => {
    const imgUrl: string = "https://scmedia.cms.test.env.works/$-$/1d927088bad34f71a0ed2e839318680b.jpg?w=490";
    const img: string = component.addImageWidth(imgUrl);
    expect(img).toBe(imgUrl);
  });
  it('trackSliderClickGTMEvent gtm data', () => {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'banner',
      'component.LabelEvent': 'virtuals',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'top banner',
      'component.LocationEvent': 'not applicable',
      'component.EventDetails': `navigate test`,
      'component.URLclicked': 'not applicable',
    };
    component['trackSliderClickGTMEvent']('test');
    expect(gtmServiceMock.push).toHaveBeenCalledWith(gtmData.event, gtmData);
  });

  it('sliderGTMTracker GAtracking handler', ()=>{
    component.page = 'virtuals';
    component['sliderGTMTracker']('test');
  });
});
