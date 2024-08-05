import { RangeLegPart } from './range-leg-part';

describe('RangeLegPart', () => {
  let betSelections;
  const outcome = {} as any;
  const range = {
    high: '2',
    low: '1',
    type: 'HANDICAP'
  };
  let service;

  beforeEach(() => {
    betSelections = {
      getOutcome: jasmine.createSpy().and.returnValue({ id: '123' })
    };

    service = new RangeLegPart(
      betSelections,
      outcome,
      range
    );
  });

  it('constructor', () => {
    expect(service.outcome).toEqual({ id: '123' });
    expect(service.range).toEqual(range);

    betSelections = {
      getOutcome: jasmine.createSpy()
    };

    service = new RangeLegPart(
      betSelections,
      outcome,
      range
    );

    expect(service.outcome).toEqual({});
    expect(service.range).toEqual(range);
  });

  it('doc', () => {
    expect(service.doc()).toEqual({ legPart: [{
      range: {
        low: '1',
        high: '2',
        rangeTypeRef: { id: 'HANDICAP' }
      },
      outcomeRef: { id: '123' }
    }]});
  });
});
