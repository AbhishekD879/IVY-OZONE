import { Component, ViewEncapsulation } from '@angular/core';

import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';

@Component({
  selector: 'quickbet-panel',
  templateUrl: './quickbet-panel.component.html',
  styleUrls: ['quickbet-panel.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class LadbrokesQuickbetPanelComponent extends QuickbetPanelComponent {}
