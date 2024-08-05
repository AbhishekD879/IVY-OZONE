import {
  Component,
  OnInit,
  OnDestroy,
  Input,
  Output,
  EventEmitter,
  ChangeDetectionStrategy,
  ChangeDetectorRef
} from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';
import { Subscription } from 'rxjs';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'competition-filters',
  templateUrl: './competition-filters.component.html',
  styleUrls: ['./competition-filters.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CompetitionFiltersComponent implements OnInit, OnDestroy {
  @Input() filters: ICompetitionFilter[] = [];
  @Input() isCompetitionsPage: boolean = false;
  @Input() sportId: string;
  @Input() marginTop: boolean = false;
  @Input() paddingTop: boolean = false;

  @Output() readonly filterChange: EventEmitter<ICompetitionFilter> = new EventEmitter<ICompetitionFilter>();

  private routeSubscription: Subscription;

  constructor(
    private activatedRoute: ActivatedRoute,
    private changeDetectorRef: ChangeDetectorRef,
    private gtmService: GtmService
  ) {
  }

  ngOnInit(): void {
    this.routeSubscription = this.activatedRoute.params
      .subscribe((params: Params) => {
        if ((params.typeName && params.className) || params.tab === 'today') {
          this.filters = this.filters.map((filter: ICompetitionFilter) => ({ ...filter, active: false }));

          this.changeDetectorRef.detectChanges();
        }
      });
  }

  ngOnDestroy(): void {
    this.routeSubscription && this.routeSubscription.unsubscribe();
  }

  /**
   * Emits selected filter to parent and marks only it as active
   * @param {ICompetitionFilter} event
   */
  onFilterChange(event: ICompetitionFilter): void {
    this.filters = this.filters.map((filter: ICompetitionFilter) => {
      if (filter.type === event.type && filter.id !== event.id) {
        filter.active = false;
      }

      return { ...filter };
    });

    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'time filters',
      eventAction: event.name,
      eventLabel: event.active === true ? 'select' : 'deselect',
      categoryID: this.sportId
    });

    this.filterChange.emit(event);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }
}
