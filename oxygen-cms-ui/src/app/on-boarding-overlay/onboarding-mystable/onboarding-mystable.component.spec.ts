
import { of, throwError } from "rxjs";
import { OnboardingMystableComponent } from "./onboarding-mystable.component";
import { ONBOARDING_OVERLAY_MyStable_DEFAULT_VALUES } from "../onboarding-coupon-stat-widgets/on-boarding-overlay.constants";

describe('OnboardingMystableComponent', () => {
  let component: OnboardingMystableComponent;
  let apiService;
  let dialogService;
  let brandService;
  let snackBar;
  let globalLoaderService;
  let router;


  beforeEach(() => {

    apiService = {
      myStableService: jasmine.createSpy('myStableService')
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };

    brandService = {
      brand: jasmine.createSpy('brand').and.returnValue('coral')
    };

    snackBar = {
      open: jasmine.createSpy('open')
    };

    component = new OnboardingMystableComponent(apiService, dialogService, brandService, snackBar, globalLoaderService, router);

  });

  describe('mystable onboarding', () => {

    it('should call ngOnInit from  mystable onboarding', () => {
      spyOn<any>(component, 'loadInitialData');
      component.ngOnInit();
    });

    it('should call revert ', () => {
      spyOn<any>(component, 'loadInitialData');
      component['revert']();
    });

    it('should call getButtonName', () => {
      const fileName = 'example.txt';
      const result = component.getButtonName(fileName);
      expect(result).toEqual('Change File');
    });

    it('should call getButtonName when there is no fileName', () => {
      const fileName = '';
      const result = component.getButtonName(fileName);
      expect(result).toEqual('Upload File');
    });

    it('should call save', () => {
      spyOn<any>(component, 'save');
      component.actionsHandler('save');
      expect(component['save']).toHaveBeenCalled();
    });

    it('should call revert', () => {
      spyOn<any>(component, 'revert');
      component.actionsHandler('revert');
      expect(component['revert']).toHaveBeenCalled();
    });

    it('should not call save or revert', () => {
      spyOn<any>(component, 'save');
      spyOn<any>(component, 'revert');
      component.actionsHandler('test');
      expect(component['save']).not.toHaveBeenCalled();
      expect(component['revert']).not.toHaveBeenCalled();
    });

    it('should return true if def is there', () => {
      const def = { fileName: 'example.txt', buttonText: 'Click Me' } as any;
      const result = component.verifyOnboarding(def);
      expect(result).toBeTruthy();
    });

    it('should return false if no buttontext ', () => {
      const def = { fileName: 'example.txt' } as any;
      const result = component.verifyOnboarding(def);
      expect(result).toBeFalsy();
    });

    it('should return false if def no buttonText ', () => {
      const def = { buttonText: 'Click Me' } as any;
      const result = component.verifyOnboarding(def);
      expect(result).toBeFalsy();
    });

    it('should return false if buttonText length > 12', () => {
      const def = { fileName: 'example.txt', buttonText: 'ThisButtonTextIsTooLong' } as any;
      const result = component.verifyOnboarding(def);
      expect(result).toBeFalsy();
    });

    it('should return false if no def', () => {
      const def = undefined;
      const result = component.verifyOnboarding(def);
      expect(result).toBeFalsy();
    });

    it('should call sendRequest with updateOnBoardingMyStable', () => {
      spyOn<any>(component, 'sendRequest');
      component.myStable = { id: 1 } as any;
      component['save']();
      expect(component['sendRequest']).toHaveBeenCalledWith('updateOnBoardingMyStable');
    });

    it('should call sendRequest with saveOnBoardingMyStable', () => {
      spyOn<any>(component, 'sendRequest');
      component.myStable = {} as any;
      component['save']();
      expect(component['sendRequest']).toHaveBeenCalledWith('saveOnBoardingMyStable');
    });

    it('should call getDefaultValues and return default values', () => {
      brandService.brand.and.returnValue('coral');
      component['getDefaultValues']();
    });

    it('should call handleUploadImageClick', () => {
      const inputElement = { click: jasmine.createSpy('click') };
      component['onboardImageUpload'] = { nativeElement: inputElement } as any;
      component.handleUploadImageClick();
      expect(inputElement.click).toHaveBeenCalled();
    });

    it('should load initial data', () => {
      const responseData = { body: {} } as any;
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['getDetailsByBrand']);
      myStableServiceSpyObj.getDetailsByBrand.and.returnValue(of(responseData));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component.actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any;
      component['loadInitialData']();
      expect(component.myStable).toEqual(responseData.body);
    });

    it('should load initial data', () => {
      const responseData = { body: { onboardImageDetails: { originalname: 'test', path: 'testPath' } } } as any;
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['getDetailsByBrand']);
      myStableServiceSpyObj.getDetailsByBrand.and.returnValue(of(responseData));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component['loadInitialData']();
      expect(component.myStable).toEqual(responseData.body);
    });

    it('should handle 404 error ', () => {
      const errorResponse = { status: 404 };
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['getDetailsByBrand']);
      myStableServiceSpyObj.getDetailsByBrand.and.returnValue(throwError(errorResponse));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      spyOn<any>(component, 'getDefaultValues');
      component['loadInitialData']();
      expect(component['getDefaultValues']).toHaveBeenCalled();
      expect(component['router'].navigate).toHaveBeenCalledWith(['/on-boarding-overlay/onboarding-mystable']);
    });

    it('should handle 500 error ', () => {
      const errorResponse = { status: 500 };
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['getDetailsByBrand']);
      myStableServiceSpyObj.getDetailsByBrand.and.returnValue(throwError(errorResponse));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component['loadInitialData']();
      expect(component['dialogService'].showNotificationDialog).toHaveBeenCalled();
    });

    it('should set myStable to default values when data.body is empty', () => {
      const responseData = { body: null };
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['getDetailsByBrand']);
      myStableServiceSpyObj.getDetailsByBrand.and.returnValue(of(responseData));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component['loadInitialData']();
      expect(component.myStable).toEqual(ONBOARDING_OVERLAY_MyStable_DEFAULT_VALUES);
    });

    it('should upload supported file without imgEntityId', () => {
      const file = new File(['file content'], 'example.jpg', { type: 'image/jpeg' });
      spyOn(component, 'uploadImage');
      component.prepareToUploadFile({ target: { files: [file] } });
      expect(component['dialogService'].showNotificationDialog).not.toHaveBeenCalled();
      expect(component.uploadImage).toHaveBeenCalledWith(file);
    });

    it('should show error dialog for unsupported file', () => {
      const file = new File(['file content'], 'example.txt', { type: 'text/plain' });
      spyOn(component, 'uploadImage');
      component.prepareToUploadFile({ target: { files: [file] } });
      expect(component.uploadImage).not.toHaveBeenCalled();
    });

    it('should call UpdateUploadImage', () => {
      const file = new File(['file content'], 'example.jpg', { type: 'image/jpeg' });
      component.imgEntityId = 123 as any;
      spyOn(component, 'UpdateUploadImage');
      component.prepareToUploadFile({ target: { files: [file] } });
      expect(component['dialogService'].showNotificationDialog).not.toHaveBeenCalled();
      expect(component.UpdateUploadImage).toHaveBeenCalledWith(file, 123);
    });

    it('should construct FormData and upload image successfully', () => {
      const file = new File(['file content'], 'example.jpg', { type: 'image/jpeg' });
      component.myStable = { isActive: true, buttonText: 'Upload', fileName: '', imageUrl: '' } as any;
      const postRes = { body: { onboardImageDetails: { originalname: 'uploaded.jpg', path: '/path/to/uploaded.jpg' } } };
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['postNewMyStableImage']);
      myStableServiceSpyObj.postNewMyStableImage.and.returnValue(of(postRes));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component.uploadImage(file);
      expect(component.onboardFormData instanceof FormData).toBe(true);
      expect(component.onboardFormData.get('onboardImg')).toBe(file);
      expect(component.onboardFormData.get('isActive')).toBe('true');
      expect(component.onboardFormData.get('buttonText')).toBe('Upload');
      expect(component.onboardFormData.get('brand')).toBeDefined();
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(component.myStable.fileName).toBe('uploaded.jpg');
    });


    it('should construct FormData and update image successfully', () => {
      const file = new File(['file content'], 'example.jpg', { type: 'image/jpeg' }) as any;
      component.myStable = { isActive: true, buttonText: 'Update', fileName: 'existing.jpg', imageUrl: '/path/to/existing.jpg' } as any;
      const postRes = { body: { onboardImageDetails: { originalname: 'uploaded.jpg', path: '/path/to/uploaded.jpg' } } };
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['updateNewMyStableImage']);
      myStableServiceSpyObj.updateNewMyStableImage.and.returnValue(of(postRes));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component.UpdateUploadImage(file, 123);
      expect(component.onboardFormData instanceof FormData).toBe(true);
      expect(component.onboardFormData.get('onboardImg')).toBe(file);
      expect(component.onboardFormData.get('isActive')).toBe('true');
      expect(component.onboardFormData.get('buttonText')).toBe('Update');
      expect(component.onboardFormData.get('brand')).toBeDefined();
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(component.myStable.fileName).toBe('uploaded.jpg');
    });

    it('should remove uploaded image successfully', () => {
      component.myStable = { id: 123, isActive: true, buttonText: 'Update', fileName: 'existing.jpg', imageUrl: '/path/to/existing.jpg' } as any;
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['removeMyStableUploadedImage']);
      myStableServiceSpyObj.removeMyStableUploadedImage.and.returnValue(of({ body: {} }));
      const mockNativeElement = jasmine.createSpyObj('mockNativeElement', ['value']);
      component['onboardImageUpload'] = { nativeElement: mockNativeElement } as any;
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component.removeUploadMystableImage();
      expect(component['onboardImageUpload'].nativeElement.value).toBe('');
      expect(component.myStable.fileName).toBe('');
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should call saveOnBoardingMyStable', () => {
      const responseData = { body: {} } as any;
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['saveOnBoardingMyStable']);
      myStableServiceSpyObj.saveOnBoardingMyStable.and.returnValue(of(responseData));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component.actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any;
      component['sendRequest']('saveOnBoardingMyStable');
      expect(component['dialogService'].showNotificationDialog).toHaveBeenCalledWith({
        title: 'Success',
        message: 'Your changes have been saved'
      });
    });

    it('should all saveOnBoardingMyStable with 500', () => {
      const errorResponse = { status: 500 };
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['saveOnBoardingMyStable']);
      myStableServiceSpyObj.saveOnBoardingMyStable.and.returnValue(throwError(errorResponse));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component['sendRequest']('saveOnBoardingMyStable');
      expect(component['dialogService'].showNotificationDialog).toHaveBeenCalledWith({
        title: 'Error on saving',
        message: 'Ooops... Something went wrong, please contact support team'
      });
    });

    it('should call saveOnBoardingMyStable', () => {
      const responseData = { body: {} } as any;
      const myStableServiceSpyObj = jasmine.createSpyObj('MyStableService', ['saveOnBoardingMyStable']);
      myStableServiceSpyObj.saveOnBoardingMyStable.and.returnValue(of(responseData));
      apiService.myStableService.and.returnValue(myStableServiceSpyObj);
      component.actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any;
      component['sendRequest']('saveOnBoardingMyStable', true);
      expect(component['dialogService'].showNotificationDialog).not.toHaveBeenCalled();
    });

  })

});
