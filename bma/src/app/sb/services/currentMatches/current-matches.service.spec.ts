import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';

describe('#CurrentMatchesService', () => {
  let service: CurrentMatchesService;

  let templateService;
  let filtersService;
  let cacheEventsService;
  let siteServerService;
  let eventService;
  let timeService;
  let routingHelperService;
  let channelService;
  let pubSubService;

  const ssClasses = [{
    class: {
      categoryCode: 'FOOTBALL',
      categoryDisplayOrder: '-10001',
      categoryId: '16',
      categoryName: 'Football',
      classSortCode: 'FB',
      classStatusCode: 'A',
      displayOrder: '0',
      hasLiveNowOrFutureEvent: 'true',
      hasOpenEvent: 'true',
      id: '87',
      isActive: 'true',
      name: 'Football Colombia',
      responseCreationTime: '2019-02-13T11:29:11.438Z',
      siteChannels: 'P,Q,C,U,I,M,'
    }
  }];

  const ssTypesByClasses = [{
    class: {
      categoryCode: 'FOOTBALL',
      categoryDisplayOrder: '-10001',
      categoryId: '16',
      categoryName: 'Football',
      children: [{
        type: {
          cashoutAvail: 'Y',
          classId: '97',
          displayOrder: '-32000',
          hasLiveNowOrFutureEvent: 'true',
          hasOpenEvent: 'true',
          id: '442',
          isActive: 'true',
          name: 'Premier League',
          siteChannels: 'P,Q,C,U,I,M,',
          typeFlagCodes: 'RD,IVA,',
          typeStatusCode: 'A'
        }
      }],
      classSortCode: 'FB',
      classStatusCode: 'A',
      displayOrder: '0',
      hasLiveNowOrFutureEvent: 'true',
      hasOpenEvent: 'true',
      id: '87',
      isActive: 'true',
      name: 'Football Colombia',
      responseCreationTime: '2019-02-13T11:29:11.438Z',
      siteChannels: 'P,Q,C,U,I,M,'
    }
  }];

  const sportConfig = {
    config: {
      request: {
        marketTemplateMarketNameIntersects: '',
        categoryId: '16'
      }
    }
  };

  beforeEach(() => {
    cacheEventsService = {
      clearByName: jasmine.createSpy('clearByName')
    };
    siteServerService = {
      getClasses: jasmine.createSpy('getClasses').and.returnValue(Promise.resolve(ssClasses)),
      getTypesByClasses: jasmine.createSpy('getTypesByClasses').and.returnValue(
        Promise.resolve(ssTypesByClasses))
    };
    templateService = {
      filterBetInRunMarkets: jasmine.createSpy('filterBetInRunMarkets'),
      filterMultiplesEvents: jasmine.createSpy('filterMultiplesEvents'),
      addIconsToEvents: jasmine.createSpy('addIconsToEvents'),
      getCorrectedOutcomeMeaningMinorCode: jasmine.createSpy('getCorrectedOutcomeMeaningMinorCode').and.returnValue('CD'),
      getEventCorectedDay: jasmine.createSpy('getEventCorectedDay').and.returnValue('sb.today')
    };
    eventService = {
      eventsByTypeIds: jasmine.createSpy('eventsByTypeIds').and.returnValue(Promise.resolve([{
        id: '123'
      }])),
      eventsByTypeWithMarketCounts: jasmine.createSpy('eventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]))
    };
    timeService = {
      getSuspendAtTime: jasmine.createSpy('getSuspendAtTime').and.returnValue('suspendAtTime')
    };
    routingHelperService = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart').and.returnValue('teamA')
    };
    channelService = {
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish:  jasmine.createSpy('publish')
    };
    filtersService = {
      initialClassIds: jasmine.createSpy('initialClassIds').and.returnValue([]),
      clearSportClassName: jasmine.createSpy('clearSportClassName')
    };

    service = new CurrentMatchesService(
      cacheEventsService,
      siteServerService,
      filtersService,
      eventService,
      timeService,
      templateService,
      routingHelperService,
      channelService,
      pubSubService
      );
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  describe('#getTypeEventsByClassName', () => {
    const eventQuickSwitch = true;
    it('Should call getTypeEventsByClassName method for football', () => {
      service.getTypeEventsByClassName('typeName', 'className', sportConfig, eventQuickSwitch).then(() => {
        expect(siteServerService.getClasses).toHaveBeenCalledWith('16');
      }).catch(() => {});
    });

    it('should throw error if no events found', () => {
      service.getTypesForClasses = jasmine.createSpy('getTypesForClasses').and.returnValue(Promise.resolve([]));
      service.getTypeEventsByClassName('typeName', 'className', sportConfig, eventQuickSwitch)
        .then()
        .catch((error) => {
          expect(error).toEqual({ noEventsFound: true });
        });
    });

    it('should get type', () => {
      const type = {
        type: {
          id: 'typeId',
          name: 'typeName'
        }
      };

      service.checkIfEqual = jasmine.createSpy('checkIfEqual').and.returnValue(true);
      service.getEventsByTypeWithMarketCounts = jasmine.createSpy('getEventsByTypeWithMarketCounts').and.returnValue(Promise.resolve([]));
      service.getTypesForClasses = jasmine.createSpy('getTypesForClasses').and.returnValue(Promise.resolve([type]));

      service.getTypeEventsByClassName('typeName', 'className', sportConfig, eventQuickSwitch)
        .then(() => {
          expect(service.checkIfEqual).toHaveBeenCalledWith('typeName', 'typeName');
          expect(service.getEventsByTypeWithMarketCounts).toHaveBeenCalledWith('typeId', sportConfig, eventQuickSwitch);
        })
        .catch((error) => {
          expect(error).toBeUndefined();
        });
    });
  });

  describe('#getOtherClasses', () => {
    it('Should call getOtherClasses method for football', () => {
      service.getOtherClasses(['1', '2'], 'categoryId');

      expect(siteServerService.getClasses).toHaveBeenCalledWith('categoryId');
    });
  });

  describe('#getAllClasses', () => {
    it('Should call getAllClasses method for football', () => {
      service.getAllClasses();

      expect(siteServerService.getClasses).toHaveBeenCalledWith('16');
    });

    it('Should call getAllClasses method for other sports', () => {
      service.getAllClasses('34');

      expect(siteServerService.getClasses).toHaveBeenCalledWith('34');
    });
  });

  describe('#getClassIdsByName', () => {
    it('Should call getClassIdsByName method for othet category ids', () => {
      service.getClassIdsByName('name', 'categoryId');

      expect(siteServerService.getClasses).toHaveBeenCalledWith('categoryId');
    });

    it('Should call getClassIdsByName method for football', () => {
      service.getClassIdsByName('name');

      expect(siteServerService.getClasses).toHaveBeenCalledWith('16');
    });

    it('Should call getClassIdsByName method for football', () => {
      siteServerService.getClasses.and.returnValue(Promise.resolve([]));

      service.getClassIdsByName('name').then(data => {
        expect(data).toEqual(undefined);
      });
    });
  });

  describe('#getOutrights', () => {
    it('Should call getOutrights method', () => {
      service.getOutrights('typeId', 'categoryId');

      expect(eventService.eventsByTypeIds).toHaveBeenCalledWith({
        eventSortCode: jasmine.any(String), // long string
        typeId: 'typeId',
        categoryId: 'categoryId',
        siteChannels: 'M',
        suspendAtTime: 'suspendAtTime'
      });
      expect(timeService.getSuspendAtTime).toHaveBeenCalled();
    });

    it('Should call getOutrights method for football only', () => {
      service.getOutrights('typeId');

      expect(eventService.eventsByTypeIds).toHaveBeenCalledWith({
        eventSortCode: jasmine.any(String), // long string
        typeId: 'typeId',
        categoryId: '16',
        siteChannels: 'M',
        suspendAtTime: 'suspendAtTime'
      });
      expect(timeService.getSuspendAtTime).toHaveBeenCalled();
    });
  });

  describe('#getTypesForClasses', () => {
    it('Should call getTypesForClasses method', () => {
      service.getTypesForClasses('className', 'categoryId').then(() => {
        expect(siteServerService.getClasses).toHaveBeenCalled();
      }).catch(() => {});
    });

    it('should call getTypesForClasses with specified this', () => {
      siteServerService.getTypesByClasses.call = jasmine.createSpy('siteServerService.getTypesByClasses.call');
      service.getClassIdsByName = jasmine.createSpy('getClassIdsByName').and.returnValue(Promise.resolve([{}]));

      service.getTypesForClasses('className', 'categoryId').then(() => {
        expect(siteServerService.getClasses.call).toHaveBeenCalledWith(siteServerService, [{}]);
      }).catch(() => {});
    });

    it('should catch error', () => {
      service.getClassIdsByName = jasmine.createSpy('getClassIdsByName').and.returnValue(Promise.resolve(null));

      service.getTypesForClasses('className', 'categoryId')
        .then(() => {})
        .catch((error) => {
          expect(error).toEqual({ noEventsFound: true });
        });
    });
  });

  describe('#getClassToSubTypeForClass', () => {
    it('Should call getClassToSubTypeForClass method', (done: DoneFn) => {
      service.getClassToSubTypeForClass('15').subscribe(data => {
        expect(siteServerService.getTypesByClasses).toHaveBeenCalledWith([15]);
        expect(data).toEqual(ssTypesByClasses[0].class.children as any);
        done();
      });
    });
  });

  describe('#getEventsByTypeWithMarketCounts', () => {
    it('should call eventsByTypeWithMarketCounts with params', () => {
      const params = {
        noEventSortCodes: 'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20',
        typeId: '1',
        marketsCount: true,
        childCount: true,
        dispSortName: undefined,
        dispSortNameIncludeOnly: undefined,
        marketTemplateMarketNameIntersects: ''
      };
      sportConfig.config.request.categoryId = '10';
      service.getEventsByTypeWithMarketCounts('1', sportConfig);

      expect(eventService.eventsByTypeWithMarketCounts).toHaveBeenCalledWith(params);
    });

    it('should call eventsByTypeWithMarketCounts with params for Football', () => {
      const params = {
        noEventSortCodes: 'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20',
        typeId: '1',
        marketsCount: true,
        childCount: true,
        competitionTemplateMarketNameOnlyIntersects: true
      };
      sportConfig.config.request.categoryId = '16';
      service.getEventsByTypeWithMarketCounts('1', sportConfig);

      expect(eventService.eventsByTypeWithMarketCounts).toHaveBeenCalledWith(params);
    });
  });
  it('should call eventsByTypeWithMarketCounts with params for quickswitch', () => {
    const params = {
      noEventSortCodes: 'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20',
      typeId: '1',
      marketsCount: true,
      childCount: true,
      competitionTemplateMarketName: true
    };
    sportConfig.config.request.categoryId = '16';
    const eventQuickSwitch = true;
    service.getEventsByTypeWithMarketCounts('1', sportConfig, eventQuickSwitch);

    expect(eventService.eventsByTypeWithMarketCounts).toHaveBeenCalledWith(params);
  });

  describe('getTypeIdFromClasses', () => {
    it('should return classItem id', () => {
      service.classCache = [{
        class: {
          id: 'classId',
          originalName: 'originalName'
        }
      }] as any;

      expect(service.getTypeIdFromClasses('originalName', [])).toEqual('classId');
    });

    it('should return empty class id', () => {
      service.classCache = [];

      expect(service.getTypeIdFromClasses('originalName', [])).toBeUndefined();
    });
  });

  it('#unSubscribeForUpdates', () => {
    service.unSubscribeForUpdates();
    expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'current-matches');
  });

  it('#subscribeForUpdates', () => {
    const events = <any>[{}];
    const channel = ['sEVENT1'];
    channelService.getLSChannelsFromArray.and.returnValue(channel);

    service.subscribeForUpdates(events);

    expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(events, true, true);
    expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', { channel, module: 'current-matches' });
  });

  it('#getFootballClasses', () => {
    service.getFootballClasses(['16', '2']).then(data => {
      expect(data.length).toEqual(2);
    }).catch(() => {});
  });

  it('#getMatchNextGoalsAmount', () => {
    expect(service.getMatchNextGoalsAmount('mrketName1')).toEqual(1);
    expect(service.getMatchNextGoalsAmount('mrketName')).toEqual(undefined);
  });

  it('#parseTemplateMarketNames', () => {
    const eventEntity = <any>{
      markets: [
        {
          templateMarketName: 'Next Team to Score',
          name: 'Score1'
        },
        {
          templateMarketName: 'Next Score',
          name: 'Score'
        }
      ]
    };
    service.parseTemplateMarketNames(eventEntity);

    expect(eventEntity.markets[0].nextScore).toEqual(1);
    expect(eventEntity.markets[1].nextScore).toEqual(undefined);
  });

  it('#applyTemplateProperties', () => {
    const eventsArray = <any>[
      {
        isUS: true,
        markets: [{ outcomes: [{}] }]
      },
      {
        isUS: false,
        markets: [{ outcomes: [{}] }]
      }
    ];
    expect(service.applyTemplateProperties(eventsArray)[0].markets[0].outcomes[0].isUS).toEqual(true);
    expect(service.applyTemplateProperties(eventsArray)[1].markets[0].outcomes[0].isUS).toEqual(false);
  });
});
