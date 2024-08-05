import { ScorecastDataService } from './scorecast-data.service';

describe('ScorecastDataService', () => {
  let service: ScorecastDataService;

  beforeEach(() => {
    service = new ScorecastDataService();
  });

  it('should call setScorecastData', ()=> {
    const data = 'data';
    service.setScorecastData(data);
    expect(service.getScorecastData()).toEqual(data);
  });
});
