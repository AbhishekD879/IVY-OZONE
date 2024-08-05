import { async } from '@angular/core/testing';
import { of } from 'rxjs';
import * as _ from 'lodash';
import { SportsQuickLinksCreateComponent } from './sports-quick-links-create.component';

describe('SportsQuickLinksCreateComponent', () => {
    let component: SportsQuickLinksCreateComponent,
        sportQuickLinksService,
        dialogRef,
        brandService,
        globalLoaderService,
        segmentStoreService;

    let quickLinksListMock: any;

    beforeEach(async(() => {
        globalLoaderService = {};
        dialogRef = {};
        brandService = {};
        segmentStoreService = {};
        
        quickLinksListMock = [{
            id: 'default',
            sportId: 0,
            pageType: 'sport',
            brand: 'Coral',
            disabled: true,
            sortOrder: 0,
            inclusionList: [],
            exclusionList: [],
            applyUniversalSegments: false
        }];

        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };
        
        let path = 'homepage/sports-quicklinks';
        segmentStoreService = {
            validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
            validateHomeModule: () => path.includes('homepage'),
        }


        sportQuickLinksService = {
            isValidLink: jasmine.createSpy('isValidLink').and.returnValue(of(
                true
            )),
            currentLinksList: jasmine.createSpy('currentLinksList').and.returnValue(of(
                quickLinksListMock
            ))
        };

        brandService = {
            isIMActive: jasmine.createSpy('isIMActive').and.returnValue(true)
        };

        component = new SportsQuickLinksCreateComponent(
            {},
            sportQuickLinksService,
            dialogRef,
            brandService,
            segmentStoreService,
            globalLoaderService
        );

        component.ngOnInit();
    }));

    it('should Init component data', () => {
        expect(component.sportsQuickLinksList).toBeDefined();
        expect(component.segmentsList).toBeDefined();
        expect(component.isSegmentValid).toBeDefined();
    });

    it('should check if segment is valid', () => {
        let flag = true;
        component.isSegmentFormValid(flag);
        expect(component.isSegmentValid).toBeTrue();
    })

    it('should check if segment is valid', () => {
        let flag = false;
        component.isSegmentFormValid(flag);
        expect(component.isSegmentValid).toBeFalse();
    })
});
