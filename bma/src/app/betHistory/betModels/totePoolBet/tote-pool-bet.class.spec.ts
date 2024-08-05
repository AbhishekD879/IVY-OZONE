import TotePoolBet from './tote-pool-bet.class';
import trifectaBet from './../../mocks/trifectaBet.mock';

describe('TotePoolBet', () => {
  let bet;
  let betHistoryMainService;
  let userService;
  let localeService;
  let timeService;
  let cashOutMapIndexService;
  let instance: TotePoolBet;
  let sbFiltersService;
  let currencyPipe;

  beforeEach(() => {
    bet = Object.assign({}, trifectaBet);

    betHistoryMainService = {
      getBetStatus: jasmine.createSpy('getBetStatus').and.returnValue('pending')
    };
    userService = {
      currencySymbol: '$'
    };
    localeService = {
      getString: jasmine.createSpy('locale.getString').and.callFake(x => x)
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('15:10')
    };
    cashOutMapIndexService = {
      create: jasmine.createSpy('cashOutMapIndexService.create')
    };

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.callFake(x => x)
    };

    instance = new TotePoolBet(
      bet,
      betHistoryMainService,
      userService,
      localeService,
      timeService,
      cashOutMapIndexService,
      currencyPipe,
      sbFiltersService
    );
  });

  describe('constructor', () => {
    it('should properly init class with ordered bet case', () => {
      expect(instance.isTotePoolBetBetModel).toBeTruthy();
      expect(instance.betTitle).toEqual('bethistory.single');
      expect(localeService.getString).toHaveBeenCalledWith('bethistory.single');
      expect(instance.toteMarketTitle).toEqual('bethistory.toteMarketTitle');
      expect(localeService.getString).toHaveBeenCalledWith('bethistory.toteMarketTitle', {
        poolType: 'Trifecta'
      });
      expect(instance.raceNumberTitle).toEqual('bethistory.toteRaceTitle');
      expect(localeService.getString).toHaveBeenCalledWith('bethistory.toteRaceTitle', {
        raceNumber: '3'
      });
      expect(sbFiltersService.orderOutcomeEntities).not.toHaveBeenCalled();
    });
    it('should properly init class with non ordered bet case', () => {
      bet.poolType = 'Win';
      instance = new TotePoolBet(
        bet,
        betHistoryMainService,
        userService,
        localeService,
        timeService,
        cashOutMapIndexService,
        currencyPipe,
        sbFiltersService
      );
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith(jasmine.anything(), false, true, true);
    });
  });

  describe('_checkIfOrderMatter', () => {
    it('should return true for Stright Trifecta bet', () => {
      instance.poolType = 'Trifecta';
      instance.lines = 1;
      expect(instance._checkIfOrderMatter()).toEqual(true);
    });
    it('should return true for Stright Exacta bet', () => {
      instance.poolType = 'Exacta';
      instance.lines = 1;
      expect(instance._checkIfOrderMatter()).toEqual(true);
    });
    it('should return false for generic Trifecta bet', () => {
      instance.poolType = 'Trifecta';
      instance.lines = 3;
      expect(instance._checkIfOrderMatter()).toEqual(false);
    });
    it('should return false for generic Execta bet', () => {
      instance.poolType = 'Exacta';
      instance.lines = 3;
      expect(instance._checkIfOrderMatter()).toEqual(false);
    });
    it('should return false for generic Win/place or other bets', () => {
      instance.poolType = 'Win';
      instance.lines = 5;
      expect(instance._checkIfOrderMatter()).toEqual(false);
    });
  });
});
