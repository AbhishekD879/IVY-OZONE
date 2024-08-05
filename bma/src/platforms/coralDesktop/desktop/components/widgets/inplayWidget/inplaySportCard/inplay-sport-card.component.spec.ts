import { InplaySportCardComponent } from './inplay-sport-card.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { of as observableOf } from 'rxjs';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

describe('InplaySportCardComponent', () => {
  let component: InplaySportCardComponent;
  let pubSubService,
    sportEventHelperService,
    filtersService,
    routingHelperService,
    router,
    marketTypeService,
    sportsConfigService,
    seoDataService;
  const expectedSportConfig = {
    path: 'football',
    id: '16',
    specialsTypeIds: [2297, 2562],
    dispSortName: 'MR',
    primaryMarkets: '|Match Betting|',
    viewByFilters: ['byLeaguesCompetitions', 'byTime'],
    oddsCardHeaderType: 'homeDrawAwayType',
    isMultiTemplateSport: false
  };

  beforeEach(() => {
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        DELETE_SELECTION_FROMCACHE: 'DELETE_SELECTION_FROMCACHE'
      }
    };
    sportEventHelperService = {
      getEventNames: jasmine.createSpy('getEventNames'),
      isFootball: jasmine.createSpy('isFootball'),
      isEventSecondNameAvailable: jasmine.createSpy('isEventSecondNameAvailable'),
      getMarketsCount: jasmine.createSpy('getMarketsCount'),
      isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType'),
      isStreamAvailable: jasmine.createSpy('isStreamAvailable').and.returnValue(true),
      showMarketsCount: jasmine.createSpy('showMarketsCount').and.returnValue(true),
    };
    filtersService = {
      groupBy: jasmine.createSpy('groupBy')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEDPURL').and.returnValue('fakeUrl')
    };
    router = {
      navigateByUrl: jasmine.createSpy(),
      events: {
        subscribe: jasmine.createSpy()
      }
    } as any;
    marketTypeService = {
      isMatchResultType: jasmine.createSpy('isMatchResultType').and.returnValue(false),
      isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType').and.returnValue(false)
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf(expectedSportConfig))
    };

    component = new InplaySportCardComponent(
      pubSubService,
      sportEventHelperService,
      filtersService,
      routingHelperService,
      router,
      marketTypeService,
      sportsConfigService,
      seoDataService
    );

    component.event = {
      id: 1,
      markets: [{}]
    } as ISportEvent;
  });

  describe('InplaySportCardComponent', () => {
    it('should redirect to EDP', () => {
      component.goToEvent(false, {} as ISportEvent);
      expect(router.navigateByUrl).toHaveBeenCalledWith('fakeUrl');
    });

    it('should return URL only', () => {
      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(component.goToEvent(false, {} as ISportEvent)).toEqual('fakeUrl');
    });

    it('should return URL and not redirect to EDP', () => {
      component.goToEvent(true, {} as ISportEvent);

      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(component.goToEvent(false, {} as ISportEvent)).toEqual('fakeUrl');
    });

    it('should test isOddButtonShown method according to event temlpate', () => {
      component.event = {
        oddsCardHeaderType: 'homeDrawAwayType'
      } as any;

      component['headerHas2Columns'] = false;
      component['headerHas3Columns'] = false;

      expect(component.isOddButtonShown(0)).toBeTruthy();
      expect(component.isOddButtonShown(1)).toBeTruthy();
      expect(component.isOddButtonShown(2)).toBeTruthy();
    });

    it('should test isOddButtonShown method according to event temlpate', () => {
      component.event = {
        oddsCardHeaderType: 'oneThreeType'
      } as any;

      component['headerHas2Columns'] = false;
      component['headerHas3Columns'] = false;

      expect(component.isOddButtonShown(0)).toBeTruthy();
      expect(component.isOddButtonShown(1)).toBeTruthy();
      expect(component.isOddButtonShown(2)).toBeTruthy();
    });

    it('should test isOddButtonShown method according to event temlpate', () => {
      component.event = {
        oddsCardHeaderType: undefined
      } as any;

      component['headerHas2Columns'] = false;
      component['headerHas3Columns'] = true;

      expect(component.isOddButtonShown(0)).toBeTruthy();
      expect(component.isOddButtonShown(1)).toBeTruthy();
      expect(component.isOddButtonShown(2)).toBeTruthy();
    });

    it('should test isOddButtonShown method according to event temlpate', () => {
      component.event = {
        oddsCardHeaderType: 'oneTwoType'
      } as any;

      component['headerHas2Columns'] = true;
      component['headerHas3Columns'] = false;

      expect(component.isOddButtonShown(0)).toBeTruthy();
      expect(component.isOddButtonShown(1)).toBeFalsy();
      expect(component.isOddButtonShown(2)).toBeTruthy();
    });
  });

  describe('NgOnInit', () => {
    it(`should define market, isEventSecondNameAvailable, eventNames, isFootball, marketsCount properties`, () => {
      component.ngOnInit();

      expect(component.market).toEqual({} as IMarket);
      expect(sportEventHelperService.isEventSecondNameAvailable).toHaveBeenCalledWith(component.event);
      expect(sportEventHelperService.getEventNames).toHaveBeenCalledWith(component.event);
      expect(sportEventHelperService.getMarketsCount).toHaveBeenCalledWith(component.event);
    });

    it('should define headerHas2Columns as false', () => {
      marketTypeService = {
        isMatchResultType: jasmine.createSpy('isMatchResultType').and.returnValue(true),
        isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType').and.returnValue(true)
      };

      expect(component['headerHas2Columns']).toBeFalsy();
    });
  });

  describe('NgOnDestroy', () => {
    it('should unsubscribe from sports config', () => {
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('in-play-sport-card-1');
      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('ngOnDestroy: should not unsubscribe from sports config', () => {
      component['sportsConfigSubscription'] = undefined;
      component.ngOnDestroy();

      expect(component['sportsConfigSubscription']).not.toBeDefined();
    });
  });

  describe('trackById', () => {
    it('should return id in outcome.id_index format', () => {
      const actualResult = component.trackById(1, {id: '1'} as IOutcome);

      expect(actualResult).toEqual('1_1');
    });

    it('should return index', () => {
      const actualResult = component.trackById(1, {} as IOutcome);

      expect(actualResult).toEqual('1');
    });
  });

  it('should call isStreamAvailable with result true', () => {
    const actualResult = component.isStreamAvailable();

    expect(actualResult).toBeTruthy();
  });

  it('should call showMarketsCount with result true', () => {
    const actualResult = component.showMarketsCount();

    expect(actualResult).toBeTruthy();
  });

  describe('isOddButtonShown', () => {
    it('should call isOddButtonShown with result true', () => {
      component['headerHas3Columns'] = false;
      const actualResult = component.isOddButtonShown(2);

      expect(actualResult).toBeTruthy();
    });

    it('should call isOddButtonShown with result false', () => {
      component['headerHas2Columns'] = true;
      component['headerHas3Columns'] = true;
      const actualResult = component.isOddButtonShown(1);

      expect(actualResult).toBeFalsy();
    });
  });

  describe('goToSeo', () => {
    it('should create seo ', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.goToSeo(event as any);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(event);
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith(event,'url');
    });
  });

});
