import { NextRacesHomeService } from './next-races-home.service';

describe('NextRacesHomeService', () => {
  let service;
  let pubsubService;
  const events = [{
    liveServChildrenChannels: 'liveServChildrenChannels,',
    liveServChannels: 'liveServChannels,'
  }];
  const cacheEventsService = {},
    templateService = {
      setCorrectPriceType: jasmine.createSpy('setCorrectPriceType').and.callFake(data => {
        return data;
      })
    },
    channelService = jasmine.createSpyObj(['getLSChannelsFromArray']),

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Good')
    },
    filterService = {
      distance: jasmine.createSpy('distance').and.returnValue('1 yard')
    };

  beforeEach(() => {
    pubsubService = {
      publish: jasmine.createSpy(),
      API: {
        PUSH_TO_GTM: 'PUSH_TO_GTM'
      }
    };

    service = new NextRacesHomeService(
      cacheEventsService as any,
      templateService as any,
      channelService as any,
      pubsubService as any,
      localeService as any,
      filterService as any
    );
  });

  describe('getNextRacesModuleConfig', () => {
    let moduleName, cmsConfig, expectedStrictConfig, expectedDynamicConfig;

    beforeEach(() => {
      service.CATEGORIES_DATA = {
        racing: {
          horseracing: { id: 21 },
          greyhound: { id: 19 }
        }
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
          }
        },
        GreyhoundNextRaces: {
          numberOfEvents: '4',
          numberOfSelections: '4',
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
        expectedStrictConfig.categoryId = '21';
        expectedDynamicConfig = {
          racingFormEvent: false,
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
        expectedDynamicConfig.racingFormEvent = true;
        expectedDynamicConfig.racingFormOutcome = true;
      });
      it('when RacingPost is missing', () => {
        delete cmsConfig.RacingDataHub;
        expectedDynamicConfig.racingFormEvent = true;
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
          it ('for string 3', () => { cmsConfig.NextRaces.numberOfEvents = '3'; });
          it ('for number 3', () => { cmsConfig.NextRaces.numberOfEvents = 3; });
          it ('for string 2', () => { cmsConfig.NextRaces.numberOfEvents = '2'; });
          it ('for number 2', () => { cmsConfig.NextRaces.numberOfEvents = 2; });
        });
        describe('should equal 5 for 3<value<=5', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 5; });
          it ('for string 5', () => { cmsConfig.NextRaces.numberOfEvents = '5'; });
          it ('for number 5', () => { cmsConfig.NextRaces.numberOfEvents = 5; });
          it ('for string 4', () => { cmsConfig.NextRaces.numberOfEvents = '4'; });
          it ('for number 4', () => { cmsConfig.NextRaces.numberOfEvents = 4; });
        });
        describe('should equal 5 for 5<value<=7', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 7; });
          it ('for string 7', () => { cmsConfig.NextRaces.numberOfEvents = '7'; });
          it ('for number 7', () => { cmsConfig.NextRaces.numberOfEvents = 7; });
          it ('for string 6', () => { cmsConfig.NextRaces.numberOfEvents = '6'; });
          it ('for number 6', () => { cmsConfig.NextRaces.numberOfEvents = 6; });
        });
        describe('should equal 12 for 7<value', () => {
          beforeEach(() => { expectedDynamicConfig.siteServerEventsCount = 12; });
          it ('for string 8', () => { cmsConfig.NextRaces.numberOfEvents = '8'; });
          it ('for number 8', () => { cmsConfig.NextRaces.numberOfEvents = 8; });
        });
        afterEach(() => { expectedDynamicConfig.eventsCount = Number(cmsConfig.NextRaces.numberOfEvents); });
      });
    });

    describe('for GH event should return configuration object combined from Strict config and GH NextRaces config', () => {
      beforeEach(() => {
        moduleName = 'greyhound';
        expectedStrictConfig.categoryId = '19';
        expectedDynamicConfig = {
          racingFormEvent: false,
          racingFormOutcome: false,
          siteServerEventsCount: 5,
          eventsCount: 4,
          priceTypeCodes: 'SP,LP',
          limitOutcomesCount: 4,
          typeFlagCodes: 'NE'
        };
      });

      it('when RacingPost is enabled', () => { /* as it is */ });
      it('when RacingPost is disabled for GH', () => {
        cmsConfig.RacingDataHub.isEnabledForGreyhound = false;
        expectedDynamicConfig.racingFormEvent = true;
        expectedDynamicConfig.racingFormOutcome = true;
      });
      it('when RacingPost is missing', () => {
        delete cmsConfig.RacingDataHub;
        expectedDynamicConfig.racingFormEvent = true;
        expectedDynamicConfig.racingFormOutcome = true;
      });
    });
    afterEach(() => {
      expect(service.getNextRacesModuleConfig(moduleName, cmsConfig)).toEqual({
        ...expectedStrictConfig, ...expectedDynamicConfig
      });
    });
  });

  describe('#getUpdatedEvents', () => {
    it('should get uodated events and set necessary attributes for displaying events', () => {
      spyOn(service, 'getEventsFromCache');
      const result = service.getUpdatedEvents(events, 'next races');

      expect(result).toEqual(events);
    });
  });

  describe('#subscribeForUpdates', () => {
    it(`should subscribe on LS updates`, () => {
      const channel = ['sEVENT1'];
      const baseTime = new Date(2013, 9, 23);
      jasmine.clock().mockDate(baseTime);
      channelService.getLSChannelsFromArray.and.returnValue(channel);

      service.subscribeForUpdates(events);

      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(events);
      expect(pubsubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
        channel,
        module: `next-races-home-${baseTime.getTime()}`
      });
      jasmine.clock().uninstall();
    });

    it('should subscribe for updates for channels', () => {
      const result = service.subscribeForUpdates(events);

      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(events);
      expect(pubsubService.publish).toHaveBeenCalled();
      expect(result).not.toBe('');
    });

    it('should subscribe for updates when no channels', () => {
      channelService.getLSChannelsFromArray.and.returnValue([]);

      const result = service.subscribeForUpdates([]);

      expect(result).toEqual('');
    });
  });

  describe('#unSubscribeForUpdates', () => {
    it('should unsubscribe for updates if channel ids exists', () => {
      service.unSubscribeForUpdates('next-races-home-1565879224866');

      expect(pubsubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'next-races-home-1565879224866');
    });

    it('should not unsubscribe for updates if channel ids dosen"t exists', () => {
      service.unSubscribeForUpdates();

      expect(pubsubService.publish).not.toHaveBeenCalled();
    });
  });

  describe('#sendGTM', () => {
    it('should send GTM tracking, via pubsub', () => {
      service.sendGTM('eventLabel', 'eventCategory');

      expect(pubsubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent',
        {
          eventCategory: 'eventCategory',
          eventAction: 'next races',
          eventLabel: 'eventLabel'
        }
      ]);
    });
  });

  describe('#trackNextRace', () => {
    it('should Track Next Races full race card click', () => {
      const sport = {} as any;
      sport.typeName = 'kempton';
      sport.localTime = '1591775448637';
      service.trackNextRace(sport);

      expect(pubsubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent',
        {
          eventCategory: 'navigation',
          eventAction: 'next races',
          eventLabel: 'kempton / 1591775448637'
        }
      ]);
    });

    it('should Track Next Races full race card click for virtuals', () => {
      const sport = {} as any;
      sport.typeName = 'kempton';
      sport.localTime = '1591775448637';
      sport.categoryId = '39'
      service.trackNextRace(sport);

      expect(pubsubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent',
        {
          eventCategory: 'navigation',
          eventAction: 'next races',
          eventLabel: 'kempton / 1591775448637',
          positionEvent: 'virtual'
        }
      ]);
    });
  });

  describe('#isItvEvent', () => {
    it('should check is event itv and return true', () => {
      const result = service.isItvEvent({
        drilldownTagNames: 'EVFLAG_FRT'
      });

      expect(result).toEqual(true);
    });

     it('should check is event itv and return false', () => {
      const result = service.isItvEvent({
        drilldownTagNames: 'flag gla'
      });

      expect(result).toEqual(false);
    });

    it(`shoud return false if event doesn't have tags`, () => {
      expect(  service.isItvEvent({ drilldownTagNames: '' }) ).toEqual(false);
    });
  });

  describe('#getGoing', () => {
    it('should should convernt going string, g -> Good', () => {
      const result = service.getGoing('G');

      expect(localeService.getString).toHaveBeenCalledWith(`racing.racingFormEventGoing.G`);
      expect(result).toEqual('Good');
    });

    it('should should convernt going string, to empty', () => {
      localeService.getString.and.returnValue('KEY_NOT_FOUND');
      const result = service.getGoing('');

      expect(localeService.getString).toHaveBeenCalledWith(`racing.racingFormEventGoing.G`);
      expect(result).toEqual('');
    });
  });

  describe('#getDistance', () => {
    it('should convert distance', () => {
      const result = service.getDistance('1y');

      expect(filterService.distance).toHaveBeenCalledWith('1y');
      expect(result).toEqual('1 yard');
    });
  });

  describe('#getTypeFlagInfo', () => {
    it('should return string containing typeFlag codes for UK', () => {
      const result = service.getTypeFlagInfo({
        isInUK: 'Yes'
      }, true);

      expect(result).toEqual('UK');
    });

    it('should return string containing typeFlag codes for IE', () => {
      const result = service.getTypeFlagInfo({
        isIrish: 'Yes'
      }, true);

      expect(result).toEqual('IE');
    });

    it('should return string containing typeFlag codes for INT', () => {
      const result = service.getTypeFlagInfo({
        isInternational: 'Yes'
      }, true);

      expect(result).toEqual('INT');
    });

    it('should return string containing typeFlag codes for typeID', () => {
      const result = service.getTypeFlagInfo({
        typeID: '12'
      }, false);

      expect(result).toEqual('12');
    });
  });

  describe('#getEventsCount', () => {
    it('should Get amount of event that we need from SS to display 3', () => {
      const result = service.getEventsCount({
        numberOfEvents: 3
      });

      expect(result).toEqual(3);
    });

    it('should Get amount of event that we need from SS to display, 5', () => {
      const result = service.getEventsCount({
        numberOfEvents: 5
      });

      expect(result).toEqual(5);
    });

    it('should Get amount of event that we need from SS to display, 7', () => {
      const result = service.getEventsCount({
        numberOfEvents: 7
      });

      expect(result).toEqual(7);
    });

    it('should Get amount of event that we need from SS to display, 12', () => {
      const result = service.getEventsCount({
        numberOfEvents: 13
      });

      expect(result).toEqual(12);
    });
  });
});
