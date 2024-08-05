import { BetslipDataService } from './betslip-data.service';

describe('BetslipDataService', () => {
  let service: BetslipDataService;
  let storageService;

  beforeEach(() => {
    service = new BetslipDataService(storageService);
    storageService = {
      get: jasmine.createSpy('get')
    };
    service = new BetslipDataService(storageService);
  });

  it('get/set placedBets', () => {
    const data: any = [{}];
    service.placedBets = data;
    expect(service.placedBets).toBe(data);
  });

  it('get/set readBets', () => {
    const data: any = [{}];
    service.readBets = data;
    expect(service.readBets).toBe(data);
  });

  it('setDefault', () => {
    service.setDefault();
    expect(service['data']).toEqual({ bets: [] });
  });

  it('getActiveSinglesIds', () => {
    service.bets = [{
      params:{
        lottoData:{lottoData :{isLotto : true}}
      },
      info: () => null
    }, {
      params:{
        lottoData: undefined
      },
      info: () => ({
        eventIds: { outcomeIds: [1] },
        type: 'SGL',
        Bet: { price: { type: 'LP' } }
      })
    }, {
      params:{
        lottoData:{lottoData :{isLotto : true}}
      },
      info: () => ({
        eventIds: { outcomeIds: [2, 3] },
        type: 'SGL',
        Bet: { price: { type: 'DIVIDEND' } }
      })
    }] as any;
    expect(service.getActiveSinglesIds()).toEqual([1]);
  });

  it('checkPrices', () => {
    service.bets = [{
      info: () => ({
        price: { props: {} }
      }),
      stake: {},
      price: { props: {} }
    }, {
      info: () => ({
        price: { priceNum: 3, priceDen: 4 }
      }),
      stake: {},
      freeBet: { id: 1 },
      price: {
        props: { priceNum: 1, priceDen: 2 }
      }
    }, {
      info: () => ({
        price: { priceNum: 3, priceDen: 4 }
      }),
      stake: {},
      freeBet: { id: 1 },
      price: {
        props: { priceNum: 3, priceDen: 2 }
      }
    }] as any;

    service.checkPrices();

    expect(service.bets[1].price.props.priceNum).toBe(service.bets[1].info().price.priceNum);
    expect(service.bets[1].price.props.priceDen).toBe(service.bets[1].info().price.priceDen);
    expect(service.bets[2].price.props.priceDen).toBe(service.bets[2].info().price.priceDen);
  });

  it('clearMultiplesStakes', () => {
    const clearUserData = jasmine.createSpy('clearUserData');
    service.bets = [{
      type: 'SGL', clearUserData
    }, {
      type: 'DBL', clearUserData
    }] as any;

    service.clearMultiplesStakes();

    expect(clearUserData).toHaveBeenCalledTimes(1);
  });

  describe('containsRegularBets', ()=>{
    it('contains bets object', () => {
      service.bets = [];
      expect(service.containsRegularBets()).toBeFalsy();
      service.bets = [{}] as any;
      expect(service.containsRegularBets()).toBeTruthy();
    });
    it('returns true if storage bets exist', ()=>{
      storageService.get.and.returnValue([{}] as any);
      expect(service.containsRegularBets()).toBeTruthy();
    });
    it('returns false if storage bets is empty', ()=>{
      storageService.get.and.returnValue([] as any);
      expect(service.containsRegularBets()).toBeFalsy();
    });
  });

  it('storeBets', () => {
    const res = service.storeBets({
      bets: [{ isMocked: true }, {}, {}]
    } as any);
    expect(res.length).toBe(3);
  });
});
