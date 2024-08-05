import { BetLiveUpdateHistory } from './bet-live-update-history';

describe('BetLiveUpdateHistory', () => {
  let bet;
  let betInfo = {};
  let betHistory: BetLiveUpdateHistory;

  beforeEach(() => {
    bet = {
      info: () => betInfo
    };

    betHistory = new BetLiveUpdateHistory(bet);
  });

  it('update', () => {
    const payload: any = { type: 'MESSAGE' };
    betHistory.update(payload);
    expect(betHistory['history'].length).toBe(1);
  });

  describe('isStarted', () => {
    it('should return false (not started)', () => {
      betInfo = {};
      expect(betHistory.isStarted()).toBeFalsy();
    });

    it('should return false (already started)', () => {
      betInfo = { error: 'EVENT_STARTED' };
      betHistory['prevState'].error = 'EVENT_STARTED';
      expect(betHistory.isStarted()).toBeFalsy();
    });

    it('should return true', () => {
      betInfo = { error: 'EVENT_STARTED' };
      betHistory['prevState'].error = null;
      expect(betHistory.isStarted()).toBeTruthy();
    });
  });

  describe('isSuspended', () => {
    it('should return false (not suspendend)', () => {
      betInfo = {};
      expect(betHistory.isSuspended()).toBeFalsy();
    });

    it('should return false (already suspended)', () => {
      betInfo = { isSuspended: true };
      betHistory['prevState'].isSuspended = true;
      expect(betHistory.isSuspended()).toBeFalsy();
    });

    it('should return true', () => {
      betInfo = { isSuspended: true };
      betHistory['prevState'].isSuspended = false;
      expect(betHistory.isSuspended()).toBeTruthy();
    });
  });

  describe('isPriceChanged', () => {
    it('should return false (starting price)', () => {
      betInfo = {
        price: { priceType: 'SP' }
      };
      expect(betHistory.isPriceChanged()).toBeFalsy();
    });

    it('should return false (prices not changed)', () => {
      betInfo = {
        price: { priceType: 'LP', priceNum: '1', priceDen: '2' }
      };
      betHistory['prevState'] = {
        price: { priceType: 'LP', priceNum: '1', priceDen: '2' }
      };
      expect(betHistory.isPriceChanged()).toBeFalsy();
    });

    it('should return true (numerator changed)', () => {
      betInfo = {
        price: { priceType: 'LP', priceNum: '1', priceDen: '2' }
      };
      betHistory['prevState'] = {
        price: { priceType: 'LP', priceNum: '11', priceDen: '2' }
      };
      expect(betHistory.isPriceChanged()).toBeTruthy();
    });

    it('should return true (denominator changed)', () => {
      betInfo = {
        price: { priceType: 'LP', priceNum: '1', priceDen: '2' }
      };
      betHistory['prevState'] = {
        price: { priceType: 'LP', priceNum: '1', priceDen: '22' }
      };
      expect(betHistory.isPriceChanged()).toBeTruthy();
    });
  });

  describe('isPriceChangedAndMarketUnsuspended', () => {
    it('should return false (no market update)', () => {
      betHistory['history'] = [{
        payload: {
          subChannel: { type: 'sPRICE' }
        }
      }] as any;
      expect(betHistory.isPriceChangedAndMarketUnsuspended()).toBeFalsy();
    });

    it('should return false (no price update)', () => {
      betHistory['history'] = [{
        payload: {
          subChannel: { type: 'sEVMKT' }
        }
      }] as any;
      expect(betHistory.isPriceChangedAndMarketUnsuspended()).toBeFalsy();
    });

    it('should return false (time difference too big)', () => {
      betHistory['history'] = [{
        payload: {
          subChannel: { type: 'sEVMKT' }
        },
        time: 2000
      }, {
        payload: {
          subChannel: { type: 'sPRICE' }
        },
        time: 100
      }] as any;
      expect(betHistory.isPriceChangedAndMarketUnsuspended()).toBeFalsy();
    });

    it('should return false (market is suspended)', () => {
      betHistory['history'] = [{
        payload: {
          subChannel: { type: 'sEVMKT' },
          message: { status: 'S' }
        },
        time: 200
      }, {
        payload: {
          subChannel: { type: 'sPRICE' }
        },
        time: 150
      }] as any;
      expect(betHistory.isPriceChangedAndMarketUnsuspended()).toBeFalsy();
    });

    it('should return true', () => {
      betHistory['history'] = [{
        payload: {
          subChannel: { type: 'sEVMKT' },
          message: { status: 'A' }
        },
        time: 200
      }, {
        payload: {
          subChannel: { type: 'sPRICE' }
        },
        time: 150
      }] as any;
      expect(betHistory.isPriceChangedAndMarketUnsuspended()).toBeTruthy();
    });
  });
});
