import { of } from 'rxjs';

import { FanzoneCbOverlayComponent } from '@app/lazy-modules/fanzone/components/fanzoneCbOverlay/fanzone-cb-overlay.component';
import { fanzoneComingBackData, fanzoneSiteCorePromotion } from '@lazy-modules/fanzone/mockData/fanzone-shared.mock';
import { SITECORE_PROMOTION_EMPTY_TEASER } from '@ladbrokesDesktop/bma/components/home/mockdata/home.component.mock';

describe('FanzoneCbOverlayComponent', () => {
  let component: FanzoneCbOverlayComponent;  
  let device;
  let windowRef;
  let timeService;
  let fanzoneStorageService;
  let storageService;
  let fanzoneSharedService;
  let changeDetectorRef;
  let userService;

  beforeEach(() => {
    device = {
      isIos: false,
      isAndroid: false,
      isMobile: true,
      isTablet: false,
      isWrapper: true
    };
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    timeService = {
      getHydraDaysDifference: jasmine.createSpy('getHydraDaysDifference').and.returnValue(of(-10)),
    };
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get').and.returnValue(null)
    };
    storageService = {
      remove: jasmine.createSpy('storageService.remove')
    }; 
    fanzoneSharedService = {
      getFanzoneBannerFromSiteCore: jasmine.createSpy('getFanzoneBannerFromSiteCore').and.returnValue(of(fanzoneSiteCorePromotion))
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    userService = {
      username: 'test'
    };
    createComponent();
    component.fanzoneCbData = fanzoneComingBackData as any;
    component.fanzoneCbData[0].iterator = {
      next: jasmine.createSpy('next')
    } as any;
  });

  function createComponent() {
    component = new FanzoneCbOverlayComponent(
      device,
      windowRef,
      timeService,
      fanzoneStorageService,
      storageService,
      fanzoneSharedService,
      changeDetectorRef,
      userService
    );
  }

  it('Show fanzone coming back popup if user visited first time', () => {
      component.ngOnInit();
      expect(component.showModal).toBeTruthy();
      expect(component.fanzoneBgImage).toBe('fzComingBackBgImageDesktop');
      expect(component.fanzoneBadge).toBe('fzComingBackBadgeUrlDesktop');
  });

  it('Hide fanzone coming back popup if user already visited', () => {
    timeService.getHydraDaysDifference = jasmine.createSpy('getHydraDaysDifference').and.returnValue(of(10)),
    fanzoneStorageService.get.and.returnValue(true);
    component.ngOnInit();
    expect(storageService.remove).toHaveBeenCalled();
    expect(component.showModal).toBeFalsy();
    expect(component.fanzoneCbData[0].iterator.next).toHaveBeenCalled();
  });

  it('Hide fanzone coming back popup if new fanzone season already started', () => {
    component.fanzoneCbData[0].fzComingBackDisplayFromDays = 0;
    fanzoneSharedService.getFanzoneBannerFromSiteCore.and.returnValue(of(SITECORE_PROMOTION_EMPTY_TEASER));
    component.ngOnInit();
    expect(component.showModal).toBeFalsy();
    expect(component.fanzoneBgImage).toBeUndefined();
    expect(component.fanzoneCbData[0].iterator.next).toHaveBeenCalled();
  });

  it('Closes dialog for ios device', () => {
    const closeDialogSpy = spyOn(FanzoneCbOverlayComponent.prototype['__proto__'], 'closeDialog');
    device.isIos = true;
    device.isWrapper = true;
    component.closeDialog();
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(component.fanzoneCbData[0].iterator.next).toHaveBeenCalled();
    expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('ios-modal-opened');
    expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('ios-modal-wrapper');
  });
  it('Closes dialog', () => {
    const closeDialogSpy = spyOn(FanzoneCbOverlayComponent.prototype['__proto__'], 'closeDialog');
    device.isIos = false;
    component.closeDialog();
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(component.fanzoneCbData[0].iterator.next).toHaveBeenCalled();
  });
});