import { of, throwError } from 'rxjs';
import { FiltersTestData } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { FilterComponent } from '@app/betpack-market-place/filter/filter.component';

describe('FilterComponent', () => {
    let component: FilterComponent;
    let snackBar;
    let apiClientService, betpackService;
    let dialogService;
    let dialog;
    let globalLoaderService;


    beforeEach(() => {
        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message }) => { }),
            showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            })
        };
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: FiltersTestData })),
            deleteFilter: jasmine.createSpy('deleteFilter').and.returnValue(of({ body: { filterAssociated: false, betpackNames: [] } })),
            postFilter: jasmine.createSpy('postFilter').and.returnValue(of({ body: {} })),
            reorderFilter: jasmine.createSpy('reorderFilter').and.returnValue(of(FiltersTestData))
        };
        apiClientService = {
            betpackService: () => betpackService
        };
        dialog = {
            open: jasmine.createSpy('dialog.open').and.returnValue({
                afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of({ body: FiltersTestData[0] }))
            })
        };
        snackBar = {
            open: jasmine.createSpy('open')
        };
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        component = new FilterComponent(dialogService, dialog, apiClientService, snackBar, globalLoaderService);
    });

    it('constructor', () => {
        expect(component).toBeDefined();
    });
    it('ngOnInit', () => {
        spyOn(component, 'loadFilters');
        component.ngOnInit();
        expect(component.loadFilters).toHaveBeenCalled();
    });
    it('loadFilters', () => {
        component.loadFilters();
        expect(component.filters).toEqual(FiltersTestData);
    });
    it('removeFilter', () => {
        component.removeFilter(FiltersTestData[0]);
        expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
            title: 'Remove Filter',
            message: 'Are You Sure You Want to Remove Filter?',
            yesCallback: jasmine.any(Function)
        });
    });
    it('reorderHandler', () => {
        component.reorderHandler({ order: [], id: '' });
        expect(snackBar.open).toHaveBeenCalled();
    });
    it('createFilter', () => {
        spyOn(component, 'loadFilters');
        component.createFilter();
        expect(component.loadFilters).toHaveBeenCalled();
        expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
            title: 'Save Completed',
            message: 'Filter is Created and Stored.'
        });
    });
    it('createFilter when no data', () => {
        dialog.open = jasmine.createSpy('dialog.open').and.returnValue({
            afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of(null))
        })
        spyOn(component, 'loadFilters');
        component.createFilter();
        expect(component.loadFilters).not.toHaveBeenCalled();
    });
    describe('sendRemoveRequest', () => {
        it('when filter is associated with betpack', () => {
            spyOn(component, 'loadFilters');
            component.sendRemoveRequest(FiltersTestData[0]);
            expect(component.loadFilters).toHaveBeenCalled();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: 'Remove Completed',
                message: 'Filter is Removed.'
            });
        });
        it('#sendRemoveRequest error', () => {
            spyOn(console, 'error');
            betpackService = {
                deleteFilter: jasmine.createSpy('deleteFilter').and.returnValue(throwError({ error: 401 })),
            };
            component.sendRemoveRequest(FiltersTestData[0]);
            expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
        })
        it('when filter is not associated with betpack', () => {
            betpackService = {
                deleteFilter: jasmine.createSpy('deleteFilter').and.returnValue(of({ body: { filterAssociated: true, betpackNames: ['Tennis BetPack'] } }))
            };
            apiClientService = {
                betpackService: () => betpackService
            };
            component = new FilterComponent(dialogService, dialog, apiClientService, snackBar, globalLoaderService);
            spyOn(component, 'loadFilters');
            component.sendRemoveRequest(FiltersTestData[0]);
            expect(component.loadFilters).toHaveBeenCalled();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: 'Remove Not Done',
                message: 'Filter is associated with ' + JSON.stringify(['Tennis BetPack'])
            });
        });
        it('filterLength', () => {
            component.filters = [
                {
                    filterActive: true
                },
                {
                    filterActive: false
                }
            ] as any;
            component.filterLength;
            expect(component.filterLength).toEqual({
                active: 1,
                inactive: 1
            });
        });
    });
});
