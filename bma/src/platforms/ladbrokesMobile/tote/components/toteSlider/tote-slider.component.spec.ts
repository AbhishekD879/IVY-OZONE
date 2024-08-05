import { of } from 'rxjs';
import { LadbrokesToteSliderComponent as ToteSliderComponent } from './tote-slider.component';

describe('LadbrokesToteSliderComponent', () => {
  let component: ToteSliderComponent;
  let gtmService: any;
  let toteService: any;
  let router: any;
  let racingGaService: any;
  let locale: any;
  let storage;
  let buildUtilityService;
  let vEPService;

  beforeEach(() => {
    gtmService = jasmine.createSpyObj('gtm', [ 'push' ]);
    toteService = {
      getEventById: jasmine.createSpy('getEventById').and.callFake(() => of({
        isResulted: false
      })),
      getToteLink: jasmine.createSpy('getToteLink').and.returnValue(of('foo'))
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };

    racingGaService = {
      trackModule: jasmine.createSpy('trackModule')
    };

    locale = {};

    vEPService ={}
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };

    buildUtilityService = {
      getLocalTime: jasmine.createSpy('buildUtilityService.getLoocalTime')
    };

    component = new ToteSliderComponent(
      toteService,
      gtmService,
      router,
      racingGaService,
      locale,
      storage,
      buildUtilityService,
      vEPService
    );
  });

  describe('trackModule method', () => {
    it('should send GA by trackModule', () => {
      component.trackModule('module', 'sport');

      expect(racingGaService.trackModule).toHaveBeenCalledWith('module', 'sport');
    });
  });
});
