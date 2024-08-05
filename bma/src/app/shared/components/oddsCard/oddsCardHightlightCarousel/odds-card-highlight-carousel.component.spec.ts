import { of } from 'rxjs';

import {
  OddsCardHighlightCarouselComponent
} from '@shared/components/oddsCard/oddsCardHightlightCarousel/odds-card-highlight-carousel.component';
import { HOMETEAMDATA, AWAYTEAMDATA, TEAMSPORTSDATA } from '@app/shared/mocks/odds-card-highlight-carousel.mock';

describe('OddsCardHighlightCarouselComponent', () => {
  let component: OddsCardHighlightCarouselComponent;
  let filtersService, templateService, marketTypeService, timeService, locale, coreToolsService, routingHelper,
    pubSubService, router, smartBoostsService, userService, commandService, changeDetectorRef,
    windowRef, betSlipSelectionsData, priceOddsButtonService, routingState, gtmTrackingService, gtmService,
    favouritesService, sportsConfigService, scoreParserService, sportEventHelperService,seoDataService;

  beforeEach(() => {
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('randomId'),
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
    };

    smartBoostsService = seoDataService = {};
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('2Up-market')
    };
    routingHelper = {};
    router = {};
    userService = {};
    commandService = {};
    windowRef = {};
    betSlipSelectionsData = {};
    priceOddsButtonService = {};
    routingState = {};
    gtmTrackingService = {};
    gtmService = {};
    favouritesService = {
      showFavourites: jasmine.createSpy('showFavourites').and.returnValue(of(null))
    };

    templateService = {
      getSportViewTypes: jasmine.createSpy(),
      getTemplate: jasmine.createSpy().and.returnValue({ name: 'tmplName' }),
      isMultiplesEvent: jasmine.createSpy()
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    timeService = {
      getLocalHourMin: jasmine.createSpy(),
      getEventTime: jasmine.createSpy()
    };

    marketTypeService = {
      isMatchResultType: () => {
      },
      isHomeDrawAwayType: () => true,
      isHeader2Columns: () => false
    };

    filtersService = {
      getTeamName: jasmine.createSpy().and.returnValue('team name')
    };

    pubSubService = {
      unsubscribe: jasmine.createSpy()
    };

    scoreParserService = {};

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {
          config: {}
        }
      })),
      getTeamColorsForSports: jasmine.createSpy('getTeamColorsForSports').and.returnValue(of(TEAMSPORTSDATA as any ))
    };

    sportEventHelperService = {
      isOutrightEvent: jasmine.createSpy('isOutrightEvent'),
      isSpecialEvent: jasmine.createSpy('isSpecialEvent')
    };

    component = new OddsCardHighlightCarouselComponent(
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
      seoDataService
    );

    component.event = {
      name: 'Test',
      id: 111,
      typeName: 'Some League',
      markets: [{
        id: 111,
        name: 'Test',
        outcomes: [{
          id: 111,
          name: 'Test'
        }]
      }],
      categoryCode: 'football',
      outcomeColumnsHeaders: null
    } as any;
    component.correctedOutcomes = [];

    component.selectedMarketObject = component.event.markets[0];
    component.outcomeColumnsTitles = ['Home', 'Draw', 'Away'];

    component['isShowMarketsCount'] = jasmine.createSpy();
    component['isStreamAvailable'] = jasmine.createSpy();
    component['transformSmartBoostsMarkets'] = jasmine.createSpy();
    component['getCorrectedOutcomes'] = jasmine.createSpy();
    component['extendWatchVariables'] = jasmine.createSpy();
    component['getOddsLabelClass'] = jasmine.createSpy();
    component['watchGroupHandler'] = jasmine.createSpy();
    component['addRecalculationEventListeners'] = jasmine.createSpy();
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('#hasEventScores', () => {
    expect(component.hasEventScores()).toBe(false);
    component.event.isStarted = true;
    component.event.comments = {} as any;
    component.event.outcomeStatus = false;
    expect(component.hasEventScores()).toBe(false);
    component.event.comments = {
      teams: {}
    };
    component.event.outcomeStatus = true;
    expect(component.hasEventScores()).toBe(false);
    component.event.outcomeStatus = false;
    expect(component.hasEventScores()).toBe(true);
  });

  it('#hasEventScores for non started Event should be falsy', () => {
    expect(component.hasEventScores()).toBe(false);
    component.event.isStarted = false;
    component.event.comments = {
      teams: {}
    };
    component.event.outcomeStatus = false;
    expect(component.hasEventScores()).toBe(false);
  });

  it('#ngOnInit should set PremChampLeague', () => {
    expect(component.isBadminton).toEqual(false);

    component.checkScores = jasmine.createSpy('checkScores').and.returnValue(false);
    spyOn<any>(component, 'isPremChampLeagueCheck').and.returnValue(true);
    spyOn<any>(component, 'setOutcomeColumnsHeaders');
    spyOn<any>(component, 'initBadmintonScores');
    spyOn<any>(component, 'getSportTeamImage');
    component.event.categoryName = 'Badminton';
    component.ngOnInit();
    expect(component.isKitsAvailable).toEqual(true);
    expect(component.isBadminton).toEqual(true);
    expect(component['initBadmintonScores']).toHaveBeenCalled();
    expect(component['isPremChampLeagueCheck']).toHaveBeenCalled();
    expect(component['setOutcomeColumnsHeaders']).toHaveBeenCalled();
    expect(component['getSportTeamImage']).toHaveBeenCalled();
  });

  it('#teamKit should format team name', () => {
    expect(component.teamKit('team::one')).toEqual('team-one');
  });

  it('#isPlayerActive checks if one player is active', () => {
    expect(component.isPlayerActive(1)).toBe(false);
    component.event.comments = {
      teams: {
        player_1: {
          isActive: false
        },
        player_2: {
          isActive: false
        }
      } as any
    };
    expect(component.isPlayerActive(1)).toBe(false);
    component.eventComments.teams.player_1.isActive = true;
    expect(component.isPlayerActive(1)).toBe(true);
    expect(component.isPlayerActive(2)).toBe(false);
    component.eventComments.teams.player_2.isActive = true;
    expect(component.isPlayerActive(1)).toBe(false);
    expect(component.isPlayerActive(2)).toBe(false);
  });

  it('#setOutcomeColumnsHeaders should set 1x2 headers for all sports except football', () => {
    component.event = {
      categoryCode: 'football',
      outcomeColumnsHeaders: null
    } as any;
    component.correctedOutcomes = [
      { outcomeMeaningMinorCode: 'H' } as any,
      { outcomeMeaningMinorCode: 'D' } as any,
      { outcomeMeaningMinorCode: 'A' } as any
    ];

    component['setOutcomeColumnsHeaders']();
    expect(component.outcomeColumnsHeaders).toEqual(['Home', 'Draw', 'Away']);

    component.event.categoryCode = 'other';
    component['setOutcomeColumnsHeaders']();
    expect(component.outcomeColumnsHeaders).toEqual(['1', 'x', '2']);

    component.event.categoryCode = 'other';
    component.correctedOutcomes = [
      { outcomeMeaningMinorCode: 'H' } as any,
      { outcomeMeaningMinorCode: 'D' } as any
    ];
    component['setOutcomeColumnsHeaders']();
    expect(component.outcomeColumnsHeaders).toEqual(['1', 'x']);
  });

  it('#setOutcomeColumnsHeaders should not set headers for undefined outcomes', () => {
    component.event = {
      categoryCode: 'football',
      outcomeColumnsHeaders: null
    } as any;
    component.correctedOutcomes = [
      undefined,
      { outcomeMeaningMinorCode: 'D' } as any,
      undefined
    ];

    component['setOutcomeColumnsHeaders']();
    expect(component.outcomeColumnsHeaders).toEqual([null, 'Draw', null]);
  });

  it('#isPremChampLeague checks if carousel is Premier or Champions league', () => {
    component.carouselByTypeId = true;
    component.event = {
      typeName: 'Premier England League',
      categoryCode: 'Football'
    } as any;
    expect(component['isPremChampLeagueCheck']()).toBe(true);
    component.event.typeName = 'Champions League';
    expect(component['isPremChampLeagueCheck']()).toBe(true);
    component.event.typeName = 'Other League';
    expect(component['isPremChampLeagueCheck']()).toBe(false);
    component.event.categoryCode = 'Other Sport';
    component.event.typeName = 'Champions League';
    expect(component['isPremChampLeagueCheck']()).toBe(false);
    component.carouselByTypeId = false;
    component.event.categoryCode = 'Football';
    component.event.typeName = 'Champions League';
    expect(component['isPremChampLeagueCheck']()).toBe(false);
  });

  it('#initBadmintonScores should set teams.home/away scores for badminton', () => {
    component.teamRoleCodes = ['player_1', 'player_2'];
    component.event = {
      comments: null
    } as any;
    component['initBadmintonScores']();
    expect(component.event.comments).toBeNull();
    expect(component.isEventHasCurrentPoints).toBeFalsy();

    component.event.comments = {
      teams: null
    };
    component['initBadmintonScores']();
    expect(component.event.comments.teams).toBeNull();
    expect(component.isEventHasCurrentPoints).toBeFalsy();

    component.event.comments = {
      runningSetIndex: 2,
      setsScores: {
        2: {
          1: '1',
          2: '0'
        }
      },
      teams: {
        player_1: {
          id: 1,
          isActive: false,
          score: '20'
        },
        player_2: {
          id: 2,
          isActive: false,
          score: '14'
        }
      } as any
    } as any;
    component['initBadmintonScores']();
    expect(component.event.comments.teams.home).toEqual({ score: '1', currentPoints: '20' });
    expect(component.event.comments.teams.away).toEqual({ score: '0', currentPoints: '14' });
    expect(component.isEventHasCurrentPoints).toBeTruthy();

    component.event.comments = {
      setsScores: {
        1: {
          1: '2',
          2: '3'
        }
      },
      teams: {
        player_1: {
          id: 1,
          isActive: false,
          score: '20'
        },
        player_2: {
          id: 2,
          isActive: false,
          score: '14'
        }
      } as any
    } as any;
    component['initBadmintonScores']();
    expect(component.event.comments.teams.home).toEqual({ score: '2', currentPoints: '20' });
    expect(component.event.comments.teams.away).toEqual({ score: '3', currentPoints: '14' });
    expect(component.isEventHasCurrentPoints).toBeTruthy();
  });

  describe('#getSportTeamImage', () => {
    it('Should get sports team data for both teams', () => {
      component.event.assetManagements = [];
      component.event.assetManagements.push(HOMETEAMDATA as any);
      component.event.assetManagements.push(AWAYTEAMDATA as any);
      component.getSportTeamImage();
      expect(component.homeTeamData).toEqual(HOMETEAMDATA as any);
      expect(component.awayTeamData).toEqual(AWAYTEAMDATA as any);
    });
    it('Should get empty  sports team data for both teams', () => {
      component.event.assetManagements = [];
      component['getSportTeamImage']();
      expect(component.homeTeamData).toEqual({});
      expect(component.awayTeamData).toEqual({});
    });
    it('Should get empty  sports team data for both teams', () => {
      delete component.event.assetManagements;
      component['getSportTeamImage']();
      expect(component.homeTeamData).toEqual({});
      expect(component.awayTeamData).toEqual({});
    });
  });

  describe('#checkForTeamsExist', () => {
    it('Should returns false if team does not exist', () => {
      component.homeTeamData = {};
      component.awayTeamData = {};
      expect( component['checkForTeamsExist']()).toBeFalsy();
    });
    it('Should returns true if team does  exist', () => {
      component.homeTeamData = HOMETEAMDATA as any;
      component.awayTeamData = AWAYTEAMDATA as any;
      expect( component['checkForTeamsExist']()).toBeTruthy();
    });
    it('Should returns true if team does  exist', () => {
      component.participants = [{id: 1}];
      expect( component['checkForTeamsExist']()).toBeFalsy();
    });
  });

  describe('#checkForTeamsImageData', () => {

    it('Should returns true if team does exist', () => {
      component.homeTeamData = HOMETEAMDATA as any;
      component.awayTeamData = AWAYTEAMDATA as any;
      component.homeTeamData.highlightCarouselToggle = true;
      component.awayTeamData.highlightCarouselToggle = true;
      expect(component.checkForTeamsImageData()).toBeTruthy();
    });
    it('Should returns false if team image data does not exist for first team case 2', () => {
      component.homeTeamData = HOMETEAMDATA as any;
      component.awayTeamData = AWAYTEAMDATA as any;
      component.homeTeamData.teamsImage = {'fileName' : ''} as any;
      expect(component.checkForTeamsImageData()).toBeFalsy();
    });

    it('Should returns false if team image data does not exist for first team case 1', () => {
      component.homeTeamData = HOMETEAMDATA as any;
      component.awayTeamData = AWAYTEAMDATA as any;
      delete component.homeTeamData.teamsImage;
      expect(component.checkForTeamsImageData()).toBeFalsy();
    });

    it('Should returns false if team image data does not exist for second team case 2', () => {
      component.homeTeamData = HOMETEAMDATA as any;
      component.awayTeamData = AWAYTEAMDATA as any;
      component.awayTeamData.teamsImage = {'fileName' : ''} as any;
      expect(component.checkForTeamsImageData()).toBeFalsy();
    });

    it('Should returns false if team image data does not exist for second team case 1', () => {
      component.homeTeamData = HOMETEAMDATA as any;
      component.awayTeamData = AWAYTEAMDATA as any;
      delete component.awayTeamData.teamsImage;
      expect(component.checkForTeamsImageData()).toBeFalsy();
    });
  });

  describe('#checkKits', () => {
    it('should call checkKits method with true', () => {
      component.isKitsAvailable = true;
      component.checkKits(true);

      expect(component.isKitsAvailable).toEqual(true);
    });

    it('should call checkKits method with false', () => {
      component.isKitsAvailable = true;
      component.checkKits(false);

      expect(component.isKitsAvailable).toEqual(false);
    });
  });

  it('#checkScores should set teams.home/away scores for darts with score', () => {
    component.event = {
      categoryId: '13',
      comments: {teams: {home: {score:2 }}}
    } as any;
    component.boxScore = false as any;

    const result = component.checkScores();
    expect(result).toBe(true);
  });
  it('#checkScores should set teams.home/away scores for no dart event score', () => {
    component.event = {
      categoryId: '32',
      comments: {teams: {home: {score:2 }}}
    } as any;
    component.boxScore = false as any;
    const result = component.checkScores();
    expect(result).toBe(true);
  });
  it('#checkScores should set teams.home/away scores for no darts ev boxscore should be true with score', () => {
    component.event = {
      categoryId: '32',
      comments: {teams: {home: {score:2 }}}
    } as any;
    component.boxScore = true as any;
    const result = component.checkScores();
    expect(result).toBe(false);
  });
  it('#checkScores should set when comments are undefined', () => {
    component.event = { categoryId: '32' } as any;
    component.boxScore = true as any;
    const result = component.checkScores();
    expect(result).toBe(false);
  });
  it('#checkScores should set when teams are undefined', () => {
    component.event = { categoryId: '32', comments: {team: {home: {score:2 }}} } as any;
    component.boxScore = true as any;
    const result = component.checkScores();
    expect(result).toBe(false);
  });
  
  describe('#twoUpMarket', () => {

    it("appendDrillDownTagNames to return appended drilldown market name", () => {
      const market = {
        drilldownTagNames: 'drilldownName_',
        name: 'twoup'
      }
      expect(component.appendDrillDownTagNames(market)).toBe('drilldownName_twoup,');
    });

    it("appendDrillDownTagNames to return only market name when no drilldownTagNames", () => {
      const market = {
        name: 'twoup'
      }
      expect(component.appendDrillDownTagNames(market)).toBe('twoup,');
    });
  });
});
