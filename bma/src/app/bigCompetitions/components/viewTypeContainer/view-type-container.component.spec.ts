import {
  ViewTypeContainerComponent
} from '@app/bigCompetitions/components/viewTypeContainer/view-type-container.component';
import { ICompetitionMarket } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

describe('ViewTypeContainerComponent', () => {

  let component: ViewTypeContainerComponent;

  let sbFiltersService;

  const updatedOutcomes = [];
  const market = {
    data: {
      markets: [
        {
          outcomes: [],
          isLpAvailable: true
        }
      ]
    }
  } as ICompetitionMarket;

  beforeEach(() => {
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy().and.returnValue(updatedOutcomes)
    };

    component = new ViewTypeContainerComponent(sbFiltersService);
    component.market = market;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.ngOnInit();
    expect(sbFiltersService.orderOutcomeEntities)
      .toHaveBeenCalledWith(market.data.markets[0].outcomes, market.data.markets[0].isLpAvailable);
    expect(market.data.markets[0].outcomes).toBe(updatedOutcomes);
  });

  it('#ngOnInit when market.data = undefined', () => {
    component.market.data = undefined;
    component.ngOnInit();
    expect(sbFiltersService.orderOutcomeEntities).not.toHaveBeenCalled();
  });
});
