import { of, throwError } from 'rxjs';

import { NavigationsComponent } from '@app/promotions/navigations/navigations.component';
import { AppConstants } from '@app/app.constants';
import { fakeAsync, tick } from '@angular/core/testing';

describe('NavigationsComponent', () => {
  let component: NavigationsComponent;
  let apiClientService, globalLoaderService, snackBar, dialogService, router;
  const mockNavData = {
    id: '62c80bd6bc54f74ed94d52d8',
    createdBy: '54905d04a49acf605d645271',
    createdByUserName: 'test.admin@coral.co.uk',
    updatedBy: '54905d04a49acf605d645271',
    updatedByUserName: 'test.admin@coral.co.uk',
    createdAt: '2022-07-08T10:49:58.638Z',
    updatedAt: '2022-07-08T10:49:58.638Z',
    brand: 'ladbrokes',
    title: 'Cricket2',
    status: 'Active'
  };
  const mockNavGroup = {
    id: '62c80bd6bc54f74ed94d52d8',
    title: 'Cricket2',
    status: true,
    updatedAt: '2022-07-08T10:49:58.638Z',
    promotionIds: [],
    navItems: []
  };

  beforeEach(() => {
    apiClientService = {
      promotionsNavigationsService: jasmine.createSpy('promotionsNavigationsService').and.returnValue(
        {
          findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: [mockNavData] })),
          postNewPromotionsNavigationsOrder: jasmine.createSpy('reorder').and.returnValue(of({ body: [] })),
          add: jasmine.createSpy('add').and.returnValue(of({ body: [] })),
          remove: jasmine.createSpy('remove').and.returnValue(of({ body: [] })),
        }
      ),
      
     
    };
    dialogService = {
        showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
        showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
            yesCallback();
        }),
        showCustomDialog: jasmine.createSpy('showCustomDialog').and
          .callFake((AddNavigationGroupComponent, { width, title, yesOption, noOption, yesCallback }) =>
            yesCallback(mockNavData)
    )};
    globalLoaderService = {
        showLoader: jasmine.createSpy('showLoader'),
        hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = jasmine.createSpyObj('snackBarSpy', ['open']);
    router = { navigate: jasmine.createSpy('navigate'), };
    component = new NavigationsComponent(
      apiClientService,
      globalLoaderService,
      dialogService,
      snackBar,
      router
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should Init', fakeAsync(() => {

    component.ngOnInit();

    tick();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component.isLoading).toEqual(false);
    expect(apiClientService.promotionsNavigationsService().findAllByBrand).toHaveBeenCalled();
  }));

  it('should re order the navigation groups based on the selected order', () => {
    const newOrder = { id: '1', order: ['first', 'second'] };
    component['reorderHandler'](newOrder);
    expect(apiClientService.promotionsNavigationsService().postNewPromotionsNavigationsOrder).toHaveBeenCalledWith(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith('New Promotions Navigations Order Saved!!', 'Ok!', {
    duration: AppConstants.HIDE_DURATION,
    });
  });


  describe('addNavigationGroup', () => {
    it('add navigation group', fakeAsync(() => {
      component.navigationGroup = [mockNavGroup];
      component['addNavigationGroup']();
      tick();
      tick();
      expect(dialogService.showCustomDialog).toHaveBeenCalled();
    }));

    it('addNavigationGroup Error scenario', fakeAsync(() => {
      apiClientService.promotionsNavigationsService().add.and.returnValue(throwError(new Error('message')));
      component.navigationGroup = [mockNavGroup];
      component['addNavigationGroup']();
      tick();
      tick();
      expect(dialogService.showCustomDialog).toHaveBeenCalled();
    }));
  });
  it('remove navigation group', () => {

    component.navigationGroup = [mockNavGroup];
    component['removeNavigationGroup'](mockNavGroup);
    expect(apiClientService.promotionsNavigationsService().remove).toHaveBeenCalledWith('62c80bd6bc54f74ed94d52d8', '""');
  });

  it('should hide spinner', () => {
    component['hideSpinner']();
    expect(component.isLoading).toEqual(false);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

});
