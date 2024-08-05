import {
    FiveASideProgressBarComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideProgressBar/fiveaside-progressbar.component';

describe('FiveASideProgressBarComponent', () => {
    let component: FiveASideProgressBarComponent;
    let changeDetectorRef;

    beforeEach(() => {
        changeDetectorRef = {
            markForCheck: jasmine.createSpy('markForCheck')
        };
        component = new FiveASideProgressBarComponent(changeDetectorRef);
    });
    describe('ngOnchanges', () => {
        it('should return super method', () => {
            const parentNgOnInit = spyOn(FiveASideProgressBarComponent.prototype['__proto__'], 'setProgress');
            component.ngOnChanges();
            expect(parentNgOnInit).toHaveBeenCalled();
            expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
    });
});
