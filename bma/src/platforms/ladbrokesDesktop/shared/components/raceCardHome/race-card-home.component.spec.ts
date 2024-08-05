import { RaceCardHomeComponent } from './race-card-home.component';
import { of as observableOf } from 'rxjs';

describe('RaceCardHomeComponent', () => {
  let component: RaceCardHomeComponent,
      nextRacesHomeService,
      router,
      localeService,
      raceDataMock,
      pubSubService,
      sbFiltersService,
      changeDetectorRef,
      cmsService,
      sortByOptionsService,
      horseracing,
      gtmService;

  const raceOutcomeData = {} as any,
        routingHelperService = {} as any,
        filtersService = {} as any,
        eventService = {} as any,
        virtualSharedService = { isVirtual: () => false } as any,
        datePipe = { transform: () => ''} as any;

  beforeEach(() => {
    raceDataMock = [
      {
        markets: [
          {
            id: '12345',
            outcomes: []
          }
        ]
      }
    ];
    nextRacesHomeService = jasmine.createSpyObj(['trackNextRace']);
    router = jasmine.createSpyObj(['navigateByUrl']);
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('More')
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue([{
        id: 'outcome1'
      },
        {
          id: 'outcome2'
        }])
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        OUTCOME_UPDATED: 'OUTCOME_UPDATED'
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.callFake((preventCache, isPromise) => {
        if (isPromise) {
          return {
            then(callback) {
              callback({
                NativeConfig: {
                  visibleNotificationIconsHorseracing: {
                    multiselectValue: {
                      '0': 'ios',
                      '1': 'android'
                    },
                    value: 'ChepstowTN'
                  }
                }
              });
            }
          };
        } else {
          return observableOf({
            SortOptions: {
              enabled: true
            },
            TotePools: {
              Enable_UK_Totepools: true
            }
          });
        }
      })
    };
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Racecard'),
      set: jasmine.createSpy('set'),
    };
    horseracing = {
      getEvent: jasmine.createSpy('getEvent').and.returnValue(Promise.resolve(['poolEventEntity'])),
      isRacingSpecials: jasmine.createSpy('isRacingSpecials'),
      setTopBarData: jasmine.createSpy('setTopBarData'),
      validateTooltip: jasmine.createSpy('validateTooltip').and.returnValue(true)
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

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
    (component['_raceData'] as any) = raceDataMock;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component['viewFullRaceText']).toBe('More');
  });
  it('should assign seeAll to viewFullRaceText', () => {
    localeService.getString = jasmine.createSpy('getString').and.returnValue('seeAll');
    component.showHeader = false;
    component.ngOnInit();
    expect(component['viewFullRaceText']).toBe('seeAll');
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

  it('formatEventTerms', () => {
    expect(component.formatEventTerms('Each Way: 1/4 odds - places 1,2')).toEqual('E/W 1/4 Places 1-2');
  });
});
