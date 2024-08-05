import { Component } from '@angular/core';

@Component({
  selector: 'racing-tooltip',
  template: `<div class="tooltip tooltip-container">
    <ng-content></ng-content>
  </div>`,
  styleUrls: ['./racing-tooltip.component.scss']
})
export class RacingTooltipComponent {}
