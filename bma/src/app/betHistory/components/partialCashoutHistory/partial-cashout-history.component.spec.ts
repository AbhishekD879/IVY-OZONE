import { PartialCashoutHistoryComponent } from './partial-cashout-history.component';

describe('PartialCashoutHistoryComponent', () => {
  let component, timeFactory, toolsService;

  const terms: any = [
    {
      stake: {
        value: '200.20'
      },
      reasonCode: 'ODDS_BOOST',
      stakeUsed: '0.00'
    },
    {
      cashoutType: 'cashoutType',
      cashoutValue: '90',
      stakeUsed: '100',
      stake: {
        value: '100.20'
      },
      reasonCode: 'PARTIAL_CASHOUT'
    },
    {
      cashoutType: 'cashoutType',
      cashoutValue: '10',
      stakeUsed: '110',
      stake: {
        value: '90'
      },
      reasonCode: 'PARTIAL_CASHOUT'
    },
  ];

  beforeEach(() => {
    timeFactory = {
      getLocalDateFromString: jasmine.createSpy()
    };
    toolsService = {
      roundTo: jasmine.createSpy('roundTo').and.returnValue(1.15)
    };

    component = new PartialCashoutHistoryComponent(timeFactory, toolsService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    // value which returned by spy of toolsService
    const cashOutResult: string = '1.15';
    // rounded sum of stake.value
    const currencySymbol = '$';

    component.terms = terms;
    component.currencySymbol = currencySymbol;
    component.ngOnInit();

    expect(component.hasCashouts).toBeTruthy();
    expect(component.remainingStake).toEqual(terms[2].stake.value);
    expect(component.terms[0].stakeUsed).toEqual('0.00');
    expect(component.totalCashedOut).toEqual(cashOutResult);
    expect(component.totalCashOutStake).toEqual(cashOutResult);
    expect(toolsService.roundTo).toHaveBeenCalledTimes(6);
    expect(component.partialHistory).toEqual([terms[1], terms[2]]);
  });

  it('getDate', () => {
    const date: string = new Date().toString();
    component.getDate(date);

    expect(timeFactory.getLocalDateFromString).toHaveBeenCalledWith(date);
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      component['calcSummary'] = jasmine.createSpy();
    });

    it('terms changed', () => {
      component.terms = [{
        reasonCode: 'PARTIAL_CASHOUT',
        stake: {
          value: 5.99
        }
      } as any];

      component.ngOnChanges({
        terms: { currentValue: component.terms }
      } as any);
      expect(component['calcSummary']).toHaveBeenCalledTimes(1);
    });

    it('terms changed', () => {
      component.ngOnChanges({
        terms: { currentValue: null }
      } as any);
      expect(component['calcSummary']).not.toHaveBeenCalled();
    });

    it('terms not changed', () => {
      component.ngOnChanges({ currencySymbol: '$' } as any);
      expect(component['calcSummary']).not.toHaveBeenCalled();
    });
  });

  it('trackByBetTermsChange should return joined string', () => {
    const index: number = 11;
    const item: any = {
      date: '101010',
      changeNo: '22',
      stake: {
        value: 1
      }
    };
    const result = component.trackByBetTermsChange(index, item);

    expect(result).toEqual('11101010221');
  });

  describe('checkIfHasPartialChashouts', () => {
    it('should return false if no terms provided', () => {
      expect(component['checkIfHasPartialChashouts'](undefined)).toBeFalsy();
    });
    it('should return false if no partial cashout reason terms', () => {
      const termsParam = [
        {
          reasonCode: 'SOME_REASON',
          stake: {
            value: 5.99
          }
        }
      ];
      expect(component['checkIfHasPartialChashouts'](termsParam as any)).toBeFalsy();
    });
    it('should return false if no positive stake terms', () => {
      const termsParam = [
        {
          reasonCode: 'PARTIAL_CASHOUT',
          stake: {
            value: 0
          }
        }
      ];
      expect(component['checkIfHasPartialChashouts'](termsParam as any)).toBeFalsy();
    });
    it('should return true if there are partial cashout reason with positive stake',
      () => {
      const termsParam = [
        {
          reasonCode: 'PARTIAL_CASHOUT',
          stake: {
            value: 5.99
          }
        }
      ];
      expect(component['checkIfHasPartialChashouts'](termsParam as any)).toBeTruthy();
    });
  });

  describe('@calcSummary', () => {
    it('should calculate summary values', () => {
      component.terms = terms;

      component['calcSummary']();

      expect(component.totalCashedOut).toEqual('1.15');
      expect(component.totalCashOutStake).toEqual('1.15');
      expect(toolsService.roundTo).toHaveBeenCalledTimes(6);
    });
  });

  describe('initialize', () => {
    it('should`t call calcSummary terms are not have partial cashout', () => {
      spyOn(component as any, 'calcSummary');
      component.terms = [];
      component['initialize']();
      expect(component['calcSummary']).not.toHaveBeenCalled();
    });
  });
});
