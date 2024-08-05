import { IBetslipBetData } from '@betslip/models/betslip-bet-data.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';

export class BetslipBetDataUtils {
  static readonly PRICE_TYPES_WITH_PAYOUT = ['LP', 'GP', 'GUARANTEED'];

  static isFreeBetUsed(betData: IBetslipBetData): boolean {
    return !!(betData.Bet.freeBet && betData.Bet.freeBet.id || betData.tokenValue);
  }

  static areFreeBetsAvailable(betData: IBetslipBetData): boolean {
    return !!(betData.Bet.freeBets && betData.Bet.freeBets.length && !betData.disabled);
  }

  static estReturnsAvalibale(bet: IBetslipBetData): boolean {
    return Boolean(bet && bet.price && BetslipBetDataUtils.PRICE_TYPES_WITH_PAYOUT.includes(bet.price.priceType));
  }

  /**
   * Check if selection is both SP and LP.
   * Not every Racing event has SP\LP option, in most cases its only SP
   * params {Object} market
   * params {Object} outcome
   * return {Boolean}
   */
  static isSPLP(market: IMarket, outcome?: IOutcome): boolean {
    const outcomeMeaningMinorCode = outcome ? outcome.outcomeMeaningMinorCode : market.outcomeMeaningMinorCode;
    return !!market.isLpAvailable &&
      !!market.isSpAvailable &&
      outcomeMeaningMinorCode !== '1' &&
      outcomeMeaningMinorCode !== '2';
  }

  /**
   * Get original outcomeMeaningMinorCode returned from site server
   * params {Object} outcome
   */
  static getOutcomeMeaningMinorCode(outcome: IOutcome): string {
    return typeof outcome.outcomeMeaningMinorCode === 'string'
      ? outcome.outcomeMeaningMinorCode
      : outcome.originalOutcomeMeaningMinorCode;
  }

  static outcomeDetails(event: ISportEvent, market: IMarket, outcome: IOutcome): Partial<IOutcomeDetails> {
    if (!event || !market || !outcome) {
      return undefined;
    }

    return {
      eventDrilldownTagNames: event.drilldownTagNames,
      marketDrilldownTagNames: market.drilldownTagNames,
      isAvailable: event.isAvailable,
      cashoutAvail: event.cashoutAvail,
      marketCashoutAvail: market.cashoutAvail,
      isMarketBetInRun: market.isMarketBetInRun,
      eventliveServChannels: event.liveServChannels,
      marketliveServChannels: market.marketliveServChannels || market.liveServChannels,
      outcomeliveServChannels: outcome.liveServChannels,
      isSPLP: BetslipBetDataUtils.isSPLP(market, outcome),
      isGpAvailable: market.isGpAvailable,
      isEachWayAvailable: market.isEachWayAvailable,
      marketPriceTypeCodes: market.priceTypeCodes,
      outcomeMeaningMinorCode: this.getOutcomeMeaningMinorCode(outcome),
      info: {
        sportId: event.sportId || event.categoryId,
        time: event.startTime,
        isStarted: event.isStarted
      }
    };
  }
}
