import { YourCallTabContentComponent } from './your-call-tab-content.component';

describe('BybCustomComponent', () => {
    let component;

    beforeEach(() => {
        component = new YourCallTabContentComponent();
    });

    //reLocate
    describe('reLocate', () => {
        it('should call reLocate', () => {
            component.dashBoardBox = {relocate : () => true};
            const retVal = component.reLocate;
            expect(retVal).toBeTruthy();
        });

        it('should not call reLocate', () => {
            component.reLocate;
            expect(component.relocate).toBeUndefined();
        });
    });
});
