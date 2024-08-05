import { CreateModuleRibbonTabComponent } from './create-module-ribbon-tab.component';
import { of as observableOf } from 'rxjs';

import { DateRange } from '@app/client/private/models/dateRange.model';
import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';

describe('CreateModuleRibbonTabComponent', () => {
    let component: CreateModuleRibbonTabComponent;
    let data;
    let dialogRef;
    let brandService;
    let moduleRibbonService;

    beforeEach(() => {
        moduleRibbonService = {
            getPossibleEventHubsToMap: jasmine.createSpy('getPossibleEventHubsToMap').and.returnValue(observableOf({ body: {} })),
        };
        dialogRef = {
            close: jasmine.createSpy("close"),
        };
        brandService = {
            brand: "bma",
        };
        component = new CreateModuleRibbonTabComponent(
            data, dialogRef, brandService, moduleRibbonService);
    });

    it('should edit', () => {
        expect(component).toBeTruthy();
    });

    describe('#ngOnInit', () => {
        it('should call loadInitData', () => {
            component.data = { data: { currentTabs: '1234', title: 'eventHub' } };
            component.ngOnInit();
            expect(moduleRibbonService.getPossibleEventHubsToMap).toHaveBeenCalled();
        });
    });

    describe('#getNewModuleRibbonTab', () => {
        it('returns moduleRibbontab data', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ directiveName: 'EventHub' };
            expect(component.getNewModuleRibbonTab()).toBe(component.moduleRibbonTab);
        });
    });

    describe('#isValidModuleRibbonTab', () => {
        it('return false when moduleRibbonTab is undefined', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{};
            expect(component.isValidModuleRibbonTab()).toBeFalsy();
        });
        it('return false when any one of the moduleRibbonTab is defined', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ brand: 'bma' };
            expect(component.isValidModuleRibbonTab()).toBeFalsy();
        });
        it('return true when any one of the moduleRibbonTab is defined', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{
                brand: 'bma', directiveName: 'test', title: 'test', internalId: '1234', url: '/module-ribbon', showTabOn: 'true'
            };
            expect(component.isValidModuleRibbonTab()).toBeTruthy();
        });
    });

    describe('#closeDialog', () => {
        it('close method to be called', () => {
            component["closeDialog"]();
            expect(dialogRef.close).toHaveBeenCalled();
        });
    });

    describe('#onChangeDirectiveName', () => {
        it('set moduleRibbontab directiveName', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ directiveName: '' };
            component.onChangeDirectiveName('test');
            expect(component.moduleRibbonTab.directiveName).toBe('test');
        });
    });

    describe('#isEventHubTab', () => {
        it('return true when directiveName matches', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ directiveName: 'EventHub' };
            expect(component.isEventHubTab()).toBeTruthy();
        });
        it('return false when directiveName matches', () => {
            component.moduleRibbonTab = <ModuleRibbonTab>{ directiveName: 'test' };
            expect(component.isEventHubTab()).toBeFalsy();
        });
    });

    describe('#loadEventHubs', () => {
        it('should return eventHubsNames', () => {
            component.data = { data: { currentTabs: '1234', title: 'eventHub' } };
            const eventHubsList = [{ indexNumber: 12345, title: 'hub' }, { indexNumber: 12345, title: 'hub123' }];
            moduleRibbonService.getPossibleEventHubsToMap = jasmine.createSpy('getPossibleEventHubsToMap').and
                .returnValue(observableOf(eventHubsList));
            component.loadEventHubs();
            expect(component.eventHubsList).toEqual(eventHubsList as IEventHub[]);
            expect(component.eventHubsNames).toEqual(["hub", "hub123"]);
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
});