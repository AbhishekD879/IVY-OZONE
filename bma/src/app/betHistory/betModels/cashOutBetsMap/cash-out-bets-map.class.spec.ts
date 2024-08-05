import { CashOutBetsMap } from 'app/betHistory/betModels/cashOutBetsMap/cash-out-bets-map.class';
import { IBetDetail } from 'app/bpp/services/bppProviders/bpp-providers.model';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';

describe('CashOutBetsMap', () => {
  let model,
    cashOutMapIndex,
    betModelService,
    cashOutErrorMessage,
    betHistoryMainService,
    localeService;

  beforeEach(() => {
    cashOutMapIndex = {};
    betModelService = jasmine.createSpyObj('betModelServiceSpy', ['getBetTimeString', 'getPotentialPayout']);
    cashOutErrorMessage = jasmine.createSpyObj('cashOutErrorMessageSpy', ['getErrorMessage']);
    betHistoryMainService = {
      getSortCode: jasmine.createSpy('getSortCode'),
      getBetStatus: jasmine.createSpy('getBetStatus'),
      getBetReturnsValue: jasmine.createSpy('getBetReturnsValue').and.returnValue({})
    };

    localeService = {};

    model = new CashOutBetsMap(cashOutMapIndex, betModelService, cashOutErrorMessage, betHistoryMainService, localeService);
  });

  describe('createUpdatedCashoutBetsMap', () => {
    it('should return map of CashoutBet instances for BPP cashout flow', () => {
      const betsMap = model.createUpdatedCashoutBetsMap( [{ betId: 'b1' }, { betId: 'b2' }] as IBetDetail[], 'XYZ', '#', false);
      expect(betsMap).toEqual({ b1: jasmine.objectContaining({ betId: 'b1' }), b2: jasmine.objectContaining({ betId: 'b2' }) });
    });

    describe('for WS Cashout flow should return map of RegularBet instances', () => {
      let fromWs = true;
      it('when flag provided explicitly', () => {});
      it('(by default)', () => { fromWs = undefined; });
      afterEach(() => {
        const betsMap = model.createUpdatedCashoutBetsMap(
          [{ id: 1, betType: {}, leg: [], stake: {} }, { id: 2, betType: {}, leg: [], stake: {} }] as IBetHistoryBet[], 'XYZ', '#', fromWs);
        expect(betsMap).toEqual({ 1: jasmine.objectContaining({ id: 1 }), 2: jasmine.objectContaining({ id: 2 }) });
      });
    });

    afterEach(() => {
      expect(model.userCurrency).toEqual('XYZ');
      expect(model.userCurrencySymbol).toEqual('#');
    });
  });
});
