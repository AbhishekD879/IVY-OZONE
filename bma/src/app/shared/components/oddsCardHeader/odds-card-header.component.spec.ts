import { of } from 'rxjs';

import { OddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';
describe('OddsCardHeaderComponent', () => {
  let component: OddsCardHeaderComponent,
    marketTypeService,
    templateService,
    oddsCardHeaderService,
    pubSubService,
    scoreParserService,
    sportsConfigService,
    sportsConfigHelperService,
    changeDetectorRef,
    coreToolsService: any;

  beforeEach(() => {
    marketTypeService = {
      isYesNoType: jasmine.createSpy('isYesNoType').and.returnValue(true),
      isOverUnderType: jasmine.createSpy('isOverUnderType').and.returnValue(true),
      isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType'),
      someEventsAreMatchResultType: jasmine.createSpy('someEventsAreMatchResultType').and.returnValue(false),
      isOneTieTwoType: jasmine.createSpy('isOneTieTwoType').and.returnValue(false),
      isOneDrawTwoType: jasmine.createSpy('isOneDrawTwoType').and.returnValue(false),
      getDisplayMarketConfig: jasmine.createSpy('getDisplayMarketConfig').and.returnValue({
        displayMarketName: 'market name'
      }),
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
    templateService = {
      getMarketViewType: jasmine.createSpy('getMarketViewType').and.returnValue('viewType'),
      isListTemplate: (selectedMarket: string)=>{
        return oddsCardConstant.LIST_TEMPLATES.indexOf(selectedMarket) !== -1;
       },
       isMultiMarketTemplate: (selectedMarket: string)=>{
        const marketFilterList = selectedMarket ? selectedMarket.split(',') : [];
        return marketFilterList.length > 1 ? true : false;
       }, 
    };
    oddsCardHeaderService = {
      getSportName: jasmine.createSpy('getSportName').and.returnValue('some'),
      isRacing: jasmine.createSpy('isRacing').and.returnValue(true),
      getLocale: jasmine.createSpy('getLocale'),
      isSpecialSection: jasmine.createSpy('isSpecialSection').and.returnValue(false),
      isEventsHaveScores: jasmine.createSpy('isEventsHaveScores'),
      sortEventsByScores: jasmine.createSpy('sortEventsByScores'),
      extendSportConfig: jasmine.createSpy('extendSportConfig'),
      showComponent: jasmine.createSpy('showComponent').and.returnValue(true),
      getMarketByTemplateMarketName: jasmine.createSpy('getMarketByTemplateMarketName').and.returnValue({ outcomes: [{}] }),
      getHeaderByMarketName: jasmine.createSpy('getHeaderByMarketName').and.returnValue('some'),
      getHeaderByViewType: jasmine.createSpy('getHeaderByViewType'),
      extractMarketNameFromEvents: jasmine.createSpy('extractMarketNameFromEvents'),
      getMultiTemplateHeader: (title) => {
        if(title === '60 Minute Betting') {
          return '60 Min';
        } else {
          return title;
        }
      }
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        EVENT_SCORES_UPDATE: 'EVENT_SCORES_UPDATE',
        DELETE_EVENT_FROM_CACHE: 'DELETE_EVENT_FROM_CACHE',
        WS_EVENT_UPDATE: 'WS_EVENT_UPDATE'
      },
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('randomUuid'),
    };
    scoreParserService = {
      getScoreHeaders: jasmine.createSpy('getScoreHEaders'),
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {}
      }))
    };
    sportsConfigHelperService = {
      getSportConfigName: jasmine.createSpy('getSportConfigName')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };

    component = new OddsCardHeaderComponent(
      marketTypeService,
      templateService,
      oddsCardHeaderService,
      pubSubService,
      coreToolsService,
      scoreParserService,
      sportsConfigService,
      sportsConfigHelperService,
      changeDetectorRef
    );

    component.sportConfig = {
      config: {
        request: {
          marketTemplateMarketNameIntersects: 'marketTemplateMarketNameIntersects'
        }
      }
    };
    component.isMarketSwitcherConfigured = true;
  });

  describe('#initHeader', () => {
    beforeEach(() => {
      component.events = [{}] as any;
    });

    it('no events', () => {
      component.events = [];
      component['oddsCardHeader'] = '1';

      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
    });

    it('no sport data in sportsConfig', () => {
      component['sportsConfig'] = {} as any;

      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
      expect(component.showOddsCardHeader).toBe(false);
      expect(marketTypeService.getDisplayMarketConfig).toHaveBeenCalled();
    });

    it('check golfOutright and no golfOutright', () => {
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
      component.events = [
        { isFinished: false, markets: [], name: 'Soderberg/Gagli/Porteous',
      eventSortCode: 'TNMT' } as any
      ];
      component.isMarketSwitcherConfigured = false;
      component['initHeader']();
      expect(component.selectedMarket).toEqual('market name');
      component.sportConfig.config.request.categoryId = '2';
      component['initHeader']();
      expect(component.selectedMarket).toEqual('market name');

    });

    it('when listTemplate is true', () => {
      component.sportConfig = {
        isFootball: true,
        config: {
          request: {
            categoryId: '16'
          }
        }
      } as any;
      component.selectedMarket = 'Winning Margin';
      component['initHeader']();
      expect(component.showOddsCardHeader).toBe(true);
    });

    it('#checkDartEventOnlyLeg Check Darts only leg If', () => {
      component.scoreHeaders = ['S', 'L'] as any;
      component.events = [{
        categoryId: '13',
        comments:{
            teams: {
            home: {
              name: 'A',
              currentPoints: '1',
              score: null
            },
            away: {
              name: 'B',
              currentPoints: '2',
              score: null
            }
          }
        }
      }] as any;
      component['checkDartEventOnlyLeg']();
      expect(component.dartsOnlyLegs).toBe(true);
    });

    it('#checkDartEventOnlyLeg Check Darts sets & legs', () => {
      component.scoreHeaders = ['S', 'L'] as any;
      component.events = [{
        categoryId: '13',
        comments:{
          teams: {
          home: {
            name: 'A',
            currentPoints: '4',
            score: '1'
          },
          away: {
            name: 'B',
            currentPoints: '5',
            score: '2'
          }
        }
        }
      }] as any;
      component['checkDartEventOnlyLeg']();
      expect(component.eventScoreLabel).toBe(true);
    });

    it('#checkDartEventOnlyLeg Check no headers', () => {
      component.scoreHeaders = null;
      component.events = [];
      component['checkDartEventOnlyLeg']();
      expect(component.eventScoreLabel).toBe(false);
    });
    it('should not call getDisplayMarketConfig', () => {
      component.sportConfig = {
        isFootball: true,
        config: {
          request: {
            categoryId: '16'
          }
        }
      } as any;

      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
      expect(component.showOddsCardHeader).toBe(false);
      expect(marketTypeService.getDisplayMarketConfig).not.toHaveBeenCalled();
    });

    it('selectedMarket not equal handicap', () => {
      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
      expect(component['showOddsCardHeader']).toEqual(false);
    });

    it('sportConfig is null', () => {
      oddsCardHeaderService.isRacing = jasmine.createSpy().and.returnValue(false);
      component.sportConfig = null as any;

      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
      expect(component['showOddsCardHeader']).toEqual(false);
    });

    it('isRacing return false', () => {
      oddsCardHeaderService.isRacing = jasmine.createSpy('isRacing').and.returnValue(false);
      oddsCardHeaderService.isSpecialSection = jasmine.createSpy('isSpecialSection').and.returnValue(true);

      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
      expect(component['showOddsCardHeader']).toEqual(false);
    });

    describe('exist sportConfig and isSpecialEvent = false', () => {
      beforeEach(() => {
        oddsCardHeaderService.isRacing = jasmine.createSpy('isRacing').and.returnValue(false);
        component['getOddsCardHeader'] = jasmine.createSpy('getOddsCardHeader').and.callThrough();
        component['setOddCardHeaderType'] = jasmine.createSpy('setOddCardHeaderType').and.callThrough();
        component['setHeaderContent'] = jasmine.createSpy('setHeaderContent').and.callThrough();
        component['showScoreHeaders'] = jasmine.createSpy('showScoreHeaders').and.callThrough();
      });

      it('exist isMultiTemplateSport', () => {
        component['initHeader']();
      });

      it('selectedMarket !== handicapTemplateMarketName', () => {
        component.sportConfig.config.request = {
          marketTemplateMarketNameIntersects: 'marketTemplateMarketNameIntersects'
        } as any;

        component['initHeader']();
      });

      it('sportName !== football', () => {
        component.sportConfig.config.oddsCardHeaderType = null;

        component['initHeader']();
      });

      it('sportName == football', () => {
        component.sportConfig.config.oddsCardHeaderType = {};
        component['sportName'] = 'football';

        component['initHeader']();
      });
      afterEach(() => {
        expect(component['setOddCardHeaderType']).toHaveBeenCalled();
        expect(component['showScoreHeaders']).toHaveBeenCalled();
        expect(component['setOddCardHeaderType']).toHaveBeenCalledTimes(2);
        expect(component['setHeaderContent']).toHaveBeenCalled();
        expect(component['getOddsCardHeader']).toHaveBeenCalledTimes(1);
      });
    });

    describe('isMarketSwitcherConfigured', () => {
      beforeEach(() => {
        oddsCardHeaderService.isRacing = jasmine.createSpy('isRacing').and.returnValue(false);
        component['getOddsCardHeader'] = jasmine.createSpy('getOddsCardHeader').and.callThrough();
        component['setOddCardHeaderType'] = jasmine.createSpy('setOddCardHeaderType').and.callThrough();
        component['setHeaderContent'] = jasmine.createSpy('setHeaderContent').and.callThrough();
        component['showScoreHeaders'] = jasmine.createSpy('showScoreHeaders').and.callThrough();
      });
      it('isMarketSwitcherConfigured false ', () => {
        component.sportConfig.config.oddsCardHeaderType = {
          outcomesTemplateType1: 'outcomesTemplateType1'
        };
        component.isMarketSwitcherConfigured = false;
        component['initHeader']();
        expect(component['setOddCardHeaderType']).toHaveBeenCalledTimes(1);
      });
      it('isMarketSwitcherConfigured true and categoryId is 16', () => {
        component.sportConfig.config.request.categoryId = '16';
        component.sportConfig.config.oddsCardHeaderType = {
          outcomesTemplateType1: 'outcomesTemplateType1'
        };
        component.isMarketSwitcherConfigured = true;
        component['initHeader']();
        expect(component['setOddCardHeaderType']).toHaveBeenCalledTimes(1);
      });
      it('isMarketSwitcherConfigured false and categoryId is 16', () => {
        component.sportConfig.config.request.categoryId = '16';
        component.sportConfig.config.oddsCardHeaderType = {
          outcomesTemplateType1: 'outcomesTemplateType1'
        };
        component.isMarketSwitcherConfigured = false;
        component['initHeader']();
        expect(component['setOddCardHeaderType']).toHaveBeenCalledTimes(1);
      });
    });
    describe('set oddsCardHeader', () => {
      beforeEach(() => {
        component.sportConfig.config.oddsCardHeaderType = {
          outcomesTemplateType1: 'outcomesTemplateType1'
        };
        oddsCardHeaderService.isRacing = jasmine.createSpy('isRacing').and.returnValue(false);

        component['setHeaderContent'] = jasmine.createSpy('setHeaderContent').and.callThrough();
        component['showScoreHeaders'] = jasmine.createSpy('showScoreHeaders').and.callThrough();
        component['setOddCardHeaderType'] = jasmine.createSpy('setOddCardHeaderType').and.callThrough();

      });
      it('if oddsCardHeaderType is obj', () => {
        component['initHeader']();

        expect(component['oddsCardHeader']).toEqual('outcomesTemplateType1');
      });

      it('if oddsCardHeaderType is string', () => {
        component.sportConfig.config.oddsCardHeaderType = 'outcomesTemplateType';

        component['initHeader']();

        expect(component['oddsCardHeader']).toEqual('outcomesTemplateType');
      });

      afterEach(() => {
        expect(component['setHeaderContent']).toHaveBeenCalled();
        expect(component['showScoreHeaders']).toHaveBeenCalled();
        expect(component['setOddCardHeaderType']).toHaveBeenCalled();
      });
    });

    it('is not special', () => {
      component['sportsConfig'] = {
        'some': {}
      } as any;

      component['initHeader']();

      expect(component['oddsCardHeader']).toBeUndefined();
      expect(component.showOddsCardHeader).toBe(false);
    });

    it('isMultiTemplateSport true/false && no oddsCardHeaderType', () => {
      component['sportConfig'] = {
        config: {
          isMultiTemplateSport: true,
          request: {
            marketTemplateMarketNameIntersects: 'marketTemplateMarketNameIntersects'
          }
        }
      } as any;
      (oddsCardHeaderService.isRacing as jasmine.Spy).and.returnValue(true);
      component['getOddsCardHeader'] = jasmine.createSpy().and.returnValue('header text');
      component['setOddCardHeaderType'] = jasmine.createSpy();
      component['setHeaderContent'] = jasmine.createSpy();

      component['initHeader']();
      expect(component['oddsCardHeader']).toBe(undefined);
      expect(component['showOddsCardHeader']).toBe(false);
      expect(component['undisplayedMarket']).toBe(null);
    });
  });

  describe('showScoreHeaders', () => {
    it('it should not set scoreHeaders if isScoreHeader=false', () => {
      component.isScoreHeader = false;
      component.showScoreHeaders('16');

      expect(component.scoreHeaders).toBe(null);
    });

    it('it should set scoreHeaders if isScoreHeader=true', () => {
      component.events = [];
      component.isScoreHeader = true;
      oddsCardHeaderService.isEventsHaveScores = jasmine.createSpy('isEventsHaveScores').and.returnValue(true);
      scoreParserService.getScoreHeaders = jasmine.createSpy('getScoreHeaders').and.returnValue(['S', 'G', 'P']);
      component.showScoreHeaders('16');

      expect(component.scoreHeaders).toEqual(['S', 'G', 'P']);
      expect(oddsCardHeaderService.sortEventsByScores).toHaveBeenCalledWith([]);
    });

    it('it should not set scoreHeaders if isScoreHeader=false', () => {
      component.events = [];
      component.isScoreHeader = true;
      oddsCardHeaderService.isEventsHaveScores = jasmine.createSpy('isEventsHaveScores').and.returnValue(true);
      scoreParserService.getScoreHeaders = jasmine.createSpy('getScoreHeaders').and.returnValue(null);

      component.showScoreHeaders('16');

      expect(component.scoreHeaders).toEqual(null);
      expect(oddsCardHeaderService.sortEventsByScores).not.toHaveBeenCalled();
    });
  });


  describe('#setHeaderContent', () => {
    it('it should set yesNoType header', () => {
      component['getFirstNotSpecialMarket'] = jasmine.createSpy().and.returnValue({});
      component.events = [{ markets: [] }] as any;
      component['oddsCardHeader'] = 'yesNoType';

      component['setHeaderContent']();

      expect(oddsCardHeaderService.getLocale).toHaveBeenCalledWith('over,under');
    });

    it('it should set homeDrawAwayType header', () => {
      component['getFirstNotSpecialMarket'] = jasmine.createSpy().and.returnValue({});
      component.events = [] as any;
      component['oddsCardHeader'] = 'homeDrawAwayType';

      component['setHeaderContent']();

      expect(oddsCardHeaderService.getLocale).toHaveBeenCalledWith('home,draw,away');
    });

    it('it should set homeAwayType header', () => {
      component['getFirstNotSpecialMarket'] = jasmine.createSpy().and.returnValue({});
      component.events = [] as any;
      component['oddsCardHeader'] = 'homeAwayType';

      component['setHeaderContent']();

      expect(oddsCardHeaderService.getLocale).toHaveBeenCalledWith('home,away');
    });

    it('should set showOddsCardHeader header', () => {
      component['availableOddsHeader'] = true;
      component['oddsCardHeader'] = 'oddsCardHeader';
      component.events = [] as any;

      component['setHeaderContent']();

      expect(component.showOddsCardHeader).toEqual(true);
    });

    it('should not set showOddsCardHeader header', () => {
      component['availableOddsHeader'] = true;
      component['hasOutcomeStatusTrue'] = true;
      component.events = [] as any;

      component['setHeaderContent']();

      expect(component.showOddsCardHeader).toEqual(false);
    });

    it('should not set showOddsCardHeader header', () => {
      component['availableOddsHeader'] = true;
      component.events = [] as any;

      component['setHeaderContent']();

      expect(component.showOddsCardHeader).toEqual(false);
    });

    it('should set OverUnderType header', () => {
      marketTypeService.isOverUnderType = jasmine.createSpy('isOverUnderType').and.returnValue(true);
      component['getFirstNotSpecialMarket'] = jasmine.createSpy().and.returnValue({});
      component.events = [{}] as any;
      component['oddsCardHeader'] = 'homeDrawAwayType';

      component['setHeaderContent']();

      expect(oddsCardHeaderService.getLocale).toHaveBeenCalledWith('over,under');
    });

    it('should set over/under header', () => {
      component['getFirstNotSpecialMarket'] = jasmine.createSpy().and.returnValue(null);
      component.events = [{}] as any;
      component['oddsCardHeader'] = 'homeDrawAwayType';
      component['getFirstNotSpecialMarket'] = jasmine.createSpy('getFirstNotSpecialMarket').and.returnValue(true);

      component['setHeaderContent']();

      expect(oddsCardHeaderService.getLocale).toHaveBeenCalledWith('over,under');
    });
  });

  describe('#getFirstNotSpecialMarket', () => {
    it('should call getFirstNotSpecialMarket', () => {
      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(true);
      component.sportConfig = {} as any;
      component['getFirstNotSpecialMarket']([{
        id: '123',
        markets: []
      }] as any);

      expect(oddsCardHeaderService.isSpecialEvent).toHaveBeenCalledWith({
        id: '123',
        markets: []
      }, {});
    });

   it('should call getFirstNotSpecialMarket with selectedMarket not equal handicap', () => {
      component.selectedMarket = 'Match Result';
      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(false);
      component.sportConfig = {} as any;
      component['getFirstNotSpecialMarket']([{
        id: '123',
        markets: [{}]
      }] as any);

      expect(oddsCardHeaderService.isSpecialEvent).toHaveBeenCalledWith({
        id: '123',
        markets: [{}]
      }, {});
    });

    it('should get filtered market to set Card Header', () => {
      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(false);
      const events = [{
        id: '123',
        markets: [{
          templateMarketName: 'Match Result'
        },
        {
          templateMarketName: ''
        }]
      }] as any;
      component.selectedMarket = 'Match Result';
      component['isFilterByTemplateMarketName'] = true;

      const result = component['getFirstNotSpecialMarket'](events);

      expect(result).toEqual({
        templateMarketName: 'Match Result'
      } as any);
    });

    it('should get filtered market to set Card Header isFilterByTemplateMarketName false', () => {
      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(false);
      const events = [{
        id: '123',
        markets: [{
          templateMarketName: 'Match Result',
          name: 'Match Betting'
        },
        {
          templateMarketName: ''
        }]
      }] as any;
      component.selectedMarket = 'Match Result';
      component['isFilterByTemplateMarketName'] = false;

      const result = component['getFirstNotSpecialMarket'](events);

      expect(result).toEqual({
        templateMarketName: 'Match Result',
          name: 'Match Betting'
      } as any);
    });
  });

  describe('#getOddsCardHeader', () => {
    it('should call getOddsCardHeader method for special event', () => {
      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(true);
      component.sportConfig = {} as any;
      component['getOddsCardHeader']([{
        id: '12345'
      }] as any);

      expect(oddsCardHeaderService.isSpecialEvent).toHaveBeenCalledWith({
        id: '12345'
      }, {});
    });

    it('should call getOddsCardHeader method for non special event', () => {
      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(false);
      component.sportConfig = {} as any;
      component['getOddsCardHeader']([{
        id: '12345',
        markets: [{
          name: 'Goals'
        }]
      }] as any);

      expect(oddsCardHeaderService.isSpecialEvent).toHaveBeenCalledWith({
        id: '12345',
        markets: [{
          name: 'Goals'
        }]
      }, {});
      expect(templateService.getMarketViewType).not.toHaveBeenCalled();
      expect(oddsCardHeaderService.getHeaderByViewType).not.toHaveBeenCalled();
    });

    it('should call getMarketViewType method for market', () => {
      const events = [{
        id: '12345',
        markets: [{
          name: 'Goals'
        }]
      }] as any;
      const sportName = 'football';
      component['selectedMarket'] = 'selectedMarket';

      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(false);
      oddsCardHeaderService.getHeaderByMarketName = jasmine.createSpy('getHeaderByMarketName').and.returnValue('');
      component.sportConfig = {} as any;
      component['getOddsCardHeader'](events, sportName);

      expect(oddsCardHeaderService.isSpecialEvent).toHaveBeenCalledWith({
        id: '12345',
        markets: [{
          name: 'Goals'
        }]
      }, {});

      expect(templateService.getMarketViewType).toHaveBeenCalled();
      expect(oddsCardHeaderService.getHeaderByViewType).toHaveBeenCalled();
    });

    it('should not call getMarketViewType method for market', () => {
      const events = [{
        id: '12345',
        markets: [{
          name: 'Goals'
        }]
      }] as any;
      const sportName = 'football';
      component['selectedMarket'] = 'selectedMarket';

      oddsCardHeaderService.isSpecialEvent = jasmine.createSpy('isSpecialEvent').and.returnValue(false);
      oddsCardHeaderService.getHeaderByMarketName = jasmine.createSpy('getHeaderByMarketName').and.returnValue('');
      oddsCardHeaderService.getMarketByTemplateMarketName = jasmine.createSpy('getMarketByTemplateMarketName').and.returnValue(null);
      component.sportConfig = {} as any;
      component['getOddsCardHeader'](events, sportName);

      expect(oddsCardHeaderService.isSpecialEvent).toHaveBeenCalledWith({
        id: '12345',
        markets: [{
          name: 'Goals'
        }]
      }, {});

      expect(oddsCardHeaderService.getHeaderByMarketName).not.toHaveBeenCalled();
      expect(templateService.getMarketViewType).not.toHaveBeenCalled();
      expect(oddsCardHeaderService.getHeaderByViewType).not.toHaveBeenCalled();
    });
  });

  describe('ngOnInit', () => {
    it('should set uuid', () => {
      component.events = [{}] as any;
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      component.ngOnInit();

      expect(coreToolsService.uuid).toHaveBeenCalled();
      expect(component['uniqueId']).toBe('randomUuid');
    });

    it('should hasOutcomeStatusTrue to equal false', () => {
      component.events = undefined as any;
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      component.ngOnInit();

      expect(component.events).toEqual([]);
      expect(component['hasOutcomeStatusTrue']).toEqual(false);
    });

    it('should hasOutcomeStatusTrue to equal true', () => {
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      component.events = [{ outcomeStatus: true }] as any;
      component.ngOnInit();

      expect(component['hasOutcomeStatusTrue']).toEqual(true);
    });

    it('should subscribe to score updates and call initHeader on update if event id matches', () => {
      component.events = [{ id: 1}] as any;
      component['initHeader'] = jasmine.createSpy('initHeader');
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((subId, updateType, updateHandler) => {
        const update = { event: { id: 1 } };

        updateHandler(update);
      });

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddsCardHeader_randomUuid', 'EVENT_SCORES_UPDATE', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddsCardHeader_randomUuid', 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddsCardHeader_randomUuid', 'WS_EVENT_UPDATE', jasmine.any(Function));
      expect(component['initHeader']).toHaveBeenCalledTimes(3);
    });

    it('should subscribe to score updates and not call initHeader on update if event id does not match', () => {
      component.events = [{ id: 2 }] as any;
      component['initHeader'] = jasmine.createSpy('initHeader').and.callThrough();
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((subId, updateType, updateHandler) => {
        const update = { event: { id: 1 } };

        updateHandler(update);
      });

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddsCardHeader_randomUuid', 'EVENT_SCORES_UPDATE', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('oddsCardHeader_randomUuid', 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
      expect(component['cachedEventsIds']).toEqual([2]);
    });

    it('should handle WS_EVENT_UPDATE event', () => {
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === 'WS_EVENT_UPDATE') {
          cb();
        }
      });
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should handle DELETE_EVENT_FROM_CACHE event', () => {
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      component['cachedEventsIds'] = [1];
      pubSubService.subscribe.and.callFake((name, channel, cb) => {
        if (channel === 'DELETE_EVENT_FROM_CACHE') {
          cb(1);
        }
      });
      component.ngOnInit();
      expect(component['cachedEventsIds'].length).toEqual(0);
    });

    it('should get sport config', () => {
      component.events = [{ id: 2 }] as any;
      sportsConfigHelperService.getSportConfigName.and.returnValue('some');
      component.sportConfig = null;
      component['initHeader'] = jasmine.createSpy('initHeader');
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      component.ngOnInit();

      expect(sportsConfigService.getSport).toHaveBeenCalledWith('some');
      expect(component.sportConfig).toBeDefined();
      expect(component['initHeader']).toHaveBeenCalled();
    });

    it('should not get sport config', () => {
      component.events = [{ id: 2 }] as any;
      sportsConfigHelperService.getSportConfigName.and.returnValue('some');
      sportsConfigService.getSport.and.returnValue(of(null));
      component.sportConfig = null;
      component['initHeader'] = jasmine.createSpy('initHeader');
      component['checkDartEventOnlyLeg'] = jasmine.createSpy('checkDartEventOnlyLeg');
      component.ngOnInit();

      expect(sportsConfigService.getSport).toHaveBeenCalledWith('some');
      expect(component.sportConfig).toBeNull();
      expect(component['initHeader']).toHaveBeenCalled();
    });
  });

  describe('#ngOnChanges', () => {
    beforeEach(() => {
      component['initHeader'] = jasmine.createSpy('initHeader').and.callThrough();
    });

    it('should have cachedEventsIds', () => {
      const changes = {
        events: {
          currentValue: 'value',
          previousValue: 'value1'
        }
      };
      component.events = [{ id: 2}] as any;

      component.ngOnChanges(changes as any);

      expect(component['cachedEventsIds']).toEqual([2]);
      expect(component['initHeader']).toHaveBeenCalled();
    });

    it('should call initHeader', () => {
      const changes = {
        events: {
          currentValue: 'value',
          previousValue: 'value'
        },
        undisplayedMarket: {
          currentValue: {
            isDisplayed: false
          }
        }
      };
      component.events = [{ id: 2}] as any;

      component.ngOnChanges(changes as any);

      expect(component['initHeader']).toHaveBeenCalled();
    });

    it('should call initHeader', () => {
      const changes = {
        selectedMarket: 'selectedMarket'
      };
      component.events = [{ id: 2}] as any;

      component.ngOnChanges(changes as any);

      expect(component['initHeader']).toHaveBeenCalled();
    });
  });

  it('should unsubscribe from pubSub', () => {
    component['uniqueId'] = '123';
    component['sportsConfigSubscription'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;

    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('oddsCardHeader_123');
    expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('@setOddCardHeaderType', () => {
    const events = [{}] as any,
      oddsCardHeader = 'oddsCardHeader';

    component['setOddCardHeaderType'](events, oddsCardHeader);

    expect(events[0].oddsCardHeaderType).toEqual(oddsCardHeader);
  });
  it('@getHeader', () => {
    expect(component.getHeader('60 Minute Betting')).toEqual('60 Min');
    expect(component.getHeader('Match Result')).toEqual('Match Result');
  });

  it('when multiMarket template is true', () => {
    component.sportConfig = {
      isFootball: true,
      config: {
        request: {
          categoryId: '16'
        }
      }
    } as any;
    component.selectedMarket = 'Match Result,Total Points,Handicap Betting';
    component.events = [{ isFinished: false, 
      markets: [
        {
          hidden: false,
          templateMarketName: 'Match Result',
          name: 'Match Result',
          outcomes: []
        },
        {
          hidden: false,
          templateMarketName: 'Total Points',
          name: 'Total Points',
          outcomes: []
        },
        {
          hidden: false,
          templateMarketName: 'Handicap Betting',
          name: 'Handicap Betting',
          outcomes: []
        }
      ], 
      name: 'Soderberg/Gagli/Porteous' }] as any;
    component['initHeader']();
    expect(component.showOddsCardHeader).toBe(true);
  });
});
