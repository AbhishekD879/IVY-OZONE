import { Component } from '@angular/core';

@Component({
  selector: 'tooltip',
  template: `<div class="tooltip tooltip-container">
    <ng-content></ng-content>
  </div>`,
  styleUrls: ['./tooltip.component.scss']
})
export class TooltipComponent {}
