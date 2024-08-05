import { Component } from '@angular/core';
import {
  RacingTooltipComponent as CoralRacingTooltipComponent
} from '@lazy-modules/market-description/components/racing-tooltip/racing-tooltip.component';

@Component({
  selector: 'racing-tooltip',
  template: `<div class="tooltip tooltip-container">
    <ng-content></ng-content>
  </div>`,
  styleUrls: ['./racing-tooltip.component.scss']
})
export class RacingTooltipComponent extends CoralRacingTooltipComponent {}
