import { YourCallMarketComponent } from '@yourcall/components/yourCallMarket/your-call-market.component';

describe('YourCallMarketComponent', () => {
  let component, yourCallMarketsService;

  beforeEach(() => {
    yourCallMarketsService = {
      onMarketToggled: jasmine.createSpy()
    };
    component = new YourCallMarketComponent(yourCallMarketsService);
    component.market = {};
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should call YourCallMarketComponent.onMarketToggled', () => {
    component.ngOnInit();
    expect(yourCallMarketsService.onMarketToggled).toHaveBeenCalledTimes(1);
  });

  it('#ngOnDestroy should call YourCallMarketComponent.onMarketToggled', () => {
    component.ngOnDestroy();
    expect(yourCallMarketsService.onMarketToggled).toHaveBeenCalledTimes(1);
  });

  it('marketLoaded', () => {
    component.loading = true;
    component.marketLoaded();
    expect(component.loading).toBeFalsy();
  });
});
