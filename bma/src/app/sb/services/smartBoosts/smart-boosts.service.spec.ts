import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { IMarket } from '@core/models/market.model';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

describe('SmartBoostsService', () => {
  let service: SmartBoostsService;
  let fracToDecServiceStub;

  const testStr = 'TestString';
  const wasPriceStub = '12/11';
  const nameStub = `${testStr} (Was ${wasPriceStub}) ${testStr}`;

  beforeEach(() => {
    fracToDecServiceStub = { getFormattedValue: jasmine.createSpy().and.returnValue(wasPriceStub) };
    service = new SmartBoostsService(fracToDecServiceStub as FracToDecService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('isSmartBoosts', () => {
    it(`should return Truth if market has flag 'MKTFLAG_PR1'`, () => {
      expect(service.isSmartBoosts({ drilldownTagNames: 'MKTFLAG_PR1' } as IMarket)).toBeTruthy();
    });

    it(`should return Truth if market has flag 'MKTFLAG_PB'`, () => {
      expect(service.isSmartBoosts({ drilldownTagNames: 'MKTFLAG_PB' } as IMarket)).toBeTruthy();
    });

    it(`should return Truth if market has bought flags 'MKTFLAG_PR1, MKTFLAG_PB'`, () => {
      expect(service.isSmartBoosts({ drilldownTagNames: 'MKTFLAG_PR1, MKTFLAG_PB' } as IMarket)).toBeTruthy();
    });

    it('should return Falthy if market is Not SmartBoost', () => {
      expect(service.isSmartBoosts({ drilldownTagNames: testStr } as IMarket)).toBeFalsy();
    });

    it('should return Falsy if no tags', () => {
      expect(service.isSmartBoosts({} as IMarket)).toBeFalsy();
    });
  });

  describe('parseName', () => {
    it('should return parsed Name', () => {
      expect(service.parseName(nameStub)).toEqual({ name: `${testStr} ${testStr}`, wasPrice: wasPriceStub });
    });

    it('should return Name if Name has Not Was price', () => {
      expect(service.parseName(testStr).name).toEqual(testStr);
    });

    it('should return empty wasPrice if Name has Not Was price', () => {
      expect(service.parseName(testStr).wasPrice).toEqual('');
    });
  });

});
