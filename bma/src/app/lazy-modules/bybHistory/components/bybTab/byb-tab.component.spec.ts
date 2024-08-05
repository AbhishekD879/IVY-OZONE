import { BybTabComponent } from './byb-tab.component';

describe('BybTabsComponent', () => {
    let component;

    beforeEach(() => {
        component = new BybTabComponent();
    });

    //placeBet
    describe('ngOnInit', () => {
        it('should call ngOnInit', () => {
            component.index = 0;
            component.tab = {active : false};
            component.ngOnInit();
            expect(component.tab.active).toBeTruthy();
        });
    });

    //onTabSelect
    describe('onTabSelect', () => {
        it('should call onTabSelect', () => {
            component.index = 0;
            component.tab = {active : false};
            component.onTabSelect(component.tab);
            expect(component.tab.active).toBeTruthy();
        });
    });
});