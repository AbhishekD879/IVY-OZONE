import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { ToteBetLeg } from '../toteBetLeg/tote-bet-leg';

import * as _ from 'underscore';
import { IUkTotePoolBet } from '@uktote/models/tote-pool.model';
import { IRacingEvent } from '@core/models/racing-event.model';
import { IUkTotePotBetConfig } from '@uktote/models/tote-pot-bet.model';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { IPoolBet } from '@bpp/services/bppProviders/bpp-providers.model';
import { IToteBetDetails, IToteLeg } from '@betslip/services/toteBetslip/tote-betslip.model';
import { IUkToteLeg } from '@uktote/models/uk-tote-leg.model';

export class TotePotBet {

  legs: ToteBetLeg[];
  isSuspended: boolean;

  readonly outcomeIdLegMap:  {[key: string]: IUkToteLeg};

  constructor(
    public pool: IUkTotePoolBet,
    public events: Array<IRacingEvent>,
    private config: IUkTotePotBetConfig,
    private ukToteService: UkToteService
  ) {
    this.pool = pool;
    this.legs = this.createToteLegs(events);
    this.events = events;
    this.outcomeIdLegMap = this.generateOutcomeIdLegMap();
  }

  /**
   * Get number of lines in bet
   */
  get numberOfLines(): number {
    const filledLegs = _.filter(this.legs, leg => leg.filled),
      legsSelectionsCount = _.map(filledLegs, leg => leg.selectionsCount),
      numberOfLines = _.reduce(legsSelectionsCount, (a, b) => a * b, 1);
    return numberOfLines;
  }
  set numberOfLines(value:number){}

  /**
   * Get selected outcomes
   */
  get selectedOutcomes(): Array<IOutcome> {
    return _.chain(this.legs)
            .map(leg => leg.selectedOutcomes)
            .flatten()
            .value();
  }
  set selectedOutcomes(value:Array<IOutcome>){}

  /**
   * Check if bet suspended
   * @returns {boolean}
   */
  checkIfBetSuspended(): boolean {
    return !this.pool.isActive || _.every(this.legs, leg => leg.isSuspended);
  }

  /**
   * Check if at least one leg filled
   * @returns {boolean}
   */
  checkIfSomeLegFilled(): boolean {
    return _.some(this.legs, leg => leg.filled);
  }

  /**
   * Check if all legs filled
   * @returns {boolean}
   */
  checkIfAllLegsFilled(): boolean {
    return _.every(this.legs, leg => leg.filled);
  }

  /**
   * Clear all legs
   */
  clear(): void {
    _.forEach(this.legs, leg => {
      leg.clear();
    });
  }

  /**
   * Get bet object ready to be used for Bet placement
   * @param stakePerLine {Number} - Stake per line value
   * @returns {{poolType, stakePerLine: *, poolItem, betNo: number}} - ready for bet placement
   * bet object
   */
  getBetObject(stakePerLine: number): IPoolBet {
    const poolId = this.pool.id,
      poolItems = this.selectedOutcomes.map(outcome => {
        return {
          poolId,
          outcome: outcome.id
        };
      });

    return {
      poolType: this.pool.type,
      stakePerLine,
      poolItem: poolItems,
      betNo: 159 // random value
    };
  }

  /**
   * Generates bet details object to be sent into Betslip
   * @returns {{poolName: *, numberOfLines, orderedLegs: Array}} - Bet details object
   */
  generateToteBetDetails(stakeRestrictions): IToteBetDetails {
    return {
      poolName: this.config.poolTypesMap[this.pool.type].name,
      numberOfLines: this.numberOfLines,
      orderedLegs: this.getStaticLegs(),
      stakeRestrictions
    };
  }

  /**
   * Get Leg linked which provided outcome belong to
   * @param outcome
   * @returns {*}
   */
  getOutcomeLinkedLeg(outcome: IOutcome): IUkToteLeg {
    return this.outcomeIdLegMap[outcome.id];
  }

  /**
   * Update isSuspended property of toteBet
   */
  updateBetStatus(): void {
    this.isSuspended = this.checkIfBetSuspended();
  }

  /**
   * Generates "outcome id" to "linked leg" map
   * @returns {Object}
   * @private
   */
  private generateOutcomeIdLegMap(): {[key: string]: IUkToteLeg} {
    const outcomeIdLegMap = {};
    _.forEach(this.legs, leg => {
      if (!leg.event || !_.isArray(leg.event.markets)) {
        return;
      }
      _.forEach(leg.event.markets[0].outcomes, (outcome: IOutcome) => {
        outcomeIdLegMap[outcome.id] = leg;
      });
    });
    return outcomeIdLegMap;
  }

  /**
   * Creates ToteBetLeg models for each Tote bet leg
   * @param {Array} events - array of event objects
   */
  private createToteLegs(events: ISportEvent[]): ToteBetLeg[] {
    const groupedByMarketIdEvens = {};
    _.forEach(events, (event: ISportEvent) => {
      const market = _.first(event.markets);
      groupedByMarketIdEvens[market.id] = event;
    });
    return _.map(this.pool.marketIds, (marketId: string, index: number) => {
      return new ToteBetLeg(index, marketId, groupedByMarketIdEvens[marketId], this.ukToteService);
    });
  }

  /**
   * Get legs array with only needed for Betslip properties
   * @returns {Array} - array of legs
   */
  private getStaticLegs(): Array<IToteLeg> {
    return this.legs.map((leg: ToteBetLeg) => {
      return {
        name: leg.name,
        event: leg.event,
        outcomes: leg.selectedOutcomes,
        eventTitle: this.ukToteService.getRaceTitle(leg.event)
      };
    });
  }

}
