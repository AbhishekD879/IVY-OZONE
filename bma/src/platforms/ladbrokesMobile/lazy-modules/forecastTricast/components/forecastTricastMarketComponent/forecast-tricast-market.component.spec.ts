import {
  ForecastTricastMarketComponent
} from '@ladbrokesMobile/lazy-modules/forecastTricast/components/forecastTricastMarketComponent/forecast-tricast-market.component';

describe('ForecastTricastMarketComponent', () => {
  let component: any;
  let local: any;
  let betBuilderService: any;
  let ukTotesHandleLiveServeUpdatesService: any;
  let ukToteLiveUpdatesService: any;
  let ukToteService: any;
  let pubSubService: any;
  let gtmService;

  beforeEach(() => {
    local = {};
    betBuilderService = {};
    ukTotesHandleLiveServeUpdatesService = {};
    ukToteLiveUpdatesService = {};
    ukToteService = {};
    pubSubService = {};
    gtmService = {};

    component = new ForecastTricastMarketComponent(
      local,
      betBuilderService,
      ukTotesHandleLiveServeUpdatesService,
      ukToteLiveUpdatesService,
      ukToteService,
      pubSubService,
      gtmService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
