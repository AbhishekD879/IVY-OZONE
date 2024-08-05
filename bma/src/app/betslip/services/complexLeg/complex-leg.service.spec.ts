import { ComplexLegService } from '@betslip/services/complexLeg/complex-leg.service';

describe('ComplexLegService', () => {
  let forecastSportsLegService: any;
  let service: ComplexLegService;

  beforeEach(() => {
    forecastSportsLegService = {
      construct: jasmine.createSpy('construct')
    };

    service = new ComplexLegService(
      forecastSportsLegService
    );
  });

  it('getTricastForecastLegs', () => {
    service['getLastDocId'] = jasmine.createSpy();
    service['setParts'] = jasmine.createSpy();

    service.getTricastForecastLegs({ type: 'FORECAST' } as any, []);
    service.getTricastForecastLegs({ type: 'FORECAST_COM' } as any, []);

    expect(service['getLastDocId']).toHaveBeenCalledTimes(2);
    expect(service['setParts']).toHaveBeenCalledTimes(1);
    expect(forecastSportsLegService.construct).toHaveBeenCalledTimes(2);
  });

  it('getLastDocId', () => {
    expect(service['getLastDocId']([])).toBe(0);
    expect(service['getLastDocId']([{ docId: 1 }] as any)).toBe(1);
    expect(service['getLastDocId']([{ docId: 1 }, { docId: 2 }] as any)).toBe(2);
  });

  it('setParts', () => {
    const leg: any = {
      parts: [{}, {}]
    };
    service['setParts'](leg);
    expect(leg.parts[0].places).toBe(1);
    expect(leg.parts[1].places).toBe(2);
  });
});
