import { PlaceLegPartService } from './place-leg-part.service';

describe('PlaceLegPartService', () => {
  let betSelections;
  let legPartService;

  let service;

  beforeEach(() => {
    betSelections = {
      getOutcome: jasmine.createSpy()
    };
    legPartService = {
      construct: jasmine.createSpy().and.returnValue({ outcome: { id: 123 } })
    };

    service = new PlaceLegPartService(legPartService, betSelections);
    service.range = null;
  });

  it('construct', () => {
    let params = {} as any;
    service.construct({}, params);
    expect(params.places).toEqual(undefined);

    params = { legParts: [] };
    service.construct({}, params);
    expect(params.places).toEqual(undefined);

    params = { legParts: [{}] };
    service.construct({}, params);
    expect(params.places).toEqual(undefined);

    params = { legParts: [{ places: 1, outcomeRef: { id: 0 } }, { places: 2, outcomeRef: { id: 1 } }], combi: 'FORECAST' };
    service.construct({ id: 1 }, params);
    expect(params.places).toEqual(2);

    params = { legParts: [{ places: 1, outcomeRef: { id: 0 } }, { places: 2, outcomeRef: { id: 1 } }], combi: 'TRICAST' };
    service.construct({ id: 1 }, params);
    expect(params.places).toEqual(2);
  });
});
