import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { HandicapSportsLegService } from '@betslip/services/handicapSportsLeg/handicap-sports-leg.service';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';
import { RangeLegPartService } from '@betslip/services/rangeLegPart/range-leg-part.service';

describe('HandicapSportsLegService', () => {
  let handicapSportsLegService: HandicapSportsLegService;
  let betSelectionService: BetSelectionsService;
  let sportsLegPriceService: SportsLegPriceService;

  const betSelection: IBetSelection = jasmine.createSpyObj({
    id: jasmine.createSpy()
  });

  beforeEach(() => {
    betSelectionService = jasmine.createSpyObj({
      mapParsed: jasmine.createSpy()
    });

    sportsLegPriceService = jasmine.createSpyObj({
      construct: jasmine.createSpy()
    });

    handicapSportsLegService = new HandicapSportsLegService(sportsLegPriceService, betSelectionService);
  });

  it('constructor', () => {
    expect(handicapSportsLegService).toBeTruthy();
    expect(handicapSportsLegService.partsType).toEqual(jasmine.any(RangeLegPartService));
  });

  it('construct: should return Leg instance', () => {
    const result = handicapSportsLegService.construct(betSelection, 1);
    expect(result).toEqual(jasmine.any(SportsLeg));
  });
});
