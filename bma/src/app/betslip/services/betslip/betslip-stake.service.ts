import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import * as _ from 'underscore';
import { BetslipFiltersService } from '@betslip/services/betslipFilters/betslip-filters.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IOutcome } from '@core/models/outcome.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IPrice } from '@core/models/price.model';
import { IBetslipBetData } from '@betslip/models/betslip-bet-data.model';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { StorageService } from '@core/services/storage/storage.service';
import { DecimalPipe } from '@angular/common';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { bs } from '@app/lazy-modules/locale/translations/en-US/bs.lang';

@Injectable({ providedIn: BetslipApiModule })
export class BetslipStakeService {
  oddsBoostEnabled: boolean;
  maxFlag: boolean = false;
  hasFreeBet: boolean;
  
  constructor(
    private overAskService: OverAskService,
    private bsFiltersService: BetslipFiltersService,
    private toolsService: CoreToolsService,
    private pubSubService: PubSubService,
    private storageService: StorageService,
    private fbService: FreeBetsService
  ) {
    this.getOddsBoostEnabled();
  }

  /**
   * Returns sum of stakes
   * roundDown for case 1.03 - 1 = 0.03000000000027 => (0.0300000027 > 0.03)
   *
   * @param {object[]} bets
   * @param {boolean} addDisabledBets
   * @return {number}
   */
  getStake(bets: IBetslipBetData[] | any, addDisabledBets?: boolean): number {
    const decimalPipe = new DecimalPipe('en-US');
    // @@ TODO added this for lotto and remove datatype any in method
    if(bets && bets.length && bets[0].isLotto){
      return Number(parseFloat((this.getLottoTotlaStake(bets)))) ;
    }else{
      return Number(parseFloat(decimalPipe.transform(Number(this.getTotalStake(bets, addDisabledBets)) - Number(this.getFreeBetStake(bets, addDisabledBets)),'.2-2').replace(/,/g, '')));
    }
  }
  getLottoTotlaStake(bets) {
    let amount = 0;
    return bets.reduce((sum: number, bet) => {
      const estAmt = bet.accaBets.reduce((accaSum: number, betType) => {
        if (betType.stake > 0) {
          accaSum += Number(betType.stake) * Number(betType.lines.number);
        }
        return accaSum;
      }, 0);
      sum = estAmt * bet.details.draws.length;
      bet.totalStakeAmount = sum.toFixed(2);
      amount += sum;
      return Number(amount);
    }, 0);
  }
  /**
   * Returns sum of free bets
   * @param {object[]} bets
   * @param {boolean} addDisabledBets
   * @return {string}
   */
  getFreeBetStake(bets: IBetslipBetData[], addDisabledBets?: boolean): string {
    return this.getSelectedBets(bets).reduce((sum: number, bet) => {
      if (this.overAskService.userHasChoice) {
        return sum + (!bet.disabled && Number(bet.tokenValue) || 0);
      }
      const condition = addDisabledBets ? bet.selectedFreeBet : bet.selectedFreeBet && !bet.disabled;
      return condition
          // if stake for the bet is entered, display full free bet value, otherwise calculate correct free bet value
          ? sum + (Number(bet.stake.perLine) ? Number(bet.selectedFreeBet.value) : bet.stake.lines * bet.stake.freeBetAmount) : sum;
    }, 0)
        .toFixed(2);
  }
  getFreeBetLabelText(bets: IBetslipBetData[],flag:boolean=false): string {
    let hasFreeBet = false;
    let hasBetToken = false;
    let hasFanzone = false;
    this.getSelectedBets(bets).forEach(bet => {
      const selectedFB = bet.selectedFreeBet;
      const fbOfferCategory = selectedFB?.freeBetOfferCategories?.freebetOfferCategory;
      if (selectedFB && fbOfferCategory) {
        if(this.fbService.isBetPack(fbOfferCategory)){
          hasBetToken=true;
        }else if(this.fbService.isFanzone(fbOfferCategory)){
          hasFanzone=true;
        }else{
          hasFreeBet=true;
        }
      }
      else if (selectedFB) {
        hasFreeBet = true;
      }
    });
    if (flag) {
      return (!hasFreeBet && hasFanzone) ? 'fanzone-bet-label' : 'free-bet-label';
    }  
      return hasFreeBet ? (hasBetToken ? bs.fbAndBT : bs.freeBet) : (hasBetToken ? bs.betToken : hasFanzone ? bs.fanZone : '');
    }
  /**
   * Returns sum of stakes and free bets
   * @param {object[]} bets
   * @param {boolean} addDisabledBets
   * @return {string}
   */
  getTotalStake(bets: IBetslipBetData[] | any, addDisabledBets?: boolean): string {
    if(!bets[0]?.isLotto){
    return this.getSelectedBets(bets)
    .reduce((sum: number, bet: IBetslipBetData | any) => {
          const condition = addDisabledBets ? bet.stake.amount : bet.stake.amount && !bet.disabled;
          let result = condition ? sum + (bet.stake.lines * +bet.stake.perLine) : sum;

          if (!this.overAskService.userHasChoice && (bet.selectedFreeBet && !bet.disabled || bet.selectedFreeBet && addDisabledBets)) {
            result += bet.Bet && bet.Bet.isEachWay
              ? Number(bet.selectedFreeBet.value)
              : bet.stake.lines * bet.stake.freeBetAmount;
          }

          return result;
        }, 0)
        .toFixed(2);
      } else {
        return this.getLottoTotlaStake(bets).toFixed(2);
       }
  }

  /**
   * Returns total estimated returns value
   * @param {object[]} bets
   * @param {boolean} areToteBetsInBetslip
   * @return {number|null}
   */
  getTotalEstReturns(bets: IBetslipBetData[] | any, areToteBetsInBetslip: boolean): number | null | string {
    if(bets.some(bet => bet.Bet?.params?.lottoData?.isLotto)) {
     bets = bets.map(selectedBet => selectedBet.Bet.params.lottoData);
    }
    const selectedBets = this.getSelectedBets(bets);

    if(bets.length > 1 && !this.checkForStraightMultiples(selectedBets, selectedBets[0].isLotto)) {
      //Should display Total Potential returns as N/A in betslip for non straight multiple selections
      return 'N/A';
    }

    let amount = 0;
    //@@TODO remove datatype any in reduce parameters below 
    const isNA = _.some(selectedBets, (bet: IBetslipBetData | any) => {
      if (!bet.disabled && !bet.isLotto) {
        if (bet.isSP && (bet.stake.perLine > 0 || bet.selectedFreeBet)) {
          return true;
        } else if (bet.stake.perLine > 0 || bet.selectedFreeBet) {
          const estReturns = bet.type === 'SGL' ? this.calculateEstReturns(bet) : this.calculateEstReturnsMultiples(bet);
          if (_.isNumber(estReturns)) {
            amount += estReturns;
          } else {
            return true;
          }
        }
      }
      /**
      * added for lotto betslip total estimations amount calculation
      */
      else if (!bet.disabled && bet.isLotto && bet.accaBets) {
        const estAmt = bet.accaBets.reduce((sum: number, betType) => {
          const accasEstReturns = parseFloat(betType.estReturns || betType.stake);
          if (accasEstReturns > 0) {
            sum += accasEstReturns;
          } return sum;
        }, 0);
        if (_.isNumber(estAmt)) {
          bet.totalEstReturns = estAmt.toFixed(2);
          amount += estAmt;
        }
      }
      return false;
    });

    return isNA || areToteBetsInBetslip ? null : amount;
  }

  /**
   * Calculate Estimated Returns for single selection
   * @param {object} bet
   * @return {number}
   */
  calculateEstReturns(bet: IBetslipBetData, index?: number): string | number {
    this.checkIndex(index);
    if (!BetslipBetDataUtils.estReturnsAvalibale(bet)) {
      return 'N/A';
    }

    if (bet.isTraderOffered) {
      return Number(bet.potentialPayout);
    }
    let stake = this.bsFiltersService.filterStakeValue(Number(bet.stake.perLine));
    const price = this.getPrices(bet);

    const freebet = (bet.selectedFreeBet && Number(bet.selectedFreeBet.value)) || 0;
    stake += bet.Bet.isEachWay ? freebet / 2 : freebet;

    const eachWayProfit = bet.Bet.isEachWay ? this.calculateExtraProfit(bet, stake) : 0;
    const decimalPipe = new DecimalPipe('en-US');
    const estReturns = decimalPipe.transform(((price.priceNum / price.priceDen * stake) + stake + eachWayProfit) - freebet , '.2-2')?.replace(/,/g, '');

    return this.maxPayoutCheck(Number(estReturns == undefined ? null : estReturns), bet.Bet.maxPayout);
  }

  /**
   * Calculate Estimated Returns for multiple selection
   * @param {Object} bet
   * @return {number | string}
   */
  calculateEstReturnsMultiples(bet: IBetslipBetData, index?: number): string | number {
    // Set potential payout value directly from readBet when trader offer new stake or change price(overask process)
    // Ignore boost as it was applied yet
    if (bet.isTraderOffered) {
      return bet.isSP || !Number(bet.potentialPayout) ? 'N/A' : Number(bet.potentialPayout);
    }

    let stake = this.bsFiltersService.filterStakeValue(Number(bet.stake.perLine));
    const actualFreeBet = bet.stake.lines * bet.stake.freeBetAmount || 0;
    const freeBet = bet.selectedFreeBet && Number(bet.selectedFreeBet.value) || 0;
    const payout = this.oddsBoostEnabled && bet.Bet.oddsBoost ? bet.Bet.oddsBoost.enhancedOddsPrice : bet.potentialPayout;
    const isBoostedEWBet = (this.oddsBoostEnabled && bet.Bet.oddsBoost && bet.Bet.isEachWay);

    stake += actualFreeBet / bet.stake.lines;

    if (bet.Bet.isEachWay) {
      const outcomes = bet.outcomes || [];
      let eachWayProfit = 1;
      if (outcomes.length > 1 && bet.stakeMultiplier === 1) {
        _.each(outcomes, (o: IOutcome) => {
          const { priceNum, priceDen } = o.price as Partial<IOutcomePrice>;
          eachWayProfit *= +o.eachWayFactorNum / +o.eachWayFactorDen * priceNum / priceDen + 1;
        });
      } else {
        eachWayProfit = bet.isSP ? 0 : +bet.Bet.payout.find((item: { legType: string }) => item.legType === 'P').potential;
      }

      stake *= Number(eachWayProfit + bet.potentialPayout);
    } else {
      stake *= Number(payout);
    }

    const estReturns = payout && !bet.isSP && !isBoostedEWBet ? this.toolsService.roundDown(stake - freeBet, 2) : 'N/A';

    return (estReturns === 'N/A') ? estReturns : this.maxPayoutCheck(estReturns, bet.Bet.maxPayout);
  }

  /**
   * @param bets {IBetslipBetData[]}
   * @returns {boolean}
   */
  private checkForStraightMultiples(bets: IBetslipBetData[] | any, isLotto: boolean) : boolean { // neeed to update interface type
    if(isLotto) {
      return true;
    }
    const multiBets = bets.filter(bet => bet.type !== 'SGL');
    if(multiBets.length === 0) {
      return false;
    }

    return multiBets.some((bet: any)=> ['DBL', 'TBL', 'AC'].some(type => bet.type.includes(type)) &&  bet.stake.params.lines === 1);
  }

  /**
   * Checks for Max payout and returns the estimated returns
   * @param {string , number}
   * @returns {number}
   */
  private maxPayoutCheck(value: number, maxPayout: string): number {
    const maxpayout = Number(maxPayout);
    if (!this.maxFlag) {
      this.maxFlag = (value > maxpayout) ? true : false;
    }
    return value < maxpayout ? value : maxpayout;
  }

  /**
  * Sets maxflag as false when the loop reruns for betslip
  * @param {number}
  * @returns {void}
  */
  private checkIndex(index: number): void {
    if (index === 0) {
      this.maxFlag = false;
    }
  }

  /**
   * Returns Only bets with enabled checkboxes if OverASK is in progress
   *   and trader has already provided their decision
   * If overask is off returns all bets
   * @param {object[]} bets
   * @returns {object[]}
   */
  private getSelectedBets(bets: IBetslipBetData[] = []): IBetslipBetData[] | any {
    return this.overAskService.isInProcess && !this.overAskService.isOnTradersReview
        ? bets.filter(bet => bet.isSelected) : bets;
  }

  /**
   * Calculate Exstra Profit
   * @param {object} bet
   */
  private calculateExtraProfit(bet: IBetslipBetData, total: number): number {
    const price = this.getPrices(bet);
    return (total * (price.priceNum / price.priceDen) * (bet.eachWayFactorNum / bet.eachWayFactorDen)) + total;
  }

  /**
   * Calculate Exstra Profit
   * @param {object} bet
   */
  private getPrices(bet: IBetslipBetData): IPrice {
    return this.oddsBoostEnabled && bet.Bet.oddsBoost && !bet.isTraderOffered ? {
      priceNum: bet.Bet.oddsBoost.enhancedOddsPriceNum,
      priceDen: bet.Bet.oddsBoost.enhancedOddsPriceDen
    } : bet.price;
  }

  private getOddsBoostEnabled(): void {
    this.oddsBoostEnabled = !!this.storageService.get('oddsBoostActive');

    this.pubSubService.subscribe('BetslipStakeService', this.pubSubService.API.ODDS_BOOST_CHANGE, (active: boolean) => {
      this.oddsBoostEnabled = active;
    });
  }
}
