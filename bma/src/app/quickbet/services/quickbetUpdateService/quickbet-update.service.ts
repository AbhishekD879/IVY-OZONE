import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { Subject } from 'rxjs';

import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { UserService } from '@core/services/user/user.service';

import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IQuickbetSelectionUpdateModel } from '@app/quickbet/models/quickbet-selection-update.model';
import { IQuickbetDeltaObjectModel } from '@app/quickbet/models/quickbet-delta-object.model';
import { IQuickbetUpdateDisableMap } from '@app/quickbet/models/quickbet-disable-map.model';
import { ISuspendedOutcomeError } from '@betslip/models/suspended-outcome-error.model';
import { IQuickbetSelectionPriceModel } from '@app/quickbet/models/quickbet-selection-price.model';

@Injectable({ providedIn: 'root' })
export class QuickbetUpdateService {
  private selection: IQuickbetSelectionModel = null;
  private update: IQuickbetSelectionUpdateModel;
  private disabled: boolean;
  private suspensionPlace: string;
  private disableMap: IQuickbetUpdateDisableMap = {
    event: false,
    market: false,
    selection: false
  };
  private eventSuspension = new Subject<ISuspendedOutcomeError>();
  private priceChange = new Subject<string>();

  constructor(
    private pubSubService: PubSubService,
    private fracToDecService: FracToDecService,
    private quickbetNotificationService: QuickbetNotificationService,
    private localeService: LocaleService,
    private userService: UserService) {
  }

  /**
   * Save selection data
   * @param {Object} selectionData
   */
  saveSelectionData(selectionData: IQuickbetSelectionModel): void {
    this.selection = selectionData;
    if (!this.selection.disabled) {
      this.quickbetNotificationService.clear();
    }
    this.getUpdatedData();
  }

  /**
   * Fill map for multiple suspension
   * @param {Object} map
   */
  fillDisableMap(map: IQuickbetUpdateDisableMap): void {
    this.disableMap = map;
  }

  /**
   * Returns Subject of event suspension
   * @returns {Subject<ISuspendedOutcomeError>}
   */
  getEventSuspension(): Subject<ISuspendedOutcomeError> {
    return this.eventSuspension;
  }

  /**
   * Returns Subject of price change
   * @returns {Subject<boolean>}
   */
  getPriceChange(): Subject<string> {
    return this.priceChange;
  }

  /**
   * Check is bet suspended or undisplayed
   */
  isDisabled(): void {
    if (this.update && this.suspensionPlace && this.update.message.displayed && this.update.message.status) {
      this.disabled = this.update.message.displayed === 'N' || this.update.message.status === 'S';
      if (this.disabled) {
        const message = this.localeService.getString('quickbet.singleDisabled', [this.suspensionPlace]);
        this.disableMap[this.suspensionPlace] = true;
        this.quickbetNotificationService.saveErrorMessage(message, 'warning', 'bet-status');
        this.handleEventSuspension({
          multipleWithDisableSingle: false,
          disableBet: this.disabled,
          msg: message
        });
      } else {
        this.disableMap[this.suspensionPlace] = false;
        const suspendedPlace = Object.keys(this.disableMap).filter((key: string) => this.disableMap[key]);
        if (!this.filterGlobalDisable(this.disableMap)) {
          this.quickbetNotificationService.clear();
          this.handleEventSuspension({
            multipleWithDisableSingle: false,
            disableBet: this.disabled,
            msg: ''
          });
        } else {
          const message = this.localeService.getString('quickbet.singleDisabled', suspendedPlace);
          this.quickbetNotificationService.saveErrorMessage(message, 'warning', 'bet-status');
          this.handleEventSuspension({
            multipleWithDisableSingle: false,
            disableBet: true,
            msg: message
          });
        }
        if (this.selection.price && this.selection.price.isPriceChanged && !suspendedPlace.length) {
          this.showPriceChange();
        }
      }
      this.pubSubService.publish(this.pubSubService.API.GET_QUICKBET_SELECTION_STATUS, [this.disabled,
        this.suspensionPlace]);
    }
  }

  /**
   * Update outcome if price updates are available
   * @param {Object} payload
   * @private
   */
  updateOutcomePrice(payload: IQuickbetDeltaObjectModel): void {
    if (Math.floor(this.selection.price.priceDen) !== Math.floor(payload.priceDen) ||
        Math.floor(this.selection.price.priceNum) !== Math.floor(payload.priceNum)) {
      const oldP = this.fracToDecService.getDecimal(this.selection.price.priceNum, this.selection.price.priceDen, 4),
        newP = this.fracToDecService.getDecimal(Math.floor(payload.priceNum), Math.floor(payload.priceDen), 4),
        isPriceChangeUp = +oldP < +newP,
        isPriceChangeDown = +oldP > +newP;

      if (this.selection.newOddsValue) {
        this.selection.oldOddsValue = this.selection.newOddsValue;
      }
      this.selection.oldPrice = {};
      Object.assign(this.selection.oldPrice, this.selection.price);
      this.selection.price = payload;

      // set new odds value after update
      this.selection.newOddsValue = <string>this.fracToDecService.getFormattedValue(payload.priceNum, payload.priceDen);
      // set new value
      if (this.selection.hasSPLP) {
        this.selection.oddsSelector[0].value = this.selection.newOddsValue;
      }
      // set flags to the selection if price changes up or down
      if (isPriceChangeUp) {
        this.selection.reboost = this.selection.isBoostActive;
        this.selection.price.isPriceChanged = true;
        this.selection.price.isPriceUp = true;
        delete this.selection.price.isPriceDown;
      }
      if (isPriceChangeDown) {
        this.selection.reboost = this.selection.isBoostActive;
        this.selection.price.isPriceChanged = true;
        this.selection.price.isPriceDown = true;
        delete this.selection.price.isPriceUp;
      }

      if (this.selection.outcomeStatusCode === 'A') {
        this.disabled = false;
      }

      // show notification that price was changed
      if (payload.isPriceChanged) {
        this.pubSubService.publish(`SELECTION_PRICE_UPDATE_${this.selection.outcomeId}`, {
          priceDen: payload.priceDen,
          priceNum: payload.priceNum
        });
          this.showPriceChange();
      }
      // recalculate est. return
      this.selection.onStakeChange();
    }
  }

  /**
   * Get odds in correct format
   * @param {Object} price
   * @param {string=} format
   * @returns {string}
   */
  getOdds(price: IQuickbetSelectionPriceModel, format: string = ''): string {
    if (!price) {
      return '';
    }

    let odds;
    const priceType = price.priceType || price.priceTypeRef && price.priceTypeRef.id || '';

    if (priceType.indexOf('SP') >= 0) {
      odds = 'SP';
    } else {
      if (this.userService.oddsFormat.indexOf('dec') >= 0 || format === 'dec') {
        odds = this.fracToDecService.getDecimal(price.priceNum, price.priceDen);
      } else {
        odds = `${price.priceNum}/${price.priceDen}`;
      }
    }

    return odds;
  }

  /**
   * Check if handicap value is changed
   * @param selection
   */
  isHandicapChanged(selection: IQuickbetSelectionModel): boolean {
    return !!(selection && selection.oldHandicapValue && selection.oldHandicapValue !== selection.handicapValue);
  }

  /**
   * Create price change message
   */
  private showPriceChange(): void {
    const oldPrice = this.getOdds(this.selection.oldPrice || this.selection.price);
    const newPrice = this.getOdds(this.selection.price);
    const message = this.localeService.getString('quickbet.priceIsChanged', [oldPrice, newPrice]);

    this.quickbetNotificationService.saveErrorMessage(message, 'warning', 'bet-status');
    this.handlePriceOrHandicapChange(message);
  }

  /**
   * Emits event after the price change
   * @param {string} msg
   */
  private handlePriceOrHandicapChange(msg: string): void {
    if (this.priceChange.observers.length) {
      this.priceChange.next(msg);
    }
  }

  /**
   * Emits event after the suspension status change
   * @param {ISuspendedOutcomeError} status
   */
  private handleEventSuspension(status: ISuspendedOutcomeError): void {
    if (this.eventSuspension.observers.length) {
      this.eventSuspension.next(status);
    }
  }

  /**
   * Get updated outcome data
   */
  private getUpdatedData(): void {
    this.pubSubService.subscribe('QuickbetUpdateService', this.pubSubService.API.QUICKBET_SELECTION_UPDATE,
      (id: string, update: IQuickbetSelectionUpdateModel) => {
      const isSelectionForUpdate = !!this.selection,
        isValidUpdate = update && update.subChannel;

      if (isSelectionForUpdate && isValidUpdate) {
          this.update = update;
          this.applyUpdate(update);
          this.isDisabled();
      }
    });
  }

  /**
   * Apply updated data to deltaObject and update selection
   * @param {Object} update
   * @private
   */
  private applyUpdate(update: IQuickbetSelectionUpdateModel): void {
    const delta = this.deltaObject(update);

    if (!this.selection.isUnnamedFavourite &&
      (update.subChannel.type === 'sPRICE' || update.subChannel.type === 'sSELCN') && this.selection.price) {
      this.updateOutcomePrice(delta);
    }

    if ((update.subChannel.type === 'sMHCAP') || (update.subChannel.type === 'sEVMKT')) {
      const val = delta.hcap_values[this.selection.outcomeMeaningMinorCode];
      const eachWayFlagUpdated: boolean = this.isEachWayFlagUpdated(update.message.ew_avail, this.selection);
      if (val) {
        this.updateHandicap(val);
      }
      if(eachWayFlagUpdated){
        this.pubSubService.publish(this.pubSubService.API.EACHWAY_FLAG_UPDATED,[update.message.ew_avail]);
      }
    }
  }

  /**
   * Update handicap if handicap updates are available
   * @param {string} val
   * @private
   */
   private updateHandicap(val: string): void {
    let newHandicap = val.replace(/[()]/g, '');

    newHandicap = this.selection.formatHandicap(newHandicap);

    if (this.selection.handicapValue === newHandicap) {
      return;
    }

    this.selection.updateHandicapValue(newHandicap);
    const errorMessage = this.localeService.getString('quickbet.handicapError',
      [this.selection.oldHandicapValue, this.selection.handicapValue]);

    if (!this.disabled) {
      this.handlePriceOrHandicapChange(errorMessage);
      this.quickbetNotificationService.saveErrorMessage(errorMessage, 'warning');
    }
  }

  /**
   * Set delta object
   * @param {Object} updateItem
   * @returns {{}}
   * @private
   */
  private deltaObject(updateItem: IQuickbetSelectionUpdateModel): IQuickbetDeltaObjectModel {
    const payload = updateItem.message;
    const handicapValues = payload.hcap_values;
    const eachWayAvailable: string = payload.ew_avail;
    let delta;

    switch (updateItem.subChannel.type) {
      case 'sPRICE':

        if (payload.lp_num || payload.lp_den) {
          let priceType;
          if (this.selection.price) {
            priceType = this.selection.price.priceType || this.selection.price.priceTypeRef.id;
          }
          delta = {
            priceDec: Number(this.fracToDecService.getDecimal(Number(payload.lp_num), Number(payload.lp_den))),
            priceDen: Number(payload.lp_den),
            priceNum: Number(payload.lp_num),
            priceType
          };
          // nullify suspension place as we don`t need to check disable/unable status when price is changed
          this.suspensionPlace = '';
        }
        break;

      case 'sSELCN':
        if (payload.lp_num || payload.lp_den) {
          let priceType;
          if (this.selection.price) {
            priceType = this.selection.price.priceType || this.selection.price.priceTypeRef.id;
          }
          delta = {
            priceDec: Number(this.fracToDecService.getDecimal(Number(payload.lp_num), Number(payload.lp_den))),
            priceDen: Number(payload.lp_den),
            priceNum: Number(payload.lp_num),
            priceType
          };
        }
        this.suspensionPlace = 'selection';
        break;

      case 'sEVMKT':
        this.suspensionPlace = 'market';
        delta = {};
        if (handicapValues || eachWayAvailable) {
          delta = {
            hcap_values: handicapValues,
            ew_avail : eachWayAvailable
          };
        }
        break;

      case 'sEVENT':
        this.suspensionPlace = 'event';
        delta = {};
        break;

      case 'sMHCAP':
        if (handicapValues) {
          delta = {
            hcap_values: handicapValues
          };
          if (delta.hcap_values.L) {
            delta.hcap_values.L = delta.hcap_values.H;
          }
        }
        break;

      default:
        delta = {};
        break;
    }

    return delta;
  }

  /**
   * Check is bet suspended or undisplayed on every level of event
   * @returns {boolean}
   */
  private filterGlobalDisable(obj: IQuickbetUpdateDisableMap): boolean {
    const objKeys = Object.keys(obj);
    return _.some(objKeys, element => obj[element] === true);
  }
  /**
   * checks if the isEachWayAvailable flag is upadated or not
   * @param ew_avail 
   * @param selection 
   * @returns 
   */
  private isEachWayFlagUpdated(ew_avail: string, selection: IQuickbetSelectionModel): boolean {
    const eachWayAvailable: boolean = ew_avail == 'Y';
    return (selection.isEachWayAvailable !== eachWayAvailable);
  }
}
