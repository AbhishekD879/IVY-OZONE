import { TennisExtensionService } from './tennis-extension.service';
import { Router } from '@angular/router';
import { flush, fakeAsync } from '@angular/core/testing';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { IMarket } from '@core/models/market.model';
import { IMarketCollection } from '@core/models/market-collection.model';

describe('TennisExtensionService', () => {
  let service: TennisExtensionService;
  let pubSubService: jasmine.SpyObj<PubSubService>;
  let routerService: jasmine.SpyObj<Router>;

  let parentScope;
  let collection: IMarketCollection;
  let tennisConfig;
  const updatedMarket: IMarket = { id: '1' } as IMarket;

  beforeEach(() => {
    parentScope = {
      marketsByCollection: [{
        name: 'Game',
        markets: [{ name: 'Game Markets' }]
      }],
      eventTabs: [{
        hidden: true,
        label: 'Game',
        id: 'tab-main-markets',
        url: '/'
      }],
      activeTab: { label: 'name' }
    };
    collection = {
      markets: [{
        hidden: false,
        outcomes: [{ outcomeStatusCode: 'A' }]
      }],
      name: 'name'
    } as IMarketCollection;
    pubSubService = jasmine.createSpyObj('PubSubService', ['subscribe', 'API']);
    routerService = jasmine.createSpyObj('Router', ['navigateByUrl']);

    service = new TennisExtensionService(
      pubSubService,
      routerService
    );
    service.parentScope = parentScope;
    service.timeOutId = undefined;
    tennisConfig = {
      config: {
        request: {},
        tabs: {
          today: {
            marketTemplateMarketNameIntersects: ''
          }
        }
      }
    };
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('ngOnDestroy', () => {
    it('should clear timeout', () => {
      service.ngOnDestroy();
      expect(service.timeOutId).toBeUndefined();
    });
  });

  describe('eventMarkets', () => {
    it('should set event markets and subscribe', () => {
      spyOn<any>(service, 'updateMarketDisplay');
      service.eventMarkets(parentScope, tennisConfig);
      expect(service.parentScope).toEqual(parentScope);
      expect(service['updateMarketDisplay']).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('tennisExtension', undefined, jasmine.any(Function));
    });
  });

  it('updateDelay', fakeAsync(() => {
    spyOn(service as any, 'updateMarketDisplay');
    service['updateDelay'](updatedMarket);
    flush();
    expect(service['updateMarketDisplay']).toHaveBeenCalledTimes(1);
  }));

  describe('updateMarketDisplay', () => {
    beforeEach(() => {
      spyOn(service as any, 'displayMarket');
      spyOn(service as any, 'displayCollection');
    });

    it('should display market and collection', () => {
      service['updateMarketDisplay']({} as any);
      expect(service['displayMarket']).toHaveBeenCalledTimes(1);
      expect(service['displayCollection']).toHaveBeenCalledTimes(1);
    });

    it('should display market and collection (no market)', () => {
      service['updateMarketDisplay'](null);
      expect(service['displayMarket']).toHaveBeenCalledTimes(1);
      expect(service['displayCollection']).toHaveBeenCalledTimes(1);
    });

    it('shoud not display market and collection', () => {
      service.parentScope.marketsByCollection[0].name = 'Test';
      service['updateMarketDisplay'](null);
      expect(service['displayMarket']).not.toHaveBeenCalled();
      expect(service['displayCollection']).not.toHaveBeenCalled();
    });
  });

  describe('displayMarket', () => {
    beforeEach(() => {
      service['tennisConfig'] = {
        config: {
          request: { marketTemplateMarketNameIntersects: 'market' }
        }
      };
    });

    it('should set filteredMarketGroup', () => {
      const market: any = { name: 'market2' };
      service.parentScope.filteredMarketGroup = [market];
      service['displayMarket'](market);
      expect(service.parentScope.filteredMarketGroup).toEqual([]);
      expect(market.hidden).toBeTruthy();
    });

    it('should set filteredMarketGroup', () => {
      const market: any = { name: 'market2', marketStatusCode: 'S', outcomes: [{}] };
      service.parentScope.filteredMarketGroup = null;
      service['displayMarket'](market);
      expect(service.parentScope.filteredMarketGroup).toBeNull();
      expect(market.hidden).toBeTruthy();
    });

    it('should not set market.hidden', () => {
      service['tennisConfig'].config.request.marketTemplateMarketNameIntersects = '';
      const market: any = { name: '' };
      service['displayMarket'](market);
      expect(market.hidden).toBeUndefined();
    });
  });

  describe('displayCollection', () => {
    it('should display collection', () => {
      spyOn<any>(service, 'checkMarketsInCollection').and.returnValue(false);
      spyOn<any>(service, 'redirectToMainMarkets');
      service['displayCollection'](collection);
      expect(service['checkMarketsInCollection'](collection)).toBe(false);
      expect(service['redirectToMainMarkets']).toHaveBeenCalled();
    });

    it('should display collection Ladbrokes collection name', () => {
      service.parentScope.eventTabs[0].label = 'Game Markets';
      spyOn<any>(service, 'checkMarketsInCollection').and.returnValue(false);
      spyOn<any>(service, 'redirectToMainMarkets');
      service['displayCollection'](collection);
      expect(service['checkMarketsInCollection'](collection)).toBe(false);
      expect(service['redirectToMainMarkets']).toHaveBeenCalled();
    });

    it('should not display collection', () => {
      spyOn<any>(service, 'checkMarketsInCollection').and.returnValue(true);
      spyOn<any>(service, 'redirectToMainMarkets');

      collection.markets[0].hidden = true;
      service['displayCollection'](collection);
      expect(service['checkMarketsInCollection'](collection)).toBe(true);
      expect(service['redirectToMainMarkets']).not.toHaveBeenCalled();
    });

    it('should not update collection', () => {
      service.parentScope.eventTabs = [
        {
          hidden: false,
          label: 'Set',
          id: 'tab-main-markets',
          url: '/'
        }
      ];
      spyOn<any>(service, 'checkMarketsInCollection').and.returnValue(true);
      spyOn<any>(service, 'redirectToMainMarkets');

      service['displayCollection'](collection);
      expect(service['checkMarketsInCollection'](collection)).toBe(true);
      expect(service['redirectToMainMarkets']).not.toHaveBeenCalled();
    });
  });

  describe('checkMarketsInCollection', () => {
    it('should check if not all markets are hidden', () => {
      expect(service['checkMarketsInCollection'](collection)).toBe(true);
    });

    it('should check if not all markets are hidden', () => {
      collection.markets[0].hidden = true;
      expect(service['checkMarketsInCollection'](collection)).toBe(false);
    });

    it('should check if all one markets are hidden', () => {
      collection.markets[0].hidden = false;
      expect(service['checkMarketsInCollection'](collection)).toBe(true);
    });
  });

  describe('checkOutcomesInMarket', () => {
    it('should check if not all outcomes "suspended', () => {
      expect(service['checkOutcomesInMarket'](collection.markets[0])).toBe(true);
    });

    it('should check if all outcomes are suspended', () => {
      collection.markets[0].outcomes[0].outcomeStatusCode = 'S';
      expect(service['checkOutcomesInMarket'](collection.markets[0])).toBe(false);
    });
  });

  describe('redirectToMainMarkets', () => {
    it('should redirect to Main Markets if possible', () => {
      service['redirectToMainMarkets']();
      expect(routerService.navigateByUrl).toHaveBeenCalledWith('/');
    });

    it('should redirect to all markets', () => {
      parentScope.eventTabs[0].id = 'tab-all-markets';
      service['redirectToMainMarkets']();
      expect(routerService.navigateByUrl).toHaveBeenCalledWith('/');
    });

    it('should not redirect to main or all markets', () => {
      parentScope.eventTabs[0].id = '';
      service['redirectToMainMarkets']();
      expect(routerService.navigateByUrl).not.toHaveBeenCalled();
    });
  });
});
