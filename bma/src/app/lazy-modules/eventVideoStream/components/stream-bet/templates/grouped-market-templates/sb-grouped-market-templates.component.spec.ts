import { SbGroupedMarketTemplatesComponent } from './sb-grouped-market-templates.component';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

describe('SbGroupedMarketTemplatesComponent', () => {
  let component: SbGroupedMarketTemplatesComponent;
  const market = {
    cashoutAvail: '',
    correctPriceTypeCode: '',
    dispSortName: '',
    eachWayFactorNum: '',
    eachWayFactorDen: '',
    eachWayPlaces: '',
    id: 'market-1',
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
    outcomes: [{id: '1', name: 'outcome1'}, {id: '2', name: 'outcome2'}],
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

  describe('SbGroupedMarketTemplatesComponent', () => {  
    beforeEach(() => {
      
      component = new SbGroupedMarketTemplatesComponent();    
    });
  
    it('SbGroupedMarketTemplatesComponent: should create component instance', () => {
      expect(component).toBeTruthy();
    });

    it('SbGroupedMarketTemplatesComponent: ngOnInit should init the component and initial market of template type: Special', () => {
      component.templateType = 'special-market';
      component.markets = [market];
      component.ngOnInit();
      expect(component.initialMarket).toEqual([component.markets[0]]);  
    });

    it('SbGroupedMarketTemplatesComponent: ngOnInit should init the component and initial market of template type: Non-Special', () => {
      component.templateType = 'market';
      component.markets = [market];
      component.ngOnInit();
      expect(component.initialMarket).toEqual([component.markets[0]]);  
    });
  
    it('SbGroupedMarketTemplatesComponent: getTrackById should track by id', () => {
      const entity = {
        id: 111
      };
      const result = component.getTrackById(0, entity);
      expect(result).toBe('111_0');
    });
  
    it('SbGroupedMarketTemplatesComponent: handleSelectionClick', () => {
      
      component.selectionClickEmit.emit = jasmine.createSpy();
      component.handleSelectionClick(market);
      expect(component.selectionClickEmit.emit).toHaveBeenCalled();
    });

    it('SbGroupedMarketTemplatesComponent: getNextOutcome', () => {
      component.templateType === 'market';
      component.markets = [market];
      component.initialMarket = [market];
      component.getNextOutcome();
      expect(component.initialMarket).toEqual([component.markets[0]]);  
    });

    it('SbGroupedMarketTemplatesComponent: getNextOutcome#fetch next market', () => {
      const market2 = {...market, id: 'market-2'};
      component.templateType === 'market';
      component.markets = [market, market2];
      component.initialMarket = [market];
      component.getNextOutcome();
      expect(component.initialMarket).toEqual([component.markets[1]]);  
    });

    it('SbGroupedMarketTemplatesComponent: getPreviousOutcome', () => {
      component.templateType === 'market';
      component.markets = [market];
      component.initialMarket = [market];
      component.getPreviousOutcome();
      expect(component.initialMarket).toEqual([component.markets[0]]);  
    });

    it('SbGroupedMarketTemplatesComponent: getPreviousOutcome#fetch prev market', () => {
      const market2 = {...market, id: 'market-2'};
      component.templateType === 'market';
      component.markets = [market, market2];
      component.initialMarket = [market2];
      component.getPreviousOutcome();
      expect(component.initialMarket).toEqual([component.markets[0]]);  
    });

    it('SbGroupedMarketTemplatesComponent: getNextOutcome with template-special-market', () => {
      component.templateType = 'special-market';
      component.markets = [market];
      component.marketOutcomePairs = [{outcome: {id: '1', name: 'outcome1'}, market}, {outcome: {id: '2', name: 'outcome2'}, market}];
      component.marketOutcomePair = component.marketOutcomePairs[0];
      // component.initialMarket = [market];
      component.getNextOutcome();
      expect(component.marketOutcomePair).toEqual(component.marketOutcomePairs[1]);  
    });

    it('SbGroupedMarketTemplatesComponent: getNextOutcome#fetch next outcome with template-special-market', () => {
      component.templateType = 'special-market';
      component.markets = [market];
      component.marketOutcomePairs = [{outcome: {id: '1', name: 'outcome1'}, market}, {outcome: {id: '2', name: 'outcome2'}, market}];
      component.marketOutcomePair = component.marketOutcomePairs[1];
      component.getNextOutcome();
      expect(component.marketOutcomePair).toEqual(component.marketOutcomePairs[0]);  
    });

    it('SbGroupedMarketTemplatesComponent: getPreviousOutcome with template-special-market', () => {
      component.templateType = 'special-market';
      component.markets = [market];
      component.marketOutcomePairs = [{outcome: {id: '1', name: 'outcome1'} as IOutcome, market}, {outcome: {id: '2', name: 'outcome2'} as IOutcome, market}];
      component.marketOutcomePair = component.marketOutcomePairs[0];
      // component.initialMarket = [market];
      component.getPreviousOutcome();
      expect(component.marketOutcomePair).toEqual(component.marketOutcomePairs[1]);  
    });

    it('SbGroupedMarketTemplatesComponent: getPreviousOutcome#fetch prev outcome with template-special-market', () => {
      component.templateType = 'special-market';
      component.markets = [market];
      component.marketOutcomePairs = [{outcome: {id: '1', name: 'outcome1'}, market}, {outcome: {id: '2', name: 'outcome2'}, market}];
      component.marketOutcomePair = component.marketOutcomePairs[1];
      component.getPreviousOutcome();
      expect(component.marketOutcomePair).toEqual(component.marketOutcomePairs[0]);  
    });
  });
});
