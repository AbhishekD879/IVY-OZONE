import { Leg } from './leg';

describe('Leg', () => {
  let leg: Leg;
  let betSelections;
  let selection;
  let partsType;

  beforeEach(() => {
    betSelections = {
      getOutcome: jasmine.createSpy('getOutcome')
    };
    selection = {
      outcomes: [{}]
    };
    partsType = {
      construct: jasmine.createSpy('construct')
    };

    leg = new Leg(
      betSelections,
      selection,
      1,
      partsType
    );
  });

  it('constructor', () => {
    expect(partsType.construct).toHaveBeenCalledTimes(1);
  });

  it('get firstOutcomeId', () => {
    leg.parts = [{
      outcome: { id: 1}
    }] as any[];
    expect(leg.firstOutcomeId).toBe(1);
  });

  it('should create leg without partsType service', () => {
    expect( new Leg(betSelections, selection, 1) ).toBeTruthy();
  });
});
