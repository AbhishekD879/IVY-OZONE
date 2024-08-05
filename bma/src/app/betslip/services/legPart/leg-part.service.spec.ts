import { LegPartService } from '@betslip/services/legPart/leg-part.service';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { LegPart } from '@betslip/services/legPart/leg-part';

describe('LegPartService', () => {
  let legPartService: LegPartService;
  let betSelectionService: BetSelectionsService;

  const selection: any = jasmine.createSpyObj({
    id: jasmine.createSpy()
  });

  beforeEach(() => {
    betSelectionService = jasmine.createSpyObj({
      getOutcome: jasmine.createSpy()
    });

    legPartService = new LegPartService(betSelectionService);
  });

  it('constructor', () => {
    expect(legPartService).toBeTruthy();
  });

  it('construct: should construct LegPart item', () => {
    const result = legPartService.construct(selection);
    expect(betSelectionService.getOutcome).toHaveBeenCalled();
    expect(result).toEqual(jasmine.any(LegPart));
  });
});
