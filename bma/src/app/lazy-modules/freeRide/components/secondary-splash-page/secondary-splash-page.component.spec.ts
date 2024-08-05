import { fakeAsync, tick } from '@angular/core/testing';
import { SecondarySplashPageComponent } from '@lazy-modules/freeRide/components/secondary-splash-page/secondary-splash-page.component';
import { of } from 'rxjs';

describe('SplashPopupComponent', () => {
  let component, deviceService, componentFactoryResolver, dialogService,
  freeRideCMSService, sessionStorageService , windowRef;

 let mockActiveCampaignInfo, mockSplashInfo, mockData; 

  beforeEach(() => {
    deviceService = {
      close: jasmine.createSpy('close')
    };
    dialogService = {
      openDialog: jasmine.createSpy('dialogService.openDialog').and.callFake((p1, p2, p3, opt) => {
        opt.data.callClose();
      })
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

    freeRideCMSService = {
        getFreeRideSplashPage: jasmine.createSpy('getFreeRideSplashPage').and.returnValue(of(mockSplashInfo)),
      } as any;

    componentFactoryResolver = {
        resolveComponentFactory: jasmine.createSpy('componentFactoryResolver.resolveComponentFactory')
      } as any;

      sessionStorageService = {
        set: jasmine.createSpy('set'),
        get: jasmine.createSpy('get')
    };

    component = new SecondarySplashPageComponent(
        deviceService, windowRef, componentFactoryResolver, dialogService,
        freeRideCMSService, sessionStorageService );

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
      freeBetTokenId: '232323232',
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
        callClose : jasmine.createSpy('callClose').and.returnValue(true),
      }
    };
    component.params = mockData;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnit', () => {
  it('should call openDialog', fakeAsync(()=> {
    const mockfreeBetDetails = sessionStorageService.get.and.returnValue(JSON.stringify(component.activeCampaignInfo))
    mockfreeBetDetails.freeBetTokenId = '232323232',
    freeRideCMSService.getFreeRideSplashPage.and.returnValue(of(mockSplashInfo));

    const data = {
      dialogClass: 'splash-popup',
      data: {
        campaginDetails: component.activeCampaignInfo,
        splashInfo: component.splashInfo,
        freeBetToken: component.freeBetToken,
         callClose : jasmine.any(Function),
      }
    };
      freeRideCMSService.getFreeRideSplashPage().subscribe();
      component.ngOnInit();

      tick();
       expect(dialogService.openDialog).toHaveBeenCalledWith(
        'splashPopup', undefined, true, data
      );
  }));
});
});
