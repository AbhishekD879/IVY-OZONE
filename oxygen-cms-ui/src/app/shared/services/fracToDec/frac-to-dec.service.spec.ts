import { FracToDecService } from '@app/shared/services/fracToDec/frac-to-dec.service';

describe('FracToDecService', () => {
  let service: FracToDecService;

  beforeEach(() => {
    service = new FracToDecService();
  });

  it('#fracToDec', () => {
    expect(service.fracToDec(1, 5)).toEqual('1.20');
  });

  it('#getDecimal should get value from constants', () => {
    expect(service.getDecimal(13, 8)).toEqual(2.62);
  });

  it('#getDecimal should calculate value', () => {
    expect(service.getDecimal(1, 2)).toEqual('1.50');
    expect(service.getDecimal(1, 2, 1)).toEqual('1.5');
  });
});
