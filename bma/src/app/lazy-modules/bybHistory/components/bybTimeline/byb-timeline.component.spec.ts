import { BybTimelineComponent } from './byb-timeline.component';

describe('BybTimelineComponent', () => {
    let component;

    beforeEach(() => {
        component = new BybTimelineComponent();
    });

    //checkCurrentStatus
    describe('ngOnInit', () => {
        it('should call ngOnInit', () => {
            component.marketGroupName = 'Total Goals';
            component.ngOnInit();
            expect(component.bybmarketName).toBe('TotalGoals');
        });
    });

    describe('ngOnChanges', () => {
        it('should call ngOnChanges', () => {
            spyOn(component, 'populateMarketGroupNames');
            spyOn(component, 'isActiveGroup');
            component.ngOnChanges(true as any);
            expect(component.populateMarketGroupNames).toHaveBeenCalled();
        });
    });

    //populateMarketGroupNames
    describe('populateMarketGroupNames', () => {
        it('should call populateMarketGroupNames reurn false', () => {
            component.switchers = [1, 2, 3];
            const retVal = component.populateMarketGroupNames();
            expect(retVal).toBeFalsy();
        });

        it('should call populateMarketGroupNames reurn false', () => {
            component.switchers = [];
            component.eachMarketGroup = { markets: [{ key: 'Total Goals', type: 'group' }] } as any;
            spyOn(component, 'parseTitle');
            component.populateMarketGroupNames();
            expect(component.switchers.length).toBeGreaterThan(0);
        });

        it('should call populateMarketGroupNames reurn false without eachmarketgroup', () => {
            component.switchers = [];
            spyOn(component, 'parseTitle');
            component.populateMarketGroupNames();
            expect(component.switchers.length).toBe(0);
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

    //parseTitle
    describe('parseTitle', () => {
        it('should call parseTitle', () => {
            component.eachMarketGroup = { markets: [{ key: '1ST HALF TOTAL', type: 'group' },
            { key: '2ND HALF TOTAL', type: 'group' },{ key: 'Total Goals', type: 'group' }] } as any;
            component.parseTitle(0);
            component.parseTitle(1);
            component.parseTitle(2);
        });
    });

    //selectGroup
    describe('selectGroup', () => {
        it('should call selectGroup', () => {
            component.eachMarketGroup = { markets: [{ key: '1ST HALF TOTAL', type: 'group' },
            { key: '2ND HALF TOTAL', type: 'group' },{ key: 'Total Goals', type: 'group' }] } as any;
            component.selectedMarket = 0;
            spyOn(component, 'reset');
            const retVal = component.selectGroup(0);
            expect(retVal).toBeFalsy();
        });

        it('should call selectGroup', () => {
            component.eachMarketGroup = { markets: [{ key: '1ST HALF TOTAL', type: 'group' },
            { key: '2ND HALF TOTAL', type: 'group' },{ key: 'Total Goals', type: 'group' }] } as any;
            component.selectedMarket = 0;
            component.selectGroup(2);
            expect(component.selectedMarket).toBe(2);
        });

        it('should call selectGroup', () => {
            component.selectGroup();
            expect(component.selectedEachMarket).toBe(undefined);
        });
    });

    //isActiveGroup
    describe('isActiveGroup', () => {
        it('should call isActiveGroup false', () => {
            component.selectedMarket = 0;
            const retVal = component.isActiveGroup(0);
            expect(retVal).toBeTruthy();
        });

        it('should call selectGroup', () => {
            component.selectedMarket = -1;
            const retVal = component.isActiveGroup(0);
            expect(retVal).toBeFalsy();
        });
    });

    //fncollapseLists
    describe('fncollapseLists', () => {
        it('should call fncollapseLists', () => {
            component.switchers = [1,2,3];
            component.fncollapseLists();
            expect(component.switchers.length).toBe(0);
        });
    });

    //displaySwitchers
    describe('displaySwitchers', () => {
        it('should call displaySwitchers', () => {
            spyOn(component, 'populateMarketGroupNames');
            const retVal = component.displaySwitchers;
            expect(retVal).toBe(false);
        });

        it('should call displaySwitchers', () => {
            component.switchers = [1,2];
            component.eachMarketGroup = {};
            spyOn(component, 'populateMarketGroupNames');
            const retVal = component.displaySwitchers;
            expect(retVal).toBe(false);
        });

        it('should call displaySwitchers', () => {
            spyOn(component, 'populateMarketGroupNames');
            component.eachMarketGroup = { markets : [1,2]};
            const retVal = component.displaySwitchers;
            expect(retVal).toBe(true);
        });

        it('should call displaySwitchers', () => {
            component.eachMarketGroup = { markets : null};
            spyOn(component, 'populateMarketGroupNames');
            const retVal = component.displaySwitchers;
            expect(retVal).toBe(false);
        });
    });
});
