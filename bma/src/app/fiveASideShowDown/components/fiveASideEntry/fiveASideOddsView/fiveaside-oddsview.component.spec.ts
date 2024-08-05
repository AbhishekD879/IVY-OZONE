import { async } from '@angular/core/testing';
import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import {
    FiveASideOddsViewComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideOddsView/fiveaside-oddsview.component';

describe('FiveASideOddsViewComponent', () => {
    let component: FiveASideOddsViewComponent;
    let fractoDecimalService;

    beforeEach(async(() => {
        fractoDecimalService = {
            getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('10/8')
        };
        component = new FiveASideOddsViewComponent(fractoDecimalService);
    }));
    describe('ngOnInit', () => {
        it('should return frac', () => {
            const [entry] = MY_ENTRIES_LIST;
            component.summary = entry as any;
            component.ngOnInit();
            expect(component.odds).toBe('@10/8');
        });
    });
    describe('ngOnChanges', () => {
        it('should return frac', () => {
            const [entry] = MY_ENTRIES_LIST;
            component.summary = entry as any;
            component.ngOnChanges({ summary: { previousValue: { data: {} } } as any });
            expect(component.odds).toBe('@10/8');
        });
        it('should return frac', () => {
            const [entry] = MY_ENTRIES_LIST;
            component.summary = entry as any;
            spyOn(component, 'oddsFormat' as any);
            component.ngOnChanges({ summary: undefined }as any);
            expect(component['oddsFormat']).not.toHaveBeenCalled();
        });
    });
});
