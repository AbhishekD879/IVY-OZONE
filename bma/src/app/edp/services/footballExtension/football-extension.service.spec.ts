import { FootballExtensionService } from './football-extension.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { CommandService } from '@core/services/communication/command/command.service';
import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IGroupedMarket, IMarketsGroup } from '@edp/services/marketsGroup/markets-group.model';
import { IMarket } from '@core/models/market.model';
import { TemplateService } from '@root/app/shared/services/template/template.service';

describe('FootballExtensionService', () => {
  let service: FootballExtensionService;
  let marketsGroupFactory: MarketsGroupService;
  let commandService: CommandService;
  let pubSubService: PubSubService;
  let templateService: TemplateService

  let parentScope;

  beforeEach(() => {
    parentScope = {
      isScorecastMarketsAvailable: false,
      liveMaketTemplateMarketName: true,
      sport: {
        isAnyMarketByPattern: jasmine.createSpy().and.returnValue(true)
      },
      isSpecialEvent: false,
      scorecastInTabs: [],
      eventEntity: {
        markets: [{
          name: 'match result',
          hidden: false,
          id: 1
        }, {
          name: 'first goal scorecast',
          id: 2
        }]
      },
      marketConfig: {},
      marketAvailable: {
        name: true
      },
      marketGroup: [
        { localeName: 'group1' }
      ]
    };
    commandService = {
      executeAsync: () => new Promise<void>(resolve => resolve()),
      API: commandApi
    } as any;

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      publish: jasmine.createSpy('publish'),
      API: {
        SET_LEAGUES_LINK: 'SET_LEAGUES_LINK'
      }
    } as any;
    templateService={
      getPopularScorer:jasmine.createSpy('getPopularScorer').and.returnValue(false),
      getOtherScorer:jasmine.createSpy('getOtherScorer').and.returnValue(false)
    } as any;

    marketsGroupFactory = {
      updateMarketsGroup: jasmine.createSpy('updateMarketsGroup'),
      templateMarketInMarketsGroups: jasmine.createSpy('templateMarketInMarketsGroups').and.returnValue(
        [{ localeName: 'group1' }, { localeName: 'group2' }]),
      generateMarketsGroup: jasmine.createSpy('generateMarketsGroup'),
      isMarketAvailable: jasmine.createSpy('isMarketAvailable'),
      groupMarkets: jasmine.createSpy('groupMarkets')
    } as any;

    service = new FootballExtensionService(
      marketsGroupFactory,
      pubSubService,
      templateService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('eventMarkets', () => {
    beforeEach(() => {
      parentScope.scorecastInTabs = ['main', 'all-markets'];
    });

    it('should get competition and season and do callCallback', () => {
      spyOn(commandService, 'executeAsync').and.callThrough();
      spyOn<any>(service, 'generateMarketsGroups').and.callFake(() => {});
      service.eventMarkets(parentScope);

      expect(service['generateMarketsGroups']).toHaveBeenCalledWith(parentScope);
    });

    it('should generate market groups', () => {
      spyOn<any>(service, 'generateMarketsGroups');
      service.eventMarkets(parentScope);

      expect(service['generateMarketsGroups']).toHaveBeenCalledWith(parentScope);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('marketsGroup', 'UPDATE_OUTCOMES_FOR_MARKET', jasmine.any(Function));
    });

    it('should not generate market groups', () => {
      parentScope.isSpecialEvent = true;
      spyOn<any>(service, 'generateMarketsGroups');
      service.eventMarkets(parentScope);

      expect(service['generateMarketsGroups']).not.toHaveBeenCalled();
    });

    it('should generate market group, subscribe, but do not update markets group', () => {
      parentScope.isSpecialEvent = false;
      spyOn<any>(service, 'generateMarketsGroups');

      service.eventMarkets(parentScope);
      expect(service['generateMarketsGroups']).toHaveBeenCalledWith(parentScope);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('marketsGroup', 'UPDATE_OUTCOMES_FOR_MARKET', jasmine.any(Function));
    });

    it('no event entity', () => {
      parentScope.eventEntity = null;
      expect(() => service.eventMarkets(parentScope)).toThrowError();
    });

    it('should update outcome for market', () => {
      parentScope.sport.isAnyMarketByPattern.and.returnValue(false);
      parentScope.isSpecialEvent = false;
      (pubSubService.subscribe as any).and.callFake((p1, p2, cb) => cb({ id: 2 }));
      service.eventMarkets(parentScope);
      expect(marketsGroupFactory.updateMarketsGroup).toHaveBeenCalledTimes(1);
    });


    it('should update outcome for market', () => {
      parentScope.sport.isAnyMarketByPattern.and.returnValue(false);
      parentScope.isSpecialEvent = false;
      (pubSubService.subscribe as any).and.callFake((p1, p2, cb) => cb({ id: 3 }));
      service.eventMarkets(parentScope);
      expect(marketsGroupFactory.updateMarketsGroup).not.toHaveBeenCalled();
    });
  });

  describe('generateMarketsGroups', () => {
    const marketConfig: IGroupedMarket[] = [{}] as IGroupedMarket[];
    const groupMarket: IMarketsGroup[] = [{ localeName: 'name' }] as IMarketsGroup[];
    it('should template markets in markets group', () => {
      spyOn<any>(service, 'generateMarketsGroups');
      (marketsGroupFactory.templateMarketInMarketsGroups as any).and.returnValue([{ localeName: 'name' }]);

      service['generateMarketsGroups'](parentScope);
      const res = marketsGroupFactory.templateMarketInMarketsGroups(marketConfig, 'name');
      expect(res).toEqual(groupMarket);
    });

    it('should NOT template markets in markets group if liveMaketTemplateMarketName is false', () => {
      const markets: IMarket[] = [{}] as IMarket[];
      const market: IGroupedMarket = {} as IGroupedMarket;
      parentScope.liveMaketTemplateMarketName = false;
      spyOn<any>(service, 'generateMarketsGroups');
      (marketsGroupFactory.isMarketAvailable as any).and.returnValue(true);

      service['generateMarketsGroups'](parentScope);
      expect(marketsGroupFactory.templateMarketInMarketsGroups).not.toHaveBeenCalled();
      const res = marketsGroupFactory.isMarketAvailable(markets, markets, market);
      expect(res).toEqual(parentScope.marketAvailable['name']);
    });
  });

  describe('group markers if group exists', () => {
    let scopeGroup;

    beforeEach(() => {
      scopeGroup = {
        isScorecastMarketsAvailable: false,
        liveMaketTemplateMarketName: false,
        isSpecialEvent: false,
        eventEntity: {
          markets: [{
            name: 'name',
            hidden: false,
            id: 1
          }]
        },
        marketGroup: [{
          localeName: 'totalGoalsByTeam'
        }],
        marketConfig: [],
        marketAvailable: {
          name: true
        }
      };
      (marketsGroupFactory.isMarketAvailable as any).and.returnValue(true);
    });

    it('groupMarkets should be called', () => {
      service['generateMarketsGroups'](scopeGroup);
      expect(marketsGroupFactory.groupMarkets).toHaveBeenCalledTimes(1);
    });

    it('groupMarkets should not be called', () => {
      scopeGroup.marketGroup = [];
      service['generateMarketsGroups'](scopeGroup);
      expect(marketsGroupFactory.groupMarkets).not.toHaveBeenCalled();
    });
  });
});
