import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { SingleSportSectionComponent } from '@ladbrokesDesktop/inPlay/components/singleSportSection/single-sport-section.component';
import { EVENT_TYPES } from '@app/inPlay/constants/event-types.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';

describe('LDSingleSportSectionComponent', () => {
  let component: SingleSportSectionComponent;
  let pubSubService;
  let inPlayMainService;
  let coreToolService;
  let sportsConfigService;
  let windowRef;
  let changeDetectorRef;
  let cmsService;
  const competitionEvents = [{
    cashoutAvail: 'cashoutAvail',
    categoryCode: 'categoryCode',
    categoryId: 'categoryId',
    categoryName: 'categoryName',
    displayOrder: 'displayOrder',
    drilldownTagNames: 'drilldownTagNames',
    eventIsLive: 'eventIsLive',
    eventSortCode: 'eventSortCode',
    eventStatusCode: 'eventStatusCode',
    id: 123
  }];
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
    inPlayMainService = {
      unsubscribeForSportCompetitionUpdates: jasmine.createSpy(),
      unsubscribeForEventsUpdates: jasmine.createSpy(),
      _getCompetitionData: jasmine.createSpy().and.returnValue(observableOf(competitionEvents)),
      getTopLevelTypeParameter: jasmine.createSpy().and.returnValue(EVENT_TYPES.LIVE_EVENT),
      subscribeForUpdates: jasmine.createSpy(),
      isCashoutAvailable: jasmine.createSpy().and.returnValue(true),
      clearDeletedEventFromType: jasmine.createSpy('clearDeletedEventFromType'),
      getSportName: jasmine.createSpy('getSportName').and.returnValue('football'),
      unsubscribeForEventUpdates : jasmine.createSpy('unsubscribeForEventUpdates'),
      checkAggregateMarkets(requestParams, competition, competitionEvents) {
        const aggregated = requestParams['marketSelector'] && requestParams['marketSelector'].split(',').length > 1;
        if(aggregated){
          const eventsList = [];
          competition.eventsIds.forEach(event => {
            const commonEvent = competitionEvents.filter(ev => ev.id == event);
            const marketsList = commonEvent.map(b => b.markets[0]);
            marketsList.forEach(market => {
              market.name = requestParams.marketSelector;
            });
            commonEvent[0].markets = marketsList;
            eventsList.push(commonEvent[0]);
          });
          return competition.events = eventsList;
        }
        else {
          return competition.events = competitionEvents;
        }
      }
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => {
        switch (b) {
          case 'INPLAY_COMPETITION_REMOVED:34:LIVE_EVENT':
            cb();
            break;
          case 'INPLAY_COMPETITION_UPDATED:34:LIVE_EVENT':
            cb();
            break;  
          case 'INPLAY_COMPETITION_ADDED:34:LIVE_EVENT':
            cb([]);
            break;
          default:
            break;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    coreToolService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('UUID')
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf(expectedSportConfig))
    };

    cmsService = {
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(observableOf(Boolean))
    };

    component = new SingleSportSectionComponent(
      inPlayMainService,
      pubSubService,
      windowRef,
      changeDetectorRef,
      coreToolService,
      sportsConfigService,
      cmsService
    );

    component.eventsBySports = {
      categoryId: '34',
      eventsByTypeName: [],
      marketSelector: 'To Qualify',
      marketSelectorOptions: ['Main markets', 'Match Betting']
    } as any;

    component.reloadData.emit = jasmine.createSpy('reloadData.emit');

    component['CATEGORIES_DATA'] = {
      gaming: {
        football: {
          id: 16
        }
      },
      tierOne: ['16', '34', '6']
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(SingleSportSectionComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('#ngOnInit', () => {
    it(`should define categoryId and topLevelType`, () => {
      component.ngOnInit();

      expect(component.categoryId).toEqual('34');
      expect(component.topLevelType).toEqual(EVENT_TYPES.LIVE_EVENT);
    });

    it('ngOnInit', () => {
      component.setExpandedFlags = jasmine.createSpy();
      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(5);
      expect(component.setExpandedFlags).toHaveBeenCalled();
    });

    it('should subscribe for updates and set addedCompetition isExpanded to true', () => {
      let inplayCompetitionHandler;
      const eventsByTypeName = [{
        showCashoutIcon: false,
        typeId: 1
      }
      ] as any;
      const addedCompetitions = {typeId: 1, events: [], isExpanded: false};

      pubSubService.subscribe.and.callFake((name, method, cb) => {
        if (method === 'INPLAY_COMPETITION_ADDED:34:LIVE_EVENT') {
          inplayCompetitionHandler = cb;
        }
      });
      component.ngOnInit();
      component.eventsBySports.eventsByTypeName = eventsByTypeName;
      component.expandedLeaguesCount = undefined;

      inplayCompetitionHandler(addedCompetitions);

      expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith([]);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(addedCompetitions.isExpanded).toBeTruthy();
      expect(eventsByTypeName[0].showCashoutIcon).toBeTruthy();
    });

    it('Should fetch event when live inplay event gets triggered', () => {
      let handler;
      pubSubService.subscribe.and.callFake((subscriber, method, cb) => {
        if (method === `WS_EVENT_LIVE_UPDATE`) {
          handler = cb;
        }
      });
      component.ngOnInit();
      handler();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('inplaySectionLiveUpdate',pubSubApi.WS_EVENT_LIVE_UPDATE, jasmine.any(Function));
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should filter "Enhanced Multiples" type if eventsBySports exist', () => {
      component.eventsBySports.eventsByTypeName = [{
        typeName: 'English Football',
      }, {
        typeName: 'Enhanced Multiples'
      }] as any;
      component.ngOnInit();

      expect(component.eventsBySports.eventsByTypeName).toEqual([{
        typeName: 'English Football',
        showCashoutIcon: true
      }] as any);
    });

    it('ngOnInit case INPLAY_COMPETITION_REMOVED with market selector', () => {
      component.isMarketSelectorVisible = jasmine.createSpy('isMarketSelectorVisible').and.returnValue(true);
      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(5);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.reloadData.emit).toHaveBeenCalledWith({
        useCache: false,
        additionalParams: {
          marketSelector: 'Main markets'
        }
      });
    });

    it('ngOnInit case INPLAY_COMPETITION_REMOVED without market selector', () => {
      component.isMarketSelectorVisible = jasmine.createSpy('isMarketSelectorVisible').and.returnValue(false);
      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(5);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.reloadData.emit).not.toHaveBeenCalled();
    });

    it('ngOnInit case INPLAY_COMPETITION_UPDATED', () => {
      spyOn(component,'setExpandedFlags');
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(5);
      expect(component.expandedFlags).toBeDefined();
      expect(component.setExpandedFlags).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should filter "Enhanced Multiples" type if eventsBySports exist', () => {
      component.eventsBySports = {} as any;
      component.ngOnInit();
      expect(component.eventsBySports).toEqual({} as any);

      component.eventsBySports.eventsByTypeName = [];
      component.ngOnInit();
      expect(component.eventsBySports.eventsByTypeName).toEqual([]);

      component.eventsBySports.eventsByTypeName = [{
        typeName: 'English Football',
      }, {
        typeName: 'Enhanced Multiples'
      }] as any;
      component.ngOnInit();

      expect(component.eventsBySports.eventsByTypeName).toEqual([{
        typeName: 'English Football',
        showCashoutIcon: true
      }] as any);
    });

    it('should delete event from data structure', () => {
      component.eventsBySports = {
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: []
      } as any;
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (b === pubSubService.API.DELETE_EVENT_FROM_CACHE) {
          cb(1);
        }
      });

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'inplay-single-sport_UUID',
        pubSubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(inPlayMainService.clearDeletedEventFromType).toHaveBeenCalledWith({
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: []
      }, 1);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  it('reloadSportData', () => {
    component.expandedFlags = {};
    const options = {
      useCache: true,
      additionalParams: {
        topLevelType: 'type',
        categoryId: 'id'
      }
    } as any;
    component.reloadSportData(options);

    expect(component.reloadData.emit).toHaveBeenCalledWith(options);
  });

  describe('#setExpandedFlags', () => {
    it('should update expandedFlags object & set true for showCashoutIcon field of eventsByTypeName', () => {
      component.expandedLeaguesCount = 4;
      component.expandedFlags = {
        1: undefined,
        2: undefined,
        3: undefined
      };
      component.eventsBySports = {
        eventsByTypeName: [
          {
            showCashoutIcon: false,
            typeId: 1
          },
          {
            showCashoutIcon: false,
            typeId: 2
          },
          {
            showCashoutIcon: false,
            typeId: 3
          }
        ]
      } as any;
      const expandedFlagsResult = {
        1: true,
        2: true,
        3: true
      };
      component.setExpandedFlags();

      component.eventsBySports.eventsByTypeName.forEach((competitionSection) => expect(competitionSection.showCashoutIcon).toBeTruthy);
      expect(component.expandedFlags).toEqual(expandedFlagsResult);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not update expandedFlags', () => {
      component.expandedFlags = {
        1: undefined,
        2: undefined,
        3: undefined
      };
      const expandedFlagsResult = {
        1: undefined,
        2: undefined,
        3: undefined
      };
      component.setExpandedFlags();

      expect(component.expandedFlags).toEqual(expandedFlagsResult);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  describe('#setExpandedFlags for HR', () => {
    let competitionSection;
    beforeEach(() => {
      competitionSection = {
        typeId: '123',
        events:[{id:'1234', startTime:'123', markets:[{id:'market1'}]}]
      } as any;
    });
    it('should set expandedFlag - true', () => {
      component.expandedFlags['1234'] = false;
      component['liveLabel'] = true;
      component['isHR'] = true;
      component.expandedLeaguesCount = 2;
      component['eventsBySports'] = {eventsByTypeName:[{
        typeId: '123',
        events:[{id:'1234', startTime:'123', markets:[{id:'market1'}]}, { id: '12345', startTime: '1234', markets:[{id:'market2'}] }]
      }]as any} as any;
      component['HREvents'] =[{id:'1234', startTime:'123', markets:[{id:'market1'}]}];
      component['setExpandedFlags']();
      expect(component.expandedFlags['1234']).toBe(true);
      expect(component.eventsBySports.eventsByTypeName[0].events[0].isExpanded).toBe(true);
      expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith([jasmine.any(Object)]);
    });
    it('should not process HR', () => {
      component['isHR'] = true;
      component['eventsBySports'] = {eventsByTypeName:[{
        typeId: '123',
        events: null
      }]as any} as any;      
      component['setExpandedFlags']();
      expect(component['HREvents']).toEqual([]);
    });
  });

  describe('#initMarketSelector', () => {
    it('should call markForCheck on market selector init', fakeAsync(() => {
      component.initMarketSelector();
      tick(1000);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));
  });

  describe('#toggleCompetitionSection', () => {
    it('should test toggling of expand/collapse state of league section', fakeAsync(() => {
      const competitionSection = {
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = [
        {
          typeId: '01',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        },
        {
          typeId: '02',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        }
      ] as any[];
      component.expandedFlags = {
        '01': false,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': false,
        '02': false
      };
      component.eventsBySports = {
        categoryCode: '01',
        categoryId: '02'
      } as any;
      component.filter = 'live';
      const requestParams = {
        categoryId: component.eventsBySports.categoryId,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        typeId: competitionSection.typeId,
        modifyMainMarkets: true
      };

      component.toggleCompetitionSection(competitionSection, sectionsArray);

      expect(component.competitionRequestInProcessFlags['01']).toBeFalsy();
      inPlayMainService._getCompetitionData(requestParams, component.eventsBySports.categoryCode)
        .subscribe((competition) => {
          expect(component.competitionRequestInProcessFlags[competitionSection.typeId]).toBeFalsy();
          expect(competitionSection.events).toEqual(competition);
          expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith(competitionSection.events);
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
      tick();
    }));

    it('should not toggle competition section if isRequestInProcess', () => {
      component.competitionRequestInProcessFlags = {1: true};
      const actualResult = component.toggleCompetitionSection({typeId: '1'} as ITypeSegment, []);

      expect(actualResult).toBeFalsy();
      expect(inPlayMainService._getCompetitionData).not.toHaveBeenCalled();
    });

    it('should unsubscribe from event updates', () => {
      const competitionSection = {typeId: '1'} as ITypeSegment;

      component.expandedFlags = {1: true};
      component.competitionRequestInProcessFlags = {1: false};
      component.toggleCompetitionSection(competitionSection, []);

      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalledWith(competitionSection);
    });

    it('should splice sectionArray', () => {
      const competitionSection = {typeId: '1'} as ITypeSegment;

      inPlayMainService._getCompetitionData.and.returnValue(observableOf([]));
      component.expandedFlags = {1: false};
      component.competitionRequestInProcessFlags = {1: false};
      component.toggleCompetitionSection(competitionSection, []);

    });
  });

  describe('#toggleCompetitionSection for HR', () => {
    beforeEach(()=>{
      component.eventsBySports = {
        categoryCode: '01',
        categoryId: '02',
        eventsByTypeName: [{
          showCashoutIcon: false,
          typeId: '01',
          competitionSection: {
            typeId: '01',
            marketSelector: 'marketSelector',
            events: [
              {
                cashoutAvail: 'cashoutAvail',
                categoryCode: 'categoryCode',
                categoryId: 'categoryId'
              }]
          }
        }]
      } as any;
    });
    it('should test toggling of expand/collapse state of league section', fakeAsync(() => {
      component.isHR = true;
      const competitionSection = {
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = 
        {
          typeId: '01',
          id:'01',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        } as any;
      component.expandedFlags = {
        '01': true,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': false,
        '02': false
      };
      component.filter = 'live';
      const requestParams = {
        categoryId: component.eventsBySports.categoryId,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        typeId: competitionSection.typeId,
        modifyMainMarkets: true
      };

      component.toggleCompetitionSection(competitionSection, sectionsArray);
      expect(sectionsArray.isExpanded).toBe(false);

      inPlayMainService._getCompetitionData(requestParams, component.eventsBySports.categoryCode)
        .subscribe((competition) => {
          expect(component.competitionRequestInProcessFlags[competitionSection.typeId]).toBeFalsy();
        });
    }));
    it('should call inPlayMainService.subscribeForUpdates', fakeAsync(() => {
      component.isHR = true;
      const competitionSection = {
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = {
        typeId: '01',
        id: 123,
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId'
      } as any;
      component.isHR = true;
      component.expandedFlags = {
        '00': true,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': false,
        '02': false
      };
      component.filter = 'live';
      const requestParams = {
        categoryId: component.eventsBySports.categoryId,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        typeId: competitionSection.typeId,
        modifyMainMarkets: true
      };
      component.toggleCompetitionSection(competitionSection, sectionsArray);
      inPlayMainService._getCompetitionData(requestParams, component.eventsBySports.categoryCode)
        .subscribe((competition) => {
          expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith([jasmine.any(Object)]);
        });
      tick();
    }));

    it('should not toggle competition section if isRequestInProcess', () => {
      component.isHR = true;
      component.competitionRequestInProcessFlags = {'01': true};
      const actualResult = component.toggleCompetitionSection({typeId: '01'} as ITypeSegment, {typeId: '01'} as any);

      expect(actualResult).toBeFalsy();
      expect(inPlayMainService._getCompetitionData).toHaveBeenCalled();
    });

    it('should unsubscribe from event updates', () => {
      component.isHR = true;
      const competitionSection = {typeId: '01'} as ITypeSegment;

      component.expandedFlags = {'01': true};
      component.competitionRequestInProcessFlags = {'01': false};
      component.toggleCompetitionSection(competitionSection, {typeId:'01',id:'01'} as any);

      expect(inPlayMainService.unsubscribeForEventUpdates).toHaveBeenCalledWith(jasmine.any(Object));
    });
    it('should assign competitionSection if eventId and competitionSection.id', () => {
      const competitionSection = {
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            id: 1,
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = {
        id: 123,
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId'
      } as any;
      component.toggleCompetitionSection(competitionSection, sectionsArray);
      expect(component.expandedFlags[competitionSection.typeId]).toBeTrue();
    });
  });

  it('#isMarketSelectorVisible ', () => {
    component.eventsBySports = {
      categoryId: '16',
      marketSelectorOptions: ['1', '2']
    } as any;
    component.categoryId = '16';
    component.inner = false;
    component.filter = 'livenow';

    const actualResult = component.isMarketSelectorVisible();

    expect(actualResult).toBeTruthy();
  });

  it('#isCashoutAvailable', () => {
    const sportEvents = [
      {
        cashoutAvail: 'cashoutAvail'
      }
    ] as any[];

    const actualResult = component.isCashoutAvailable(sportEvents, true);

    expect(actualResult).toBeTruthy();
  });

  describe('#getSectionTitle', () => {
    const competitionSectionData = {
      typeSectionTitleAllSports: 'all sports title',
      typeSectionTitleOneSport: 'one sport title'
    } as any;

    it('should return: all sports title', () => {
      component.inner = true;

      const actualResult = component.getSectionTitle(competitionSectionData);

      expect(actualResult).toEqual(competitionSectionData.typeSectionTitleAllSports);
    });

    it('should return one sport title', () => {
      component.inner = false;

      const actualResult = component.getSectionTitle(competitionSectionData);

      expect(actualResult).toEqual(competitionSectionData.typeSectionTitleOneSport);
    });
  });

  it('ngOnDestroy: should remove listeners', function () {
    component.eventsBySports = {} as any;
    component.ngOnDestroy();

    expect(inPlayMainService.unsubscribeForSportCompetitionUpdates).toHaveBeenCalledWith(component.eventsBySports);
    expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalledWith(component.eventsBySports);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('inplay-single-sport_UUID');
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('inplaySectionLiveUpdate');
    expect(component.eventsBySports.eventsByTypeName).toEqual([]);
  });

  it('ngOnDestroy: should unsubscribe from marketSwitcherConfig',  () => {
    component['marketSwitcherConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(component['marketSwitcherConfigSubscription'].unsubscribe).toHaveBeenCalled();
  });

  describe('ngOnChanges', () => {
    it('should reset expanded flags',  () => {
      component.setExpandedFlags = jasmine.createSpy('setExpandedFlags');
      component.ngOnChanges({eventsBySports: {}} as any);

      expect(component.setExpandedFlags).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not reset expanded flags', () => {
      component.setExpandedFlags = jasmine.createSpy('setExpandedFlags');
      component.ngOnChanges({});

      expect(component.setExpandedFlags).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });
  });

  it('should return item typeId', () => {
    const actualResult = component.trackByTypeId(1, {typeId: '2'});

    expect(actualResult).toEqual('2');
  });

  it('should return item id', () => {
    const actualResult = component.trackByEventId(1, {id: '2'});

    expect(actualResult).toEqual('21');
  });

  it('should not change the visibility of Cashout Icon', () => {
    component.eventsBySports = {} as ISportSegment;

    const actualResult = component.setExpandedFlags();

    expect(actualResult).toBeUndefined();
  });

  describe('check for isMarketSwitcherConfigured', () => {
    it('should set isMarketSwitcherConfigured to true if cmsService getMarketSwitcherFlagValue return true', () => {
      cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
        .and.callFake((flag) => {
          expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
          flag = true;
          expect(component.isMarketSwitcherConfigured).toBe(true);
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
    });
    it('should set isMarketSwitcherConfigured to false if cmsService getMarketSwitcherFlagValue return false', () => {
      cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
        .and.callFake((flag) => {
          expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
          flag = false;
          expect(component.isMarketSwitcherConfigured).toBe(false);
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
    });
  });
});
