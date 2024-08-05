// import { FormControl, FormGroup } from '@angular/forms';
import { async, TestBed } from '@angular/core/testing';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared/shared.module';
import { CreateOnboardComponent } from './create-onboard.component';



describe('CreateOnboardComponent', () => {
  let component: CreateOnboardComponent;
  let dialogService;
  let formBuilder;
  let router;
  let betpackOnboardService;

  beforeEach(async(() => {
    router = { navigate: jasmine.createSpy('navigate') };
    TestBed.configureTestingModule({
      declarations: [CreateOnboardComponent],
      imports: [SharedModule, FormsModule, ReactiveFormsModule],
      providers: [
        { provide: FormBuilder, useValue: { FormBuilder } },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    formBuilder = {
      group: jasmine.createSpy('group')
    }
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
        if (closeCallback) {
          closeCallback();
        }
      })
    }
    router = { navigate: jasmine.createSpy('navigate') };
    betpackOnboardService = {
      setOnboardData: jasmine.createSpy('setOnboardData')
    }
    component = new CreateOnboardComponent(formBuilder, dialogService, router, betpackOnboardService)
  });

  describe('ngOnInit', () => {
    it('should call breadcrumbsData', () => {
      spyOn(component, 'createFormGorup');
      component.ngOnInit();
      expect(component.breadcrumbsData).toBeDefined;
      expect(component.createFormGorup).toHaveBeenCalled();
    })
  })

  describe('createFormGorup', () => {
    it('general calls', () => {
      component.createFormGorup();
      expect(formBuilder.group).toHaveBeenCalled();
    });
  });

  describe('isValidForm', () => {
    it('should return false', () => {
      spyOn(component, 'createFormGorup');
      component.onboardingFormGroup = new FormGroup({});
      component.onboardingFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.createFormGorup();
      component.isValidForm();
      expect(component.onboardingFormGroup.valid).toBeTruthy();
    });
  });


  describe('prepareToUploadFile', () => {
    it('should upload file on calling prepareToUploadFile', () => {
      const event = {
        'target': {
          'id': 'upload-banner',
          'files': [{
            'name': 'AccaPlusBanner.png',
            'size': 38656,
            'type': 'image/png'
          }]
        }
      } as any;
      component.prepareToUploadFile(event);
      expect(component.disableBottons).toBeFalsy();
    });
    it('should upload file on calling prepareToUploadFile no support file', () => {
      const event = {
        'target': {
          'id': 'upload-banner',
          'files': [{
            'name': 'AccaPlusBanner.png',
            'size': 38656,
            'type': 'image/'
          }]
        }
      } as any;
      spyOn(component, 'createFormGorup');
      component.onboardingFormGroup = new FormGroup({});
      component.onboardingFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.createFormGorup();
      component.prepareToUploadFile(event);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: `Error. Unsupported file type.`,
        message: 'Supported \"jpeg\" and \"png\".'
      });
    });
  });

  describe('uploadImageFile', () => {
    it('Should  Uploaded file', () => {
      spyOn(component, 'createFormGorup');
      const event = {
        'target': {
          'classList': []
        }
      } as any;
      component['imageUploadInput'] = {
        nativeElement: {
          click: jasmine.createSpy('click')
        }
      } as any;
      component.createFormGorup();
      component.uploadImageFile(event);
      expect(component['imageUploadInput'].nativeElement.click).toHaveBeenCalledTimes(1);
    });
  });

  describe('RemoveMainImage', () => {
    it('Should Remove the Uploaded file', () => {
      spyOn(component, 'createFormGorup');
      component['imageUploadInput'] = {
        nativeElement: {
          value: ''
        }
      } as any;
      const event = {
        'target': {
          'classList': ['main-image-btn']
        }
      } as any;
      component.createFormGorup();
      component.removeMainImage(event);
      expect(component.disableBottons).toBeTruthy()
    });
    it('Should Remove the Uploaded file', () => {
      spyOn(component, 'createFormGorup');
      component['imageUploadInput'] = {
        nativeElement: {
          value: ''
        }
      } as any;
      const event = {
        'target': {
          'classList': ['main-image-btn-not']
        }
      } as any;
      component.createFormGorup();
      component.removeMainImage(event);
      expect(component.disableBottons).toBeFalsy()
    });
  });

  describe('generateUuid', () => {
    it('should call generateUuid', () => {
      spyOn(component, 'createFormGorup');
      component.createFormGorup();
      component['generateUuid']();
    });
  });

  describe('addChanges', () => {
    it('should call addChanges', () => {
      spyOn(component, 'generateUuid' as any);
      spyOn(component, 'createFormGorup');
      component.onboardingFormGroup = new FormGroup({});
      component.onboardingFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.createFormGorup();
      component.addChanges();
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
        {
          title: 'To save onboard image', message: 'Click on save changes in landing page to save the added image',
          closeCallback: jasmine.any(Function)
        }
      );
      expect(betpackOnboardService.setOnboardData).toHaveBeenCalled();
    });
  });

  describe('revertChanges', () => {
    it('should call revertChanges', () => {
      spyOn(component, 'createFormGorup');
      component.onboardingFormGroup = new FormGroup({});
      component.onboardingFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.createFormGorup();
      component.revertChanges();
    });
  });
});
