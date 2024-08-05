import { async } from '@angular/core/testing';
import { ExtraNavigationPointsListComponent } from './extra-navigation-points-list.component';
import { of } from 'rxjs';
import { Order } from '@app/client/private/models/order.model';
import { ExtraNavigationPointsCreateComponent } from '../extra-navigation-points-create/extra-navigation-points-create.component';
import { AppConstants } from '@app/app.constants';

describe('ExtraNavigationPointsListComponent', () => {
  let component, globalLoaderService,
    dialogService,
    extraNavigationPointsApiService,
    router,
    matSnackBar;

  let extraNavigationPointsListMock;

  beforeEach(async(() => {
    router = { navigate: jasmine.createSpy('navigate') };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        .and.callFake(({ title, message, yesCallback }) => yesCallback()),
      showCustomDialog: jasmine.createSpy('showCustomDialog')
        .and.callFake((ExtraNavigationPointsCreateComponent, { width, title, yesOption, noOption, yesCallback }) => yesCallback()),
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.returnValue(of({}))
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    extraNavigationPointsListMock = [
      {
        "id": "5d528924c9e77c00010872b5",
        "featureTag": "12f tag"
      }
    ]

    extraNavigationPointsApiService = {
      getNavigationPointsList: jasmine.createSpy('getNavigationPointsList').and.returnValue(of(
        {
          body: extraNavigationPointsListMock
        }
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
    component = new ExtraNavigationPointsListComponent(
      extraNavigationPointsApiService,
      globalLoaderService,
      dialogService,
      router,
      matSnackBar//,
      // segmentStoreService
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

  it('should call getNavigationPointsList method', () => {

    component.ngOnInit();
    expect(extraNavigationPointsApiService.getNavigationPointsList).toHaveBeenCalled();
  });

  it('#reorderHandler should save new navigation points', () => {
    const newOrder: Order = { order: ['123'], id: '321', segmentName: 'Universal' };
    component.reorderHandler(newOrder);
    expect(extraNavigationPointsApiService.reorderNavigationPoints).toHaveBeenCalled();
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
      let extraNavigationPoint = { id: '1' };
      component.extraNavigationPoints = [];
      component.createNavigationPoint();
      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(extraNavigationPointsApiService.createNavigationPoint);
      expect(dialogService.showCustomDialog).toHaveBeenCalledWith(
        ExtraNavigationPointsCreateComponent, {
        width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
        title: 'Add New Special Super Button',
        yesOption: 'Save',
        noOption: 'Cancel',
        yesCallback: jasmine.any(Function)
      });
      expect(extraNavigationPointsApiService.createNavigationPoint).toHaveBeenCalled();
      expect(component.extraNavigationPoints.length).toBe(1);
      expect(router.navigate).toHaveBeenCalledWith([`/quick-links/extra-navigation-points/${extraNavigationPoint.id}`]);
    });
  });

  describe('#removehandler', () => {
    it('should remove data', () => {
      let extraNavigationPoint = { id: '1', title: 'title' };
      component.extraNavigationPoints = [{ id: '1', title: 'title' }];
      component.removeHandler(extraNavigationPoint);
      expect(dialogService.showConfirmDialog).toHaveBeenCalledWith(
        {
          title: `Remove ${extraNavigationPoint.title}`,
          message: `Are You Sure You Want to Remove ${extraNavigationPoint.title}?`,
          yesCallback: jasmine.any(Function)
        });
      expect(extraNavigationPointsApiService.deleteNavigationPoint).toHaveBeenCalledWith(extraNavigationPoint.id);
      expect(component.extraNavigationPoints.length).toBe(0);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Remove Completed',
        message: 'Special Super Button is Removed'
      });
    });
  });
});
