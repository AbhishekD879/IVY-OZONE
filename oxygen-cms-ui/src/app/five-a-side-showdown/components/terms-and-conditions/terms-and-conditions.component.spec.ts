import { of, throwError } from 'rxjs';

import { TermsAndConditionsComponent
 } from '@app/five-a-side-showdown/components/terms-and-conditions/terms-and-conditions.component';
import { T_AND_C } from '@app/five-a-side-showdown/components/terms-and-conditions/terms-and-conditions.mock';

describe('TermsAndConditionsComponent', () => {
  let component: TermsAndConditionsComponent;
  let apiService;
  let dialogService;
  let brandService;
  let termsConditionService;

  beforeEach(() => {
    termsConditionService = {
      getDetailsByBrand: jasmine.createSpy('getDetailsByBrand').and.returnValue(of({
        body: T_AND_C
      })),
      updateTermsAndConditions: jasmine.createSpy('updateTermsAndConditions').and.returnValue(of({
        body: T_AND_C
      })),
      saveTermsAndConditions: jasmine.createSpy('saveTermsAndConditions').and.returnValue(of({
        body: T_AND_C
      }))
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback(T_AND_C);
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    apiService = {
      termsConditionService: () => termsConditionService
    };
    component = new TermsAndConditionsComponent(apiService, dialogService, brandService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should get details by brand', () => {
      component.headerTextEditor = {
        update: jasmine.createSpy('update')
      } as any;
      component.ngOnInit();
      expect(component.termsAndConditions).not.toBeNull();
    });
    it('should not get details by brand, when error throwed (404)', () => {
      termsConditionService.getDetailsByBrand.and.returnValue(throwError({error: {status: '404'}}));
      component.headerTextEditor = {
        update: jasmine.createSpy('update')
      } as any;
      component.ngOnInit();
      expect(component.termsAndConditions).not.toBeNull();
    });
    it('should not get details by brand, when error throwed (501)', () => {
      termsConditionService.getDetailsByBrand.and.returnValue(throwError({error: {status: '501'}}));
      component.headerTextEditor = {
        update: jasmine.createSpy('update')
      } as any;
      component.ngOnInit();
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Error occurred',
        message: 'Ooops... Something went wrong, please contact support team'
      });
    });
  });

  describe('#actionsHandler', () => {
    it('should save t&c', () => {
      component.termsAndConditions = {
        createdAt: ''
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(component.termsAndConditions).not.toBeNull();
    });
    it('should edit t&c', () => {
      component.termsAndConditions = {
        createdAt: '1234'
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(component.termsAndConditions).not.toBeNull();
    });
    it('should edit t&c (With Error)', () => {
      termsConditionService.updateTermsAndConditions.and.returnValue(throwError({error: '404'}))
      component.termsAndConditions = {
        createdAt: '1234'
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Error on saving',
        message: 'Ooops... Something went wrong, please contact support team'
      });
    });
    it('should revert faq', () => {
      spyOn(component as any, 'loadInitialData');
      const event = 'revert';
      component.actionsHandler(event);
      expect(component['loadInitialData']).toHaveBeenCalled();
    });
    it('should set default condition', () => {
      spyOn(console, 'error');
      const event = 'racdom';
      component.actionsHandler(event);
      expect(component.termsAndConditions).toBeUndefined();
    });
  });

  describe('#updateBlurb', () => {
    it('should update question field when not empty', () => {
      component.termsAndConditions = {
        text: null
      } as any;
      component['updateBlurb']('new Text');
      expect(component.termsAndConditions.text).toEqual('new Text');
    });
    it('should not update question field when empty', () => {
      component.termsAndConditions = {
        text: null
      } as any;
      component['updateBlurb'](null);
      expect(component.termsAndConditions.text).toBeNull();
    });
  });

  describe('#verifyTermsAndConditions', () => {
    it('should return true', () => {
      const response = component.verifyTermsAndConditions({ id: 1} as any);
      expect(response).toBe(true);
    });
    it('should return false', () => {
      const response = component.verifyTermsAndConditions(null);
      expect(response).toBe(false);
    });
  });
});
