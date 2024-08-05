import { InShopBetsPageComponent } from '@app/betHistory/components/inShopBetsPage/in-shop-bets-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InShopBetsPageComponent', () => {
  let component: InShopBetsPageComponent;
  let pubSubService;
  let userService;
  let localeService;
  let ezNavVanillaService;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    userService = {};

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('')
    };

    ezNavVanillaService = {};

    component = new InShopBetsPageComponent(
      pubSubService,
      userService,
      localeService,
      ezNavVanillaService
    );
  });

  describe('ngOnInit', () => {
    it('should hide spinner and error', () => {
      spyOn(component, 'hideSpinner');
      spyOn(component, 'hideError');
      userService.status = true;

      component.ngOnInit();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.hideError).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component['cmpName'], 'SESSION_LOGIN', jasmine.any(Function) );
    });

    it('shoud show error message', () => {
      userService.status = false;
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledTimes(3);
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['cmpName']);
  });
  
});
