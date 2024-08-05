import * as _ from 'underscore';

import {
  IBetHistoryBet, IBetHistoryLeg,
  IBetType, IBetHistoryStake
} from '../../models/bet-history.model';
import { RegularBetBase } from '../regularBetBase/regular-bet-base.class';
import { IBetTermsChange } from 'app/bpp/services/bppProviders/bpp-providers.model';
import { CashoutErrorMessageService } from '../../services/cashoutErrorMessageService/cashout-error-message.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { CHANNEL } from '@shared/constants/channel.constant';

export class RegularBet extends RegularBetBase {
  legType: string;
  stake: number;
  stakePerLine: string;
  sortType: string;
  betTermsChange: IBetTermsChange[];

  betGroupId?: string;
  betGroupOrder?: string;
  betGroupType?: string;

  winnings: { value: string }[];
  livePriceWinnings?: { value: string}[];

  bybType?: string;
  source?: string;
  contestId?: string;

  constructor(bet: IBetHistoryBet,
              public betModelService,
              public currency,
              public currencySymbol,
              public cashOutMapIndex,
              private betHistoryMainService,
              private localeService: LocaleService,
              public cashOutErrorMessage: CashoutErrorMessageService,
              public cashoutConstants) {
    super(bet, betModelService, currency, currencySymbol, cashOutMapIndex, cashOutErrorMessage);

    this.setBetProperties(bet);

    this.initializeLegs(bet);

    this.setCashoutProperties(bet);

    this.setBybType(bet);
  }

  setBetProperties(bet: IBetHistoryBet): void {
    this.betId = bet.id.toString();
    this.betType = (bet.betType as IBetType).code;
    this.legType = bet.leg[0] ? bet.leg[0].legType.code : null;
    this.stakePerLine = (bet.stake as IBetHistoryStake).stakePerLine;
    this.stake = (bet.stake as IBetHistoryStake).value;
    this.tokenValue = (bet.stake as IBetHistoryStake).tokenValue;
    this.tokenType = bet.freebetTokens?.freebetToken?.freebetOfferCategories?.freebetOfferCategory;
    this.sortType = [CHANNEL.fiveASide, CHANNEL.byb].includes(bet.source) ? '' : this.betHistoryMainService.getSortCode(this.leg);
    this.totalStatus = this.betHistoryMainService.getBetStatus(this);
    this.potentialPayout = this.betHistoryMainService.getBetReturnsValue(this, this.totalStatus).value;
  }

  initializeLegs(bet: IBetHistoryBet): void {
    const isBetSettled = bet.settled === 'Y';

    _.each(this.leg, (legItem: IBetHistoryLeg) => {
      this.initializeParts(legItem);

      this.setLegProperties(legItem);

      this.initializeItemsArrays(legItem);
      this.initializeCashOutMap(legItem, isBetSettled);
    });
  }

  initializeParts(legItem: IBetHistoryLeg): void {
    _.each(legItem.part, part => {
      part.description = part.outcome[0].name;
      if (part.handicap !== null && typeof part.handicap === 'object' && part.handicap.length) {
        const handicapObj = _.findWhere(part.handicap, { formatted: 'Y' });
        part.handicap = handicapObj ? handicapObj.value.toString() : '';
      } else if (typeof part.handicap !== 'string') {
        part.handicap = '';
      }
      part.eventId = part.outcome[0].event.id;
      part.marketId = part.outcome[0].market.id;
      part.outcomeId = part.outcome[0].id;
      part.eventMarketDesc = part.outcome[0].market.name;
      part.priceNum = Number(part.price[0].priceNum);
      part.priceDen = Number(part.price[0].priceDen);
      part.result = part.outcome[0].result.value;
      if (part.eachWayTerms && part.eachWayTerms[0]) {
        part.eachWayPlaces = part.eachWayTerms[0].eachWayPlaces;
        part.eachWayNum = part.eachWayTerms[0].eachWayNum;
        part.eachWayDen = part.eachWayTerms[0].eachWayDen;
      }
    });
  }

  setLegProperties(legItem: IBetHistoryLeg): void {
    legItem.part = this.betModelService.createOutcomeName(legItem.part);
    legItem.status = undefined;
    legItem.backupEventEntity = legItem.part[0].outcome[0].event;
    legItem.backupEventEntity.startTime = this.normalizeDate(legItem.backupEventEntity.startTime);
    legItem.backupEventEntity.categoryId = legItem.part[0].outcome[0].eventCategory.id;
  }

  /**
   * Format date string to have correct TZD sign
   * @param  {String} dateString [String date - expected to be "2018-03-12 13:39:20",
   *                              without TZD signs]
   * @return {String}            [Correct date string with TZD signs]
   */
  normalizeDate(dateString: string): string {
    return dateString.replace(' ', 'T');
  }

  private setBybType(bet: IBetHistoryBet): void {
    if (bet.source === CHANNEL.fiveASide) {
      this.bybType = this.localeService.getString('bethistory.bybHeader.fiveASide');
    } else if (bet.source === CHANNEL.byb) {
      this.bybType = this.localeService.getString('bethistory.bybHeader.byb');
    }
  }
}
