import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { SplashPopupComponent } from '@lazy-modules/freeRide/components/splash-popup/splash-popup.component';

describe('SplashPopupComponent', () => {
  let component, deviceService, loc, windowRef, router, renderer, closeDialogSpy, freeRideService;

 let mockActiveCampaignInfo, mockSplashInfo, mockData; 

  beforeEach(() => {
    closeDialogSpy = spyOn(SplashPopupComponent.prototype['__proto__'], 'closeDialog');
    deviceService = {
      close: jasmine.createSpy('close')
    };
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('classList.add'),
            remove: jasmine.createSpy('classList.remove')
          }
        },
        querySelector: jasmine.createSpy('querySelector'),
      },
      nativeWindow: {
        location: {
          href: '/promotions'
        }
      }
    };
    loc = {
      onPopState: jasmine.createSpy('onPopState')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    renderer = {
      renderer: {
        removeClass: jasmine.createSpy()
      }
    };

    freeRideService = {
      sendGTM: jasmine.createSpy('freeRideService.sendGTM')
    } as any;
    
    component = new SplashPopupComponent(deviceService, windowRef, loc, router, freeRideService);
    component.dialog = { closeOnOutsideClick: true };
    component.freeRide = {
      initOverlay: jasmine.createSpy()
    };

    mockSplashInfo = {
      id: '61444cdf945a415d47458c05',
      brand: 'ladbrokes',
      welcomeMsg: 'welcome to splash',
      termsAndCondition: 'terms',
      buttonText: 'Lets go',
      isBetReceipt: true,
      isHomePage: false,
      splashImageUrl: '/images/uploads/freeRideSplashPage/fa6d2f07-9c0e-400b-86d0-b80030468380.png',
      bannerImageUrl: '/images/uploads/freeRideSplashPage/4e1a319d-7eef-4bf6-a80b-2539868b000a.PNG',
      freeRideLogoUrl: '/images/uploads/freeRideSplashPage/bd44e29e-4ea8-4bf6-85e3-31e6c1b6f4a2.png'
    };

    mockActiveCampaignInfo = {
      id: '614ac62e78dbc52724af3987',
      name: 'TEST_23',
      brand: 'ladbrokes',
      displayFrom: '2021-09-23T07:02:21.270Z',
      displayTo: '2021-09-23T07:02:21.270Z',
      isPotsCreated: true,
      questionnarie: {
        questions: [
          {
            questionId: 1,
            quesDescription: 'Question 1',
            options: [
              {
                optionId: 1,
                optionText: 'top player'
              },
              {
                optionId: 2,
                optionText: 'Dark player'
              },
              {
                optionId: 3,
                optionText: 'Surprise Me'
              }
            ],
            chatBoxResp: 'Great choice'
          }
        ],
        summaryMsg: 'Question is saved',
        welcomeMessage: 'welcomeMessage',
        horseSelectionMsg: 'Please select right horse'
      }
    };

    component.activeCampaignInfo = mockActiveCampaignInfo;
    component.splashInfo = mockSplashInfo;
    component.freeBetToken = '232323232';
     mockData = {
      dialogClass: 'splash-popup',
      data: {
        campaginDetails: component.campaign,
        splashInfo: component.splashInfo,
        freeBetToken: component.freeBetToken,
        //callClose : jasmine.any(Function),
        callClose : jasmine.createSpy('callClose').and.returnValue(true),
      }
    };
    component.params = mockData;
  });

  it(`should be instance of 'AbstractDialogComponent'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });

  it('should create component instance', () => {
    expect(loc.onPopState).toHaveBeenCalledWith(jasmine.any(Function));
    expect(component).toBeTruthy();
  });

  describe('open', () => {
    it('should get data', () => {

      component.params = mockData;
      const openSpy = spyOn(SplashPopupComponent.prototype['__proto__'], 'open');
      // const params = mockData;
     // AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(component.dialog.closeOnOutsideClick).toBeFalsy();
      expect(openSpy).toHaveBeenCalled();
      expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('splashPopup-modal-open');
    });
  });

  describe('toggle', () => {
    it('should toggle to false if given true', () => {
      component.toggle(true);
      expect(component.isSoundChecked).toEqual(false);
      component.toggle(false);
      expect(component.isSoundChecked).toEqual(true);
    });

    it('should toggle to true if given false', () => {
      component.toggle(false);
      expect(component.isSoundChecked).toEqual(true);
    });

    it('should toggle to true if given false', () => {
      component.toggle(false);
      expect(component.isSoundChecked).toEqual(true);
    });
  });

  describe('goToFreeRideOverlay', () => {
    it(`should close splashPopup and display freeRide overlay`, () => {
      component.campaign = {
        'questions': [
          {
            'questionId': 1,
            'quesDescription': 'q1',
            'options': [
              {
                'optionId': 1,
                'optionText': 'o1'
              },
              {
                'optionId': 2,
                'optionText': 'o2'
              },
              {
                'optionId': 3,
                'optionText': 'o2'
              }
            ],
            'chatBoxResp': 'cbr'
          }
        ],
        'summaryMsg': 'Summary',
        'welcomeMessage': 'Welcome',
        'horseSelectionMsg': 'Horse select'
      };
      component.splashInfo = {
        id: '61444cdf945a415d47458c05',
        brand: 'ladbrokes',
        welcomeMsg: 'welcome to splash',
        termsAndConditionLink: 'link',
        termsAndConditionHyperLinkText:'Please click',
        buttonText: 'Lets go',
        splashImageUrl: '/images/uploads/freeRideSplashPage/c210706c-b665-4042-8d42-6a68843643c2.png',
        bannerImageUrl: '/images/uploads/freeRideSplashPage/4633b1f8-db5b-4d0e-9007-b72ea610063f.png',
        freeRideLogoUrl: '/images/uploads/freeRideSplashPage/1333f29a-5ce8-4113-bd22-0987e06ac94b.png'
      };

      component.goToFreeRideOverlay();
      expect(closeDialogSpy).toHaveBeenCalled();
      expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('splashPopup-modal-open');
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('#freeRideOverlay');
    });
  });

  describe('closeSplashDialog', () => {
    it('should call sendGTM', () => {
      component.params = mockData;
      component.closeSplashDialog(true);
      expect(freeRideService.sendGTM).toHaveBeenCalled();
    });
  });

  describe('freeRideClose', () => {
    it('should set overLayFlag', () => {
      component.params = mockData;
      component.freeRideClose();
      expect(component.overLayFlag).toBeFalse();
    });
  });
});
