import { QuickDepositService } from '@betslip/services/quickDeposit/quick-deposit.service';
import { UserService } from '@core/services/user/user.service';

describe('QuickDepositService', () => {
  let service: QuickDepositService;

  let userService;

  beforeEach(() => {
    userService = {
      status: true
    };

    service = new QuickDepositService(userService);
  });

  it('should create QuickDepositService', () => {
    expect(service).toBeTruthy();
  });

  describe('checkQuickDeposit', () => {
    it('should set field showQuickDepositForm as FALSE if freebet used and balance > stake', () => {
      const result = service.checkQuickDeposit(5, 1, 5, 1, false, false, false);
      expect(result.showQuickDepositForm).toEqual(false);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });

    it('should set field showQuickDepositForm as FALSE', () => {
      const result = service.checkQuickDeposit(5, 1, 5, 1, false, false, false);
      expect(result.showQuickDepositForm).toEqual(false);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });

    it('should set field showQuickDepositForm as FALSE if user ballance === null', () => {
      const result = service.checkQuickDeposit(5, 0, null, 1, false, false, false);
      expect(result.showQuickDepositForm).toEqual(false);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });

    it('should set field showQuickDepositForm as true if balance is not Defined', () => {
      const result = service.checkQuickDeposit(5, 1, undefined, 1, false, false, false);
      expect(result.showQuickDepositForm).toEqual(true);
      expect(result.neededAmountForPlaceBet).toEqual('5.00');
    });

    it('should set field showQuickDepositForm as if user balance < stake', () => {
      const result = service.checkQuickDeposit(null, 0, -1, 1, false, false, false);
      expect(result.showQuickDepositForm).toEqual(true);
      expect(result.neededAmountForPlaceBet).toEqual('0.00');
    });

    it('should set field showQuickDepositForm false if selection is suspended', () => {
      const result = service.checkQuickDeposit(null, 0, null, 0, true, false, true);
      expect(result.showQuickDepositForm).toEqual(true);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });

    it('should set field showQuickDepositForm true if showQuickDepositForm passed', () => {
      const result = service.checkQuickDeposit(null, 0, null, 0, true, false, true);
      expect(result.showQuickDepositForm).toEqual(true);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });

    it('should set field showQuickDepositForm as if user balance < stake', () => {
      const result = service.checkQuickDeposit(null, 0, null, 0, false, false);
      expect(result.showQuickDepositForm).toEqual(false);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });


    it('should set field showQuickDepositForm as if user balance < stake(when no isSelectionSuspended parameter were found)', () => {
      const result = service.checkQuickDeposit(null, 0, null, 0, false);
      expect(result.showQuickDepositForm).toEqual(false);
      expect(result.neededAmountForPlaceBet).toEqual(0);
    });

    it('should set field showQuickDepositForm as true if stake is bigger than user balance', () => {
      const result = service.checkQuickDeposit(5, 1, 2, 1, false, false, false);
      expect(result.showQuickDepositForm).toEqual(true);
      expect(result.neededAmountForPlaceBet).toEqual('3.00');
    });
  });

  describe('#isUserAbleToDeposit', () => {
    it('should return false when userBalanceAvailable is false', () => {
      const result = service['isUserAbleToDeposit'](false, 1, true);
      expect(result).toBeFalsy();
    });

    it('should return false when bsSelections is zero', () => {
      const result = service['isUserAbleToDeposit'](true, 0, true);
      expect(result).toBeFalsy();
    });

    it('should return false when placeBetsPending is true', () => {
      const result = service['isUserAbleToDeposit'](true, 1, true);
      expect(result).toBeFalsy();
    });

    it('should return false when user status is false', () => {
      service = new QuickDepositService({ status: false } as UserService);
      const result = service['isUserAbleToDeposit'](true, 1, false);
      expect(result).toBeFalsy();
    });

    it('should return true', () => {
      const result = service['isUserAbleToDeposit'](true, 1, false);
      expect(result).toBeTruthy();
    });
  });
});
