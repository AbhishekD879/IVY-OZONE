import { LadbrokesSwitchersComponent } from './switchers.component';

describe('LadbrokesSwitchersComponent', () => {
  let component: LadbrokesSwitchersComponent;
  let localeService;
  let router;
  let gtmTrackingService;
  let domToolsService;
  let gtmService,filtersService;

  beforeEach(() => {
    localeService = {};
    router = {};
    domToolsService = {};
    gtmTrackingService = {};
    gtmService = {
      push: jasmine.createSpy()
    };
    component = new LadbrokesSwitchersComponent(
      localeService,
      router,
      gtmTrackingService,
      domToolsService,
      gtmService,filtersService
    );
  });

  describe('instance', () => {
    it('should be created', () => {
      expect(component).toBeTruthy();
    });
  });

  describe('#is5ASideTab', () => {
    it('should call is5ASideTab and retrun true', () => {
      expect(component.is5ASideTab('5-a-side')).toEqual(true);
    });

    it('should call is5ASideTab and retrun false', () => {
      expect(component.is5ASideTab('Main markets')).toEqual(false);
    });
  });
});
