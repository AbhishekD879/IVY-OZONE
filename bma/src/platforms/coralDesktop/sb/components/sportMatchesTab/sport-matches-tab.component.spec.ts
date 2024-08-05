import { DesktopSportMatchesTabComponent } from './sport-matches-tab.component';
import { of as observableOf } from 'rxjs';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';

describe('DesktopSportMatchesTabComponent', () => {
  let component: DesktopSportMatchesTabComponent;
  let activatedRoute;
  let marketSortService;
  let sportTabsService;
  let enhancedMultiplesService;
  let storageService;
  let pubSubService;
  let windowRef;
  let changeDetectorRef;
  let locationService;
  let favouritesService;
  let gtmService, routingHelperService, router;
  let cmsService;
  let competitionFiltersService;
  let vanillaApiService;
  let user
  let templateService;
  let deviceService;
  let timeService;

  beforeEach(() => {
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy()
        }
      }
    };

    cmsService = {
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(observableOf(Boolean))
    };

    competitionFiltersService = {
      filterEvents: jasmine.createSpy('filterEvents').and.returnValue([])
    };

    sportTabsService = {
      deleteEvent: jasmine.createSpy(),
      eventsBySections: jasmine.createSpy()
    };

    marketSortService = {
      setMarketFilterForMultipleSections: jasmine.createSpy()
    };

    enhancedMultiplesService = {
      getEnhancedMultiplesEvents: jasmine.createSpy().and.returnValue(observableOf([]).toPromise())
    };

    storageService = {
      get: jasmine.createSpy()
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {}
    };

    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake(cb => cb()),
        setInterval: jasmine.createSpy()
      }
    };

    changeDetectorRef = {
      detach: jasmine.createSpy(),
      detectChanges: jasmine.createSpy()
    };

    locationService = {
      path: jasmine.createSpy().and.callFake(() => 'matches/page')
    };

    gtmService = {
      push: jasmine.createSpy()
    };

    routingHelperService = {
      formInplayUrl: jasmine.createSpy(),
      formCompetitionUrl: jasmine.createSpy().and.returnValue('football/competitions')
    };

    favouritesService = {
      isFavouritesEnabled: true
    };

    router = {
      navigateByUrl: jasmine.createSpy()
    };
    vanillaApiService = {}
    user = {}

    vanillaApiService = {}
    user = {}

    templateService = {
      isListTemplate: (selectedMarket: string)=>{
       return oddsCardConstant.LIST_TEMPLATES.indexOf(selectedMarket) !== -1;
      }
    };
    deviceService = {};

    component = new DesktopSportMatchesTabComponent(
      activatedRoute,
      cmsService,
      sportTabsService,
      marketSortService,
      enhancedMultiplesService,
      storageService,
      pubSubService,
      windowRef,
      changeDetectorRef,
      locationService,
      gtmService,
      routingHelperService,
      favouritesService,
      router,
      competitionFiltersService,
      vanillaApiService,
      user,
      templateService,
      deviceService,
      timeService
    );

    component.sport = ({
      getByTab: jasmine.createSpy().and.returnValue(observableOf([]).toPromise()),
      readonlyRequestConfig: {categoryId: 129},
      subscribeLPForUpdates: jasmine.createSpy(),
      unSubscribeLPForUpdates: jasmine.createSpy(),
      config: {
        tier: 0
      }
    } as any);
  });

  it('#filterEvents', () => {
    spyOn<any>(component, 'initMarketSelector');
    component.filterEvents('someFilter');

    expect(component['initMarketSelector']).toHaveBeenCalledWith('someFilter');
  });

  it('should not filterEvents', () => {
    spyOn<any>(component, 'initMarketSelector');
    component['activeMarketFilter'] = 'testFilter';
    component.filterEvents('testFilter');

    expect(component['initMarketSelector']).not.toHaveBeenCalled();
  });

  it('should filterEvents', () => {
    spyOn<any>(component, 'initMarketSelector');
    component['activeMarketFilter'] = 'testFilter';
    component.filterEvents('newTestFilter');

    expect(component['initMarketSelector']).toHaveBeenCalledWith('newTestFilter');
  });
});
