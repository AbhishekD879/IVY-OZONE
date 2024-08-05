import { GamingOverlayComponent } from '@lazy-modules/gamingOverlay/components/gaming-overlay.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('GamingOverlayComponent', () => {
  let component, windowRef, pubSubService, rendererService;

  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        GAMING_OVERLAY_OPEN: 'GAMING_OVERLAY_OPEN',
        GAMING_OVERLAY_CLOSE: 'GAMING_OVERLAY_CLOSE'
      }
    };
    windowRef = {
      nativeWindow: {
        location: {
          href: ''
        }
      },
      document: {
        querySelector: jasmine.createSpy('querySelector'),
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener')
      }
    };
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy(),
        removeClass: jasmine.createSpy()
      }
    };

    component = new GamingOverlayComponent(
      windowRef,
      pubSubService,
      rendererService
    );
  });

  it('should create a component', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    pubSubService.subscribe.and.callFake((name, channel, callBack) => {
      if (channel === 'GAMING_OVERLAY_OPEN') {
        callBack();
      }
    });
    component.ngOnInit();
    expect(component.isActive).toBe(true);
    expect(windowRef.document.addEventListener).toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });

  describe('handleCloseClick', () => {
    it('on close icon clicked', fakeAsync(() => {
      component.handleCloseClick();
      tick(2500);
      expect(pubSubService.publish).toHaveBeenCalledWith('GAMING_OVERLAY_CLOSE');
      expect(component.isActive).toBe(false);
      expect(windowRef.document.removeEventListener).toHaveBeenCalled();
      expect(rendererService.renderer.addClass).toHaveBeenCalled();
      expect(rendererService.renderer.removeClass).toHaveBeenCalled();
    }));
  });

  describe('onSportsOverlayLoaded', () => {
    it('called on eventlistener', fakeAsync(() => {
      const mockEvent = {
        target: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({
            classList: { add: jasmine.createSpy(), remove: jasmine.createSpy() }
          })
        }
      };
      component.onSportsOverlayLoaded(mockEvent);
      tick(2500);
      expect(mockEvent.target.querySelector().classList.add).toHaveBeenCalled();
      expect(mockEvent.target.querySelector().classList.remove).toHaveBeenCalled();
    }));
  });
});
