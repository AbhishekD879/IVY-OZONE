import { fakeAsync, tick } from '@angular/core/testing';
import { YourCallCorrectScoreComponent } from '@yourcall/components/yourCallCorrectScore/your-call-correct-score.component';
import { Subject } from 'rxjs';

describe('#YourCallCorrectScoreComponent', () => {
  let component;
  let yourCallMarketsService;
  let yourcallDashboardService;

  beforeEach(() => {
    yourCallMarketsService = {
      isRestoredNeeded: jasmine.createSpy('isRestoredNeeded').and.returnValue(true),
      restoreBet: jasmine.createSpy('restoreBet'),
      isSelected: jasmine.createSpy('isSelected'),
      selectValue: jasmine.createSpy('selectValue'),
      selectedSelectionsSet: new Set(),
      betPlacedStatus$: new Subject<any>(),
      betRemovalsubject$: new Subject<any>()
    };

    yourcallDashboardService = {
        items : [{selection:{id: 1} }, {selection :{id: 2} }]
    };

    component = new YourCallCorrectScoreComponent(yourCallMarketsService,yourcallDashboardService);
    component.market = {
      selections: [
        {
          odds: 'Infinity',
          relatedTeamType: 1,
          bettingValue1: 1,
          bettingValue2: 2
        },
        {
          odds: '1/2',
          relatedTeamType: 1
        },
        {
          odds: '3/4',
          relatedTeamType: 1,
          bettingValue2: null
        }
      ]
    };
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnChanges', () => {
    it('should call ngOnChanges isRestoredNeeded true', () => {
      component.ngOnChanges();

      expect(yourCallMarketsService.isRestoredNeeded).toHaveBeenCalled();
      expect(yourCallMarketsService.restoreBet).toHaveBeenCalled();
    });

    it('should call ngOnChanges isRestoredNeeded false', () => {
      yourCallMarketsService.isRestoredNeeded.and.returnValue(false);
      component.ngOnChanges();

      expect(yourCallMarketsService.isRestoredNeeded).toHaveBeenCalled();
      expect(yourCallMarketsService.restoreBet).not.toHaveBeenCalled();
    });

    it('should call ngOnChanges getSelectedSlectionVal true', () => {
      yourCallMarketsService.isRestoredNeeded.and.returnValue(false);
      spyOn(component, 'getSelectedSlectionVal').and.returnValue(true);
      component.ngOnChanges();

      expect(yourCallMarketsService.isRestoredNeeded).toHaveBeenCalled();
      expect(yourCallMarketsService.restoreBet).not.toHaveBeenCalled();
    });
  });

  describe('#toggleShow', () => {
    it('should call toggleShow filterValueType all', () => {
      component.filterValueType = 'all';
      component.toggleShow();

      expect(component.allShown).toEqual(false);
      expect(component.filterValueType).toEqual('main');
    });

    it('should call toggleShow filterValueType main', () => {
      component.filterValueType = 'main';
      component.toggleShow();

      expect(component.allShown).toEqual(true);
      expect(component.filterValueType).toEqual('all');
    });
  });

  describe('#groupMarkets', () => {
    it('should call groupMarkets', () => {
      component.groupMarkets();

      expect(component.groupedMarkets).toEqual([
        [{ odds: '1/2', relatedTeamType: 1 }, { odds: '3/4', relatedTeamType: 1, bettingValue2: null }], undefined, undefined]);
    });

    it('should call subject with val', fakeAsync(() => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.groupMarkets();
      yourCallMarketsService.betRemovalsubject$.next(1);
      tick();
      expect(component.groupedMarkets).toEqual([
        [{ odds: '1/2', relatedTeamType: 1 }, { odds: '3/4', relatedTeamType: 1, bettingValue2: null }], undefined, undefined]);
    }));

    it('should call subject with val and return false', fakeAsync(() => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.currentSelection = {id: 1};
      spyOn(component, 'getSelectedSlectionVal').and.returnValue(false);
      component.groupMarkets();
      yourCallMarketsService.betRemovalsubject$.next(1);
      tick();
      expect(component.groupedMarkets).toEqual([
        [{ odds: '1/2', relatedTeamType: 1 }, { odds: '3/4', relatedTeamType: 1, bettingValue2: null }], undefined, undefined]);
    }));

    it('should call subject with val', fakeAsync(() => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.currentSelection = {id: 1};
      spyOn(component, 'getSelectedSlectionVal').and.returnValue(true);
      component.groupMarkets();
      yourCallMarketsService.betRemovalsubject$.next(1);
      tick();
      expect(component.groupedMarkets).toEqual([
        [{ odds: '1/2', relatedTeamType: 1 }, { odds: '3/4', relatedTeamType: 1, bettingValue2: null }], undefined, undefined]);
    }));
  });

  describe('#getScores', () => {
    it('should call getScores if relatedTeamType === 1', () => {
      const result = component.getScores({ odds: '1/2', relatedTeamType: 1, bettingValue1: 2, bettingValue2: 1 });

      expect(result).toEqual('2 - 1');
    });

    it('should call getScores if relatedTeamType !== 1', () => {
      const result = component.getScores({ odds: '1/2', relatedTeamType: 2, bettingValue1: 6, bettingValue2: 4 });

      expect(result).toEqual('4 - 6');
    });
  });

  describe('#selectValue', () => {
    it('should call selectValue', () => {
     component.selectValue({} as any);

      expect(yourCallMarketsService.selectValue).toHaveBeenCalledWith(component.market, {});
    });
  });

  describe('#isSelected', () => {
    it('should call isSelected', () => {
      component.isSelected({} as any);

      expect(yourCallMarketsService.isSelected).toHaveBeenCalledWith(component.market, {});
    });
  });

  describe('#onScoreChange', () => {
    it('should call getSelectedObj', () => {
      component.getSelectedObj = jasmine.createSpy('getSelectedObj').and.returnValue(true);
      component.checkForNull = jasmine.createSpy('checkForNull');
      component.onScoreChange();

      expect(component.getSelectedObj).toHaveBeenCalled();
      expect(component.checkForNull).not.toHaveBeenCalled();
    });

    it('should call checkForNull', () => {
      component.getSelectedObj = jasmine.createSpy('getSelectedObj').and.returnValue(false);
      component.checkForNull = jasmine.createSpy('checkForNull');
      component.onScoreChange();

      expect(component.getSelectedObj).toHaveBeenCalled();
      expect(component.checkForNull).toHaveBeenCalled();
    });
  });

  describe('#trackByMarket', () => {
    it('should call trackByMarket', () => {
      const result = component.trackByMarket(1, [{ odds: '1/2', id: '1231', title: 'title'}] as any);

      expect(result).toEqual('11/21231title');
    });
  });

  describe('#trackBySelection', () => {
    it('should call trackBySelection', () => {
      const result = component.trackBySelection(1, { title: 'title', id: '1231', displayOrder: '-1000'});

      expect(result).toEqual('1title1231-1000');
    });
  });

  describe('#resetDropdown', () => {
    it('should call resetDropdown', () => {
      component.selectedValueHome = 1;
      component.selectedValueAway = 2;
      component['resetDropdown']();

      expect(component.selectedValueHome).toEqual(0);
      expect(component.selectedValueAway).toEqual(0);
    });
  });

  describe('#addToDashboard', () => {
    it('should call addToDashboard with selected value', () => {
      component.getSelectedObj = jasmine.createSpy('getSelectedObj').and.returnValue({});
      component.addToDashboard();

      expect(yourCallMarketsService.selectValue).toHaveBeenCalledWith(component.market, {});
    });

    it('should call addToDashboard and resetDropdown', () => {
      component.getSelectedObj = jasmine.createSpy('getSelectedObj').and.returnValue(null);
      component.selectedValueHome = 1;
      component.selectedValueAway = 2;

      component.addToDashboard();

      expect(component.selectedValueHome).toEqual(0);
      expect(component.selectedValueAway).toEqual(0);
      expect(yourCallMarketsService.selectValue).not.toHaveBeenCalled();
    });

    it('should call addToDashboard and resetDropdown', () => {
      component.selectedValueHome = 1;
      component.selectedValueAway = 2;
      yourCallMarketsService.selectedSelectionsSet.add(1);
      spyOn(component, 'getSelectedObj').and.returnValue({id: 1});
      spyOn(component, 'getSelectedSlectionVal').and.returnValue(true);
      component.addToDashboard();

      expect(yourCallMarketsService.selectValue).toHaveBeenCalled();
    });
  });

  describe('#getSelectedObj', () => {
    it('should call getSelectedObj and find object', () => {
      component.selectedValueHome = 1;
      component.selectedValueAway = 2;
      const result = component['getSelectedObj']();

      expect(result).toEqual({ odds: 'Infinity', relatedTeamType: 1, bettingValue1: 1, bettingValue2: 2 });
    });

    it('should call getSelectedObj and not find object', () => {
      component.selectedValueHome = 1;
      component.selectedValueAway = 1;
      const result = component['getSelectedObj']();

      expect(result).toEqual(undefined);
    });
  });

  describe('#checkForNull', () => {
    it('should call checkForNull (this.selectedValueHome = false; this.selectedValueAway = 1)', () => {
      component.selectedValueAway = 1;
      const result = component['checkForNull']();

      expect(result).toEqual(undefined);
    });

    it('should call checkForNull (this.selectedValueHome = false; this.selectedValueAway = false)', () => {
      const result = component['checkForNull']();

      expect(result).toEqual({
        odds: '3/4',
        relatedTeamType: 1,
        bettingValue2: null
      });
    });
  });

    describe('updateSelectionSet', () => {
        it('should updateSelectionSet', () => {
            component.updateSelectionSet();
            expect(yourCallMarketsService.selectedSelectionsSet.size).toBeGreaterThan(0);
        });

        it('should updateSelectionSet without items', () => {
            yourCallMarketsService.selectedSelectionsSet = new Set();
            yourcallDashboardService.items = [{ selection: {} }];
            component.updateSelectionSet();
            expect(yourCallMarketsService.selectedSelectionsSet.size).toBeGreaterThan(0);
        });

        it('should updateSelectionSet without items and selection', () => {
          yourCallMarketsService.selectedSelectionsSet = new Set();
          yourcallDashboardService.items = [{ sel: {} }];
          component.updateSelectionSet();
          expect(yourCallMarketsService.selectedSelectionsSet.size).toBeGreaterThan(0);
      });
    });

    //ngOnInit(
    describe('ngOnInit with true', () => {
        it('should ngOnInit', fakeAsync(() => {
            spyOn(component, 'resetDropdown');
            component.betButtonText = '';
            component.ngOnInit();
            yourCallMarketsService.betPlacedStatus$.next(true);
            tick();
            expect(component.betButtonText).toBe('ADD TO BET BUILDER');
        }));

        it('should ngOnInit with false', fakeAsync(() => {
            spyOn(component, 'resetDropdown');
            component.betButtonText = '';
            component.ngOnInit();
            yourCallMarketsService.betPlacedStatus$.next(false);
            tick();
            expect(component.betButtonText).toBe('');
        }));
    });

    //rotateA
    describe('rotateA', () => {
        it('should rotateA with false', () => {
            component.selectedValueAway = 0;
            component.scoreAway = [1,2,3,4,5];
            component.scoreHome = [1,2,3,4,5];
            spyOn(component, 'resetDropdown');
            spyOn(component, 'getSelectedSlectionVal').and.returnValue(false);
            component.betButtonText = '';
            component.rotateA(1);
            component.rotateH(1);
            expect(component.betButtonText).toBe('ADD TO BET BUILDER');
        });

        it('should rotateA with true', () => {
            component.selectedValueAway = 0;
            component.scoreAway = [1,2,3,4,5];
            component.scoreHome = [1,2,3,4,5];
            spyOn(component, 'resetDropdown');
            spyOn(component, 'getSelectedSlectionVal').and.returnValue(true);
            component.betButtonText = '';
            component.rotateA(-1);
            component.rotateH(-1);
            expect(component.betButtonText).toBe('ADDED');
        });

        it('should rotateA with true with minus', () => {
          component.selectedValueHome = -2;
          component.scoreAway = [1,2,3,4,5];
          component.scoreHome = [1,2,3,4,5];
          spyOn(component, 'resetDropdown');
          spyOn(component, 'getSelectedSlectionVal').and.returnValue(true);
          component.betButtonText = '';
          component.rotateA(-1);
          component.rotateH(-1);
          expect(component.betButtonText).toBe('ADDED');
      });
    });

    //getSelectedSlectionVal
    describe('getSelectedSlectionVal', () => {
        it('getSelectedSlectionVal', () => {
            component.market = {selections: [{id: 1,bettingValue1 : 1, bettingValue2: 1}]};
            component.selectedValueHome =  1;
            component.selectedValueAway =  1;
            component.getSelectedSlectionVal();
            expect(component.currentSelection).toBe(component.market.selections[0]);
        });

        it('getSelectedSlectionVal with null', () => {
            component.market = {selections: [{id: 1,bettingValue2: null}]};
            component.getSelectedSlectionVal();
            expect(component.currentSelection).toBe(component.market.selections[0]);
        });

        it('getSelectedSlectionVal with null with id in set', () => {
          component.selectedValueHome = 1;
          yourCallMarketsService.selectedSelectionsSet.add(1);
          component.currentSelection = {id : 1};
          const retVal = component.getSelectedSlectionVal();
          expect(retVal).toBeFalsy();
      });

      it('getSelectedSlectionVal', () => {
        component.market = {selections: [{id: 1,bettingValue1 : 1, bettingValue2: 1}]};
        component.selectedValueHome =  1;
        component.selectedValueAway =  1;
        yourCallMarketsService.selectedSelectionsSet.add(1);
        const retVal = component.getSelectedSlectionVal();
        expect(retVal).toBeTruthy();
    });
    });
});
