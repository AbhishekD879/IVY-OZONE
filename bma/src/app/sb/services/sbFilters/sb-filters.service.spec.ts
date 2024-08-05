import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';

describe('SbFiltersService', () => {
  let service: SbFiltersService;

  beforeEach(() => {
    service = new SbFiltersService();
  });

  describe('orderOutcomeEntities tests', () => {
    let outcomes;

    beforeEach(() => {
      service['filterSpOutcomes'] = jasmine.createSpy('filterSpOutcomes').and.returnValue([]);

      outcomes = [{
        name: '3',
        outcomeMeaningMinorCode: '1',
        prices: [{
          priceNum: 1,
          priceDen: 3
        }]
      }, {
        name: '2 N/R',
        runnerNumber: 1,
        prices: [{
          priceNum: 1,
          priceDen: 4
        }]
      }, {
        name: '7',
        outcomeMeaningMinorCode: '2',
        runnerNumber: 2,
        prices: []
      }, {
        name: '4',
        outcomeMeaningMinorCode: '2',
        prices: []
      }, {
        name: '8',
        outcomeMeaningMinorCode: '2',
        runnerNumber: 3,
        prices: []
      }, {
        name: '9',
        outcomeMeaningMinorCode: '2',
        runnerNumber: 1,
        prices: []
      }, {
        name: 'x',
        outcomeMeaningMinorCode: '2',
        runnerNumber: 10,
        prices: []
      }, {
        name: 'z',
        outcomeMeaningMinorCode: '2',
        runnerNumber: 10,
        prices: []
      }, {
        name: 'z',
        outcomeMeaningMinorCode: '2',
        runnerNumber: 10,
        prices: []
      }, {
        name: '5',
        runnerNumber: 6,
        prices: [{
          priceNum: 1,
          priceDen: 3
        }]
      }, {
        name: '1',
        runnerNumber: 2,
        prices: [{
          priceNum: 3,
          priceDen: 1
        }]
      }, {
        name: '6',
        runnerNumber: 2,
        prices: [{
          priceNum: 1,
          priceDen: 3
        }]
      }];
    });

    it('isLpAvailable: true', () => {
      service.orderOutcomeEntities(outcomes, true);
      expect(service['filterSpOutcomes']).not.toHaveBeenCalled();
    });

    it('isLpAvailable: "true"', () => {
      service.orderOutcomeEntities(outcomes, 'true');
      expect(service['filterSpOutcomes']).not.toHaveBeenCalled();
    });

    it('isLpAvailable: "true"', () => {
      const result = service.orderOutcomeEntities(outcomes, 'true');
      expect(service['filterSpOutcomes']).not.toHaveBeenCalled();
      expect(result.map(outcome => outcome['name'])).toEqual(['2 N/R', '6', '5', '1', '9', '7', '8', 'x', 'z', 'z', '3', '4']);
    });

    it('isLpAvailable: false, sortByRunnerNumber: true', () => {
      service.orderOutcomeEntities(outcomes, false, false, true);
      expect(service['filterSpOutcomes']).toHaveBeenCalledWith(outcomes, true, undefined);
    });

    it('isLpAvailable: false, sortByRunnerNumber: false', () => {
      service.orderOutcomeEntities(outcomes, false, false, false);
      expect(service['filterSpOutcomes']).toHaveBeenCalledWith(outcomes, false, undefined);
    });

    it('sortBy NonRunner', () => {
      const result = service.orderOutcomeEntities(outcomes, true, true, true);
      expect(result.map(outcome => outcome['name'])).toEqual(['6', '5', '1', '9', '7', '8', 'x', 'z', 'z', '2 N/R', '3', '4']);
    });

    it('sortBy NonRunner false', () => {
      const result = service.orderOutcomeEntities(outcomes, true, true, false);
      expect(result.map(outcome => outcome['name'])).toEqual(['6', '5', '1', '9', '7', '8', 'x', 'z', 'z', '2 N/R', '3', '4']);
    });

    it('hideFavourite', () => {
      const result = service.orderOutcomeEntities(outcomes, true, true, true, true, true);

      expect(result.map(outcome => outcome['name'])).toEqual(['6', '5', '1', '9', '7', '8', 'x', 'z', 'z']);
    });

    it('should detect nonRunners if they are not hidden', () => {
      const outcomesNonRunners = [
        {
          name: 'Runner',
          runnerNumber: 1,
          prices: []
        },
        {
          name: 'NonRunner N/R',
          runnerNumber: 2,
          prices: []
        },
        {
          name: 'Unnamed',
          runnerNumber: 3,
          prices: []
        }
      ] as any;

      const result = service.orderOutcomeEntities(outcomesNonRunners, true, false, false, false, false);

      expect(result[0].nonRunner).toEqual(false);
      expect(result[1].nonRunner).toEqual(true);
      expect(result[2].nonRunner).toEqual(false);
    });
  });

  it('outcomeMinorCodeName', () => {
    expect(service.outcomeMinorCodeName('H')).toBe('sb.home');
    expect(service.outcomeMinorCodeName('A')).toBe('sb.away');
    expect(service.outcomeMinorCodeName('D')).toBe('sb.draw');
    expect(service.outcomeMinorCodeName('TEST')).toBeFalsy();
  });

  it('orderOutcomeEntities will filter by name', () => {
    const outcomes = [{
      name: 'c',
      runnerNumber: 3,
      prices: []
    } as any, {
      name: 'a',
      runnerNumber: 2,
      prices: []
    } as any, {
      name: 'a',
      runnerNumber: 4,
      prices: []
    } as any, {
      name: 'b',
      runnerNumber: 1,
      prices: []
    } as any];

    const result = service.orderOutcomeEntities(outcomes, 'true');

    expect(result.map(outcome => outcome['name'])).toEqual(['b', 'a', 'c', 'a']);
  });

  describe('filterSpOutcomes', () => {
    it('when there are runnerNumbers', () => {
      const outcomes = [{
        name: '2',
        runnerNumber: 2
      } as any, {
        name: '3',
        runnerNumber: 3
      } as any, {
        name: '1',
        runnerNumber: 2
      } as any];

      const result = service['filterSpOutcomes'](outcomes, true);
      expect(result.map(outcome => Number(outcome.runnerNumber))).toEqual([2, 2, 3]);
    });

    it('when there are not runnerNumbers', () => {
      const outcomes = [{
        name: '3'
      } as any, {
        name: '2'
      } as any, {
        name: '1'
      } as any];

      const result = service['filterSpOutcomes'](outcomes, true);
      expect(result.map(outcome => outcome.name)).toEqual(['1', '2', '3']);
    });
  });

  it('outcomePrice', () => {
    let outcome = { prices: [] } as any;
    expect(service['outcomePrice'](outcome)).toBe(null);

    outcome = { prices: [{ priceNum: 1, priceDen: 1 }] };
    expect(service['outcomePrice'](outcome)).toBe(2);
  });

  it('findFavourite', () => {
    let outcomes = [{ name: '1', outcomeMeaningMinorCode: '1' }, { name: '2' }, { name: '3', outcomeMeaningMinorCode: '2' }] as any;

    outcomes = service['findFavourite'](outcomes, '1');
    expect(outcomes.map(outcome => outcome['name'])).toEqual(['2', '3', '1']);

    outcomes = service['findFavourite'](outcomes, '2');
    expect(outcomes.map(outcome => outcome['name'])).toEqual(['2', '1', '3']);

    outcomes = service['findFavourite'](outcomes, '3');
    expect(outcomes.map(outcome => outcome['name'])).toEqual(['2', '1', '3']);
  });

  it('findRunnerNumbers', () => {
    let outcomes = [{ runnerNumber: 1 }, {}, { runnerNumber: 2 }] as any;
    expect(service['findRunnerNumbers'](outcomes)).toBe(2);

    outcomes = [{}, {}, {}];
    expect(service['findRunnerNumbers'](outcomes)).toBe(0);
    expect(service['findRunnerNumbers']()).toBeUndefined();
  });

  it('getOutcomesWithoutFav', () => {
    let outcomes = [{ outcomeMeaningMinorCode: '1' }, {}, { outcomeMeaningMinorCode: '2' }] as any;
    expect(service['getOutcomesWithoutFav'](outcomes)).toBe(1);

    outcomes = [{ outcomeMeaningMinorCode: '3' }, {}, { outcomeMeaningMinorCode: '4' }];
    expect(service['getOutcomesWithoutFav'](outcomes)).toBe(3);
    expect(service['getOutcomesWithoutFav']()).toBeUndefined();
  });

  describe('orderOutcomesByName', () => {
    it('should separate sort runners and nonrunners by name', () => {
      const input = [{
        name: 'aname N/R'
      }, {
        name: 'bname',
      }, {
        name: 'aname',
      }, {
        name: 'Unnamed 2nd',
        outcomeMeaningMinorCode: 2
      }, {
        name: 'bname N/R'
      }, {
        name: 'Unnamed',
        outcomeMeaningMinorCode: 1
      }] as any;
      const res = service.orderOutcomesByName(input);
      expect(res).toEqual([{
        name: 'aname',
      }, {
        name: 'bname',
      }, {
        name: 'aname N/R',
        nonRunner: true
      }, {
        name: 'bname N/R',
        nonRunner: true
      }, {
        name: 'Unnamed',
        outcomeMeaningMinorCode: 1
      }, {
        name: 'Unnamed 2nd',
        outcomeMeaningMinorCode: 2
      }] as any);
    });

    it('should sort non runner outcomes by runner number if market is susp and there are no prices', () => {
      const input = [{
        name: 'aname N/R',
        runnerNumber: 3
      }, {
        name: 'bname N/R',
        runnerNumber: 1
      }, {
        name: 'aname',
      }, {
        name: 'unnamed 2nd',
      }] as any;
      const res = service.orderOutcomesByName(input);
      expect(res).toEqual([{
        name: 'aname',
      },  {
        name: 'unnamed 2nd',
      }, {
        name: 'bname N/R',
        runnerNumber: 1,
        nonRunner: true
      }, {
        name: 'aname N/R',
        runnerNumber: 3,
        nonRunner: true
      }] as any);
    });

    it('should sort non runner outcomes by name if market is susp and there are no prices', () => {
      const input = [{
        name: 'aname N/R'
      }, {
        name: 'bname N/R'
      }, {
        name: 'aname',
      }, {
        name: 'unnamed 2nd',
      }] as any;
      const res = service.orderOutcomesByName(input);
      expect(res).toEqual([{
        name: 'aname',
      }, {
        name: 'unnamed 2nd',
      }, {
        name: 'aname N/R',
        nonRunner: true
      }, {
        name: 'bname N/R',
        nonRunner: true
      }] as any);
    });

    it('should sort non runner outcomes by runner number if a > b', () => {
      const input = [{
        name: 'aname N/R',
        runnerNumber: 1
      }, {
        name: 'bname N/R',
        runnerNumber: 2
      }] as any;
      expect(service.orderOutcomesByName(input)).toEqual([{
        name: 'aname N/R',
        runnerNumber: 1,
        nonRunner: true
      }, {
        name: 'bname N/R',
        runnerNumber: 2,
        nonRunner: true
      }] as any);
    });

    it('should sort non runner outcomes by name if a.name < b.name', () => {
      const input = [{
        name: 'bname N/R'
      }, {
        name: 'aname N/R'
      }] as any;
      expect(service.orderOutcomesByName(input)).toEqual([{
        name: 'aname N/R',
        nonRunner: true
      }, {
        name: 'bname N/R',
        nonRunner: true
      }] as any);
    });

    it('should not sort runners by name', () => {
      const input = [{
        name: 'bname'
      }, {
        name: 'bname'
      }] as any;
      expect(service.orderOutcomesByName(input)).toEqual(input as any);
    });

    it('should not sort non runners by name', () => {
      const input = [{
        name: 'aname N/R'
      }, {
        name: 'aname N/R'
      }] as any;
      expect(service.orderOutcomesByName(input)).toEqual([{
        name: 'aname N/R',
        nonRunner: true
      }, {
        name: 'aname N/R',
        nonRunner: true
      }] as any);
    });

    it('should not sort non runners by runner number', () => {
      const input = [{
        name: 'aname N/R',
        runnerNumber: 1
      }, {
        name: 'aname N/R',
        runnerNumber: 1
      }] as any;
      expect(service.orderOutcomesByName(input)).toEqual([{
        name: 'aname N/R',
        runnerNumber: 1,
        nonRunner: true
      }, {
        name: 'aname N/R',
        runnerNumber: 1,
        nonRunner: true
      }] as any);
    });
  });

  describe('@sorting by trapNumber:', () => {
    it('orderOutcomeEntities and filterSpOutcomes', () => {
      const outcomes = [
        { runnerNumber: 2, trapNumber: 2, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 } },
        { runnerNumber: 1, trapNumber: 3, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 } },
        { runnerNumber: 3, trapNumber: 1, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 } }] as any;

      const sortedByTraps = [
        { runnerNumber: 3, trapNumber: 1, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 }, nonRunner: false },
        { runnerNumber: 2, trapNumber: 2, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 }, nonRunner: false },
        { runnerNumber: 1, trapNumber: 3, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 }, nonRunner: false }] as any;

      const sortedByRunNumbers = [
        { runnerNumber: 1, trapNumber: 3, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 }, nonRunner: false },
        { runnerNumber: 2, trapNumber: 2, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 }, nonRunner: false },
        { runnerNumber: 3, trapNumber: 1, name: 'Lorem', prices: { priceNum: 2, priceDen: 1 }, nonRunner: false }] as any;

      let test = outcomes;
      expect(service.orderOutcomeEntities(test, false, false,
        true, false, false, true)).toEqual(sortedByTraps);

      test = outcomes;
      expect(service.orderOutcomeEntities(test, false, false,
        true, false, false, false)).toEqual(sortedByRunNumbers);

      test = outcomes;
      expect(service.orderOutcomeEntities(test, true, false,
        true, false, false, true)).toEqual(sortedByTraps);

      test = outcomes;
      expect(service.orderOutcomeEntities(test, true, false,
        true, false, false, false)).toEqual(sortedByRunNumbers);
    });
  });
});
