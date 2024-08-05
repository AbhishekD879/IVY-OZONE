import { FanzoneAppModuleService } from "@app/fanzone/services/fanzone-module.service";
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { FANZONE_BANNER, FANZONE_DETAILS, FANZONE_TAB, FANZONE_TEAM_DATA } from "@app/fanzone/services/mockdata/fanzone-module.service.mock";
import { REQUEST_PARAMS, GEN_FILTER_PARAMS, STRIP_EVENT_ENTITY, typeEventsSSResponse } from '@app/fanzone/mockData/fanzone-outrights.component.mock';

describe('FanzoneAppModuleService', () => {
    let service;
    let vanillaApiService;
    let siteServerRequestHelperService;
    let timeService;
    let ssUtility;
    let buildUtility;
    let simpleFilters;

    const fanzoneDetails = FANZONE_DETAILS;
    const fanzoneBanner = FANZONE_BANNER;
    const teamData = FANZONE_TEAM_DATA;
    const fanzoneTab = FANZONE_TAB;

    beforeEach(() => {

        vanillaApiService = {
            get: jasmine.createSpy('get').and.returnValue(of(fanzoneBanner))
        };

        siteServerRequestHelperService = {
            getOutrightsByTypeIds: jasmine.createSpy().and.returnValue(Promise.resolve(typeEventsSSResponse))
        };

        timeService = {
            getSuspendAtTime: jasmine.createSpy('getSuspendAtTime').and.returnValue('2022-03-23T13:37:30.000Z')
        };

        ssUtility = {
            queryService: jasmine.createSpy('queryService').and.returnValue(Promise.resolve([])),
            stripResponse: jasmine.createSpy('stripResponse').and.callFake(e => e)
        };

        simpleFilters = {
            genFilters: jasmine.createSpy().and.returnValue(REQUEST_PARAMS.simpleFilters)
        } as any;

        buildUtility = {
            eventBuilder: jasmine.createSpy('eventBuilder')
        };

        service = new FanzoneAppModuleService(
            vanillaApiService,
            siteServerRequestHelperService,
            timeService,
            ssUtility,
            buildUtility,
            simpleFilters
        );

    });

    it('should create service instance', () => {
        expect(service).toBeTruthy();
    });

    it('Should Retrieves list of fanzone banners from sitecore', () => {
        service.getFanzoneImagesFromSiteCore().subscribe((fanzoneBannerData) => {
            expect(fanzoneBannerData).toEqual(fanzoneBanner)
        });
    });

    it('should return the tab data', () => {
        const tab = service.createTab('NOW & NEXT', 'now_next', '/fanzone', true);

        expect(tab).toEqual(fanzoneTab);
    });

    it('should return the tab data with visible set as false', () => {
        const tab = service.createTab('NOW & NEXT', 'now_next', '/fanzone', false);

        expect(tab).toEqual({ title: 'NOW & NEXT', id: 'now_next', url: '/fanzone', visible: false, showTabOn: 'both', newSignPostingIcon: false });
    });

    it('should return the tab data with visible set as true', () => {
        const tab = service.createTab('NOW & NEXT', 'now_next', '/fanzone');

        expect(tab).toEqual(fanzoneTab);
    });

    it('should return the tab data with url and visible field default value ', () => {
        const tab = service.createTab('NOW & NEXT', 'now_next');

        expect(tab).toEqual({ title: 'NOW & NEXT', id: 'now_next', url: '', visible: true, showTabOn: 'both', newSignPostingIcon: false });
    });

    it('getFanzoneOutrights', fakeAsync(() => {
        ssUtility.queryService.and.callFake(method => {
            method('test data');
            return Promise.resolve(STRIP_EVENT_ENTITY);
        });

        service.getFanzoneOutrights(REQUEST_PARAMS.typeId, '4dsgumo7d4zupm2ugsvm4zm4d');
        tick();

        expect(simpleFilters.genFilters).toHaveBeenCalledWith(GEN_FILTER_PARAMS as any);
        expect(ssUtility.queryService).toHaveBeenCalledWith(
            jasmine.any(Function),
            {
                typeId: REQUEST_PARAMS.typeId,
                simpleFilters: REQUEST_PARAMS.simpleFilters
            }
        );
        expect(siteServerRequestHelperService.getOutrightsByTypeIds).toHaveBeenCalled();
    }));
});
