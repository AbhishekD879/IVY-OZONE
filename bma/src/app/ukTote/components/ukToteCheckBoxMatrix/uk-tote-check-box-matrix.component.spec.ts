import {
  UkToteCheckBoxMatrixComponent
} from '@uktote/components/ukToteCheckBoxMatrix/uk-tote-check-box-matrix.component';
import { IOutcome } from '@core/models/outcome.model';

describe('UkToteCheckBoxMatrixComponent', () => {
  let component: UkToteCheckBoxMatrixComponent;
  let betBuilderService,
      pubsub,
      coreTools;
  let map;

  beforeEach(() => {
    map = {
      '234': {
        '1st': 'checked',
        '2nd': 'open',
        '3rd': 'open'
      }
    } as any;

    betBuilderService = {
      add: jasmine.createSpy(),
      API: {},
    };
    pubsub = {
      API: {
        CLEAR_BETBUILDER: 'CLEAR_BETBUILDER'
      },
      publishSync: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy()
    };
    coreTools = {
      uuid: jasmine.createSpy().and.returnValue('123')
    };

    component = new UkToteCheckBoxMatrixComponent(betBuilderService, pubsub, coreTools);
  });

  it('ngOnInit', () => {
    const outcomeId = 'outcomeId';
    component.clear = jasmine.createSpy();
    pubsub.subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback(outcomeId));
    component.ngOnInit();
    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'checkboxMatrixCtrl 123', pubsub.API.CLEAR_BETBUILDER, jasmine.any(Function)
    );
    expect(component.clear).toHaveBeenCalledWith(outcomeId);
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('checkboxMatrixCtrl 123');
    expect(pubsub.publishSync).toHaveBeenCalled();
  });

  it('trackByIndex', () => {
    const index = 5;
    const result = component.trackByIndex(index);
    expect(result).toBe(index);
  });

  it('get checkBoxMatrix', () => {
    component.outcome = { id: '234' } as IOutcome;
    component.map = map;
    const expectedCheckBoxMatrix = [
      {
        key: '1st',
        value: 'checked'
      },
      {
        key: '2nd',
        value: 'open'
      },
      {
        key: '3rd',
        value: 'open'
      }
    ];
    const result = component.checkBoxMatrix;
    expect(result).toEqual(expectedCheckBoxMatrix);
  });

  describe('getCssClass', () => {
    it('isSuspended true and nonRunner', () => {
      const element = {
        key: 'key',
        value: 'value'
      };
      component.isSuspended = true;
      component.outcome = { nonRunner: true } as IOutcome;
      const result = component.getCssClass(element);
      expect(result).toBe('value disabled non-runner');
    });

    it('isSuspended false and not nonRunner', () => {
      const element = {
        key: 'key',
        value: 'value'
      };
      component.isSuspended = false;
      component.outcome = { nonRunner: false } as IOutcome;
      const result = component.getCssClass(element);
      expect(result.trim()).toBe('value');
    });
  });

  describe('checkPlace', () => {
    it('should trigger run check and call map update emitter', () => {
      component.map = map;
      spyOn(component, 'runChecks');
      spyOn(component.mapUpdate, 'emit');
      component.checkPlace('234', '1st');
      expect(component.runChecks).toHaveBeenCalledWith({'234': {'1st': 'open', '2nd': 'open', '3rd': 'open'}} as any);
      expect(component.mapUpdate.emit).toHaveBeenCalledWith({'234': {'1st': 'open', '2nd': 'open', '3rd': 'open'}} as any);
    });

    it('should change checkbox open to checked', () => {
      component.map = map;
      spyOn(component, 'runChecks');
      component.checkPlace('234', '2nd');
      expect(component.map['234']['2nd']).toEqual('checked');
    });
  });

  describe('clear', () => {
    it('outcomeId', () => {
      const outcomeId = '234';
      const expectedMap = {
        '234': {
          '1st': 'open',
          '2nd': 'open',
          '3rd': 'disabled'
        }
      } as any;
      component.map = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          '3rd': ''
        }
      } as any;
      component.runChecks = jasmine.createSpy();
      component.clear(outcomeId);
      expect(component.map).toEqual(expectedMap);
      expect(component.runChecks).toHaveBeenCalledWith(component.map);
    });

    it('no outcomeId', () => {
      const expectedMap = {
        '234': {
          '1st': 'open',
          '2nd': 'open',
          '3rd': 'open'
        }
      } as any;
      component.map = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          '3rd': 'checked'
        }
      } as any;
      component.clear(null);
      expect(component.map).toEqual(expectedMap);
    });
  });

  describe('runChecks', () => {
    it('currentPool.poolType', () => {
      const id = '234';
      const mapToCheck = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          'any': 'checked'
        }
      } as any;
      component.outcomesMap = {
        '234': {
          '1st': 'open'
        }
      } as any;
      component.currentPool = { poolType: 'poolType' } as any;
      component.setEnables = jasmine.createSpy();
      component.setDisables = jasmine.createSpy();
      component.runChecks(mapToCheck);
      expect(betBuilderService.add).toHaveBeenCalledWith(jasmine.objectContaining({
        betModel: component.selectedOutcomes,
        poolType: component.currentPool.poolType,
        currentPool: component.currentPool
      }));
      expect(component.setEnables).toHaveBeenCalledWith(mapToCheck);
      expect(component.setDisables).toHaveBeenCalledTimes(2);
      expect(component.selectedOutcomes['1st']).toBe(component.outcomesMap[id]);
      expect(component.selectedOutcomes['any']).toEqual([ component.outcomesMap[id] ]);
    });

    it('no currentPool', () => {
      const id = '234';
      const mapToCheck = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          'any': 'checked'
        }
      } as any;
      component.outcomesMap = {
        '234': {
          '1st': 'open'
        }
      } as any;
      component.currentPool = null;
      component.setEnables = jasmine.createSpy();
      component.setDisables = jasmine.createSpy();
      component.runChecks(mapToCheck);
      expect(betBuilderService.add).toHaveBeenCalledWith(jasmine.objectContaining({
        betModel: component.selectedOutcomes,
        poolType: null,
        currentPool: null
      }));
      expect(component.setEnables).toHaveBeenCalledWith(mapToCheck);
      expect(component.setDisables).toHaveBeenCalledTimes(2);
      expect(component.selectedOutcomes['1st']).toBe(component.outcomesMap[id]);
      expect(component.selectedOutcomes['any']).toEqual([ component.outcomesMap[id] ]);
    });
  });

  it('setEnables', () => {
    const mapToUpdate = {
      '234': {
        '1st': 'checked',
        '2nd': 'open',
        'any': 'disabled'
      }
    } as any;
    const expectedMap = {
      '234': {
        '1st': 'checked',
        '2nd': 'open',
        'any': 'open'
      }
    } as any;
    component.setEnables(mapToUpdate);
    expect(mapToUpdate).toEqual(expectedMap);
  });

  describe('setDisables', () => {
    it('col === "any" && index !== "any"', () => {
      const mapToUpdate = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          'any': 'disabled'
        }
      } as any;
      component.setDisables(mapToUpdate, '', 'any');
      expect(mapToUpdate['234']['2nd']).toBe('disabled');
    });

    it('col !== "any" && index === "any"', () => {
      const mapToUpdate = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          'any': 'open'
        }
      } as any;
      component.setDisables(mapToUpdate, '', '1st');
      expect(mapToUpdate['234']['any']).toBe('disabled');
    });

    it('col !== "any" && index !== "any" && id === row', () => {
      const mapToUpdate = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          'any': 'open'
        }
      } as any;
      component.setDisables(mapToUpdate, '234', '1st');
      expect(mapToUpdate['234']['2nd']).toBe('disabled');
    });

    it('col !== "any" && index !== "any" && index === col', () => {
      const mapToUpdate = {
        '234': {
          '1st': 'checked',
          '2nd': 'open',
          'any': 'open'
        }
      } as any;
      component.setDisables(mapToUpdate, '235', '2nd');
      expect(mapToUpdate['234']['2nd']).toBe('disabled');
    });
  });
});
