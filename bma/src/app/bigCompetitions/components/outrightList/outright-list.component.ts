import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { TemplateService } from '@shared/services/template/template.service';
import { TimeService } from '@core/services/time/time.service';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'list-view-widget',
  templateUrl: './outright-list.html'
})
export class ListViewWidgetComponent implements OnInit {

  @Input() eventEntity: ISportEvent;
  @Input() market: IMarket;
  @Input() maxDisplay: number;
  @Input() moduleTitle?: number;

  limit: number;
  outcomesCount: number;
  id: string;

  constructor(
    private templateService: TemplateService,
    private timeService: TimeService
  ) {}

  ngOnInit(): void {
    this.limit = this.maxDisplay;
    this.outcomesCount = this.market.outcomes.length;
    this.id = _.uniqueId();

    if (this.market.isEachWayAvailable) {
      this.market.terms = this.templateService.genTerms(this.market);
    }
  }

  limitTo(events: IOutcome[]): IOutcome[] {
    this.outcomesCount = this.market.outcomes.length;
    if (this.limit) {
      return events.slice(0, this.limit);
    }
    return events;
  }

  trackByFn(index: number, item: IOutcome): string {
    return `${index}${item.id}`;
  }

  /*
   * Expand/Hide selections
   */
  expandSelections(): void {
    this.limit = !this.limit ? this.maxDisplay : null;
  }

  /*
   * Set terms in header, or date if terms don`t exist.
   */
  setHeader(): string {
    return this.timeService.formatByPattern(new Date(this.eventEntity.startTime), 'EEEE, dd-MMM-yy h:mm a').replace("AM", "am").replace("PM","pm");
  }
}

