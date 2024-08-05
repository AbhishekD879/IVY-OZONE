import { Component, Input, Output, EventEmitter } from '@angular/core';

import {
  RacingFeaturedComponent as MainRacingFeaturedComponent
} from '@app/lazy-modules/racingFeatured/components/racingFeatured/racing-featured.component';

@Component({
  selector: 'racing-featured',
  templateUrl: './racing-featured.component.html'
})
export class RacingFeaturedComponent extends MainRacingFeaturedComponent {
  @Input() isEnabledCardState: boolean;
  @Input() isLimitReached: boolean;
  @Input() isClearBuildCardState: boolean;

  @Output() readonly fetchCardId = new EventEmitter();

  emitFetchCardId(event): void {
    this.fetchCardId.emit(event);
  }
}
