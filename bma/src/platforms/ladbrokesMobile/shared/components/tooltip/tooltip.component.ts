import { Component } from '@angular/core';

import { TooltipComponent as BaseTooltipComponent } from '@shared/components/tooltip/tooltip.component';

@Component({
  selector: 'tooltip',
  template: `<div class="tooltip tooltip-container">
    <ng-content></ng-content>
  </div>`,
  styleUrls: ['./tooltip.component.scss']
})
export class TooltipComponent extends BaseTooltipComponent {}
