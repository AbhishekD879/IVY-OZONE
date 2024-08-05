import { OddsFormatPipe } from './odds-format.pipe';

describe('OddsFormatPipe', () => {
  let pipe, fracToDecService;

  beforeEach(() => {
    fracToDecService = {
      getFormattedValue: jasmine.createSpy()
    };
    pipe = new OddsFormatPipe(fracToDecService);
  });

  describe('transform', () => {
    it('should return SUSP', () => {
      expect(pipe.transform(0, 0, '', false)).toEqual('SUSP');
    });
    it('should return SP', () => {
      expect(pipe.transform(0, 0, '', true)).toEqual('SP');
    });
    it('should return SP too', () => {
      expect(pipe.transform(0, 0, 'SP', false)).toEqual('SP');
    });
    it('should return formatted price', () => {
      pipe.transform(1, 2, '-', true);
      expect(fracToDecService.getFormattedValue).toHaveBeenCalledWith(1, 2);
    });
  });
});
