
import { throwError } from 'rxjs';
import { of } from 'rxjs-compat/observable/of';
import { OnboardingCouponStatWidgetComponent } from './onboarding-coupon-stat-widgets.component';
import { ONBOARDING_CSW_OVERLAY } from './onboarding-CSW.mock';

describe('OnboardingCouponStatWidgetComponent', () => {
  let component: OnboardingCouponStatWidgetComponent;
  let apiService;
  let dialogService;
  let couponStatWidgetService;
  let brandService;
  let snackBar;
  let globalLoaderService;

  beforeEach(() => {
    snackBar = {
      open: jasmine.createSpy('open')
    } as any;
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog']);

    couponStatWidgetService = {
      getDetailsByBrand: jasmine.createSpy('getDetailsByBrand').and.returnValue(of({
        body: ONBOARDING_CSW_OVERLAY
      })),
      updateWelcomeOverlay: jasmine.createSpy('updateWelcomeOverlay').and.returnValue(of({
        body: ONBOARDING_CSW_OVERLAY
      })),
      removeCouponStatImage: jasmine.createSpy('removeCouponStatImage').and.returnValue(of({
        body: ONBOARDING_CSW_OVERLAY
      })),
      postNewCouponStatImage: jasmine.createSpy('removeCouponStatImage').and.returnValue(of({
        body: ONBOARDING_CSW_OVERLAY
      })),
      updateOnBoardingCouponStat: jasmine.createSpy('removeCouponStatImage').and.returnValue(of({
        body: ONBOARDING_CSW_OVERLAY
      })),
      saveOnBoardingCouponStat: jasmine.createSpy('removeCouponStatImage').and.returnValue(of({
        body: ONBOARDING_CSW_OVERLAY
      }))
    }
    apiService = {
      couponStatWidgetService: () => couponStatWidgetService
    };
    component = new OnboardingCouponStatWidgetComponent(apiService, dialogService, brandService, snackBar, globalLoaderService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  })


  it('should get details by brand', () => {
    component.ngOnInit();
    expect(component.couponStatWidget).not.toBeNull();
  });
  it('should not get details by brand, when error throwed (404)', () => {
    couponStatWidgetService.getDetailsByBrand.and.returnValue(throwError({ status: 404 }));
    component.ngOnInit();
    expect(component.couponStatWidget).not.toBeNull();
  });
  it('should not get details by brand, when error throwed (501)', () => {
    couponStatWidgetService.getDetailsByBrand.and.returnValue(throwError({ status: 501 }));
    component.ngOnInit();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Error occurred',
      message: 'Ooops... Something went wrong, please contact support team'
    });
  });

  it('should return true', () => {
    const response = component.verifyOnboarding({ id: 1 } as any);
    expect(response).toBe(true);
  });
  it('should return false', () => {
    const response = component.verifyOnboarding(null);
    expect(response).toBe(false);
  });

  it('call remove', () => {
    component.couponStatWidget = { id: '1' } as any;
    component.remove();
    expect(component.couponStatWidget).toBeDefined();
  });

  it('call remove error scenario', () => {
    couponStatWidgetService.removeCouponStatImage.and.returnValue(throwError({
      error: '401'
    }))
    component.couponStatWidget = { id: '1' } as any;
    component.remove();
    expect(component.couponStatWidget).toBeDefined();
  });

  it('call uploadCouponWidgetStat', () => {
    component.couponStatWidget = { id: '1' } as any;
    component.uploadCouponWidgetStat({} as any);
    expect(component.couponStatWidget).toBeDefined();
  });

  it('call uploadCouponWidgetStat error scenario', () => {
    couponStatWidgetService.postNewCouponStatImage.and.returnValue(throwError({
      error: '401'
    }))
    component.couponStatWidget = { id: '1' } as any;
    component.uploadCouponWidgetStat({} as any);
    expect(component.couponStatWidget).toBeDefined();
  });


  it('call actionsHandler save', () => {

    component.couponStatWidget = { createdAt: '1/2/22' } as any;
    component.actionsHandler('save');
    expect(component.couponStatWidget).toBeDefined();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Success',
      message: 'Your changes have been saved'
    });
  });

  it('call actionsHandler save error scenario', () => {
    couponStatWidgetService.updateOnBoardingCouponStat.and.returnValue(throwError({
      error: '401'
    })),
      component.couponStatWidget = { createdAt: '1/2/22' } as any;
    component.actionsHandler('save');
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Error on saving',
      message: 'Ooops... Something went wrong, please contact support team'
    });
  });

  it('call actionsHandler update', () => {
    component.couponStatWidget = {} as any;
    component.actionsHandler('save');
    expect(component.couponStatWidget).toBeDefined();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Success',
      message: 'Your changes have been saved'
    });
  });

  it('call actionsHandler revert', () => {
    component.actionsHandler('revert');
    expect(component.couponStatWidget).toBeDefined();
  });

  it('call actionsHandler default', () => {
    component.actionsHandler('edit');
    expect(component.couponStatWidget).toBeUndefined();
  });

})