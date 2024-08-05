import { fakeAsync, tick, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';

import { ApiClientService } from '@app/client/private/services/http';
import { AppConstants, CSPSegmentConstants } from '@app/app.constants';
import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import { Order } from '@app/client/private/models/order.model';
import { ModuleRibbonListComponent } from './module-ribbon-list.component';

describe('ModuleRibbonListComponent', () => {
    let component: ModuleRibbonListComponent;

    let apiClientService;
    let globalLoaderService;
    let dialogService;
    let router;
    let snackBar;
    let segmentManagerService;

    beforeEach(() => {
        apiClientService = {
            moduleRibbonTab: jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getByBrand: jasmine.createSpy('getByBrand').and.returnValue(of({ body: {} })),
                setOrder: jasmine.createSpy('setOrder').and.returnValue(of({ body: {} })),
                remove: jasmine.createSpy('remove').and.returnValue(of({ body: {} })),
                add: jasmine.createSpy('add').and.returnValue(of({ body: {} })),
            })
        };
        dialogService = {
            showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            }),
            showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
            showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((CreateModuleRibbonTabComponent, {
                width, title, yesOption, noOption, yesCallback
            }) => {
                yesCallback();
            })
        };
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };
        snackBar = {
            open: jasmine.createSpy('open')
        };
        router = jasmine.createSpyObj('routerSpy', ['navigate']);
        segmentManagerService = {
            getSegmentMessage: jasmine.createSpy('getSegmentMessage').and.returnValue(of({}))
        };

        component = new ModuleRibbonListComponent(
            apiClientService, globalLoaderService, dialogService, router, snackBar, segmentManagerService);
        TestBed.configureTestingModule({
            declarations: [ModuleRibbonListComponent],
            providers: [
                { provide: ApiClientService, useValue: apiClientService }
            ],
            schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA]
        }).compileComponents();
    });


    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('#ngOnit', () => {
        it('when module is segmented', fakeAsync(() => {
            segmentManagerService.getSegmentMessage = jasmine.createSpy('getSegmentMessage').and.returnValue(of(
                { segmentModule: 'module-ribbon-tab', segmentValue: 'test2' }));
            component.ngOnInit();
            tick();
            expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.moduleRibbonTab);
            expect(component.moduleRibbonTabs).toBeDefined();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
            expect(component.selectedSegment).toBe('test2');
            expect(segmentManagerService.getSegmentMessage).toHaveBeenCalled();
        }));
        it('when Module is universal', fakeAsync(() => {
            segmentManagerService.getSegmentMessage = jasmine.createSpy('getSegmentMessage').and.returnValue(of(
                { segmentModule: 'module-ribbon', segmentValue: 'test2' }));
            component.ngOnInit();
            tick();
            expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.moduleRibbonTab);
            expect(component.moduleRibbonTabs).toBeDefined();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
            expect(component.selectedSegment).toBe(CSPSegmentConstants.UNIVERSAL_TITLE);
            expect(segmentManagerService.getSegmentMessage).toHaveBeenCalled();
        }));
        it('when moduleRibbonTab is subscribed', fakeAsync(() => {
            segmentManagerService.getSegmentMessage = jasmine.createSpy('getSegmentMessage').and.returnValue(of(
                { segmentModule: 'module-ribbon', segmentValue: 'test2' }));
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                getByBrand: jasmine.createSpy('getByBrand').and.returnValue(of({ body: { id: '452435234', showTabOn: 'Desktop' } })),
            });
            component.ngOnInit();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.moduleRibbonTab);
            expect(component.moduleRibbonTabs).toBeDefined();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
            expect(component.selectedSegment).toBe(CSPSegmentConstants.UNIVERSAL_TITLE);
            expect(segmentManagerService.getSegmentMessage).toHaveBeenCalled();
        }));
    });

    describe('#visibleItems', () => {
        it('return visible records length', fakeAsync(() => {
            component.moduleRibbonTabs = [{ visible: true }, { visible: false }] as ModuleRibbonTab[];
            expect(component.visibleItems).toBe(1);
        }));
    });

    describe('#reorderHandler', () => {
        it('return visible records length', fakeAsync(() => {
            const newOrder: Order = { order: ['123'], id: '321' };
            component.reorderHandler(newOrder);
            expect(snackBar.open).toHaveBeenCalledWith(
                `NEW MODULE RIBBON TAB ORDER SAVED!!`, 'OK!',
                { duration: AppConstants.HIDE_DURATION, }
            );
        }));
    });

    describe('#removeModuleRibbonTab', () => {
        it('should show dialog and remove coupon', () => {
            component.moduleRibbonTabs = [{ id: '1' }, { id: '2' }] as ModuleRibbonTab[];
            const moduleRibbonTab = <ModuleRibbonTab>{ id: '1' };
            component.removeModuleRibbonTab(moduleRibbonTab);
            expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
                title: 'Remove Module Ribbon Tab',
                message: 'Are You Sure You Want to Remove Module Ribbon Tab?',
                yesCallback: jasmine.any(Function)
            });
            expect(apiClientService.moduleRibbonTab().remove).toHaveBeenCalledWith(moduleRibbonTab.id);
            expect(component.moduleRibbonTabs).toEqual([component.moduleRibbonTabs[0]]);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: 'Remove Completed',
                message: 'Module Ribbon Tab is Removed.'
            });
        });
    });

    describe('#createModuleRibbonTab', () => {
        it('should show dialog and remove coupon', () => {
            component.moduleRibbonTabs = [{ id: '1' }, { id: '2' }] as ModuleRibbonTab[];
            const moduleRibbonTab = <ModuleRibbonTab>{ id: '3' };
            apiClientService.moduleRibbonTab = jasmine.createSpy('moduleRibbonTab').and.returnValue({
                add: jasmine.createSpy('add').and.returnValue(of({ body: moduleRibbonTab })),
            });
            component.createModuleRibbonTab();
            expect(dialogService.showCustomDialog).toHaveBeenCalled();
            expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
            expect(component.moduleRibbonTabs.length).toBe(3);
            expect(router.navigate).toHaveBeenCalledWith(['/module-ribbon-tabs/3']);
        });
    });

    describe('#showHideSpinner', () => {
        it('call hieLoader when flag is true', fakeAsync(() => {
            component['showHideSpinner'](true);
            expect(component.isLoading).toBeTruthy();
            expect(globalLoaderService.showLoader).toHaveBeenCalled();
        }));
        it('call hieLoader when flag is false', fakeAsync(() => {
            component['showHideSpinner'](false);
            expect(component.isLoading).toBeFalsy();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
        }));
    });
});