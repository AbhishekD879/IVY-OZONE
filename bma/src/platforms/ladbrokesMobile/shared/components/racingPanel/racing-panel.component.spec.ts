import { RacingPanelComponent } from './racing-panel.component';
import {
  RacingPanelComponent as CoralRacingPanelComponent
} from '@shared/components/racingPanel/racing-panel.component';

describe('RacingPanelComponent', () => {
  let component: RacingPanelComponent;
  let localeService;
  let router;
  let routingHelperService,
  seoDataService,
  pubsub,
  gtmService;
  let lpAvailabilityService;
  let activatedRoute

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy().and.returnValue('Test string')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy().and.returnValue('EDPpath')
    };
    lpAvailabilityService = {
      check: jasmine.createSpy().and.returnValue(true)
    }
    activatedRoute = {
      snapshot: {
            paramMap: {
              get: jasmine.createSpy('get')
            }
          }

    }
    seoDataService = {};
    pubsub = {};
    gtmService = {};
    component = new RacingPanelComponent(
      localeService,
      router,
      routingHelperService,
      seoDataService,
      pubsub,
      gtmService,
      lpAvailabilityService,
      activatedRoute
    );
  });

  describe('instance', () => {
    it('should be created', () => {
      expect(component).toBeTruthy();
    });

    it('should extend CoralRacingPanelComponent', () => {
      expect(component instanceof CoralRacingPanelComponent).toBeTruthy();
    });
  });
});
