import { RetailOverlayComponent } from '@retail/components/retailOverlay/retail-overlay.component';
import { of } from 'rxjs';

describe('RetailOverlayComponent', () => {
  let component: RetailOverlayComponent;
  let location;
  let storage;
  let retailService;
  let nativeBridgeService;
  let router;
  let changeDetectorRef;

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
      checkRetail: jasmine.createSpy('checkRetail').and.returnValue(of({}))
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

    component = new RetailOverlayComponent(
      location,
      storage,
      retailService,
      nativeBridgeService,
      router,
      changeDetectorRef
    );
  });

  it('should use OnPush strategy', () => {
    expect(RetailOverlayComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.showOverlay = jasmine.createSpy('showOverlay');
    });

    describe('isHomeURL === true', () => {
      beforeEach(() => {
        location.path.and.returnValue('home');
      });

      it('should call retailService.checkRetail and set retailOverlayRemain to 3', () => {
        storage.get.and.returnValue(null);
        retailService.checkRetail.and.returnValue(of(true));

        component.ngOnInit();

        retailService.checkRetail().subscribe(isRetail => {
          expect(component.showOverlay).toHaveBeenCalled();
          expect(storage.set).toHaveBeenCalledWith('retailOverlayRemain', 3);
          expect(storage.setCookie).toHaveBeenCalledWith('CONNECT_TRACKER', 'true', '.coral.co.uk', 183);
        });
      });

      it('should call retailService.checkRetail and set retailOverlayRemain to 0', () => {
        storage.get.and.returnValue(null);
        retailService.checkRetail.and.returnValue(of(false));

        component.ngOnInit();

        retailService.checkRetail().subscribe(isRetail => {
          expect(component.showOverlay).not.toHaveBeenCalled();
          expect(storage.set).toHaveBeenCalledWith('retailOverlayRemain', 0);
          expect(storage.setCookie).toHaveBeenCalledWith('CONNECT_TRACKER', 'true', '.coral.co.uk', 183);
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

    it('should do nothing if isHomeURL is false', () => {
      location.path.and.returnValue('test');

      component.ngOnInit();

      expect(retailService.checkRetail).not.toHaveBeenCalled();
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

      expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('retail_overlay', {});
    });

    it('should set isVisible to false', () => {
      component.hideOverlay();

      expect(component.isVisible).toBeFalsy();
    });

    it('should resetCount', () => {
      component.hideOverlay(true);

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
