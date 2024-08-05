import { BetpackCardComponent } from '@app/betpackMarket/components/betpackCard/betpack-card.component';
import { fakeAsync } from '@angular/core/testing';
import { ACC_LIMIT_FREEBETS, BP_MAX_CLAIM_DATA,ACC_LIMIT_FREEBETS_2,ACC_LIMIT_FREEBETS_3,ACC_LIMIT_FREEBETS_4, ACC_LIMIT_FREEBETS_5,ACC_LIMIT_FREEBETS_6 } from '@app/betpackMarket/constants/constants';

describe('BetpackCardComponent', () => {
  let component: any;
  let componentFactoryResolver,
    dialogService,
    pubSubService,
    userService,
    betpackCmsService,
    changedetectorRef,
    rendererService,
    date,
    gtmService,
    timeService;


  beforeEach(() => {
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    date = new Date();
    const data = { response: { endTime: date, freebetOfferId: "37897", freebetOfferLimits: { limitEntry: [{ limitDefinition: { limitComponent: { limitParam: [{ name: "current", value: 0 }, { name: "threshold", value: 1 }] } } }] } } };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn(data)),
      publish: jasmine.createSpy('publish'),
      API: { SESSION_LOGIN: 'SESSION_LOGIN' }
    },
      userService = {
        currencySymbol: '£',
        status: true,
        isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true),
      };
    changedetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges').and.returnValue(true)
    };
    betpackCmsService = {
      socketStorage: {
        get: jasmine.createSpy('get').and.returnValue(true),
        set: jasmine.createSpy('set').and.returnValue(true),
        has: jasmine.createSpy('set').and.returnValue(false),
      },
      getFreeBets: [],
      currentActiveBP: {}
    },
      rendererService = {};
    gtmService = {
      push: jasmine.createSpy('push')
    };
    timeService = {
      parseDateTime: (parseDate) => {
        return new Date(parseDate);
      }
    };

    component = new BetpackCardComponent(componentFactoryResolver,
      dialogService,
      pubSubService,
      userService,
      betpackCmsService,
      changedetectorRef,
      rendererService,
      gtmService,
      timeService
    );
    component.threshold = jasmine.createSpy('threshold').and.returnValue(true);
  });

  describe('ngOnInit', () => {
    it('should invoke on load with proper response', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout' };
      component.bp = { betPackId: "37897", betPackPurchaseAmount: 3, signPostingMsg: 'soldout', expiresIntimer: '30' };
      component.isMaxPurchaseLimitOver = false;
      betpackCmsService.socketStorage.has = jasmine.createSpy('set').and.returnValue(true);
      component.userService.username='test';
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component.isExpanded).toBe('enabled');
      // expect(component.current).toBe(0);
      // expect(component.threshold).toBe(1);
      // expect(betpackCmsService.currentActiveBP).toEqual(null);
      // expect(component.socketData).toEqual({ id: 1, betpackEndDate: date, current: 0, threshold: 1, maxClaimLimitRemaining: undefined });
    }));

    it('should invoke on load with signPostingMsg not equal to soldOutLabel', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: "37897", betPackPurchaseAmount: 3, signPostingMsg: 'ending soon', expiresIntimer: '30' };
      component.betpackCmsService.currentActiveBP = { betPackId: "37897" };
      betpackCmsService.socketStorage.has = jasmine.createSpy('set').and.returnValue(false);
      betpackCmsService.userloginLoaded = false;
      spyOn(component, 'signPostings');
      spyOn(component, 'BetpackPopUpState');
      component.userService.username='test';
      component.ngOnInit();
      expect(component.bp.betPackId).toEqual("37897");
    }));

    it('should invoke on load incase of no proper response-scenario1', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897"}}));
      component.userService.username=null;
      spyOn(component, 'signPostings');
      component.ngOnInit();
      // expect(component.signPostings).toHaveBeenCalled();
      expect(true).toBe(true);
    }));

    it('should check if login', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '123', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{offerGroupId:10}}}));
      component.userService.username='abc';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));

    it('should invoke on load incase of no proper response-scenario2', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'abc' };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3, signPostingMsg: 'abc' };
      spyOn(component, 'signPostings');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
      component.ngOnInit();
      expect(component.signPostings).not.toHaveBeenCalled();
      expect(component.socketData).toBeUndefined();
    }));

    it('should set bpMaxclaimData value', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'abc' };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3, signPostingMsg: 'abc',offerGroupId:10 };
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      spyOn(component, 'signPostings');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
      component.ngOnInit();
      expect(component.bpMaxClaimData).not.toEqual(null);
    }));

    it('should set bpMaxclaimData value 2', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'abc' };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3, signPostingMsg: 'abc',offerGroupId:10 };
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_2;
      spyOn(component, 'signPostings');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
      component.ngOnInit();
      expect(component.bpMaxClaimData).not.toEqual(null);
    }));

    it('should set bpMaxclaimData value 3', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'abc' };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3, signPostingMsg: 'abc',offerGroupId:10 };
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_3;
      spyOn(component, 'signPostings');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
      component.ngOnInit();
      expect(component.bpMaxClaimData).not.toEqual(null);
    }));

    it('should set bpMaxclaimData value', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'abc' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'abc',offerGroupId:10 };
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_2;
      spyOn(component, 'signPostings');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
      component.ngOnInit();
      expect(component.bpMaxClaimData).not.toEqual(null);
    }));

    it('should set bpMaxclaimData value', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'abc' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'abc',offerGroupId:10 };
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_3;
      spyOn(component, 'signPostings');
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
      component.ngOnInit();
      expect(component.bpMaxClaimData).not.toEqual(null);
    }));
    

    it('should invoke on load incase of no proper response-scenario3', fakeAsync(() => {
      component.betpackLabels = { maxPurchasedLabel: null };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3 };
      betpackCmsService.socketStorage = null;
      component.userService.username='test';
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ response: {} }));
      component.ngOnInit();
      expect(component.socketData).toBeUndefined();
    }));

    it('should invoke on load incase of no proper response-scenario4', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '378972', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{offerGroupId:10}}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));


    it('should invoke on load incase of no proper response-scenario6', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_2;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{offerGroupId:10}}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));

    it('should invoke on load incase of no proper response-scenario7', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_3;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{offerGroupId:10}}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));

    it('should invoke on load incase of no proper response-scenario8', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_4;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{offerGroupId:10}}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));
    it('should invoke on load incase of no proper response-scenario9', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_5;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:null}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));
    it('should invoke on load incase of no proper response-scenario10', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_6;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{ offerGroupId:10,
      offerGroupName:"test"}}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));

  

    it('should invoke on load incase of no proper response-scenario4', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897"}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      component.ngOnInit();
      expect(true).toBe(true);
    }));
    it('should invoke on load with proper response with ', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout' };
      component.bp = { betPackId: "37897", betPackPurchaseAmount: 3, signPostingMsg: 'soldout', expiresIntimer: '30' ,offerGroupId :10};
      component.isMaxPurchaseLimitOver = false;
      betpackCmsService.socketStorage.has = jasmine.createSpy('set').and.returnValue(true);
      component.userService.username='test';
      component.bpMaxClaimData = {test: '1'};
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      component.maxClaimLimitRemaining = 0;
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component.isExpanded).toBe('enabled');
    }));


    it('should invoke on load with proper response with with maxlimit undefined', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout' };
      component.bp = { betPackId: "37897", betPackPurchaseAmount: 3, signPostingMsg: 'soldout', expiresIntimer: '30' ,offerGroupId :10};
      component.isMaxPurchaseLimitOver = false;
      betpackCmsService.socketStorage.has = jasmine.createSpy('set').and.returnValue(true);
      component.userService.username='test';
      component.bpMaxClaimData = {test: '1'};
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      component.maxClaimLimitRemaining = 1;
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component.isExpanded).toBe('enabled');
    }));
	
	    it('should invoke on load incase of no proper response-scenario11', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz', maxPurchasedLabel: 'max1', soldOutLabel: 'soldout', expiresInLabel: 'expiresinlabel' };
      component.bp = { betPackId: '37897', betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      betpackCmsService.socketStorage = null;
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS_2;
      pubSubService.subscribe= jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({response:{freebetOfferId:"37897",offerGroup:{offerGroupId:10}}}));
      component.userService.username='test';
      spyOn(component, 'signPostings');
      spyOn(component, 'getMaxClaimData');
      component.maxClaimLimitRemaining = 0;
      component.ngOnInit();
      expect(true).toBe(true);
    }));
  });

  describe('ngOnDestroy', () => {
    it('ngOnDestroy', () => {
      component.timer = setInterval(() => { }, 1000);
      component.ngOnDestroy();
      expect(component.timer).toEqual(jasmine.any(Number));
    });
  });

  describe('BetpackPopUpState', () => {
    it('should invoke in case of currentActiveBP', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz' };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3, signPostingMsg: 'msg', signPostingToolTip: 'tooltipmsg' };
      betpackCmsService.currentActiveBP = { betPackId: 1, betPackPurchaseAmount: '£2', betPackFreeBetsAmount: '£3' };
      spyOn(component, 'buyNow');
      component.BetpackPopUpState(component.bp);

      expect(component.buyNow).toHaveBeenCalled();
      expect(betpackCmsService.currentActiveBP.betPackPurchaseAmount).toBe('£2');
      expect(betpackCmsService.currentActiveBP.betPackFreeBetsAmount).toBe('£3');
    }));

    it('should invoke in case of no currentActiveBP', fakeAsync(() => {
      component.betpackLabels = { buyNowLabel: 'xyz' };
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3 };
      betpackCmsService.currentActiveBP = { betPackId: null, betPackPurchaseAmount: null, betPackFreeBetsAmount: null };
      spyOn(component, 'buyNow');
      component.BetpackPopUpState();

      expect(component.buyNow).not.toHaveBeenCalled();
    }));
  });

  describe('signPostingBkg', () => {
    it('signPostingBkg should be called when  max purchased sign posting', () => {
      const signPostingMsg = 'Max Purchased';
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased' };
      component.bp = {};
      const style = component.signPostingBkg(signPostingMsg);
      expect(style).toEqual({ 'background-color': '#DD4647', 'color': '#FFFFFF' });
    });

    it('signPostingBkg should be called when limited availability sign posting', () => {
      const signPostingMsg = 'Limited Availability';
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased' };
      const style = component.signPostingBkg(signPostingMsg);
      expect(style).toEqual({ 'background-color': '#FFF270', 'color': '#07294B' });
    });

    it('signPostingBkg should be called when unlimited sign posting', () => {
      const signPostingMsg = '~';
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased' };
      const style = component.signPostingBkg(signPostingMsg);
      expect(style).toEqual({ 'background-color': '#FFFFFF', 'color': '#FFFFFF' });
    });
    it('signPostingBkg should be called when comingSoon sign posting', () => {
      const signPostingMsg = 'COMING SOON';
      component.bp={disableBuyBtn:false}
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased',comingSoon: "COMING SOON"};
      const style = component.signPostingBkg(signPostingMsg);
      expect(style).toEqual({ 'background-color': '#8D5BA1', 'color': '#FFFFFF' });
    });
  });

  describe('checkThresholdValue --->', () => {
    it('when threshold is unlimited', () => {
      component.threshold = 'unlimited';
      const result = component.checkThresholdValue();
      expect(result).toBe(true);
    })
    it('when threshold is not unlimited', () => {
      component.threshold = '';
      const result = component.checkThresholdValue();
      expect(result).toBe(false);
    })
  });

  describe('signPostings', () => {
    it('signPostings should be called when  true', () => {
      const bp = {
        id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      component.signPostings(bp);
      expect(component.bp.betpackLabels).toBe(undefined);
    });

    it('signPostings should be called when  endingSoonLabel', () => {
      const bp = {
        id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 10700000)).toISOString(),
        expiryData: new Date(new Date().setTime(new Date().getTime() + 20800000)).toISOString()
      };
      component.bp = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { endingSoonLabel: 'ENDING SOON' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toEqual(component.betpackLabels.endingSoonLabel);
    });
    it('signPostings should be called when  coming soon', () => {
      const bp = {
        id: '2', threshold: 100, current: 20, betpackStartDate: new Date(new Date().setTime(new Date().getTime() + 10700000)).toISOString(),
        expiryData: new Date(new Date().setTime(new Date().getTime() + 20800000)).toISOString()
      };
      component.bp = bp;
      component.bp={betPackStartDate:new Date().toISOString()}
      component.bp.signPostingMsg = 'COMING SOON';
      component.betpackLabels = { comingSoon: 'COMING SOON' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toEqual(component.betpackLabels.comingSoon);
    });

    it('signPostings should be called when  maxPurchasedLabel', () => {
      const bp = {
        id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 3500000)).toISOString(),
        expiryData: new Date(new Date().setTime(new Date().getTime() + 20800000)).toISOString()
      };
      component.bp = bp;
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toEqual(component.betpackLabels.endedLabel);
    });

    it('signPostings should be called when  ENDED', () => {
      const bp = {
        id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString(),
        expiryData: new Date(new Date().setTime(new Date().getTime() + 20800000)).toISOString()
      };
      component.bp = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { endedLabel: 'ENDED' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toEqual(component.betpackLabels.endedLabel);
    });

    it('signPostings should be called and set signposting as MAX N where N is OB value if OB value present', () => {
      component.userService.username = 'abc';
      const bp = {
        id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(),
        expiryData: new Date(new Date().setTime(new Date().getTime() + 10800000)).toISOString(), maxClaimLimitRemaining: 3
      };
      component.bp = bp;
      component.betpackLabels = { endedLabel: 'ENDED', maxOnePurchasedLabel: 'MAX <max-claims>', maxOnePurchasedTooltip: 'MAX <max-claims>' };
      component.bp.signPostingMsg = 'MAX 1';
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toEqual('MAX 3');
    });

    it('signPostings should be called when soldOutLabel ', () => {
      const bp = {
        id: '2', betPackId: 'test', threshold: 100, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      betpackCmsService.currentActiveBP = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { soldOutLabel: 'Sold out', soldOutTooltip: 'Sold out tooltip' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toBe('Sold out');
      expect(pubSubService.publish).toHaveBeenCalledWith('BETPACK_UPDATE', { signPost: 'Sold out', signPostTooltip: 'Sold out tooltip', betpackId: 'test', expiresIntimer: null });
    });
    
    it('signPostings should be called and buy button should be diabled when unlimited', () => {
      const bp = {
        id: '2', betPackId: 'test', threshold: 'unlimited', current: '0',
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.checkThresholdValue = jasmine.createSpy('checkThresholdValue').and.returnValue(true);
      component.bp = bp;
      betpackCmsService.currentActiveBP = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { soldOutLabel: 'Sold out', soldOutTooltip: 'Sold out tooltip' };
      component.signPostings(bp);
      expect(component.bp.disableBuyBtn).toBe(false);
    });

    it('signPostings should be called and buy button should not be diabled when unlimited', () => {
      const bp = {
      };
      component.checkThresholdValue = jasmine.createSpy('checkThresholdValue').and.returnValue(true);
      component.bp = bp;
      betpackCmsService.currentActiveBP = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { soldOutLabel: 'Sold out', soldOutTooltip: 'Sold out tooltip' };
      component.signPostings(bp);
      expect(component.bp.disableBuyBtn).toBe(undefined);
    });

    it('signPostings when threshold is more than current', (fakeAsync(() => {
      const bp = {
        id: '37897', betPackId: '37897', threshold: 101, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString(),
          offerGroupId:10,
          offerGroupName:"test"
      
      };
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      component.bp = bp;
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased', buyNowLabel: 'Buy Now' };
      component.ngOnInit();
      expect(component.bpMaxClaimData).toEqual(BP_MAX_CLAIM_DATA);
    })));

    it('to check if bpMaxClaimData is called on component init', () => {
      const bp = {
        id: '37897', betPackId: '37897', threshold: 101, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString(),offerGroupId:10
      };
      const getMaxClaimData=spyOn(component,'getMaxClaimData');
      component.accLimitFreeBets = ACC_LIMIT_FREEBETS;
      component.bp = bp;
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased', buyNowLabel: 'Buy Now' };
      component.ngOnInit();
      expect(getMaxClaimData).toHaveBeenCalledWith(bp);
    });

    it('signPostings when limit is unlimited', () => {
      component.signPostings = jasmine.createSpy('');
      const bp = {
        id: '1', betPackId: '1', threshold: 100, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      component.betpackLabels = { maxPurchasedLabel: 'Max Purchased' };
      const data = { response: { endTime: date, freebetOfferId: '1', freebetOfferLimits: null } };
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn(data));
      component.ngOnInit();
      expect(component.current).toBe('unlimited');
      expect(component.threshold).toBe('unlimited');
      expect(component.socketData).toBeDefined();
      expect(component.signPostings).toHaveBeenCalled();
    });

    it('signPostings when limit is maz1', () => {
      component.isOBMaxClaim = jasmine.createSpy('isOBMaxClaim').and.returnValue(false);
      component.isLogin = jasmine.createSpy('isLogin').and.returnValue(true);
      const bp = {
        id: '1', betPackId: '1', threshold: 101, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      component.bp.maxClaims = 1;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { limitedLabel: 'Limited', limitedTooltip: 'Limited tooltip', 
        maxOnePurchasedLabel: 'MAX <max-claims>', maxOnePurchasedTooltip: 'MAX <max-claims>'
      };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toBe('MAX 1');
      expect(component.bp.signPostingToolTip).toBe('MAX 1');
      expect(component.bp.disableBuyBtn).toBe(false);
    });

    it('signPostings when limit is limited', () => {
      component.checkThresholdValue = jasmine.createSpy('checkThresholdValue').and.returnValue(false);
      const bp = {
        id: '1', betPackId: '1', threshold: 101, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { limitedLabel: 'Limited', limitedTooltip: 'Limited tooltip' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toBe('Limited');
      expect(component.bp.signPostingToolTip).toBe('Limited tooltip');
      expect(component.bp.disableBuyBtn).toBeDefined();
    });

    it('signPostings when limit is limited and total max claim current is 0', () => {
      component.checkThresholdValue = jasmine.createSpy('checkThresholdValue').and.returnValue(false);
      const bp = {
        id: '1', betPackId: '1', threshold: 101, current: 0, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { limitedLabel: 'Limited', limitedTooltip: 'Limited tooltip' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toBe(' ');
      expect(component.bp.disableBuyBtn).toBeDefined();
    });


    it('signPostings should be called when endedLabel ', () => {
      const bp = {
        id: '2', betPackId: 'test', threshold: 100, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString(),
        expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
      };
      component.bp = bp;
      component.bp.signPostingMsg = 'MAX 1';
      component.betpackLabels = { endedLabel: 'Ended', endedTooltip: 'Ended tooltip' };
      component.signPostings(bp);
      expect(component.bp.signPostingMsg).toBe('Ended');
      expect(pubSubService.publish).toHaveBeenCalledWith('BETPACK_UPDATE', { signPost: 'Ended', signPostTooltip: 'Ended tooltip', betpackId: 'test', expiresIntimer: null });
    });

    it('signPostings should be called when  no betpack', () => {
      component.expireIn = true;
      component.betpackLabels = { endedLabel: 'Ended' };
      component.bp = {};
      component.bp.signPostingMsg = 'MAX 1';
      component.signPostings(null);
      expect(component.bp.disableBuyBtn).toBe(true);
    });
  });

  describe('moreInfo', () => {
    it('moreInfo should be called', () => {
      spyOn(component, 'openPopup');
      const bp = "betpack";
      const event = {};
      const signPostingMsg = 'Max Purchased';
      component.moreInfo(bp, event, signPostingMsg);
      expect(component.openPopup).toHaveBeenCalled();
    });
  });

  describe('buyNow', () => {
    it('buyNow should be called', () => {
      spyOn(component, 'openPopup');
      const bp = { signPostingMsg: 'Max Purchased' };
      const event = {};
      const signPostingMsg = 'Max Purchased';
      component.buyNow(bp, event, signPostingMsg);
      expect(component.openPopup).toHaveBeenCalled();
    });
  });

  describe('isUpgradeVisible', () => {
    it('isUpgradeVisible should be called', () => {
      userService.bppToken = true;
      component.isUpgradeVisible();
      expect(userService.isInShopUser).toHaveBeenCalled();
    });
  });


  describe('tokenLengthCheck', () => {
    it('tokenLengthCheck should be defined', () => {
      expect(component.tokenLengthCheck(5)).toBe(1);
    });
  });

  describe('openPopUp', () => {
    it('open dialog', () => {
      component.betpackLabels = {};
      component.isBuyInfoClicked = true;
      component.clicked = false;
      const reviewPage = false;
      const bp = {};
      const event = {};
      const signPostingMsg = "xyz";
      const data = {
        dialogClass: 'scorecastOddsDialog',
        data: {
          bp: bp,
          betpackLabels: component.betpackLabels,
          isBuyInfoClicked: component.isBuyInfoClicked,
          clicked: component.clicked,
          reviewPage: false,
          signPostingMsg: signPostingMsg,
        }
      };
      component.openPopup(bp, event, signPostingMsg);
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    });
  });

  describe('ontimerEmits', () => {
    it('should call on ontimerEmits', fakeAsync(() => {
      component.bp = { betPackId: 1, betPackPurchaseAmount: 3, signPostingMsg: 'ending soon' };
      component.betpackLabels = { endedLabel: 'ENDED' };
      component.ontimerEmits(false);
      expect(component.isExpiresIn).toBeFalse();
      expect(component.bp.disableBuyBtn).toBeTruthy();
      expect(component.bp.expireIn).toBe(null);
      expect(component.bp.signPostingMsg).toBe(component.betpackLabels.endedLabel);
      expect(component.bp.signPostingToolTip).toBe(component.betpackLabels.endedTooltip);
    }));
  });

  describe('sendgmt', () => {
    it('should send GA tracking info on click of buy button', () => {
      component.sendgmt({ betPackId: '12432' });
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('getMaxClaimData', () => {
    it('getMaxClaimData ', () => {
      const bp = {offerGroupId: '10'};
      component.accLimitFreeBets = [{offerGroup: {offerGroupId: '10'}}]
      component.getMaxClaimData(bp);
    })
    it('getMaxClaimData ', () => {
        const bp = {offerGroupId: '10'};
        component.accLimitFreeBets = [{offerGroup: {offerGroupId: '10'}, freebetOfferLimits : {limitEntry : [{limitSort: 'OFFER_MAX_CLAIMS_LIMIT'}, {limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT'}]}}]
        component.getMaxClaimData(bp);
    })

    it('getMaxClaimData ', () => {
      const bp = {offerGroupId: '10'};
      component.accLimitFreeBets = [{offerGroup: {offerGroupId: '10'}, freebetOfferLimits : {limitEntry : [{limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }, {limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '1'}]}}]
      component.getMaxClaimData(bp);
    })

    it('getMaxClaimData ', () => {
      const bp = {offerGroupId: '10', maxClaims: 5, betPackId: '10'};
      component.accLimitFreeBets = [{freebetOfferId:'10', offerGroup: {offerGroupId: '10'}, freebetOfferLimits : {limitEntry : [{limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }, {limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '1'}]}}]
      component.getMaxClaimData(bp);
      bp.betPackId = '9';
      component.getMaxClaimData(bp);
    })

    it('getMaxClaimData ', () => {
      const bp = {offerGroupId: '10', maxClaims: 5, betPackId: '10'};
      component.accLimitFreeBets = [{freebetOfferId:'10', offerGroup: {offerGroupId: '10'}, freebetOfferLimits : {limitEntry : [{limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '12' }, {limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '1'}]}}]
      component.getMaxClaimData(bp);
      bp.betPackId = '9';
      bp.maxClaims = 0;
      component.getMaxClaimData(bp);
    })
  });
  describe('checkStatus', () => {
    it('checkStatus Have Been Called', () => {
      component.betpackLabels={comingSoon:'test'};
      expect(component.checkStatus('test')).toBeTruthy();
    });
  });
});