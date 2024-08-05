import { NextRacesService } from '@core/services/racing/nextRaces/next-races.service';

describe('NextRacesService', () => {
  let service: NextRacesService;
  let cacheEventsService;
  let templateService;
  let channelService;
  let pubSubService;

  beforeEach(() => {
    cacheEventsService = {
      stored: jasmine.createSpy()
    };
    templateService = {};
    channelService = {
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue([])
    };
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };
    service = new NextRacesService(
      <any>cacheEventsService,
      <any>templateService,
      <any>channelService,
      <any>pubSubService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service.cacheKey).toEqual('nextRaces');
  });

  describe('getNextRacesModuleConfig', () => {
    let moduleName, cmsConfig, expectedStrictConfig, expectedDynamicConfig;

    beforeEach(() => {
      service.racingData = {
        horseracing: { id: 21 },
        greyhound: { id: 19 }
      };

      cmsConfig = {
        NextRaces: {
          title: 'Next Races',
          isInUK: 'Yes',
          isIrish: 'Yes',
          isInternational: 'Yes',
          showPricedOnly: 'No',
          numberOfEvents: '10',
          numberOfSelections: '3',
          typeID: '123',
          typeDateRange: {
            from: 'from',
            to: 'to'
          },
          isVirtualRacesEnabled: "No"
        },
        GreyhoundNextRaces: {
          numberOfEvents: '4',
          numberOfSelections: '4',
          isVirtualRacesEnabled: "No"
        },
        RacingDataHub: {
          isEnabledForGreyhound: true,
          isEnabledForHorseRacing: true,
        }
      };

      expectedStrictConfig = {
        siteChannels: 'M',
        excludeUnnamedFavourites: true,
        templateMarketNameOnlyEquals: '|Win or Each Way|',
        isActive: true,
        eventStatusCode: 'A',
        outcomeStatusCode: 'A',
        marketStatusCodeExists: 'A',
        marketStatusCode: 'A',
        date: 'nextFour',
        priceHistory: true,
        isRawIsOffCodeNotY: true,
        hasOpenEvent: 'true'
      };
    });

    describe('for HR event should return configuration object combined from Strict config and HR NextRaces config', () => {
      beforeEach(() => {
        moduleName = 'horseracing';
        expectedStrictConfig.categoryId = 21;
        expectedDynamicConfig = {
          racingFormOutcome: false,
          typeId: '123',
          limitOutcomesCount: 3,
          siteServerEventsCount: 12,
          eventsCount: 10,
          startTime: 'from',
          endTime: 'to'
        };
      });

      it('when RacingPost is enabled and typeID is provided', () => { /* as it is */ });
      it('when RacingPost is disabled', () => {
        cmsConfig.RacingDataHub.isEnabledForHorseRacing = false;
        expectedDynamicConfig.racingFormOutcome = true;
      });
      it('when RacingPost is missing', () => {
        delete cmsConfig.RacingDataHub;
        expectedDynamicConfig.racingFormOutcome = true;
      });

      describe('when typeID is not provided', () => {
        beforeEach(() => {
          delete cmsConfig.NextRaces.typeID;
          delete expectedDynamicConfig.typeId;
          jasmine.clock().mockDate(new Date('2017-11-07T16:45:00.000Z'));
          expectedDynamicConfig.startTime = '2017-11-07T15:45:00.000Z';
          expectedDynamicConfig.endTime = '2017-11-08T16:45:00.000Z';
        });
        it('with all flags available', () => {
          expectedDynamicConfig.typeFlagCodes = 'UK,IE,INT';
        });
        it('with all flags disabled', () => {
          cmsConfig.NextRaces.isInUK = 'No';
          cmsConfig.NextRaces.isIrish = 'No';
          cmsConfig.NextRaces.isInternational = 'No';
          expectedDynamicConfig.typeFlagCodes = '';
        });
      });

      it('when NextRaces.showPricedOnly is Yes', () => {
        cmsConfig.NextRaces.showPricedOnly = 'Yes';
        expectedDynamicConfig.priceTypeCodesExists = 'LP';
      });

      it('when NextRaces.numberOfSelections is provided as number', () => {
        cmsConfig.NextRaces.numberOfSelections = 5;
        expectedDynamicConfig.limitOutcomesCount = 5;
      });

      describe('for different values of NextRaces.numberOfSelections', () => {
        describe('should equal 3 for value<=3', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 3; });
          it('for string 3', () => { cmsConfig.NextRaces.numberOfEvents = '3'; });
          it('for number 3', () => { cmsConfig.NextRaces.numberOfEvents = 3; });
          it('for string 2', () => { cmsConfig.NextRaces.numberOfEvents = '2'; });
          it('for number 2', () => { cmsConfig.NextRaces.numberOfEvents = 2; });
        });
        describe('should equal 5 for 3<value<=5', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 5; });
          it('for string 5', () => { cmsConfig.NextRaces.numberOfEvents = '5'; });
          it('for number 5', () => { cmsConfig.NextRaces.numberOfEvents = 5; });
          it('for string 4', () => { cmsConfig.NextRaces.numberOfEvents = '4'; });
          it('for number 4', () => { cmsConfig.NextRaces.numberOfEvents = 4; });
        });
        describe('should equal 5 for 5<value<=7', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 7; });
          it('for string 7', () => { cmsConfig.NextRaces.numberOfEvents = '7'; });
          it('for number 7', () => { cmsConfig.NextRaces.numberOfEvents = 7; });
          it('for string 6', () => { cmsConfig.NextRaces.numberOfEvents = '6'; });
          it('for number 6', () => { cmsConfig.NextRaces.numberOfEvents = 6; });
        });
        describe('should equal 12 for 7<value', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 12; });
          it('for string 8', () => { cmsConfig.NextRaces.numberOfEvents = '8'; });
          it('for number 8', () => { cmsConfig.NextRaces.numberOfEvents = 8; });
        });
        afterEach(() => { expectedDynamicConfig.eventsCount = Number(cmsConfig.NextRaces.numberOfEvents); });
      });
    });

    describe('for GH event should return configuration object combined from Strict config and GH NextRaces config', () => {
      beforeEach(() => {
        moduleName = 'greyhound';
        expectedStrictConfig.categoryId = 19;
        expectedDynamicConfig = {
          racingFormOutcome: false,
          siteServerEventsCount: 5,
          eventsCount: 4,
          priceTypeCodes: 'SP,LP',
          limitOutcomesCount: 4,
          typeFlagCodes: 'NE',
          hasOpenEvent: 'true'
        };
      });

      it('when RacingPost is enabled', () => { /* as it is */ });
      it('when RacingPost is disabled for GH', () => {
        cmsConfig.RacingDataHub.isEnabledForGreyhound = false;
        expectedDynamicConfig.racingFormOutcome = true;
      });
      it('when RacingPost is missing', () => {
        delete cmsConfig.RacingDataHub;
        expectedDynamicConfig.racingFormOutcome = true;
      });
    });
    afterEach(() => {
      expect(service.getNextRacesModuleConfig(moduleName, cmsConfig)).toEqual({
        ...expectedStrictConfig, ...expectedDynamicConfig
      });
    });
  });

  describe('getEventsFromCache', () => {
    it('should get cached events', () => {
      service['getEventsFromCache']('horseracing');
      expect(cacheEventsService.stored).toHaveBeenCalledWith(service['cacheKey'], 'nextFour', '21');
    });
  });

  describe('subscribeForUpdates', () => {
    it('subscribeForUpdates !channels', () => {
      const event = <any>{};
      expect(service.subscribeForUpdates([event])).toEqual('');
      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith([event]);
    });

    it('subscribeForUpdates channels', () => {
      const event = <any>{};
      channelService.getLSChannelsFromArray.and.returnValue(['CH1']);
      expect(service.subscribeForUpdates([event]).indexOf('next-races') > -1).toEqual(true);
    });
  });

  describe('unSubscribeForUpdates', () => {
    it('unSubscribeForUpdates !subscriptionId', () => {
      service.unSubscribeForUpdates(null);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('unSubscribeForUpdates subscriptionId', () => {
      service.unSubscribeForUpdates('1');
      expect(pubSubService.publish).toHaveBeenCalled();
    });
  });

  it('getGHNextRacesModuleConfigCMS when cmsConfig is undefined', () => {
    const filterParam = {
      racingFormOutcome: true,
      siteServerEventsCount: 5,
      priceTypeCodes: 'SP,LP',
      typeFlagCodes: 'NE',
      eventsCount: 4,
      limitOutcomesCount: 4,
      templateMarketNameOnlyEquals: '|Win or Each Way|'
    };
    expect(service['getGHNextRacesModuleConfigCMS'](undefined)).toEqual(filterParam);
  });

  it('getGHNextRacesModuleConfigCMS', () => {
    const config = {
      RacingDataHub: {
        isEnabledForGreyhound: true
      },
      GreyhoundNextRaces: {
        numberOfEvents: 7,
        numberOfSelections: 3
      }
    } as any;
    const filterParam = {
      racingFormOutcome: false,
      siteServerEventsCount: 7,
      priceTypeCodes: 'SP,LP',
      typeFlagCodes: 'NE',
      eventsCount: 7,
      limitOutcomesCount: 3,
      templateMarketNameOnlyEquals: '|Win or Each Way|'
    };
    expect(service['getGHNextRacesModuleConfigCMS'](config)).toEqual(filterParam);
  });

  describe('getNextRacesModuleConfig when virtuals', () => {
    let moduleName, cmsConfig;

    beforeEach(() => {
      service.racingData = {
        horseracing: { id: 39 },
        greyhound: { id: 39 }
      };

      cmsConfig = {
        NextRaces: {
          title: 'Next Races',
          isInUK: 'Yes',
          isIrish: 'Yes',
          isInternational: 'Yes',
          showPricedOnly: 'No',
          numberOfEvents: '10',
          numberOfSelections: '3',
          isVirtualRacesEnabled: "Yes",
          virtualRacesIncluded: [
            "Surrey Downs",
          ],
          virtualRacesDateRange: {
            from: "2023-02-25T12:19:00+05:30",
            to: "2023-02-25T12:25:00+05:30"
          }
        },
        GreyhoundNextRaces: {
          numberOfEvents: '4',
          numberOfSelections: '4',
          isVirtualRacesEnabled: "Yes",
          virtualRacesIncluded: [
            "Barking hall",
          ],
          virtualRacesDateRange: {
            from: "2023-02-25T12:19:00+05:30",
            to: "2023-02-25T12:25:00+05:30"
          }
        }
      };
    });

    describe('for HR event should return configuration object combined from HR NextRaces config', () => {

      beforeEach(() => {
        moduleName = 'horseracing';
      });

      it('HR Module getNextRacesModuleConfig', () => {
        const output = {
          "categoryId": 39,
          "siteChannels": "M",
          "excludeUnnamedFavourites": true,
          "isActive": true,
          "eventStatusCode": "A",
          "outcomeStatusCode": "A",
          "marketStatusCodeExists": "A",
          "marketStatusCode": "A",
          "date": "nextFour",
          "priceHistory": true,
          "isRawIsOffCodeNotY": true,
          "hasOpenEvent": "true",
          "marketTemplateMarketNameIntersects": "|Win or Each Way|,|Win or each way|,|To-Win|,|Win|,|Win or EW|",
          "typeFlagCodes": "UK,IE,INT,VR",
          "racingFormOutcome": true,
          "limitOutcomesCount": 3,
          "siteServerEventsCount": 12,
          "eventsCount": 10,
          "startTime": "2017-11-07T15:45:00.000Z",
          "endTime": "2017-11-08T16:45:00.000Z",
          "isVirtualRacesEnabled": true,
          "virtualRacesIncluded": [
            "Surrey Downs"
          ],
        }

        expect(service.getNextRacesModuleConfig(moduleName, cmsConfig)).toEqual(output);
      });

    });

    describe('for GH event should return configuration object combined from GH NextRaces config', () => {

      beforeEach(() => {
        moduleName = 'greyhound';
      });

      it('GH Module getNextRacesModuleConfig', () => {
        const output = {
          "categoryId": 39,
          "siteChannels": "M",
          "excludeUnnamedFavourites": true,
          "isActive": true,
          "eventStatusCode": "A",
          "outcomeStatusCode": "A",
          "marketStatusCodeExists": "A",
          "marketStatusCode": "A",
          "date": "nextFour",
          "priceHistory": true,
          "isRawIsOffCodeNotY": true,
          "hasOpenEvent": "true",
          "racingFormOutcome": true,
          "siteServerEventsCount": 5,
          "marketTemplateMarketNameIntersects": "|Win or Each Way|,|Win or each way|,|To-Win|,|Win|,|Win or EW|",
          "priceTypeCodes": "SP,LP",
          "typeFlagCodes": "NE,VR",
          "eventsCount": 4,
          "limitOutcomesCount": 4,
          "isVirtualRacesEnabled": true,
          "virtualRacesIncluded": [
            "Barking hall"
          ],
        }
        expect(service.getNextRacesModuleConfig(moduleName, cmsConfig)).toEqual(output);
      });
    });

    describe('getTypeFlagInfo', () => {
      it('should call getTypeFlagInfo', () => {
        service['getTypeFlagInfo']({ isVirtualRacesEnabled: 'No' } as any, false) as any;
      })
    })

    //virtualTimesConfig
    describe('virtualTimesConfig', () => {
      it('should call virtualTimesConfig', () => {
        service['virtualTimesConfig']({ VirtualsExcludeTimeRange: { from: '00:00:00' } } as any, 'from') as any;
      })
    })

    //isCurrentTimeAdded
    describe('isCurrentTimeAdded', () => {
      it('should call isCurrentTimeAdded end greater than start', () => {
        const retVal = service['isCurrentTimeAdded']([{hh: '00', mm: '00', ss: '00'}] as any, [{hh: '23', mm: '59', ss: '59'}] as any) as any;
        expect(retVal).toBeFalsy();
      })
      it('should call isCurrentTimeAdded start greater than end', () => {
        const retVal = service['isCurrentTimeAdded']([{hh: '00', mm: '00', ss: '01'}] as any, [{hh: '00', mm: '00', ss: '00'}] as any) as any;
        expect(retVal).toBeFalsy();
      })
      it('should call isCurrentTimeAdded skip case', () => {
        const retVal = service['isCurrentTimeAdded']([] as any, null) as any;
        expect(retVal).toBeTruthy();
      })
    })
  });
});
