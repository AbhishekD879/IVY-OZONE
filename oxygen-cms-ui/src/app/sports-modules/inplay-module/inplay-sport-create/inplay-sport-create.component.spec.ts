
import { HomeInplayModule } from '@root/app/client/private/models/inplaySportModule.model';
import { of } from 'rxjs';
import { InplaySportCreateComponent } from './inplay-sport-create.component';


describe('InplaySportCreateComponent', () => {
    let component: InplaySportCreateComponent,
        sportsModulesService,
        brandService,
        dialogRef,
        globalLoaderService;

    const inPLaySportsMock = {
        id: 'test',
        eventCount: 11,
        categoryId: '123',
        tier: 'UNTIED',
        sportName: 'Cricket',
        brand: 'Ladbrokes'
    };

    const sportNamesMock = [{
        categoryId: 123,
        sportName: 'Cricket',
        sportTier: 'UNITED'
    },
    {
        categoryId: 1233,
        sportName: 'FootBall',
        sportTier: 'UNITED'
    }];


    const inplaySportMock: HomeInplayModule = {
        id: '123',
        eventCount: 1,
        categoryId: '123',
        tier: 'UNITED',
        sportName: 'Cricket',
        brand: 'bma',
        updatedBy: null,
        updatedAt: null,
        createdBy: null,
        createdAt: null,
        updatedByUserName: null,
        createdByUserName: null,
        inclusionList: [],
        exclusionList: [],
        universalSegment: true
    };

    const segConfigMockData = {
        exclusionList: [],
        inclusionList: [''],
        universalSegment: true
    }

    beforeEach(() => {
        sportsModulesService = {
            getAllSportNames: jasmine.createSpy('getAllSportNames').and.returnValue(of(sportNamesMock)),
            saveNewInplaySport: jasmine.createSpy('saveNewInplaySport').and.returnValue(of(inPLaySportsMock))
        };
        brandService = {
            brand: 'bma'
        };
        dialogRef = { close: jasmine.createSpy('dialogRef.close') };
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        component = new InplaySportCreateComponent(
            sportsModulesService,
            brandService,
            dialogRef,
            globalLoaderService
        );
        component.sportsList = sportNamesMock;
        component.inplaySport = inplaySportMock;
    });


    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

    it('#ngOnInit', () => {
        component.ngOnInit();
        expect(sportsModulesService.getAllSportNames).toHaveBeenCalled();
    });

    it('closeDialog', () => {
        component.closeDialog();
        expect(dialogRef.close).toHaveBeenCalled();
    });

    it('isSegmentFormValid', () => {
        component.isSegmentFormValid(true);
        expect(component.isSegmentValid).toBe(true);
    });

    it('isEventCountValid', () => {
        component.isEventCountValid();
        expect(component.inplaySport.eventCount).toBe(1);
    });

    it('modifiedSegmentsHandler', () => {
        component.modifiedSegmentsHandler(segConfigMockData);
        expect(component.inplaySport.sportName).toBe('Cricket');
    });

    it('createInplaySport', () => {
        component.createInplaySport();
        expect(sportsModulesService.saveNewInplaySport).toHaveBeenCalled();
    });

    it('onSportsChange', () => {
        component.inplaySport = inplaySportMock;
        component.onSportsChange('Cricket');
        expect(component.inplaySport.sportName).toEqual('Cricket');
    });
});
