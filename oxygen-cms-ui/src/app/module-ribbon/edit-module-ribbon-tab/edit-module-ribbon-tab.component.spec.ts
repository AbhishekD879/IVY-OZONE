import { EditModuleRibbonTabComponent } from './edit-module-ribbon-tab.component';
import { of as observableOf } from 'rxjs';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import { Params } from '@angular/router';
import { ModuleRibbonTab } from '@app/client/private/models';
import { CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { tabsTypes } from '@app/module-ribbon/constant/tabs-types.constant';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { DateRange } from '@app/client/private/models/dateRange.model';

describe('EditModuleRibbonTabComponent', () => {
    let component: EditModuleRibbonTabComponent;
    let moduleRibbonService;
    let activatedRoute;
    let router;
    let apiClientService;
    let globalLoaderService;
    let dialogService;
    let segmentManagerService;

    beforeEach(() => {
        router = jasmine.createSpyObj('routerSpy', ['navigate']);
        activatedRoute = { params: observableOf({ id: 'mockId' }) };
        moduleRibbonService = {
            getPossibleEventHubsToMap: jasmine.createSpy('getPossibleEventHubsToMap').and.returnValue(observableOf({ body: { createdBy: '123' } })),
        };
        dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog']);
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };
        apiClientService = {
            moduleRibbonTab: jasmine.createSpy('moduleRibbonTab').and.returnValue({
                udpate: jasmine.createSpy('udpate').and.returnValue(observableOf({ body: { createdBy: '123' } })),
                remove: jasmine.createSpy('remove').and.returnValue(observableOf({ body: { createdBy: '123' } })),
                getById: jasmine.createSpy('getById').and.returnValue(observableOf({ body: { createdBy: '123' } })),
                getByBrand: jasmine.createSpy('getByBrand').and.returnValue(observableOf({ body: { createdBy: '123' } })),
            })
        };
        segmentManagerService = {
            updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
        };
        component = new EditModuleRibbonTabComponent(
            moduleRibbonService, activatedRoute, router, apiClientService, globalLoaderService,
            dialogService, segmentManagerService);
    });
    it('should edit', () => {
        expect(component).toBeTruthy();
    });

    describe('#ngOnInit', () => {
        it('should call loadInitData', () => {
            component.ngOnInit();
            expect(globalLoaderService.showLoader).toHaveBeenCalled();
        });
    });

    describe('#isValidForm', () => {
        it('should return module length when moduleRibbonTab having value', () => {
            const moduleRibbonTab = { title: 'test' } as ModuleRibbonTab;
            const result = component['isValidForm'](moduleRibbonTab);
            expect(result).toBe(true);
        });
        it('should return module length when moduleRibbonTab is undefined', () => {
            const moduleRibbonTab = {} as ModuleRibbonTab;
            const result = component['isValidForm'](moduleRibbonTab);
            expect(result).toBeUndefined();
        });
    });

    describe('#saveChanges', () => {
        beforeEach(() => {
            component.actionButtons = { extendCollection: jasmine.createSpy('extendCollection') };
        });
        it('should save and open dialog with Universal', () => {
            const moduleData = <ModuleRibbonTab>{ applyUniversalSegments: true };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                udpate: jasmine.createSpy('udpate').and.returnValue(observableOf({ body: moduleData })),
            });
            component.saveChanges();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTab).toEqual(moduleData);
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.moduleRibbonTab);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                    title: `Module Ribbon Tab Saving`, message: `Module Ribbon Tab is Saved.`,
                    closeCallback: jasmine.any(Function)
                }
            );
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalled();
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalledWith(
                { segmentModule: CSPSegmentLSConstants.MODULE_RIBBON_TAB, segmentValue: CSPSegmentConstants.UNIVERSAL_TITLE });
        });

        it('should save and open dialog with Universal and exclusion segment', () => {
            const moduleData = <ModuleRibbonTab>{ applyUniversalSegments: true, exclusionList: ['Cricket', 'Football'] };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                udpate: jasmine.createSpy('udpate').and.returnValue(observableOf({ body: moduleData })),
            });
            component.saveChanges();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTab).toEqual(moduleData);
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.moduleRibbonTab);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                    title: `Module Ribbon Tab Saving`, message: `Module Ribbon Tab is Saved.`,
                    closeCallback: jasmine.any(Function)
                }
            );
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalled();
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalledWith(
                { segmentModule: CSPSegmentLSConstants.MODULE_RIBBON_TAB, segmentValue: 'Cricket,Football' });
        });

        it('should save and open dialog with Segment Inclusion not defined', () => {
            const moduleData = <ModuleRibbonTab>{ applyUniversalSegments: false, inclusionList: [] };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                udpate: jasmine.createSpy('udpate').and.returnValue(observableOf({ body: moduleData })),
            });
            component.saveChanges();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTab).toEqual(moduleData);
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.moduleRibbonTab);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                    title: `Module Ribbon Tab Saving`, message: `Module Ribbon Tab is Saved.`,
                    closeCallback: jasmine.any(Function)
                }
            );
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalled();
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalledWith(
                { segmentModule: CSPSegmentLSConstants.MODULE_RIBBON_TAB, segmentValue: CSPSegmentConstants.UNIVERSAL_TITLE });
        });

        it('should save and open dialog with Segment inclusion defined', () => {
            const moduleData = <ModuleRibbonTab>{ applyUniversalSegments: false, inclusionList: ['Cricket', 'Football'] };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                udpate: jasmine.createSpy('udpate').and.returnValue(observableOf({ body: moduleData })),
            });
            component.saveChanges();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTab).toEqual(moduleData);
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.moduleRibbonTab);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                    title: `Module Ribbon Tab Saving`, message: `Module Ribbon Tab is Saved.`,
                    closeCallback: jasmine.any(Function)
                }
            );
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalled();
            expect(segmentManagerService.updateSegmentMessage).toHaveBeenCalledWith(
                { segmentModule: CSPSegmentLSConstants.MODULE_RIBBON_TAB, segmentValue: 'Cricket,Football' });
        });
    });

    describe('#revertChanges', () => {
        it('should call loadInitData', () => {
            component.revertChanges();
            expect(globalLoaderService.showLoader).toHaveBeenCalled();
        });
    });

    describe('#removeModuleRibbonTab', () => {
        it('should remove and route to view page', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ id: 'id' };
            component.removeModuleRibbonTab();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(router.navigate).toHaveBeenCalledWith(['/module-ribbon-tabs']);
        });
    });

    describe('#loadInitData', () => {
        beforeEach(() => {
            component.directiveNames = tabsTypes;
            activatedRoute.params = observableOf({ pageType: 'add', id: '1' } as Params);
        });
        it('should load data when directiveName is EventHub', () => {
            const segmentsObj = { exclusionList: [], inclusionList: [], applyUniversalSegments: true };
            const moduleData = <ModuleRibbonTab>{ id: 'id', title: 'success', directiveName: 'EventHub', ...segmentsObj };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getById: jasmine.createSpy('getById').and.returnValue(observableOf({ body: moduleData })),
            });
            component['loadInitData']();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTab).toEqual(moduleData);
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
            expect(component.isLoading).toBeFalse();
        });
        it('should load data when directiveName is not EventHub', () => {
            const segmentsObj = { exclusionList: [], inclusionList: [], applyUniversalSegments: true };
            const moduleData = <ModuleRibbonTab>{ id: 'id', title: 'success', directiveName: 'EventHub', ...segmentsObj };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getById: jasmine.createSpy('getById').and.returnValue(observableOf({ body: moduleData })),
            });
            component['loadInitData']();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTab).toEqual(moduleData);
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
            expect(component.isLoading).toBeFalse();
        });
        it('should throw error when 404', () => {
            apiClientService.moduleRibbonTab().getById.and.returnValue(Observable.throw({ status: 404 }));
            component['loadInitData']();
            expect(component.isLoading).toBeFalse();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
        });
    });

    describe('#onChangeDirectiveName', () => {
        beforeEach(() => {
            component.directiveNames = tabsTypes;
            component.moduleRibbonTab = <ModuleRibbonTab>{};
            component.eventHubsList = [];
            component.loadEventHubs = jasmine.createSpy().and.returnValue(observableOf(null));
        })
        it('should call loadEventHubs when directiveName is not EventHub', () => {
            component['onChangeDirectiveName']('test');
            expect(component.moduleRibbonTab.directiveName).toBe('test');
            expect(component.loadEventHubs).not.toHaveBeenCalled();
        });
        it('should call loadEventHubs when directiveName is EventHub', () => {
            component['onChangeDirectiveName']('EventHub');
            expect(component.moduleRibbonTab.directiveName).toBe('EventHub');
            expect(component.loadEventHubs).toHaveBeenCalledTimes(1);
        });
    });

    describe('#onChangeShowTabOn', () => {
        it('should update showTabOn property', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{};
            component['onChangeShowTabOn']('test');
            expect(component.moduleRibbonTab.showTabOn).toBe('test');
        });
    });

    describe('#actionsHandler', () => {
        it('should call remove', () => {
            spyOn(component as any, 'removeModuleRibbonTab');
            component['actionsHandler']('remove');
            expect(component['removeModuleRibbonTab']).toHaveBeenCalled();
        });
        it('should call save', () => {
            spyOn(component as any, 'saveChanges');
            component['actionsHandler']('save');
            expect(component['saveChanges']).toHaveBeenCalled();
        });
        it('should call revert', () => {
            spyOn(component as any, 'revertChanges');
            component['actionsHandler']('revert');
            expect(component['revertChanges']).toHaveBeenCalled();
        });
        it('should call default', () => {
            component['actionsHandler']('default');
        });
    });

    describe('#isEventHubTab', () => {
        it('should return true', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ directiveName: 'EventHub' };
            expect(component.isEventHubTab()).toBeTruthy();
        });
        it('should return false', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ directiveName: 'test' };
            expect(component.isEventHubTab()).toBeFalsy();
        });
    });

    describe('#setChosenHub', () => {
        it('should url doesnot match', () => {
            component.eventHubsList = [{ indexNumber: 12345, title: 'hub' }] as IEventHub[];
            component.setChosenHub('/module-ribbon-tabs');
            expect(component.selectedHubName).toBeUndefined();
        });
        it('should url matches and index matches', () => {
            component.eventHubsList = [{ indexNumber: 12345, title: 'hub1234' }] as IEventHub[];
            component.setChosenHub('/module-ribbon-tabs/edit/12345');
            expect(component.selectedHubName).toBe('hub1234');
        });
        it('should url matches and index doesnot matches', () => {
            component.eventHubsList = [{ indexNumber: 1234567, title: 'hub1234' }] as IEventHub[];
            component.setChosenHub('/module-ribbon-tabs/edit/12345');
            expect(component.selectedHubName).toBeUndefined();
        });
    });

    describe('#loadTabs', () => {
        it('should remove when id matches', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ id: '1234' };
            let brandData = [{ id: '1234' }, { id: '2345' }];
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getByBrand: jasmine.createSpy('getByBrand').and.returnValue(observableOf({ body: brandData })),
            });
            component.loadTabs();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(brandData.length).toBe(2);
        });
        it('should not remove when id mis-matches', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ id: '1234' };
            let brandData = [{ id: '12345' }, { id: '2345' }];
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getByBrand: jasmine.createSpy('getByBrand').and.returnValue(observableOf({ body: brandData })),
            });
            component.loadTabs();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(brandData.length).toBe(2);
        });
    });

    describe('#loadEventHubs', () => {
        it('should save and open dialog', () => {
            const tabsData = <ModuleRibbonTab>{ id: '1234' };
            const eventHubsList = [{ indexNumber: 12345, title: 'hub' }] as IEventHub[];
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getByBrand: jasmine.createSpy('getByBrand').and.returnValue(observableOf({ body: tabsData })),
            });
            moduleRibbonService.getPossibleEventHubsToMap = jasmine.createSpy('getPossibleEventHubsToMap').and
                .returnValue(observableOf({ body: eventHubsList }));
            component.loadEventHubs();
            expect(component.eventHubsList).toBe(eventHubsList);
        });
    });

    describe('#onChangeSelectedHub', () => {
        it('when eventHubname matches', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{};
            component.eventHubsList = [{ indexNumber: 1234, title: 'eventHubName' }] as IEventHub[];
            component.onChangeSelectedHub('eventHubName');
            expect(component.moduleRibbonTab.internalId).toBe('tab-eventhub-1234');
            expect(component.moduleRibbonTab.url).toBe('/home/eventhub/1234');
            expect(component.moduleRibbonTab.hubIndex).toBe(1234);
        });
    });

    describe('#handleVisibilityDateUpdate', () => {
        it('set startdate and endDate', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ displayFrom: '', displayTo: '' };
            const daterange = <DateRange>{ startDate: '2021-09-08', endDate: '2021-09-30' };
            component.handleVisibilityDateUpdate(daterange);
            expect(component.moduleRibbonTab.displayFrom).toBe(daterange.startDate);
            expect(component.moduleRibbonTab.displayTo).toBe(daterange.endDate);
        });
    });

    // describe('#validationHandler', () => {
    //     it('should save and open dialog', () => {
    //     });
    // });

    // describe('#isSegmentFormValid', () => {
    //     it('should save and open dialog', () => {
    //     });
    // });

    // describe('#modifiedSegmentsHandler', () => {
    //     it('should save and open dialog', () => {
    //     });
    // });
});