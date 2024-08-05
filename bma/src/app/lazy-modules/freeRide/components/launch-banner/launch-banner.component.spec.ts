import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IFreeRideCampaign, ISplashPage } from '@lazy-modules/freeRide/models/free-ride';
import { LaunchBannerComponent } from '@lazy-modules/freeRide/components/launch-banner/launch-banner.component';

describe('LaunchBannerComponent', () => {
  let component: LaunchBannerComponent;
  let freeBetsService;
  let userService;
  let dialogService;
  let freeRideService;
  let pubSubService;
  let changeDetectorRef;
  let componentFactoryResolver;
  let mockActiveCampaignInfo;
  let mockSplashInfo;
  let freeRideHelperService;
  let freeRideCMSService;
  let sessionStorageService;
  const freeBetsRes: IFreebetToken = {
    tokenId: '2200000778',
    freebetTokenId: '2200000778',
    freebetOfferId: '28985',
    freebetOfferName: 'CRM-Offer-1',
    freebetOfferDesc: 'LASPRETLASPONONFRBNN',
    freebetTokenDisplayText: '',
    freebetTokenValue: '5.00',
    freebetAmountRedeemed: '0.00',
    freebetTokenRedemptionDate: '2022-03-29 06:47:43',
    freebetRedeemedAgainst: '2022-03-29 06:47:43',
    freebetTokenExpiryDate: '2022-03-29 06:47:43',
    freebetMinPriceNum: '',
    freebetMinPriceDen: '',
    freebetTokenAwardedDate: '2022-03-29 06:47:43',
    freebetTokenStartDate: '2022-03-29 06:47:43',
    freebetTokenType: 'BETBOOST',
    freebetTokenRestrictedSet: {
        level: '',
        id: ''
    },
    freebetGameName: '',
    freebetTokenStatus: '',
    currency: '',
    tokenPossibleBet: {
        name: '',
        betLevel: '',
        betType: '',
        betId: '',
        channels: ''
    },
    tokenPossibleBets: [{
        name: '',
        betLevel: '',
        betType: '',
        betId: '',
        channels: ''
    }],
    freebetOfferType: '',
    tokenPossibleBetTags: {
        'tagName': 'FRRIDE'
    }
};
  beforeEach(() => {
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
    freeRideService = {
      getFreeRide: jasmine.createSpy('freeRideService.getFreeRide'),
      sendGTM: jasmine.createSpy('freeRideService.sendGTM'),
    } as any;

    freeRideCMSService = {
      getFreeRideSplashPage: jasmine.createSpy('getFreeRideSplashPage').and.returnValue(of(mockSplashInfo)),
    } as any;

    freeBetsService = {
      isFRFreeBets: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(freeBetsRes)),
        next: jasmine.createSpy('next').and.returnValue(of(freeBetsRes))
      }
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('componentFactoryResolver.resolveComponentFactory')
    } as any;
    dialogService = {
      openDialog: jasmine.createSpy('openDialog').and.callFake((p1, p2, p3, opt) => {
        opt.data.callClose();
      })
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => {
        callback(() => {
          return true;
        });
      }),
      API: { FREE_RIDE_BET: 'FREE_RIDE_BET' },
      publish: jasmine.createSpy('publish')
    } as any;
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    sessionStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
  };

    component = new LaunchBannerComponent(
      freeBetsService,
      userService,
      componentFactoryResolver,
      dialogService,
      freeRideService,
      freeRideHelperService,
      freeRideCMSService,
      sessionStorageService,
      pubSubService,
      changeDetectorRef
    );

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
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
    expect(component.isUsed$).toBeTruthy();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('freeRideOverlay', 'FREE_RIDE_BET', jasmine.any(Function));
  });

  describe('openPopUp', () => {
    it('open dialog', () => {

      component.activeCampaignInfo = mockActiveCampaignInfo;
      component.splashInfo = mockSplashInfo;
      component.freeBetToken = '232323232';
      const data = {
        dialogClass: 'splash-popup',
        data: {
          campaginDetails: component.activeCampaignInfo,
          splashInfo: component.splashInfo,
          freeBetToken: component.freeBetToken,
           callClose : jasmine.any(Function),
        }
      };
      component.openPopUp();

      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith('splashPopup', undefined, true, data);
    });
  });

  describe('loadInitialData', () => {
    const mockSplashInfo: ISplashPage = {
      id: '61444cdf945a415d47458c05',
      brand: 'ladbrokes',
      welcomeMsg: 'welcome to splash',
      termsAndCondition: 'terms',
      buttonText: 'Lets go',
      splashImageUrl: '/images/uploads/freeRideSplashPage/fa6d2f07-9c0e-400b-86d0-b80030468380.png',
      bannerImageUrl: '/images/uploads/freeRideSplashPage/4e1a319d-7eef-4bf6-a80b-2539868b000a.PNG',
      freeRideLogoUrl: '/images/uploads/freeRideSplashPage/bd44e29e-4ea8-4bf6-85e3-31e6c1b6f4a2.png',
      isBetReceipt: true,
      isHomePage: false,
    };
    const activeCampaignDetail: IFreeRideCampaign = {
        id: '61711866f5c4a05b22fd8a0b',
        name: 'Campaign_01_dev',
        brand: 'ladbrokes',
        displayFrom: '2021-11-01T02:51:50Z',
        displayTo: '2021-11-01T17:51:50Z',
        isPotsCreated: false,
        questionnarie: {
            questions: [
                {
                    questionId: 1,
                    quesDescription: 'q1',
                    options: [
                        {
                            optionId: 1,
                            optionText: 'o1'
                        },
                        {
                            optionId: 2,
                            optionText: 'o2'
                        },
                        {
                            optionId: 3,
                            optionText: 'o2'
                        }
                    ],
                    chatBoxResp: 'cbr'
                },
                {
                    questionId: 2,
                    quesDescription: 'q2',
                    options: [
                        {
                            optionId: 4,
                            optionText: 'o1'
                        },
                        {
                            optionId: 5,
                            optionText: 'o2'
                        },
                        {
                            optionId: 6,
                            optionText: 'o3'
                        }
                    ],
                    chatBoxResp: 'cbr2'
                },
                {
                    questionId: 3,
                    quesDescription: 'q3',
                    options: [
                        {
                            optionId: 7,
                            optionText: 'o1'
                        },
                        {
                            optionId: 8,
                            optionText: 'o2'
                        },
                        {
                            optionId: 9,
                            optionText: 'o3'
                        }
                    ],
                    chatBoxResp: 'cbr3'
                }
            ],
            summaryMsg: 'Summary',
            welcomeMessage: 'Welcome',
            horseSelectionMsg: 'Horse select'
        }
    };
    it('should set launchImg if get response from getFreeRide', fakeAsync(()=> {
      sessionStorageService.get.and.returnValue(JSON.stringify(activeCampaignDetail))
      freeRideCMSService.getFreeRideSplashPage.and.returnValue(of(mockSplashInfo));
        freeRideCMSService.getFreeRideSplashPage().subscribe();
        component.loadInitialData();
        tick();
        expect(component.launchImg).toEqual('https://cms.coral.co.uk/cms//images/uploads/freeRideSplashPage/4e1a319d-7eef-4bf6-a80b-2539868b000a.PNG');
    }));
    it('should call console.warn if get error from getFreeRide', ()=> {
        spyOn(console,'warn');
        freeRideCMSService.getFreeRideSplashPage.and.returnValue(throwError('error'));
        component.loadInitialData();
        expect(console.warn).toHaveBeenCalled();
    });
  });

  describe('checkHomeBetslipConfig', () => {
    it('set sportsConfig ifconfig is  betslip ', () => {

      component.splashInfo = mockSplashInfo;
      component.checkHomeBetslipConfig('BETSLIP');

    expect(component.splashConfig).toEqual(true);
    });

    it('set sportsConfig ifconfig is  HOME ', () => {
      component.splashInfo = mockSplashInfo;
      component.checkHomeBetslipConfig('HOME');

    expect(component.splashConfig).toEqual(false);
    });

    it('set sportsConfig ifconfig default ', () => {
      component.splashInfo = mockSplashInfo;
      component.checkHomeBetslipConfig('test');

    expect(component.splashConfig).toEqual(true);
    });
  });
});
