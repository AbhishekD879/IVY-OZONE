import { of } from 'rxjs';
import { StreamBetTutorialPopUpComponent } from './stream-bet-tutorial-pop-up.component';

describe('StreamBetTutorialPopUpComponent', () => {
  let component: StreamBetTutorialPopUpComponent;
  let windowRefService;
  let deviceService;
  let storageService;
  let rendererService;
  let cmsService;
  beforeEach(() => {
    windowRefService = {
      document: {
        getElementById: jasmine.createSpy('getElementById'),
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          tagName: 'BODY'
        } as any),
        querySelectorAll: jasmine.createSpy().and.returnValue([
          { className: 'top-bar', remove: jasmine.createSpy() },
          { className: 'network-indicator-parent', remove: jasmine.createSpy() },
          { className: 'network-indicator-parent-lads', remove: jasmine.createSpy() }
        ]),
        getElementsByClassName: jasmine.createSpy().and.returnValue([
          { className: 'footer-wrapper', remove: jasmine.createSpy() },
          { className: 'timeline', remove: jasmine.createSpy() }
        ]),
        appendChild: jasmine.createSpy('appendChild'),
        contains: jasmine.createSpy('contains')
      }
    };
    deviceService = {
      isWrapper: true
    };
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    rendererService = {
      renderer: {
        removeClass: jasmine.createSpy(),
        addClass: jasmine.createSpy()
      }
    };
    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig')
    }
    component = new StreamBetTutorialPopUpComponent(windowRefService, rendererService, deviceService, cmsService, storageService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('ngOnInit', () => {
    it('should assign storage.set and get cms config for wrapper', () => {
      cmsService.getFeatureConfig.and.returnValue(of({ title: 'stream and bet native' }));
      component.ngOnInit();
      expect(component.streamBetTutorialConfigNative).toEqual({ title: 'stream and bet native' });
      expect(rendererService.renderer.addClass).toHaveBeenCalled();
    });
    it('should assign storage.set and get cms config for not wrapper', () => {
      deviceService.isWrapper = false;
      component.isStreambetTutorialDisplayed = false;
      cmsService.getFeatureConfig.and.returnValue(of({ title: 'stream and bet web' }));
      component.ngOnInit();
      expect(component.streamBetTutorialConfig).toEqual({ title: 'stream and bet web' });
      expect(rendererService.renderer.addClass).toHaveBeenCalled();
    });
    it('should not call cms and add class', () => {
      component.isStreambetTutorialDisplayed = true;
      cmsService.getFeatureConfig.and.returnValue(of({ title: 'stream and bet native' }));
      component.ngOnInit();
      expect(component.streamBetTutorialConfigNative).not.toEqual({ title: 'stream and bet web' });
    });
  });
  describe('closeTutorial', () => {
    it('should call remove calls and update popuploaded', () => {
      component.homeBody = { test: 'body' } as any;
      component.closeTutorial();
      expect(rendererService.renderer.removeClass).toHaveBeenCalled()
      expect(component.popUpLoaded).toBeFalse();
    })
  });
  describe('ngOndestroy', () => {
    it('should call closeTutorial', () => {
      spyOn(component, 'closeTutorial');
      component.ngOnDestroy();
      expect(component['closeTutorial']).toHaveBeenCalled();
    });
  });
});
