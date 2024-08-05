import { of as observableOf, throwError } from 'rxjs';

import { ToteBetReceiptComponent } from './tote-bet-receipt.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('ToteBetReceiptComponent', () => {
  let component: ToteBetReceiptComponent;
  let userService;
  let toteBetslipService;
  let deviceService;
  let pubSubService;
  let storageService;
  let toteBetReceiptService;
  let toteBet;
  let cmsService;
  let gtmService;
  let windowRefService;

  beforeEach(() => {
    userService = {
      currencySymbol: '$'
    };
    toteBetslipService = {
      addToteBet: jasmine.createSpy(),
      removeToteBet: jasmine.createSpy(),
      getTokenValue: jasmine.createSpy().and.returnValue('')
    };
    deviceService = {
      deviceService: true,
      isMobile: true
    };
    windowRefService = {
      nativeWindow: {
        NativeBridge : { pushNotificationsEnabled: true },
        location: {
          pathname: 'testPath'
        }
      }
    } as any;
    pubSubService = {
      publish: jasmine.createSpy(),
      API: pubSubApi
    };
    toteBet = {
      poolCurrencyCode: 'GBP',
      events: [{categoryId: '21'}]
    };
    storageService = {
      get: () => {
        return toteBet;
      }
    };
    toteBetReceiptService = {
      getToteBetReceipt: () => observableOf([{
        date: '123',
        stake: '2.45'
      }])
    };
    cmsService = {
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(observableOf({
        svg: 'svg',
        svgId: 'svgId'
      })),
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        CelebratingSuccess: {
          cashoutMessage: "YOU HAVE CASHED OUT: {amount}!!",
          celebrationBannerURL: "{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}",
          celebrationMessage: "CONGRATS!",
          displayCelebrationBanner: true,
          duration: 48,
          winningMessage: "YOU HAVE WON: {amount}!!",
          displaySportIcon: ["openbets", "settledbets", "cashoutbets", "betreceipt", "edpmybets"]
        }
      }))
    };
    gtmService = {
      push: jasmine.createSpy()
    };

    component = new ToteBetReceiptComponent(pubSubService, deviceService, toteBetslipService,
      storageService, toteBetReceiptService, userService, cmsService,gtmService,windowRefService);
  });

  it('should create and init component: success', () => {
    expect(component).toBeTruthy();
    expect(component.poolCurrencyCode).toEqual('GBP');
    expect(component.userCurrencySymbol).toEqual('$');
  });

  it('should create and init component: failed', () => {
    component['toteBetReceiptService'].getToteBetReceipt = jasmine.createSpy().and.returnValue(throwError(
      'Failed to fetch'
    ));
    component['getToteBetReceipt']();
    expect(component.loadComplete).toBeTruthy();
    expect(component.loadFailed).toBeTruthy();
  });

  it('Should track site core banners', () => {
    component.trackSiteCoreBanners("p1%20-%201-2-free%20week%2012%20-%20uk%20-%2027th%20march%20-%201st%20april");
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('getItemSvg as empty', () => {
    cmsService.getItemSvg.and.returnValue(observableOf({}));
    component.toteBetDetails = {svgId: null} as any;
    component['setSvgId']();
    expect(component.toteBetDetails.svgId).toBe('icon-generic');
  });
  it('getItemSvg with totebet as null', () => {
    cmsService.getItemSvg.and.returnValue(observableOf({}));
    component['toteBet'] = null;
    component['setSvgId']();
  });
  it('getItemSvg with totebet events as null', () => {
    cmsService.getItemSvg.and.returnValue(observableOf({}));
    component['toteBet'] = {events: [null]} as any;
    component['setSvgId']();
  });
  it('setSvgId with cms config as null', () => {
    cmsService.getSystemConfig.and.returnValue(observableOf(null));
    component['setSvgId']();
  });
  it('setSvgId with cms config CelebratingSuccess as null', () => {
    cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: null}));
    component['setSvgId']();
  });
  it('setSvgId with cms config displaySportIcon as undefined', () => {
    cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: {displaySportIcon: undefined}}));
    component['setSvgId']();
    expect(component.isSportIconEnabled).not.toBeTrue();
  });
  describe('done', () => {
    it('done', () => {
      component.done();
      expect(pubSubService.publish).toHaveBeenCalledTimes(2);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });

    it('done (no mobile)', () => {
      component['deviceService']['isMobile'] = false;
      component.done();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('show-slide-out-betslip', false);
    });
  });

  it('reuse', () => {
    component['toteBet'] = {
      poolBet: {
        freebetTokenId: '1234',
        freebetTokenValue: '1234'
      }
    } as any;
    component.reuse();

    expect(toteBetslipService.addToteBet).toHaveBeenCalledTimes(1);
    expect(toteBetslipService.addToteBet).toHaveBeenCalledWith({poolBet: {}},{poolBet: {}});

    expect(pubSubService.publish).toHaveBeenCalledTimes(2);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.REUSE_TOTEBET);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
  });

  it('should getToteBet', () => {
    component['storageService']['get'] = jasmine.createSpy('get').and.returnValue(undefined);
    expect(component['getToteBet']()).toEqual(null);
  });
});
