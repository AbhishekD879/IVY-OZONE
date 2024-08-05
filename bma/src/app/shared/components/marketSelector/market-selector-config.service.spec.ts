import { MarketSelectorConfigService } from './market-selector-config.service';

describe ('MarketSelectorConfigService', () => {
  let service: MarketSelectorConfigService;

  beforeEach(() => {
    service = new MarketSelectorConfigService();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });
});


