import TotePotPoolBet from './TotePotPoolBetClass';
import quadpotBet from './../../mocks/quadpotBet.mock';

describe('TotePotPoolBet', () => {
  let bet;
  let betHistoryMainService;
  let userService;
  let localeService;
  let timeService;
  let cashOutMapIndexService;
  let instance: TotePotPoolBet;
  let sbFiltersService;
  let currencyPipe;

  beforeEach(() => {
    bet = Object.assign({}, quadpotBet);

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

    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.callFake(x => x)
    };

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    instance = new TotePotPoolBet(
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
      expect(instance.isTotePotPoolBetBetModel).toBeTruthy();
      expect(instance.betTitle).toEqual('bethistory.totepool');
      expect(localeService.getString).toHaveBeenCalledWith('bethistory.totepool');
      expect(instance.toteMarketTitle).toEqual('Quadpot');

      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledTimes(4);
    });
  });

});
