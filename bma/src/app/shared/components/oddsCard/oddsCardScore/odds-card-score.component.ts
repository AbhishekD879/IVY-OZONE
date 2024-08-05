import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { ITypedScoreData } from '@core/services/scoreParser/models/score-data.model';

@Component({
  selector: 'odds-card-score',
  styleUrls: ['./odds-card-score.component.scss'],
  templateUrl: './odds-card-score.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OddsCardScoreComponent {
  @Input() score: string[][];
  @Input() showServingTeam?: boolean;
  @Input() servingTeams?: number[];
  @Input() isHeaderShown?: boolean;
  @Input() boxScore?: ITypedScoreData;
  @Input() isHomeDrawAwayType: boolean = true;
  @Input() scoreHeaders?: string[];
  @Input() scoreClass?: boolean;
  @Input() platform?: string;
  @Input() emptyScore?: boolean;
  trackByIndex(index: number): number {
    return index;
  }
}
