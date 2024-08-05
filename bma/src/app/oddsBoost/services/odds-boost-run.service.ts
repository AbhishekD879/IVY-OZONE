
import { Injectable, Injector } from '@angular/core';

import { CommandService } from '@core/services/communication/command/command.service';
import { OddsBoostService } from '@oddsBoostModule/services/odds-boost.service';

import { IBetInfo } from '@betslip/services/bet/bet.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { Bet } from '@betslip/services/bet/bet';

@Injectable()
export class OddsBoostRunService {
  constructor(
    private commandService: CommandService,
    private injector: Injector
  ) {}

  run(): void {
    this.commandService.register(this.commandService.API.ODDS_BOOST_INIT,
      tokens => this.oddsBoostService.init(tokens).toPromise());
    this.commandService.register(this.commandService.API.ODDS_BOOST_TOKENS_SHOW_POPUP,
      () => this.oddsBoostService.showTokensInfoDialog().toPromise());
    this.commandService.register(this.commandService.API.GET_ODDS_BOOST_ACTIVE,
      () => Promise.resolve(this.oddsBoostService.isBoostActive()));
      this.commandService.register(this.commandService.API. GET_ODDS_BOOST_ACTIVE_FROM_STORAGE,
        () => Promise.resolve(this.oddsBoostService.getBoostActiveFromStorage()));
    this.commandService.register(this.commandService.API.ODDS_BOOST_SHOW_FB_DIALOG,
      (selectOddsBoostFirst: boolean, type: string) => this.oddsBoostService.showOddsBoostFreeBetDialog(selectOddsBoostFirst, type));
    this.commandService.register(this.commandService.API.ODDS_BOOST_SET_MAX_VAL,
      (value: string) => this.oddsBoostService.setMaxBoostValue(value));
    this.commandService.register(this.commandService.API.ODDS_BOOST_OLD_PRICE,
      (betslipStake: IBetInfo, type: string) => this.oddsBoostService.getOldPriceFromBetslipStake(betslipStake, type));
    this.commandService.register(this.commandService.API.ODDS_BOOST_NEW_PRICE,
      (betslipStake: IBetInfo, type: string) => this.oddsBoostService.getNewPriceFromBetslipStake(betslipStake, type));
    this.commandService.register(this.commandService.API.ODDS_BOOST_OLD_QB_PRICE,
      (selection: IQuickbetSelectionModel) => this.oddsBoostService.getOldPriceFromQuickBet(selection));
    this.commandService.register(this.commandService.API.ODDS_BOOST_NEW_QB_PRICE,
      (selection: IQuickbetSelectionModel) => this.oddsBoostService.getNewPriceFromQuickBet(selection));
    this.commandService.register(this.commandService.API.ODDS_BOOST_SHOW_SP_DIALOG,
      () => this.oddsBoostService.showOddsBoostSpDialog());
    this.commandService.register(this.commandService.API.ODDS_BOOST_SETTLE_TOKEN,
      (tokens: Bet[]) => this.oddsBoostService.settleOddsBoostTokens(tokens).toPromise());
    this.commandService.register(this.commandService.API.ODDS_BOOST_MAX_STAKE_EXCEEDED,
      (stake: number) => this.oddsBoostService.isMaxStakeExceeded(stake));
    this.commandService.register(this.commandService.API.GET_ODDS_BOOST_TOKENS,
      (isPageRefresh?: boolean) => this.oddsBoostService.getOddsBoostTokens(isPageRefresh).toPromise());
  }

  private get oddsBoostService(): OddsBoostService {
    return this.injector.get(OddsBoostService);
  }

  private set oddsBoostService(value: OddsBoostService){}
}
