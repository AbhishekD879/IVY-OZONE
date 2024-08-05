import { FiveASidePrizePoolComponent } from '@app/fiveASideShowDown/components/fiveASidePrizePool/fiveaside-prize-pool.component';

describe('FiveASidePrizePoolComponent', () => {
  let component: FiveASidePrizePoolComponent;

  beforeEach(() => {
    component = new FiveASidePrizePoolComponent();

  });

  describe('constructor', () => {
    it('should create component instance', () => {
      expect(component).toBeTruthy();
    });
  });

  describe('#returnOne', () => {
    it('should  return one for key value pipe', () => {
      expect(component['returnOne']()).toBe(1);
    });
  });

  describe('#addOrdinalSuffix', () => {
    it('Should return number + "st Prize"', () => {
      const num = '21';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('21st');
    });

    it('Should return number range + "th"', () => {
      const num = '2-100';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('2-100th');
    });

    it('Should return number range + "th"', () => {
      const num = '1 - 4';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('1-4th');
    });

    it('Should return number range + "17-23rd"', () => {
      const num = '17 - 23';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('17-23rd');
    });

    it('Should return number range + "17-22nd"', () => {
      const num = '17 - 22';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('17-22nd');
    });

    it('Should return number range + "17-21st"', () => {
      const num = '17 - 21';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('17-21st');
    });

    it('Should return number range + "17-24th"', () => {
      const num = '17 - 24';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('17-24th');
    });

    it('Should return number range + "17-25th"', () => {
      const num = '17 - 25';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('17-25th');
    });

    it('Should return number range + "st for 1 suffx"', () => {
      const num = '1 - 1';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('1-1st');
    });

    it('Should return number range + "st for 1 suffx"', () => {
      const num = '2 - 1';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('2-1st');
    });

    it('Should return number range + "st for 1 suffx"', () => {
      const num = '3 - 1';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('3-1st');
    });

    it('Should return number range + "nd for 2 suffx"', () => {
      const num = '1 - 2';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('1-2nd');
    });

    it('Should return number range + "nd for 2 suffx"', () => {
      const num = '2 - 1';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('2-1st');
    });


    it('Should return number range + "rd for 3 suffx"', () => {
      const num = '1 - 3';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('1-3rd');
    });

    it('Should return number range + "rd for 3 suffx"', () => {
      const num = '2 - 3';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('2-3rd');
    });

    it('Should return number range + "rd for 3 suffx"', () => {
      const num = '3 - 2';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('3-2nd');
    });


    it('Should return number + "nd Prize"', () => {
      const num = '22';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('22nd');
    });

    it('Should return number + "rd Prize"', () => {
      const num = '23';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('23rd');
    });

    it('Should return number + "th Prize"', () => {
      const num = '25';
      const suffix = component.addOrdinalSuffix(num);

      expect(suffix).toEqual('25th');
    });
  });
  it('should return signposting Url', () => {
    expect(component.getSignpostingUrl('url')).not.toBeNull();
  });

  describe('#fixedDecimals', () => {
    it('should return with decimals fixed to 2', () => {
      const result = component.fixedDecimals("0.1231231");
      expect(result).toEqual("0.12");
    });
    it('should return without decimals', () => {
      const result = component.fixedDecimals("10.0");
      expect(result).toEqual("10");
    });
  });
});
