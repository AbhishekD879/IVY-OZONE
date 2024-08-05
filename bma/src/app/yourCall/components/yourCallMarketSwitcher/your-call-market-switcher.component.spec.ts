import { YourCallMarketSwitcherComponent } from '@yourcall/components/yourCallMarketSwitcher/your-call-market-switcher.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('YourCallMarketSwitcherComponent', () => {
  let component: YourCallMarketSwitcherComponent;
  let yourCallMarketsService;

  beforeEach(() => {
    yourCallMarketsService = {
      prepareMarket: jasmine.createSpy('prepareMarket').and.returnValue(Promise.resolve()),
      isRestoredNeeded: jasmine.createSpy('isRestoredNeeded').and.returnValue(true),
      restoreBet: jasmine.createSpy('restoreBet'),
      selectValue: jasmine.createSpy('selectValue'),
      isSelected: jasmine.createSpy('selectValue')
    };

    component = new YourCallMarketSwitcherComponent(
      yourCallMarketsService
    );

    component.market = {
      groups: {
        0: {
          value: 2
        },
        1: {
          value: 3
        }
      },
      getSelectionsForGroup: () => [1, 2],
      selections: [{}, {}],
      key: '1'
    } as any;
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('#onInit', () => {
    beforeEach(() => {
      component.selectGroup = jasmine.createSpy();
    });

    it('should set true if market has selections', fakeAsync(() => {
      component.ngOnInit();
      tick();
      expect(component.isMarketSelections).toBeTruthy();
    }));

    it('should set false if market hasn`t selections', fakeAsync(() => {
      component.market.selections = [];

      component.ngOnInit();
      tick();
      expect(component.isMarketSelections).toBeFalsy();
    }));

    it('should call selectGroup and define isInit to Equal true', fakeAsync(() => {
      const loadedSpy = spyOn(component.marketLoaded, 'next');
      component.ngOnInit();
      tick();

      expect(component.isInit).toEqual(true);
      expect(component.selectGroup).toHaveBeenCalledWith(0);
      expect(loadedSpy).toHaveBeenCalled();
    }));

    it('should call selectGroup and check case when index < this.switchers.length ', fakeAsync(() => {
      component.market = {
        groups: [{
        value: 2
      }, {
        value: 3
      }],
        getSelectionsForGroup: () => [1],
        selections: [{}, {}],
        key: '1',
        selected: [ {
          group: 1,
          value: 1,
        }]
      } as any;
      component.switchers = [{ value: 1, title: 'dd' }, { value: 2, title: 'dd' }];
      component.ngOnInit();
      tick();

      expect(component.selectGroup).toHaveBeenCalledWith(-1);
      expect(component.allShown).toEqual(true);
    }));

    it('should set value for switchers', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(component.switchers).toEqual({
        0: {
            value: 2
          },
          1: {
            value: 3
          }
      } as any);
    }));

    it('should define all Shown', fakeAsync(() => {
      component.ngOnInit();
      tick();
      expect(component.allShown).toBeDefined();
      expect(component.allShown).toEqual(true);
    }));

    it('should restore bets from storage functionality', fakeAsync(() => {
      component.ngOnInit();
      tick();
      const res = yourCallMarketsService['restoreBet'];

      expect(res).toHaveBeenCalledWith(component.market);
    }));

    it('should call selectGroup', fakeAsync(() => {
      const index = 0;
      component.switchers = { value: 1, title: 'dd' } [1];
      component.ngOnInit();
      tick();

      expect(component.selectGroup).toHaveBeenCalledWith(index);
    }));

    it('should not restoreBet', fakeAsync(() => {
      yourCallMarketsService.isRestoredNeeded = jasmine.createSpy('isRestoredNeeded').and.returnValue(false);
      component.ngOnInit();
      tick();
      const res = yourCallMarketsService['restoreBet'];

      expect(res).not.toHaveBeenCalled();
    }));
  });

  describe('#toggleShow', () => {
    it('should set allShown true?/false value and call limitSelections', () => {
      component['limitSelections'] = jasmine.createSpy();
      component.allShown = true;
      component.toggleShow();

      expect(component.allShown).toEqual(false);
    });
  });

  describe('#selectValue', () => {
    it('should select Value', () => {
      component.selectValue(1);
      const res = yourCallMarketsService['selectValue'];

      expect(res).toHaveBeenCalledWith(component.market, 1);
    });
  });

  describe('#selectGroup', () => {
    it('should select group', () => {
      component['limitSelections'] = jasmine.createSpy();
      component.switchers = [{ value: 1, title: 'dd' }];
      component.selectGroup(0);

      expect(component.selections).toEqual([ 1, 2 ] as any);
      expect(component.selectedGroup).toEqual(0);
    });
  });

  describe('#isSelected', () => {
    it('check is Selected', () => {
      component.isSelected(3);
      const res = yourCallMarketsService['isSelected'];

      expect(res).toHaveBeenCalledWith(component.market, 3);
    });
  });

  describe('#trackBySwitchers', () => {
    it('should track By Switchers and return string', () => {
      const result = component.trackBySwitchers(3, {value: 1, title: '2'});

      expect(result).toEqual('31');
    });
  });

  describe('#trackBySelections', () => {
    it('should track By Selections and return string', () => {
      const selection = {
        id: 1,
        title: '2',
        obtainedPlayerFeed: 2
      } as any;
      const result = component.trackBySelections(3, selection);

      expect(result).toEqual('312');
    });
  });

  describe('#get limitTo', () => {
    it('should return length', () => {
      expect(component.limitTo).toBe(undefined);
      component.length = 2;
      expect(component.limit).not.toBeDefined();
    });

    it('#showPrev checks if arrow-prev is shown', () => {
      component.length = 1;
      component.allShown = true;
      expect(component.limitTo).toEqual(1);
    });

    it('#showPrev checks if arrow-prev is shown', () => {
      component.length = 3;
      component.limit = 1;
      component.allShown = false;
      expect(component.limitTo).toEqual(1);
    });
  });

  describe('#limitSelections', () => {
    it('should set switch selection', () => {
     component['limitSelections']();

     expect(component.switcherSelections).toEqual([]);
    });
  });

  describe('#isActiveGroup', () => {
    it('check is Active group', () => {
      component.isActiveGroup(0);
      expect(component.selectedGroup).toEqual(0);
    });
  });
});
