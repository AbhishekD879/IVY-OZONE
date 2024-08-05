import { SplashPageComponent } from './splash-page.component';
import { of } from 'rxjs';
import { SplashTestData } from '@app/client/private/models/freeRideSplashScreen.model';
import { fakeAsync, tick } from '@angular/core/testing';
import { FormControl, FormGroup } from '@angular/forms';

describe('SplashPageComponent', () => {
  let component: SplashPageComponent;
  let dialogService;
  let brandService;
  let freeRideService;
  const splashData = {};
  const getAllSplashData = SplashTestData;

  beforeEach(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
        yesCallback();
      })
    };
    brandService = {};
    freeRideService = {
      getAllSplashData: jasmine.createSpy('getAllSplashData').and.returnValue(of(getAllSplashData)),
      splashData: jasmine.createSpy('splashData').and.returnValue(of({ body: splashData }))
    };
    component = new SplashPageComponent(
      dialogService, freeRideService, brandService
    );
  });
  it('constructor', () => {
    expect(component).toBeDefined();
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });


  describe('ngOnInit', () => {
    it('general calls', fakeAsync(() => {
      component.splashFormGroup = new FormGroup({});
       spyOn(component, 'createFormGorup');
       spyOn(component, 'loadSplashData');
      component.splashFormGroup = new FormGroup({});
       component.splashFormGroup.addControl('welcomeMsg', new FormControl('test'));
       component.splashFormGroup.addControl('buttonText', new FormControl('test'));
       component.splashFormGroup.addControl('termsAndConditionLink', new FormControl('test'));
       component.splashFormGroup.addControl('termsAndConditionHyperLinkText', new FormControl('test'));
       tick();
      component.ngOnInit();
      expect(component.createFormGorup).toHaveBeenCalled();
      expect(component.loadSplashData).toHaveBeenCalled();
    })
  );
  });

  describe('createFormGorup', () => {
    it('initialize the form', () => {
      component.createFormGorup();
      expect(component.splashFormGroup.get('launchBannerName')).toBeTruthy();
      expect(component.splashFormGroup.get('splashPageName')).toBeTruthy();
      expect(component.splashFormGroup.get('freeRideImg')).toBeTruthy();
      expect(component.splashFormGroup.get('welcomeMsg')).toBeTruthy();
      expect(component.splashFormGroup.get('termsAndConditionLink')).toBeTruthy();
      expect(component.splashFormGroup.get('termsAndConditionHyperLinkText')).toBeTruthy();
      expect(component.splashFormGroup.get('buttonText')).toBeTruthy();
    });

  });

  describe('loadSplashData', () => {
    it('calls getAllSplashData function', () => {
      component.createFormGorup();
      component.responseData = getAllSplashData;
      component.loadSplashData();
      expect(freeRideService.getAllSplashData).toHaveBeenCalled();
    });

  });


  describe('prepareToUploadFile', () => {
    it('should upload file on calling prepareToUploadFile', () => {
      const event = {
        'target': {
          'id': 'upload-launch-banner',
          'files': [{
            'name': 'AccaPlusBanner.png',
            'size': 38656,
            'type': 'image/png'
          }]
        }
      } as any;
      component.createFormGorup();
      component.responseData = getAllSplashData;
      component.prepareToUploadFile(event);
      expect(component.splashFormGroup.get('launchBannerName').value).toBe('AccaPlusBanner.png');
    });


    it('should throw error on incorrect file type ', () => {
      const event = {
        'target': {
          'id': 'upload-launch-banner',
          'files': [{
            'name': 'AccaPlusBanner.png',
            'size': 38656,
            'type': 'image/jpg'
          }]
        }
      } as any;
      component.createFormGorup();
      component.prepareToUploadFile(event);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: `Error. Unsupported file type.`,
        message: 'Supported \"jpeg\" and \"png\".'
      });

    });
  });


  describe('RemoveMainImage', () => {
    it('Should Remove the Uploaded file', () => {
      const event = {
        'target': {
          'classList': [`splash-image-btn`]
        }
      } as any;
      component.createFormGorup();
      component.removeMainImage(event);
      expect(component.splashImage).toBeUndefined();

    });
    it('Should Remove the Uploaded file for freeRideImg', () => {
      const event = {
        'target': {
          'classList': []
        }
      } as any;
      component.createFormGorup();
      component.removeMainImage(event);
      expect(component.splashFormGroup.get('freeRideImg').value).toMatch('');

    });
  });

  describe('constructFormData', () => {
    it('Should construct splash form data', () => {
      component.responseData = getAllSplashData;
      component.responseData.freeRideLogo = {
        'filename': '9dc6fb37-9169-4d67-8620-51c24337bf1e.png',
        'originalname': 'test-image4.png',
        'path': '/images/uploads/freeRidelogo',
        'size': 3001,
        'filetype': 'image/png'

      };
      component.responseData.freeRideLogoFileName = 'test-image4.png';
      component.constructFormData();
      expect(component.splashFormData).toBeInstanceOf(FormData);
    });
  });

  describe('disableSave', () => {
    it('should return false', () => {
      component.createFormGorup();
      component.loadSplashData();
      component.disableSave();
      expect(component.splashFormGroup.valid).toBeFalsy();

    });
    it('should return true', () => {
      component.createFormGorup();
      spyOn(component, 'loadSplashData');
      component.splashFormGroup.get('launchBannerName').setValue('test');
      component.splashFormGroup.get('splashPageName').setValue('test');
      component.splashFormGroup.get('freeRideImg').setValue('test');
      component.splashFormGroup.get('welcomeMsg').setValue('test');
      component.splashFormGroup.get('termsAndConditionLink').setValue('test');
      component.splashFormGroup.get('termsAndConditionHyperLinkText').setValue('test');
      component.splashFormGroup.get('buttonText').setValue('test');
      component.disableSave();
      expect(component.splashFormGroup.valid).toBeTruthy();
    });

  });
  describe('saveChanges', () => {
    it('should save changes using put call', () => {
      component.createFormGorup();
      component.splashFormGroup.get('launchBannerName').setValue('test');
      component.splashFormGroup.get('splashPageName').setValue('test');
      component.splashFormGroup.get('freeRideImg').setValue('test');
      component.splashFormGroup.get('welcomeMsg').setValue('test');
      component.splashFormGroup.get('termsAndConditionLink').setValue('test');
      component.splashFormGroup.get('termsAndConditionHyperLinkText').setValue('test');
      
      component.splashFormGroup.get('buttonText').setValue('test');
      component.responseData = getAllSplashData;
      component.responseData.freeRideLogo = {
        'filename': '9dc6fb37-9169-4d67-8620-51c24337bf1e.png',
        'originalname': 'test-image4.png',
        'path': '/images/uploads/freeRidelogo',
        'size': 3001,
        'filetype': 'image/png'

      };
      component.saveChanges();
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Uploaded',
        message: 'Your Data is uploaded successfully'
      });
    });
  });
});
