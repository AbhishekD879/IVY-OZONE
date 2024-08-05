import { BetslipFiltersService } from './betslip-filters.service';

describe('BetslipFiltersService', () => {
  let service;
  let timeService;

  const testStr = 'TestString';

  beforeEach(() => {
    timeService = {
      isEqualDatesByPattern: () => {},
      formatByPattern: () => {}
    };

    service = new BetslipFiltersService(timeService);
  });

  describe('filterStakeValue', () => {
    it('should return default value', () => {
      expect(service.filterStakeValue('')).toEqual(0);
    });

    it('should return numbers from passed value', () => {
      expect(service.filterStakeValue('1.50-test')).toEqual(1.5);
      expect(service.filterStakeValue(2.22)).toEqual(2.22);
      expect(service.filterStakeValue('test-2.20')).toEqual(2.2);
    });
  });

  describe('handicapValueFilter', () => {
    it('should filter handicap with + sign', () => {
      expect(service.handicapValueFilter('5.5')).toEqual('+5.5');
      expect(service.handicapValueFilter('2')).toEqual('+2');
    });

    it('should filter handicap with - sign', () => {
      expect(service.handicapValueFilter('-5.5')).toEqual('-5.5');
      expect(service.handicapValueFilter('-2')).toEqual('-2');
    });
  });

  describe('multiplesSort', () => {
    it('should sort TBL and DBL bets', () => {
      const bets = [{ type: 'TBL' }, { type: 'DBL' }];
      const result = service.multiplesSort(bets, bets.length);

      expect(result[0]).toEqual(bets[1]);
      expect(result[1]).toEqual(bets[0]);
    });

    it('should sort ACC pattern accumulator bets', () => {
      const bets = [{ type: 'ACC3' }, { type: 'AC26' }, { type: 'ACC2' }];
      const result = service.multiplesSort(bets, 30);

      expect(result[0]).toEqual(bets[0]);
      expect(result[1]).toEqual(bets[2]);
      expect(result[2]).toEqual(bets[1]);
    });

    it('should sort ACC not pattern accumulator bets', () => {
      const bets = [{ type: 'ACC3' }, { type: 'AC26' }, { type: 'ACC2' }];
      const result = service.multiplesSort(bets, bets.length);

      expect(result[0]).toEqual(bets[0]);
      expect(result[1]).toEqual(bets[1]);
      expect(result[2]).toEqual(bets[2]);
    });
  });

  describe('todayTomorrowDate', () => {
    it(`should check it's today`, () => {
      spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValue(true);

      service.todayTomorrowDate(testStr, true, true);

      expect(service['timeService'].isEqualDatesByPattern.calls.argsFor(0))
        .toEqual([jasmine.any(Date), testStr, 'dd/MM/yyyy', true]);
    });

    describe('isShort', () => {
      it(`should return 'Today' if it's today`, () => {
        spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValue(true);

        expect(service.todayTomorrowDate(testStr, true)).toEqual('Today');
      });

      it(`should return 'Tomorrow' if it's tomorrow`, () => {
        spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValues(false, true, true);

        expect(service.todayTomorrowDate(testStr, true)).toEqual('Tomorrow');
      });

      it(`should return return formatted tate`, () => {
        spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValues(false, true, false);
        spyOn(service['timeService'], 'formatByPattern');

        service.todayTomorrowDate(testStr, true, true);

        expect(service['timeService'].formatByPattern.calls.argsFor(0)).toEqual([testStr, 'd MMM, yyyy', null, true]);
      });
    });

    describe('isShort equal False', () => {
      it(`should return formatted date for 'Today'`, () => {
        spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValue(true);
        spyOn(service['timeService'], 'formatByPattern').and.returnValue('hh:mm a');

        expect(service.todayTomorrowDate(testStr, false, true)).toEqual('hh:mm a, Today');
        expect(service['timeService'].formatByPattern.calls.argsFor(0)).toEqual([testStr, 'hh:mm a', null, true]);
      });

      it(`should return formatted date for 'Tomorrow'`, () => {
        spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValues(false, true, true);
        spyOn(service['timeService'], 'formatByPattern').and.returnValue('hh:mm a');

        expect(service.todayTomorrowDate(testStr, false, true)).toEqual('hh:mm a, Tomorrow');
        expect(service['timeService'].formatByPattern.calls.argsFor(0)).toEqual([testStr, 'hh:mm a', null, true]);
      });

      it(`should return return formatted tate`, () => {
        spyOn(service['timeService'], 'isEqualDatesByPattern').and.returnValues(false, true, false);
        spyOn(service['timeService'], 'formatByPattern');

        service.todayTomorrowDate(testStr, false, true);

        expect(service['timeService'].formatByPattern.calls.argsFor(0)).toEqual([testStr, 'hh:mm a, d MMM, yyyy', null, true]);
      });
    });
  });
});
