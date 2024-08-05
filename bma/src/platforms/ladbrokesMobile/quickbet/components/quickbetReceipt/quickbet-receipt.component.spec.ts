import { LadbrokesQuickbetReceiptComponent } from '@ladbrokesMobile/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { IQuickbetReceiptDetailsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { of } from 'rxjs';


describe('#LadbrokesQuickbetReceiptComponent', () => {
  let  component: LadbrokesQuickbetReceiptComponent,
       user,
       filtersService,
       quickbetService,
       nativeBridge,
       window,
       germanSupportService,
       storageService,
      pubSubService,
      racingPostTipService,
      http,
      cmsService,
      fiveASideEntryConfirmationService,
      fiveASideContestSelectionService,
      freeBetsService,
      gtmService,maxPayOutErrorService,
      locale,firstBetGAService,
      betReuseService,
      freeRideHelperService,sessionStorage,
      bonusSuppressionService;

  beforeEach(() => {
    user = {
      currencySymbol: '$',
      receiptViewsCounter: 0,
      winAlertsToggled: false,
      set: jasmine.createSpy()
    };

    filtersService = {
      setCurrency: jasmine.createSpy(),
      filterPlayerName: jasmine.createSpy('filterPlayerName').and.returnValue(''),
      filterAddScore: jasmine.createSpy('filterAddScore').and.returnValue('')
    };

    quickbetService = {
      getOdds: jasmine.createSpy('getOdds'),
      getEWTerms: jasmine.createSpy('getEWTerms'),
      getLinesPerStake: jasmine.createSpy('getLinesPerStake'),
      isVirtualSport: jasmine.createSpy('isVirtualSport').and.returnValue(true),
      getBybSelectionType: jasmine.createSpy('getBybSelectionType')
    };

    fiveASideEntryConfirmationService = {
      getShowdownConfirmationDisplay: jasmine.createSpy('getShowdownConfirmationDisplay'),
    };

    fiveASideContestSelectionService = {
      defaultSelection: jasmine.createSpy('defaultSelection')
    };

    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
        enabled: true,
        title: 'MaxPayOut',
        link: 'https://coral.co.uk/',
        click: 'here'
      } as any)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        maxPayOut: {
          maxPayoutFlag: true
        }
      }))
    };


    nativeBridge = {
      onActivateWinAlerts: jasmine.createSpy()
    };

    window = {
      nativeWindow: {
        pushNotificationsEnabled: true
      }
    };
    pubSubService = {};
    http = {};

    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser')
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };
    racingPostTipService = {};

    gtmService = {
      push: jasmine.createSpy()
    };

    freeBetsService = {
      store: jasmine.createSpy('store'),
      getFreeBetsState: jasmine.createSpy('getFreeBetsState').and.returnValue({
        availble: true, data: [{ freebetTokenId: 123 }, { freebetTokenId: 143 }]
      })
    };

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled'),
    };
    betReuseService = {
      reuseQuickBet: jasmine.createSpy('reuseQuickBet')
    }
    
    component = new LadbrokesQuickbetReceiptComponent(
      user,
      filtersService,
      quickbetService,
      nativeBridge,
      window,
      pubSubService,
      http,
      storageService,
      racingPostTipService,
      cmsService,
      fiveASideEntryConfirmationService,
      gtmService,
      maxPayOutErrorService,
      fiveASideContestSelectionService,
      freeBetsService,
      germanSupportService,
      freeRideHelperService,
      locale,
      firstBetGAService,
      betReuseService,
      sessionStorage,
      bonusSuppressionService
    );

    component.selection = {
      stake: '1.22'
    } as IQuickbetSelectionModel;

    component.betReceipt = {
      bet: { id: 1 },
      stake: {
        amount: '100',
        freebet: '10',
        stakePerLine: '111',
      },
      legParts: [{
        eventDesc: '',
        marketDesc: '',
        handicap: '',
        outcomeDesc: ''
      }],
      price: {
        priceType: 'test_price'
      },
      payout: { potential: '99' },
      oddsValue: '1/2'
    } as IQuickbetReceiptDetailsModel;
  });

  it('should create LadbrokesQuickbetReceiptComponent instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should set isGermanUser', () => {
      LadbrokesQuickbetReceiptComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component['getRcaeInfo'] =jasmine.createSpy('getRcaeInfo');
      component['getRacingPostData'] =jasmine.createSpy('getRacingPostData');
      component.ngOnInit();
      expect(component.isGermanUser).toBe(undefined);
    });
  });

  afterEach(() => {
    component = null;
  });
});
