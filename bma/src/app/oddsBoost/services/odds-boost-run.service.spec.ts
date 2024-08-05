import { of as observableOf } from 'rxjs';
import { commandApi } from '@app/core/services/communication/command/command-api.constant';
import { OddsBoostService } from './odds-boost.service';
import { OddsBoostRunService } from './odds-boost-run.service';

describe('OddsBoostRunService', () => {
  let commandService;
  let injector;
  let service;

  beforeEach(() => {
    commandService = {
      API: commandApi,
      register: jasmine.createSpy().and.callFake((p1, cb) => {
        if (typeof cb === 'function') { cb(); }
      })
    };
    injector = {
      get: jasmine.createSpy().and.returnValue({
        init: () => observableOf(null),
        showTokensInfoDialog: () => observableOf([]),
        isBoostActive: () => {},
        getBoostActiveFromStorage: () => {},
        showOddsBoostFreeBetDialog: () => {},
        setMaxBoostValue: () => {},
        getOldPriceFromBetslipStake: () => {},
        getNewPriceFromBetslipStake: () => {},
        getOldPriceFromQuickBet: () => {},
        getNewPriceFromQuickBet: () => {},
        showOddsBoostSpDialog: () => {},
        settleOddsBoostTokens: () => observableOf([]),
        isMaxStakeExceeded: () => {},
        getOddsBoostTokens: () => observableOf([])
      })
    };

    service = new OddsBoostRunService(
      commandService,
      injector
    );
  });

  it('run', () => {
    service.run();

    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_INIT, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_TOKENS_SHOW_POPUP, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.GET_ODDS_BOOST_ACTIVE, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.GET_ODDS_BOOST_ACTIVE_FROM_STORAGE, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_SHOW_FB_DIALOG, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_SET_MAX_VAL, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_OLD_PRICE, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_NEW_PRICE, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_OLD_QB_PRICE, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_NEW_QB_PRICE, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_SHOW_SP_DIALOG, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_SETTLE_TOKEN, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_MAX_STAKE_EXCEEDED, jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      commandService.API.GET_ODDS_BOOST_TOKENS, jasmine.any(Function)
    );
  });

  it('get oddsBoostService', () => {
    expect(service.oddsBoostService).toBeTruthy();
    expect(injector.get).toHaveBeenCalledWith(OddsBoostService);
  });
});
