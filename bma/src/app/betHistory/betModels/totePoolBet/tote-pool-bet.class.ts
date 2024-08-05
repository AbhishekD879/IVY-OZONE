import { CurrencyPipe } from '@angular/common';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { TimeService } from '@core/services/time/time.service';
import { IBetHistoryOutcome, IOutcome } from '@core/models/outcome.model';

import { betHistoryConstants } from '@app/betHistory/constants/bet-history.constant';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import { IBetHistoryPoolBet } from '@app/betHistory/models/bet-history.model';
import TotePoolBetBase from '@app/betHistory/betModels/totePoolBetBase/TotePoolBetBaseClass';

import { SbFiltersService } from '@app/sb/services/sbFilters/sb-filters.service';

export default class TotePoolBet extends TotePoolBetBase {
  isTotePoolBetBetModel: boolean;
  betTitle: string;
  poolOutcomes: IBetHistoryOutcome[];
  toteMarketTitle: string;
  raceNumberTitle: string;
  isOrderedBet: boolean;
  orderedOutcomes: IOutcome[];

  constructor(
    bet: IBetHistoryPoolBet,
    betHistoryMainService: BetHistoryMainService,
    userService: UserService,
    locale: LocaleService,
    timeService: TimeService,
    cashOutMapIndex: CashoutMapIndexService,
    currencyPipe: CurrencyPipe,
    public sbFiltersService: SbFiltersService
  ) {
    super(bet,
      betHistoryMainService,
      userService,
      locale,
      timeService,
      cashOutMapIndex,
      currencyPipe);
    /**
     * @private
     */
    this.isTotePoolBetBetModel = true;
    this.betTitle = locale.getString('bethistory.single');
    this.poolOutcomes = _.pluck(this.leg[0].part, 'outcome');
    this.toteMarketTitle = locale.getString('bethistory.toteMarketTitle', { poolType: this.poolType });
    this.raceNumberTitle = locale.getString('bethistory.toteRaceTitle', { raceNumber: this.leg[0].raceNumber });
    this.isOrderedBet = this._checkIfOrderMatter();
    this._setFavourites(this.poolOutcomes);
    /**
     * If outcomes aren't already ordered, they should be ordered by Runner Number
     */
    if (this.isOrderedBet) {
      this.orderedOutcomes = this.poolOutcomes;
    } else {
      this.orderedOutcomes = this.sbFiltersService.orderOutcomeEntities(this.poolOutcomes, false, true, true);
    }
  }

  /**
   * Check if should show runner number
   * Note: Bet is ordered for only Stright Exacta and Stright Trifecta Tote bet types
   * @private
   */
  _checkIfOrderMatter(): boolean {
    const isExactaBet = this.poolType === betHistoryConstants.BET_TYPES.TOTE_EXACTA,
      isTrifectaBet = this.poolType === betHistoryConstants.BET_TYPES.TOTE_TRIFECTA,
      isStrightExactaBet = isExactaBet && +this.lines === 1,
      isStrightTrifectaBet = isTrifectaBet && +this.lines === 1;

    return isStrightExactaBet || isStrightTrifectaBet;
  }
}
