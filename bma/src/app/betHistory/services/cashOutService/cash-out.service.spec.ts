import { CashOutService } from '@app/betHistory/services/cashOutService/cash-out.service';

describe('Cash-out service unit tests', () => {
  let service: CashOutService;
  let localeService, cashOutMapService, gtm, toolsService, filtersService, cashOutErrorMessage, cashoutDataProvider,
    pubsub, awsService, clientUserAgentService, cashoutBetsStreamService, liveServConnectionService, deviceService;

  beforeEach(() => {
    localeService = cashOutMapService = gtm = toolsService = filtersService =
      cashOutErrorMessage = cashoutDataProvider = pubsub = awsService = clientUserAgentService = cashoutBetsStreamService =
        liveServConnectionService = deviceService = {} as any;

    service = new CashOutService(localeService, cashOutMapService, gtm, toolsService, filtersService,
      cashOutErrorMessage, cashoutDataProvider, pubsub, awsService, clientUserAgentService, cashoutBetsStreamService,
      liveServConnectionService, deviceService);
  });

  afterAll(() => {
    service = null;
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it ('should get new instance of partial cash out model', () => {
    expect(service.createPartialCashOut()).toBeTruthy();
  });

  it ('should get new instance of full cash out instance', () => {
    expect(service.createFullCashOut()).toBeTruthy();
  });

  it('should generates terms string', () => {
    const part = {
      eventMarketDesc: 'x',
      eachWayPlaces: undefined,
      eachWayNum: 1,
      eachWayDen: 2
    };
    expect(service.getEachWayTerms(null, '')).toBe('');
    expect(service.getEachWayTerms(part, '')).toBe('x');
    expect(service.getEachWayTerms(part, 'y')).toBe('x');
    expect(service.getEachWayTerms(part, 'y')).toBe('x');
    part.eachWayPlaces = 3;
    expect(service.getEachWayTerms(part, 'e')).toBe('x, 1/2 odds - places 1,2,3');
    part.eventMarketDesc = undefined;
    expect(service.getEachWayTerms(part, '')).toBe('');
    expect(service.getEachWayTerms(part, 'e')).toBe(', 1/2 odds - places 1,2,3');
  });

  describe('#createPartialCashOut', () => {
    it('should create Partial CashOut instanse', () => {
      const PartialCashOut =  service.createPartialCashOut();

      expect(PartialCashOut).toBeTruthy();
    });
  });
});
