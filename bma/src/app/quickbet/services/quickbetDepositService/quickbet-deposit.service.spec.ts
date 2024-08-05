import { QuickbetDepositService } from './quickbet-deposit.service';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('QuickbetDepositService', () => {
  let quickbetNotificationService;
  let userService;
  let pubSubService;
  let service;

  beforeEach(() => {
    userService = {
      status: true,
      sportBalance: 5,
      getUserDepositMessage: jasmine.createSpy('getUserDepositMessage').and.returnValue('foo'),
      getUserDepositNeededAmount: jasmine.createSpy('getUserDepositNeededAmount').and.returnValue('95.00')
    };

    quickbetNotificationService = {
      clear: jasmine.createSpy('clear'),
      saveErrorMessage: jasmine.createSpy('saveErrorMessage'),
      config: {
        location: 'quick-deposit'
      }
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    createService();
  });

  function createService() {
    service = new QuickbetDepositService(quickbetNotificationService, userService, pubSubService);
  }

  describe('Testing init', () => {
    let successHandler,
      errorHandler;

    beforeEach(() => {
      successHandler = jasmine.createSpy('successHandler');
      errorHandler = jasmine.createSpy('errorHandler');
    });

    it('!this.user.status', () => {
      userService.status = false;
      expect(service.init(false)).toBe(false);
    });


    it('Should execute pubSubService with publish PAYMENT_ACCOUNTS_PASSED', () => {
      service.init(true);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.PAYMENT_ACCOUNTS_PASSED);
    });


    it('Should Not execute pubSubService with publish PAYMENT_ACCOUNTS_PASSED', () => {
      service.init(false);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubApi.PAYMENT_ACCOUNTS_PASSED);
    });

    it('Should Not execute pubSubService with publish PAYMENT_ACCOUNTS_PASSED(default isBeforePlaceBet)', () => {
      service.init();
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubApi.PAYMENT_ACCOUNTS_PASSED);
    });

    it('Should clear deposit message and quickDepositModel when stake is too low and user either select input or ' +
      'select other bet value', () => {
      quickbetNotificationService.config = { errorCode: 'STAKE_TOO_LOW' };
      service.update(2, true);

      expect(quickbetNotificationService.saveErrorMessage).not.toHaveBeenCalled();
      expect(quickbetNotificationService.clear).toHaveBeenCalledWith('quick-deposit');
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
        neededAmountForPlaceBet: '',
      }));
    });
  });

  describe('Testing update method', () => {
    it('Should update info panel and extend quickDepositModel', () => {
      service.update(100, false);
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalled();
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(jasmine.any(String), 'deposit', 'quick-deposit');
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
        neededAmountForPlaceBet: '95.00',
      }));
    });

    it('Should clear deposit message and quickDepositModel when user has enough amount to place bet', () => {
      quickbetNotificationService.config = { location: 'quick-deposit' };
      service.update(2, true);

      expect(quickbetNotificationService.saveErrorMessage).not.toHaveBeenCalled();
      expect(quickbetNotificationService.clear).toHaveBeenCalledWith('quick-deposit');
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
        neededAmountForPlaceBet: '',
      }));
    });

    it('Should not clear deposit message when current message is not deposit related', () => {
      quickbetNotificationService.config = { location: 'bet-status' };
      service.update(2, true);

      expect(quickbetNotificationService.saveErrorMessage).not.toHaveBeenCalled();
      expect(quickbetNotificationService.clear).not.toHaveBeenCalled();
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
        neededAmountForPlaceBet: '',
      }));
    });

    it('Should extend quickDepositModel but doesn"t update deposit error message', () => {
      service.update(10, true);

      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalled();
      expect(userService.getUserDepositMessage).toHaveBeenCalled();
      expect(userService.getUserDepositNeededAmount).toHaveBeenCalledWith(20, false);
      expect(quickbetNotificationService.clear).not.toHaveBeenCalled();
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
        neededAmountForPlaceBet: '95.00',
      }));
    });

    it('Should extend quickDepositModel but doesn"t update deposit error message(isEachWay was not passed)', () => {
      service.update(10);

      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalled();
      expect(quickbetNotificationService.clear).not.toHaveBeenCalled();
      expect(userService.getUserDepositNeededAmount).toHaveBeenCalledWith(10, false);
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
        neededAmountForPlaceBet: '95.00',
      }));
    });

    it('Should call getUserDepositMessage', () => {
      service.update(10, false);

      expect(userService.getUserDepositMessage).toHaveBeenCalledWith(10, false);
      expect(userService.getUserDepositNeededAmount).toHaveBeenCalledWith(10, false);
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith('foo', 'deposit', 'quick-deposit');
    });
  });

  it('Should Update info panel and extend quickDepositModel -- without isEachWay', () => {
    service.update(100, undefined);
    expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(jasmine.any(String), 'deposit', 'quick-deposit');
    expect(service.quickDepositModel).toEqual(jasmine.objectContaining({
      neededAmountForPlaceBet: '95.00',
    }));
  });

  it('Should Update info panel and extend quickDepositModel with isEachWay', () => {
    service.update(50, true);
    expect(userService.getUserDepositNeededAmount).toHaveBeenCalledWith(100, false);
    expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(jasmine.any(String), 'deposit', 'quick-deposit');
  });

  it('!this.user.status && !isNeededAmountForPlaceBet)', () => {
    userService.status = false;
    service.update(100, false);
    expect(quickbetNotificationService.clear).toHaveBeenCalled();
    expect(service.quickDepositModel).toEqual(jasmine.objectContaining({ neededAmountForPlaceBet: '' }));
  });

  it('!this.user.status && !isNeededAmountForPlaceBet with isEachWay)', () => {
    userService.status = false;
    service.update(100, true);
    expect(quickbetNotificationService.clear).toHaveBeenCalled();
    expect(service.quickDepositModel).toEqual(jasmine.objectContaining({ neededAmountForPlaceBet: '' }));
  });

  it('Should clear quickDeposit model', () => {
      service.clearQuickDepositModel();
      expect(service.quickDepositModel).toEqual(jasmine.objectContaining({ neededAmountForPlaceBet: undefined }));
  });
});
