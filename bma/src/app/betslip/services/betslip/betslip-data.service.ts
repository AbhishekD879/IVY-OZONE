import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { IBetslipData } from '@betslip/models/betslip-bet-data.model';
import { Bet } from '@betslip/services/bet/bet';
import { IBetInfo, IEventIdsObject } from '@betslip/services/bet/bet.model';
import { BetStake } from '@betslip/services/betStake/bet-stake';
import * as _ from 'underscore';
import { StorageService } from '@core/services/storage/storage.service';

@Injectable({ providedIn: BetslipApiModule })
export class BetslipDataService {

  private data: IBetslipData = { bets: [] };
  private placedData: IBetslipData = { bets: [] };
  private readBetData: any = { bets: [] };

  constructor(private storageService: StorageService){}

  get bets(): Bet[] {
    return this.data && this.data.bets;
  }

  set bets(bets: Bet[]) {
    this.data.bets = bets;
  }

  get betslipData(): IBetslipData {
    return this.data;
  }

  set betslipData(data: IBetslipData) {
    this.data = data;
  }

  get placedBets(): IBetslipData {
    return this.placedData;
  }

  set placedBets(data: IBetslipData) {
    this.placedData = data;
  }

  get readBets(): any {
    return this.readBetData;
  }

  set readBets(data: any) {
    this.readBetData = data;
  }

  setDefault() {
    this.data = {
      bets: []
    };
  }

  /**
   * Get outcome ids of every single
   * @return{array} outcome ids
   */
  getActiveSinglesIds(): number[] {
    const ids = [];
    let infoObj: Partial<IBetInfo>;
    _.forEach(this.bets, (bet: Bet) => {
      infoObj = bet.info();
      //@@TODO added for testing in betslip-data.service.ts 63
     if(!bet.params.lottoData?.isLotto){
      if (infoObj && infoObj.eventIds && infoObj.type === 'SGL' && !infoObj.disabled && infoObj.Bet.price.type !== 'DIVIDEND') {
        ids.push((<IEventIdsObject>infoObj.eventIds).outcomeIds[0]);
      }
     }
    });
    return ids;
  }

  /**
   * Checks if prices in bet object are equal to prices in outcome,
   * if not, updates.
   */
  checkPrices(): void {
    let infoObj: Partial<IBetInfo>;

    _.each(this.bets, (bet: Bet) => {
      infoObj = bet.info();

      const stake = <BetStake>bet.stake,
        price = infoObj.price;

      stake.placement = <number>stake.perLine * 1;
      if (bet.freeBet && bet.freeBet.id) {
        stake.placement += stake.freeBetAmount;
      }
      if (infoObj.price && bet.price.props.priceNum &&
          bet.price.props.priceDen && price.priceNum &&
          price.priceDen && (bet.price.props.priceNum !== price.priceNum ||
              bet.price.props.priceDen !== price.priceDen)) {
        bet.price.props.priceNum = price.priceNum;
        bet.price.props.priceDen = price.priceDen;
      }
    });
  }

  /**
   * Clear all user stake data in multiple bets
   */
  clearMultiplesStakes(): void {
    _.each(this.bets, (bet: Bet) => {
      if (bet.type !== 'SGL') {
        bet.clearUserData();
      }
    });
  }

  /**
   * Checks if there are any regular bets in betslip
   * @returns {bool}
   */
  containsRegularBets(): boolean {
    const betData = this.storageService.get('betSelections');
    return (betData && !!betData.length) || (this.bets && !!this.bets.length);
  }

  storeBets(build: IBetslipData): Bet[] {
    this.betslipData.tempBets = _.filter(build.bets, (bet: Bet) => {
      return !!bet.isMocked;
    });
    this.betslipData = build;
    return build.bets;
  }
}
