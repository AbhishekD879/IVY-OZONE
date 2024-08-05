import { SbRacingMarketItemComponent } from './sb-racing-market-item.component';
import { IMarket } from '@core/models/market.model';

describe('SbRacingMarketItemComponent', () => {
  let component: SbRacingMarketItemComponent;
  let raceOutcomeDetailsService;

  beforeEach(() => {
    raceOutcomeDetailsService = {
      isNumberNeeded: jasmine.createSpy()
    };
    component = new SbRacingMarketItemComponent(raceOutcomeDetailsService);    
  });

  it('SbRacingMarketItemComponent: should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('SbRacingMarketItemComponent: getTrackById should track by id', () => {
    const entity = {
      id: 111
    };
    const result = component.getTrackById(0, entity);
    expect(result).toBe('111_0');
  });

  it('SbRacingMarketItemComponent: handleSelectionClick', () => {
    const market = {
      cashoutAvail: '',
      correctPriceTypeCode: '',
      dispSortName: '',
      eachWayFactorNum: '',
      eachWayFactorDen: '',
      eachWayPlaces: '',
      id: '',
      isLpAvailable: true,
      isMarketBetInRun: true,
      isSpAvailable: true,
      liveServChannels: '',
      isEachWayAvailable: false,
      liveServChildrenChannels: '',
      marketsNames: '',
      marketStatusCode: '',
      name: '',
      nextScore: 0,
      outcomes: [],
      periods: [],
      priceTypeCodes: '',
      terms: '',
      templateMarketId: 0,
      templateMarketName: '',
      viewType: 'inplay',
      label: 'label',
      isTopFinish: true,
      isToFinish: false,
      insuranceMarkets: false,
      isOther: true,
      isWO: false
    } as IMarket;
    component.selectionClickEmit.emit = jasmine.createSpy();
    component.handleSelectionClick(market);
    expect(component.selectionClickEmit.emit).toHaveBeenCalled();
  });
});
