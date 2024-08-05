import { BybTabsComponent } from './byb-tabs.component';

describe('BybTabsComponent', () => {
    let component;

    beforeEach(() => {
        component = new BybTabsComponent();
    });

    //placeBet
    describe('ngOnInit', () => {
        it('should call ngOnInit', () => {
            component.tabs = [{},{}];
            component.ngOnInit();
            expect(component.tabs.active).toBeFalsy();
        });
    });

    //trackByIndex
    describe('trackByIndex', () => {
        it('should call trackByIndex', () => {
            const retVal = component.trackByIndex(1);
            expect(retVal).toBe(1);
        });
    });

    //isEnabledMarketSwitchers
    describe('isEnabledMarketSwitchers', () => {
        it('should call isEnabledMarketSwitchers', () => {
            component.enabledMarketSwitchers = {m1: 1};
            const retVal = component.isEnabledMarketSwitchers({market: 'm1'});
            expect(retVal).toBe(1);
        });
    });

    //onTabChange
    describe('onTabChange', () => {
        it('should call onTabChange', () => {
            component.tabs = [{market: 'm1', active: false},{market: 'm2', active: false}];
            component.onTabChange({market: 'm1'});
            expect(component.tabs[0].active).toBeTruthy();
        });
    });
});