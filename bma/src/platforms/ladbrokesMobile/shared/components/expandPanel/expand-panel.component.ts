import { Component, ViewEncapsulation } from '@angular/core';
import { ExpandPanelComponent as AppExpandPanelComponent } from '@app/shared/components/expandPanel/expand-panel.component';

@Component({
  selector: 'expand-panel',
  templateUrl: 'expand-panel.component.html',
  styleUrls: ['expand-panel.component.scss'],
  encapsulation:ViewEncapsulation.None
})

export class ExpandPanelComponent extends AppExpandPanelComponent {}
