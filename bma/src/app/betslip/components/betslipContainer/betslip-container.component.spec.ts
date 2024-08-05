import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BetslipContainerComponent } from './betslip-container.component';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { betslipReceiptBannerData, betslipReceiptBannerEmptyData } from '@app/betslip/components/betslipContainer/mockData/betslip-receipt-banner-data.mock';

describe('BetslipContainerComponent', () => {
  let localeService;
  let cmsService;
  let pubSubService;
  let sessionService;
  let component: BetslipContainerComponent;
  let nativeBridgeService;
  let device;
  let overAskService;
  let storageService,sessionStorageService, betReceiptService,changeDetector;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy()
    };
    cmsService = {
      triggerSystemConfigUpdate: jasmine.createSpy(),
      getSystemConfig: jasmine.createSpy().and.returnValue( of({winAlerts: { enabled: true }}) )
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    sessionService = {
      whenSession: jasmine.createSpy().and.returnValue(Promise.resolve(true))
    };
    nativeBridgeService = {
      onActivateWinAlerts: jasmine.createSpy()
    };
    device = {
      isMobile: true,
      isMobileOnly: true
    };
    overAskService = {};

    storageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'betSelections') { return [{ details: { cashoutAvail: 'Y', marketCashoutAvail: 'Y' }}] }
      }), 
      set: jasmine.createSpy('set')
    };

    betReceiptService = {
      getBetReceiptSiteCoreBanners: jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(of(betslipReceiptBannerData)),
    };
    
    sessionStorageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'betPlaced') { return false }
      }), 
      set: jasmine.createSpy('set')
    };
    changeDetector = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
  };
    component = new BetslipContainerComponent(localeService, cmsService, pubSubService,
      sessionService, nativeBridgeService, device, overAskService, storageService,sessionStorageService, betReceiptService,changeDetector);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
    expect(component['modes']).toBeDefined();
    expect(localeService.getString).toHaveBeenCalledTimes(6);
  });

  it('get MODES', () => {
    expect(component.MODES).toBe(component['modes']);
  });

  it('set MODES', () => {
    component['MODES'] = {};
    expect(component.MODES).toEqual({});
  })

  describe('selectBetSlipTab', () => {
    it('selectBetSlipTab', () => {
      component.mode = null;

      component.selectBetSlipTab('betslip', true);

      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubApi.BETSLIP_LABEL, 'betslip'
      );
    });

    it('selectBetSlipTab (update system config)', () => {
      component['modes'].betslip = 'betslip';

      component.selectBetSlipTab('betslip', false);

      expect(cmsService.triggerSystemConfigUpdate).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubApi.BETSLIP_LABEL, 'betslip'
      );
    });

    it('getBetslipReceiptBanners from betreceipt',()=> {
      component['bsMode'] = 'betReceipt';
      component.bsReceiptBannerImages = [];
      component.MODES.betReceipt = 'betReceipt';
      betReceiptService.getBetReceiptSiteCoreBanners = jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(of(betslipReceiptBannerData));
      component['getBetslipReceiptBanners']();
      expect(component.bsReceiptBannerImages).toEqual([{ bannerName : "betreceipttest", imageSrc: 'https://scmedia.cms.test.env.works/$-$/4d4490f2c2a44cff98790a4d8eaa49a4.jpg', imageHref: 'https://test.sports.coral.co.uk/promotions/all' } ]);
    })

    it('getBetslipReceiptBanners from totebet receipt',()=> {
      component['bsMode'] = 'toteBetReceipt';
      component.bsReceiptBannerImages = [];
      component.MODES.betReceipt = 'toteBetReceipt';
      betReceiptService.getBetReceiptSiteCoreBanners = jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(of(betslipReceiptBannerData));
      component['getBetslipReceiptBanners']();
      expect(component.bsReceiptBannerImages).toEqual([{ bannerName : "betreceipttest",imageSrc: 'https://scmedia.cms.test.env.works/$-$/4d4490f2c2a44cff98790a4d8eaa49a4.jpg', imageHref: 'https://test.sports.coral.co.uk/promotions/all' } ]);
    })

    it('getBetslipReceiptBanners when not in mobile device',()=> {
      device.isMobileOnly = false;
      component['bsMode'] = 'toteBetReceipt';
      component.bsReceiptBannerImages = [];
      component.MODES.betReceipt = 'toteBetReceipt';
      betReceiptService.getBetReceiptSiteCoreBanners = jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(of(betslipReceiptBannerData));
      component['getBetslipReceiptBanners']();
      expect(component.bsReceiptBannerImages).toEqual([]);
    })
    
    it('getBetBannerReceiptsData failure', fakeAsync(()=> {
      betReceiptService.getBetReceiptSiteCoreBanners = jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(of(betslipReceiptBannerEmptyData)),
      component.bsReceiptBannerImages = [];
      component['getBetslipReceiptBanners']();
      tick();
      expect(component.bsReceiptBannerImages).toEqual([]);
    }));

    it('getBetslipReceiptBanners when data from sitecore is empty',()=> {
      device.isMobileOnly = false;
      component['bsMode'] = 'toteBetReceipt';
      component.bsReceiptBannerImages = [];
      component.MODES.betReceipt = 'toteBetReceipt';
      betReceiptService.getBetReceiptSiteCoreBanners = jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(of([]));
      component['getBetslipReceiptBanners']();
      expect(component.bsReceiptBannerImages).toEqual([]);
    })

    it('checkIfBannersLoaded when it is mobile device and banners are loaded',()=> {
      component.device.isMobileOnly = true;
      component.bannersLoaded = true;
      const res = component.checkIfBannersLoaded();
      expect(res).toBe(true);
    })

    it('checkIfBannersLoaded when it is not a mobile device',()=> {
      component.device.isMobileOnly = false;
      const res = component.checkIfBannersLoaded();
      expect(res).toBe(true);
    })

    it('checkIfBannersLoaded when it is mobile device and banners are not loaded',()=> {
      component.device.isMobileOnly = true;
      component.bannersLoaded = false;
      const res = component.checkIfBannersLoaded();
      expect(res).toBe(undefined);
    })

    it('selectBetSlipTab (close bet receipt) should call native Bridge', () => {
      component.selectBetSlipTab('Bet Receipt', false);
      component.winAlertsBets = ['111', '222'];
      component.winAlertsReceiptId = '333';
      component.selectBetSlipTab('betslip');

      expect(nativeBridgeService.onActivateWinAlerts).toHaveBeenCalledWith('333', ['111', '222']);
    });
  });

    it('ngOnInit', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
      component.selectBetSlipTab = jasmine.createSpy();
      component.sessionStateDefined = true;

      component.ngOnInit();
      tick();

      expect(component.selectBetSlipTab).toHaveBeenCalledTimes(6);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
          component.tag, [pubSubService.API.SUCCESSFUL_LOGIN], jasmine.any(Function)
      );
      expect(sessionService.whenSession).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.tag, pubSubService.API.SESSION_LOGOUT, jasmine.any(Function)
      );
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.tag, pubSubApi.HOME_BETSLIP, jasmine.any(Function)
      );
      expect(cmsService.getSystemConfig.toHaveBeenCalled);
      expect(component.sysConfig).toEqual({ winAlerts: { enabled: true } });
    }));

    it('ngOnInit', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb('betslip'));
      component.selectBetSlipTab = jasmine.createSpy();
      component.sessionStateDefined = true;

      component.ngOnInit();
      tick();
      expect(component.selectBetSlipTab).toHaveBeenCalledTimes(5);
    }));

    it('ngOnInit (whenSession error #1)', fakeAsync(() => {
      sessionService.whenSession.and.returnValue(Promise.reject());
      component.selectBetSlipTab = jasmine.createSpy();

      component.ngOnInit();
      tick();
      expect(component.selectBetSlipTab['calls'].count()).toBe(1);
    }));

    it('ngOnInit (whenSession error #2)', fakeAsync(() => {
      sessionService.whenSession.and.returnValue(Promise.reject('error msg'));
      component.selectBetSlipTab = jasmine.createSpy();

      component.ngOnInit();
      tick();
      expect(component.selectBetSlipTab['calls'].count()).toBe(1);
    }));

    it('ngOnInit (!sessionStateDefined)', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((file, method, cb) => {
        if (method[0] === 'SESSION_LOGOUT') {
          cb();
        } else {
          cb('betslip');
        }
      });

      component.ngOnInit();
      tick();
      component.sessionStateDefined = false;

      spyOn(component, 'selectBetSlipTab');

      expect(component.selectBetSlipTab).not.toHaveBeenCalled();
    }));

    describe('ngOnInit BETSLIP_UPDATED', () => {
      beforeEach(() => {
        component.selectBetSlipTab = jasmine.createSpy('selectBetSlipTab');
        component['modes'].betslip = 'betslip';
        component['modes'].betReceipt = 'Bet Receipt';
      });
      it('should select betslip after betreceipt', fakeAsync(() => {
        pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
        component.sessionStateDefined = true;
        storageService.get.and.callFake((n)=>{
          if(n === 'betPlaced'){
            return false;
          }else if(n === 'betSelections'){
            return [];
          }
        })
        component.ngOnInit();
        tick();
        expect(pubSubService.subscribe).toHaveBeenCalledWith(
          component.tag, 'BETSLIP_UPDATED', jasmine.any(Function)
        );
        expect(component.selectBetSlipTab).toHaveBeenCalled();
      }));

      it('should not select betslip', fakeAsync(() => {
        component.sessionStateDefined = true;

        component.ngOnInit();
        tick();
        expect(pubSubService.subscribe).toHaveBeenCalledWith(
          component.tag, 'BETSLIP_UPDATED', jasmine.any(Function)
        );
        expect(component.selectBetSlipTab).toHaveBeenCalledTimes(2);
      }));
    });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component.tag);
  });

  describe('BetslipContainerComponent', () => {
    it('setWinAlertsBets should add betId', () => {
      const event = { receipt: { receipt: '111', uniqueId: '222' } as IBetDetail, value: true };

      component.setWinAlertsBets(event);

      expect(component.winAlertsReceiptId).toBe('111');
      expect(component.winAlertsBets).toEqual(['111']);
      expect(storageService.set).toHaveBeenCalledWith('winAlertsEnabled', true);
    });

    it('setWinAlertsBets should remove betId', () => {
      const event = { receipt: { receipt: '111', uniqueId: '222' } as IBetDetail, value: false };
      component.winAlertsBets = ['111', '333'];
      component.winAlertsReceiptId = '444';
      component.setWinAlertsBets(event);

      expect(component.winAlertsBets).toEqual(['333']);
      expect(component.winAlertsReceiptId).toEqual('444');
      expect(storageService.set).not.toHaveBeenCalledWith('winAlertsEnabled', false);
    });

    it('setWinAlertsBets should remove last betId', () => {
      const event = { receipt: { receipt: '111', uniqueId: '222' } as IBetDetail, value: false };
      component.winAlertsBets = ['111'];
      component.winAlertsReceiptId = '444';
      component.setWinAlertsBets(event);
      expect(storageService.set).toHaveBeenCalledWith('winAlertsEnabled', false);
    });

    it('should setWinAlertsBets (winAlertsReceiptId)', () => {
      const event = { receipt: { receipt: '111', uniqueId: '222' } as IBetDetail, value: true };
      component.winAlertsReceiptId = '333';

      component.setWinAlertsBets(event);

      expect(component.winAlertsReceiptId).toBe('333');
    });
  });

  it('should emit the height', () => {
    const bsHeight = 100;
    component.handleHeightUpdate(bsHeight);
    expect(component.bsMaxHeight).toEqual(`${bsHeight}px`);
  });

  it('should emit the height', () => {
    const bsHeight = 0;
    component.handleHeightUpdate(bsHeight);
    expect(component.bsMaxHeight).toEqual(`100%`);
  });
});


