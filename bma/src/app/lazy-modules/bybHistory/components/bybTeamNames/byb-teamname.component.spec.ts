import { BybTeamNameComponent } from './byb-teamname.component';

describe('BybCustomComponent', () => {
    let component;

    beforeEach(() => {
        component = new BybTeamNameComponent();
    });

    //checkCurrentStatus
    describe('ngOnInit', () => {
        it('should call ngOnInit', () => {
            component.marketGroupArr = [1,2,3];
            spyOn(component, 'populateMarketGroupNames');
            component.ngOnInit();
            expect(component.populateMarketGroupNames).toHaveBeenCalled();
        });
    });

    //populateMarketGroupNames
    describe('populateMarketGroupNames', () => {
        it('should call populateMarketGroupNames', () => {
            component.switchers = [];
            component.marketGroupArr = [{key: 'Total Goals', game : {homeTeam : 'Liverpool', visitingTeam: 'Arsenal'}, type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Home', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Away', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Awaasdasdy', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Match Booking Points', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Total Corners', type: 'group',available:false,  markets: [{key: 'k1'}] as any}] as any;
            component.populateMarketGroupNames();
            expect(component.switchers.length).toBeGreaterThan(0);
        });

        it('should call populateMarketGroupNames without marketGroupArr', () => {
            component.populateMarketGroupNames();
            expect(component.switchers.length).toBe(0);
        });
    });

    //parseTitle
    describe('parseTitle', () => {
        it('should call parseTitle', () => {
            component.switchers = [];
            component.marketGroupArr = [{key: 'Total Goals', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Home', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Away', type: 'group',available:false,  markets: [{key: 'k1'}] as any},
            {key: 'Total Corners', type: 'group',available:false,  markets: [{key: 'k1'}] as any}] as any;
            component.parseTitle(0);
        });
    });

    //trackByFn
    describe('trackByFn', () => {
        it('should call trackByFn', () => {
            const retVal = component.trackByFn(0);
            const retValSwitchers = component.trackBySwitchers(0);
            expect(retVal).toBe(0);
            expect(retValSwitchers).toBe(0);
        });
    });

    //selectGroup
    describe('selectGroup', () => {
        it('should call selectGroup', () => {
            component.selectedGroup = 0;
            const retVal = component.selectGroup(0);
            expect(retVal).toBeFalsy();
        });

        it('should call selectGroup', () => {
            component.selectedGroup = 0;
            component.marketGroupArr = [1,2,3];
            const retVal = component.selectGroup(1);
            expect(retVal).toBeTruthy();
        });
    });

    //isActiveGroup
    describe('isActiveGroup', () => {
        it('should call isActiveGroup false', () => {
            component.selectedGroup = 0;
            const retVal = component.isActiveGroup(0);
            expect(retVal).toBeTruthy();
        });

        it('should call isActiveGroup true', () => {
            component.selectedGroup = 0;
            const retVal = component.isActiveGroup(1);
            expect(retVal).toBeFalsy();
        });
    });

    //displaySwitchers
    describe('displaySwitchers', () => {
        it('should call displaySwitchers', () => {
            component.marketGroupArr = [1,2,3];
            component.switchers = [1,2,3];
            component.displaySwitchers;
            expect(component.selectedGroupMarket).toBe(undefined);
        });

        it('should call displaySwitchers', () => {
            component.marketGroupArr = [1,2,3];
            component.switchers = [];
            const retVal = component.displaySwitchers;
            expect(retVal).toBeTruthy();
        });
    });
});
