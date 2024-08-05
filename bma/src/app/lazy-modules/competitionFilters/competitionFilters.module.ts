import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import {
  CompetitionFiltersComponent
} from '@lazy-modules/competitionFilters/components/competitionFilters/competition-filters.component';
import {
  CompetitionFilterComponent
} from '@lazy-modules/competitionFilters/components/competitionFilters/competitionFilter/competition-filter.component';

@NgModule({
  imports: [SharedModule],
  declarations: [CompetitionFiltersComponent, CompetitionFilterComponent],
  exports: [CompetitionFiltersComponent],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CompetitionFiltersModule {
  static entry = CompetitionFiltersComponent;
}
