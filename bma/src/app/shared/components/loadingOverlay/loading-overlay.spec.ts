import { LoadingOverlayComponent } from '@shared/components/loadingOverlay/loading-overlay.component';

describe('LoadingOverlayComponent', () => {
  let pubsub;
  let changeDetectorRef;
  let component;
  let vanillaApiService;
  beforeEach(() => {
    pubsub = {};
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new LoadingOverlayComponent(
      pubsub,
      changeDetectorRef,
      vanillaApiService
    );
  });

  it('should', () => {
    component.toggleVisibleState({
      overlay: true,
      spinner: true
    });

    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });
});
