import { RaceCardHomeComponent } from './race-card-home.component';

describe('RaceCardHomeComponent', () => {
  let component: RaceCardHomeComponent;

  let nextRacesHomeService;
  let router;
  let cmsService;
  let sortByOptionsService;
  let horseracing;
  let gtmService;

  const raceOutcomeData = {} as any;
  const routingHelperService = {} as any;
  const localeService = {} as any;
  const sbFiltersService = {} as any;
  const filtersService = {} as any;
  const pubSubService = {} as any;
  const eventService = {} as any;
  const changeDetectorRef = {} as any;
  const virtualSharedService = { isVirtual: () => false } as any;
  const datePipe = { transform: () => '' } as any;

  beforeEach(() => {
    nextRacesHomeService = jasmine.createSpyObj(['trackNextRace']);
    router = jasmine.createSpyObj(['navigateByUrl']);
    component = new RaceCardHomeComponent(
      raceOutcomeData,
      routingHelperService,
      nextRacesHomeService,
      localeService,
      sbFiltersService,
      filtersService,
      pubSubService,
      router,
      eventService,
      virtualSharedService,
      datePipe,
      changeDetectorRef,
      cmsService,
      sortByOptionsService,
      horseracing,
      gtmService,
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('trackEvent', () => {
    const entity = {} as any;

    beforeEach(() => {
      spyOn(component, 'formEdpUrl').and.returnValue('formEdpUrl');
      component.moduleType = 'moduleType';
    });

    it(`should run input track function`, () => {
      component.trackFunction = jasmine.createSpy();

      component.trackEvent(entity);

      expect(component.trackFunction).toHaveBeenCalledWith(entity);
      expect(nextRacesHomeService.trackNextRace).not.toHaveBeenCalled();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });

    it(`should trackNextRace`, () => {
      component.trackEvent(entity);

      expect(nextRacesHomeService.trackNextRace).toHaveBeenCalledWith(entity, component.moduleType);
    });

    it(`should formEdpUrl`, () => {
      component.trackEvent(entity);

      expect(component.formEdpUrl).toHaveBeenCalledWith(entity);
    });

    it(`should navigate to formatted link`, () => {
      component.trackEvent(entity);

      expect(router.navigateByUrl).toHaveBeenCalledWith('formEdpUrl');
    });
  });
});
