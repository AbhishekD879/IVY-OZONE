import { BetSelectionService } from './bet-selection.service';

describe('Testing BetSelection', () => {
  let service;
  let mockSelection;
  let outcome;

  beforeEach(() => {
    outcome = {
      errorMsg: 'Event Suspended',
      id: '430582695',
      prices: [{
        priceDen: '1',
        priceNum: '2',
        priceType: 'LP'
      }]
    };
    mockSelection = {
      linePicks : {},
      outcomes: [outcome],
      goToBetslip: false,
      winPlace: 'EACH_WAY',
      id: 'SGL|430582695',
      hasBPG: false,
      eventIsLive: true,
      hasEachWay: false,
      price: {
        priceType: 'LP',
        priceNum: '8',
        priceDen: '1'
      },
      details: {},
      isVirtual: false
    };
    service = new BetSelectionService();
  });

  it('should pass correct params format to BetSelection.zip method', () => {
    const selection = service.construct(mockSelection),
      result = selection.zip();

    expect(result.isSuspended).toEqual(true);
    expect(result.outcomesIds).toEqual(['430582695']);
    expect(result.id).toEqual('SGL|430582695');
    expect(result.isVirtual).toEqual(false);
  });

  it('should return correct price', () => {
    const selection = service.construct(mockSelection);

    expect(selection.price).toEqual(outcome.prices[0]);
    delete selection.selectionPrice;
    expect(selection.price).toEqual(outcome.prices[0]);
  });

  it('should extend price', () => {
    const newPrice = {
      priceDen: '10',
      priceNum: '12'
    };
    const selection = service.construct(mockSelection);

    selection.price = newPrice;

    expect(selection.selectionPrice).toEqual(jasmine.objectContaining(newPrice));
  });

  it('should parse correct price', () => {
    mockSelection.outcomes = [];
    mockSelection.price = null;
    const selection = service.construct(mockSelection);

    expect(selection.price).toEqual({});
  });

  it('should store correct price type', () => {
    mockSelection.price.priceType = 'SP';
    const selection = service.construct(mockSelection);

    expect(selection.price).toEqual({
      priceDen: '1',
      priceNum: '2',
      priceType: 'SP'
    });
  });

  it('should restoreSelections', () => {
    const outcomes = [
      {
        id: '1',
        details: {
          isRacing: true,
          isEachWayAvailable: true,
          isGpAvailable: true
        }
      },
      {
        id: '3',
        details: {
          isRacing: true
        }
      }
    ];
    
    const selections = [{isLotto :true, outcomesIds: ['1', '2'] ,outcomes: outcomes, details: {}}];
    const restoredSelections = service.restoreSelections(<any>selections, <any>outcomes);
    restoredSelections[0].errs = <any>[{ code: 100 }];
    expect(restoredSelections[0].isRacing).toEqual(true);
    expect(restoredSelections[0].errs[0].code).toEqual(100);
    expect(restoredSelections[0].isMatch(10)).toEqual(false);
  });

  it('should pass params to bet with empty details', () => {
    mockSelection = {
      linePicks : {},
      goToBetslip: false,
      id: 'SGL|123',
      price: {
        priceType: 'LP',
        priceNum: '8',
        priceDen: '1'
      },
      isVirtual: false
    };
    const selection = service.construct(mockSelection),
    result = selection.zip();
    expect(result.goToBetslip).toEqual(false);
  });


  it('should pass correct params format to bet details with selections or stake', () => {
    mockSelection = {
      linePicks : {},
      goToBetslip: false,
      winPlace: 'EACH_WAY',
      id: 'SGL|123',
      price: {
        priceType: 'LP',
        priceNum: '8',
        priceDen: '1'
      },
      details: {stake: '0.01', selections: '1', draws:[{id:234}]},
      isVirtual: false,
      isLotto: true
    };
    const selection = service.construct(mockSelection),
    result = selection.zip();
    expect(result.isLotto).toEqual(true);
  });
});
