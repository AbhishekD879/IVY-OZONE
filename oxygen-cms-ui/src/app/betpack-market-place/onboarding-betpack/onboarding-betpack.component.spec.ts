import { of, throwError } from 'rxjs';
import { BetPackModelMock, onboardFormArray, onboardFormDataModel, onboardFormDataModelNoId, onboardFormDataModelNoId1, onboardImageDataModel } from '../betpack-mock';
import { OnboardingBetpackComponent } from './onboarding-betpack.component';

describe('OnboardingBetpackComponent', () => {
  let component: OnboardingBetpackComponent;
  let betpackOnboardService;
  let dialogService;
  let apiClientService;
  let globalLoaderService;
  let snackBar;
  let brandService;

  beforeEach(() => {
    betpackOnboardService = {
      putOnboardData: jasmine.createSpy('putOnboardData').and.returnValue(of({ body: onboardImageDataModel })),
      postOnboardData: jasmine.createSpy('putOnboardData').and.returnValue(of({ body: '1' })),
      getOnboardData: jasmine.createSpy('getOnboardData').and.returnValue(of({ body: onboardImageDataModel })),
      deleteOnboardImage: jasmine.createSpy('deleteOnboardImage').and.returnValue(of({})),
      setCreateOnboardData: jasmine.createSpy('setCreateOnboardData').and.returnValue(of({})),
      sendEditRequest: jasmine.createSpy('sendEditRequest').and.returnValue(of({ body: BetPackModelMock })),
      setUpdateOnboardData: jasmine.createSpy('setUpdateOnboardData'),
      setEmpty: jasmine.createSpy('setEmpty').and.returnValue(of({ body: BetPackModelMock })),
    };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
        yesCallback();
      }),
      showNotificationDialog: jasmine.createSpy('showConfirmDialog')
    };
    snackBar = {
      open: jasmine.createSpy('open'),
    }
    console.log('betpackOnboardService', betpackOnboardService)
    apiClientService = {
      onboardbetpackService: () => betpackOnboardService
    };
    globalLoaderService = {
      hideLoader: jasmine.createSpy('hideLoader'),
      showLoader: jasmine.createSpy('showLoader')
    }
    brandService = {
      brand: 'bma'
    };
    // router = { navigate: jasmine.createSpy('navigate') };
    // activatedRoute = {
    //     params: of({ id: '1' })
    // };
    component = new OnboardingBetpackComponent(betpackOnboardService, dialogService, apiClientService, globalLoaderService, snackBar, brandService);
  });
  afterEach(()=>{
    component=undefined

  })
  describe('ngOnInit', () => {
    it('ngOnInit', () => {
      spyOn(component as any, 'loadIntialData');
      component.ngOnInit();
      expect(component.loadIntialData).toHaveBeenCalled()
    })
  })
  describe('loadIntialData', () => {
    it('loadIntialData when res and loading true', () => {
      component.newOnboardData = [{ id: '1' }] as any;
      spyOn(component as any, 'showHideSpinner');
      component['loadIntialData']();
      expect(component['showHideSpinner']).toHaveBeenCalled();
    });
    it('#loadIntialData when no res and loading true', () => {
      spyOn(component as any, 'showHideSpinner');
      betpackOnboardService = {
        getOnboardData: jasmine.createSpy('getOnboardData').and.returnValue(of({})),
      };
      component.newOnboardData = [{ id: '1' }] as any;
      component['loadIntialData']();
      expect(component['showHideSpinner']).toHaveBeenCalled();
    })
    it('#loadIntialData should call isLoading, false case', () => {
      component.newOnboardData = [{ id: '1' }] as any;
      component['loadIntialData'](false);
    });
    it('#loadIntialData error', () => {
      spyOn(component as any, 'showHideSpinner');
      spyOn(component as any, 'errorNotify');
      betpackOnboardService = {
        getOnboardData: jasmine.createSpy('getOnboardData').and.returnValue(throwError({ error: 401 })),
      };
      component['loadIntialData']();
      expect(component.errorNotify).toHaveBeenCalled();
    })
  })
  describe('showHideSpinner', () => {
    it('showLoader', () => {
      component['showHideSpinner']();
      expect(globalLoaderService.showLoader).toHaveBeenCalled()
    })
    it('hideLoader', () => {
      component['showHideSpinner'](false);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled()
    })
  })
  describe('uploadNotify', () => {
    it('uploadNotify', () => {
      component.uploadNotify();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled()
    })
  })
  describe('errorNotify', () => {
    it('errorNotify', () => {
      component.errorNotify('error');
      expect(dialogService.showNotificationDialog).toHaveBeenCalled()
    })
  })
  describe('constructFormData', () => {
    it('constructFormData when onboardImageData if', () => {
      component.disabled = true;
      component.onboardData = onboardFormArray as any;
      component.onboardImageData = {
        id: "sdf",
        isActive: true,
        images:[],
        brand: '',
        createdBy: '',
        createdAt: '',
        updatedBy: '',
        updatedAt: '',
        updatedByUserName: '',
        createdByUserName: ''

      }
      let retVal = component.constructFormData();
      expect(retVal).toBeInstanceOf(FormData);
    })
    it('constructFormData when onboardImageData else', () => {
      component.disabled = true;
      component.onboardData = onboardFormArray as any;
      let retVal = component.constructFormData();
      expect(retVal).toBeInstanceOf(FormData);
    })
  })
  describe('removeOnboardBetPack', () => {
    it('removeOnboardBetPack', () => {
      spyOn(component as any, 'removeImageRequest');
      let event = onboardFormDataModel as any;
      component.removeOnboardBetPack(event);
      expect(dialogService.showConfirmDialog).toHaveBeenCalled()
    });
  })
  describe('removeImageRequest', () => {
    it('removeImageRequest when true', () => {
      spyOn(component as any, 'showHideSpinner');
      spyOn(component as any, 'loadIntialData');
      spyOn(component as any, 'isValid');
      component.onboardData = onboardFormArray;
      component.newOnboardData = [{ id: '1' }] as any;
      component.onboardImageData = {
        id: '1'
      } as any;
      component.removeImageRequest(onboardFormDataModel);
      expect(snackBar.open).toHaveBeenCalled();
      component.removeImageRequest(onboardFormDataModelNoId);
      expect(component.isValid).toHaveBeenCalled();
    });
    it('removeImageRequest when false', () => {
      spyOn(component as any, 'showHideSpinner');
      spyOn(component as any, 'loadIntialData');
      spyOn(component as any, 'isValid');
      component.onboardData = onboardFormArray;
      component.newOnboardData = [{ id: '1' }] as any;
      component.onboardImageData = {
        id: '1'
      } as any;
      component.removeImageRequest(onboardFormDataModelNoId1);
      expect(component.isValid).toHaveBeenCalled();
    });
  })
  describe('activeStatus', () => {
    it('activeStatus', () => {
      spyOn(component as any, 'isValid');
      component.disabled = true;
      component.activeStatus();
      expect(component.isValid).toHaveBeenCalled()
    })
  })
  describe('isValid', () => {
    it('isValid when onboard data', () => {
      betpackOnboardService.getOnboardData.and.returnValue(onboardFormArray);
      component.onboardData = onboardFormArray as any;
      component.disabled = true;
      component.onboardImageData = {
        id: '1',
        isActive: true
      } as any;
      component.isValid();
      expect(component.buttonDisabled).toBeFalsy();
    })
    it('isValid when no onboard data1', () => {
      component.onboardData = {} as any;
      component.disabled = true;
      component.onboardImageData = {
        id: '1',
        isActive: true
      } as any;
      component.isValid();
      expect(component.buttonDisabled).toBeTruthy();
    })
    it('isValid when no onboard data2', () => {
      component.onboardData = {} as any;
      component.disabled = true;
      component.onboardImageData = {
        id: '1',
        isActive: false
      } as any;
      component.isValid();
      expect(component.buttonDisabled).toBeFalsy();
    })
    it('isValid when no onboard data no imagedata', () => {
      component.onboardData = []
      component.disabled = true;
      betpackOnboardService.getOnboardData.and.returnValue([]);
      component.onboardImageData = {
        id: '1',
        isActive: true
      } as any;
      component.isValid();
      expect(component.buttonDisabled).toBeTruthy();
    })
  })
  describe('reorderHandler', () => {
    it('reorderHandler when length', () => {
      spyOn(component as any, 'saveChanges');
      component.onboardData = onboardFormArray as any;
      component.onboardImageData = {
        images: ['1'],
        isActive: true
      } as any;
      component.reorderHandler({ id: '1' } as any);
      expect(component.saveChanges).toHaveBeenCalled();
    })
    it('reorderHandler when no length', () => {
      spyOn(component as any, 'saveChanges');
      component.onboardData = onboardFormArray as any;
      component.onboardImageData = {
        images: [],
        isActive: true
      } as any;
      component.reorderHandler({ id: '1' } as any);
      expect(betpackOnboardService.setUpdateOnboardData).toHaveBeenCalled();
    })
  })
  describe('setEmpty', () => {
    it('setEmpty', () => {
      component.setEmpty();
      expect(betpackOnboardService.setEmpty).toHaveBeenCalled()
    })
  })
  describe('saveChanges', () => {
    it('saveChanges when reorderImage', () => {
      spyOn(component as any, 'sendSaveRequest');
      component.reorderImage = true;
      component.saveChanges();
      expect(component.sendSaveRequest).toHaveBeenCalled();
    })
    it('saveChanges when reorderImage false', () => {
      spyOn(component as any, 'sendSaveRequest');
      component.reorderImage = false;
      component.saveChanges();
      expect(dialogService.showConfirmDialog).toHaveBeenCalled();
    })
  })
  describe('sendSaveRequest', () => {
    it('sendSaveRequest when reorderImage', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'setEmpty');
      spyOn(component as any, 'loadIntialData');
      spyOn(component as any, 'uploadNotify');
      spyOn(component as any, 'showHideSpinner');
      component.onboardImageData = {
        id: '1'
      } as any;
      component.reorderImage = false;
      component.sendSaveRequest();
      expect(component['showHideSpinner']).toHaveBeenCalled();
    })
    it('sendSaveRequest when reorderImage when onboardImagedata and false', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'setEmpty');
      spyOn(component as any, 'loadIntialData');
      spyOn(component as any, 'showHideSpinner');
      component.onboardImageData = {
        id: '1'
      } as any;
      component.reorderImage = true;
      component.sendSaveRequest();
      expect(snackBar.open).toHaveBeenCalled();
    })
    it('sendSaveRequest when reorderImage when onboardImagedata and noresp', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'loadIntialData');
      betpackOnboardService = {
        putOnboardData: jasmine.createSpy('putOnboardData').and.returnValue(of({}))
      };
      component.onboardImageData = {
        id: '1'
      } as any;
      component.reorderImage = true;
      component.sendSaveRequest();
      expect(component.loadIntialData).not.toHaveBeenCalled();
    })
    it('sendSaveRequest when error', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'errorNotify');
      spyOn(component as any, 'showHideSpinner');
      betpackOnboardService = {
        putOnboardData: jasmine.createSpy('putOnboardData').and.returnValue(throwError({ error: 401 }))
      };
      component.onboardImageData = {
        id: '1'
      } as any;
      component.reorderImage = true;
      component.sendSaveRequest();
      expect(component.errorNotify).toHaveBeenCalled();
    })
    it('sendSaveRequest when reorderImage when null and false', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'setEmpty');
      spyOn(component as any, 'uploadNotify');
      spyOn(component as any, 'loadIntialData');
      spyOn(component as any, 'showHideSpinner');
      component.onboardImageData = null;
      component.reorderImage = false;
      component.sendSaveRequest();
      expect(component['showHideSpinner']).toHaveBeenCalled();
    })
    it('sendSaveRequest when reorderImage when null and true', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'setEmpty');
      spyOn(component as any, 'loadIntialData');
      spyOn(component as any, 'showHideSpinner');
      component.onboardImageData = null;
      component.reorderImage = true;
      component.sendSaveRequest();
      expect(snackBar.open).toHaveBeenCalled();
    })
    it('sendSaveRequest when reorderImage when null and noresp', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'setEmpty');
      betpackOnboardService = {
        postOnboardData: jasmine.createSpy('postOnboardData').and.returnValue(of(undefined))
      };
      component.onboardImageData = null;
      component.reorderImage = true;
      component.sendSaveRequest();
      expect(component.setEmpty).not.toHaveBeenCalled();
    })
    it('sendSaveRequest when error', () => {
      spyOn(component as any, 'constructFormData');
      spyOn(component as any, 'errorNotify');
      spyOn(component as any, 'showHideSpinner');
      betpackOnboardService = {
        postOnboardData: jasmine.createSpy('postOnboardData').and.returnValue(throwError({ error: 401 }))
      };
      component.onboardImageData = null;
      component.reorderImage = true;
      component.sendSaveRequest();
      expect(component.errorNotify).toHaveBeenCalled();
    })
    it('#sendSaveRequest should call isLoading, false case', () => {
      component.onboardImageData = {
        id: '1'
      } as any;
      component.onboardData = onboardFormArray as any;
      component['sendSaveRequest'](false);
    });
  })
});



