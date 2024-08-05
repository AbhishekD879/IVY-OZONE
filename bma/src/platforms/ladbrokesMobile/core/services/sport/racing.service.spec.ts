import { RacingService } from './racing.service';
import { IMarket } from '@core/models/market.model';

describe('RacingService-ladbrokes', () => {
  let service: RacingService;

  let timeformService;
  let ukToteService;
  let dailyRacingService;
  let eventFactory;
  let templateService;
  let timeService;
  let filtersService;
  let liveUpdatesWSService;
  let channelService;
  let lpAvailabilityService;
  let commandService;
  let localeService;
  let racingYourcallService;
  let pubSubService;
  let cmsService;
  let racingPostService;
  let routingHelperservice;

  beforeEach(() => {
    timeformService = {
      getGreyhoundRaceById: jasmine.createSpy().and.returnValue((Promise.resolve([])))
    };
    ukToteService = {};
    eventFactory = {
      isAnyCashoutAvailable: jasmine.createSpy(),
      isAnyLiveStreamAvailable: jasmine.createSpy()
    };
    dailyRacingService = {};
    templateService = {};
    timeService = {};
    filtersService = {
      orderBy: jasmine.createSpy('orderBy').and.callFake(v => v)
    };
    liveUpdatesWSService = {};
    channelService = {};
    lpAvailabilityService = {};
    commandService = {};
    localeService = {
      getString: jasmine.createSpy().and.returnValue('Win or Each Way')
    };
    racingYourcallService = {};
    pubSubService = {};
    cmsService = {};
    racingPostService = {};
    routingHelperservice = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart').and.callFake(v => {
        return v.replace(/([^a-zA-Z0-9])+/g, '-').toLowerCase();
      })
    };

    service = new RacingService(
      timeformService,
      ukToteService,
      dailyRacingService,
      eventFactory,
      templateService,
      timeService,
      filtersService,
      liveUpdatesWSService,
      channelService,
      lpAvailabilityService,
      commandService,
      localeService,
      racingYourcallService,
      pubSubService,
      cmsService,
      racingPostService,
      routingHelperservice
    );
  });

  it('Tests if RacingService Created', () => {
    expect(service).toBeTruthy();
  });

  describe('sortRacingMarketsByTabs', () => {
    it('should set path and label to the market', () => {
      const markets = [
        {
          templateMarketName: 'Win or Each Way',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].path).toEqual('win-or-each-way');
      expect(actualResult[0].label).toEqual('Win or Each Way');
      expect(routingHelperservice.encodeUrlPart).not.toHaveBeenCalled();
    });

    it('should not add market with incorrect eventId', () => {
      const markets = [
        {
          templateMarketName: 'Top 3 Finish',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Win or Each Way',
          eventId: '12135494'
        }
      ];
      const eventId = '12135494';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].label).not.toEqual('Top 3 Finish');
      expect(actualResult[0].label).toEqual('Win or Each Way');
    });

    it('should group To Finish markets', () => {
      const markets = [
        {
          templateMarketName: 'Top 3 Finish',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Top 2 Finish',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';

      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].markets[0].templateMarketName).toEqual('Top 3 Finish');
      expect(actualResult[0].markets[1].templateMarketName).toEqual('Top 2 Finish');
      expect(actualResult[0].markets[0].isTopFinish).toEqual(true);
    });

    it('should group insurance markets', () => {
      const markets = [
        {
          templateMarketName: 'Insurance 2 Places',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Insurance 3 Places',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].markets[0].templateMarketName).toEqual('Insurance 2 Places');
      expect(actualResult[0].markets[1].templateMarketName).toEqual('Insurance 3 Places');
      expect(actualResult[0].markets[0].insuranceMarkets).toEqual(true);
    });

    it('should set label and path to not mapped market', () => {
      const eventId = '12135493';
      const markets = [{
        templateMarketName: 'Win/Win',
        name: 'Seven Emirates v Three Coins',
        eventId
      }, {
        templateMarketName: 'Betting Without',
        name: 'Betting Without Soaring9/ Star',
        eventId
      }];
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0]).toEqual(jasmine.objectContaining({
        label: markets[0].name,
        path: 'seven-emirates-v-three-coins'
      }));
      expect(actualResult[1]).toEqual(jasmine.objectContaining({
        label: markets[1].name,
        path: 'betting-without-soaring9-star'
      }));
    });
  });
});
