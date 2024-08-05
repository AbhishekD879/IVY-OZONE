import { MarketSelectorTrackingService } from './market-selector-tracking.service';

describe('MarketSelectorStorageService', () => {
    let marketSelectorTrackingService: MarketSelectorTrackingService;
    let gtmService;

    beforeEach(() => {
          gtmService = {
            push: jasmine.createSpy('push')
          };
          marketSelectorTrackingService = new MarketSelectorTrackingService(
            gtmService
        );
    });

    describe('@ngOnInit', () => {
      it('selector data should be null', () => {
        marketSelectorTrackingService.sendGTMDataOnMarketSelctorChange('golf', '');
        expect(marketSelectorTrackingService['gtmService'].push).toHaveBeenCalled();
      });
    });
});