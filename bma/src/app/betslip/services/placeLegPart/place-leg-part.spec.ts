import { PlaceLegPart } from './place-leg-part';

describe('PlaceLegPart', () => {
  let betSelections;
  let outcome;
  let params;

  let service;

  beforeEach(() => {
    betSelections = {
      getOutcome: jasmine.createSpy()
    };
    outcome = {
      id: '123'
    };
    params = {};

    service = new PlaceLegPart(betSelections, outcome, params);
    service.range = null;
  });

  it('getPlaces', () => {
    expect(service.getPlaces({ places: '' })).toEqual('');
    expect(service.getPlaces({ places: { 123: {}}})).toEqual({});
    expect(service.getPlaces({ places: {}})).toEqual('*');
  });

  it('get data', () => {
    service.places = {};
    expect(service.data).toEqual({});
  });

  it('set data', () => {
    service.data = { test: 123 };
    expect(service.places).toEqual({ test: 123 });
  });

  it('doc', () => {
    expect(service.doc()).toEqual({ legPart: [{ outcomeRef: { id: '123' }}] });
    service.places = { test: 123 };
    expect(service.doc()).toEqual({ legPart: [{ places: { test: 123 }, outcomeRef: { id: '123' }}] });
  });
});
