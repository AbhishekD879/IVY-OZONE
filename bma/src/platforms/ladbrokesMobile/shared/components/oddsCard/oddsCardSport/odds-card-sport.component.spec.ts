import { OddsCardSportComponent } from '@ladbrokesMobile/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { of } from 'rxjs';

describe('LadOddsCardSportComponent', () => {
  let component: OddsCardSportComponent;

  let templateService, marketTypeService, timeService, locale, filtersService, coreToolsService, routingHelper,
    pubSubService, router, smartBoostsService, userService, commandService, changeDetectorRef,
    windowRef, betSlipSelectionsData, priceOddsButtonService, routingState, gtmTrackingService, gtmService,
    favouritesService, sportsConfigService, scoreParserService, sportEventHelperService,seoDataService;

  beforeEach(() => {
    templateService = {
      getSportViewTypes: () => {
        return {};
      },
      getTemplate: () => {
        return {};
      },
      isMultiplesEvent: () => false
    };

    marketTypeService = {
      isMatchResultType: jasmine.createSpy('isMatchResultType').and.returnValue(false),
      isHeader2Columns: jasmine.createSpy('isHeader2Columns').and.returnValue(false),
      isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType').and.returnValue(true)
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    timeService = {
      determineDay: () => 'today',
      getLocalHourMin: () => {},
      isInNext24HoursRange: () => true,
      getEventTime: jasmine.createSpy().and.returnValue('12:00, 12 Mar')
    } as any;

    locale = {
      getString: () => 'test'
    } as any;

    filtersService = {
      getTeamName: () => 'teamA',
      groupBy: jasmine.createSpy('groupBy').and.callFake(v => v)
    };

    coreToolsService = {
      hasOwnDeepProperty: jasmine.createSpy('hasOwnDeepProperty').and.callFake(
        (obj, path) => {
          const segments = path.split('.');
          if (!segments.length) {
            return;
          }
          let current = obj;
          while (typeof current === 'object' && segments.length) {
            current = current[segments.shift()];
          }
          if (!segments.length && current !== undefined) {
            return true;
          }
        }
      ),
      getOwnDeepProperty: jasmine.createSpy('getOwnDeepProperty').and.callFake(
        (obj, path) => {
          const segments = path.split('.');
          let current = obj;
          while (typeof current === 'object' && segments.length) {
            current = current[segments.shift()];
          }
          if (!segments.length) {
            return current;
          }
        }
      ),
      uuid: jasmine.createSpy('uuid').and.returnValue('randomId'),
    } as any;

    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('some url')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((name: string, chnl: any, func: Function) => func({ event: { id: 1 } } as any)),
      API: {
        OUTCOME_UPDATED: 'OUTCOME_UPDATED',
        DELETE_SELECTION_FROMCACHE: 'DELETE_SELECTION_FROMCACHE',
        EVENT_SCORES_UPDATE: 'EVENT_SCORES_UPDATE',
        EVENTS_CLOCK_UPDATE: 'EVENTS_CLOCK_UPDATE',
        MOVE_EVENT_TO_INPLAY: 'MOVE_EVENT_TO_INPLAY',
        ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION',
        BETSLIP_SELECTIONS_UPDATE: 'BETSLIP_SELECTIONS_UPDATE',
        ADD_TO_QUICKBET: 'ADD_TO_QUICKBET',
        REMOVE_FROM_QUICKBET: 'REMOVE_FROM_QUICKBET'
      }
    };

    router = seoDataService = {};

    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ })
    };

    userService = {};

    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(false)),
      API: {
        IS_ADDTOBETSLIP_IN_PROCESS: 'IS_ADDTOBETSLIP_IN_PROCESS'
      }
    };

    windowRef = {
      nativeWindow: {}
    };

    betSlipSelectionsData = {
      getSelectionsByOutcomeId: jasmine.createSpy('getSelectionsByOutcomeId').and.returnValue([{}])
    };

    priceOddsButtonService = {
      animate: jasmine.createSpy('animate').and.returnValue(Promise.resolve(true))
    };

    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment')
    };

    gtmTrackingService = {
      detectTracking: jasmine.createSpy('detectTracking')
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };

    favouritesService = {
      registerListener: () => {
        return { then: jasmine.createSpy('then')};
      },
      deRegisterListener: jasmine.createSpy('deRegisterListener'),
      add: jasmine.createSpy('add').and.returnValue({
        catch: jasmine.createSpy('catch')
      }),
      isFavourite: jasmine.createSpy().and.returnValue(Promise.resolve()),
      showFavourites: jasmine.createSpy('showFavourites').and.returnValue(of(true))
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {
          config: {}
        }
      }))
    };

    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType'),
      parseScores: jasmine.createSpy('parseScores')
    };

    sportEventHelperService = {
      isOutrightEvent: jasmine.createSpy('isOutrightEvent'),
      isSpecialEvent: jasmine.createSpy('isSpecialEvent')
    };

    component = new OddsCardSportComponent(
      templateService as any,
      marketTypeService as any,
      timeService as any,
      locale as any,
      filtersService as any,
      coreToolsService as any,
      routingHelper as any,
      pubSubService as any,
      router as any,
      smartBoostsService as any,
      userService as any,
      commandService as any,
      windowRef as any,
      betSlipSelectionsData as any,
      priceOddsButtonService as any,
      routingState as any,
      gtmTrackingService as any,
      gtmService as any,
      favouritesService as any,
      sportsConfigService as any,
      scoreParserService,
      sportEventHelperService,
      changeDetectorRef,
      seoDataService as any
    );

    component.event = {
      name: 'Test',
      id: 111,
      marketsCount: 3,
      markets: [{
        id: 111,
        name: 'Test',
        outcomes: [{
          id: 111,
          name: 'Test'
        }]
      }],
      categoryName: 'categoryName',
      isStarted: true,
      eventIsLive: true,
      comments: {
        teams: {
          home: {},
          away: {}
        }
      }
    } as any;
    component.teamRoleCodes = ['home', 'away'];
    component.selectedMarketObject = component.event.markets[0];
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {

    it('component properties should be initialized', () => {
      spyOn(component, 'goToEvent').and.returnValue('/edp');
      spyOn(component, 'isClockAllowed').and.returnValue(false);
      component.eventStartedOrLive = false;
      component.eventSecondName = 'foo';
      component.selectedMarket = '';
      component.ngOnInit();

      expect(component.goToEvent).toHaveBeenCalledWith(true);
      expect(component.linkToEventPage).toBe('/edp');

      expect(component.isClockAllowed).toHaveBeenCalled();
      expect(component.ifClockAllowed).toBe(false);

      expect(component.isTeamNames).toBe(true);
      expect(component.oddsLabel).toBe('12:00 12 Mar');
    });

    it('should handle MOVE_EVENT_TO_INPLAY pubSub update', () => {
      component['watchGroupHandler'] = jasmine.createSpy('watchGroupHandler');
      component.event.comments = {
        teams: {
          home: { },
          away: { },
        }
      } as any;
      component.eventStartedOrLive = true;
      pubSubService.subscribe.and.callFake((handlerName: string, updateType: string, callback: Function) => {
        if (updateType === 'MOVE_EVENT_TO_INPLAY') {
          const eventUpdate = {
            id: 1
          };
          callback(eventUpdate);
        }
      });
      component.event.id = 1;
      component.ngOnInit();

      expect(component['watchGroupHandler']).toHaveBeenCalledTimes(3);
    });
  });

  it('ngOnChanges with isEventStartedOrLive true', () => {
    const changes = {};
    const oddsLabel = 'test,123'; 
    component.oddsLabel = oddsLabel;
    component.isEventStartedOrLive = true;

    component.ngOnChanges(changes as any);

    expect(component.oddsLabel).toEqual(oddsLabel);
  });

  it('ngOnChanges with isEventStartedOrLive false', () => {
    const changes = {};
    const oddsLabel = 'test,123'; 
    component.oddsLabel = oddsLabel;
    component.isEventStartedOrLive = false;

    component.ngOnChanges(changes as any);

    expect(component.oddsLabel).not.toContain(',');
  });

  it('ngOnChanges with oddsLabel null', () => {
    const changes = {};
    component.oddsLabel = null;
    component.isEventStartedOrLive = false;

    component.ngOnChanges(changes as any);

    expect(component.oddsLabel).toEqual(null);
  });
});
