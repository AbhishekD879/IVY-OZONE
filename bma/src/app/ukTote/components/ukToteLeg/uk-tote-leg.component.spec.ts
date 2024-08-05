import { SimpleChanges } from '@angular/core';
import { UkToteLegComponent } from '@uktote/components/ukToteLeg/uk-tote-leg.component';
import { IOutcome } from '@core/models/outcome.model';
import { FRACTIONAL_TO_DECIMAL_MAP } from '@core/services/constants/frac-to-dec.constant';

describe('UkToteLegComponent', () => {
  let component;
  let ukToteService;
  let deviceService;
  let pubSubService;
  let fracToDecService;
  const sortedOutcomes = [];

  beforeEach(() => {
    ukToteService = {
      sortOutcomes: jasmine.createSpy('sortOutcomes').and.returnValue(sortedOutcomes),
      getRaceTitle: jasmine.createSpy('getRaceTitle').and.returnValue('race title'),
      isOutcomeSuspended: jasmine.createSpy('isOutcomeSuspended').and.returnValue(false)
    };
    pubSubService =  {
      API: {
        UK_TOTE_LEG_UPDATED: 'UK_TOTE_LEG_UPDATED'
      },
      publish: jasmine.createSpy('publish')
    };
    fracToDecService = {
      oddsFormat: 'frac',
      getFormattedValue: (priceNum: number, priceDen: number) => {
        if (fracToDecService.oddsFormat === 'frac') {
          return `${priceNum}/${priceDen}`;
        }
        const predefinedDecimalValue = FRACTIONAL_TO_DECIMAL_MAP[`${priceNum}/${priceDen}`];

        if (predefinedDecimalValue) {
          return predefinedDecimalValue;
        }

        return (1 + (priceNum / priceDen)).toFixed(2);
      }
    }
    component = new UkToteLegComponent(ukToteService, deviceService, fracToDecService, pubSubService);
  });

  it('ngOnInit', () => {
    component['initData'] = jasmine.createSpy('initData');
    component.ngOnInit();
    expect(component['initData']).toHaveBeenCalled();
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      component['initData'] = jasmine.createSpy('initData');
    });

    it( 'no current value for toteLegVal in changes', () => {
      const changes = {
        toteLegVal: {
          firstChange: true,
          currentValue: undefined,
          previousValue: null,
          isFirstChange: () => true
        }
      } as SimpleChanges;
      component.expandedSummary = [ true ];
      component.ngOnChanges(changes);
      expect(component['initData']).not.toHaveBeenCalled();
      expect(component.expandedSummary).toEqual(jasmine.arrayContaining([ true ]));
    });

    it('no previous value for toteLegVal in changes', () => {
      const changes = {
        toteLegVal: {
          firstChange: true,
          currentValue: {},
          previousValue: undefined,
          isFirstChange: () => true
        }
      } as SimpleChanges;
      component.expandedSummary = [ true ];
      component.ngOnChanges(changes);
      expect(component['initData']).not.toHaveBeenCalled();
      expect(component.expandedSummary).toEqual(jasmine.arrayContaining([ true ]));
    });

    it('previous and current values for toteLegVal in changes', () => {
      const changes = {
        toteLegVal: {
          firstChange: false,
          currentValue: {},
          previousValue: {},
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component.expandedSummary = [ true ];
      component.ngOnChanges(changes);
      expect(component['initData']).toHaveBeenCalled();
      expect(component.expandedSummary).toEqual(jasmine.arrayContaining([]));
    });
  });

  it('trackByOutcomes', () => {
    const index = 5;
    const outcome = { id: '8' } as IOutcome;
    const result = component.trackByOutcomes(index, outcome);
    expect(result).toBe('8');
  });

  it('get toteLeg', () => {
    const toteLegValue = {};
    component.toteLegVal = toteLegValue;
    expect(component.toteLeg).toBe(toteLegValue);
  });

  it('get market outcomes when no marketEntity', () => {
    const result = component['getMarketOutcomes']();
    expect(result).toEqual(sortedOutcomes);
    expect(ukToteService.sortOutcomes).toHaveBeenCalledWith(jasmine.arrayContaining([]));
  });

  it('get market outcomes when marketEntity is set', () => {
    const outcomes = [];
    component.toteLegVal = {
      event: {
        markets: [ { outcomes } ]
      }
    };
    const result = component['getMarketOutcomes']();
    expect(result).toBe(sortedOutcomes);
    expect(ukToteService.sortOutcomes).toHaveBeenCalledWith(outcomes);
  });

  describe('get marketEntity', () => {
    it('no toteLeg', () => {
      component.toteLegVal = null;
      const result = component.marketEntity;
      expect(result).toBeNull();
    });

    it('no event', () => {
      component.toteLegVal = { event: null };
      const result = component.marketEntity;
      expect(result).toBeNull();
    });

    it('no markets', () => {
      component.toteLegVal = {
        event: {
          markets: null
        }
      };
      const result = component.marketEntity;
      expect(result).toBeNull();
    });

    it('no first market', () => {
      component.toteLegVal = {
        event: {
          markets: []
        }
      };
      const result = component.marketEntity;
      expect(result).toBeUndefined();
    });

    it('should return market', () => {
      const market = {};
      component.toteLegVal = {
        event: {
          markets: [ market ]
        }
      };
      const result = component.marketEntity;
      expect(result).toBe(market);
    });
  });

  describe('get eventEntity', () => {
    it('no toteLeg', () => {
      component.toteLegVal = null;
      const result = component.eventEntity;
      expect(result).toBeNull();
    });

    it('no event', () => {
      component.toteLegVal = { event: null };
      const result = component.eventEntity;
      expect(result).toBeNull();
    });

    it('should return event', () => {
      const event = {};
      component.toteLegVal = { event };
      const result = component.eventEntity;
      expect(result).toBe(event);
    });
  });

  describe('get raceTitle', () => {
    it('no event', () => {
      component.toteLegVal = {};
      const result = component['getRaceTitle']();
      expect(result).toBe('');
      expect(ukToteService.getRaceTitle).not.toHaveBeenCalled();
    });

    it('should get title from event', () => {
      component.toteLegVal = { event: {} };
      const result = component['getRaceTitle']();
      expect(result).toBe('race title');
      expect(ukToteService.getRaceTitle).toHaveBeenCalledWith(component.toteLeg.event);
    });
  });

  describe('onExpandSummary', () => {
    it('no item by index', () => {
      component.expandedSummary = [];
      component.onExpandSummary(0);
      expect(component.expandedSummary[0]).toBeTruthy();
    });

    it('should toggle item value', () => {
      component.expandedSummary = [ true ];
      component.onExpandSummary(0);
      expect(component.expandedSummary[0]).toBeFalsy();
    });
  });

  describe('selectOutcome', () => {
    it('outcome is not selected', () => {
      const outcomeId = '83729';
      component.toteLegVal = {
        isOutcomeSelected: jasmine.createSpy().and.returnValue(false),
        selectOutcome: jasmine.createSpy()
      };
      component.selectOutcome(outcomeId);
      expect(component.toteLeg.isOutcomeSelected).toHaveBeenCalledWith(outcomeId);
      expect(component.toteLeg.selectOutcome).toHaveBeenCalledWith(outcomeId);
      expect(component.pubSubService.publish).toHaveBeenCalledWith(
        component.pubSubService.API.UK_TOTE_LEG_UPDATED,
        component.toteLeg
      );
    });

    it('outcome is selected', () => {
      const outcomeId = '5456461';
      component.toteLegVal = {
        isOutcomeSelected: jasmine.createSpy().and.returnValue(true),
        deselectOutcome: jasmine.createSpy()
      };
      component.selectOutcome(outcomeId);
      expect(component.toteLeg.isOutcomeSelected).toHaveBeenCalledWith(outcomeId);
      expect(component.toteLeg.deselectOutcome).toHaveBeenCalledWith(outcomeId);
      expect(component.pubSubService.publish).toHaveBeenCalledWith(
        component.pubSubService.API.UK_TOTE_LEG_UPDATED,
        component.toteLeg
      );
    });
  });

  describe('checkIfOutcomeSuspended', () => {
    it('isPoolBetSuspended true, isOutcomeSuspended true, outcomeEntity.nonRunner false', () => {
      const outcomeEntity = { nonRunner: false };
      component.isPoolBetSuspended = true;
      component['isOutcomeSuspended'] = jasmine.createSpy().and.returnValue(true);
      const result = component.checkIfOutcomeSuspended(outcomeEntity);
      expect(component['isOutcomeSuspended']).toHaveBeenCalledWith(outcomeEntity);
      expect(result).toBeTruthy();
    });

    it('toteLeg.isSuspended true, isOutcomeSuspended false', () => {
      const outcomeEntity = {};
      component.isPoolBetSuspended = false;
      component.toteLegVal = { isSuspended: true };
      component['isOutcomeSuspended'] = jasmine.createSpy().and.returnValue(false);
      const result = component.checkIfOutcomeSuspended(outcomeEntity);
      expect(component['isOutcomeSuspended']).toHaveBeenCalledWith(outcomeEntity);
      expect(result).toBeTruthy();
    });

    it('toteLeg.isSuspended false, isOutcomeSuspended true, outcomeEntity.nonRunner true', () => {
      const outcomeEntity = { nonRunner: true };
      component.isPoolBetSuspended = false;
      component.toteLegVal = { isSuspended: false };
      component['isOutcomeSuspended'] = jasmine.createSpy().and.returnValue(true);
      const result = component.checkIfOutcomeSuspended(outcomeEntity);
      expect(component['isOutcomeSuspended']).toHaveBeenCalledWith(outcomeEntity);
      expect(result).toBeFalsy();
    });

    it('isWholeBetSuspended false, isOutcomeSuspended true', () => {
      const outcomeEntity = { nonRunner: false };
      component.isPoolBetSuspended = false;
      component.toteLegVal = { isSuspended: false };
      component['isOutcomeSuspended'] = jasmine.createSpy().and.returnValue(true);
      const result = component.checkIfOutcomeSuspended(outcomeEntity);
      expect(component['isOutcomeSuspended']).toHaveBeenCalledWith(outcomeEntity);
      expect(result).toBeTruthy();
    });
  });

  it('isOutcomeSuspended', () => {
    const outcome = {};
    const result = component['isOutcomeSuspended'](outcome);
    expect(component.ukToteService.isOutcomeSuspended).toHaveBeenCalledWith(outcome);
    expect(result).toBeFalsy();
  });

  it('initData', () => {
    const outcome = {};
    const marketOutcomes = [outcome];
    const title = 'Race title';
    component['checkIfOutcomeSuspended']
      = jasmine.createSpy('checkIfOutcomeSuspended').and.returnValue(true);
    component['getMarketOutcomes'] = jasmine.createSpy('getMarketOutcomes').and.returnValue(marketOutcomes);
    component['getRaceTitle'] = jasmine.createSpy('getRaceTitle').and.returnValue(title);
    component.toteLegVal = {
      event: {
        markets: [
          {
            outcomes: [outcome]
          }
        ]
      }
    } as any;

    component['initData']();

    expect(component['getMarketOutcomes']).toHaveBeenCalled();
    expect(component['getRaceTitle']).toHaveBeenCalled();
    expect(component['checkIfOutcomeSuspended']).toHaveBeenCalledWith(outcome);
    expect(component.market).toBe(component.toteLegVal.event.markets[0]);
    expect(component.event).toBe(component.toteLegVal.event);
    expect(component.marketOutcomes).toBe(marketOutcomes);
    expect(component.raceTitle).toBe(title);
    expect(component.outcomeSuspensionStatuses).toEqual([true]);
  });
  it('should call fracToDec', () => {
    fracToDecService.oddsFormat = 'frac';
    expect(component.fracToDec(9,2)).toBe('9/2');
    fracToDecService.oddsFormat = 'decimal';
    expect(component.fracToDec(9,2)).toBe('5.50');
    fracToDecService.oddsFormat = 'frac';
    expect(component.fracToDec(undefined,2)).toBe('undefined/2');
  });
});
