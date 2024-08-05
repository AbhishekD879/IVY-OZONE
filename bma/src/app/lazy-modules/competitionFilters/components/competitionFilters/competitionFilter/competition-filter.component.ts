import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';

@Component({
  selector: 'competition-filter',
  templateUrl: './competition-filter.component.html',
  styleUrls: ['./competition-filter.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CompetitionFilterComponent {
  @Input() filter: ICompetitionFilter;
  @Output() readonly filterChange: EventEmitter<ICompetitionFilter> = new EventEmitter<ICompetitionFilter>();

  /**
   * Emits filter to the parent component
   * @param {ICompetitionFilter} filter
   */
  onFilterSelect(filter: ICompetitionFilter): void {
    filter.active = !filter.active;

    this.filterChange.emit(filter);
  }
}
