import {
  TimelineTutorialOverlayComponent
} from '@lazy-modules/timeline/components/timelineTutorialOverlay/timeline-tutorial-overlay.component';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('TimelineTutorialOverlayComponent', () => {
  let component: TimelineTutorialOverlayComponent;
  let cms;
  let windowRef;
  let storageService;
  let rendererService;
  let domSanitizer;
  let elementRef;
  let changeDetectorRef;
  let pubSubService;

  const details = {
    showSplashPage: true,
    text: 'text'
  };

  beforeEach(() => {
    cms = {
      getTimelineTutorialDetails: jasmine.createSpy().and.returnValue(of(details))
    };
    windowRef = {
      document: {
        getElementById: jasmine.createSpy(),
        querySelector: jasmine.createSpy().and.returnValue({})
      }
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy().and.returnValue({})
    };
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass')
      }
    };

    domSanitizer = {
      sanitize: jasmine.createSpy('sanitize').and.returnValue('<HTML>'),
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('<HTML>')
    };

    elementRef = {
      nativeElement: {
        id: 'timelineTutorial',
        remove: () => {}
      }
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    pubSubService = {
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb()),
      API: {
        SHOW_TIMELINE_TUTORIAL: 'SHOW_TIMELINE_TUTORIAL'
      }
    };

    createComponent();

    component.timelineSettings = {
      id: '1',
      enabled: false,
      newIcon: true,
      pageUrls: '/horse-racing',
      liveCampaignId: 'id',
      liveCampaignName: 'name'
    };

    component.timelineTutorialElement = elementRef;
  });

  function createComponent() {
    component = new TimelineTutorialOverlayComponent(
      cms, windowRef, storageService, rendererService, domSanitizer, changeDetectorRef, pubSubService
    );
  }

  it('should create TimelineTutorialOverlayComponent instance', () => {
    component.handleTimelineTutorialDisplay = jasmine.createSpy();
    component.ngOnInit();

    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith(component['title'], pubSubService.API.SHOW_TIMELINE_TUTORIAL, jasmine.any(Function));
    expect(component.handleTimelineTutorialDisplay).toHaveBeenCalled();
  });

  describe('handleTimelineTutorialDisplay', () => {
    it('should show tutorial', () => {
      component['compareCampaignIds'] = jasmine.createSpy().and.returnValue(true);
      component.showTutorial = jasmine.createSpy();

      component.handleTimelineTutorialDisplay();

      expect(component.showTutorial).toHaveBeenCalled();
    });

    it('should trigger callback', () => {
      component['compareCampaignIds'] = jasmine.createSpy().and.returnValue(false);
      component.removeTutorial = jasmine.createSpy();

      component.handleTimelineTutorialDisplay();

      expect(component.removeTutorial).toHaveBeenCalled();
    });
  });

  describe('showTutorial', () => {
    beforeEach(() => {
      component.timelineSettings = {
        id: '1',
        enabled: true,
        newIcon: true,
        pageUrls: '/horse-racing',
        liveCampaignId: 'id',
        liveCampaignName: 'test'
      };
    });

    it('should call for showTutorial()', () => {
      component.ngOnInit();

      expect(component['cms'].getTimelineTutorialDetails).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should not show tutorial when getTimelineTutorialDetails returns null', () => {
      spyOn(component, 'removeTutorial');
      cms.getTimelineTutorialDetails = jasmine.createSpy('getTimelineTutorialDetails').and.returnValue(of(null));
      component.showTutorial();

      expect(component['cms'].getTimelineTutorialDetails).toHaveBeenCalled();
    });

    it('should call for showTutorial() headerTitle', () => {
      // eslint-disable-next-line @typescript-eslint/no-shadow
      const details = {
        showSplashPage: true,
        text: null
      };
      cms.getTimelineTutorialDetails = jasmine.createSpy('getTimelineTutorialDetails').and.returnValue(of(details));

      component.showTutorial();
      expect(component.headerTitle).toBe('');
    });
  });

  it('should call ngOnDestroy()', fakeAsync(() => {
    component['tltDetailsSub'] = { unsubscribe: jasmine.createSpy('unsubscribe')} as any;
    component['routeChangeSub'] = {unsubscribe: jasmine.createSpy('unsubscribe')} as any;
    tick();
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['title']);
    expect(component['tltDetailsSub'].unsubscribe).toHaveBeenCalled();
  }));

  describe('compareCampaignIds', () => {
    it('should return false if no timelineSettings', () => {
      component.timelineSettings = null;
      expect(component['compareCampaignIds']()).toBeFalsy();
    });

    it('should return false if timelineSettings disabled', () => {
      component.timelineSettings = {
        enabled: false
      } as any;
      expect(component['compareCampaignIds']()).toBeFalsy();
    });

    it('should return true if no storage data set yet', () => {
      component.timelineSettings = {
        enabled: true
      } as any;
      storageService.get = jasmine.createSpy('get').and.returnValue(null);
      expect(component['compareCampaignIds']()).toBeTruthy();
    });

    it('should return true if campaign ids are different', () => {
      component.timelineSettings = {
        enabled: true,
        liveCampaignId: '123'
      } as any;
      expect(component['compareCampaignIds']()).toBeTruthy();
    });

    it('should return true if campaign ids are the same', () => {
      component.timelineSettings = {
        enabled: true,
        liveCampaignId: '123'
      } as any;
      storageService.get = jasmine.createSpy('get').and.returnValue({ liveCampaignId: '123' });
      expect(component['compareCampaignIds']()).toBeFalsy();
    });
  });
});
