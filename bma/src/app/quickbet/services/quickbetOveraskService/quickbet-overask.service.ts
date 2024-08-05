import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { StorageService } from '@core/services/storage/storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IQuickbetOveraskResponseModel } from '@app/quickbet/models/quickbet-overask-response.model';
import {
  ILegPartModel,
  IQuickbetBetModel,
  ISelectionForStorageModel
} from '@app/quickbet/models/quickbet-common.model';

@Injectable({ providedIn: 'root' })
export class QuickbetOveraskService {

  constructor(
    private pubSubService: PubSubService,
    private storageService: StorageService) {
  }

  /**
   * Execute
   * @param {Object} responseData
   * @param {Object} selectionData
   */
  execute(responseData: IQuickbetOveraskResponseModel, selectionData: IQuickbetSelectionModel): void {
    const betSelections = [this.getSelectionForStorage(responseData, selectionData)];

    this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], true);
    this.storageService.set('betSelections', betSelections);
    this.pubSubService.publish(this.pubSubService.API.EXECUTE_OVERASK, responseData);
  }

  /**
   * Get selection for storage
   * @param responseData
   * @param {Object} selectionData
   * @returns {{}}
   * @private
   */
  private getSelectionForStorage({ bet }: { bet: IQuickbetBetModel[] },
                                 selectionData: IQuickbetSelectionModel): ISelectionForStorageModel {
    let userStake: string;
    if (selectionData && selectionData.freebet) {
      userStake = selectionData.stake ? parseFloat(selectionData.stake).toString() : '';
    } else {
      userStake = parseFloat(selectionData.stake).toString();
    }
    const quickBet: IQuickbetBetModel = bet[0],
      legParts: ILegPartModel[] = quickBet && quickBet.leg[0].sportsLeg.legPart,
      userEachWay: boolean = quickBet && quickBet.leg[0].sportsLeg.winPlaceRef.id === 'EACH_WAY',
      userFreeBet: string = selectionData && selectionData.freebet ? selectionData.freebet.freebetTokenId : '',
      outcomesIds: string[] = this.getOutcomeIds(legParts),
      type: string = selectionData.selectionType === 'scorecast' ? 'SCORECAST' : 'SGL',
      id: string = `${type}|${outcomesIds.join('|')}`;

    return {
      outcomesIds,
      userStake,
      userEachWay,
      userFreeBet,
      goToBetslip: false,
      id,
      price: selectionData.isLP ? selectionData.price : { priceType: 'SP' },
      type,
      typeName: selectionData.typeName,
      eventIsLive: selectionData.eventIsLive,
      hasBPG: selectionData.hasGP,
      hasEachWay: selectionData.isEachWayAvailable,
      isSuspended: ['eventStatusCode', 'marketStatusCode', 'outcomeStatusCode'].some(status => selectionData[status] === 'S')
    };
  }

  /**
   * Retrieves outcome ids from the list of leg parts in place bet response.
   * @param {Array} legParts
   * @return {Array}
   * @private
   */
  private getOutcomeIds(legParts: ILegPartModel[]): string[] {
    return _.map(legParts, legPart => legPart.outcomeRef.id);
  }
}

