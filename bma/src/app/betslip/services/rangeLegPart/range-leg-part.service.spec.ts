import { RangeLegPartService } from './range-leg-part.service';

describe('RangeLegPartService', () => {
  let betSelections;
  let service;

  beforeEach(() => {
    betSelections = {
      getOutcome: jasmine.createSpy()
    };

    service = new RangeLegPartService(betSelections);
    service.range = null;
  });

  it('construct handicap', () => {
    service.construct({ id: '123' } as any, {
      handicap: {
        raw: '2',
        type: 'WH'
      }
    });

    expect(service.range).toEqual({
      type: 'WESTERN_HANDICAP',
      low: '2',
      high: '2'
    });
  });

  it('construct legParts handicap', () => {
    service.construct({} as any, {
      legParts: [{
        range: {
          rangeTypeRef: {
            id: 'WH'
          },
          low: '2',
          high: '2'
        }
      }]
    });

    expect(service.range).toEqual({
      type: 'WH',
      low: '2',
      high: '2'
    });
  });

  it('construct legParts handicap no rangeTypeRef', () => {
    service.construct({} as any, {
      legParts: [{
        range: {
          low: '2',
          high: '2'
        }
      }]
    });

    expect(service.range).toEqual({
      type: '',
      low: '2',
      high: '2'
    });
  });

  it('construct not handicap', () => {
    service.construct({} as any, {
      legParts: null
    });

    expect(service.range).toEqual(null);
  });
});
