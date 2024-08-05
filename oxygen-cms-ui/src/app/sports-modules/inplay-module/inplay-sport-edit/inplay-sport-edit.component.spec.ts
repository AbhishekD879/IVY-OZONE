
import { Params } from '@angular/router';
import { CSPSegmentLSConstants } from '@root/app/app.constants';
import { HomeInplayModule } from '@root/app/client/private/models/inplaySportModule.model';
import { ISegmentModel, ISegmentMsg } from '@root/app/client/private/models/segment.model';
import { Observable } from 'rxjs';
import { of } from 'rxjs/observable/of';
import { InplaySportEditComponent } from './inplay-sport-edit.component';

const inPLaySportsMock: HomeInplayModule = {
    id: '57fcfcd9b6aff9ba6c252a2c',
    eventCount: 11,
    categoryId: '123',
    tier: 'TIER_1',
    sportName: 'Cricket',
    brand: 'Ladbrokes',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: ''
};

const segConfigMockData: ISegmentModel = {
    exclusionList: [],
    inclusionList: ['Cricket','FootBall'],
    universalSegment: false
}

const routeParams: Params = {
    linkId: '57fcfcd9b6aff9ba6c252a2c',
    moduleId: '5beee1bbc9e77c0001fb69e3'
};

const segmentMsgMock: ISegmentMsg = {
    segmentModule: 'inplay-sport',
    segmentValue: 'Cricket'
};

describe('InplaySportEditComponent', () => {
    let component: InplaySportEditComponent,
        sportsModulesService,
        router,
        activatedRoute,
        sportsModulesBreadcrumbsService,
        segmentStoreService,
        dialogService,
        globalLoaderService;


    beforeEach(() => {

        router = {
            navigate: jasmine.createSpy('navigate'),
            url: '/current-test-url'
        };

        activatedRoute = {
            params: Observable.of(routeParams)
        };

        sportsModulesBreadcrumbsService = {
            getBreadcrubs: jasmine.createSpy('getBreadcrubs')
                .and.returnValue(Observable.of([{
                    label: 'test label',
                    url: 'test/url/inplay'
                }]))
        };

        sportsModulesService = {
            getInplaySportById: jasmine.createSpy('getInplaySportById').and.returnValue(of(inPLaySportsMock)),
            updateNewInplaySport: jasmine.createSpy('updateNewInplaySport').and.returnValue(of(inPLaySportsMock)),
            deleteSportById: jasmine.createSpy('deleteSportById').and.returnValue(of(inPLaySportsMock)),
            saveNewInplaySport: jasmine.createSpy('saveNewInplaySport').and.returnValue(of(inPLaySportsMock))
        };

        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        segmentStoreService = {
            getSegmentMessage: jasmine.createSpy('getSegmentMessage').and.returnValue(of(segmentMsgMock)),
            setSegmentValue: jasmine.createSpy('setSegmentValue')
        };

        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog')
        };

        component = new InplaySportEditComponent(
            router,
            activatedRoute,
            sportsModulesBreadcrumbsService,
            sportsModulesService,
            globalLoaderService,
            segmentStoreService,
            dialogService
        );
        component.inplaySport = inPLaySportsMock;
        component.routeParams = routeParams;
        component.inplayActionButtons = {
            extendCollection: jasmine.createSpy('extendCollection')
        };
    });


    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

    it('#ngOnInit', () => {
        spyOn(component as any, 'loadInitialData');
        activatedRoute.params = of(routeParams as Params);

        component.ngOnInit();
        expect(component.routeParams).toEqual(routeParams);
        expect(component['loadInitialData']).toHaveBeenCalled();
    });

    it('modifiedSegmentsHandler', () => {
        const inPlaySport: HomeInplayModule = {
            id: '57fcfcd9b6aff9ba6c252a2c',
            eventCount: 11,
            categoryId: '123',
            tier: 'TIER_1',
            sportName: 'Cricket',
            brand: 'Ladbrokes',
            createdBy: '',
            createdAt: '',
            updatedBy: '',
            updatedAt: '',
            updatedByUserName: '',
            createdByUserName: '',
            exclusionList: [],
            inclusionList: ['Cricket','FootBall'],
            universalSegment: false
        };
        component.modifiedSegmentsHandler(segConfigMockData);
        expect(component.inplaySport).toEqual(inPlaySport);
    });

    it('isSegmentFormValid', () => {
        component.isSegmentFormValid(true);
        expect(component.isSegmentValid).toBe(true);
    });

    it('actionsHandler remove', () => {
        component.inplaySport.id = '57fcfcd9b6aff9ba6c252a2c';
        component.routeParams = {
            linkId: '57fcfcd9b6aff9ba6c252a2c',
            moduleId: '5beee1bbc9e77c0001fb69e3'
        };

        component.actionsHandler('remove');
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(sportsModulesService.deleteSportById).toHaveBeenCalledWith('57fcfcd9b6aff9ba6c252a2c');
        expect(router.navigate).toHaveBeenCalledWith([
            'sports-pages/homepage/sports-module/inplay/5beee1bbc9e77c0001fb69e3'
          ]);
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('actionsHandler save', () => {
        component.actionsHandler('save');

        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(sportsModulesService.updateNewInplaySport).toHaveBeenCalled();
        expect(segmentStoreService.setSegmentValue).toHaveBeenCalledWith(inPLaySportsMock,CSPSegmentLSConstants.INPLAY_SPORTS_MODULE);
        expect(dialogService.showNotificationDialog).toHaveBeenCalled();
        expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
            {
              title: 'Inplay Sports Module', message: 'Inplay Sports is Saved.',
              closeCallback: jasmine.any(Function)
            }
          );
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('actionsHandler revert', () => {
        spyOn(component as any, 'loadInitialData');
        component.actionsHandler('revert');
        expect(component['loadInitialData']).toHaveBeenCalled();
        expect(component.isRevert).toBeTrue();
    });

    it('#validationHandler should validate form before update/create', () => {
      component.isSegmentValid = true;
      component.eventCount = { valid: true } as any;
      component.inplaySport = { eventCount: 1 } as any;
      expect(component.validationHandler()).toBeTruthy();
  
      component.isSegmentValid = false;
      component.eventCount = { valid: true } as any;
      component.inplaySport = { eventCount: 1 } as any;
      expect(component.validationHandler()).toBeFalsy();
  
      component.isSegmentValid = true;
      component.eventCount = { valid: true } as any;
      component.inplaySport = { eventCount: -1 } as any;
      expect(component.validationHandler()).toBeFalsy();
  
      component.isSegmentValid = true;
      component.eventCount = { valid: false } as any;
      component.inplaySport = { eventCount: 1 } as any;
      expect(component.validationHandler()).toBeFalsy();
      
      component.isSegmentValid = true;
      component.eventCount = { valid: true } as any;
      component.inplaySport = { eventCount: null } as any;
      expect(component.validationHandler()).toBeFalsy();
    });
});


