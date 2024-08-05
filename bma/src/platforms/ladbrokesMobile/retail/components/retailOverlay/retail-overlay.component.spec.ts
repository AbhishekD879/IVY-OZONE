import { RetailOverlayComponent } from '@ladbrokesMobile/retail/components/retailOverlay/retail-overlay.component';
import { of } from 'rxjs';

describe('RetailOverlayComponent', () => {
  let component: RetailOverlayComponent;
  let location;
  let storage;
  let retailService;
  let nativeBridgeService;
  let router;
  let changeDetectorRef;
  let gtmService;
  let userService;
  let deviceService;
  let trackEventData;

  beforeEach(() => {
    location = {
      path: jasmine.createSpy('path')
    };
    storage = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get'),
      setCookie: jasmine.createSpy('setCookie')
    };
    retailService = {
      checkGridRetail: jasmine.createSpy('checkGridRetail').and.returnValue(of({}))
    };
    nativeBridgeService = {
      onOpenPopup: jasmine.createSpy('onOpenPopup'),
      onClosePopup: jasmine.createSpy('onClosePopup')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    trackEventData = {
      event: 'trackEvent',
      eventCategory: 'Grid',
      eventAction: 'Menu',
      eventLabel: null
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    userService = {
      accountBusinessPhase: null,
    };
    deviceService = {
      isWrapper: false
    };

    component = new RetailOverlayComponent(
      location,
      storage,
      retailService,
      nativeBridgeService,
      router,
      changeDetectorRef,
      gtmService,
      userService,
      deviceService
    );
  });

  it('should use OnPush strategy', () => {
    expect(RetailOverlayComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.showOverlay = jasmine.createSpy('showOverlay');
    });

    describe('isWrapper === true', () => {
      beforeEach(() => {
        location.path.and.returnValue('home');
        deviceService.isWrapper = true;
      });

      it('should call retailService.checkGridRetail and set retailOverlayRemain to 0', () => {
        storage.get.and.returnValue(null);
        retailService.checkGridRetail.and.returnValue(of(false));

        component.ngOnInit();

        retailService.checkGridRetail().subscribe(isRetail => {
          expect(component.showOverlay).not.toHaveBeenCalled();
          expect(storage.set).toHaveBeenCalledWith('retailOverlayRemain', 0);
          expect(storage.setCookie).toHaveBeenCalledWith('grid', 'true', '.ladbrokes.com', 183);
        });
      });

      it('should call showOverlay', () => {
        const showCount = 1;
        storage.get.and.returnValue(showCount);

        component.ngOnInit();

        expect(component.showOverlay).toHaveBeenCalled();
        expect(storage.set).toHaveBeenCalledWith('retailOverlayRemain', showCount - 1);
      });

      it('should set isVisible to false',  () => {
        storage.get.and.returnValue(0);

        component.ngOnInit();

        expect(component.isVisible).toBeFalsy();
      });
    });

    it('should do nothing if isWrapper is false', () => {
      location.path.and.returnValue('test');

      component.ngOnInit();

      expect(retailService.checkGridRetail).not.toHaveBeenCalled();
      expect(component.showOverlay).not.toHaveBeenCalled();
      expect(storage.set).not.toHaveBeenCalled();
      expect(storage.setCookie).not.toHaveBeenCalled();
    });
  });

  describe('showOverlay', () => {
    it('should set isVisible to true', () => {
      component.showOverlay();

      expect(component.isVisible).toBeTruthy();
    });

    it('should call nativeBridgeService.onOpenPopup', () => {
      component.showOverlay();

      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith('retail_overlay');
    });

    it('should call markForCheck', () => {
      component.showOverlay();

      expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
    });
  });

  describe('hideOverlay', () => {
    it('should call nativeBridgeService.onClosePopup', () => {
      component.hideOverlay();
      userService.accountBusinessPhase = '';
      trackEventData.eventLabel = userService.accountBusinessPhase;
      expect(component['gtmService'].push).toHaveBeenCalledWith('trackEvent', trackEventData);
      expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('retail_overlay', {});
    });

    it('should set isVisible to false', () => {
      component.hideOverlay();
      userService.accountBusinessPhase = '';
      trackEventData.eventLabel = userService.accountBusinessPhase;
      expect(component['gtmService'].push).toHaveBeenCalledWith('trackEvent', trackEventData);
      expect(component.isVisible).toBeFalsy();
    });

    it('should resetCount', () => {
      component.hideOverlay(true);
      userService.accountBusinessPhase = '';
      trackEventData.eventLabel = userService.accountBusinessPhase;
      expect(component['gtmService'].push).toHaveBeenCalledWith('trackEvent', trackEventData);

      expect(storage.set).toHaveBeenCalledWith('retailOverlayRemain', 0);
    });
  });

  describe('navigateToRetail', () => {
    it('should call hideOverlay', () => {
      component.hideOverlay = jasmine.createSpy('hideOverlay');
      component.navigateToRetail();

      expect(component.hideOverlay).toHaveBeenCalledWith(false);
    });

    it('should navigate to /retail', () => {
      component.navigateToRetail();

      expect(router.navigate).toHaveBeenCalledWith(['/retail']);
    });
  });
});
