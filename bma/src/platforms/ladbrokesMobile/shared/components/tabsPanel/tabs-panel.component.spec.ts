import { of as observableOf } from 'rxjs';
import { LadbrokesTabsPanelComponent } from './tabs-panel.component';

describe('LadbrokesTabsPanelComponent', () => {
  let component: LadbrokesTabsPanelComponent;
  let elementRef;
  let locale;
  let router;
  let gtmTrackingService;
  let navigationService;
  let casinoMyBetsIntegratedService;

  beforeEach(() => {
    elementRef = { nativeElement: {} };
    router = {
      navigate: jasmine.createSpy('navigate'),
      events: observableOf({})
    };
    locale = jasmine.createSpyObj('locale', ['getString']);
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    gtmTrackingService = jasmine.createSpyObj('gtmService', ['setLocation', 'clearLocation']);
    casinoMyBetsIntegratedService = {};

    component = new LadbrokesTabsPanelComponent(
     elementRef,
     locale,
     router,
     gtmTrackingService,
     casinoMyBetsIntegratedService,
     navigationService
    );
  });

  describe('instance', () => {
    it('should be created', () => {
      expect(component).toBeTruthy();
    });
  });

});
