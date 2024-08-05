import { ScorecastSportsLegService } from './scorecast-sports-leg.service';

describe('ScorecastSportsLegService', () => {
  let sportsLegPriceService;
  let betSelectionService;
  let service;

  beforeEach(() => {
    sportsLegPriceService = {
      getOutcome: jasmine.createSpy()
    };
    betSelectionService = {};

    service = new ScorecastSportsLegService(sportsLegPriceService, betSelectionService);
  });

  it('construct', () => {
    expect(service.construct({ id: '123' } as any, 123).winPlace).toEqual('WIN');
    expect(service.construct({ id: '123' } as any, 123).combi).toEqual('SCORECAST');
  });
});
