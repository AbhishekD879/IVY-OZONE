import { Component, Input } from '@angular/core';

import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';

@Component({
  selector: 'uk-tote-selections-overview',
  templateUrl: './uk-tote-selection-overwiew.component.html'
})
export class UkToteSelectionOverwiewComponent {

  @Input() poolBet: TotePotBet;
  @Input() expanded: boolean;

  readonly LIST_ITEM_HEIGHT = 40;
  readonly MAX_ITEMS_TO_SHOW = 4;
  readonly ADDITIONAL_BOTTOM_OFFSET = 20;

  constructor(
    private pubsub: PubSubService
  ) { }

  trackBySelectedOutcome(index: number, outcome: IOutcome): string {
    return outcome.id;
  }

  /**
   * Get name of selection
   * @param {Object} outcome - outcome entity
   * @returns {string}
   */
  getSelectionName(outcome: IOutcome): string {
    return !outcome.isFavourite ? `${outcome.runnerNumber}. ${outcome.name}` : outcome.name;
  }

  /**
   * Deselect outcome
   * @param outcome - outcome entity.
   */
  deselectOutcome(outcome: IOutcome): void {
    const linkedLeg = this.poolBet.getOutcomeLinkedLeg(outcome);
    linkedLeg.deselectOutcome(outcome.id);
    this.pubsub.publish(this.pubsub.API.UK_TOTE_LEG_UPDATED, linkedLeg);
  }
}
