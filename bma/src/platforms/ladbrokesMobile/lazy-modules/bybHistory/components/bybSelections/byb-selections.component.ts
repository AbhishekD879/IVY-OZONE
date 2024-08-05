import { Component, ChangeDetectionStrategy } from '@angular/core';

import { BybSelectionsComponent } from '@lazy-modules/bybHistory/components/bybSelections/byb-selections.component';

@Component({
  selector: 'byb-selections',
  templateUrl: '../../../../../../app/lazy-modules/bybHistory/components/bybSelections/byb-selections.component.html',
  styleUrls: [
    '../../../../../../app/lazy-modules/bybHistory/components/bybSelections/byb-selections.component.scss',
    './byb-selections.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesBybSelectionsComponent extends BybSelectionsComponent {}
