import { LadbrokesBetslipReceiptComponent } from '@ladbrokesMobile/betslip/components/betslipReceipt/betslip-receipt.component';
import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LadbrokesBetslipReceiptComponent', () => {
  let component: LadbrokesBetslipReceiptComponent;

  let user,
    betReceiptService,
    sessionService,
    storageService,
    betSlipBannerService,
    betInfoDialogService,
    locationStub,
    gtmService,
    router,
    commandService,
    device,
    nativeBridgeService,
    windowRefService,
    bannersService,
    germanSupportService,
    bodyScrollLockService,
    gtmTrackingService,
    overAskService,
    localeService,
    pubSubService,
    // http,
    racingPostTipService,
    bppErrorService,
    sessionStorageService,
    freeRideHelperService,
    fbService,
    firstBetGAService,
    changeDetectionRef,
    scorecastDataService,
    bonusSuppressionService;

  beforeEach(() => {
    user = {
      oddsFormat: 'frac',
      receiptViewsCounter: 0,
      winAlertsToggled: false,
      set: jasmine.createSpy()
    };
    betReceiptService = {
      getActiveSportsEvents: jasmine.createSpy('getActiveSportsEvents'),
      getActiveFootballEvents: jasmine.createSpy('getActiveFootballEvents'),
      getGtmObject: jasmine.createSpy().and.returnValue({}),
      reuse: jasmine.createSpy('reuse'),
      done: jasmine.createSpy('done'),
      clearMessage: jasmine.createSpy('clearMessage'),
      getBetReceipts: jasmine.createSpy('getBetReceipts').and.returnValue(observableOf({}))
    };
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve({}))
    };
    storageService = {
      remove: jasmine.createSpy('remove'),
      get: jasmine.createSpy('get')
    };
    betSlipBannerService = {
      setIsBannerAvailable: jasmine.createSpy(),
      setBanner: jasmine.createSpy()
    };
    betInfoDialogService = {
      multiple: jasmine.createSpy()
    };
    locationStub = {
      path: () => ''
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    gtmTrackingService = {};
    router = {
      navigate: jasmine.createSpy()
    };
    commandService = {
      executeAsync: () => Promise.resolve({
        streamActive: true,
        streamID: '111'
      }),
      API: {
        GET_LIVE_STREAM_STATUS: ''
      }
    };
    device = {};
    nativeBridgeService = {};
    windowRefService = {
      nativeWindow: {
        pushNotificationsEnabled: true
      }
    } as any;
    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser').and.returnValue(true)
    };
    bannersService = {
      fetchBetslipOffersFromAEM: jasmine.createSpy('fetchBetslipOffersFromAEM').and.returnValue(
        observableOf({ offers: [] })
      )
    };
    bodyScrollLockService = {
      enableBodyScroll: jasmine.createSpy('enableBodyScroll')
    };
    overAskService = {};
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };
    racingPostTipService = {};
    bppErrorService = jasmine.createSpyObj('bppErrorService', ['showPopup', 'errorHandler']);
    changeDetectionRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled'),
    };
    scorecastDataService = {
      setScorecastData: (data)=> { return data},
      getScorecastData: ()=> { return 'data'},
    }
  });

  function createComponent() {
    component = new LadbrokesBetslipReceiptComponent(
      user,
      betReceiptService,
      sessionService,
      storageService,
      betInfoDialogService,
      locationStub,
      gtmService,
      router,
      commandService,
      device,
      gtmTrackingService,
      bodyScrollLockService,
      nativeBridgeService,
      windowRefService,
      overAskService,
      localeService,
      pubSubService,
      // http,
      bppErrorService,
      racingPostTipService,
      sessionStorageService,
      freeRideHelperService,
      fbService,
      germanSupportService,
      firstBetGAService,
      changeDetectionRef,
      bonusSuppressionService,
      scorecastDataService
      );
  }
  
  afterEach(() => {
    component = null;
  });

  it('should create component instance', () => {
    createComponent();
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('#ngOnInit', () => {
      spyOn(LadbrokesBetslipReceiptComponent.prototype['__proto__'], 'ngOnInit');
      createComponent();
      component.ngOnInit();

      expect(component.isGermanUser).toBeTruthy();
    });
  });
  describe('#reloadComponent', () => {
    it('#reload', () => {
      spyOn(LadbrokesBetslipReceiptComponent.prototype['__proto__'], 'ngOnInit');
      createComponent();
      component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
      component.reloadComponent();

      expect(component.isGermanUser).toBeTruthy();
    });
  });
});
