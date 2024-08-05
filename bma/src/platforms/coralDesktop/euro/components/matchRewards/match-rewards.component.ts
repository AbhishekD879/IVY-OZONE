import { Component } from '@angular/core';
import { MatchRewardsComponent } from '@euro/components/matchRewards/match-rewards.component';

@Component({
  selector: 'match-rewards',
  templateUrl: './match-rewards.component.html',
  styleUrls: ['./match-rewards.component.scss']
})

export class DesktopMatchRewardsComponent extends MatchRewardsComponent {}
