import { BetslipSelectionsDataService } from './betslip-selections-data';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('BetslipSelectionsDataService', () => {
  const quickBet = {
    outcomeId: '10'
  };

  const selection = {
    betsCount: 12,
    selections: [{
      price: {
        id: '10'
      },
      id: '12',
      params: {
        id: '10'
      },
      outcomes: [
        {
          id: '12',
        }
      ]
    }]
  };
  let service: BetslipSelectionsDataService;

  let pubsub;
  let storageService;

  const createService = () => {
    service = new BetslipSelectionsDataService(
      pubsub,
      storageService
    );
  };

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy('get').and.returnValue(selection.selections)
    };
    pubsub = {
      subscribe: jasmine.createSpy().and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        if (channel === pubsub.API.QUICKBET_OPENED) {
          channelFunction(quickBet);
        }
      }),
      API: pubSubApi
    };
  });

  it('should get selection from local storage', () => {
    createService();
    expect(storageService.get).toHaveBeenCalledWith('betSelections');
  });

  describe('QUICKBET OPENED', () => {
    beforeEach(() => {
      createService();
    });

    it('should subscribe', () => {
      service.subscribe();
      expect(pubsub.subscribe).toHaveBeenCalledWith('betSlipSelectionsData', pubsub.API.BETSLIP_SELECTIONS_UPDATE, jasmine.any(Function));
      expect(pubsub.subscribe).toHaveBeenCalledWith('betSlipSelectionsData', pubsub.API.QUICKBET_OPENED, jasmine.any(Function));
      expect(pubsub.subscribe).toHaveBeenCalledWith('betSlipSelectionsData', pubsub.API.QUICKBET_PANEL_CLOSE, jasmine.any(Function));
      expect(pubsub.subscribe).toHaveBeenCalledTimes(3);
    });

    it('should count selections', fakeAsync(() => {
      service.subscribe();
      tick();
      expect(service.count()).toBe(1);
    }));

    it('should contains id\'s', fakeAsync(() => {
      service.subscribe();
      tick();
      expect(service.contains(['10', '12'], ['10', '12'])).toBe(false);
      expect(service.contains(['10', '12'], ['1', '2'])).toBe(false);
      expect(service.contains(['1', '2'], ['10', '12'])).toBe(true);
    }));

    it('should get quickbet selection', fakeAsync(() => {
      service.subscribe();
      tick();
      expect(JSON.stringify(service.getQuickbetSelection())).toBe(JSON.stringify(quickBet));
    }));

    it('should get selections by outcome id', fakeAsync(() => {
      const selectionList = [{price: {priceType: 'SP'}}];
      service.subscribe();
      tick();
      expect(JSON.stringify(service.getSelectionsByOutcomeId('12'))).toBe(JSON.stringify([selection.selections[0]]));
      expect(JSON.stringify(service.getSelectionsByOutcomeId('10'))).toBe(JSON.stringify(selectionList));
      expect(JSON.stringify(service.getSelectionsByOutcomeId('11'))).toBe(JSON.stringify([]));
    }));
  });

  describe('QUICKBET PANEL CLOSE', () => {
    beforeEach(() => {
      pubsub = {
        subscribe: jasmine.createSpy().and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel !== pubsub.API.QUICKBET_OPENED) {
            channelFunction(quickBet);
          }
        }),
        API: pubSubApi
      };
      createService();
    });

    it('should get quickbet selection', fakeAsync(() => {
      service.subscribe();
      tick();
      expect(service.getQuickbetSelection()).toBe(null);
    }));
  });
});
