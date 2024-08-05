import { LoadingScreenComponent } from './loading-screen.component';
import { of } from 'rxjs';
import { fakeAsync, flush } from '@angular/core/testing';

describe('LoadingScreenComponent', () => {
  let component: LoadingScreenComponent;
  let deviceService: any;
  let cms: any;
  let windowRef: any;
  let changeDetectorRef: any;
  let pubsub: any;
  let routingState: any;

  beforeEach(() => {
    deviceService = {
      isTablet: true
    };
    cms = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        FeatureToggle: {
          skeletonLoadingScreen: true
        }
      }))
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    } as any;
    pubsub = {
      publish: jasmine.createSpy('publish'),
      API: {
        PERFORMANCE_MARK: 'PERFORMANCE_MARK'
      }
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy(),
      getCurrentUrl: jasmine.createSpy()
    };
    changeDetectorRef = jasmine.createSpyObj(['markForCheck']);

    component = new LoadingScreenComponent(deviceService, cms, windowRef, changeDetectorRef, pubsub, routingState);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('initial values', fakeAsync(() => {
    component.ngOnInit();
    expect(component.isTablet).toBeTruthy();
    expect(component.numberOfElements).toEqual(11);
    expect(component.numberOfSurfaceBets).toEqual(2);
    expect(component.numberOfPricesOrLines).toEqual(3);
    expect(component.numberOfGenericElements).toEqual(6);
    (component as any).device.isTablet = false;
    component.ngOnInit();
    expect(component.numberOfGenericElements).toEqual(3);
    flush();
    expect(component.skeletonFeatureEnabled).toBeTruthy();
    expect(component.initialized).toBeTruthy();
  }));

  describe('ngOnChanges', () => {
    beforeEach(() => {
      component['skeletonFeatureEnabled'] = true as any;
      component['initialized'] = true;
    });
    it('should not fail', () => {
      component.ngOnChanges({});
    });
    describe('should work correct if displayed prop changed', () => {
      it('#ngOnChanges should hide skeleton from the DOM', fakeAsync(() => {
        component.ngOnChanges({
          displayed: {
            currentValue: false
          }
        } as any);

        expect(component.hide).toBeTruthy();
        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 800);
      }));

      it('#ngOnChanges should remove from DOM if no CMS response yet', fakeAsync(() => {
        component['skeletonFeatureEnabled'] = undefined as any;
        component['initialized'] = false;
        component.longRenderView = true;
        component.ngOnChanges({
          displayed: {
            currentValue: false
          }
        } as any);
        flush();
        expect(component.hide).toBeTruthy();
        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      }));

      it('#ngOnChanges should`n call clear timeout if skeleton feature disabled', fakeAsync(() => {
        component['skeletonOnlyDisplayed'] = true as any;
        component['skeletonFeatureEnabled'] = false as any;
        component.ngOnChanges({
          displayed: {
            currentValue: false
          }
        } as any);
        expect(windowRef.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      }));

      it('#ngOnChanges should`n call clear timeout if onlySpinner is true', fakeAsync(() => {
        component['skeletonOnlyDisplayed'] = true as any;
        component['onlySpinner'] = true as any;
        component.ngOnChanges({
          displayed: {
            currentValue: false
          }
        } as any);
        expect(windowRef.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      }));

      it('#ngOnChanges should`n hide skeleton from the DOM', fakeAsync(() => {
        component['skeletonOnlyDisplayed'] = true as any;
        component.ngOnChanges({
          displayed: {
            currentValue: false
          }
        } as any);
        expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
        expect(component.hide).toBeFalsy();
      }));

      it('#ngOnChanges should not hide skeleton from the DOM', () => {
        component['skeletonOnlyDisplayed'] = false as any;
        component.ngOnChanges({
          displayed: {
            currentValue: true
          }
        } as any);
        expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
        expect(component.hide).toBeFalsy();
      });
    });
    describe('should work correct if skeletonOnlyDisplayed prop changed', () => {
      it('#ngOnChanges should not hide skeleton from the DOM', () => {
        component['displayed'] = true as any;
        component.ngOnChanges({
          skeletonOnlyDisplayed: {
            currentValue: false
          }
        } as any);
        expect(component.hide).toBeFalsy();
      });
      it('#ngOnChanges should hide skeleton from the DOM', () => {
        component['displayed'] = false as any;
        component.ngOnChanges({
          skeletonOnlyDisplayed: {
            currentValue: false
          }
        } as any);
        expect(component.hide).toBeTruthy();
      });
      it('#ngOnChanges should not hide skeleton from the DOM', () => {
        component.longRenderView = true;
        component['displayed'] = false as any;
        component.ngOnChanges({
          skeletonOnlyDisplayed: {
            currentValue: true
          }
        } as any);
        expect(component.hide).toBeFalsy();
      });
    });
    describe('publishPerformanceMark', () => {
      it('#publishPerformanceMarkShould get Called', () => {
        routingState.getCurrentSegment.and.returnValue('tab');
        component.publishPerformanceMark();
        expect(pubsub.publish).toHaveBeenCalledWith('PERFORMANCE_MARK');
      });
      it('#publishPerformanceMarkShould not get Called', () => {
        routingState.getCurrentSegment.and.returnValue('home');
        component.publishPerformanceMark();
        expect(pubsub.publish).not.toHaveBeenCalled();
      });
    });
  });
});
