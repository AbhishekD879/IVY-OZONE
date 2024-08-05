import { async } from '@angular/core/testing';
import { Observable, of } from 'rxjs';
import { SportsQuickLinksListComponent } from './sports-quick-links-list.component';
import { CSPSegmentLSConstants } from '@app/app.constants';

describe('SportsQuickLinksListComponent', () => {
    let component: SportsQuickLinksListComponent;

    let globalLoaderService,
        apiClientService,
        sportQuickLinksService,
        errorService,
        dialogService,
        segmentStoreService,
        matSnackBar,
        activatedRoute;

    let quickLinksListMock: any;

    beforeEach(async(() => {

        quickLinksListMock = [
            {
                "id": "5d528924c9e77c00010872b5",
                "inclusionList": ["Cricket"],
                "exclusionList": ["Rugby"]
            }
        ]

        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        apiClientService = {
            sportsQuickLink: jasmine.createSpy('sportsQuickLink').and.returnValue({
                reorder: jasmine.createSpy('reorder').and.returnValue(of({
                    body: {}
                })),
                delete: jasmine.createSpy('delete').and.returnValue(of({
                    body: {}
                }))
            })
        }

        sportQuickLinksService = {
            getSportsQuickLinks: jasmine.createSpy('getSportsQuickLinks').and.returnValue(of(
                quickLinksListMock
            )),
            loadQuickLinks: jasmine.createSpy('loadQuickLinks').and.returnValue(of(
                quickLinksListMock
            )),
            loadSegmentQuickLinks: jasmine.createSpy('loadSegmentQuickLinks').and.returnValue(of(
                quickLinksListMock
            )),
            validateLinks: jasmine.createSpy('validateLinks').and.returnValue(of(
                quickLinksListMock
            )),
            maxLinksAmount: jasmine.createSpy('maxLinksAmount').and.returnValue(3),
            isLinksListValid: jasmine.createSpy('isLinksListValid').and.returnValue(true),
            getHubIndex: jasmine.createSpy('getHubIndex').and.returnValue(Observable.of(0)),
        };

        errorService = {
          emitError: jasmine.createSpy('emitError')
        };

        dialogService = {
            showConfirmDialog: jasmine.createSpy('showConfirmDialog')
                .and.returnValue(Observable.of({}))
                .and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            })
        };

        let path = 'homepage/sports-quicklinks';
    
        segmentStoreService = {
          validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
          validateHomeModule: () => path.includes('homepage'),
          getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.SPORTS_QUICK_LINK }),
          updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
        };

        activatedRoute = {
          snapshot: {
            paramMap: {
              get: jasmine.createSpy('paramMap.get').and.returnValue('12345')
            }
          },
          params: of({
            sport: 'football',
            id: '12345'
          })
        };

        matSnackBar = {
            open: jasmine.createSpy('open')
        };

        component = new SportsQuickLinksListComponent(
            apiClientService,
            sportQuickLinksService,
            errorService,
            dialogService,
            globalLoaderService,
            activatedRoute,
            matSnackBar,
            segmentStoreService
        );
    }));

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should success showLoader', () => {
        component.ngOnInit();
        expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
    });

    it('should define properties', () => {
        expect(component.sportsQuickLinks).toBeDefined();
        expect(component.searchField).toBeDefined();
        expect(component.dataTableColumns).toBeDefined();
        expect(component.searchableProperties).toBeDefined();
    });

    it('should call segmentHandler method', () => {
        const segment = 'Cricket';
        component['segmentHandler'](segment);
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledTimes(1);
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should get quickLinksList by segment', () => {
        component.selectedSegment = 'Cricket';
        component.pageId = '0';
        component.pageType = 'sport';
        component['segmentHandler'](component.selectedSegment);
        expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledWith(component.selectedSegment, component.pageId, component.pageType);
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledTimes(1);
        expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(1);

        expect(component.sportsQuickLinks).toEqual(quickLinksListMock);
    });

    it('should not get any quickLinksList if there is no segment matching', () => {
        sportQuickLinksService.loadSegmentQuickLinks.and.returnValue(of(null));
        component.selectedSegment = 'FootBall';
        component.pageId = '0';
        component.pageType = 'sport';
        component['segmentHandler'](component.selectedSegment);
        expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledWith(component.selectedSegment, component.pageId, component.pageType);
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledTimes(1);

        expect(component.sportsQuickLinks).toEqual(null);
    });

    it('should get all quickLinksList if the segment is null', () => {
        sportQuickLinksService.loadSegmentQuickLinks.and.returnValue(of(quickLinksListMock[0]));
        component.selectedSegment = null;
        component.pageId = '0';
        component.pageType = 'sport';
        component['segmentHandler'](component.selectedSegment);
        expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledWith(component.selectedSegment, component.pageId, component.pageType);
        expect(sportQuickLinksService.loadSegmentQuickLinks).toHaveBeenCalledTimes(1);
        expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(1);

        expect(component.sportsQuickLinks).toEqual(quickLinksListMock[0]);
    });

    it('#reorderHandler should save new quick links', () => {
        const REORDER_MOCK = {
        id: '5fd20007eecbb12b1e9678a1',
        order: [
          '5fd20007eecbb12b1e9678a1',
          '5fd20021eecbb12b1e9678a3',
          '5fd775d551b2c11cb747e20c',
          '5fd99526be7df85d739c6f6d',
          '5fd775d551b2c11cb747e20b',
          '5fd775d651b2c11cb747e20d'
        ]
      };
        component['reorderHandler'](REORDER_MOCK);
        expect(matSnackBar.open).toHaveBeenCalled();
    });
});