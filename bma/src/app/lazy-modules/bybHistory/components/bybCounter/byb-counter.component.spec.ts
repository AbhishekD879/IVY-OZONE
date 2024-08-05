import { BybCounterComponent } from './byb-counter.component';

describe('BybCustomComponent', () => {
    let component, marketService, dashBoardService;

    beforeEach(() => {
        marketService = {
            selectedSelectionsSet: new Set(),
            selectValue: jasmine.createSpy('selectValue').and.returnValue(1),
            markets: [{ selections: [{ id: '0', relatedTeamType: 0 }, { id: '1', relatedTeamType: 1 }, { id: '2', relatedTeamType: 2 }] },
            {}],
            isSelected: jasmine.createSpy('isSelected').and.returnValue(1),
            loadSelectionData: jasmine.createSpy('loadSelectionData').and.returnValue(Promise.resolve(([{ selections: [{ title: 'arsenal' }] }]))),
        };
        dashBoardService = {
            items: [{ selection: { id: '1', relatedTeamType: 0 } },{}]
        };
        component = new BybCounterComponent(marketService, dashBoardService);
    });
    //ngOnChanges
    describe('ngOnChanges', () => {
        it('should call ngOnChanges with initial 0', () => {
            spyOn(component, 'selectValue');
            component.ngOnChanges();
            expect(component.index).toBe(0);
        });
    });

    describe('ngOnInit', () => {
        it('should call ngoninit with initial 0', () => {
            component.initial = -1;
            component.ngOnInit();
            expect(component.initial).toBe('0');
        });
    });
    //selectValue
    describe('selectValue', () => {
        it('should call selectValue with initial 0', () => {
            component.selectedMap = [[1]];
            component.selectValue();
            expect(component.initial).not.toBe(undefined);
        });

        it('should call selectValue with undefined', () => {
            component.selectValue();
            expect(component.initial).toBe(undefined);
        });
    });

    //rotate
    describe('rotate', () => {
        it('should call rotate with 1', () => {
            component.myMapArr = [1,2,3];
            spyOn(component, 'displayVal');
            component.rotate(3);
            expect(component.displayVal).toHaveBeenCalled();
        });

        it('should call rotate with -1', () => {
            component.myMapArr = [1,2,3];
            spyOn(component, 'displayVal');
            component.rotate(-1);
            expect(component.displayVal).toHaveBeenCalled();
        });
    });

    //displayVal
    describe('displayVal', () => {
        it('should call displayVal', () => {
            component.myMapArr = [[1]];
            component.index = 0;
            component.displayVal();
            expect(component.initial).toBe(1);
        });
    });

    //selectedValue
    describe('selectedValue', () => {
        it('should call selectedValue', () => {
            const map = new Map();
            map.set(0,{selection : {id: 1}});
            component.selectedMap = map;
            component.initial = 0;
            marketService.selectedSelectionsSet.add(10);
            component.index = 0;
            component.selectedValue();
        });

        it('should call selectedValue', () => {
            const map = new Map();
            map.set(0,{selection : {id: 0}});
            component.selectedMap = map;
            component.initial = 0;
            marketService.selectedSelectionsSet.add(0);
            component.index = 0;
            component.selectedValue();
        });

        it('should call selectedValue selection undefined', () => {
            const map = new Map();
            map.set(0,{});
            component.selectedMap = map;
            component.initial = 0;
            marketService.selectedSelectionsSet.add(0);
            component.index = 0;
            component.selectedValue();
        });

        it('should call selectedValue selection undefined and not present', () => {
            const map = new Map();
            map.set(0,{});
            component.selectedMap = map;
            component.initial = 0;
            marketService.selectedSelectionsSet.add(1);
            component.index = 0;
            component.selectedValue();
        });
    });

    //removeSelection
    describe('removeSelection', () => {
        it('should call removeSelection', () => {
            const map = new Map();
            map.set(0,{selection : {id: 0}});
            component.selectedMap = map;
            component.initial = 0;
            component.removeSelection();
        });
    });

    //updateSelectionSet
    describe('updateSelectionSet', () => {
        it('should call updateSelectionSet', () => {

            component.updateSelectionSet();
        });
    });

    //checkCurrentStatus
    describe('checkCurrentStatus', () => {
        it('should call checkCurrentStatus with removeAllMarkets', () => {
            const map = new Map();
            marketService.selectedSelectionsSet = new Set();
            marketService.selectedSelectionsSet.add(1);
            map.set(0,{selection : {id: 1}});
            component.selectedMap = map;
            marketService.lastRemovedMarket = 1;
            component.initial = 0;
            component.checkCurrentStatus();
            expect(component.addToSlipText).toBe('ADDED');
        });

        it('should call checkCurrentStatus', () => {
            const map = new Map();
            map.set(0,{selection : {id: 1}});
            component.selectedMap = map;
            marketService.removeAllMarkets = true;
            marketService.lastRemovedMarket = 1;
            component.initial = 0;
            component.checkCurrentStatus();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        });

        it('should call checkCurrentStatus with undefined map', () => {
            const map = new Map();
            map.set(0,{selection : {id: 1}});
            marketService.removeAllMarkets = true;
            marketService.lastRemovedMarket = 1;
            component.initial = 0;
            component.checkCurrentStatus();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        });

        it('should call checkCurrentStatus with out initial in map', () => {
            const map = new Map();
            map.set(1,{selection : {id: 1}});
            component.selectedMap = map;
            marketService.removeAllMarkets = true;
            marketService.lastRemovedMarket = 1;
            component.initial = 0;
            component.checkCurrentStatus();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        });

        it('should call checkCurrentStatus with out initial in map', () => {
            const map = new Map();
            map.set(1,{selection : ''});
            component.selectedMap = map;
            marketService.removeAllMarkets = true;
            marketService.lastRemovedMarket = 1;
            component.initial = 0;
            component.checkCurrentStatus();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        });
    });
});
