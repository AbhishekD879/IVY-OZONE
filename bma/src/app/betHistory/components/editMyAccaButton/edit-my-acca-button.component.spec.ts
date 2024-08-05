import { EditMyAccaButtonComponent } from './edit-my-acca-button.component';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';

describe('EditMyAccaButtonComponent', () => {
  let component: EditMyAccaButtonComponent,
   editMyAccaService,
   cashoutPanelService,
   user,
   storageService,
   serviceClosureService

  beforeEach(() => {
    editMyAccaService = {
      hasSuspendedLegs: jasmine.createSpy('hasSuspendedLegs').and.returnValue(false),
      toggleBetEdit: jasmine.createSpy('toggleBetEdit'),
      showEditCancelMessage: jasmine.createSpy('showEditCancelMessage'),
      cancelActiveEdit: jasmine.createSpy('cancelActiveEdit'),
      isEmaInProcess: true,
      unsavedAcca: null,
      savedAccas: {},
      removeSavedAcca: jasmine.createSpy('removeSavedAcca')
    };
    cashoutPanelService = {
      setPartialState: jasmine.createSpy('setPartialState')
    };

    user = {
      editMyAccaTooltipSeen: false,
      set: jasmine.createSpy('user.set'),
      username: 'test'
    };

    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get')
    };

    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus')
    };
    
    component = new EditMyAccaButtonComponent(
      editMyAccaService,
      cashoutPanelService,
      user,
      storageService,
      serviceClosureService
    );

    component.bet = {
      isAccaEdit: false
    } as IBetHistoryBet;
  });

  it('constructor', () => {
    expect(component).toBeDefined();
    expect(component.tooltipSeen).toBeFalsy();
    expect(storageService.set).toHaveBeenCalledWith('tooltipsSeen', {'editMyAccaTooltipSeen-test': true});
  });

  describe('toggleBetEdit', () => {
    beforeEach(() => {
      component.bet = {
        id: 1,
        betId: 1,
        leg: [{}],
        resetCashoutSuccessState: jasmine.createSpy('resetCashoutSuccessState')
      } as any;
    });

    it('toggleBetEdit (should call toggleBetEdit)', () => {
      component.gtmLocation = 'cashout';
      component.bet.isAccaEdit = false;

      editMyAccaService.savedAccas = { 1: 'success'};
      component.toggleBetEdit();
      expect(editMyAccaService.toggleBetEdit).toHaveBeenCalledWith(component.bet, 'cashout');
      expect(editMyAccaService.unsavedAcca).toBeNull();
      expect(editMyAccaService.removeSavedAcca).toHaveBeenCalledWith('1');
      expect(component.bet.resetCashoutSuccessState).toHaveBeenCalled();
    });

    it('toggleBetEdit (should set unsaved acca)', () => {
      editMyAccaService.savedAccas = { 2: 'success'};
      component.bet.isAccaEdit = true;
      component.toggleBetEdit();
      expect(editMyAccaService.unsavedAcca).toEqual(component.bet);
      expect(component.bet.resetCashoutSuccessState).toHaveBeenCalled();
    });

    it('toggleBetEdit (partial cashout in progress)', () => {
      component.bet.isAccaEdit = false;
      component.bet.isPartialActive = true;
      component.toggleBetEdit();
      expect(cashoutPanelService.setPartialState).toHaveBeenCalledWith(component.bet, false);
      expect(component.bet.resetCashoutSuccessState).toHaveBeenCalled();
    });
  });

  describe('isEditButtonDisabled', () => {
    it('isEditButtonDisabled true', () => {
      component['editMyAccaService'].hasSuspendedLegs = jasmine.createSpy().and.returnValue(true);
      component.bet = {
        isAccaEdit: false
      } as any;
      expect(component.isEditButtonDisabled()).toEqual(true);
    });

    it('isEditButtonDisabled true#2', () => {
      component.bet = {
        isAccaEdit: true,
        inProgress: true,
        isPartialActive: true
      } as any;
      expect(component.isEditButtonDisabled()).toEqual(true);
    });

    it('isEditButtonDisabled true#3', () => {
      (<any>component['editMyAccaService']).isEmaInProcess = true;
      component.bet = {
        isAccaEdit: true,
        isPartialActive: false
      } as any;
      expect(component.isEditButtonDisabled()).toEqual(true);
    });

    it('isEditButtonDisabled false', () => {
      (<any>component['editMyAccaService']).isEmaInProcess = false;
      component['editMyAccaService'].hasSuspendedLegs = jasmine.createSpy().and.returnValue(false);
      component.bet = {
        isAccaEdit: false
      } as any;
      expect(component.isEditButtonDisabled()).toBeFalsy();
    });

    it('isEditButtonDisabled false#2', () => {
      (<any>component['editMyAccaService']).isEmaInProcess = false;
      component['editMyAccaService'].hasSuspendedLegs = jasmine.createSpy().and.returnValue(true);
      component.bet = {
        isAccaEdit: true,
        isPartialActive: false
      } as any;
      expect(component.isEditButtonDisabled()).toBeFalsy();
    });

    it('isEditButtonDisabled true when CASHOUT_SELN_SUSPENDED #2', () => {
      component.bet = {
        isAccaEdit: false,
        isPartialActive: false,
        cashoutValue: 'CASHOUT_SELN_SUSPENDED'
      } as any;
      expect(component.isEditButtonDisabled()).toBeTruthy();
    });

    it('isEditButtonDisabled true when legs has 2UpMarket', () => {
      component.bet = {
        isAccaEdit: false,
        isPartialActive: false,
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        leg:[{ eventEntity: {categoryId:'16'},
               part: [{eventMarketDesc: 'Both Teams to Score'}]
             },
             { eventEntity: { categoryId: '16' },
               part: [{ eventMarketDesc: 'Match Result1' }]
             }
            ]
      } as any;
      expect(component.isEditButtonDisabled()).toBeTruthy();
    });
  });

  describe('getButtonLabel', () => {
    it('should getButtonLabel(edit)', () => {
      expect(component.getButtonLabel()).toEqual('ema.editMyBet');
    });

    it('should getButtonLabel(cancel)', () => {
      component.bet.isAccaEdit = true;
      expect(component.getButtonLabel()).toEqual('ema.cancel');
    });
  });
});
