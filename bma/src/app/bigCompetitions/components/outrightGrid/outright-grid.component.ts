import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { TemplateService } from '@shared/services/template/template.service';
import { TimeService } from '@core/services/time/time.service';
import { IOutcome } from '@core/models/outcome.model';
import { IParticipantFromName } from '@app/bigCompetitions/services/participants/participants.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';

@Component({
  selector: 'grid-view-widget',
  templateUrl: './outright-grid.html',
  styleUrls: ['./outright-grid.component.scss']
})
export class GridViewWidgetComponent implements OnInit {

  @Input() eventEntity: ISportEvent;
  @Input() market: IMarket;
  @Input() maxDisplay: number;
  @Input() gtmModuleTitle?: string;

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
      this.market.terms = this.templateService.genTerms(this.market).toUpperCase();
    }
  }

  limitTo(outcomes: IOutcome[]): IOutcome[] {
    this.outcomesCount = this.market.outcomes.length;
    if (this.limit) {
      return outcomes.slice(0, this.limit);
    }
    return outcomes;
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

  /*
   * Create selection name.
   */
  getOutcomeName(participants: IParticipantFromName): string {
    return participants.AWAY ? `${participants.HOME.name} vs ${participants.AWAY.name}` : participants.HOME.name;
  }

  /*
   * Check if outcomes count is 2/4
   */
  isTwoColumns(): boolean {
    return this.limit && this.limit < this.outcomesCount ? this.limit === 2 || this.limit === 4
                      : this.outcomesCount === 2 || this.outcomesCount === 4;
  }
}
