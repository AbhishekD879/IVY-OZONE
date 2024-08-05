import { of, throwError } from 'rxjs';
import { FILTER1, FILTER2, FILTER3, FILTER4, FiltersTestData, FiltersTestData1, FiltersTestData2 } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { EditFilterComponent } from '@app/betpack-market-place/filter/edit-filter/edit-filter.component';
import { EditNewFilterMock } from '@app/betpack-market-place/betpack-mock';

describe('EditFilterComponent', () => {
    let component: EditFilterComponent;
    let router;
    let apiClientService, betpackService;
    let dialogService;
    let activatedRoute;
    let globalLoaderService;


    beforeEach(() => {
        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
                closeCallback();
            })
        };
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: FiltersTestData })),
            deleteFilter: jasmine.createSpy('deleteFilter').and.returnValue(of({ body: { filterAssociated: false, betpackNames: [] } })),
            putFilter: jasmine.createSpy('putFilter').and.returnValue(of({ body: { filterAssociated: false, betpackNames: [] } })),
            getFilterById: jasmine.createSpy('getFilterById').and.returnValue(of({ body: EditNewFilterMock })),
        };
        apiClientService = {
            betpackService: () => betpackService
        };
        router = {
            navigate: jasmine.createSpy('navigate')
        };
        activatedRoute = {
            params: of({ id: '1' })
        };
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        component = new EditFilterComponent(router, activatedRoute, apiClientService, globalLoaderService, dialogService);
    });

    it('constructor', () => {
        expect(component).toBeDefined();
    });
    it('ngOnInit', () => {
        spyOn<any>(component, 'loadInitData');
        component.ngOnInit();
        expect(component['loadInitData']).toHaveBeenCalled();
    });
    it('isValidForm', () => {
        const filter1 = FILTER1;
        const filter2 = FILTER2;
        const filter3 = FILTER3;
        const filter4 = FILTER4;
        expect(component.isValidForm(filter2)).toBeTruthy();
        expect(component.isValidForm(filter1)).toBeFalsy();
        expect(component.isValidForm(filter3)).toBeFalsy();
        expect(component.isValidForm(filter4)).toBeFalsy();
        expect(component.isValidForm(FiltersTestData[0])).toBeFalsy();
        expect(component.isValidForm(FiltersTestData1[0])).toBeTruthy();
        expect(component.isValidForm(FiltersTestData2[0])).toBeFalsy();


    });
    describe('removeFilter And saveChanges', () => {
        it('when filter is associated with betpack', () => {
            component.editFilter = FiltersTestData[0];
            component.removeFilter();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: 'Remove Completed',
                message: 'Filter is Removed.',
                closeCallback: jasmine.any(Function)
            });

            component.saveChanges();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: `Filter Saving`,
                message: `Filter is Saved.`,
                closeCallback: jasmine.any(Function)
            });
        });
        it('when filter is not associated with betpack', () => {
            betpackService = {
                deleteFilter: jasmine.createSpy('deleteFilter').and.returnValue(of({ body: { filterAssociated: true, betpackNames: ['Tennis BetPack'] } })),
                putFilter: jasmine.createSpy('putFilter').and.returnValue(of({ body: { filterAssociated: true, betpackNames: ['Tennis BetPack'] } })),
            };
            apiClientService = {
                betpackService: () => betpackService
            };
            component = new EditFilterComponent(router, activatedRoute, apiClientService, globalLoaderService, dialogService);
            component.editFilter = FiltersTestData[0];
            component.removeFilter();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: 'Remove Not Done',
                message: 'Filter is associated with ' + JSON.stringify(['Tennis BetPack']),
                closeCallback: jasmine.any(Function)
            });

            component.saveChanges();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: 'Save Not Done',
                message: 'Filter is associated with ' + JSON.stringify(['Tennis BetPack']),
                closeCallback: jasmine.any(Function)
            });
        });
    });
    describe('#action Handler', () => {
        it('#actionHandler should call correct method', () => {
            spyOn(component, 'saveChanges');
            component.actionsHandler('save');
            expect(component.saveChanges).toHaveBeenCalled();

            spyOn(component, 'removeFilter');
            component.actionsHandler('remove');
            expect(component.removeFilter).toHaveBeenCalled();

            spyOn<any>(component, 'loadInitData');
            component.actionsHandler('revert');
            expect(component['loadInitData']).toHaveBeenCalled();
        });
        it('#actionHandler should do nothing if wrong event', () => {
            spyOn(component, 'saveChanges');
            spyOn(component, 'removeFilter');
            spyOn<any>(component, 'loadInitData');
            component.actionsHandler('test-event');
            expect(component.saveChanges).not.toHaveBeenCalled();
            expect(component.removeFilter).not.toHaveBeenCalled();
            expect(component['loadInitData']).not.toHaveBeenCalled();
        });
    });
    describe('loadInitData', () => {
        it('loadInitData when isLoading', () => {
            component['loadInitData']();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled()
        });
        it('#loadInitData should call isLoading, false case', () => {
            component['loadInitData'](false);
        });
        it('#loadInitData error', () => {
            betpackService = {
                getFilterById: jasmine.createSpy('getFilterById').and.returnValue(throwError({ error: 401 }))
            };
            component['loadInitData']();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled()
        })
    })
    describe('filterCheck', () => {
        it('filterCheck when isLoading', () => {
            component['filterCheck']('All');
            expect(component.isHaveAll).toBeTruthy();
        });
        it('#filterCheck special char', () => {
            component['filterCheck']('All@');
            expect(component.isHaveAll).toBeFalsy();
        })
    })
});
