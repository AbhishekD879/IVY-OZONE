import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BetSelections } from '@betslip/services/betSelections/bet-selections';
import { IBetSelection, IParams } from '@betslip/services/betSelection/bet-selection.model';
import { IOutcome } from '@core/models/outcome.model';
import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetSelection } from '@betslip/services/betSelection/bet-selection';


@Injectable({ providedIn: BetslipApiModule })
export class BetSelectionsService extends BetSelections {
  static ngInjectableDef = undefined;

  constructor(
    public pubSubService: PubSubService
  ) {
    super(pubSubService);
  }

  addSelection(selection: IBetSelection): void {
    this.selectionsData.push(selection);
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, this.selectionsData);
  }

  removeSelection(selection: IBetSelection): void {
    const index = this.selectionsData.indexOf(selection);
    this.selectionsData.splice(index, 1);
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, this.selectionsData);
  }
  
  /**
   * @param {BetSelection[]} selections
   * @memberof BetSelectionsService
   */
  removeMultiSelection(selections: BetSelection[]): void {
    _.each(selections, selection => {
      const index = this.selectionsData.indexOf(selection);
      this.selectionsData.splice(index, 1);
    });
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, this.selectionsData);
  }

  updateSelection(updatedSelection:IBetSelection) {
    const index = this.selectionsData.findIndex(selection => updatedSelection.id.toString().includes(selection.id));
    this.selectionsData[index] = updatedSelection;
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, this.selectionsData);
  }

  removeSelectionById(id: number): void {
    const selection: IBetSelection = _.findWhere(this.selectionsData, { id });
    this.removeSelection(selection);
  }

  getOutcome(outcomeId: string | number): IBetSelection | IOutcome {
    return this.selectionsData.reduce((result, sel) => {
      return _.find(sel.outcomes, { id: outcomeId }) || result;
    }, null);
  }

  findById(id: string, isLotto: boolean = false, priceId: string = ''): IBetSelection {
    let betFound: IBetSelection;

    if (id.includes('SCORECAST')) {
      if (this.selectionsData.length) {
        const filteredBet = _.filter(this.selectionsData, selection => {
          return _.every(id.split('|'), (item: string) => selection.id.includes(item));
        });
        betFound = filteredBet[0];
      }
    } else if(isLotto) {
      betFound = this.selectionsData.find(selection => id.includes(selection.id) && priceId === selection.details.priceId);
    } else {
      betFound = _.find(this.selectionsData, { id });
    }
    if (!betFound) {
      _.forEach(this.selectionsData, (selection: IBetSelection) => {
        if (selection.id == id || (selection.params && selection.params.id === id)) {
          betFound = selection;
        }
      });
    }
    return betFound;
  }

  flush(): void {
    this.selectionsData = [];
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, this.selectionsData);
  }

  count(): number {
    return this.selectionsData.length;
  }

  mapParsed(params: IParams): IBetSelection {
    const type = this.getBetType(params);
    const id = `${type}|${params.outcomes.map((outcome: IOutcome) => outcome.id).join('|')}`;
    return this.findById(id);
  }

  private getBetType(params: IParams): string {
    const type = params.combi || 'SGL';

    if (
      /^(FORE|TRI)CAST$/.test(type) &&
      params.legParts.some((part: ILegPart) => part.places === '*')
    ) {
      return `${type}_COM`;
    }

    return type;
  }
}
