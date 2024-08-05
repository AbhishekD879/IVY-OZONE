import { async } from '@angular/core/testing';
import { NavigationPointsListComponent } from './navigation-points-list.component';
import { Observable, of } from 'rxjs';
import { Order } from '@app/client/private/models/order.model';
import { AppConstants, CSPSegmentLSConstants } from '@app/app.constants';

describe('NavigationPointsListComponent', () => {
  let component, globalLoaderService,
    dialogService,
    navigationPointsApiService,
    router,
    segmentStoreService,
    matSnackBar;

  let navigationPointsListMock;
  let segmentsMock;

  beforeEach(async(() => {
    router = { navigate: jasmine.createSpy('navigate') };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        .and.callFake(({ title, message, yesCallback }) => yesCallback()),
      showCustomDialog: jasmine.createSpy('showCustomDialog')
        .and.callFake((NavigationPointsCreateComponent, { width, title, yesOption, noOption, yesCallback }) => yesCallback()),
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.returnValue(of({}))
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    segmentsMock = [
      { "id": 101, "name": "Universal" },
      { "id": 201, "name": "Cricket" }
    ];

    navigationPointsListMock = [
      {
        "id": "5d528924c9e77c00010872b5",
        "segments": ["Cricket"],
        "segmentsExcl": ["Rugby"]
      }
    ];

    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.SURFACE_BET_TAB }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };
    navigationPointsApiService = {
      getNavigationPointsBySegment: jasmine.createSpy('getNavigationPointsBySegment').and.returnValue(of(
        {body:navigationPointsListMock}
      )),
      getSegments: jasmine.createSpy('getSegments').and.returnValue(of(
        segmentsMock
      )),
      reorderNavigationPoints: jasmine.createSpy('reorderNavigationPoints').and.returnValue(of({ body: { order: ['123'], id: '321' } })),
      createNavigationPoint: jasmine.createSpy('createNavigationPoint').and.returnValue(of({ body: { id: '1' } })),
      deleteNavigationPoint: jasmine.createSpy('deleteNavigationPoint').and.returnValue(of({ body: { id: '1', title: 'title' } }))
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    matSnackBar = {
      open: jasmine.createSpy('open')
    };
    component = new NavigationPointsListComponent(
      navigationPointsApiService,
      globalLoaderService,
      dialogService,
      router,
      matSnackBar,
      segmentStoreService
    );

  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should define properties', () => {
    expect(component.searchField).toBeDefined();
    expect(component.dataTableColumns).toBeDefined();
    expect(component.searchableProperties).toBeDefined();
  });

  it('should call segmentHandler method', () => {
    let segment = 'Universal';
    component.segmentHandler(segment);
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(navigationPointsApiService.getNavigationPointsBySegment).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('should get navigationPointsList by segment', () => {
    const segment = 'Cricket';
    component['segmentHandler'](segment);
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(navigationPointsApiService.getNavigationPointsBySegment).toHaveBeenCalledWith('Cricket');
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
  
  it('#reorderHandler should save new navigation points', () => {
    const newOrder: Order = { order: ['123'], id: '321', segmentName: 'Universal' };
    component.reorderHandler(newOrder);
    expect(navigationPointsApiService.reorderNavigationPoints).toHaveBeenCalled();
    expect(matSnackBar.open).toHaveBeenCalledWith(
      'New Super Buttons Order Saved!!',
      'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
  });

  describe('#createNavigationPoint', () => {
    it('should create a navigation-point', () => {
      component.createNavigationPoint();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith([`/quick-links/navigation-points/add`]);
    });
  });

  describe('#removehandler', () => {
    it('should remove data', () => {
      let navigationPoint = { id: '1', title: 'title' };
      component.navigationPoints = [{ id: '1', title: 'title' }];
      component.removeHandler(navigationPoint);
      expect(dialogService.showConfirmDialog).toHaveBeenCalledWith(
        {
          title: `Remove ${navigationPoint.title}`,
          message: `Are You Sure You Want to Remove ${navigationPoint.title}?`,
          yesCallback: jasmine.any(Function)
        });
      expect(navigationPointsApiService.deleteNavigationPoint).toHaveBeenCalledWith(navigationPoint.id);
      expect(component.navigationPoints.length).toBe(0);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Remove Completed',
        message: 'Super Button is Removed'
      });
    });
  });
});
