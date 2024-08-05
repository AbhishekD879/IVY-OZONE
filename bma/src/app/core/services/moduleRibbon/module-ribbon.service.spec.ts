import { ModuleRibbonService } from './module-ribbon.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';

describe('ModuleRibbonService', () => {
  let service;
  let location;
  let device;
  let pubSubService;
  let locale;
  let privateMarketsService;
  let router;
  const events = [{
    markets: []
  }, {
    markets: [{
      outcomes: []
    }]
  }, {
    markets: [{
      outcomes: [{ id: 1 }]
    }]
  }];

  beforeEach(() => {
    location = {
      isCurrentPathEqualTo: jasmine.createSpy('isCurrentPathEqualTo')
    };
    device = {};
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    locale = {
      getString: jasmine.createSpy('getString')
    };
    privateMarketsService = {
      markets: jasmine.createSpy('markets').and.returnValue(of(events))
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    service = new ModuleRibbonService(location, device, pubSubService, locale, privateMarketsService, router);
  });

  describe('constructor', () => {
    it('should set initial values', () => {
      expect(locale.getString).toHaveBeenCalled();
      expect(service.moduleList).toEqual([]);
      expect(service.privateMarket).toEqual(jasmine.objectContaining({
        directiveName: 'PrivateMarkets',
        visible: true,
        modules: [],
        showTabOn: 'both',
        id: 'tab-private-markets',
        url: '/home/private-markets'
      }));
    });

    it('should set privateMarketsUrl', () => {
      expect(service.privateMarketsUrl).toEqual('/home/private-markets');
    });
  });

  describe('isPrivateMarketsTab', () => {
    it('should return false if moduleList is not available', () => {
      service.moduleList = null;

      expect(service.isPrivateMarketsTab()).toBeFalsy();
    });

    it('should return false if moduleList is empty', () => {
      service.moduleList = [];

      expect(service.isPrivateMarketsTab()).toBeFalsy();
    });

    it('should return false if first module is not private markets', () => {
      service.moduleList = [{ directiveName: 'PrivateMarketsFake' }];

      expect(service.isPrivateMarketsTab()).toBeFalsy();
    });

    it('should return true if first module is private markets', () => {
      service.moduleList = [{ directiveName: 'PrivateMarkets' }];

      expect(service.isPrivateMarketsTab()).toBeTruthy();
    });
  });

  describe('isPrivateMarketsAvailable', () => {
    it('should return false if first module is private markets', () => {
      service.moduleList = [{ directiveName: 'PrivateMarkets' }];

      expect(service['isPrivateMarketsAvailable']([])).toBeFalsy();
    });

    it('should return false if no events passed', () => {
      service.moduleList = [{ directiveName: 'PrivateMarketsFake' }];

      expect(service['isPrivateMarketsAvailable'](null)).toBeFalsy();
      expect(service['isPrivateMarketsAvailable']([])).toBeFalsy();
    });

    it('should return false if empty markets in event passed', () => {
      const emptyMarkets = [{ markets: [] }];
      service.moduleList = [{ directiveName: 'PrivateMarketsFake' }];

      expect(service['isPrivateMarketsAvailable'](emptyMarkets)).toBeFalsy();
    });

    it('should return false if empty outcomes in market passed', () => {
      const emptyOutcomes = [{
        markets: [{
          outcomes: []
        }]
      }];
      service.moduleList = [{ directiveName: 'PrivateMarketsFake' }];

      expect(service['isPrivateMarketsAvailable'](emptyOutcomes)).toBeFalsy();
    });

    it('should return true if outcomes are passed in event passed', () => {
      service.moduleList = [{ directiveName: 'PrivateMarketsFake' }];

      expect(service['isPrivateMarketsAvailable'](events)).toBeTruthy();
    });
  });

  it ('should get Private Mrarkets', () => {
    service.getPrivateMarketTab([]);

    expect(privateMarketsService.markets).toHaveBeenCalled();
  });

  describe('addTab', () => {
    it('should not notify via pubsub if modulelist not available', () => {
      service.moduleList = null;
      service['addTab']([]);

      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });

    it('should not notify via pubsub if modulelist is empty', () => {
      service['addTab']([]);

      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });

    it('should add private markets tab', () => {
      service.moduleList = [{ directiveName: 'someName' }];
      service['addTab'](events);

      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(service.privateMarketNamespace, ['SESSION_LOGOUT', 'HIDE_PRIVATE_MARKETS_TAB'], jasmine.any(Function));
      expect(service.moduleList[0].directiveName).toEqual('PrivateMarkets');
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });

    it('should add private markets tab and subscribe for events to Remove Tab', () => {
      service.moduleList = [{ directiveName: 'someName' }];
      service['addTab'](events);

      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(service.privateMarketNamespace, ['SESSION_LOGOUT', 'HIDE_PRIVATE_MARKETS_TAB'], jasmine.any(Function));
    });
  });

  describe('removeTab', () => {
    it('should add private markets tab, subscribe for events to Remove Tab and remove tab', () => {
      pubSubService.subscribe.and.callFake((namespace, eventName, callback) => {
        callback();
      });

      service.moduleList = [{ directiveName: 'someModule' }];
      service['addTab'](events);

      expect(service.moduleList).toEqual([{ directiveName: 'someModule' }]);
    });
    it('should remove first tab if it was privat markets', () => {
      service.moduleList = [{ directiveName: 'PrivateMarkets' }, { directiveName: 'someModule' }];
      service.removeTab();

      expect(service.moduleList).toEqual([{ directiveName: 'someModule' }]);
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('should remove first tab and redirect to home page', () => {
      service.moduleList = [{ directiveName: 'PrivateMarkets' }, { directiveName: 'someModule' }];
      location.isCurrentPathEqualTo.and.returnValue('/home/private-markets');

      service.removeTab();

      expect(service.moduleList).toEqual([{ directiveName: 'someModule' }]);
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should remove first tab and unsubscribe from privateMarket tab events', () => {
      service.moduleList = [{ directiveName: 'PrivateMarkets' }, { directiveName: 'someModule' }];
      service.removeTab();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(service.privateMarketNamespace);
    });
  });
});
