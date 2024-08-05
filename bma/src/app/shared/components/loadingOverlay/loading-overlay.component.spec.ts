import { LoadingOverlayComponent } from '@shared/components/loadingOverlay/loading-overlay.component';
import { Subject } from 'rxjs';

describe('LoadingOverlayComponent', () => {
  const name = 'LoadingOverlay';

  let component: LoadingOverlayComponent,
    pubsub,
    changeDetectorRef,
    vanillaApiService;

  beforeEach(() => {
    pubsub = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        TOGGLE_LOADING_OVERLAY: 'TOGGLE_LOADING_OVERLAY'
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    vanillaApiService = {
      playBreakSubject: new Subject<boolean>()
    };
    component = new LoadingOverlayComponent(pubsub, changeDetectorRef, vanillaApiService);
  });

  it('constructor', () => {
    expect(component.overlayVisible).toBeFalsy();
    expect(component.spinnerVisible).toBeFalsy();
    expect(component.NAME).toEqual(name);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(pubsub.subscribe).toHaveBeenCalledWith(name, pubsub.API.TOGGLE_LOADING_OVERLAY, jasmine.any(Function));
  });

  it('ngOnInit with subject', () => {
    component.ngOnInit();
    // const spyOnNext = spyOn(component['vanillaApiService'].playBreakSubject, 'next');
    vanillaApiService.playBreakSubject.next(true);
    expect(component.isOverlayPlayBreakAdjusted).toBeTruthy();
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubsub.unsubscribe).toHaveBeenCalledWith(name);
  });

  describe('toggleVisibleState', () => {
    it('should set remain initial value', () => {
      component['toggleVisibleState']({} as any);

      expect(component.overlayVisible).toBeFalsy();
      expect(component.spinnerVisible).toBeFalsy();
    });

    it('should set new overlay and spinner options', () => {
      component['toggleVisibleState']({ overlay: true, spinner: true });

      expect(component.overlayVisible).toBeTruthy();
      expect(component.spinnerVisible).toBeTruthy();
    });

    afterEach(() => {
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });
});
