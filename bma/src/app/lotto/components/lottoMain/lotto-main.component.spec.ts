

import { of as observableOf, of, throwError } from 'rxjs';
import { LottoMainComponent } from './lotto-main.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant'; 
import { NavigationEnd } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';
describe('LottoMainComponent', () => {
  let component: LottoMainComponent;

  let lottoService;
  let userService;
  let cmsService;
  let changeDetector;
  let pubSubService;
  let userBalanceUpdCb;
  let messageUpdateCb;
  let menuUpdateCb;
  let router;
  let locale;

  beforeEach(() => {
    lottoService = {
      getLotteriesByLotto: jasmine.createSpy().and.returnValue(observableOf(null)),
      getMenuItems: jasmine.createSpy(),
      setLottoCmsBanner: jasmine.createSpy(),
      cmsLotto: jasmine.createSpy()
    
    };

    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test_string')
    };

    changeDetector = {
      detectChanges: jasmine.createSpy()
    };

    userService = {
      currencySymbol: '$',
      status: true,
      currency: 'USD',
      oddsFormat: 9,
      sportBalance: 99
    };

    cmsService = {
      getItemSvg: jasmine.createSpy().and.returnValue(observableOf({})),
      svg:'icon',
      svgId:'icon',

      getLottoBanner: jasmine.createSpy('getLottoBanner').and.returnValue(of({
          globalBannerLink: 'string',
          globalBannerText: 'string',
          lottoConfig: [{
            name: 'lotto',
            brand: "ladbrokes"
          }]
      }))
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, callback) => {
        if (method === 'USER_BALANCE_UPD') {
          userBalanceUpdCb = callback;
        } else if (method === 'MSG_UPDATE') {
          messageUpdateCb = callback;
        } else if (method === 'MENU_UPDATE') {
          menuUpdateCb = callback;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    router={
      navigate: jasmine.createSpy('navigate'),
      url: 'test.com',

      isLinesummaryPage:true,
      events: of(new NavigationEnd(1, "linesummary", '')),
    }

    component = new LottoMainComponent(
      lottoService,
      userService,
      cmsService,
      changeDetector,
      pubSubService,
      router,
      locale
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should get lotteries by lotto', () => {
      component['init'] = () => { };
      component.ngOnInit();
      expect(lottoService.getLotteriesByLotto).toHaveBeenCalled();
    });

    it('should show error', ()=>{
      component['init'] = jasmine.createSpy('init');
      lottoService.getLotteriesByLotto = jasmine.createSpy('getLotteriesByLotto').and.returnValue(throwError('error'));
      component.ngOnInit();

      expect(component.state.error).toBeTruthy();
      expect(component.state.loading).toBeFalsy();
      expect(component['init']).not.toHaveBeenCalled();
    });

    it('should show error new ', () => {
      component['init'] = jasmine.createSpy('init');
      lottoService.getLotteriesByLotto = jasmine.createSpy('getLotteriesByLotto').and.returnValue(throwError('error'));
      component.ngOnInit();
      expect(component.state.error).toBeTruthy();
    });

  it("should get lottocmsBanner data", () => {
    component['init'] = jasmine.createSpy('init');
    component['ngOnInit']();
    component.lottoData = {};
    expect(component.state.loading).toBeFalsy();
  })

  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('lottoMainCtrl');
  });

  describe('init', () => {
    it('init', () => {
      component.lottoData = {};
      component['getSession'] = jasmine.createSpy('getSession');
      component['init']();
      menuUpdateCb('lotto-69');

      expect(cmsService.getItemSvg).toHaveBeenCalledWith('Lotto');
      expect(component['getSession']).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('lottoMainCtrl', 'USER_BALANCE_UPD', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('lottoMainCtrl', 'MSG_UPDATE', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('lottoMainCtrl', 'MENU_UPDATE', jasmine.any(Function));
      expect(changeDetector.detectChanges).toHaveBeenCalled();
      expect(component.activeUrl).toBe('lotto-69');
    });

    it('should get session data',  () => {
      component['getSession'] = jasmine.createSpy('getSession');
      lottoService.getLotteriesByLotto = jasmine.createSpy('getLotteriesByLotto').and.returnValue(throwError('error'));
      component['init']();
      userBalanceUpdCb();

      expect(component['getSession']).toHaveBeenCalled();
    });

    it('should set lotto message', () => {
      const message = { msg: 'msg', type: 'type' };
      component['init']();
      messageUpdateCb(message);

      expect(component.lottoMessage).toEqual(message);
      expect(changeDetector.detectChanges).toHaveBeenCalled();
    });
    it('should set route', fakeAsync(() => {
      const message = { msg: 'msg', type: 'type' };
      component['ngOnInit']();
      tick();
      // messageUpdateCb(message);
      expect(component.isLinesummaryPage).toBeTruthy();

    }));
  });

  it('getSession', () => {
    component['getSession']();
    expect(component.currencySymbol).toEqual('$');
    expect(component.sessionStatus).toEqual(true);
    expect(component.currency).toEqual('USD');
    expect(component.oddsFormat).toEqual(9);
    expect(component.userBalance).toEqual(99);
  });
});
