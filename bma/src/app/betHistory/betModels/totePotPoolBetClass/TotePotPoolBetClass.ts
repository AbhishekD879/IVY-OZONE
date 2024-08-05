import * as _ from 'underscore';

import TotePoolBetBase from '../totePoolBetBase/TotePoolBetBaseClass';
import { BetHistoryMainService } from '../../services/betHistoryMain/bet-history-main.service';
import { CashoutMapIndexService } from '../../services/cashOutMapIndex/cashout-map-index.service';

import { UserService } from '@core/services/user/user.service';
import { LocaleService } from 'app/core/services/locale/locale.service';
import { TimeService } from 'app/core/services/time/time.service';
import { SbFiltersService } from 'app/sb/services/sbFilters/sb-filters.service';
import { IBetHistoryLeg, IBetHistoryPoolBet } from 'app/betHistory/models/bet-history.model';
import { IBetHistoryOutcome } from 'app/core/models/outcome.model';
import { CurrencyPipe } from '@angular/common';

export default class TotePotPoolBetClass extends TotePoolBetBase {
  isTotePotPoolBetBetModel: boolean;
  betTitle: string;
  toteMarketTitle: string;
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
    super(
      bet,
      betHistoryMainService,
      userService,
      locale,
      timeService,
      cashOutMapIndex,
      currencyPipe
    );
    /**
     * @private
     */
    this.isTotePotPoolBetBetModel = true;
    this.betTitle = locale.getString('bethistory.totepool');
    this.toteMarketTitle = this.poolType;
    this.orderOutcomes();
  }

  /**
   * Order outcome for each leg
   */
  orderOutcomes() {
    _.forEach(this.leg, (leg: IBetHistoryLeg) => {
      const legOutcomes: IBetHistoryOutcome[] = _.map(leg.part, part => part.outcome);
      this._setFavourites(legOutcomes);
      leg.orderedOutcomes = this.sbFiltersService.orderOutcomeEntities(legOutcomes, false, true, true);
    });
  }
}
