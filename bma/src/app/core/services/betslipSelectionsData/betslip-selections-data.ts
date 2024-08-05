import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { IQuickbetSelectionModel } from '../../models/quickbet-selection.model';
import { StorageService } from '@core/services/storage/storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

export interface IEmptySelectionWithPrice {
  price: {
    priceType: string;
  };
}

@Injectable()
export class BetslipSelectionsDataService {
  private selections: IBetSelection[];
  private quickbetSelection: IQuickbetSelectionModel;

  constructor(
    private pubsubService: PubSubService,
    private storageService: StorageService
  ) {
    this.selections = this.storageService.get('betSelections') || [];
  }

  subscribe(): void {
    this.pubsubService.subscribe(
      'betSlipSelectionsData',
      this.pubsubService.API.BETSLIP_SELECTIONS_UPDATE,
      (...args: IBetSelection[]) => {
        this.selections = args;
      });

    this.pubsubService.subscribe(
      'betSlipSelectionsData',
      this.pubsubService.API.QUICKBET_OPENED,
      (qbSelection: IQuickbetSelectionModel) => {
        this.quickbetSelection = qbSelection;
      });

    this.pubsubService.subscribe('betSlipSelectionsData', this.pubsubService.API.QUICKBET_PANEL_CLOSE, () => {
      this.quickbetSelection = null;
    });
  }

  /**
   * Returns selections count that are in the betSlip module
   * @returns {Number}
   */
  count(): number {
    return this.selections.length;
  }

  /**
   * Returns boolean value that corresponds is selection in betSlip
   * @param {string[]} outcomeIds
   * @param {string[]} qbOutcomeIds
   * @returns {boolean}
   */
  contains(outcomeIds: string[], qbOutcomeIds: string[]): boolean {
    let isInBetslipSelections = false;
    const isInQuickbetSelection = this.quickbetSelection &&
      _.every(qbOutcomeIds, (outcomeId: string) => this.quickbetSelection.outcomeId.indexOf(outcomeId) !== -1);

    _.each(this.selections, (selection: IBetSelection) => {
      if (selection.params && selection.params.id && _.every(outcomeIds, outcomeId => selection.params.id.indexOf(outcomeId) !== -1)
       || _.every(outcomeIds, (outcomeId: string) => (<string>selection.id).indexOf(outcomeId) !== -1)) {
        isInBetslipSelections = true;
      }
    });

    return isInBetslipSelections || isInQuickbetSelection;
  }

  /*
  * Get quickbet selection object
  * @returns {object}
  * */
  getQuickbetSelection(): IQuickbetSelectionModel {
    return this.quickbetSelection;
  }

  /**
   * Returns selection by id from betSlip selections
   * @param outcomeId
   * @returns {Array.<T>}
   */
  getSelectionsByOutcomeId(outcomeId: string): (IBetSelection | IEmptySelectionWithPrice)[]  {
    const betslipSelections = this.selections.filter((selection: IBetSelection) => {
      const outcomes = selection.outcomesIds || _.pluck(selection.outcomes, 'id');
      return outcomes.length === 1 && outcomes.includes(outcomeId);
    });

    if (betslipSelections.length) {
      return betslipSelections;
    }

    const quickbetSelection = this.quickbetSelection &&
                                this.quickbetSelection.outcomeId === outcomeId;

    if (quickbetSelection) {
      return [{
        price: {
          priceType: this.quickbetSelection.price ? this.quickbetSelection.price.priceType : 'SP'
        }
      }];
    }

    return [];
  }
}
