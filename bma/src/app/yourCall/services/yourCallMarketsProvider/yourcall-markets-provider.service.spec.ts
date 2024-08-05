import { YourCallMarketsProviderService } from '@yourcall/services/yourCallMarketsProvider/yourcall-markets-provider.service';
import { YOURCALL_BANACH_MARKETS } from '@yourcall/constants/yourcall-banach-markets';
import { YOURCALL_DATA_PROVIDER } from '@yourcall/constants/yourcall-data-provider';
import { YourCallMarketGroup } from '@yourcall/models/markets/yourcall-market-group';
import { YourCallMarketPlayer } from '@yourcall/models/markets/yourcall-market-player';
import { YourCallMarketGroupItem } from '@yourcall/models/markets/yourcall-market-group-item';
import { YourCallMarket } from '@yourcall/models/markets/yourcall-market';
import { YourCallMarketGroupPlayer } from '@yourcall/models/markets/yourcall-market-group-player';

describe('YourCallMarketsProviderService', () => {
  let service: YourCallMarketsProviderService;

  beforeEach(() => {
    const locale: any = {
      testFiled: 'some test string'
    };

    service = new YourCallMarketsProviderService(locale);
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  describe('BYB_MAP', () => {
    it('should return instance of YourCallMarketGroup', () => {
      expect(service.BYB_MAP({grouping: 'Test grouping'})).toEqual(jasmine.any(YourCallMarketGroup));
    });

    it('should return instance of YourCallMarketPlayer', () => {
      expect(service.BYB_MAP({grouping: 'Player Bets'})).toEqual(jasmine.any(YourCallMarketPlayer));
    });

    it('should return correct instance, depend on current case', () => {
      const data = {
        parent: 'someParent'
      };

      expect(service.BYB_MAP({...data, groupName: YOURCALL_BANACH_MARKETS.SHOWN_CARD}) as any).toEqual(jasmine.any(YourCallMarket));
      expect(service.BYB_MAP({
        ...data,
        groupName: YOURCALL_BANACH_MARKETS.FIRST_GOAL
      }) as any).toEqual(jasmine.any(YourCallMarketGroupPlayer));
      expect(service.BYB_MAP({
        ...data,
        groupName: YOURCALL_BANACH_MARKETS.PLAYER_2_GOALS
      }) as any).toEqual(jasmine.any(YourCallMarketGroupPlayer));
      expect(service.BYB_MAP({
        ...data,
        groupName: YOURCALL_BANACH_MARKETS.PLAYER_3_GOALS
      }) as any).toEqual(jasmine.any(YourCallMarketGroupPlayer));
      expect(service.BYB_MAP({
        ...data,
        groupName: YOURCALL_BANACH_MARKETS.ANYTIME_GOAL
      }) as any).toEqual(jasmine.any(YourCallMarketGroupPlayer));
      expect(service.BYB_MAP({
        ...data,
        groupName: YOURCALL_BANACH_MARKETS.FIRST_BOOKING
      }) as any).toEqual(jasmine.any(YourCallMarketGroupPlayer));
    });

    it('should return instance of YourCallMarketGroupItem', () => {
      expect(service.BYB_MAP({
        groupName: YOURCALL_BANACH_MARKETS,
        parent: 'someParent'
      })).toEqual(jasmine.any(YourCallMarketGroupItem));
    });

    it('should return instance of YourCallMarket', () => {
      expect(service.BYB_MAP({})).toEqual(jasmine.any(YourCallMarket));
    });
  });

  describe('getInstance', () => {
    it('should return instance of YourCallMarket', () => {
      expect(service.getInstance({})).toEqual(jasmine.any(YourCallMarket));
    });

    it('should return instance of YourCallMarketGroupItem', () => {
      expect((service.getInstance({
        provider: YOURCALL_DATA_PROVIDER.BYB,
        groupName: YOURCALL_BANACH_MARKETS,
        parent: 'some parent'
      }) as any)).toEqual(jasmine.any(YourCallMarketGroupItem));
    });
  });
});
