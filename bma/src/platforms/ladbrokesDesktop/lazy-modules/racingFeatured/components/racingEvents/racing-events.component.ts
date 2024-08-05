import { Component, Input, Output, EventEmitter } from '@angular/core';

import {
  RacingEventsComponent as MainRacingEventsComponent
} from '@app/lazy-modules/racingFeatured/components/racingEvents/racing-events.component';

@Component({
  selector: 'racing-events',
  templateUrl: './racing-events.component.html'
})
export class RacingEventsComponent extends MainRacingEventsComponent {
  @Input() isEnabledCardState: boolean;
  @Input() isLimitReached: boolean;
  @Input() isClearBuildCardState: boolean;

  @Output() readonly fetchCardId = new EventEmitter();

  emitFetchCardId(cardIdObj: { id: string}): void {
    this.fetchCardId.emit(Object.assign({}, cardIdObj));
  }
}

