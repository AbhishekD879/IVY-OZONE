import { CMSSegmentDataTableComponent } from './cms.segement-data.table.component';

describe('CMSSegmenteDataTableComponent', () => {
    let component: CMSSegmentDataTableComponent,
        sortableTableService,
        sanitizer,
        addRemoveStyleService,
        snackBar;

    beforeEach(() => {
        sortableTableService = {
            addSorting: jasmine.createSpy()
        };
        sanitizer = {};
        addRemoveStyleService = {
            addStyle: jasmine.createSpy()
        };

        component = new CMSSegmentDataTableComponent(
            sortableTableService,
            sanitizer,
            addRemoveStyleService  ,
            snackBar       
        );
    });

    it('should call addReorderingToTable', () => {
        component.reorder = true;
        component['addReorderingToTable'] = jasmine.createSpy();
        component.ngAfterViewInit();
        expect(component.addReorderingToTable).toHaveBeenCalled();
    });
    it('should not call addReorderingToTable', () => {
        component.reorder = false;
        component['addReorderingToTable'] = jasmine.createSpy();
        component.ngAfterViewInit();
        expect(component.addReorderingToTable).not.toHaveBeenCalled();
    });
    it('#addReorderingToTable', () => {
        component.addReorderingToTable();
        expect(sortableTableService.addSorting).toHaveBeenCalled();
    });
    it('#selectingShowOnSportsRibbon', () => {
        spyOn(component.showOnSportsFlagChange, 'emit');
        component.selectingShowOnSportsRibbon(false,1);
        expect(component.showOnSportsFlagChange.emit).toHaveBeenCalled();
    });
    it('#selectingShowOnSurfaceBets', () => {
        spyOn(component.showOnSportsFlagChange, 'emit');
        component.selectingShowOnSurfaceBets(false,1, 'Enabled');
        expect(component.showOnSportsFlagChange.emit).toHaveBeenCalled();
    });
});
