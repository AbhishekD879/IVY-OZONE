import { ForecastSportsLegService } from '@betslip/services/forecastSportsLeg/forecast-sports-leg.service';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { LegPartService } from '@betslip/services/legPart/leg-part.service';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { PlaceLegPartService } from '@betslip/services/placeLegPart/place-leg-part.service';
import * as _ from 'underscore';
import { IOutcomePrice } from '@core/models/outcome-price.model';

describe('ForecastSportsLegService', () => {
  let forecastSportsLegService: ForecastSportsLegService;
  let betSelectionService: BetSelectionsService;
  let legPartService: LegPartService;
  let sportsLegPriceService: SportsLegPriceService;

  const betSelection: IBetSelection = {
    id: 'testid',
    type: 'COMBI',
    winPlace: 'EXPLICIT_PLACES',
    price: { id: 'test1'} as IOutcomePrice
  } as IBetSelection;

  beforeEach(() => {
    betSelectionService = jasmine.createSpyObj({
      mapParsed: jasmine.createSpy()
    });

    legPartService = jasmine.createSpyObj({
      construct: jasmine.createSpy()
    });

    sportsLegPriceService = jasmine.createSpyObj({
      construct: jasmine.createSpy()
    });

    forecastSportsLegService = new ForecastSportsLegService(sportsLegPriceService, legPartService, betSelectionService);
  });

  it('constructor', () => {
    expect(forecastSportsLegService).toBeTruthy();
    expect(forecastSportsLegService.partsType).toEqual(jasmine.any(PlaceLegPartService));
  });

  it('construct: should call extenDefault method', () => {
    spyOn(forecastSportsLegService, 'extendDefault').and.callThrough();
    forecastSportsLegService.construct(betSelection, 10);

    expect(forecastSportsLegService.extendDefault).toHaveBeenCalledWith(betSelection);
  });

  it('extendDefault: Underscore extends should be called', () => {
    spyOn(_, 'extend').and.callThrough();
    const result = forecastSportsLegService.extendDefault(betSelection);
    expect(result).toEqual({
      combi: 'COMBI',
      places: '',
      id: 'testid',
      type: 'COMBI',
      winPlace: 'EXPLICIT_PLACES',
      price: { id: 'test1', priceType: 'DIVIDEND', type: 'DIVIDEND', props: {} }
    } as IBetSelection);
    expect(_.extend).toHaveBeenCalledTimes(2);
  });
});
