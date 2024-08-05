import { ChangeDetectionStrategy, Component } from '@angular/core';

import { OddsCardScoreComponent as AppOddsCardScoreComponent } from '@shared/components/oddsCard/oddsCardScore/odds-card-score.component';

@Component({
  selector: 'odds-card-score',
  styleUrls: ['./odds-card-score.component.scss'],
  templateUrl: '../../../../../../app/shared/components/oddsCard/oddsCardScore/odds-card-score.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OddsCardScoreComponent extends AppOddsCardScoreComponent { }
