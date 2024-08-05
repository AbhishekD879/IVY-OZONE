import { Component, OnInit, Input } from '@angular/core';
import * as _ from 'underscore';

import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'race-list',
  templateUrl: 'race-list.component.html',
  styleUrls: ['race-list.component.scss']
})
export class RaceListComponent implements OnInit {

  @Input() events: ISportEvent[];
  @Input() expanded: boolean;
  @Input() limit: number;
  @Input() sportName: string;
  @Input() eventsOrder: string[];

  orderedEvents: ISportEvent[];

  limited: number;
  private readonly PAGE_LIMIT = 9999;

  constructor(
    private lpAvailability: LpAvailabilityService,
    private routingHelperService: RoutingHelperService,
    private timeService: TimeService
  ) { }

  ngOnInit(): void {
    this.limited = this.limit;
    this.orderedEvents = this.orderEvents(this.events);
  }

  isLpAvailable(eventEntity: ISportEvent): boolean {
    return this.lpAvailability.check(eventEntity);
  }

  getLink(sportName: string, eventEntity: ISportEvent): string {
    if (sportName === 'tote') {
      return eventEntity.isResulted
        ? `/${sportName}/results`
        : `/${sportName}/event/${eventEntity.id}`;
    }
    return this.routingHelperService.formResultedEdpUrl(eventEntity);
  }

  showMore(): void {
    this.limited = this.limited + this.limit;
    this.orderedEvents = this.orderEvents(this.events);
  }

  getIconName(): string {
    return this.sportName === 'greyhound' ? '#greyhound-icon' : '#horseracing-icon';
  }

  getRaceTime(eventEntity: ISportEvent): string {
    return `${eventEntity.localTime} ${eventEntity.typeName}`;
  }

  private orderEvents(events: ISportEvent[]): ISportEvent[] {
    return _.sortBy(events, (eventEntity: ISportEvent) => {
      return this.getSortFields(eventEntity);
    }).splice(0, this.limited || this.PAGE_LIMIT);
  }

  private getSortFields(eventEntity: ISportEvent): string {
    return _.reduce(this.eventsOrder, (res, field) => {
      if (field === 'localTime' && eventEntity[field]) {
        eventEntity[field] = this.timeService.formatHours(eventEntity[field]);
      }
      return `${res}_${eventEntity[field]}`;
    }, '');
  }

}
