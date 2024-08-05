import { Component, OnInit, Input } from '@angular/core';
import { BigCompetitionsSpecialsService } from '@app/bigCompetitions/services/bigCompetitionsSpecials/big-competitions-specials-service';
import { IGroupedByDateItem, IGroupedByDateObj, ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';

@Component({
  selector: 'competition-specials-view',
  templateUrl: 'competition-specials-view.component.html'
})
export class CompetitionSpecialsViewComponent implements OnInit {
  @Input() openMarketTabs: boolean[];
  @Input() initialData: ITypeSegment[];
  @Input() eventsBySections: ITypeSegment[];
  @Input() showLimit: number;
  @Input() inner: boolean;
  @Input() viewAllUrl: string;

  showAllGroupedByDate: boolean;
  groupedLimit: number = 10;

  constructor(
    private bigCompetitionsSpecialsService: BigCompetitionsSpecialsService,
    private filtersService: FiltersService,
  ) {}

  ngOnInit(): void {
    this.viewAllUrl = this.filtersService.filterLink(this.viewAllUrl);
    this.openMarketTabs[0] = true;
    this.showAllGroupedByDate = !this.showLimit;
    this.eventsBySections = this.orderedSections(this.eventsBySections);
    _.each(this.eventsBySections, (eventsBySection: ITypeSegment) => {
      if (eventsBySection.typeName === 'Enhanced Multiples') {
        eventsBySection.groupedByDate = this.groupedEvents(eventsBySection.groupedByDate);
      }
    });
  }

  isShowButtonEnabled(eventsBySection: ITypeSegment): boolean {
    return this.showLimit && eventsBySection.typeName !== 'Enhanced Multiples' && eventsBySection.events.length > this.showLimit;
  }

  isShowButtonForGroupedByDateEnabled(groupedByDate: IGroupedByDateItem[]): boolean {
    groupedByDate = _.toArray(groupedByDate);
    return this.bigCompetitionsSpecialsService.isShowButtonForGroupedByDateEnabled(groupedByDate, this.showLimit);
  }

  trackByIndex(index: number): number {
    return index;
  }

  trackById(index: number, event: ISportEvent): string {
    return `${index}${event.id}`;
  }

  orderedSections(eventsBySection: ITypeSegment[]): ITypeSegment[] {
    return _.sortBy(eventsBySection, 'typeDisplayOrder');
  }

  limitTo(eventsBySection: ITypeSegment): ISportEvent[] {
    if (!eventsBySection.showAll && this.showLimit) {
      return eventsBySection.events.slice(0, this.showLimit);
    }
    return eventsBySection.events;
  }

  groupedEvents(groupedEvents:  IGroupedByDateObj): IGroupedByDateObj {
    _.each(groupedEvents, (groupedEvent: IGroupedByDateItem) => {
      _.each(groupedEvent.events, (event: ISportEvent) => {
        const outcomesCount: number = event.markets[0].outcomes.length;

        if (this.groupedLimit > outcomesCount) {
          event.groupedLimit = outcomesCount;
          this.groupedLimit = this.groupedLimit - outcomesCount;
        } else {
          event.groupedLimit = this.groupedLimit;
          this.groupedLimit = 0;
        }
      });
    });

    return groupedEvents;
  }

  showGroupedHeader(grouped: IGroupedByDateItem): boolean {
    return _.some(grouped.events, event => event.groupedLimit > 0) || this.showAllGroupedByDate;
  }
}
