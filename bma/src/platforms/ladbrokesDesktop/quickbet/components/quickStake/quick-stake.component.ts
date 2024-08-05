import { Component } from '@angular/core';
import { QuickStakeComponent } from '@app/quickbet/components/quickStake/quick-stake.component';

@Component({
  selector: 'quick-stake',
  templateUrl: '../../../../../app/quickbet/components/quickStake/quick-stake.component.html',
  styleUrls: ['../../../../../app/quickbet/components/quickStake/quick-stake.component.scss', 'quick-stake.component.scss']
})
export class LadbrokesDeskQuickStakeComponent extends QuickStakeComponent {}
