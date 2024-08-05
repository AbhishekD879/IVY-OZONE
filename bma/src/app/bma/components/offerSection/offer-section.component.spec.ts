import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { OffersSectionComponent } from './offer-section.component';

describe('OffersSectionComponent', () => {
  let component: OffersSectionComponent;
  let cmsService;
  let existNewUserService;
  let carouselService;
  let casinoLinkService;
  let user;
  let windowRef;
  let gtmService;
  let deviceService;
  let coreTools;
  let pubSubService;
  let navigationService;
  let carousel;

  const offersData = [{
    name: 'offer',
    offers: [{}]
  }];

  beforeEach(() => {
    carousel = {
      toIndex: jasmine.createSpy('toIndex')
    };
    cmsService = {
      getOffers: jasmine.createSpy('getOffers').and.returnValue(of(offersData))
    };
    existNewUserService = {
      filterExistNewUserItems: jasmine.createSpy('filterExistNewUserItems').and.returnValue([])
    };
    carouselService = {
      get: jasmine.createSpy('get').and.returnValue(carousel)
    };
    casinoLinkService = {
      decorateCasinoLink: jasmine.createSpy('decorateCasinoLink').and.returnValue([{
        useDirectImageUrl: true,
        image: null,
        directImageUrl: 'url'
      }])
    };
    user = {
      vipLevel: false
    };
    windowRef = {
      nativeWindow: {
        location: {
          href: ''
        },
        setTimeout: jasmine.createSpy().and.callFake(cb => cb())
      }
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    deviceService = {
      strictViewType: true
    };
    coreTools = {
      deepClone: jasmine.createSpy('deepClone').and.callFake(v => v)
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };

    component = new OffersSectionComponent(
      cmsService,
      existNewUserService,
      carouselService,
      casinoLinkService,
      user,
      windowRef,
      gtmService,
      deviceService,
      coreTools,
      pubSubService,
      navigationService
    );
  });

  it('should init', () => {
    pubSubService.subscribe.and.callFake((name, channel, cb) => cb());
    spyOn(component as any, 'getOffers').and.callThrough();
    spyOn(component as any, 'checkOffersChanges').and.callThrough();

    component.ngOnInit();

    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'offersSection', [pubSubService.API.SESSION_LOGOUT, pubSubService.API.SESSION_LOGIN], jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith('offersSection', 'RELOAD_COMPONENTS', jasmine.any(Function));
    expect(component['getOffers']).toHaveBeenCalled();
    expect(component['checkOffersChanges']).toHaveBeenCalled();
  });

  it('should destroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('offersSection');
  });

  it('should go to slide', () => {
    component.gotToSlide(1, 1);
    expect(carouselService.get).toHaveBeenCalledWith('offers-carousel-1');
    expect(carousel.toIndex).toHaveBeenCalledWith(1);
  });

  describe('setActiveSlide', () => {
    it('should return true', () => {
      carouselService.get.and.returnValue({ currentSlide: 1 });
      expect(component.setActiveSlide(1, 1)).toBe(true);
    });

    it('should return false', () => {
      carouselService.get.and.returnValue(null);
      expect(component.setActiveSlide(1, 1)).toBe(false);
    });
  });

  it('should send GTM', () => {
    const offer: any = {
      name: 'offerName',
    };
    component.sendGTM(offer, 1);
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'banner',
      eventAction: 'click',
      eventLabel: 'offername',
      location: 'offers module',
      vipLevel: '',
      position: '2'
    }));
  });

  it('should redirect', () => {
    component.redirect('betslip/test');
    expect(component['navigationService'].openUrl).toHaveBeenCalledWith('betslip/test');
  });

  describe('trackBy', () => {
    const offer: any = {
      sportName: 'test',
      displayTo: 'category',
      name: 'offerName'
    };
    const offersList = {
      name: 'list',
      offers: [offer]
    };

    it('should trackByOffers', () => {
      expect(component.trackByOffers(1, offer)).toBe('1_test_category');
    });

    it('should trackByOffersData', () => {
      expect(component.trackByOffersData(2, offersList)).toBe('2_list_1');
    });

    it('should trackBySlide', () => {
      expect(component.trackBySlide(3, offer)).toBe('3_test_category');
    });
  });

  describe('onCarouselInit', () => {
    it(`should set isCarouselInited for current carousel`, () => {
      component.onCarouselInit(true, 3);
      expect(component.isCarouselInited[3]).toBeTruthy();
    });

    it(`should set isCarouselInited for current carousel`, () => {
      component.onCarouselInit(false, 1);
      expect(component.isCarouselInited[1]).toBeFalsy();
    });
  });

  describe('checkOffersChanges', () => {
    it('should set cmsData', () => {
      component['checkOffersChanges']();
      expect(component['cmsData']).toBe(offersData as any);
    });

    it('should not set cmsData', () => {
      cmsService.getOffers.and.returnValue(of(null));
      component['checkOffersChanges']();
      expect(component['cmsData']).toBeUndefined();
    });
  });

  describe('getOffers', () => {
    beforeEach(() => {
      spyOn(component as any, 'hideOffersWidget').and.callThrough();
    });

    it('should set offersData as empty array and hide widget', () => {
      component['getOffers']();
      expect(component.offersData).toEqual([]);
      expect(component['hideOffersWidget']).toHaveBeenCalledTimes(1);
    });

    it('should handle offers and hide widget', () => {
      spyOn(component as any, 'handlingOffers').and.returnValue([]);
      component['offersData'] = [];
      component['cmsData'] = [{}] as any;
      component['getOffers']();
      expect(component['handlingOffers']).toHaveBeenCalledTimes(1);
      expect(component['hideOffersWidget']).toHaveBeenCalledTimes(1);
    });

    it('should handle offers and do not hide widget', () => {
      spyOn(component as any, 'handlingOffers').and.returnValue([{}]);
      component['offersData'] = [];
      component['cmsData'] = [{}] as any;
      component['getOffers']();
      expect(component['handlingOffers']).toHaveBeenCalledTimes(1);
      expect(component['hideOffersWidget']).not.toHaveBeenCalled();
    });
  });

  it('handlingOffers', () => {
    existNewUserService.filterExistNewUserItems.and.callFake(v => v);
    casinoLinkService.decorateCasinoLink.and.callFake(v => v);

    const cmsData: any = [{
      offers: []
    }, {
      offers: [
        { useDirectImageUrl: true, directImageUrl: 'img' }, {}
      ]
    }];

    expect( component['handlingOffers'](cmsData) ).toEqual([{
      offers: [
        { useDirectImageUrl: true, directImageUrl: 'img', image: 'img' }, {}
      ]
    }] as any);
  });

  it('getOffersData should subscribe for SESSION_LOGOUT, SESSION_LOGIN, RELOAD_COMPONENTS', () => {
    component['getOffersData']('mobile');

    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith('offersSection', [pubSubService.API.SESSION_LOGOUT, pubSubService.API.SESSION_LOGIN], jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('offersSection', pubSubService.API.RELOAD_COMPONENTS, jasmine.any(Function));
  });
});
