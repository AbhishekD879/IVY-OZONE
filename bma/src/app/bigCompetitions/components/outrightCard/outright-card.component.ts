import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IParticipantFromName } from '@app/bigCompetitions/services/participants/participants.model';

@Component({
  selector: 'card-view',
  templateUrl: './outright-card.component.html'
})
export class CardViewComponent implements OnInit {

  @Input() eventEntity: ISportEvent;
  @Input() market: IMarket;
  @Input() maxDisplay: number;
  @Input() moduleTitle?: number;

  gtmModuleTitle: string;
  limit: number;
  hideShowNext: boolean;
  id: string;

  constructor() {}

  ngOnInit(): void {
    this.limit = this.maxDisplay;
    this.hideShowNext = this.limit < this.market.outcomes.length;
    this.id = _.uniqueId();
  }

  /**
   * Show next market outcomes
   */
  showNext(): void {
    this.limit = this.limit + this.maxDisplay;
    this.hideShowNext = this.limit < this.market.outcomes.length;
  }

  trackByFn(index: number, item: IOutcome): string {
    return `${index}${item.id}`;
  }

  /**
   * Create selection name.
   */
  getOutcomeName(participants: IParticipantFromName): string {
    this.hideShowNext = this.limit < this.market.outcomes.length;
    return participants.AWAY ? `${participants.HOME.name} vs ${participants.AWAY.name}` : participants.HOME.name;
  }
}
