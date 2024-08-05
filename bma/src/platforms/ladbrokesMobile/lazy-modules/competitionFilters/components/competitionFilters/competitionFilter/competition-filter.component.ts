import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  CompetitionFilterComponent as AppCompetitionFilterComponent
} from '@lazy-modules/competitionFilters/components/competitionFilters/competitionFilter/competition-filter.component';

@Component({
  selector: 'competition-filter',
  // eslint-disable-next-line max-len
  templateUrl: '../../../../../../../app/lazy-modules/competitionFilters/components/competitionFilters/competitionFilter/competition-filter.component.html',
  styleUrls: [
    // eslint-disable-next-line max-len
    '../../../../../../../app/lazy-modules/competitionFilters/components/competitionFilters/competitionFilter/competition-filter.component.scss',
    './competition-filter.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CompetitionFilterComponent extends AppCompetitionFilterComponent {}
