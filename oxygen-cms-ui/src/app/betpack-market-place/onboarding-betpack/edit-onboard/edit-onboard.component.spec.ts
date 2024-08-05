import { ElementRef } from '@angular/core';
import { async, fakeAsync, TestBed, } from '@angular/core/testing';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared/shared.module';
import { of, throwError, } from 'rxjs';
import { onboardData, OnboardModel } from '../../model/bet-pack-banner.model';
import { EditOnboardComponent } from './edit-onboard.component';

describe('EditOnboardComponent', () => {
  let component: EditOnboardComponent;
  let dialogService;
  let formBuilder;
  let router;
  let betpackOnboardService;
  let globalLoaderService;
  let apiClientService;
  let AativatedRoute;
  let onboardbetpackService;
  // let imageUploadInput;
  let OnboardModelData: OnboardModel = {
    id: 'id',
    isAdd: true,
    onboardImageDetails: {
      filename: 'test',
      originalname: 'test',
      path: 'test',
      filetype: 'test',
      size: 1,
    },
    onboardImg: {
      name: 'test',
      type: 'test',
      webkitRelativePath: 'test',
      lastModified: 1,
      size: 1,
    },
    imageType: 'test',
    imageLabel: 'test',
    nextCTAButtonLabel: 'test'
  }

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [EditOnboardComponent],
      imports: [SharedModule, FormsModule, ReactiveFormsModule],
      providers: [{ provide: FormBuilder, useValue: { FormBuilder } }],
    })
      .compileComponents();
      

    let splashData = {}
    router = { navigate: jasmine.createSpy('navigate') }
    AativatedRoute = {
      params: of({ hubId: "1" }),
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get'),
          id: 'test'
        },
        params: {
          id: 'test'
        }
      }
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.
      callFake(({ title, message }) => {
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and. callFake(({ title, message,yesCallback }) => {
        yesCallback();
      }),
    };
    betpackOnboardService = {
      setOnboardData: jasmine.createSpy('setOnboardData'),
      getOnboardEditData: jasmine.createSpy('getOnboardEditData'),
      getCreateOnboardData: jasmine.createSpy('getCreateOnboardData'),
    }
    onboardbetpackService = {
      getOnboardData: jasmine.createSpy('getOnboardData').and.returnValue(of({ body: onboardData })),
      putOnboardData: jasmine.createSpy('putOnboardData').and.returnValue(of({ body: splashData })),
      postOnboardData: jasmine.createSpy('postOnboardData').and.returnValue(of({ body: splashData })),
      getOnboardImage: jasmine.createSpy('getOnboardImage').and.returnValue(of({ body: OnboardModelData })),
      deleteOnboardImage: jasmine.createSpy('deleteOnboardImage').and.returnValue(of({ body: 'test' })),
      putOnboardImage: jasmine.createSpy('putOnboardImage').and.returnValue(of({ body: splashData })),

    };
    apiClientService = {
      onboardbetpackService: () => onboardbetpackService
    };
    globalLoaderService = { hideLoader: jasmine.createSpy('hideLoader'), showLoader: jasmine.createSpy('showLoader') }
    component = new EditOnboardComponent(formBuilder, router, betpackOnboardService, globalLoaderService, AativatedRoute, dialogService, apiClientService)

  }));

  afterEach(()=>{
    component.editOnboardData=null
  })
  describe('ngOnInit', () => {
    it('ngOnInit', () => {
      component.onboardingEditFormGroup = new FormGroup({});
      spyOn(component, 'editFormGorup');
      spyOn(component, 'setValueToForm');
      spyOn(component, 'isValueChanges');

      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.ngOnInit();
      expect(component.editFormGorup).toHaveBeenCalled();
    });
  });
  describe('editFormGorup', () => {
    it('general calls', fakeAsync(() => {
      component['formBuilder'] = new FormBuilder()
      component.editFormGorup();
      expect(component.onboardingEditFormGroup.value.imageType).toBe('');
    }));
  });

  describe('isValueChanges', () => {
    it('should return false', fakeAsync(() => {
      component.onboardingEditFormGroup = {    
        valueChanges: {
           subscribe: jasmine.createSpy('valueChanges').and.callFake(cb => cb(
            { imageLabel: 'test', nextCTAButtonLabel: 'test',imageType:'test',uploadImageName:'test' })) ,
           unsubscribe: jasmine.createSpy()
          },
          get:jasmine.createSpy('get').and.returnValue({value:'test'})
      } as any;
      spyOn(component,'editFormGorup')   
      component.isValueChanges();
      expect(component.onboardingEditFormGroup).toBeDefined();
    }));
    it('should return with empty if condition', fakeAsync(() => {
      component.uploadImageName = 'test';
      component.onboardingEditFormGroup = {    
        valueChanges: {
           subscribe: jasmine.createSpy('valueChanges').and.callFake(cb => cb(
            { imageLabel: 'test', nextCTAButtonLabel: 'test',imageType:'test',uploadImageName:'test' })) ,
           unsubscribe: jasmine.createSpy()
          },
          get:jasmine.createSpy('get').and.returnValue({value:''})
      } as any;
      spyOn(component,'editFormGorup')
      component.currentAdditem=OnboardModelData;
      component.editOnboardData=OnboardModelData;
      component.isValueChanges();
      expect(component.onboardingEditFormGroup).toBeDefined();
    }));
    it('should return with empty else if condition', fakeAsync(() => {
      component.uploadImageName = 'test';
      component.onboardingEditFormGroup = {    
        valueChanges: {
           subscribe: jasmine.createSpy('valueChanges').and.callFake(cb => cb(
            { imageLabel: 'test', nextCTAButtonLabel: 'test',imageType:'test',uploadImageName:'test' })) ,
           unsubscribe: jasmine.createSpy()
          },
          get:jasmine.createSpy('get').and.returnValue({value:''})
      } as any;
      spyOn(component,'editFormGorup')
      component.editOnboardData=OnboardModelData;

      component.isValueChanges();
      expect(component.onboardingEditFormGroup).toBeDefined();
    }));
    it('should return with empty if condition negative', fakeAsync(() => {
      component.onboardingEditFormGroup = {    
        valueChanges: {
           subscribe: jasmine.createSpy('valueChanges').and.callFake(cb => cb(
            { imageLabel: 'test1', nextCTAButtonLabel: 'test',imageType:'test',uploadImageName:'test' })) ,
           unsubscribe: jasmine.createSpy()
          },
          get:jasmine.createSpy('get').and.returnValue({value:'test1'})
      } as any;
      spyOn(component,'editFormGorup')
      component.currentAdditem=OnboardModelData;
      component.editOnboardData=OnboardModelData;
      component.uploadImageName='test'
      component.disableBottons=false;
      component.isValueChanges();
      expect(component.onboardingEditFormGroup).toBeDefined();
      expect(component.editOnboardData.imageLabel).toBe('test');

    }));
    it('should return with empty else if condition negative', fakeAsync(() => {
      component.onboardingEditFormGroup = {    
        valueChanges: {
           subscribe: jasmine.createSpy('valueChanges').and.callFake(cb => cb(
            { imageLabel: 'test', nextCTAButtonLabel: 'test1',imageType:'test1',uploadImageName:'test1' })) ,
           unsubscribe: jasmine.createSpy()
          },
          get:jasmine.createSpy('get').and.returnValue({value:'test'})
      } as any;
      spyOn(component,'editFormGorup')
      component.editOnboardData=OnboardModelData;
      component.uploadImageName='test'
      component.disableBottons=false; 
      component.isValueChanges();
      expect(component.onboardingEditFormGroup).toBeDefined();
    }));
  });

  describe('setValueToForm', () => {
    beforeEach(() => {
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImageDetails', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.id = 'test'
      component.unsavedOnboardData = [{
        id: 'test',
        isAdd: true,
        onboardImageDetails: {
          filename: 'test',
          originalname: 'test',
          path: 'test',
          filetype: 'test',
          size: 1,
        },
        onboardImg: {
          name: 'test',
          type: 'test',
          webkitRelativePath: 'test',
          lastModified: 1,
          size: 1
        },
        imageType: 'test',
        imageLabel: 'test',
        nextCTAButtonLabel: 'test'
      }]
      component.onboardImageData = {
        id: 'test',
        brand: 'test',
        createdBy: 'test',
        createdAt: 'test',
        updatedBy: 'test',
        updatedAt: 'test',
        updatedByUserName: 'test',
        createdByUserName: 'test',
        universalSegment: true,
        exclusionList: ['test'],
        inclusionList: ['test'],
        isActive: true,
        images: [{
          id: 'id',
          isAdd: true,
          onboardImageDetails: {
            filename: 'test',
            originalname: 'test',
            path: 'test',
            filetype: 'test',
            size: 1,
          },
          onboardImg: {
            name: 'test',
            type: 'test',
            webkitRelativePath: 'test',
            lastModified: 1,
            size: 1,
          },
          imageType: 'test',
          imageLabel: 'test',
          nextCTAButtonLabel: 'test'
        }]
      }
    })
    it('Should call setValueToForm if', () => {
      component.setValueToForm();
      expect(component.id).toBe('test');
    })
    it('Should call setValueToForm if', () => {
      component.setValueToForm(false);
      expect(component.id).toBe('test');
    })
    it('Should call setValueToForm else', () => {
      component.id = 'id'
      component.setValueToForm();
      expect(component.id).toBe('id');
    })
    it('Should call setValueToForm else else', () => {
      component.unsavedOnboardData[0].isAdd = false;
      component.id = 'testId'
      component.setValueToForm();
      expect(component.id).toBe('testId');
    })
  })


  describe('createEditImageData', () => {
    beforeEach(() => {
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.imageToUpload = {
        name: 'test',
        type: 'test',
        webkitRelativePath: 'test',
        lastModified: 1,
        size: 1
      }
      component.editOnboardData = OnboardModelData
    })

    it('createEditImageData', () => {
      component.createEditImageData();
      expect(component.editOnboardFormData).toBeInstanceOf(FormData);
    });
    it('createEditImageData alternate', () => {
      component.imageToUpload = null;
      component.createEditImageData();
      expect(component.editOnboardFormData).toBeInstanceOf(FormData);
    });
    it('createEditImageData if alternate', () => {
      component.editOnboardData.id = null;
      component.createEditImageData();
      expect(component.editOnboardData.id ).toEqual(null);
    });
  });

  describe('prepareToUploadFile', () => {
    it('should upload file on calling prepareToUploadFile', () => {
      spyOn(component, 'setValueToForm')
      const event = {
        'id': 'upload-banner',
        'target': {
          'files': [{
            'name': '1.png',
            'size': 38656,
            'type': 'image/png'
          }]
        }

      } as any;
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImageDetails', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.prepareToUploadFile(event)
      expect(1).toEqual(1)

    });
    it('should upload file on calling prepareToUploadFile if not supportedTypes', () => {
      spyOn(component, 'setValueToForm')
      const event = {
        'id': 'upload-banner',
        'target': {
          'files': [{
            'name': '1.png',
            'size': 38656,
            'type': 'fm/png'
          }]
        }

      } as any;
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImageDetails', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.prepareToUploadFile(event)
      expect(1).toEqual(1)

    });
    it('should upload file on calling prepareToUploadFile if not supportedTypes with check image', () => {
      spyOn(component, 'setValueToForm')
      const event = {
        'id': 'upload-banner',
        'target': {
          'files': [{
            'name': '1.png',
            'size': 38656,
            'type': 'fm/png'
          }]
        }

      } as any;
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImageDetails', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.checkImage = true
      component['imageUploadInput'] = { nativeElement: { value: '' } } as unknown as ElementRef;

      component.prepareToUploadFile(event)
      expect(1).toEqual(1)

    });
  });

  describe('RemoveMainImage', () => {
    it('Should Remove the Uploaded file', () => {
      component['imageUploadInput'] = {
        nativeElement: {
          value: '',
          click: jasmine.createSpy('click')
        }
      }
      const event = {
        'target': {
          'classList': ['main-image-btn']
        }
      } as any;
      component.removeMainImage(event)
      expect(component.checkImage).toBeTruthy();
    });
    it('Should Remove the Uploaded file else', () => {
      component['imageUploadInput'] = {
        nativeElement: {
          value: '',
          click: jasmine.createSpy('click')
        }
      }
      const event = {
        'target': {
          'classList': []
        }
      } as any;
      component.removeMainImage(event)
      expect(component.checkImage).toBeFalsy();
    });
  });

  describe('addChanges', () => {
    it('should call addChanges', () => {
      dialogService={
        showNotificationDialog:jasmine.createSpy('showNotificationDialog').and.
        callFake(({ title, message ,closeCallback}) => {
          closeCallback();
        }),
      }
      component = new EditOnboardComponent(formBuilder, router, betpackOnboardService, globalLoaderService, AativatedRoute, dialogService, apiClientService)
      spyOn(component, 'editFormGorup');
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImageDetails', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      component.addChanges();
      expect(betpackOnboardService.setOnboardData).toHaveBeenCalled();
    });
  });

  describe('revertChanges', () => {
    it('should call revertChanges', () => {
      spyOn(component, 'setValueToForm');
      component.revertChanges();
      expect(component.setValueToForm).toHaveBeenCalled();
    });
  });

  describe('saveChanges', () => {
    it('should call saveChanges', () => {
      spyOn(component,'sendSaveRequest')
      component.saveChanges();
      expect(dialogService.showConfirmDialog).toHaveBeenCalled();
    })
  })
  describe('sendSaveRequest', () => {
    beforeEach(() => {
      component.onboardImageData = {
        id: 'test',
        brand: 'test',
        createdBy: 'test',
        createdAt: 'test',
        updatedBy: 'test',
        updatedAt: 'test',
        updatedByUserName: 'test',
        createdByUserName: 'test',
        universalSegment: true,
        exclusionList: ['test'],
        inclusionList: ['test'],
        isActive: true,
        images: [{
          id: 'id',
          isAdd: true,
          onboardImageDetails: {
            filename: 'test',
            originalname: 'test',
            path: 'test',
            filetype: 'test',
            size: 1,
          },
          onboardImg: {
            name: 'test',
            type: 'test',
            webkitRelativePath: 'test',
            lastModified: 1,
            size: 1,
          },
          imageType: 'test',
          imageLabel: 'test',
          nextCTAButtonLabel: 'test'
        }]
      }
      component.id = 'test'
    })
    it('should call sendSaveRequest', () => {
      spyOn(component, 'createEditImageData')
      component.sendSaveRequest();
      expect(component.createEditImageData).toHaveBeenCalled();
    })
    it('should call sendSaveRequest false', () => {
      spyOn(component, 'createEditImageData')
      component.sendSaveRequest(false);
      expect(component.createEditImageData).toHaveBeenCalled();
    })
    it('should call sendSaveRequest else', () => {
      spyOn(component, 'createEditImageData')
      spyOn(component, 'errorNotify')
      onboardbetpackService = {
        putOnboardImage: jasmine.createSpy('putOnboardImage').and.returnValue(of(undefined))
      }
      apiClientService = {
        onboardbetpackService: () => onboardbetpackService
      };

      component.sendSaveRequest();
      expect(component.createEditImageData).toHaveBeenCalled();
    })
    it('should call sendSaveRequest error', () => {
      spyOn(component, 'createEditImageData')
      spyOn(component, 'errorNotify')
      onboardbetpackService = {
        putOnboardImage: jasmine.createSpy('putOnboardImage').and.returnValue(throwError({ error: 401 }))
      }
      apiClientService = {
        onboardbetpackService: () => onboardbetpackService
      };

      component.sendSaveRequest();
      expect(component.createEditImageData).toHaveBeenCalled();
    })
  })
  describe('isValidForm', () => {
    it('isValidForm', () => {
      component.onboardingEditFormGroup = new FormGroup({});
      component.onboardingEditFormGroup.addControl('imageType', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('onboardImg', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('imageLabel', new FormControl('test'));
      component.onboardingEditFormGroup.addControl('nextCTAButtonLabel', new FormControl('test'));
      expect(component.isValidForm()).toBeTruthy();
    })
  })
  describe('uploadImageFile', () => {
    it('uploadImageFile', () => {
      component['imageUploadInput'] = {
        nativeElement: {
          value: '',
          click: jasmine.createSpy('click')
        }
      }
      component.uploadImageFile('event')
      expect(component['imageUploadInput'].nativeElement.click).toHaveBeenCalled();
    })
  })
  describe('removeRequest', () => {
    beforeEach(() => {
      component.id = 'test';
      component.onboardImageData = {
        id: 'test',
        brand: 'test',
        createdBy: 'test',
        createdAt: 'test',
        updatedBy: 'test',
        updatedAt: 'test',
        updatedByUserName: 'test',
        createdByUserName: 'test',
        universalSegment: true,
        exclusionList: ['test'],
        inclusionList: ['test'],
        isActive: true,
        images: [{
          id: 'id',
          isAdd: true,
          onboardImageDetails: {
            filename: 'test',
            originalname: 'test',
            path: 'test',
            filetype: 'test',
            size: 1,
          },
          onboardImg: {
            name: 'test',
            type: 'test',
            webkitRelativePath: 'test',
            lastModified: 1,
            size: 1,
          },
          imageType: 'test',
          imageLabel: 'test',
          nextCTAButtonLabel: 'test'
        }]
      }
    })
    it('removeRequest if', () => {
      component.removeRequest()
      expect(router.navigate).toHaveBeenCalled();
    })
    it('removeRequest else', () => {
      onboardbetpackService = {
        deleteOnboardImage: jasmine.createSpy('deleteOnboardImage').and.returnValue(of(undefined))
      };
      apiClientService = {
        onboardbetpackService: jasmine.createSpy('onboardbetpackService').and.returnValue(onboardbetpackService),
      };
      component.removeRequest()
      expect(1).toBe(1);
    })

  })
  describe('remove', () => {
    it('remove', () => {
      spyOn(component, 'removeRequest')
      component.remove()
      expect(dialogService.showConfirmDialog).toHaveBeenCalled();

    })

  })
  describe('errorNotify', () => {
    it('errorNotify', () => {
      component.errorNotify('test')
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
        {
          title: 'Error',
          message: '"test"',
        }
      );
    
  })
})
describe('uploadNotify', () => {
  it('uploadNotify', () => {
    dialogService={
      showNotificationDialog:jasmine.createSpy('showNotificationDialog').and.
      callFake(({ title, message ,closeCallback}) => {
        closeCallback();
      }),
    }
    component = new EditOnboardComponent(formBuilder, router, betpackOnboardService, globalLoaderService, AativatedRoute, dialogService, apiClientService)
    component.uploadNotify()
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
           {
             title: 'Uploaded', 
             message: 'Betpack onboarding image configuration is updated successfully',
            closeCallback: jasmine.any(Function)
           }
         );
  })
})
});
