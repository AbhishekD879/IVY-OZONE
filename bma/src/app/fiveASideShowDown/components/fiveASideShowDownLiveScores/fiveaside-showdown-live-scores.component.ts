import { Component, Input } from '@angular/core';
import { SHOWDOWN_CARDS } from '@app/fiveASideShowDown/constants/constants';
@Component({
  selector: 'fiveaside-showdown-live-scores',
  template: ``
})

export class FiveASideShowdownLiveScoresComponent {
  @Input() isMatchFullTime: boolean;
  @Input() homeScore: number;
  @Input() awayScore: number;
  readonly SIMPLE = SHOWDOWN_CARDS.SIMPLE;
  animatingComponentId = '1';
  animationDelay = SHOWDOWN_CARDS.ANIMATION_DELAY;
}
