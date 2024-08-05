import {
  MarketDescriptionComponent
 } from '@lazy-modules/market-description/components/market-description/market-description.component';

describe('MarketDescriptionComponent', () => {
  let component;
  let changeDetectorRef;
  let pubSubService;

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    pubSubService = {
      API: {
        HAS_MARKET_DESCRIPTION: 'HAS_MARKET_DESCRIPTION'
      },
      publish: jasmine.createSpy('publish')
    };
    component = new MarketDescriptionComponent(changeDetectorRef, pubSubService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
