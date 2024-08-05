import { LegPart } from './leg-part';

describe('LegPart', () => {
  let legPart: LegPart;
  let betSelectionsService;
  let outcomeParam;

  beforeEach(() => {
    betSelectionsService = {
      getOutcome: jasmine.createSpy('getOutcome').and.returnValue({})
    };
    outcomeParam = {};

    legPart = new LegPart(
      betSelectionsService,
      outcomeParam
    );
  });

  it('doc', () => {
    expect(legPart.doc()).toEqual(jasmine.any(Object));
  });

  it('set outcome from param', () => {
    betSelectionsService.getOutcome.and.returnValue(null);
    const param: any = {};
    expect(new LegPart(betSelectionsService, param).outcome).toBe(param);
  });
});
