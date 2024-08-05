import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from "rxjs";
import { LuckyDipComponent } from './lucky-dip.component';

describe('LuckyDipComponent', () => {
  let component: LuckyDipComponent;

  let dialogService;
  let brandService;
  let apiClientService;

  let mockLuckyDipData =
  {
    id: ' 63ecd2a079768e6cf926a83b',
    luckyDipBannerConfig: {
      animationImgPath: 'https:/animation.com',
      bannerImgPath: 'https:/ banner.com',
      infoIconImgPath: 'https:/ info.com'
    },
    luckyDipFieldsConfig: {
      title: 'Lucky DIp test 1',
      desc: 'Here u can play',
      welcomeMessage: 'Welcome to COntest',
      betPlacementTitle: 'First title',
      betPlacementStep1: 'Step 1',
      betPlacementStep2: 'Step 2',
      betPlacementStep3: 'Step 3',
      termsAndConditionsURL: 'http:/ url.com',
      playerCardDesc: 'Player 1',
      potentialReturnsDesc: 'Win Money'
    }, playerPageBoxImgPath: ' https: /path1.com'
  }

  let mockLuckyDip = {
    id: '123',
    brand: 'ladbrokes',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    luckyDipBannerConfig: {
      animationImgPath: '',
      bannerImgPath: '',
      overlayBannerImgPath: ''
    },
    luckyDipFieldsConfig: {
      title: '',
      desc: '',
      welcomeMessage: '',
      betPlacementTitle: '',
      betPlacementStep1: '',
      betPlacementStep2: '',
      betPlacementStep3: '',
      termsAndConditionsURL: '',
      playerCardDesc: '',
      potentialReturnsDesc: '',
      placebetCTAButton: '',
      backCTAButton: '',
      gotItCTAButton: '',
      depositButton: ''
    },
    playerPageBoxImgPath: '',
  };

  beforeEach(() => {
    dialogService = { showNotificationDialog: jasmine.createSpy('showNotificationDialog') };

    brandService = {};

    apiClientService = {
      luckyDipService: jasmine.createSpy('luckyDipService').and.returnValue({
        getLuckyDipData: jasmine.createSpy('getLuckyDipData').and.returnValue(of({ body: [] })),
        luckyDipData: jasmine.createSpy('luckyDipData').and.returnValue(of({ body: [] })),
      })
    };


    component = new LuckyDipComponent(
      dialogService, brandService, apiClientService
    );
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(apiClientService.luckyDipService().getLuckyDipData).toHaveBeenCalled();
  });

  describe('loadInitialData', () => {
    it('If getting data from id', fakeAsync(() => {
      mockLuckyDipData.id = ' 63ecd2a079768e6cf926a83b';
      apiClientService.luckyDipService().getLuckyDipData.and.returnValue(of(mockLuckyDipData));
      component.loadInitialData();
      tick();
      tick();
      expect(apiClientService.luckyDipService().getLuckyDipData).toHaveBeenCalled();
      expect(component.luckyDip).toBeDefined();
    }));

    it('If getting data from id and tEditor is true', fakeAsync(() => {
      component.tEditor = {
        update: jasmine.createSpy('update')
      } as any;
      mockLuckyDipData.id = ' 63ecd2a079768e6cf926a83b';
      apiClientService.luckyDipService().getLuckyDipData.and.returnValue(of(mockLuckyDipData));
      component.loadInitialData();
      tick();
      tick();
      expect(apiClientService.luckyDipService().getLuckyDipData).toHaveBeenCalled();
      expect(component.luckyDip).toBeDefined();
    }));

    it('If getting data from id and descEditor is true', fakeAsync(() => {
      component.descEditor = {
        update: jasmine.createSpy('update')
      } as any;
      mockLuckyDipData.id = ' 63ecd2a079768e6cf926a83b';
      apiClientService.luckyDipService().getLuckyDipData.and.returnValue(of(mockLuckyDipData));
      component.loadInitialData();
      tick();
      tick();
      expect(apiClientService.luckyDipService().getLuckyDipData).toHaveBeenCalled();
      expect(component.luckyDip).toBeDefined();
    }));

    it('If getting data from id and titleEditor is true', fakeAsync(() => {
      component.titleEditor = {
        update: jasmine.createSpy('update')
      } as any;
      mockLuckyDipData.id = ' 63ecd2a079768e6cf926a83b';
      apiClientService.luckyDipService().getLuckyDipData.and.returnValue(of(mockLuckyDipData));
      component.loadInitialData();
      tick();
      tick();
      expect(apiClientService.luckyDipService().getLuckyDipData).toHaveBeenCalled();
      expect(component.luckyDip).toBeDefined();
    }));

    it('If not getting data from id', fakeAsync(() => {
      mockLuckyDipData.id = null;
      apiClientService.luckyDipService().getLuckyDipData.and.returnValue(of({}));

      component.loadInitialData();
      tick();
      tick();
      expect(apiClientService.luckyDipService().getLuckyDipData).toHaveBeenCalled();

    }));
  });

  describe('saveChanges', () => {
    it('Getting data from luckyDipService ', fakeAsync(() => {

      component.luckyDipForm = {
        form: {
          dirty: true,
          valid: true,
          markAsPristine: jasmine.createSpy('markAsPristine')
        }
      } as any;
      component.luckyDip.id = '123'

      apiClientService.luckyDipService().luckyDipData.and.returnValue(of({ body: mockLuckyDipData }));


      component.saveChanges();
      tick();
      tick();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    }));

    it('disableSaveBtn not to be true', fakeAsync(() => {

      component.luckyDip.id = '123'

      apiClientService.luckyDipService().luckyDipData.and.returnValue(of(null));

      component.saveChanges();
      tick();
      expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
    }));
    it('getting error from luckyDipService', fakeAsync(() => {

      component.luckyDip.id = '123'

      apiClientService.luckyDipService().luckyDipData.and.returnValue(throwError({ error: 'error' }));

      component.saveChanges();
      tick();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    }));
  });

  describe('disableSave', () => {
    it('If welcomeMessage is empty', () => {
      component.luckyDipForm = {
        form: {
          dirty: true,
          valid: true,
        }
      } as any;
      component.luckyDip.luckyDipFieldsConfig.welcomeMessage = '';
      component.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL = '';
      component.luckyDip.luckyDipFieldsConfig.playerCardDesc = '';
      component.luckyDip.luckyDipFieldsConfig.potentialReturnsDesc = '';

      component.disableSave()

      expect(component.disableSave).toBeTruthy();
    });

    it('If termsAndConditionsURL is empty', () => {
      component.luckyDipForm = {
        form: {
          dirty: true,
          valid: false,
        }
      } as any;
      component.luckyDip.luckyDipFieldsConfig.welcomeMessage = '123';
      component.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL = '';
      component.luckyDip.luckyDipFieldsConfig.playerCardDesc = '';
      component.luckyDip.luckyDipFieldsConfig.potentialReturnsDesc = '';

      component.disableSave()

      expect(component.disableSave).toBeTruthy();
    });
    it('If playerCardDesc is empty', () => {
      component.luckyDipForm = {
        form: {
          dirty: true,
          valid: true,
        }
      } as any;
      component.luckyDip.luckyDipFieldsConfig.welcomeMessage = '123';
      component.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL = '123';
      component.luckyDip.luckyDipFieldsConfig.playerCardDesc = '';
      component.luckyDip.luckyDipFieldsConfig.potentialReturnsDesc = '';

      component.disableSave()

      expect(component.disableSave).toBeTruthy();
    });
    it('If potentialReturnsDesc is empty', () => {
      component.luckyDipForm = {
        form: {
          dirty: true,
          valid: true,
        }
      } as any;
      component.luckyDip.luckyDipFieldsConfig.welcomeMessage = '123';
      component.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL = '123';
      component.luckyDip.luckyDipFieldsConfig.desc = '123';
      component.luckyDip.luckyDipFieldsConfig.title = '';

      component.disableSave()

      expect(component.disableSave).toBeTruthy();
    });
  });

  it('If luckyDipForm is not dirty', () => {
    component.luckyDipForm = {
      form: {
        dirty: false,
        valid: false,
        markAsPristine: jasmine.createSpy('markAsPristine')
      }
    } as any;

    component.luckyDip.luckyDipFieldsConfig.welcomeMessage = '';
    component.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL = '';
    component.luckyDip.luckyDipFieldsConfig.playerCardDesc = '';
    component.luckyDip.luckyDipFieldsConfig.potentialReturnsDesc = '';
    component.disableSave()

    expect(component.disableSave).toBeTruthy();
  });

  it('If luckyDipForm is not dirty but valid', () => {
    component.luckyDipForm = {
      form: {
        dirty: false,
        valid: true,
        markAsPristine: jasmine.createSpy('markAsPristine')
      }
    } as any;

    component.luckyDip.luckyDipFieldsConfig.welcomeMessage = '';
    component.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL = '';
    component.luckyDip.luckyDipFieldsConfig.playerCardDesc = '';
    component.luckyDip.luckyDipFieldsConfig.potentialReturnsDesc = '';
    component.disableSave()

    expect(component.disableSave).toBeTruthy();
  });

  it('updateLuckyDip', () => {
    const event = {
      stopPropagation: jasmine.createSpy('stopPropagation')
    };
    const val = 'luckyDipFieldsConfig.welcomeMessage'
    component.updateLuckyDip(event as any, val)

    expect(component.disableSave).toBeTruthy();
  });

  it('isEqualCollection', () => {
    component.luckyDip = mockLuckyDip;
    component.luckyDipCopy = mockLuckyDip;

    component.isEqualCollection()

    expect(component.luckyDip).toEqual(component.luckyDipCopy);
  });

});
