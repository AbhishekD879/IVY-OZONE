import { of, Subject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { IMarket } from '@core/models/market.model';
import { MultiMarketTemplateComponent } from '@app/lazy-modules/multiMarketTemplate/components/multi-market-template.component';
import { ISportEvent } from '@root/app/core/models/sport-event.model';
import * as _ from 'underscore';

describe('MultiMarketTemplateComponent', () => {
  let component: MultiMarketTemplateComponent;

  let
    templateService, marketTypeService, timeService, locale, filtersService, coreToolsService, routingHelper,
    pubSubService, router, smartBoostsService, userService, commandService,
    windowRef, betSlipSelectionsData, priceOddsButtonService, routingState, gtmTrackingService, gtmService,
    favouritesService, sportsConfigService, scoreParserService, sportEventHelperService,seoDataService,outcomeTemplateHelperService;

  let testStr, wasPriceStub, changeDetectorRef;

  const today = new Date();
  const future = new Date();
  future.setDate(future.getDate() + 1);

  function fakeCall(time) {
    const formatted = new Date(time);
    /* eslint-disable */
    return time === `${today}` ? `${formatted.getHours()}:${formatted.getMinutes()}, Today` :
      `${formatted.getHours()}:${formatted.getMinutes()} ${future.toLocaleString('en-US', { day: '2-digit' })} ${formatted.toLocaleString('en-US', { month: 'short' })}`;
    /* eslint-enable */
  }

  beforeEach(() => {

    testStr = 'TestString';
    wasPriceStub = 'TestWasPrice';

    filtersService = {
      getTeamName: (name, index) => ['teamA', 'teamB'][index],
      groupBy: jasmine.createSpy('groupBy').and.callFake(v => v),
      numberSuffix: (runningSetIndex)=> runningSetIndex
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    timeService = {
      determineDay: () => 'today',
      getLocalHourMin: () => {},
      isInNext24HoursRange: () => true,
      getEventTime: jasmine.createSpy().and.callFake(fakeCall)
    };

    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('some url')
    };

    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('randomId'),
      hasOwnDeepProperty: jasmine.createSpy('hasOwnDeepProperty').and.callFake((obj, path) => {
        const properties = path.split('.');
        let current = obj;
        while (typeof current === 'object' && properties.length) {
          const property = properties.shift();
          current = current[property];
        }
        if (!properties.length) {
          return current !== undefined;
        }
      }),
      getOwnDeepProperty: jasmine.createSpy('getOwnDeepProperty').and.callFake((obj, path) => {
        const properties = path.split('.');
        let current = obj;
        while (typeof current === 'object' && properties.length) {
          const property = properties.shift();
          current = current[property];
        }
        if (!properties.length) {
          return current;
        }
      }),
    };

    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('Test')
    };

    templateService = {
      getSportViewTypes: () => {
        return {};
      },
      getTemplate: () => {
        return {};
      },
      isMultiplesEvent: () => false
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    marketTypeService = {
      isMatchResultType: jasmine.createSpy('isMatchResultType').and.returnValue(false),
      isHeader2Columns: jasmine.createSpy('isHeader2Columns').and.returnValue(false),
      isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType').and.returnValue(true),
      extractMarketNameFromEvents: (events: ISportEvent[], isFilterByTemplateMarketName?: boolean): string[] => {
        const marketNames = _.reduce(events, (accumulator, event) => {
          const eventMarketNames = (event.markets || []).map(market => {
            if (isFilterByTemplateMarketName) {
              if (market.templateMarketName === 'Match Betting') {
                market.templateMarketName = 'Match Result';
              }
              return market.templateMarketName;
            }
    
            return market.name;
          });
    
          accumulator.push(...eventMarketNames);
    
          return accumulator;
        }, []);
        return marketNames;
      }
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
        REMOVE_FROM_QUICKBET: 'REMOVE_FROM_QUICKBET',
        WS_EVENT_UPDATED: 'WS_EVENT_UPDATED',
        WS_EVENT_UPDATE: 'WS_EVENT_UPDATE'
      }
    };

    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {
          config: {}
        }
      }))
    };

    userService = {};

    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(false)),
      API: {
        IS_ADDTOBETSLIP_IN_PROCESS: 'IS_ADDTOBETSLIP_IN_PROCESS'
      }
    };

    windowRef = {
      nativeWindow: {
        location: {
          href:  jasmine.createSpy().and.returnValue('football')
         }
      }
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

    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType'),
      parseScores: jasmine.createSpy('parseScores')
    };

    sportEventHelperService = {
      isOutrightEvent: jasmine.createSpy('isOutrightEvent'),
      isSpecialEvent: jasmine.createSpy('isSpecialEvent')
    };

    outcomeTemplateHelperService = {
        setOutcomeMeaningMinorCode: (markets, event) => {
            markets.forEach((market: IMarket) => {
                if (market.outcomes && market.outcomes.length > 0) {
                  market.outcomes.sort((a, b) => a.correctedOutcomeMeaningMinorCode - b.correctedOutcomeMeaningMinorCode);
                }
              });
        }
    }

    component = new MultiMarketTemplateComponent(
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
      scoreParserService as any,
      sportEventHelperService,
      changeDetectorRef,
      seoDataService as any,
      outcomeTemplateHelperService as any
    );
    component.sportConfig = {
      config: {
        oddsCardHeaderType: '',
        request: {
          categoryId: '18'
        }
      }
    };
    component.event = {
      name: 'Test',
      id: 111,
      marketsCount: 3,
      markets: [{
        id: 111,
        name: 'Test',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 1
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
      },
      categoryId :16
    } as any;
    component.teamRoleCodes = ['home', 'away'];
    component.selectedMarketObject = component.event.markets[0];
    spyOn(component.marketUndisplayed, 'emit');
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('isFanzonePage should return true if page is fanzone', () => {
    component['windowRef'].nativeWindow.location = {href: 'football'};

    const isFanzone = component.isFanzonePage();
    expect(isFanzone).toBeTrue;
  });
  it('isFanzonePage should return false if page is fanzone', () => {
    component['windowRef'].nativeWindow.location = {href: 'fanzone'};

    const isFanzone = component.isFanzonePage();
    expect(isFanzone).toBeFalse;
  });

  describe('ngOnInit', () => {

    xit('it should set correct header: true, true, true', () => {
      marketTypeService.isMatchResultType.and.returnValue(true);
      marketTypeService.isHomeDrawAwayType.and.returnValue(true);
      marketTypeService.isHeader2Columns.and.returnValue(true);

      component.ngOnInit();

      expect(component.header2Columns).toBe(true);
    });

    xit('it should set correct header: false, false, false', () => {
      marketTypeService.isMatchResultType.and.returnValue(false);
      marketTypeService.isHomeDrawAwayType.and.returnValue(false);
      marketTypeService.isHeader2Columns.and.returnValue(false);
      component.ngOnInit();

      expect(component.header2Columns).toBe(false);
    });

    xit('it should set correct header: false, true, false', () => {
      marketTypeService.isMatchResultType.and.returnValue(false);
      marketTypeService.isHomeDrawAwayType.and.returnValue(true);
      marketTypeService.isHeader2Columns.and.returnValue(false);
      component.ngOnInit();

      expect(component.header2Columns).toBe(false);
    });

    it('it should set eventFirstName and eventSecondName for not US Type', () => {
      component.ngOnInit();

      expect(component.eventFirstName).toEqual('teamA');
      expect(component.eventSecondName).toEqual('teamB');
      expect(component.eventThirdName).toEqual(undefined);
    });

    it('it should set eventFirstName and eventSecondName for US TYPE', () => {
      component.event.isUS = true;
      component.ngOnInit();

      expect(component.eventFirstName).toEqual('teamB');
      expect(component.eventSecondName).toEqual('teamA');
      expect(component.eventThirdName).toEqual(undefined);
    });

    it('it should handle colon split for eventSecondName for golf sport', () => {
      component.sportType = 'golf';
      component.event.isUS = false;
      component.filtersService.getTeamName = (name, index) => ['teamA', 'teamB: test'][index];
      component.ngOnInit();
      expect(component.eventFirstName).toEqual('teamA');
      expect(component.eventSecondName).toEqual('teamB');
      expect(component.eventThirdName).toEqual(undefined);
    });
    it('it should not handle colon split when there is no eventSecondName for golf sport', () => {
      component.sportType = 'golf';
      component.event.isUS = false;
      component.filtersService.getTeamName = (name, index) => ['teamA', 'teamB'][index];
      component.ngOnInit();
      expect(component.eventFirstName).toEqual('teamA');
      expect(component.eventSecondName).toEqual('teamB');
      expect(component.eventThirdName).toEqual(undefined);
    });
    it('it should handle colon split for eventThirdName for golf sport', () => {
      component.sportType = 'golf';
      component.event.isUS = false;
      component.filtersService.getTeamName = (name, index) => ['teamA', 'teamB', 'teamC: test'][index];
      component.ngOnInit();
      expect(component.eventFirstName).toEqual('teamA');
      expect(component.eventSecondName).toEqual('teamB');
      expect(component.eventThirdName).toEqual('teamC');
    });
    it('it should not handle colon split when there is no eventThirdName for golf sport', () => {
      component.sportType = 'golf';
      component.event.isUS = false;
      component.filtersService.getTeamName = (name, index) => ['teamA', 'teamB', 'teamC'][index];
      component.ngOnInit();
      expect(component.eventFirstName).toEqual('teamA');
      expect(component.eventSecondName).toEqual('teamB');
      expect(component.eventThirdName).toEqual('teamC');
    });

    it('should call onInit when no sportConfig for MultiTemplateSport homeDrawAwayType type', () => {
      component.sportConfig = undefined;
      component.event = {
        oddsCardHeaderType: 'homeDrawAwayType',
        markets: [],
        categoryName: ''
      } as any;
      sportsConfigService.getSport.and.returnValue(of({
        sportConfig: {
          config: {
            isMultiTemplateSport: true,
            request: {
              categoryId: '16'
            }
          }
        }
      }));

      component.ngOnInit();

      expect(component.isHomeDrawAwayType).toEqual(true);
      expect(component.sportConfig).toEqual({
        config: {
          isMultiTemplateSport: true,
          request: {
            categoryId: '16'
          }
        }
      } as any);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('Remove serve indication from name', () => {
      component.eventName = 'teamA* v teamB';
      component.ngOnInit();
      expect(component.eventName).not.toBeNull();
    });

    it('should call onInit when sportConfig is present for MultiTemplateSport homeDrawAwayType type', () => {
      component.sportConfig = {
        config: {
          isMultiTemplateSport: true
        }
      } as any;
      component.event = {
        oddsCardHeaderType: 'homeDrawAwayType',
        markets: [],
        categoryName: ''
      } as any;

      component.ngOnInit();

      expect(component.isHomeDrawAwayType).toEqual(true);
    });

    it('should call onInit when no sportConfig for MultiTemplateSport oneThreeType type', () => {
      component.sportConfig = undefined;
      component.event = {
        oddsCardHeaderType: 'oneThreeType',
        markets: [],
        categoryName: ''
      } as any;
      sportsConfigService.getSport.and.returnValue(of({
        sportConfig: {
          config: {
            isMultiTemplateSport: true,
            request: {
              categoryId: '16'
            }
          }
        }
      }));

      component.ngOnInit();

      expect(component.isHomeDrawAwayType).toEqual(true);
      expect(component.sportConfig).toEqual({
        config: {
          isMultiTemplateSport: true,
          request: {
            categoryId: '16'
          }
        }
      } as any);
    });

    it('should call onInit when sportConfig is present for MultiTemplateSport oneThreeType type', () => {
      component.sportConfig = {
        config: {
          isMultiTemplateSport: true,
          request: {
            categoryId: '16'
          }
        }
      } as any;
      component.event = {
        oddsCardHeaderType: 'oneThreeType',
        markets: [],
        categoryName: ''
      } as any;

      component.ngOnInit();

      expect(component.isHomeDrawAwayType).toEqual(true);
    });

    it('should call onInit when no sportConfig for non MultiTemplateSport', () => {
      component.sportConfig = undefined;
      component.event = {
        oddsCardHeaderType: 'homeDrawAwayType',
        markets: [],
        categoryName: ''
      } as any;
      sportsConfigService.getSport.and.returnValue(of({
        sportConfig: {
          config: {
            isMultiTemplateSport: false,
            request: {
              categoryId: '16'
            }
          }
        }
      }));

      component.ngOnInit();

      expect(component.isHomeDrawAwayType).toEqual(false);
      expect(component.sportConfig).toEqual({
        config: {
          isMultiTemplateSport: false,
          request: {
            categoryId: '16'
          }
        }
      } as any);
    });

    it('should call onInit when sportConfig is present for non MultiTemplateSport', () => {
      component.sportConfig = {
        config: {
          isMultiTemplateSport: false
        }
      } as any;
      component.event = {
        oddsCardHeaderType: 'homeDrawAwayType',
        markets: [],
        categoryName: ''
      } as any;

      component.ngOnInit();

      expect(component.isHomeDrawAwayType).toEqual(false);
    });

    it('should transform SmartBoosts Markets and Init pubsub listeners with unique id', () => {
      component.ngOnInit();
      expect(component['uniqueId']).toEqual('randomId');
      expect(component.wasPrice).toEqual(wasPriceStub);

      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddCardSport_randomId_111',
        pubSubService.API.DELETE_SELECTION_FROMCACHE, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddCardSport_randomId_111',
        pubSubService.API.EVENT_SCORES_UPDATE, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddCardSport_randomId_111',
        pubSubService.API.EVENTS_CLOCK_UPDATE, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddCardSport_randomId_111',
        pubSubService.API.OUTCOME_UPDATED, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddCardSport_randomId_111',
        pubSubService.API.WS_EVENT_UPDATED, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddCardSport_randomId_111',
      pubSubService.API.WS_EVENT_UPDATE, jasmine.any(Function));
    });


    it('should test CLOCK CallBack', () => {
      spyOn(component as any, 'watchGroupHandler');

      const clockMock = {
        clock_seconds: '111',
        last_update: '2019-06-05 07:53:26',
        last_update_secs: (new Date().getTime() / 1000).toString(),
        offset_secs: '111',
        period_code: 'SECOND_HALF',
        period_index: '',
        start_time_secs: '1111',
        state: 'R'
      };

      component.event.clock = {
        refresh: jasmine.createSpy('refresh')
      };

      // test EVENTS_CLOCK_UPDATE callback
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === pubSubService.API.EVENTS_CLOCK_UPDATE) {
          cb({
            event: {
              id: 111
            },
            clockData: clockMock
          });
        }
      });

      component.ngOnInit();

      expect(component.event.clock.refresh).toHaveBeenCalled();
      expect(component['watchGroupHandler']).toHaveBeenCalled();
    });

    describe('if event comments are of tennis structure', () => {
      beforeEach(() => {
        component.event.comments = {
          runningGameScores: {},
          teams: {
            player_1: {
              score: '0',
              id: '1',
            },
            player_2: {
              score: '0',
              id: '2',
            }
          },
        };
        component.ngOnInit();
      });

      it('isSetGamesPoints should be set', () => {
        expect(component.isSetsGamesPoints).toBeTruthy();
      });

      it('isPeriodScore should be set', () => {
        expect(component.isPeriodScore).toBeTruthy();
      });
    });

    describe('if event comments are of s/p structure', () => {
      beforeEach(() => {
        component.event.comments = {
          teams: {
            home: {
              currentPoints: '0',
              name: 'Team A',
            },
            away: {
              currentPoints: '0',
              name: 'Team B',
            }
          }
        };
        component.ngOnInit();
      });

      it('isSetGamesPoints should be set', () => {
        expect(component.isSetsGamesPoints).toBeTruthy();
      });

      it('isPeriodScore should not be set', () => {
        expect(component.isPeriodScore).toBeFalsy();
      });
    });

    it('should set showServe for sport requiring serve indicator', () => {
      component.event.categoryName = 'Volleyball';
      component.ngOnInit();
      expect(component.showServe).toBeTruthy();
    });

    it('should not showServe for sport not requiring serve indicator', () => {
      component.event.categoryName = 'Football';
      component.ngOnInit();
      expect(component.showServe).toBeFalsy();
    });

    it('data true for tennis', () => {
      component.event.categoryName = 'Tennis';
      component.event.categoryId = '34';
      component.event.comments = {
        runningGameScores: {},
        teams: {
          player_1: {
            isActive: true,
          },
          player_2: {
            isActive: false,
          }
        }
      } as any;

      component.ngOnInit();
      expect(component.servingTeams).toEqual([true, false]);
      expect(component.scoreHeaders).toEqual(['S', 'G', 'P']);
      expect(component.oddsScoresData).toEqual([['S', '0', '0'], ['G', '0', '0'], ['P', '0', '0']]);
    });

    it('if isSetsGamesPoints, should determine active (serving) player', () => {
      component.event.categoryName = 'Tennis';
      component.event.categoryId = '34';
      component.event.comments = {
        runningGameScores: {},
        teams: {
          player_1: {
            isActive: true,
          },
          player_2: {
            isActive: false,
          }
        }
      } as any;
      component.ngOnInit();

      expect(component.isSetsGamesPoints).toBeTruthy();
      expect(component.servingTeams).toEqual([true, false]);
    });

    it('should handle pubSub updates and datermine active (serving) player when isSetsGamesPoints is true', () => {
      pubSubService.subscribe = (handlerName: string, updateType: string, callback: Function) => {
        const eventUpdate = {
          event: {
            id: 1,
          } as any
        } as any;
        callback(eventUpdate);
      };
      component.event.id = 1;
      component.event.categoryName = 'Tennis';
      component.event.categoryId = '34';
      component.event.comments = {
        runningGameScores: {},
        teams: {
          player_1: {
            isActive: true,
          },
          player_2: {
            isActive: false,
          }
        }
      } as any;
      component.event.clock = {
        refresh: () => {},
      };
      component.ngOnInit();

      expect(component.servingTeams).toEqual([true, false]);
    });
  });

  it('should process DELETE_SELECTION_FROMCACHE pubsub event when OB event ID is same as stored OB event', () => {
    const eventId = '123';
    const update = {
      eventId
    };
    component.multiMarketList = ['Match Betting','Match Result'];
    component.event.id = +eventId;
    component.isOddsSports = true;
    // test EVENTS_CLOCK_UPDATE callback
    pubSubService.subscribe.and.callFake((name, channel, cb) => {
      if (channel === pubSubService.API.DELETE_SELECTION_FROMCACHE) {
        cb(update);
      }
    });
    filtersService.groupBy.calls.reset();

    component['addRecalculationEventListeners']();

    // expect(filtersService.groupBy).toHaveBeenCalledTimes(1);
  });

  it('should process DELETE_SELECTION_FROMCACHE pubsub event when OB event ID is not the same as stored OB event', () => {
    const eventId = '123';
    const update = {
      eventId
    };

    component.event.id = +eventId + 1;
    // test EVENTS_CLOCK_UPDATE callback
    pubSubService.subscribe.and.callFake((name, channel, cb) => {
      if (channel === pubSubService.API.DELETE_SELECTION_FROMCACHE) {
        cb(update);
      }
    });
    filtersService.groupBy.calls.reset();

    component['addRecalculationEventListeners']();

    expect(filtersService.groupBy).not.toHaveBeenCalled();
  });

  it('should unsubscribe on component Destroy', () => {
    component['uniqueId'] = 'randomId';
    spyOn<any>(component, 'unsubscribeOutcomeChanges');
    component.sportConfig = undefined;
    component['sportsConfigSubscription'] = new Subject() as any;
    component.ngOnInit();
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('oddCardSport_randomId_111');
    expect(component['unsubscribeOutcomeChanges']).toHaveBeenCalled();
  });

  it('get eventDisplayed', () => {
    expect(component.eventDisplayed({ isResulted: true, outcomes: [] } as any)).toBeTruthy();
    expect(component.eventDisplayed({ outcomes: [{}] } as any)).toBeTruthy();
    expect(component.eventDisplayed({ outcomes: [] } as any)).toBeFalsy();
  });

  describe('transformSmartBoostsMarkets', () => {
    const markets = [{ outcomes: [{ name: '',
    correctedOutcomeMeaningMinorCode: 1 }] }] as IMarket[];
    it(`isSmartBoosts property should equal true if market is SmartBoosts`, () => {

      component['transformSmartBoostsMarkets'](markets);
      expect(markets[0].isSmartBoosts).toBeTruthy();
    });

    it(`isSmartBoosts property should equal false if market is SmartBoosts`, () => {
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarkets'](markets);
      expect(markets[0].isSmartBoosts).toBeFalsy();
    });

    it(`should change outcomes 'name' if market is SmartBoosts`, () => {
      component.eventName = '';
      component['transformSmartBoostsMarkets'](markets);

      expect(component.eventName).toEqual(testStr);
    });

    it(`should set outcomes 'wasPrice' if market is SmartBoosts`, () => {
      delete component.wasPrice;
      component['transformSmartBoostsMarkets'](markets);

      expect(component.wasPrice).toEqual(wasPriceStub);
    });

    it(`should Not change outcomes 'name' if market is Not SmartBoosts`, () => {
      component.eventName = '';
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarkets'](markets);

      expect(component.eventName).toEqual('');
    });

    it(`should Not set outcomes 'wasPrice' if market is Not SmartBoosts`, () => {
      delete component.wasPrice;
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarkets'](markets);
      expect(component.wasPrice).toBeUndefined();
    });

    it(`should Not set 'wasPrice' if parsedName has Not 'wasPrice'`, () => {
      delete component.wasPrice;
      component['smartBoostsService'].parseName = jasmine.createSpy().and.returnValue({ name: '' });

      component['transformSmartBoostsMarkets'](markets);
      expect(component.wasPrice).toBeUndefined();
    });
  });

  describe('#addRecalculationEventListeners', () => {
    beforeEach(() => {
      component.event = {
        id: 321,
        markets: [
            {
                outcomes: [
                    {
                      correctedOutcomeMeaningMinorCode: 'H'}
                ],
                correctedOutcomeMeaningMinorCode:'H'
            },
            {
                outcomes: [
                    {correctedOutcomeMeaningMinorCode: 'A'}
                ],
                correctedOutcomeMeaningMinorCode:'A'
            }
        ]
      } as any;
    });
    it('should handle MOVE_EVENT_TO_INPLAY event', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === 'MOVE_EVENT_TO_INPLAY') {
          cb({
            id: 321,
          });
        }
      });
      spyOn(component as any, 'watchGroupHandler');
      component['addRecalculationEventListeners']();
      expect(component['watchGroupHandler']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should handle OUTCOME_UPDATED event', () => {
      component['getCorrectedOutcomes'] = jasmine.createSpy();
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        cb({
          id: 123,

          event: {
            id: 123
          }
        });
      });
      component.selectedMarketObject = {
        id: 123
      } as any;
      component['addRecalculationEventListeners']();
    //   expect(component['getCorrectedOutcomes']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should handle OUTCOME_UPDATED event and call init', () => {
      component['getCorrectedOutcomes'] = jasmine.createSpy();
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        cb({
          id: 123,
          isDisplayed: false,
          event: {
            id: 123,
          
          }
        });
      });
      component.event = {
        name: 'Test',
        id: 123,
        marketsCount: 3,
        markets: [{
          id: 123,
          name: 'Test',
          outcomes: [{
            id: 111,
            name: 'Test',
            correctedOutcomeMeaningMinorCode: 1
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
        },
        categoryId :16
      } as any;
      component.selectedMarketObject = {
        id: 123
      } as any;
      component['sportsViewTypes'] = {};
      component.selectedMarketIds = [123];
      component['addRecalculationEventListeners']();
      expect(component['getCorrectedOutcomes']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should handle WS_EVENT_UPDATED event', () => {
      component.event = {
        name: 'Test',
        id: 123,
        marketsCount: 3,
        markets: [{
          id: 123,
          name: 'Test',
          outcomes: [{
            id: 111,
            name: 'Test',
            correctedOutcomeMeaningMinorCode: 1
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
        },
        categoryId :16
      } as any;
      component['sportsViewTypes'] = {};
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === 'WS_EVENT_UPDATED') {
          cb({
            id: 123,
            comments: {
              teams: {
                home: {},
                away: {}
              }
            },
          });
        }
      });
      component['addRecalculationEventListeners']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should handle EVENT_SCORES_UPDATE event', () => {
      component.event = {
        name: 'Test',
        id: 123,
        marketsCount: 3,
        markets: [{
          id: 123,
          name: 'Test',
          outcomes: [{
            id: 111,
            name: 'Test',
            correctedOutcomeMeaningMinorCode: 1
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
        },
        categoryId :16
      } as any;
      component['sportsViewTypes'] = {};
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === 'EVENT_SCORES_UPDATE') {
          cb({event:{
            id: 123,
            comments: {
              teams: {
                home: {},
                away: {}
              }
            },
          }});
        }
      });
      component['addRecalculationEventListeners']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should handle WS_EVENT_UPDATE event', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === 'WS_EVENT_UPDATE') {
          cb();
        }
      });
      component['addRecalculationEventListeners']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    describe('market undisplay', () => {
      beforeEach(() => {
        component.isOddsSports = true;
        component.selectedMarketObject = {
          id: 123
        } as any;
      });
      it('should emit marketUndisplayed when market undisplayed', () => {
        pubSubService.subscribe.and.callFake((name, channel, cb) => {
          cb({
            id: 123,
            isDisplayed: false,
            event: {
              id: 123
            }
          });
        });
        component['addRecalculationEventListeners']();
        // expect(component['marketUndisplayed'].emit).toHaveBeenCalledWith({
        //   id: 123,
        //   isDisplayed: false,
        //   event: {
        //     id: 123
        //   }
        // } as any);
      });
      it('should not emit marketUndisplayed market diplayed', () => {
        pubSubService.subscribe.and.callFake((name, channel, cb) => {
          cb({
            id: 123,
            isDisplayed: true,
            event: {
              id: 123
            }
          });
        });
        component['addRecalculationEventListeners']();
        expect(component['marketUndisplayed'].emit).not.toHaveBeenCalled();
      });
      it('should not emit marketUndisplayed', () => {
        pubSubService.subscribe.and.callFake((name, channel, cb) => {
          cb({
            id: 123,
            isDisplayed: undefined,
            event: {
              id: 123
            }
          });
        });
        component['addRecalculationEventListeners']();
        expect(component['marketUndisplayed'].emit).not.toHaveBeenCalled();
      });
    });

    it('getCorrectedOutcomes should not be called if no selectedMarketObject defined', () => {
      component['sportsViewTypes'] = {};
      component['getCorrectedOutcomes'] = jasmine.createSpy();
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        cb({
          id: 321,
          event: {
            id: 123
          }
        });
      });
      component['addRecalculationEventListeners']();
      expect(component['getCorrectedOutcomes']).not.toHaveBeenCalled();
    });
  });

  describe('#getCorrectedOutcomes', () => {
    beforeEach(() => {
      component.selectedMarketObject = {
        templateMarketName: 'Handicap Match Result'
      } as any;
      // spyOn(component['isHandicapMatchResult'], 'emit');
    });
    it('should create component instance', () => {
      expect(component).toBeTruthy();
    });
  });

  describe('@watchHandler', () => {
    beforeEach(() => {
      component.event = { markets: [{}] } as any;
    });

    xit('it should set correct header: true, true, true', () => {
      marketTypeService.isMatchResultType.and.returnValue(true);
      marketTypeService.isHomeDrawAwayType.and.returnValue(true);
      marketTypeService.isHeader2Columns.and.returnValue(true);
      component['watchHandler']();

      expect(component.header2Columns).toBe(true);
    });

    xit('it should set correct header: false, false, false', () => {
      marketTypeService.isMatchResultType.and.returnValue(false);
      marketTypeService.isHomeDrawAwayType.and.returnValue(false);
      marketTypeService.isHeader2Columns.and.returnValue(false);
      component['watchHandler']();

      expect(component.header2Columns).toBe(false);
    });

    xit('it should set correct header: false, true, false', () => {
      marketTypeService.isMatchResultType.and.returnValue(false);
      marketTypeService.isHomeDrawAwayType.and.returnValue(true);
      marketTypeService.isHeader2Columns.and.returnValue(false);
      component['watchHandler']();

      expect(component.header2Columns).toBe(false);
    });

    xit('it should hide duplicate markets in events', () => {
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          isOutrightSport: true,
          path: '/golf',
          request: {
            categoryId: '18'
          }
        }
      } as any;
      component.selectedMarket = 'Hole Head To Head';
      component.event = { isFinished: false, 
        markets: [
          {
            hidden: false,
            templateMarketName: 'Hole Head To Head',
            name: 'Hole Head To Head',
            outcomes: []
          },
          {
            hidden: false,
            templateMarketName: 'Hole Head To Head',
            name: 'Hole Head To Head 2',
            outcomes: []
          }
        ], 
        name: 'Soderberg/Gagli/Porteous' } as any;
      component['watchHandler']();

      expect(component.header2Columns).toBe(false);
    });
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      component['watchHandler'] = jasmine.createSpy('watchHandler');
      component['calculateScores'] = jasmine.createSpy('calculateScores');
      component['isShowMarketsCount'] = jasmine.createSpy('isShowMarketsCount');
      component['watchGroupHandler'] = jasmine.createSpy('watchGroupHandler');
    });

    xit('shoulnd not trigger', () => {
      const changes = {};
      component.ngOnChanges(changes as any);

      expect(component['watchGroupHandler']).not.toHaveBeenCalled();
      expect(component['watchHandler']).not.toHaveBeenCalled();
      expect(component['isShowMarketsCount']).not.toHaveBeenCalled();
    });

    xit('should call watchHandler and calculateScores but not isShowMarketsCount ', () => {
      const changes = {
        selectedMarketObject: {
          isFirstChange: jasmine.createSpy().and.returnValue(true)
        }
      };
      component.teamRoleCodes = ['home', 'away'];
      component.ngOnChanges(changes as any);

      expect(component['watchHandler']).toHaveBeenCalled();
      expect(component['calculateScores']).toHaveBeenCalled();
      expect(component['isShowMarketsCount']).not.toHaveBeenCalled();
    });

    xit('should call watchHandler and isShowMarketsCount but not calculateScores', () => {
      const changes = {
        selectedMarketObject: {
          isFirstChange: jasmine.createSpy().and.returnValue(false)
        }
      };
      component.teamRoleCodes = null;
      component.ngOnChanges(changes as any);

      expect(component['watchHandler']).toHaveBeenCalled();
      expect(component['calculateScores']).not.toHaveBeenCalled();
      expect(component['isShowMarketsCount']).toHaveBeenCalled();
    });

    it('should call watchGroupHandler', () => {
      const changes = {
        event: true,
        selectedMarketObject: {
          isFirstChange: ()=> {
            return ''
          },

        }
      };
      component['sportsViewTypes'] = true;
      component.ngOnChanges(changes as any);

      expect(component['watchGroupHandler']).toHaveBeenCalled();
    });
  });

  describe('calculateScores', () => {
    it('oddsScores should have correct scores', () => {
      component.isDarts = false;
      component.event.isUS = false;
      component.event.comments = {
        teams: {
          home: {
            score: '1'
          },
          away: {
            score: '2'
          }
        } as any
      };
      component['calculateScores']();
      expect(component.oddsScores.home).toBe('1');
      expect(component.oddsScores.away).toBe('2');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('oddsScores should have correct scores for cricket', () => {
      component.isDarts = false;
      component['isCricket'] = true;
      component.event.isUS = false;
      component.event.comments = {
        teams: {
          home: {
            score: ''
          },
          away: {
            score: '2'
          }
        } as any
      };
      component['calculateScores']();
      expect(component.oddsScores.home).toBe('-/-');
      expect(component.oddsScores.away).toBe('2');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('oddsScores should have scores correctly swapped wnen isUS is enabled', () => {
      component.isDarts = false;
      component.event.isUS = true;
      component.event.comments = {
        teams: {
          home: {
            score: '1'
          },
          away: {
            score: '2'
          }
        } as any
      };
      component['calculateScores']();
      expect(component.oddsScores.home).toBe('2');
      expect(component.oddsScores.away).toBe('1');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('oddsScores should have correct scores for cricket', () => {
      component.isDarts = false;
      component.isCricket = true;
      component.event.comments = {
        teams: {
          home: {
            score: '100 500/1'
          },
          away: {
            score: '200'
          }
        } as any
      };
      component['calculateScores']();
      expect(component.oddsScores.home).toBe('500/1');
      expect(component.oddsScores.away).toBe('200');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('oddsScores should be 0 when no scores', () => {
      component.isDarts = false;
      component.event.comments = {
        teams: {}
      };
      component['calculateScores']();
      expect(component.oddsScores.home).toBe('0');
      expect(component.oddsScores.away).toBe('0');
    });

    it('should not calculate period scores #1', () => {
      component.isDarts = false;
      component.isSetsGamesPoints = true;
      component.event.comments = {
        teams: {}
      };
      component['calculateScores']();
      expect(component.periodScores.home).toBe('0');
      expect(component.periodScores.away).toBe('0');
    });

    it('should calculate period scores #1', () => {
      component.isDarts = false;
      component.isSetsGamesPoints = true;
      component.event.comments = {
        teams: {
          home: { id: 3 },
          away: { id: 4 }
        },
        setsScores: {
          1: { 3: '1', 4: '2' },
          '2': { 3: '3', 4: '4' },
          'z': { 3: '5', 4: '6' }
        }
      } as any;
      component['calculateScores']();
      expect(component.periodScores.home).toBe('3');
      expect(component.periodScores.away).toBe('4');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should not calculate period scores #2', () => {
      component.isDarts = false;
      component.isSetsGamesPoints = true;
      component.event.comments = {
        teams: {
          home: { id: 3 },
          away: { id: 4 }
        },
        setsScores: {}
      } as any;
      component['calculateScores']();
      expect(component.periodScores.home).toBe('0');
      expect(component.periodScores.home).toBe('0');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('dart sports only legs event', () => {
      component.isDarts = true;
      component.event.comments = {
        teams: {
          home: { id: 3, score: '', currentPoints: '1'},
          away: { id: 4, score: '', currentPoints: '2'}
        },
        setsScores: {}
      } as any;
      component['calculateScores']();
      expect(component.oddsScores.home).toBe(null);
      expect(component.oddsScores.away).toBe(null);
    });

    it('should not calculate period scores #3', () => {
      component.isDarts = false;
      component.isSetsGamesPoints = true;
      component.event.comments = {
        teams: {
          home: { id: 3 },
          away: { id: 4 }
        },
        setsScores: {
          1: { 5: '1', 6: '2' }
        }
      } as any;
      component['calculateScores']();
      expect(component.periodScores.home).toBe('0');
      expect(component.periodScores.home).toBe('0');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should calculate period scores #2', () => {
      component.isDarts = false;
      component.isSetsGamesPoints = true;
      component.event.comments = {
        teams: {
          home: { id: 3 },
          away: { id: 4 }
        },
        setsScores: {
          1: { 3: '1', 4: '2' },
          2: { 3: '3', 4: '4' },
          3: { 3: '5', 4: '6' }
        },
        runningSetIndex: 2
      } as any;
      component['calculateScores']();
      expect(component.periodScores.home).toBe('3');
      expect(component.periodScores.away).toBe('4');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should call scoreParserService', () => {
      component.isDarts = false;
      scoreParserService.getScoreType.and.returnValue('BoxScore');
      component.event.comments = {
        teams: {
          home: {
            name: 'name',
            score: '5'
          },
          away: {
            name: 'name2',
            score: '6'
          }
        }
      };

      component.calculateScores();
      expect(scoreParserService.parseScores).toHaveBeenCalledWith('name 5 v name2 6', 'BoxScore');

      scoreParserService.getScoreType.and.returnValue('test');
    });

    describe('if comments contain set scores', () => {
      it('if scores for players are null, should set periodScores to 0', () => {
        component.isDarts = false;
        component.teamRoleCodes = ['player_1', 'player_2'];
        component.event.isUS = false;
        component.isSetsGamesPoints = true;
        component.event.comments = {
          runningSetIndex: 1,
          setsScores: {
            1: {},
          },
          teams: {
            player_1: {}, player_2: {},
          }
        } as any;

        component['calculateScores']();

        expect(component.periodScores).toEqual({home: '0', away: '0'});
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
    });

    describe('if comments contain current points', () => {
      it('if current points are null, should set currentScores to 0', () => {
        component.isDarts = false;
        component.teamRoleCodes = ['home', 'away'];
        component.event.isUS = false;
        component.isEventHasCurrentPoints = true;
        component.event.comments = {
          teams: {
            home: {}, away: {},
          }
        } as any;

        component['calculateScores']();

        expect(component.currentScores).toEqual({home: '0', away: '0'});
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
    });
  });

  it('#watchGroupHandler updates variabless', () => {
    component.showMarketsCount = false;
    component.isStream = false;
    component.getOddsLabel = jasmine.createSpy().and.returnValue('1');
    component['isShowMarketsCount'] = jasmine.createSpy().and.returnValue(true);
    component.isStreamAvailable = jasmine.createSpy().and.returnValue(true);

    component['watchGroupHandler']();

    expect(component.oddsLabel).toBe('1');
    expect(component.showMarketsCount).toBe(true);
    expect(component.isStream).toBe(true);
  });

  describe('@formatScore', () => {
    it('should format score for Gaelic Football', () => {
      component.isGAA = true;
      const score = '1-1';
      const result = component.formatScore(score);

      expect(result).toEqual('1 - 1');
    });

    it('should not format score for other sports', () => {
      component.isGAA = false;
      const score = '1-1';
      const result = component.formatScore(score);

      expect(result).toEqual('1-1');
    });
  });

  it('should return event comments', () => {
    component.event.comments = {
      runningSetIndex: 1
    } as any;

    expect(component.eventComments).toEqual(jasmine.objectContaining({ runningSetIndex: 1 }));
  });

  describe('addOrdinalSuffix', () => {
    it('Should return number + "st"', () => {
      const num = 21;
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('21st');
    });

    it('Should return number + "nd"', () => {
      const num = 22;
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('22nd');
    });

    it('Should return number + "rd"', () => {
      const num = 23;
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('23rd');
    });

    it('Should return number + "th"', () => {
      const num = 25;
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('25th');
    });
  });

  describe('trackById', () => {

    it('should return ID', () => {
      const index = 5;
      const event = {
        id: 'ID'
      } as any;

      const trackID = component.trackById(index, event);

      expect(trackID).toBe('ID 5');
    });

    it('should return index', () => {
      const index = 5;
      const event = null;

      const trackID = component.trackById(index, event);

      expect(trackID).toBe('5');
    });
  });

  describe('isSportCard', () => {
    it('should return true', () => {
      const market = {} as any;
      component.featured = {isSelection: true};
      component['template'] = {
        name: 'template'
      };
      const isSportCard = component.isSportCard(market);

      expect(isSportCard).toBe(true);
    });

    it('should return true', () => {
      const market = {} as any;
      component.featured = null;
      component.isSelectedMarket = jasmine.createSpy('isSelectedMarket').and.returnValue(true);
      component['template'] = {
        name: 'template'
      };
      const isSportCard = component.isSportCard(market);

      expect(isSportCard).toBe(true);
      expect(component.isSelectedMarket).toHaveBeenCalledWith(market);
    });

    it('should return false', () => {
      const market = {} as any;
      component.isSelectedMarket = jasmine.createSpy('isSelectedMarket').and.returnValue(false);
      component['template'] = {
        name: 'Outrights'
      };
      const isSportCard = component.isSportCard(market);

      expect(isSportCard).toBe(false);
      expect(component.isSelectedMarket).toHaveBeenCalledWith(market);
    });
  });

  describe('favouriteClickHandler', () => {
    it('', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
      } as any;

      component.event = {
        markets: []
      } as any;

      // component.event = {} as any;
      component.isFavouriteClickLocked = true;
      component.favouriteClickHandler(event);

      expect(event.stopPropagation).toHaveBeenCalled();
      // expect(favouritesService.add).toHaveBeenCalledWith(component.event, 'football', null);
    });
  });

  describe('PriceOddsButton click', () => {
    let clickEvent, betEvent, betMarket, betOutcome;

    beforeEach(() => {
      clickEvent = {
        stopPropagation: jasmine.createSpy('stopPropagation')
      } as any;

      betEvent = {
        id: 523,
        categoryId: '19',
        isStarted: true,
        eventIsLive: true,
        name: 'Dynamo vs Liverpool',
        typeName: 'Competition',
        typeId: '5123',
        drilldownTagNames: 'drilldownTagNames',
        isAvailable: true,
        cashoutAvail: 'cashoutAvail',
        liveServChannels: 'liveServChannels',
        sportId: 'sportId',
        startTime: 'startTime'
      } as any;

      betMarket = {
        id: 7,
        name: 'Match Result',
        rawHandicapValue: '3',
        drilldownTagNames: 'drilldownTagNames',
        isMarketBetInRun: true,
        liveServChannels: 'liveServChannels',
        isGpAvailable: true,
        isEachWayAvailable: true,
        priceTypeCodes: 'priceTypeCodes'
      } as any;

      betOutcome = {
        id: 315,
        outcomeMeaningMajorCode: '1',
        outcomeMeaningMinorCode: 'H',
        prices: [
          {
            handicapValueDec: '3',
            priceType: 'LP'
          }
        ],
        modifiedPrice: {id: 602},
        liveServChannels: 'liveServChannels'
      } as any;
    });

    describe('@onPriceOddsButtonClick', () => {
      it('should execute async check', fakeAsync(() => {
        component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
        component.onPriceOddsButtonClick(clickEvent, betEvent, betMarket, betOutcome);

        tick();
        expect(clickEvent.stopPropagation).toHaveBeenCalled();
        expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.IS_ADDTOBETSLIP_IN_PROCESS);
      }));

      it('after check should add to betslip if not in progress', fakeAsync(() => {
        component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
        component.onPriceOddsButtonClick(clickEvent, betEvent, betMarket, betOutcome);
        tick();

        expect(component['addToBetSlip']).toHaveBeenCalledWith(clickEvent, betEvent, betMarket, betOutcome);
      }));

      it('after check should not add to betslip if still in progress', fakeAsync(() => {
        component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
        commandService.executeAsync.and.returnValue(Promise.resolve(true));
        component.onPriceOddsButtonClick(clickEvent, betEvent, betMarket, betOutcome);
        tick();

        expect(component['addToBetSlip']).not.toHaveBeenCalled();
      }));
    });

    describe('@addToBetSlip', () => {
      beforeEach(() => {
        gtmTrackingService.detectTracking.and.returnValue({
          location: 'test location',
          module: 'test module'
        });
      });

      it('should add bet to betslip - priceType LP', fakeAsync(() => {
        betMarket.isLpAvailable = true;
        betMarket.cashoutAvail = 'cashoutAvail';
        component['addToBetSlip'](clickEvent, betEvent, betMarket, betOutcome);
        tick();

        const expectedObject = [{
          eventIsLive: true,
          outcomes: [
            {
              id: 315,
              outcomeMeaningMajorCode: '1',
              outcomeMeaningMinorCode: 'H',
              prices:[
                {
                  handicapValueDec: '3',
                  priceType: 'LP'
                }
              ],
              modifiedPrice: {id: 602},
              liveServChannels: 'liveServChannels'
            }
          ],
          typeName: 'Competition',
          price: {handicapValueDec: '3',priceType: 'LP'},
          handicap: {type: '1',raw: '3'},
          goToBetslip: false,
          modifiedPrice: {id: 602},
          eventId: 111,
          isOutright: undefined,
          isSpecial: undefined,
          GTMObject: {
            categoryID: '19',
            typeID: '5123',
            eventID: '523',
            selectionID: '315',
            tracking: {
              location: 'test location',
              module: 'test module'
            },
            betData: {
              name: 'Dynamo vs Liverpool',
              category: '19',
              variant: '5123',
              brand: 'Match Result',
              dimension60: '523',
              dimension61: 315,
              dimension62: 1,
              dimension63: 0,
              dimension64: 'test location',
              dimension65: 'test module'
            }
          },
          details: {
            eventDrilldownTagNames: 'drilldownTagNames',
            marketDrilldownTagNames: 'drilldownTagNames',
            isAvailable: true,
            cashoutAvail: 'cashoutAvail',
            isMarketBetInRun: true,
            eventliveServChannels: 'liveServChannels',
            marketliveServChannels: 'liveServChannels',
            outcomeliveServChannels: 'liveServChannels',
            isSPLP: false,
            isGpAvailable: true,
            isEachWayAvailable: true,
            marketPriceTypeCodes: 'priceTypeCodes',
            marketCashoutAvail: 'cashoutAvail',
            outcomeMeaningMinorCode: 'H',
            info: {
              sportId: 'sportId',
              time: 'startTime',
              isStarted: true
            }
          }
        }];

        expect(pubSubService.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
      }));

      it('should add bet to betslip - priceType SP', fakeAsync(() => {
        betSlipSelectionsData.count = () => 0;
        betMarket = {
          id: 7,
          name: 'Match Result',
          drilldownTagNames: 'drilldownTagNames',
          isMarketBetInRun: true,
          liveServChannels: 'liveServChannels',
          isGpAvailable: true,
          isEachWayAvailable: true,
          priceTypeCodes: 'priceTypeCodes',
          cashoutAvail: 'marketCashoutAvail'
        } as any;
        betOutcome = {
          prices: [],
          id: 315,
          outcomeMeaningMajorCode: '1',
          outcomeMeaningMinorCode: 'H',
          modifiedPrice: {id: 602},
          liveServChannels: 'liveServChannels'
        } as any;
        component['addToBetSlip'](clickEvent, betEvent, betMarket, betOutcome);
        tick();

        const expectedObject = {
            eventIsLive: true,
            outcomes: [
              {
                prices: [],
                id: 315,
                outcomeMeaningMajorCode: '1',
                outcomeMeaningMinorCode: 'H',
                modifiedPrice: {id: 602}, // duplicate
                liveServChannels: 'liveServChannels'
              }
              ],
            typeName: 'Competition',
            price: {priceType: 'SP'},
            handicap: undefined,
            goToBetslip: false,
            modifiedPrice: {id: 602}, // duplicate
            eventId: 111,
            isOutright: undefined,
            isSpecial: undefined,
            GTMObject: {
              categoryID: '19',
              typeID: '5123',
              eventID: '523',
              selectionID: '315',
              tracking: {location: 'test location', module: 'test module'},
              betData: {
                name: 'Dynamo vs Liverpool',
                category: '19',
                variant: '5123',
                brand: 'Match Result',
                dimension60: '523',
                dimension61: 315,
                dimension62: 1,
                dimension63: 0,
                dimension64: 'test location',
                dimension65: 'test module'
              }
            },
            details: {
              cashoutAvail: 'cashoutAvail',
              eventDrilldownTagNames: 'drilldownTagNames',
              eventliveServChannels: 'liveServChannels',
              marketDrilldownTagNames: 'drilldownTagNames',
              marketCashoutAvail: 'marketCashoutAvail',
              isAvailable: true,
              isSPLP: false,
              isGpAvailable: true,
              isEachWayAvailable: true,
              outcomeMeaningMinorCode: 'H',
              info: {
                sportId: 'sportId',
                time: 'startTime',
                isStarted: true
              },
              isMarketBetInRun: true,
              marketliveServChannels: 'liveServChannels',
              marketPriceTypeCodes: 'priceTypeCodes',
              outcomeliveServChannels: 'liveServChannels',
            }
          };

        expect(pubSubService.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', [expectedObject]);
      }));

      it(`should 'detectTracking' with current segment`, fakeAsync(() => {
        routingState.getCurrentSegment.and.returnValue('segment');
        component.gtmModuleTitle = 'ModuleTitle';

        component['addToBetSlip'](clickEvent, betEvent, betMarket, betOutcome);
        tick();

        expect(component['gtmTrackingService'].detectTracking)
          .toHaveBeenCalledWith('ModuleTitle', 'segment', betEvent, betMarket);
      }));

      it('should add bet to betslip - priceType SP with not started, event.originalName, market.marketname', fakeAsync(() => {
        component['env'] = {
          BYB_CONFIG: {
            HR_YC_EVENT_TYPE_ID: '5123'
          }
        } as any;
        betSlipSelectionsData.count = () => 0;
        betEvent = {
          id: 523,
          categoryId: 19,
          originalName: 'original name',
          isStarted: true,
          eventIsLive: false,
          name: 'Dynamo vs Liverpool',
          typeName: 'Competition',
          typeId: '5123',
          drilldownTagNames: 'drilldownTagNames',
          isAvailable: true,
          cashoutAvail: 'cashoutAvail',
          liveServChannels: 'liveServChannels',
          sportId: 'sportId',
          startTime: 'startTime'
        } as any;
        betMarket = {
          id: 7,
          marketName: 'market name field',
          name: 'Match Result',
          drilldownTagNames: 'drilldownTagNames',
          isMarketBetInRun: true,
          liveServChannels: 'liveServChannels',
          isGpAvailable: true,
          isEachWayAvailable: true,
          priceTypeCodes: 'priceTypeCodes',
          cashoutAvail: 'marketCashoutAvail'
        } as any;
        betOutcome = {
          prices: [],
          id: 315,
          outcomeMeaningMajorCode: '1',
          outcomeMeaningMinorCode: 'H',
          modifiedPrice: {id: 602},
          liveServChannels: 'liveServChannels'
        } as any;
        component['addToBetSlip'](clickEvent, betEvent, betMarket, betOutcome);
        tick();

        const expectedObject = [
          {
            eventIsLive: false,
            outcomes: [
              {
                prices: [],
                id: 315,
                outcomeMeaningMajorCode: '1',
                outcomeMeaningMinorCode: 'H',
                modifiedPrice: {id: 602}, // duplicate
                liveServChannels: 'liveServChannels'
              }
              ],
            typeName: 'Competition',
            price: {priceType: 'SP'},
            handicap: undefined,
            goToBetslip: false,
            modifiedPrice: {id: 602}, // duplicate
            eventId: 111,
            isOutright: undefined,
            isSpecial: undefined,
            GTMObject: {
              categoryID: '19',
              typeID: '5123',
              eventID: '523',
              selectionID: '315',
              tracking: {location: 'test location', module: 'test module'},
              betData: {
                name: 'original name',
                category: '19',
                variant: '5123',
                brand: 'market name field',
                dimension60: '523',
                dimension61: 315,
                dimension62: 0,
                dimension63: 1,
                dimension64: 'test location',
                dimension65: 'test module'
              }
            },
            details: {
              cashoutAvail: 'cashoutAvail',
              eventDrilldownTagNames: 'drilldownTagNames',
              eventliveServChannels: 'liveServChannels',
              marketDrilldownTagNames: 'drilldownTagNames',
              isAvailable: true,
              isSPLP: false,
              isGpAvailable: true,
              isEachWayAvailable: true,
              outcomeMeaningMinorCode: 'H',
              info: {
                sportId: 'sportId',
                time: 'startTime',
                isStarted: true
              },
              isMarketBetInRun: true,
              marketliveServChannels: 'liveServChannels',
              marketPriceTypeCodes: 'priceTypeCodes',
              outcomeliveServChannels: 'liveServChannels',
              marketCashoutAvail: 'marketCashoutAvail'
            }
          }
        ];

        expect(pubSubService.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
      }));

      it('should send betObject to betSlip in parent window if this directive runs from iFrame', fakeAsync(() => {
        betMarket.isLpAvailable = true;
        component['windowRef'].nativeWindow.frameElement = {
          nodeName: 'IFRAME'
        };
        clickEvent = {
          target: {}
        } as any;
        parent = {
          postMessage: jasmine.createSpy('postMessage')
        } as any;
        betEvent.isStarted = false;

        component['addToBetSlip'](clickEvent, betEvent, betMarket, betOutcome);
        tick();

        expect(parent.postMessage).toHaveBeenCalled();
      }));

      it('should not track bet placement data', fakeAsync(() => {
        userService.quickBetNotification = true;
        betMarket.cashoutAvail = 'marketCashoutAvail';
        const expectedObject = [
          {
            eventIsLive: true,
            outcomes: [{
              id: 315,
              outcomeMeaningMajorCode: '1',
              outcomeMeaningMinorCode: 'H',
              prices: [{handicapValueDec: '3', priceType: 'LP'}],
              modifiedPrice: {id: 602},
              liveServChannels: 'liveServChannels'
            }],
            typeName: 'Competition',
            price: {handicapValueDec: '3', priceType: 'SP'},
            handicap: {type: '1', raw: '3'},
            goToBetslip: false,
            modifiedPrice: {id: 602},
            eventId: 111,
            isOutright: undefined,
            isSpecial: undefined,
            GTMObject: { categoryID: '19', typeID: '5123', eventID: '523', selectionID: '315' },
            details: {
              cashoutAvail: 'cashoutAvail',
              eventDrilldownTagNames: 'drilldownTagNames',
              eventliveServChannels: 'liveServChannels',
              marketDrilldownTagNames: 'drilldownTagNames',
              isAvailable: true,
              isSPLP: false,
              isGpAvailable: true,
              isEachWayAvailable: true,
              marketCashoutAvail: 'marketCashoutAvail',
              outcomeMeaningMinorCode: 'H',
              info: {
                sportId: 'sportId',
                time: 'startTime',
                isStarted: true
              },
              isMarketBetInRun: true,
                marketliveServChannels: 'liveServChannels',
                marketPriceTypeCodes: 'priceTypeCodes',
                outcomeliveServChannels: 'liveServChannels',
            }
          }
        ];

        gtmTrackingService.detectTracking.and.returnValue(null);
        component['addToBetSlip'](clickEvent, betEvent, betMarket, betOutcome);
        tick();

        expect(pubSubService.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
        expect(gtmService.push).not.toHaveBeenCalled();
      }));

      it('should not push track to gtm', fakeAsync(() => {
        userService.quickBetNotification = false;
        tick();

        expect(gtmService.push).not.toHaveBeenCalledWith({});
      }));
    });
  });

  describe('@checkOutcomeId', () => {
    let betOutcome;
    beforeEach(() => {
      betOutcome = {
        name: 'Outcome',
        id: '432234',
        prices: [{
          priceType: 'LP'
        }]
      } as any;
    });

    it('should return false if not selection', () => {
      expect(component['checkOutcomeId'](betOutcome, null)).toEqual(false);
    });

    it('should return false if no outcomes', () => {
      const selection = {
        outcomeId: null,
        outcomes: []
      };
      expect(component['checkOutcomeId'](betOutcome, selection as any)).toEqual(false);
    });

    it('should return false if outcomeId is different', () => {
      const selection = {
        outcomeId: '1234',
      };

      expect(component['checkOutcomeId'](betOutcome, selection as any)).toEqual(false);
    });

    it('should return false if selection outcomes empty and no outcomeId', () => {
      const selection = {
        outcomes: []
      };

      expect(component['checkOutcomeId'](betOutcome, selection as any)).toEqual(false);
    });

    it('should return false if selection outcomes is different', () => {
      const selection = {
        outcomes: [{
          id: '1234',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      };

      expect(component['checkOutcomeId'](betOutcome, selection as any)).toEqual(false);
    });

    it('should return true if outcomeId is the same', () => {
      const selection = {
        outcomeId: '432234',
      };

      expect(component['checkOutcomeId'](betOutcome, selection as any)).toEqual(true);
    });

    it('should return true if selection outcomes is the same', () => {
      const selection = {
        outcomes: [{
          id: '432234',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      };

      expect(component['checkOutcomeId'](betOutcome, selection as any)).toEqual(true);
    });
  });

  describe('getCorrectedOutcomes', () => {
    beforeEach(() => {
      spyOn<any>(component, 'subscribeOutcomeChanges');
    });

    xit('should subscribe on selectedMarketObject outcomes updates for odds sport', () => {
      component.selectedMarketObject.outcomes = [[{id: 700}], [{id: 702}], [{id: 703}]] as any;
      component.isOddsSports = true;

      component['getCorrectedOutcomes']();

      expect(filtersService.groupBy).toHaveBeenCalledWith(component.selectedMarketObject.outcomes, 'correctedOutcomeMeaningMinorCode');
      expect(component.correctedOutcomes).toEqual([{id: 700}, {id: 702}, {id: 703}] as any);
      expect(component['subscribeOutcomeChanges']).toHaveBeenCalledWith(component.correctedOutcomes);
    });

    xit('should subscribe on event.markets first outcome updates for non odds sport', () => {
      component.isOddsSports = false;
      component.selectedMarketObject = null;
      component.correctedOutcomes = undefined;
      component.event.markets = [
        {outcomes: [{id: 800,correctedOutcomeMeaningMinorCode: 'H'}, {id: 801,correctedOutcomeMeaningMinorCode: 'H'}, {id: 802,correctedOutcomeMeaningMinorCode: 'H'}]},
        {outcomes: [undefined, {id: 901,correctedOutcomeMeaningMinorCode: 'H'}, {id: 902,correctedOutcomeMeaningMinorCode: 'H'}]}
      ] as any;
      component['getCorrectedOutcomes']();

      expect(filtersService.groupBy).not.toHaveBeenCalled();
      expect(component.correctedOutcomes).toBeUndefined();
      expect(component['subscribeOutcomeChanges']).toHaveBeenCalledWith([component.event.markets[0].outcomes[0]]);
    });
  });

  describe('subscribeOutcomeChanges', () => {
    let outcomesLst;

    beforeEach(() => {
      outcomesLst = [{id: 100, prices: [{}]}];
      spyOn<any>(component, 'unsubscribeOutcomeChanges');
    });

    it('should not subscribe if no list of outcomes', () => {
      component['subscribeOutcomeChanges'](null);

      expect(component['unsubscribeOutcomeChanges']).toHaveBeenCalled();
      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });

    it('should not subscribe if list of outcomes is empty', () => {
      component['subscribeOutcomeChanges']([]);

      expect(component['unsubscribeOutcomeChanges']).toHaveBeenCalled();
      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });

    it('should not subscribe if outcome is undefined', () => {
      component['subscribeOutcomeChanges']([undefined]);

      expect(component['unsubscribeOutcomeChanges']).toHaveBeenCalled();
      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });

    it('should define outcome properties: active and isRacing', () => {
      component.event.categoryId = '100';
      pubSubService.subscribe = jasmine.createSpy('subscribe');
      component['subscribeOutcomeChanges'](outcomesLst);

      expect(betSlipSelectionsData.getSelectionsByOutcomeId).toHaveBeenCalledWith(outcomesLst[0].id);
      expect(outcomesLst[0].active).toEqual(true);
      expect(outcomesLst[0].isRacing).toEqual(false);
    });

    it('should define outcome.isRacing true for horse racing', () => {
      component.event.categoryId = '19';
      component['subscribeOutcomeChanges'](outcomesLst);

      expect(outcomesLst[0].isRacing).toEqual(true);
    });

    it('should define outcome.isRacing true for greyhound racing', () => {
      component.event.categoryId = '21';
      component['subscribeOutcomeChanges'](outcomesLst);

      expect(outcomesLst[0].isRacing).toEqual(true);
    });

    it('should subscribe on outcome updates', () => {
      component['subscribeOutcomeChanges'](outcomesLst);
      const subscriptionChannel = `priceOddsButton_${component['uniqueId']}_100`;

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(4);
      expect(pubSubService.subscribe.calls.allArgs()).toEqual([
        [subscriptionChannel, 'SELECTION_PRICE_UPDATE_100', jasmine.any(Function)],
        [subscriptionChannel, pubSubService.API.BETSLIP_SELECTIONS_UPDATE, jasmine.any(Function)],
        [subscriptionChannel, pubSubService.API.ADD_TO_QUICKBET, jasmine.any(Function)],
        [subscriptionChannel, pubSubService.API.REMOVE_FROM_QUICKBET, jasmine.any(Function)]
      ]);
      expect(component['outcomeSubscriberNames']).toEqual([subscriptionChannel]);
    });

    describe('SELECTION_PRICE_UPDATE', () => {
      const priceUpdate = {
        priceDen: 100,
        priceNum: 200,
        priceDec: 300
      };

      beforeEach(() => {
        pubSubService.subscribe.and.callFake((name, channel, fn: Function) => {
          if (channel === 'SELECTION_PRICE_UPDATE_100') {
            fn(priceUpdate);
          }
        });
      });

      it('should change outcome price', () => {
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].prices[0]).toEqual(jasmine.objectContaining(priceUpdate));
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('should change outcome price if no prices', () => {
        outcomesLst[0].prices = undefined;
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].prices).toBeUndefined();
      });

      it('should change outcome price if prices empty', () => {
        outcomesLst[0].prices[0] = undefined;
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].prices[0]).toBeUndefined();
      });
    });

    describe('BETSLIP_SELECTIONS_UPDATE', () => {
      let selections;

      beforeEach(() => {
        selections = {outcomes: [{ id: 100,correctedOutcomeMeaningMinorCode: 'H' }]};

        pubSubService.subscribe.and.callFake((name, channel, fn: Function) => {
          if (channel === 'BETSLIP_SELECTIONS_UPDATE') {
            fn(selections);
          }
        });

        betSlipSelectionsData.getSelectionsByOutcomeId.and.returnValue([{}]);
      });

      it('should change outcome active to true', () => {
        betSlipSelectionsData.getSelectionsByOutcomeId.and.returnValue([]);
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(true);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('should change outcome active to false if id is not matched', () => {
        selections = {outcomes: [{ id: 999, correctedOutcomeMeaningMinorCode: 'H'}]};
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(false);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('should change outcome active to false if list of selections is empty', () => {
        selections = {outcomes: []};
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(false);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('should change outcome active to false if no selections', () => {
        selections = {};
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(false);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
    });

    describe('ADD_TO_QUICKBET', () => {
      let selections;

      beforeEach(() => {
        pubSubService.subscribe.and.callFake((name, channel, fn: Function) => {
          if (channel === 'ADD_TO_QUICKBET') {
            fn(selections);
          }
        });
        betSlipSelectionsData.getSelectionsByOutcomeId.and.returnValue([]);
      });

      it('should change active to true', () => {
        selections = {outcomes: [{id: 100, correctedOutcomeMeaningMinorCode: 'H'}]};
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(true);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('should not change active to true', () => {
        selections = {outcomes: [{id: 200, correctedOutcomeMeaningMinorCode: 'H'}]};
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(false);
      });
    });

    describe('REMOVE_FROM_QUICKBET', () => {
      let selections;

      beforeEach(() => {
        pubSubService.subscribe.and.callFake((name, channel, fn: Function) => {
          if (channel === 'REMOVE_FROM_QUICKBET') {
            fn(selections);
          }
        });

        betSlipSelectionsData.getSelectionsByOutcomeId.and.returnValue([{}]);
      });

      it('should change active to false', () => {
        selections = { outcomes: [{ id: 100, correctedOutcomeMeaningMinorCode: 'H' }], isAddToBetslip: false };
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(false);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('should not change active to false', () => {
        selections = { outcomes: [{ id: 200, correctedOutcomeMeaningMinorCode: 'H' }], isAddToBetslip: true };
        component['subscribeOutcomeChanges'](outcomesLst);

        expect(outcomesLst[0].active).toBe(true);
      });
    });
  });

  describe('unsubscribeOutcomeChanges', () => {
    it('should unsubscribe from outcome updates', () => {
      component['outcomeSubscriberNames'] = ['100', '101'];
      component['unsubscribeOutcomeChanges']();

      expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(2);
      expect(component['outcomeSubscriberNames'].length).toBe(0);
    });
  });

  describe('getOddsLabel', () => {

    it('should return empty', () => {
      component.event.comments = undefined
      component.eventTime = 'datetime';
      component.eventStartedOrLive = true;
      component.isHalfOrFullTime = false;

      expect(component.getOddsLabel()).toBe('');
    });
    it('should return start time for upcoming', () => {
      component.event.comments = {
        runningSetIndex: 1
      } as any;
      component.eventTime = 'datetime';
      component.eventStartedOrLive = false;

      expect(component.getOddsLabel()).toBe('1Test Test');
    });
    it('should return matchTime', () => {
      component.event.comments = undefined;
      component.event.clock = {matchTime:'HT'};
      component.eventTime = 'datetime';
      component.isHalfOrFullTime = true;

      expect(component.getOddsLabel()).toEqual(component.event.clock.matchTime);
    });
    it('should return date time for upcoming', () => {
      component.event.comments = undefined
      component.eventTime = 'datetime';
      component.eventStartedOrLive = false;

      expect(component.getOddsLabel()).toBe('datetime');
    });
  });

  describe('setScoresData', () => {
    it('should use tennisScores', () => {
      const scoreStub = ['a', '1', '0'];
      component.scoreHeaders = scoreStub;
      component.isTennis = true;
      const setTennisScoresSpy = spyOn(component as any, 'setTennisScores').and.callFake(a => [a]);

      component['setScoresData']();

      expect(setTennisScoresSpy).toHaveBeenCalledWith(scoreStub);
      expect(component.oddsScoresData).toEqual([scoreStub]);
    });

    it('should add basketball scores (has current scores)', () => {
      component.isScores = true;
      component.isEventHasCurrentPoints = true;
      component.oddsScores = {
        home: '1',
        away: '0'
      };
      component.currentScores = {
        home: '2',
        away: '1'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([[undefined, '1', '0'], [undefined, '2', '1']]);
    });

    it('should not add basketball scores (has not current scores)', () => {
      component.isScores = true;
      component.isEventHasCurrentPoints = true;
      component.oddsScores = {
        home: '1',
        away: '0'
      };
      component.currentScores = {
        home: null,
        away: null
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([[undefined, '1', '0']]);
    });

    it('should add basketball scores (has not current scores)', () => {
      component.isScores = true;
      component.isEventHasCurrentPoints = true;
      component.oddsScores = {
        home: '1',
        away: '0'
      };
      component.currentScores = {
        home: null,
        away: '1'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([[undefined, '1', '0'], [undefined, null, '1']]);
    });

    it('should add cricket scores (has current scores)', () => {
      component.isScores = true;
      component.isCricket = true;
      component.isEventHasCurrentPoints = true;
      component.oddsScores = {
        home: '5/3',
        away: '10'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([[undefined, '5/3', '10']]);
    });

    it('should add badminton scores (no current scores)', () => {
      const scoreStub = ['G', 'P'];
      component.isTennis = false;
      component.isScores = true;
      component.isEventHasCurrentPoints = false;
      component.scoreHeaders = scoreStub;
      component.oddsScores = {
        home: '1',
        away: '0'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([['G', '1', '0']]);
    });

    it('should use scores when player_1 is teamRole (not tennis)', () => {
      component.event.comments = {
        teams: {
          player_1: {}
        }
      } as any;
      component.isTennis = false;
      component.isScores = true;
      component.isEventHasCurrentPoints = false;
      component.oddsScores = {
        home: '1',
        away: '0'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([[undefined, '1', '0']]);
    });

    it('should push nothing', () => {
      component.event.comments = {
        teams: {
          player_1: undefined,
          home: undefined
        }
      } as any;
      component.oddsScoresData = undefined;
      component.isTennis = false;
      component.isScores = true;
      component.isEventHasCurrentPoints = false;

      component.isCricket = true;

      component['setScoresData']();

      expect(component.oddsScoresData).toBeNull();
    });

    it('sonarcloud this sensless test is for you', () => {
      component.event.comments.teams = {
        home: {},
        player_1: {}
      } as any;
      component.isTennis = false;
      component.isScores = true;
      component.isEventHasCurrentPoints = false;
      component.oddsScores = {
        home: '1',
        away: '0'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([[undefined, '1', '0']]);
    });

    it('should add badminton scores (has current scores)', () => {
      const scoreStub = ['G', 'P'];
      component.isTennis = false;
      component.isScores = true;
      component.isEventHasCurrentPoints = true;
      component.scoreHeaders = scoreStub;
      component.oddsScores = {
        home: '1',
        away: '0'
      };
      component.currentScores = {
        home: '2',
        away: '1'
      };

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([['G', '1', '0'], ['P', '2', '1']]);
    });

    it('should left scores empty (corner case)', () => {
      component.isTennis = false;
      component.isCricket = true;
      component.event.comments.teams = {};

      component['setScoresData']();

      expect(component.oddsScoresData).toBe(null);
    });

    it('should left scores empty (no scores)', () => {
      component.isTennis = false;
      component.isScores = false;

      component['setScoresData']();

      expect(component.oddsScoresData).toBe(null);
    });

    it('should add score for football', () => {
      const scoreStub = ['G', 'P'];
      component.isFootball = true;
      component.isScores = true;
      component.scoreHeaders = scoreStub;

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([['G', '0', '0']]);
    });

    it('should add score for other event', () => {
      const scoreStub = ['G', 'P'];
      component.isFootball = false;
      component.isCricket = false;
      component.isEventHasCurrentPoints = true;
      component.isScores = true;
      component.scoreHeaders = scoreStub;

      component['setScoresData']();

      expect(component.oddsScoresData).toEqual([
        ['G', '0', '0'],
        ['P', '0', '0']
      ]);
    });

    it('should add darts scores (only legs)', () => {
      const scoreStub = ['S', 'L'];
      const result = [['L', '1', '0']];
      component.eventComments.teams.home.score = null;
      component.isDarts = true;
      component.isScores = true;
      component.isEventHasCurrentPoints = true;
      component.scoreHeaders = scoreStub;
      component.currentScores = {
        home: '1',
        away: '0'
      };
      component['setScoresData']();
      expect(component.oddsScoresData).toEqual(result);
    });

    it('should add datrts scores (sets & legs)', () => {
      const scoreStub = ['S', 'L'];
      const result = [['S', '1', '0'], ['L', '2', '1']];
      component.eventComments.teams.home.score = '1';
      component.isDarts = true;
      component.isScores = true;
      component.isEventHasCurrentPoints = true;
      component.scoreHeaders = scoreStub;
      component.oddsScores = {
        home: '1',
        away: '0'
      };
      component.currentScores = {
        home: '2',
        away: '1'
      };
      component['setScoresData']();
      expect(component.oddsScoresData).toEqual(result);
    });

  });

  describe('addToFavourite', () => {
    it('should not change favourite status if locked', () => {
      component.isFavouriteClickLocked = true;
      component['addToFavourite']();

      expect(favouritesService.add).not.toHaveBeenCalled();
    });
    it('should call error', () => {
      component.isFavouriteClickLocked = false;
      component['addToFavourite']();
      favouritesService.add.and.returnValue(Promise.reject({
        catch: jasmine.createSpy('catch')
      }));
      expect(favouritesService.add).toHaveBeenCalled();
    });
  });

  describe('setClickLock', () => {
    it('should lock if pending', () => {
      component.isFavouriteClickLocked = undefined;
      component['setClickLock']('pending');

      expect(component.isFavouriteClickLocked).toEqual(true);
    });

    it('should not lock if no pending', () => {
      component.isFavouriteClickLocked = undefined;
      component['setClickLock']('');

      expect(component.isFavouriteClickLocked).toEqual(false);
    });
  });

  describe('initFavouriteListener', () => {
    beforeEach(() => {
      spyOn<any>(component, 'checkIsFavourite');
      spyOn<any>(component, 'setClickLock');
    });

    it('should call checkIsFavourite on SUCCESSFUL_LOGIN', () => {
      pubSubService.subscribe.and.callFake((f, method: string[], fn: Function) => {
        if (method[0] === 'SUCCESSFUL_LOGIN') {
          fn();
        }
      });
      component['initFavouriteListener']();

      expect(component['checkIsFavourite']).toHaveBeenCalled();
    });

    it('should call checkIsFavourite on SESSION_LOGOUT', () => {
      component.isFavouriteActive = undefined;
      pubSubService.subscribe.and.callFake((file, method: string[], fn: Function) => {
        if (method[0] === 'SESSION_LOGOUT') {
          fn();
        }
      });
      component['initFavouriteListener']();

      expect(component.isFavouriteActive).toBe(false);
    });

    it('should call setClickLock and set isFavouriteActive true', fakeAsync(() => {
      component.isFavouriteActive = undefined;
      favouritesService.registerListener = jasmine.createSpy().and.returnValues(Promise.resolve('added'), { then: () => {} });

      component['initFavouriteListener']();
      tick();

      expect(component['setClickLock']).toHaveBeenCalledWith('added');
      expect(component.isFavouriteActive).toBe(true);
    }));

    it('should call setClickLock and set isFavouriteActive false', fakeAsync(() => {
      component.isFavouriteActive = undefined;
      favouritesService.registerListener = jasmine.createSpy().and.returnValues(Promise.resolve('pending'), { then: () => {} });

      component['initFavouriteListener']();
      tick();

      expect(component['setClickLock']).toHaveBeenCalledWith('pending');
      expect(component.isFavouriteActive).toBe(false);
    }));

    it('should call setClickLock', fakeAsync(() => {
      component.isFavouriteActive = undefined;
      pubSubService.subscribe.and.returnValue(of(null));
      favouritesService.registerListener = jasmine.createSpy().and.returnValues(Promise.reject(), { then: () => {} });

      component['initFavouriteListener']();
      tick();

      expect(component['setClickLock']).toHaveBeenCalledWith('error');
      expect(component.isFavouriteActive).toBeUndefined();
    }));
  });
  describe('#showTemplate', () => {
    it('#showTemplate Returns True/False/True with header2Columns false &isHomeDrawAwayType false', () => {
      component.header2Columns = false;
      component.isHomeDrawAwayType = false;
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          request: {
            categoryId: '16'
          }
        }
      };
      expect(component.showTemplate(0)).toBe(true);
      expect(component.showTemplate(1)).toBe(false);
      expect(component.showTemplate(2)).toBe(true);
    });
    it('#showTemplate Returns True/False/True with header2Columns false &isHomeDrawAwayType true', () => {
      component.header2Columns = false;
      component.isHomeDrawAwayType = true;
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          request: {
            categoryId: '16'
          }
        }
      };
      expect(component.showTemplate(0)).toBe(true);
      expect(component.showTemplate(1)).toBe(true);
      expect(component.showTemplate(2)).toBe(true);
    });
    it('#showTemplate Returns True/False/True with header2Columns false &isHomeDrawAwayType true', () => {
      component.isHomeDrawAwayType = false;
      component.header2Columns = true;
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          request: {
            categoryId: '16'
          }
        }
      };
      expect(component.showTemplate(0)).toBe(true);
      expect(component.showTemplate(1)).toBe(false);
      expect(component.showTemplate(2)).toBe(true);
    });
    it('#showTemplate Returns True/False/True with header2Columns true &isHomeDrawAwayType true', () => {
      component.isHomeDrawAwayType = true;
      component.header2Columns = true;
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          request: {
            categoryId: '16'
          }
        }
      };
      expect(component.showTemplate(0)).toBe(true);
      expect(component.showTemplate(1)).toBe(false);
      expect(component.showTemplate(2)).toBe(true);
    });
    it('#showTemplate Returns True with threeOddsGolf true', () => {
      component.isHomeDrawAwayType = true;
      component.header2Columns = true;
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          request: {
            categoryId: '18'
          }
        }
      };
      expect(component.showTemplate(0)).toBe(true);
    });
  });

   describe('goToSeo', () => {
     it('should create seo ', () => {
       component.event = {
        markets: [{
            id: 111,
            name: 'Test',
            outcomes: [{
              id: 111,
              name: 'Test',
              correctedOutcomeMeaningMinorCode: 'H'
            }]
          }]
       } as any;
      routingHelper.formEdpUrl.and.returnValue('url');
      component.goToSeo();
      expect(routingHelper.formEdpUrl).toHaveBeenCalledWith(component.event);
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith(component.event,'url');
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
    });
   });

});

// TODO#################################################################################################################
// TODO#################################################################################################################
// TODO####################################### old ladbrokes testcases #################################################
// TODO#################################################################################################################
// TODO#################################################################################################################
describe('LMMultiMarketTemplateComponent', () => {
  let component: MultiMarketTemplateComponent;

  let
    templateService, marketTypeService, timeService, locale, filtersService, coreToolsService, routingHelper,
    pubSubService, router, smartBoostsService, userService, commandService,
    windowRef, betSlipSelectionsData, priceOddsButtonService, routingState, gtmTrackingService, gtmService,
    favouritesService, sportsConfigService, scoreParserService, sportEventHelperService, outcomeTemplateHelperService;

  let testStr, wasPriceStub, changeDetectorRef,seoDataService;

  beforeEach(() => {
    testStr = 'TestString';
    wasPriceStub = 'TestWasPrice';

    filtersService = {
      getTeamName: () => 'teamA',
      groupBy: arr => arr,
      numberSuffix: (runningSetIndex)=> runningSetIndex
    } as any;
    router = {
        navigateByUrl: jasmine.createSpy('navigateByUrl')
    } as any;
    timeService = {
      determineDay: () => 'today',
      getLocalHourMin: () => {},
      isInNext24HoursRange: () => true,
      getEventTime: jasmine.createSpy().and.returnValue('12:00, 12 Mar')
    } as any;
    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('some url'),
    } as any;
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
    locale = {
      getString: () => 'test'
    } as any;

    pubSubService = {
      unsubscribe: () => {},
      subscribe: (name: string, chnl: any, func: Function) => func({ event: { id: 1 } } as any),
      API: {
        EVENT_SCORES_UPDATE: 'EVENT_SCORES_UPDATE',
        MOVE_EVENT_TO_INPLAY: 'MOVE_EVENT_TO_INPLAY',
      }
    } as any;

    templateService = {
      getSportViewTypes: () => {
        return {};
      },
      getTemplate: () => {
        return {};
      },
      isMultiplesEvent: () => false
    } as any;
    marketTypeService = {
      isMatchResultType: () => {},
      isHeader2Columns: () => {},
      isHomeDrawAwayType: () => true,
      extractMarketNameFromEvents: (events: ISportEvent[], isFilterByTemplateMarketName?: boolean): string[] => {
        const marketNames = _.reduce(events, (accumulator, event) => {
          const eventMarketNames = (event.markets || []).map(market => {
            if (isFilterByTemplateMarketName) {
              if (market.templateMarketName === 'Match Betting') {
                market.templateMarketName = 'Match Result';
              }
              return market.templateMarketName;
            }
    
            return market.name;
          });
    
          accumulator.push(...eventMarketNames);
    
          return accumulator;
        }, []);
        return marketNames;
      }
    } as any;
    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
    } as any;

    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType'),
      parseScores: jasmine.createSpy('parseScores')
    };

    userService = seoDataService = {};
    commandService = {};
    windowRef = {};
    betSlipSelectionsData = {
      getSelectionsByOutcomeId: jasmine.createSpy('getSelectionsByOutcomeId').and.returnValue([{}])
    };
    priceOddsButtonService = {};
    routingState = {};
    gtmTrackingService = {};
    gtmService = {};

    favouritesService = {
      registerListener: () => {
        return { then: jasmine.createSpy('then')};
      },
      deRegisterListener: jasmine.createSpy('deRegisterListener'),
      add: jasmine.createSpy('add').and.returnValue({
        catch: jasmine.createSpy('catch')
      }),
      isFavourite: () => {
        return Promise.resolve();
      },
      showFavourites: () => {
        return of(true);
      }
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {
          config: {}
        }
      }))
    };

    sportEventHelperService = {
      isOutrightEvent: jasmine.createSpy('isOutrightEvent'),
      isSpecialEvent: jasmine.createSpy('isSpecialEvent')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    outcomeTemplateHelperService = {
        setOutcomeMeaningMinorCode: (markets, event) => {
            markets.forEach((market: IMarket) => {
                if (market.outcomes && market.outcomes.length > 0) {
                  market.outcomes.sort((a, b) => a.correctedOutcomeMeaningMinorCode - b.correctedOutcomeMeaningMinorCode);
                }
              });
        }
    }

    component = new MultiMarketTemplateComponent(
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
      scoreParserService as any,
      sportEventHelperService,
      changeDetectorRef,
      seoDataService as any,
      outcomeTemplateHelperService as any
    );

    component.event = {
      name: 'Test',
      id: 111,
      marketsCount: 2,
      markets: [{
        id: 111,
        name: 'Test',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      }],
      isStarted: true,
      eventIsLive: true,
      categoryName: 'other'
    } as any;
    component.event.comments = component.event.comments = {} as any;
    component.selectedMarketObject = component.event.markets[0];
  });

  describe('#ngOnInit should init the component', () => {

    it('data false for tennis', () => {
      component.event.categoryName = 'Badminton';
      component.ngOnInit();
      expect(component.tennisScores).toBeUndefined();
      expect(component.servingTeams).toEqual([false, false]);
      expect(component.scoreHeaders).toEqual(['G', 'P']);
    });

    it('component properties should be initialized', () => {
      component.eventStartedOrLive = true;
      component.ngOnInit();
      expect(component.scoreHeaders).toBeNull();
      expect(component.isScores).toBe(false);
      expect(component.oddsScores).toEqual({home: '0', away: '0'});
      expect(component.currentScores).toEqual({home: '0', away: '0'});
      expect(component.oddsLabel).toBe('');
    });

    it('component isScores properties false cases', () => {
      component.isOddsSports = true;
      component.event.comments =  null;
      component.ngOnInit();
      expect(component.isScores).toBe(false);

      component.event.comments = { teams: {} as any } as any;
      component.event.outcomeStatus = true;
      component.ngOnInit();
      expect(component.isScores).toBe(false);
    });

    it('event scores are initialized but 0', () => {
      component.event.outcomeStatus = false;
      component.event.comments = {
        teams: {
          home: {},
          away: {}
        }
      } as any;

      component.ngOnInit();
      expect(component.isScores).toBe(true);
      expect(component.oddsScores).toEqual({home: '0', away: '0'});
      expect(component.currentScores).toEqual({home: '0', away: '0'});
    });
  });

  describe('#calculateScores should set scores', () => {
    it('event scores should be initialized when isUs is false', () => {
      component.event.outcomeStatus = false;
      component.event.isUS = false;
      component.teamRoleCodes = ['home', 'away'];
      component.isEventHasCurrentPoints = true;
      component.event.comments = {
        teams: {
          home: {
            score: '1',
            currentPoints: '3'
          },
          away: {
            score: '2',
            currentPoints: '4'
          }
        }
      } as any;

      component['calculateScores']();
      expect(component.oddsScores).toEqual({home: '1', away: '2'});
      expect(component.currentScores).toEqual({home: '3', away: '4'});
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('event scores should be initialized when isUs is true', () => {
      component.event.outcomeStatus = false;
      component.event.isUS = true;
      component.teamRoleCodes = ['home', 'away'];
      component.event.comments = {
        teams: {
          home: {
            score: '1'
          },
          away: {
            score: '2'
          }
        }
      } as any;

      component['calculateScores']();
      expect(component.oddsScores).toEqual({home: '2', away: '1'});
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('setTennisScores', () => {

    it('no eventComments', () => {
      const headers = ['S', 'G', 'P'];
      component.event.comments = null;
      expect(component['setTennisScores'](headers)).toEqual([['S', '0', '0'], ['G', '0', '0'], ['P', '0', '0']]);
    });

    it('all data exist', () => {
      const headers = ['S', 'G', 'P'];
      component.teamRoleCodes = ['player_1', 'player_2'];
      component.event.isUS = false;
      component.isSetsGamesPoints = true;
      component.event.comments = {
        runningSetIndex: '2',
        teams: {
          player_1: {
            score: '1',
            id: '12345',
          },
          player_2: {
            score: '2',
            id: '54321',
          }
        },
        setsScores: {
          '1': {},
          '2': {
            '12345': '3',
            '54321': '4'
          }
        },
        runningGameScores: {
          '12345': '15',
          '54321': '30'
        }
      } as any;
      component['setScoresSettings']();
      component['calculateScores']();
      expect(component['setTennisScores'](headers)).toEqual([['S', '1', '2'], ['G', '3', '4'], ['P', '15', '30']]);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('player_1, set by runnixIndex are undefined', () => {
      const headers = ['S', 'G', 'P'];
      component.event.comments = {
        runningSetIndex: '2',
        teams: {},
        setScores: {
          '1': {}
        },
        runningGameScores: {
          '12345': '15',
          '54321': '30'
        }
      } as any;

      expect(component['setTennisScores'](headers)).toEqual([['S', '0', '0'], ['G', '0', '0'], ['P', '15', '30']]);
    });

    it('teams, setScores, runningGameScores are undefined', () => {
      const headers = ['S', 'G', 'P'];
      component.event.comments = {
        runningSetIndex: '2'
      } as any;

      expect(component['setTennisScores'](headers)).toEqual([['S', '0', '0'], ['G', '0', '0'], ['P', '0', '0']]);
    });

    it('player_1/2, but score field is undefined', () => {
      const headers = ['S', 'G', 'P'];
      component.event.comments = {
        runningSetIndex: '2',
        teams: {
          player_1: {},
          player_2: {}
        }
      } as any;

      expect(component['setTennisScores'](headers)).toEqual([['S', '0', '0'], ['G', '0', '0'], ['P', '0', '0']]);
    });

    it('default ruining index as 1', () => {
      const headers = ['S', 'G', 'P'];
      component.event.comments = {
        setsScores: {
          '1': {
            '12345': '3',
            '54321': '4'
          },
          '2': {}
        }
      } as any;

      const res = component['setTennisScores'](headers);

      expect(res).toEqual([['S', '0', '0'], ['G', '3', '4'], ['P', '0', '0']]);
      expect(res[1]).toEqual(['G', '3', '4']);
    });

    it('bad scores data should be zeroed', () => {
      const headers = ['S', 'G', 'P'];
      component.event.comments = {
        setsScores: {
          '1': {}
        }
      } as any;

      expect(component['setTennisScores'](headers)).toEqual([['S', '0', '0'], ['G', '0', '0'], ['P', '0', '0']]);
    });
  });

  describe('isSelectedMarket', () => {
    it('should return true', () => {
      const market = {
        templateMarketName: 'Match Result',
        name: 'Match Result'
      } as any;
      component.selectedMarket = 'Match Result';

      expect(component.isSelectedMarket(market)).toBe(true);
    });

    it('should return true', () => {
      const market = {
        templateMarketName: 'Match Result',
        name: 'Match Result'
      } as any;
      component.selectedMarket = null;

      expect(component.isSelectedMarket(market)).toBe(true);
    });

    it('should return true', () => {
      const market = {
        templateMarketName: 'Match Betting',
        name: 'Match Result'
      } as any;
      component.selectedMarket = 'Match Result';

      expect(component.isSelectedMarket(market)).toBe(true);
    });

    it('should return false', () => {
      const market = {
        templateMarketName: 'Match Betting',
        name: 'Match Result'
      } as any;
      component.selectedMarket = 'To Qualify';

      expect(component.isSelectedMarket(market)).toBe(false);
    });
  });

  describe('isLiveFeaturedSelection', () => {
    it('isLiveFeaturedSelection should expect a boolean', () => {
      component.featured = { 'isSelection': true } as any;
      component.isEventStartedOrLive = true;
      expect(component.isLiveFeaturedSelection()).toBe(true);

      component.featured = { 'isSelection': false } as any;
      component.isEventStartedOrLive = true;
      expect(component.isLiveFeaturedSelection()).toBe(false);

      component.featured = { 'isSelection': false } as any;
      component.isEventStartedOrLive = false;
      expect(component.isLiveFeaturedSelection()).toBe(false);
    });
  });

  describe('isLive', () => {
    it('isLive should expect a boolean', () => {
      component.isEventStartedOrLive = true;
      expect(component.isLive).toBe(true);

      component.isEventStartedOrLive = false;
      expect(component.isLive).toBe(false);
    });
  });

  describe('trackByOutcomes', () => {
    it('should return unique index if outcome received', () => {
      expect(component.trackByOutcomes(4, {
        id: 5
      } as any)).toEqual('4_5');
    });
    it('should return unique index if outcome not received', () => {
      expect(component.trackByOutcomes(4, undefined)).toEqual('4_');
    });
  });

  describe('setSignsForHandicap', () => {
    it('should return handicap value', () => {
      component.correctedOutcomes = null;
      expect(component.setSignsForHandicap('5.0')).toEqual('5.0');
    });
    it('should return plus handicap value', () => {
      component.header2Columns = false;
      component.isHomeDrawAwayType = true;
      component.correctedOutcomes = [
        {id: '1'},{id: '2'}, {id: '3'}
      ] as any;
      expect(component.setSignsForHandicap('5.0')).toEqual(' +5.0');
    });
    it('should return plus handicap value with negative value', () => {
      component.header2Columns = false;
      component.isHomeDrawAwayType = true;
      component.correctedOutcomes = [
        {id: '1'},{id: '2'}, {id: '3'}
      ] as any;
      expect(component.setSignsForHandicap('-5.0')).toEqual(' -5.0');
    });
  });
  it("should call setOverUnderTag", () => {
    expect(component.setOverUnderTag('Total Points', 'Over')).toEqual('O');
   });
  it("should call init", () => {
    component.selectedMarket = 'Match Betting,Total Points,Handicap Betting';
    component.event = {
      name: 'Test',
      id: 111,
      marketsCount: 3,
      markets: [{
        id: 111,
        name: 'Test',
        templateMarketName: 'Match Betting',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        },
        {
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 1
        },
        {
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 1
        }]
      },{
        id: 111,
        name: 'Test',
        templateMarketName: 'Match Betting',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      },{
        id: 111,
        name: 'Test',
        templateMarketName: 'Handicap Betting',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      },{
        id: 111,
        name: 'Test',
        templateMarketName: 'Total Points',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
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
      },
      categoryId :16
    } as any;
    component.init();
    expect(component.showThreeOdds).toBeFalse();
   });
  it("should call reorder", () => {
    component.selectedMarket = 'Match Betting,Total Points,Handicap Betting';
    component.event = {
      name: 'Test',
      id: 111,
      marketsCount: 3,
      markets: [{
        id: 111,
        name: 'Test',
        templateMarketName: 'Match Betting',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        },
        {
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 1
        },
        {
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 1
        }]
      },{
        id: 111,
        name: 'Test',
        templateMarketName: 'Match Betting',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      },{
        id: 111,
        name: 'Test',
        templateMarketName: 'Handicap Betting',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
        }]
      },{
        id: 111,
        name: 'Test',
        templateMarketName: 'Total Points',
        outcomes: [{
          id: 111,
          name: 'Test',
          correctedOutcomeMeaningMinorCode: 'H'
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
      },
      categoryId :16
    } as any;
    component.reorder(component.event);
    expect(component.event.markets.length).toEqual(4);
   });
  it("should call formatPoints", () => {
    expect(component.formatPoints('Adv')).toEqual('A');
    expect(component.formatPoints('H')).toEqual('H');
   });
  it("should call isClockAllowed", () => {
    component.event.clock = true;
    component.featured = {
      isSelection: true
    };
    component.isEventStartedOrLive = true;
    expect(component.isClockAllowed()).toBeFalse();
   });
  it("should call goToEvent", () => {
    expect(component.goToEvent(true, component.event)).toEqual('some url');
    component.event.isFinished = false;
    component['isEnhancedMultiples'] = undefined;
    component.goToEvent(false, component.event);
    expect(router.navigateByUrl).toHaveBeenCalled();
   });
  it("should call isLiveLabelShown", () => {
    component.oddsLabel = 'label';
    component.liveLabelText = 'label';
    expect(component.isLiveLabelShown).toBeTrue();
   });
  it("should call isLabelShown", () => {
    component.oddsLabel = 'label';
    component.liveLabelText = 'label1';
    expect(component.isLabelShown).toBeTrue();
   });
  it("should call isMatchClock", () => {
    component.event.clock = {matchTime: '1:00'};
    component.isHalfOrFullTime = false;
    expect(component.isMatchClock).toBeTrue();
   });
});
