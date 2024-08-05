import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';

import { IQuickbetOddsSelectorModel } from '@app/quickbet/models/quickbet-common.model';
import { IQuickbetSelectionPriceModel } from '@app/quickbet/models/quickbet-selection-price.model';
import { IQuickbetStoredStateModel } from '@app/quickbet/models/quickbet-stored-state.model';
import { IQuickbetRequestModel } from '@app/quickbet/models/quickbet-selection-request.model';
import { IQuickbetPlaceBetModel } from '@app/quickbet/models/quickbet-place-bet.model';
import { IQuickbetOddsBoostModel } from '@app/quickbet/models/quickbet-odds-boost.model';
import { IOutcome } from '@core/models/outcome.model';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { DecimalPipe } from '@angular/common';
import { IFreebetToken} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ILuckyDipFieldsConfig } from '@lazy-modules/luckyDip/models/luckyDip';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
/**
 * Model for Quickbet selection. New instance will inherit all properties from selection param:
 */
export class IQuickbetSelectionModel {
  categoryId: string;
  categoryName: string;
  classId: string;
  className: string;
  currency: string;
  disabled: boolean;
  eachWayFactorDen: number;
  eachWayFactorNum: number;
  eachWayPlaces:string;
  eventId: string;
  eventIsLive: undefined | boolean;
  eventName: string;
  eventStatusCode: string;
  freebet: IFreebetToken;
  freebetList?: IFreebetToken[];
  fanzoneList?: IFreebetToken[];
  freebetValue: number;
  hasGP: boolean;
  hasLP: boolean;
  hasSP: boolean;
  hasSPLP: boolean;
  isEachWay: boolean;
  isEachWayAvailable: boolean;
  isLP: boolean;
  isLpAvailable: boolean;
  isMarketBetInRun: boolean;
  isRacingSport: boolean;
  isSpAvailable: boolean;
  isStarted: boolean;
  isUnnamedFavourite: boolean;
  marketId: string;
  marketName: string;
  marketStatusCode: string;
  oddsSelector: IQuickbetOddsSelectorModel[];
  oldOddsValue: string;
  outcomeId: string;
  outcomeMeaningMinorCode: string;
  outcomeName: string;
  outcomeStatusCode: string;
  potentialPayout: string;
  price: IQuickbetSelectionPriceModel;
  oldPrice?: IQuickbetSelectionPriceModel | {};
  requestData: IQuickbetRequestModel;
  selectionType: string;
  stake: null | string | any;
  stakeAmount: number;
  startTime: Date;
  typeId: string;
  typeName: string;
  priceDec: number;
  newOddsValue: string;
  handicapValue: string;
  oldHandicapValue: string;
  isYourCallBet?: boolean;
  isBoostActive?: boolean;
  reboost?: boolean;
  markets?: {}[] | any;
  error?: {
    code: string;
    subErrorCode?: string;
    selectionUndisplayed?: string;
  };
  oddsBoost?: IQuickbetOddsBoostModel;
  outcomes?: IOutcome[];

  isOutright: boolean;
  isSpecial: boolean;
  freeBetOfferCategory?: string;
  drilldownTagNames ?:string;
  maxPayout ? : string;
  isLuckyDip:boolean;
  luckyDipCmsData?: ILuckyDipFieldsConfig;
  templateMarketName?: string;
  luckyDipMarketName?: string;
  isStreamBet?: boolean;
  
  constructor(
    selection: IQuickbetSelectionModel,
    storedState: IQuickbetStoredStateModel,
    private userService: UserService,
    private fracToDecService: FracToDecService,
    private clientUserAgentService: ClientUserAgentService,
    private toolsService: CoreToolsService,
    private timeSyncService: TimeSyncService
  ) {
    const defaultProperties = {
      currency: this.userService.currencySymbol,
      isEachWay: storedState.userEachWay || false,
      freebet: storedState.freebet || 0,
      stake: storedState.userStake || null,
      stakeAmount: 0,
      potentialPayout: 0,
      freebetValue: 0,
      isLuckyDip:storedState.isLuckyDip
    };

    this.setOddsValue(selection);
    _.extend(this, defaultProperties, selection);
    // Calculate potential payout
    this.onStakeChange();
  }

  /**
   * Handler for selection's stake change.
   */
  onStakeChange(): void {
    this.potentialPayout = this.getPotentialPayout();
    this.stakeAmount = parseFloat(this.stake) || 0;
  }

  /**
   * Formats place bet model.
   * @returns {Object}
   */
  formatBet(): IQuickbetPlaceBetModel {
    const price: string = this.isLP ? `${this.price.priceNum}/${this.price.priceDen}` : 'SP';
    const freebetToken = this.freebet ? { freebet: { id: Number(this.freebet.freebetTokenId), stake: this.freebetValue.toString() }} : {};
    const oddsBoostToken = this.isBoostActive ? { freebet: { oddsBoost: true }} : {};
    const handicapObj = this.handicapValue ? { handicap: Number(this.handicapValue) } : {};
    const marketId = this.getLuckydipMarketId();
    return _.extend({}, {
      token: this.userService.bppToken,
      winType: this.isEachWay ? 'EACH_WAY' : 'WIN',
      stake: this.stake ? `${+this.stake}` : '0',
      currency: this.userService.currency,
      price,
      ip: this.timeSyncService.ip,
      clientUserAgent: this.clientUserAgentService.getId(),// We don't need pass isLotto && isVirtual params,
      // as quickbet is not present on desktop
      marketId
    }, _.extend(freebetToken, oddsBoostToken), handicapObj);
  }

  /**
   * Update currency by default
   */
  updateCurrency(): void {
    this.currency = this.userService.currencySymbol;
  }

  /**
   * Update handicap value and outcome name
   * @param {string} val
   */
  updateHandicapValue(val: string): void {
    if (val !== this.handicapValue) {
      this.oldHandicapValue = this.handicapValue;
      this.handicapValue = val;
      this.outcomeName = this.outcomeName.replace(/[(][-+]\d+.\d+[)]/, `(${val})`);
    }
  }

  /**
   * Format handicap value in string with +/- in the beginning
   * @param {string} val
   */
  formatHandicap(val: string): string {
    return `${Number(val) < 0 ? '' : '+'}${Number(val).toFixed(1)}`;
  }

  /**
   * Update selection status
   */
  setStatus(status: boolean, place: string): void {
    switch (place) {
    case ('event'):
      this.eventStatusCode = status ? 'S' : 'A';
      break;
    case ('market'):
      this.marketStatusCode = status ? 'S' : 'A';
      break;
    default:
      this.outcomeStatusCode = status ? 'S' : 'A';
    }

    this.disabled = this.isSuspended(this.eventStatusCode) || this.isSuspended(this.marketStatusCode) ||
      this.isSuspended(this.outcomeStatusCode);
  }

  /**
   * set odds value
   * @param {Object} eventData
   * @private
   */
  private setOddsValue(eventData: IQuickbetSelectionModel): void {
    if (eventData.price) {
      const priceNum = eventData.price.priceNum,
        priceDen = eventData.price.priceDen;
      eventData.oldOddsValue = <string>this.fracToDecService.getFormattedValue(priceNum, priceDen);
      eventData.oddsSelector = [{
        name: 'LP',
        value: eventData.oldOddsValue
      }, {
        name: 'SP',
        value: 'SP'
      }];
    }
  }

  /**
   * Calculate Extra Profit
   * @returns {*}
   * @private
   */
  private calculateExtraProfit(stake: number, price: IQuickbetSelectionPriceModel): number {
    if (!price || !this.isEachWay) {
      return 0;
    }

    return (stake * (price.priceNum / price.priceDen) * (this.eachWayFactorNum / this.eachWayFactorDen)) + stake;
  }

  /**
   * Calculate Estimated Returns for single selection
   * @returns {string}
   * @private
   */
  private getPotentialPayout(): string {
    let stake = parseFloat(this.stake) || 0;
    stake += this.isEachWay ? this.freebetValue / 2 : this.freebetValue;
    const price = this.getPrices(this.price);
    const eachWayProfit = price && this.isEachWay ? this.calculateExtraProfit(stake, price) : 0;
    const decimalPipe = new DecimalPipe('en-US');
    return this.isLP ?
           decimalPipe.transform(((price.priceNum / price.priceDen * stake) + stake + eachWayProfit) - this.freebetValue , '.2-2').replace(/,/g, '')
           : 'N/A';
  }

  /**
   * Calculate Exstra Profit
   * @param {object} bet
   */
  private getPrices(price: IQuickbetSelectionPriceModel): IQuickbetSelectionPriceModel {
    return this.isBoostActive && this.oddsBoost ? {
      priceNum: +this.oddsBoost.enhancedOddsPriceNum,
      priceDen: +this.oddsBoost.enhancedOddsPriceDen
    } : price;
  }

  /**
   * Check if status is suspended
   * @param status {string}
   * @returns {boolean}
   * @private
   */
  private isSuspended(status: string): boolean {
    return _.indexOf(status, ('S')) > -1;
  }

  /* 
  * To return market id if LuckyDip market tag name is configured 
   * @returns {string}
   * @private
  */
  private getLuckydipMarketId():string{
    const market = this.markets && this.markets[0];
      return  market && market.drilldownTagNames && 
      market.drilldownTagNames.includes(LUCKY_DIP_CONSTANTS.MKTFLAG_LD)? 
      this.marketId : LUCKY_DIP_CONSTANTS.EMPTY_STRING;
  }
}
