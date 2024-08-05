import { CashoutErrorMessageService } from '@app/betHistory/services/cashoutErrorMessageService/cashout-error-message.service';


describe('CashoutErrorMessageService', () => {
  let locale: any;
  let service: CashoutErrorMessageService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.callFake(value => value)
    } as any;

    service = new CashoutErrorMessageService(locale as any);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('getParticularErrorMessage', () => {
    it('should return default message if no param received', () => {
      expect(service.getParticularErrorMessage())
        .toEqual('bethistory.cashoutBet.cashoutUnvailable.default');
    });

    it('should return particular message if param received', () => {
      expect(service.getParticularErrorMessage('stringTest'))
        .toEqual('bethistory.cashoutBet.cashoutUnvailable.stringTest');
    });
  });

  describe('getErrorMessage', () => {
    it('should return default error for default case', () => {
      expect(service.getErrorMessage(undefined as any)).toEqual({
        msg: '',
        type: 'error'
      });
    });

    it('shoult return bet worth nothing error bet worth nothing case in cashoutStatus', () => {
      const betWorthNothingBet = {
        cashoutStatus: 'BET_WORTH_NOTHING',
        betType: 'BET_WORTH_NOTHING',
        currencySymbol: '$'
      } as any;
      expect(service.getErrorMessage(betWorthNothingBet)).toEqual({
        msg: 'bethistory.cashoutBet.cashoutUnvailable.betWorthNothing',
        type: 'error'
      });
    });

    it('shoult return default error if DB_ERROR case in cashoutValue and cashoutStatus is available', () => {
      const betWorthNothingBet = {
        cashoutStatus: 'BET_WORTH_NOTHING',
        cashoutValue: 'DB_ERROR',
        betType: 'BET_WORTH_NOTHING',
        currencySymbol: '$'
      } as any;
      expect(service.getErrorMessage(betWorthNothingBet)).toEqual({
        msg: '',
        type: 'error'
      });
    });

    it('shoult return bet worth nothing error bet worth nothing case in cashoutValue', () => {
      const betWorthNothingBet = {
        cashoutValue: '0.00',
        betType: 'BET_WORTH_NOTHING',
        currencySymbol: '$'
      } as any;
      expect(service.getErrorMessage(betWorthNothingBet)).toEqual({
        msg: 'bethistory.cashoutBet.cashoutUnvailable.betWorthNothing',
        type: 'error'
      });
    });

    it('shoult return default error if not bet worth nothing case in cashoutValue', () => {
      const betWorthNothingBet = {
        cashoutValue: 'NOT_BET_WORTH_NOTHING',
        betType: 'NOT_BET_WORTH_NOTHING',
        currencySymbol: '$'
      } as any;
      expect(service.getErrorMessage(betWorthNothingBet)).toEqual({
        msg: '',
        type: 'error'
      });
    });

    it('should set suspended message type and empty message for suspended cashoutValue', () => {
      expect(service.getErrorMessage({ cashoutValue: 'SELN_SUSP', cashoutStatus: 'SELN_SUSP'} as any)).toEqual({
        msg: '',
        type: 'suspended'
      } as any);
    });
  });
});


