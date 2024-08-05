import { fakeAsync, tick } from '@angular/core/testing';
import { YourCallMarketGroupComponent } from './your-call-market-group.component';

describe('YourCallMarketGroupComponent', () => {
  let yourCallMarketsService;
  let component;

  beforeEach(() => {
    yourCallMarketsService = {
      loadMarket: jasmine.createSpy('yourCallMarketsService').and.returnValue(Promise.resolve({})),
      isRestoredNeeded: jasmine.createSpy('isRestoredNeeded'),
      restoreBet: jasmine.createSpy('restoreBet')
    };

    component = new YourCallMarketGroupComponent(yourCallMarketsService);
  });

  it('ngOnInit', fakeAsync(() => {
    const loadedSpy = spyOn(component.marketLoaded, 'next');
    component.market = { markets: [{ getShortTitle: () => 'market1' }] };

    component.ngOnInit();
    tick();

    expect(component.switchers).toEqual([{ name: 'market1' }]);
    expect(loadedSpy).toHaveBeenCalled();
  }));
});
