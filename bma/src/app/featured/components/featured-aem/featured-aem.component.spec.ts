import { FeaturedAemComponent } from './featured-aem.component';
import environment from '@environment/oxygenEnvConfig';

describe('FeaturedAemComponent', () => {
  let component: FeaturedAemComponent;

  const aem: any = {
    _id: 'abrakadabra',
    data: [],
    maxOffers: 3
  };

  let pubsub;
  let user;
  let deviceService;
  let storage;
  let carouselService;
  let gtmService;
  let windowRef;
  let bannerClickService;

  beforeEach(() => {
    pubsub = {
      subscribe: jasmine.createSpy().and.callFake((name, channels, callback) => {
        callback();
      }),
      unsubscribe: jasmine.createSpy(),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      }
    };
    user = {};
    deviceService = {};
    storage = {
      get: jasmine.createSpy()
    };
    carouselService = {
      remove: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    windowRef = {
      nativeWindow: {
        location: {
          pathname: '/'
        }
      }
    };
    bannerClickService = {
      handleFeaturedAemSlideClick: jasmine.createSpy('handleFeaturedAemSlideClick')
    };
    component = new FeaturedAemComponent(
      pubsub,
      user,
      deviceService,
      storage,
      carouselService,
      gtmService,
      windowRef,
      bannerClickService
    );

    component.aem = aem;
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(pubsub.subscribe).toHaveBeenCalledWith('featuredAem_abrakadabra', ['SESSION_LOGIN', 'SESSION_LOGOUT'], jasmine.any(Function));
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('featuredAem_abrakadabra');
    expect(carouselService.remove).toHaveBeenCalledTimes(1);
    expect(carouselService.remove).toHaveBeenCalledWith('abrakadabra');
  });

  it('#ngOnChanges should not update data', () => {
    component['filterSlides'] = jasmine.createSpy('filterSlides');
    component.ngOnChanges({aem: undefined});
    component.ngOnChanges({aem: { previousValue: undefined }} as any);
    expect(component['filterSlides']).not.toHaveBeenCalled();
  });

  it('#ngOnChanges should update data', () => {
    component['filterSlides'] = jasmine.createSpy('filterSlides');
    component.ngOnChanges({aem: { previousValue: {} }} as any);
    expect(component['filterSlides']).toHaveBeenCalledTimes(1);
  });

  it('trackBySlide', () => {
    expect(component.trackBySlide(<any>{
      offerName: '1',
      displayOrder: '0'
    })).toEqual('10');
  });

  describe('handleClick', () => {
    let event, slide;
    beforeEach(() => {
      event = { preventDefault: jasmine.createSpy('preventDefault') };
      slide = {
        offerName: 'offerName',
        offerTitle: 'offerTitle',
        appUrl: 'appLink',
        appTarget: '_self'
      };
      component.handleClick(event, slide);
      expect(event.preventDefault).toHaveBeenCalled();
      expect(bannerClickService.handleFeaturedAemSlideClick).toHaveBeenCalledWith('appLink', '_self');
    });
    it('should handle click 1 time', () => {});
    it('should handle click 2 times (gtm pushed only once)', () => {
      component.handleClick(event, slide);
    });
    afterEach(() => {
      expect(gtmService.push).toHaveBeenCalledTimes(1);
    });
  });

  it('handleActiveSlide', () => {
    component.slides = <any>[{
      offerName: 'offerName',
      offerTitle: 'offerTitle'
    }];
    component.handleActiveSlide(1);
    expect(gtmService.push).toHaveBeenCalledTimes(1);
  });

  it('should test terms and conditions', () => {
    component.slides = <any>[{
      webTandC: 'testTC',
      mobTandCLink: 'testLink'
    }];
    component.termsAndConditions  = {
      showTC: false,
      text: undefined,
      href: undefined,
    };
    component.termsAndConditions = component.getTermsAndConditions(1);
    expect(component.termsAndConditions.showTC).toBeTruthy();
    expect(component.termsAndConditions.text).toEqual('testTC');
    expect(component.termsAndConditions.href).toEqual('testLink');

    component.slides = <any>[{
      offerName: 'offerName',
      offerTitle: 'offerTitle'
    }];
    component.termsAndConditions = component.getTermsAndConditions(1);
    expect(component.termsAndConditions.showTC).toBeFalsy();
    expect(component.termsAndConditions.text).toBeUndefined();
    expect(component.termsAndConditions.href).toBeUndefined();
  });

  it('handleActiveSlide 2 times', () => {
    component.slides = <any>[{
      offerName: 'offerName',
      offerTitle: 'offerTitle'
    }];
    component.handleActiveSlide(1);
    component.handleActiveSlide(1);
    expect(gtmService.push).toHaveBeenCalledTimes(1);
  });

  it('handleActiveSlide', () => {
    component.slides = [];
    component.handleActiveSlide(1);
    expect(gtmService.push).not.toHaveBeenCalled();
  });

  it('handleActiveSlide', () => {
    component.slides = <any>[{
      offerName: 'offerName',
      offerTitle: 'offerTitle'
    }];
    component.handleActiveSlide(2);
    expect(gtmService.push).not.toHaveBeenCalled();
  });

  describe('filters', () => {
    const res: any = [{
      selectChannels: ['1/app', '1/desktop', '1/mobile', '1/tablet'],
      userType: ['1/anonymous'],
      imsLevel: ['1/10', '1/2']
    }];

    beforeEach(() => {
      component['deviceService'].isTablet = true;
      component['deviceService'].isMobile = true;
      component['deviceService'].isDesktop = true;
      component['deviceService'].isWrapper = true;
      aem.data = res;
    });

    it('filterByChannel & USER_TYPES.ANONYMOUS', () => {
      component.ngOnInit();
      expect(component.slides).toEqual(res);
    });

    it('filterByChannel & USER_TYPES', () => {
      user.username = 'testUser';
      user.vipLevel = '10';
      component.ngOnInit();
      expect(component.slides).toEqual(res);
    });
  });

  it('#getUserType should return type for existing ladbrokes user', () => {
    environment.brand = 'ladbrokes';
    storage.get.and.returnValue({});
    expect(component['getUserType']()).toBe('existing');
  });

  it('#getUserType should return type for new ladbrokes user', () => {
    environment.brand = 'ladbrokes';
    storage.get.and.returnValue(null);
    expect(component['getUserType']()).toBe('new');
  });

  it('should use OnPush strategy', () => {
    expect(FeaturedAemComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
