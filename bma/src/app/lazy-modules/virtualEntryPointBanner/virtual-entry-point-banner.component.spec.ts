import { Router } from '@angular/router';
import { VirtualEntryPointBannerComponent } from './virtual-entry-point-banner.component';
import { VanillaApiService } from '@frontend/vanilla/core';
import { UserService } from '@app/core/services/user/user.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { VirtualHubService } from '@app/vsbr/services/virtual-hub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { of as observableOf } from 'rxjs';

describe('VirtualEntryPointBannerComponent', () => {
  let component: VirtualEntryPointBannerComponent;
  let windowRefService;
  let router: jasmine.SpyObj<Router>;
  let vanillaApiService: jasmine.SpyObj<VanillaApiService>;
  let userService: jasmine.SpyObj<UserService>;
  let deviceService: jasmine.SpyObj<DeviceService>;
  let virtualHubService: jasmine.SpyObj<VirtualHubService>;
  let gtmService: jasmine.SpyObj<GtmService>;
  let vEPService;
  let cmsService;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        open: jasmine.createSpy('open')
      }
    };
    router = jasmine.createSpyObj('Router', ['navigateByUrl']);
    vanillaApiService = jasmine.createSpyObj('VanillaApiService', ['getSiteCoreImages']);
    userService = jasmine.createSpyObj('UserService', ['isLoggedIn']);
    deviceService = jasmine.createSpyObj('DeviceService', ['isDesktop']);
    virtualHubService = jasmine.createSpyObj('VirtualHubService', ['getSiteCoreImages']);
    gtmService = jasmine.createSpyObj('GtmService', ['push']);
    vEPService = {
      targetTab : {
        subscribe: (cb) => cb()
      }
    }
    cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({VirtualEntryPointConfig: {enabled: true}}))};
    component = new VirtualEntryPointBannerComponent(
      windowRefService,
      router,
      vanillaApiService,
      userService,
      deviceService,
      virtualHubService,
      gtmService,
      vEPService,
      cmsService
    );
  });

  describe('@ngOninit', () => {
    it('it should call loadSiteCoreImageConfig', () => {
      component['loadSiteCoreImageConfig'] = jasmine.createSpy('loadSiteCoreImageConfig');
      component.targetTab = {
        interstitialBanners: {
          bannerEnabled: true,
          desktopBannerId: 'desktopBannerId',
          mobileBannerId: 'mobileBannerId'
        }
      } as any;
      component.ngOnInit();
      expect(component['loadSiteCoreImageConfig']).toHaveBeenCalled();
      component.targetTab = undefined;
      component.ngOnInit();
      component.targetTab = {} as any;
      component.isUnTiedSport = true;
      component.ngOnInit();

    })
  })
  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with default values', () => {
    expect(component.entryPointBanners).toBeUndefined();
    expect(component['selectedVirtualBanner']).toEqual({ imgUrl: '', altText: '' });
  });
  it('should load sitecore image config and set banner properties', () => {
    const siteCoreOffers = {
      offers: [
        { Id: 'desktopBannerId', imgUrl: 'desktopImageUrl' },
        { Id: 'mobileBannerId', imgUrl: 'mobileImageUrl' }
      ]
    };
    const targetTab = {
      interstitialBanners: {
        bannerEnabled: true,
        desktopBannerId: 'desktopBannerId',
        mobileBannerId: 'mobileBannerId'
      }
    } as any;
    virtualHubService.getSiteCoreImages.and.returnValue(observableOf(siteCoreOffers));

    component.targetTab = targetTab;
    component['loadSiteCoreImageConfig']();

    expect(virtualHubService.getSiteCoreImages).toHaveBeenCalledWith('EntryPointBanners');
    expect(component.entryPointBanners).toEqual(siteCoreOffers);
    virtualHubService.entryPointSiteCoreOffers = {} as any;
    component['loadSiteCoreImageConfig']();
    expect(virtualHubService.getSiteCoreImages).toHaveBeenCalledWith('EntryPointBanners');
    virtualHubService.entryPointSiteCoreOffers = { offers: [] } as any;
    component['loadSiteCoreImageConfig']();
    expect(virtualHubService.getSiteCoreImages).toHaveBeenCalledWith('EntryPointBanners');
  });

  it('should not called', () => {
    component.targetTab = {
      interstitialBanners: {
        bannerEnabled: true,
        desktopBannerId: 'desktopBannerId',
        mobileBannerId: 'mobileBannerId'
      }
    } as any;
    deviceService.isDesktop = false;
    expect(virtualHubService.getSiteCoreImages).not.toHaveBeenCalled();
    virtualHubService.entryPointSiteCoreOffers = { offers: [{}, {}, {}] } as any;
    component['loadSiteCoreImageConfig']();
    expect(virtualHubService.getSiteCoreImages).not.toHaveBeenCalled();
  })

  it('should handle banner click event', () => {
    const offer = {};
    const targetTabConfig = { interstitialBanners: { redirectionUrl: 'bannerUrl' } } as any;
    component.targetTab = targetTabConfig;

    component.onBannerClick(offer, targetTabConfig);

    expect(router.navigateByUrl).toHaveBeenCalledWith('bannerUrl');
  });

  it('should not redirect if  banner click if cta exists', () => {
    const offer = {};
    let targetTabConfig = { interstitialBanners: { redirectionUrl: 'bannerUrl', ctaButtonLabel: 'cta' } } as any;
    component.targetTab = targetTabConfig;

    component.onBannerClick(offer, targetTabConfig);

    expect(router.navigateByUrl).not.toHaveBeenCalledWith('bannerUrl');
    targetTabConfig = {} as any;
    component.targetTab = targetTabConfig;
    component.onBannerClick(offer, targetTabConfig);
    targetTabConfig = undefined;
    component.targetTab = targetTabConfig;
    component.onBannerClick(offer, targetTabConfig);
  });


  it('should handle CTA button click event', () => {
    const offer = { target: '_blank' };
    const targetTabConfig = { interstitialBanners: { redirectionUrl: 'ctaUrl' } } as any;
    component.targetTab = targetTabConfig;

    component.onCtaButtonClick(offer, targetTabConfig);

    expect(windowRefService.nativeWindow.open).toHaveBeenCalledWith('ctaUrl', '_blank');
  });

  it('should handle CTA button click event with external link', () => {
    const offer = { target: '_blank' };
    const targetTabConfig = { interstitialBanners: { redirectionUrl: 'http://external.com' } } as any;
    component.targetTab = targetTabConfig;

    component.onCtaButtonClick(offer, targetTabConfig);

    expect(windowRefService.nativeWindow.open).toHaveBeenCalledWith('http://external.com', '_blank');
  });

  it('should handle CTA button click event with internal link', () => {
    const offer = { target: '_self' };
    const targetTabConfig = { interstitialBanners: { redirectionUrl: 'internalUrl' } } as any;
    component.targetTab = targetTabConfig;

    component.onCtaButtonClick(offer, targetTabConfig);

    expect(router.navigateByUrl).toHaveBeenCalledWith('internalUrl');
  });

  it('should handle CTA button click event without redirection URL', () => {
    let offer = { target: '_self' };
    let targetTabConfig = { interstitialBanners: {} } as any;
    component.targetTab = targetTabConfig;

    component.onCtaButtonClick(offer, targetTabConfig);

    expect(router.navigateByUrl).not.toHaveBeenCalled();

    targetTabConfig = {} as any;
    component.targetTab = targetTabConfig;
    component.onCtaButtonClick(offer, targetTabConfig);
    targetTabConfig = undefined;
    offer = undefined;
    component.targetTab = targetTabConfig;
    component.onCtaButtonClick(offer, targetTabConfig);
  });


  it('should track CTA button click event with GTM', () => {
    const offer = { target: '_self' };
    const targetTabConfig = {
      interstitialBanners: {
        ctaButtonLabel: 'CTA Button',
        redirectionUrl: 'ctaUrl'
      }
    } as any;
    component.targetTab = targetTabConfig;
    component.onCtaButtonClick(offer, targetTabConfig);

    expect(gtmService.push).toHaveBeenCalledWith('Event.Tracking', {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'banner',
      'component.LabelEvent': 'virtual sports',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'football virtual banner',
      'component.LocationEvent': 'event details page',
      'component.EventDetails': 'CTA Button cta',
      'component.URLclicked': 'ctaUrl'
    });
  });

  it('should track banner click event with GTM', () => {
    const offer = { target: '_self' };
    const targetTabConfig = {
      interstitialBanners: {
        redirectionUrl: 'bannerUrl'
      }
    } as any;
    component.targetTab = targetTabConfig;
    component.onBannerClick(offer, targetTabConfig);

    expect(gtmService.push).toHaveBeenCalledWith('Event.Tracking', {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'banner',
      'component.LabelEvent': 'virtual sports',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'football virtual banner',
      'component.LocationEvent': 'event details page',
      'component.EventDetails': 'banner click',
      'component.URLclicked': 'bannerUrl'
    });
  });

  it('should track banner load event with GTM', () => {
    component['onBannerLoadGTMEvent']();

    expect(gtmService.push).toHaveBeenCalledWith('contentView', {
      event: 'contentView',
      'component.CategoryEvent': 'banner',
      'component.LabelEvent': 'virtual sports',
      'component.ActionEvent': 'load',
      'component.PositionEvent': 'football virtual banner',
      'component.LocationEvent': 'event details page',
      'component.EventDetails': 'football virtual banner',
      'component.URLclicked': 'not applicable'
    });
  });


  it('should return true if banner position matches index', () => {
    component.targetTab = {
      interstitialBanners: {
        bannerPosition: 2, 
      },
    } as any;
    component.eventsBySections = [{}, {}, {}]; 

    const result = component.isBannerPositionEnabled(2);

    expect(result).toBe(true);
  });

  it('should return true if last item and banner position is greater than or equal to the last item index', () => {
    component.targetTab = {
      interstitialBanners: {
        bannerPosition: 6, 
      },
    } as any;
    component.eventsBySections = [{}, {}, {}, {}]; 

    const result = component.isBannerPositionEnabled(4);

    expect(result).toBe(true);
  });

  it('should return tundefined', () => {
    component.targetTab = {
      interstitialBanners: {
        bannerPosition: 6, 
      },
    } as any;
    component.eventsBySections = undefined

    const result = component.isBannerPositionEnabled(4);

    expect(result).toBe(false);
  });

  it('should return true if index is -1', () => {

    component.targetTab = {
      interstitialBanners: {
        bannerPosition: 0,
      },
    } as any;
    const result = component.isBannerPositionEnabled(-1);

    expect(result).toBe(true);
  });

  it('should return false if banner position does not match index and it is not the last item', () => {
    component.targetTab = {
      interstitialBanners: {
        bannerPosition: 2, 
      },
    } as any;
    component.eventsBySections = [{}, {}, {}]; 

    const result = component.isBannerPositionEnabled(1);

    expect(result).toBe(false);
  });

  it('should target tab undefined', () => {
    component.eventsBySections = [{}, {}, {}]; 

    const result = component.isBannerPositionEnabled(3);

    expect(result).toBe(false);
  });

  it('should interstitialBanners undefined', () => {
    component.targetTab = {
     
    } as any;
    component.eventsBySections = [{}, {}, {}]; 

    const result = component.isBannerPositionEnabled(3);

    expect(result).toBe(false);
  });

describe('getBannerImageUrl', () => {
  it('getBannerImageUrl', () => {
    component.isUnTiedSport = true;
    component.isBannerPositionEnabled = () => true
    component.targetTab = {interstitialBanners : {desktopBannerId: 1, bannerEnabled: true} as any} as any;
    component.entryPointBanners = {offers : [{Id: 1, imgUrl: 'imgUrl'} as any]}
    deviceService.isDesktop = true;
    component['getBannerImageUrl']();
    deviceService.isDesktop = false;
    component['getBannerImageUrl']();
  })

  it('getBannerImageUrl targetrab undefined', () => {
    component.isUnTiedSport = true;
    component.isBannerPositionEnabled = () => true
    component.targetTab = undefined;
    component.entryPointBanners = {offers : [{Id: 1, imgUrl: 'imgUrl'} as any]}
    deviceService.isDesktop = true;
    component['getBannerImageUrl']();
    deviceService.isDesktop = false;
    component['getBannerImageUrl']();
  })

  it('getBannerImageUrl interstitialBanners undeifned', () => {
    component.isUnTiedSport = true;
    component.isBannerPositionEnabled = () => true
    component.targetTab = {interstitialBanners_1 : {desktopBannerId: 1, bannerEnabled: true} as any} as any;
    component.entryPointBanners = {offers : [{Id: 1, imgUrl: 'imgUrl'} as any]}
    deviceService.isDesktop = true;
    component['getBannerImageUrl']();
    deviceService.isDesktop = false;
    component['getBannerImageUrl']();
  })

  it('getBannerImageUrl interstitialBanners undeifned', () => {
    component.isUnTiedSport = true;
    component.isBannerPositionEnabled = () => true
    component.targetTab = {interstitialBanners_1 : {desktopBannerId: 1, bannerEnabled: true} as any} as any;
    component.entryPointBanners = {offers : [{Id: 1, imgUrl: 'imgUrl'} as any]}
    deviceService.isDesktop = true;
    component['getBannerImageUrl']();
    deviceService.isDesktop = false;
    component['getBannerImageUrl']();
  })

  it('getBannerImageUrl selectedVirtualBanner undefined', () => {
    component.isUnTiedSport = false;
    component.isBannerPositionEnabled = () => true
    component.targetTab = {interstitialBanners : {desktopBannerId: 1, bannerEnabled: true} as any} as any;
    component.entryPointBanners = {offers : [{Id: 11, imgUrl: 'imgUrl'} as any]}
    deviceService.isDesktop = true;
    component['getBannerImageUrl']();
    deviceService.isDesktop = false;
    component['getBannerImageUrl']();
  })
})


describe('isDisplay', () => {
  it('isDisplay', () => {
    component.isDisplayed = false
    component.isDisplay();
    expect(component.isDisplayed).toBeTruthy();
  })

})
});
