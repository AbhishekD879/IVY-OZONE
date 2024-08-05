import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  CompetitionFiltersComponent as AppCompetitionFiltersComponent
} from '@lazy-modules/competitionFilters/components/competitionFilters/competition-filters.component';

@Component({
  selector: 'competition-filters',
  templateUrl: '../../../../../../app/lazy-modules/competitionFilters/components/competitionFilters/competition-filters.component.html',
  styleUrls: [
    '../../../../../../app/lazy-modules/competitionFilters/components/competitionFilters/competition-filters.component.scss',
    './competition-filters.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CompetitionFiltersComponent extends AppCompetitionFiltersComponent {}
