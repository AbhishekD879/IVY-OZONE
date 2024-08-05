import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { BybCustomComponent } from './byb-custom.component';

describe('BybCustomComponent', () => {
    let component, marketService, dashBoardService, bybSelectedSelectionsService;

    beforeEach(() => {
        marketService = {
            selectedSelectionsSet: new Set(),
            selectValue: jasmine.createSpy('selectValue').and.returnValue(1),
            markets: [{selections: [{id: '0',relatedTeamType: 0},{id: '1',relatedTeamType: 1},{id: '2',relatedTeamType: 2}]},
             {}],
            isSelected: jasmine.createSpy('isSelected').and.returnValue(1),
            loadSelectionData: jasmine.createSpy('loadSelectionData').and.returnValue(Promise.resolve(([{selections: [{title: 'ARSENAL'}]}]))),
            removeId$ : {
                subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
                next: jasmine.createSpy('next').and.returnValue(of(true))
              },
        };
        dashBoardService = {
            items: [{selection: {id: '1',relatedTeamType: 0}}],
            removeId$ :  {
                subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
                next: jasmine.createSpy('next').and.returnValue(of(true))
              },
        };
        bybSelectedSelectionsService = {
            betPlacementSubject$: new Subject<any>(),
        };
        component = new BybCustomComponent(marketService, dashBoardService, bybSelectedSelectionsService);
    });

    describe('ngOnInit', () => {
        it('should call ngoninit with initial 0', () => {
            component.isInitial = 0;
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnInit();
            expect(component.populateMarketGroupNames).not.toHaveBeenCalled();
        });

        it('should call ngoninit with initial -1', () => {
            component.isInitial = -1;
            spyOn(component, 'populateMarketGroupNames');
            component.marketGroupArr = [{}];
            component.switchers = [{}];
            component.ngOnInit();
            expect(component.populateMarketGroupNames).toHaveBeenCalled();
        });

        it('should call ngoninit with response', fakeAsync(() => {
            component.isInitial = 0;
            component.marketGroupArr = [{}];
            component.switchers = [{}];
            spyOn(component, 'populateMarketGroupNames');
            spyOn(component, 'reset');
            component.ngOnInit();
            tick();
            bybSelectedSelectionsService.betPlacementSubject$.next(true);
            expect(component.reset).toHaveBeenCalled();
        }));

        it('should call ngoninit with removeId$', fakeAsync(() => {
            component.isInitial = 0;
            dashBoardService.removeId$ = new Subject();
            marketService.selectedSelectionsSet.add(1);
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnInit();
            dashBoardService.removeId$.next(1);
            tick();
            expect(marketService.selectedSelectionsSet.size).toBe(0);
        }));

        it('should call ngoninit with removeId$ without selection', fakeAsync(() => {
            component.isInitial = 0;
            dashBoardService.removeId$ = new Subject();
            marketService.selectedSelectionsSet.add(1);
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnInit();
            dashBoardService.removeId$.next();
            tick();
            expect(marketService.selectedSelectionsSet.size).toBe(1);
        }));
    });

    describe('selectGroup', () => {
        it('should call selectGroup initial false', () => {
            component.isInitial = false;
            component.selectedGroup = 0;
            component.selectGroup(0);
        });

        it('should call selectGroup initial true', () => {
            component.isInitial = true;
            component.selectedGroup = 0;
            component.marketGroupArr = [{},{}];
            component.switchers = [{},{}];
            spyOn(component, 'loadMarket');
            component.selectGroup(1);
        });

        it('should call selectGroup initial true with isGroup', () => {
            component.isInitial = true;
            component.selectedGroup = 0;
            component.marketGroupArr = [{'isGroup': true},{'isGroup': true}];
            component.switchers = [{'isGroup': true},{'isGroup': true}];
            spyOn(component, 'loadMarket');
            component.selectGroup(1);
        });

        it('should call selectGroup with currentSelection ', () => {
            component.isInitial = true;
            component.selectedGroup = 0;
            component.marketGroupArr = [{'isGroup': true},{'isGroup': true}];
            component.switchers = [{'isGroup': true},{'isGroup': true}];
            spyOn(component, 'loadMarket');
            component.currentSelection = {id : 1};
            marketService.selectedSelectionsSet.add(1);
            component.selectGroup(1);
        });

        it('should call selectGroup with currentSelection without ID ', () => {
            component.isInitial = true;
            component.selectedGroup = 0;
            component.marketGroupArr = [{'isGroup': true},{'isGroup': true}];
            component.switchers = [{'isGroup': true},{'isGroup': true}];
            spyOn(component, 'loadMarket');
            component.currentSelection = {};
            marketService.selectedSelectionsSet.add(1);
            component.selectGroup(1);
        });
    });

    describe('isActiveGroup', () => {
        it('should isActiveGroup return true', () => {
            component.isInitial = false;
            component.selectedGroup = 0;
            const retVal =component.isActiveGroup(0);
            expect(retVal).toBeTruthy();
        });

        it('should isActiveGroup return true', () => {
            component.isInitial = false;
            component.selectedGroup = 0;
            const retVal =component.isActiveGroup(1);
            expect(retVal).toBeFalsy();
        });
    });

    describe('populateMarketGroupNames', () => {
        it('should populateMarketGroupNames populate', () => {
            component.marketGroupArr = [{'key': 'Total Goals','isGroup': true},{'key': 'Total Goals','isGroup': true}];
            component.switchers = [];
            component.populateMarketGroupNames();
            expect(component.switchers.length).toBeGreaterThan(0);
        });

        it('should populateMarketGroupNames populate without marketgroupArr', () => {
            component.switchers = [];
            component.populateMarketGroupNames();
            expect(component.switchers.length).toBe(0);
        });
    });

    describe('parseName', () => {
        it('should parseName', () => {
            component.marketGroupArr = [{'key': 'Total Goals','isGroup': true},{'key': 'Total Goals','isGroup': true}];
            component.switchers = [];
            component.teamA = 'India';
            component.teamB = 'Australia';
            const unFormattedNameA= component.parseName('HOME');
            const unFormattedNameB= component.parseName('AWAY');
            const unFormattedNameAll= component.parseName('Both');
            expect(unFormattedNameA).toBe('India');
            expect(unFormattedNameB).toBe('Australia');
            expect(unFormattedNameAll).toBe('BOTH');
        });
    });

    describe('loadMarket', () => {
        xit('should loadMarket', fakeAsync(() => {
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        }));

        it('should loadMarket with parentSelectionInput', fakeAsync(() => {
            component.parentSelectionInput = {name: 'arsenal', id: 1};
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: 'ARSENAL', id: 1}]}])));
            marketService.selectedSelectionsSet = new Set();
            marketService.selectedSelectionsSet.add(1);
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADDED');
        }));

        it('should loadMarket without selections', fakeAsync(() => {
            marketService.loadSelectionData.and.returnValue(Promise.resolve({}));
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe(undefined);
        }));

        it('should loadMarket without selection data', fakeAsync(() => {
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: {}}])));
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe(undefined);
        }));

        xit('should loadMarket without selection data with out title field', fakeAsync(() => {
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: null}]}])));
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        }));

        xit('should loadMarket without selection data with out title', fakeAsync(() => {
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{}]}])));
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        }));

        it('should loadMarket with parentSelectionInput without title', fakeAsync(() => {
            component.parentSelectionInput = { id: 1};
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: 'ARSENAL', id: 1}]}])));
            marketService.selectedSelectionsSet = new Set();
            marketService.selectedSelectionsSet.add(1);
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADDED');
        }));

        it('should loadMarket with parentSelectionInput without title with both yes', fakeAsync(() => {
            component.parentSelectionInput = { id: 1, name: 'Yes'};
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: 'Yes', id: 1}]}])));
            marketService.selectedSelectionsSet = new Set();
            marketService.selectedSelectionsSet.add(1);
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADDED');
        }));

        it('should loadMarket with parentSelectionInput without title with true', fakeAsync(() => {
            component.parentSelectionInput = { id: 1, name: 'YES'};
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: 'YES', id: 1}]}])));
            marketService.selectedSelectionsSet = new Set();
            marketService.selectedSelectionsSet.add(1);
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADDED');
        }));

        it('should loadMarket with parentSelectionInput and BB', fakeAsync(() => {
            component.parentSelectionInput = { id: 1, name: 'YES'};
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: 'YES', id: 1}]}])));
            marketService.selectedSelectionsSet = new Set();
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        }));

        it('should loadMarket without selection and add to bb', fakeAsync(() => {
            component.currentSelection = null;
            marketService.loadSelectionData.and.returnValue(Promise.resolve(([{selections: [{title: 'YES1', id: 1}]}])));
            marketService.selectedSelectionsSet = new Set();
            marketService.selectedSelectionsSet.add(1);
            component.loadMarket();
            tick();
            expect(component.addToSlipText).toBe('ADD TO BET BUILDER');
        }));
    });

    describe('selectedValue', () => {
        it('should selectedValue', () => {
            component.selectedGroup = -1;
            spyOn(component, 'addMarketBettingSelections');
            component.selectedValue();
            expect(component.addMarketBettingSelections).not.toHaveBeenCalled();
        });
        it('should selectedValue', () => {
            component.selectedGroup = 0;
            component.groupName= 'Match Betting';
            spyOn(component, 'addMarketBettingSelections');
            component.selectedValue();
            expect(component.addMarketBettingSelections).toHaveBeenCalled();
        });

        it('should selectedValue', () => {
            component.selectedGroup = 0;
            component.currentIndex = 1;
            component.currentSelection = 1;
            component.groupName= 'Match Betting';
            spyOn(component, 'addMarketBettingSelections');
            spyOn(component, 'isSelected');
            spyOn(component, 'updateSelectionSet');
            component.selectedValue();
            expect(component.addMarketBettingSelections).toHaveBeenCalled();
        });
    });

    describe('updateSelectionSet', () => {
        it('should updateSelectionSet', () => {
            component.updateSelectionSet();
            expect(marketService.selectedSelectionsSet.size).toBe(1);
        });

        it('should updateSelectionSet without items', () => {
            dashBoardService.items = [{selection : {}}];
            component.updateSelectionSet();
            expect(marketService.selectedSelectionsSet.size).toBe(0);
        });
    });

    describe('isSelected', () => {
        it('should isSelected', () => {
            const retVal = component.isSelected();
            expect(retVal).toBe(1);
        });
    });

    //addMarketBettingSelections
    describe('addMarketBettingSelections', () => {
        it('should addMarketBettingSelections', () => {
            component.key = 'BOTH';
            component.currentSelection = {};
            component.currentIndex = 0;
            component.addMarketBettingSelections();
            expect( component.currentSelection.relatedTeamType).toBe(0);
        });

        it('should addMarketBettingSelections HOME', () => {
            component.key = 'HOME';
            component.currentSelection = {};
            component.currentIndex = 0;
            component.addMarketBettingSelections();
            expect( component.currentSelection.relatedTeamType).toBe(1);
        });

        it('should addMarketBettingSelections AWAY', () => {
            component.key = 'AWAY';
            component.currentSelection = {};
            component.currentIndex = 0;
            component.addMarketBettingSelections();
            expect( component.currentSelection.relatedTeamType).toBe(2);
        });
    });

    describe('reset', () => {
        it('should reset', () => {
            component.isInitial = false;
            component.selectedGroup = 10;
            component.reset();
            expect(component.selectedGroup).toBe(-1);
        });
        it('should reset', () => {
            component.isInitial = true;
            component.selectedGroup = 10;
            component.reset();
            expect(component.selectedGroup).toBe(10);
        });
    });

    describe('checkCurrentStatus', () => {
        it('should checkCurrentStatus', () => {
            component.currentSelection = {id: 1};
            marketService['removeAllMarkets'] = true;
            marketService['lastRemovedMarket'] = 1;
            component.checkCurrentStatus();
            expect( marketService['removeAllMarkets']).toBeFalsy();
        });
        it('should checkCurrentStatus without removeAllMarkets', () => {
            component.currentSelection = {id: 1};
            marketService['removeAllMarkets'] = false;
            marketService['lastRemovedMarket'] = 2;
            marketService.selectedSelectionsSet.add(1);
            component.checkCurrentStatus();
            expect( marketService['removeAllMarkets']).toBeFalsy();
        });
        it('should checkCurrentStatus without currentSelection', () => {
            component.currentSelection = {};
            marketService['removeAllMarkets'] = false;
            marketService['lastRemovedMarket'] = 2;
            component.checkCurrentStatus();
            expect( marketService['removeAllMarkets']).toBeFalsy();
        });

        it('should checkCurrentStatus without currentSelection undefined', () => {
            marketService['removeAllMarkets'] = false;
            marketService['lastRemovedMarket'] = 2;
            component.checkCurrentStatus();
            expect( marketService['removeAllMarkets']).toBeFalsy();
        });
    });

    //ngOnChanges
    describe('ngOnChanges', () => {
        it('should ngOnChanges', () => {
            component.isInitial = true;
            const changes = {key : {firstChange : false}};
            component.currentSelection = {id : 1};
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnChanges(changes);
            expect(component.currentSelection).toBeNull();
        });

        it('should ngOnChanges', () => {
            component.isInitial = false;
            const changes = {key : {firstChange : false}};
            component.currentSelection = {};
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnChanges(changes);
            expect(component.currentSelection).toBeNull();
        });

        it('should ngOnChanges seelction undefined', () => {
            component.isInitial = false;
            const changes = {key : {firstChange : false}};
            component.currentSelection = {};
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnChanges(changes);
            expect(component.currentSelection).toBeNull();
        });

        it('should ngOnChanges', () => {
            component.isInitial = false;
            const changes = {key : {firstChange : false}};
            component.currentSelection = {};
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnChanges(changes);
            expect(component.currentSelection).toBeNull();
        });
    });

    //displaySwitchers
    describe('displaySwitchers', () => {
        it('should displaySwitchers', () => {
            component.switchers= [1];
            component.marketGroupArr = [1,2];
            spyOn(component, 'populateMarketGroupNames');
            const retVal = component.displaySwitchers;
            expect(retVal).toBeGreaterThan(0);
        });

        it('should displaySwitchers without switchers', () => {
            component.switchers= [];
            component.marketGroupArr = [{val : 1}];
            spyOn(component, 'populateMarketGroupNames');
            const retVal = component.displaySwitchers;
            expect(retVal).toBeGreaterThan(0);
        });

        it('should displaySwitchers without val', () => {
            component.switchers= [];
            component.marketGroupArr = [{}];
            spyOn(component, 'populateMarketGroupNames');
            component.displaySwitchers;
            expect(component.selectedGroupMarket).toBe(undefined);
        });

        it('should displaySwitchers without marketgroupArr', () => {
            component.switchers= [];
            spyOn(component, 'populateMarketGroupNames');
            component.displaySwitchers;
            expect(component.selectedGroupMarket).toBe(undefined);
        });
    });

    //fillparentSelectionMarketType
    describe('fillparentSelectionMarketType', () => {
        it('should call fillparentSelectionMarketType', () => {
            component.parentSelection.teamType = -1;
            component.groupName  = 'MATCH BETTING';
            component.fillparentSelectionMarketType(0);
            component.fillparentSelectionMarketType(2);
            component.fillparentSelectionMarketType(1);
            expect(component.parentSelection.teamType).toBe(0)
        });


        it('should call fillparentSelectionMarketType', () => {
            component.parentSelection.teamType = -1;
            component.groupName  = 'BOTH TEAMS';
            component.fillparentSelectionMarketType(2);
            expect(component.parentSelection.teamType).toBe(2)
        });
    });
});
