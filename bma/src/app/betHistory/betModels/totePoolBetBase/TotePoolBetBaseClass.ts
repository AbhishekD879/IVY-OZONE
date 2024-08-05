import PoolBetBase from '../poolBetBase/pool-bet-base.class';
import * as _ from 'underscore';
import { TimeService } from '@core/services/time/time.service';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { BetHistoryMainService } from '../../services/betHistoryMain/bet-history-main.service';
import { CashoutMapIndexService } from '../../services/cashOutMapIndex/cashout-map-index.service';
import { IBetHistoryLeg, IBetHistoryPoolBet } from '@app/betHistory/models/bet-history.model';
import { IBetHistoryOutcome } from '@core/models/outcome.model';
import { CurrencyPipe } from '@angular/common';

export default class TotePoolBetBaseClass extends PoolBetBase {
  isScoop6Pool: boolean;
  fixedEventLinked: boolean;
  isToteBet: boolean = true;
  isUkToteBet: boolean;
  externalPools = ['Scoop6', 'ITV7 Placepot','Placepot7'];
  constructor(
    bet: IBetHistoryPoolBet,
    betHistoryMainService: BetHistoryMainService,
    userService: UserService,
    locale: LocaleService,
    timeService: TimeService,
    cashOutMapIndex: CashoutMapIndexService,
    currencyPipe: CurrencyPipe,
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
    this.isScoop6Pool = this.externalPools.includes(this.poolType);
    this.isUkToteBet = this.bet.poolSource === 'TOTE';
  }

  /**
   * Add properties related to live updates
   */
  addLiveUpdatesProperties() {
    this._fillIdsProperties();
    this._updateCashoutMapIndex(this.leg);
  }

  /**
   * Changed bet ids from TOTE events to Fixed odds events
   * @param linkedEntitiesMap {Object} - map of tote events ids to linked fixed odds event ids
   */
  extendWithLinkedEvents(linkedEntitiesMap) {
    _.forEach(this.leg, leg => {
      _.forEach(leg.part, part => {
        const linkedOutcomeId = linkedEntitiesMap[part.outcome.id],
          linkedMarketId = linkedEntitiesMap[part.outcome.market.id],
          linkedObEventId = linkedEntitiesMap[part.outcome.event.id];

        part.outcome.event.toteEventId = part.outcome.event.id; // remember id of tote event (even if not overridden below)

        if (linkedOutcomeId) {
          part.outcome.id = linkedOutcomeId;
        }
        if (linkedMarketId) {
          part.outcome.market.id = linkedMarketId;
        }
        if (linkedObEventId) {
          part.outcome.event.id = linkedObEventId;
        }
      });
    });
    this.fixedEventLinked = true;
  }

  /**
   * Mark outcomes which are favourites
   * @param outcomes
   * @private
   */
  _setFavourites(outcomes: IBetHistoryOutcome[]): void {
    _.forEach(outcomes, (outcome: IBetHistoryOutcome) => {
      outcome.isFavourite = !!outcome.outcomeMeaningMinorCode;
    });
  }

  /**
   * Get Scoop 6 track name
   * TODO: Change this when OB will fix this on theis side
   * @param legName {Object} - leg entity
   * @returns {string}
   * @private
   */
  getScoop6TrackName(legName: string = ''): string {
    const trackNameWithRaceInfo = legName.split('Clone Race of ');
    if (trackNameWithRaceInfo.length !== 2) {
      return '';
    }
    const raceName = trackNameWithRaceInfo[1].split(' Race ');
    return raceName[0];
  }

  /**
   * Get race title
   * @param toteLeg - tote leg
   * @returns {string}
   * @private
   */
  getRaceTitle(toteLeg: IBetHistoryLeg): string {
    const formattedStartTime = this.timeService.formatByPattern(new Date(toteLeg.startTime), 'HH:mm'),
      trackName = this.isScoop6Pool ? this.getScoop6TrackName(toteLeg.name) : toteLeg.track;

    return `${formattedStartTime} ${trackName}`;
  }

}
