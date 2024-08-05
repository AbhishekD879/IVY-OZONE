import { RaceCardInplayComponent } from './race-card-inplay.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { RacingGaService } from '@app/racing/services/racing-ga.service';


describe('#RaceCardComponent', () => {
  let component: RaceCardInplayComponent;
  let raceOutcomeData;
  let routingHelperService;
  let localeService;
  let domTools;
  let windowRef;
  let elementRef;
  let renderer;
  let commandService;
  let carouselService;
  let sbFiltersService;
  let filtersService;
  let pubSubService;
  let router;
  let templateService;
  let outcomeUpdateCb;
  let virtualSharedService;
  let datePipe;
  let nextRacesHomeService;
  let eventService;
  let changeDetectorRef;
  let sortByOptionsService;
  let racingGaService;
  let gtm;
  const mockString = 'More';

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue(mockString)
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, cb) => {
        if (method === 'OUTCOME_UPDATED') {
          outcomeUpdateCb = cb;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        location: {
          pathname: 'pathname'
        }
      }
    };
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    renderer = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(() => { })
      }
    };
    racingGaService = new RacingGaService(gtm, localeService, pubSubService);
    racingGaService.sendGTM = jasmine.createSpy('sendGTM');
    racingGaService.trackNextRacesCollapse = jasmine.createSpy('trackNextRacesCollapse');
    racingGaService.trackNextRace = jasmine.createSpy('trackNextRace');
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(racingGaService)),
      API: {
        RACING_GA_SERVICE: 'test'
      }
    };
    templateService = {
      genTerms: jasmine.createSpy().and.returnValue('test')
    };
    carouselService = {
      get: jasmine.createSpy('get').and.returnValue({
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous')
      })
    };
    domTools = {
      getWidth: jasmine.createSpy('getWidth')
    };
    filtersService = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    raceOutcomeData = {
      isGenericSilk: jasmine.createSpy('isGenericSilk'),
      isGreyhoundSilk: jasmine.createSpy('isGreyhoundSilk'),
      isNumberNeeded: jasmine.createSpy('isNumberNeeded'),
      getSilkStyle: jasmine.createSpy('getSilkStyle'),
      isSilkAvailable: jasmine.createSpy('isSilkAvailable'),
      isValidSilkName: jasmine.createSpy('isValidSilkName')
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue([{
        id: 'outcome1'
      },
      {
        id: 'outcome2'
      }])
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    virtualSharedService = {
      isVirtual: jasmine.createSpy('isVirtual'),
      formVirtualEventUrl: jasmine.createSpy('formVirtualEventUrl')
    };

    datePipe = {
      transform: () => '20:15'
    } as any;

    nextRacesHomeService = {
      getGoing: jasmine.createSpy('getGoing'),
      getDistance: jasmine.createSpy('getDistance')
    };
    eventService = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable').and.returnValue({
        liveStreamAvailable: true
      })
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Price'),
      set: jasmine.createSpy('set'),
    };
    component = new RaceCardInplayComponent(elementRef, domTools, raceOutcomeData, routingHelperService, windowRef, commandService,
      localeService, sbFiltersService, filtersService, renderer, carouselService, pubSubService, router, templateService,
      virtualSharedService, datePipe, nextRacesHomeService, eventService, changeDetectorRef, racingGaService, sortByOptionsService);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
  describe('ngOnChanges', () => {
    it('should call processOutcomes and generateEachWayTerms', () => {
      const changes = { raceData: { id: '1' } } as any;
      spyOn(component as any, 'processOutcomes');
      spyOn(component as any, 'generateEachWayTerms');
      component.ngOnChanges(changes);
      expect(component['processOutcomes']).toHaveBeenCalled();
      expect(component['generateEachWayTerms']).toHaveBeenCalled();
    });
    it('should not call processOutcomes and generateEachWayTerms', () => {
      spyOn(component as any, 'processOutcomes');
      spyOn(component as any, 'generateEachWayTerms');
      const changes = {} as any;
      component.ngOnChanges(changes);
      expect(component['processOutcomes']).not.toHaveBeenCalled();
      expect(component['generateEachWayTerms']).not.toHaveBeenCalled();
    });
  });

  describe('ngOnInit', () => {
    it('should call processOutcomes and generateEachWayTerms', () => {
      spyOn(component as any, 'processOutcomes');
      spyOn(component as any, 'generateEachWayTerms');
      component.ngOnInit();
      expect(component['processOutcomes']).toHaveBeenCalled();
      expect(component['generateEachWayTerms']).toHaveBeenCalled();
    });
  });
});
