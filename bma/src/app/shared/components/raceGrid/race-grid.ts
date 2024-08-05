import { Component, Input, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { TimeService } from '@core/services/time/time.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRaceGridMeetingTote, IRaceGridMeeting, IClassTypeName } from '@core/models/race-grid-meeting.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

@Component({
  selector: 'race-grid',
  templateUrl: './race-grid.html',
  styleUrls: ['./race-grid.scss']
})
export class RaceGridComponent implements OnInit {
  @Input() raceType: string;
  @Input() eventsData: IRaceGridMeetingTote[] & IRaceGridMeeting;
  @Input() eventsOrder: Array<string>;
  @Input() meetingsOrder?: Array<string>;
  @Input() racingGroup?: ISportEvent[];
  @Input() racingGroupFlag?: string;
  @Input() sportName?: string;

  public meetings: (IRaceGridMeetingTote | ISportEvent | IClassTypeName)[];

  public isTote: boolean;

  constructor(
    private timeService: TimeService,
    private locale: LocaleService,
    private lpAvailability: LpAvailabilityService,
    private datePipe: DatePipe,
    private routingHelperService: RoutingHelperService
  ) {

  }

  ngOnInit(): void {
    this.isTote = this.raceType === 'tote';
    this.sortAndFillMeetings();
  }

  /**
   * Get Full Date
   * @returns {string}
   */
  getFullDate(): string {
    const currentDate: Date = new Date();
    const getDayNumber: string = this.datePipe.transform(currentDate, 'd'); //
    const getDay: string = this.isTote ? this.datePipe.transform(currentDate, 'EEEE')
      : this.locale.getString(this.timeService.getDayI18nValue(currentDate.toString()));
    const getMonth: string = this.isTote ? this.datePipe.transform(currentDate, 'MMM')
      : this.locale.getString(this.timeService.getMonthI18nValue(currentDate, false));
    return `${getDay} ${getDayNumber} / ${getMonth}`;
  }

  /**
   * Get Race Type Icon
   * @returns {string}
   */
  raceTypeIcon(): string {
    const raceTypeId: string = this.isTote ? this.eventsData[0].events[0].categoryId
      : this.eventsData.events[0] ? this.eventsData.events[0].categoryId : '0';

    return `#${Number(raceTypeId) === 19 ? 'greyhound' : 'horseracing'}-icon`;
  }

  /**
   * Check if Live Price available
   * @param {Object} event
   * @returns {Boolean}
   */
  isLpAvailable(event: ISportEvent): boolean {
    return this.lpAvailability.check(event);
  }

  /**
   * Generate URL for event details page or results page
   * @param {string} eventEntity
   */
  genEventDetailsUrl(eventEntity: ISportEvent | IRaceGridMeetingTote | any): string {
    let eventUrl = '';

    if (this.isTote) {
      eventUrl += `/tote`;
      eventUrl += eventEntity.isResulted ? `/results` : `/event/${eventEntity.id}`;
    } else {
      eventUrl += this.routingHelperService.formResultedEdpUrl(eventEntity);
    }

    return eventUrl;
  }

  trackById(index: number, event: ISportEvent): string {
    return event.id ? `${index}${event.id}` : index.toString();
  }

  /**
   * Ordering events according to provided order
   * @param meeting
   * @returns {Object}
   */
  orderEvents(meeting: IRaceGridMeetingTote | ISportEvent | any): (IRaceGridMeetingTote | ISportEvent)[] {
    const racingGroupFiltered = this.isTote ? meeting.events
      : _.filter(this.racingGroup, race => race.typeName === meeting.name);
    return this.orderData(racingGroupFiltered, this.eventsOrder);
  }

  /**
   * Order meetings according to provided order
   */
  private sortAndFillMeetings(): void {
    this.meetings = this.isTote ? this.orderData(this.eventsData, this.meetingsOrder)
      : _.sortBy(this.eventsData.classesTypeNames[this.racingGroupFlag], 'name');
  }

  /**
   * Sorts data by several params
   * @param {Array<IRaceGridMeetingTote | ISportEvent>} items
   * @param {Array<string>} order
   * @return {Array<IRaceGridMeetingTote | ISportEvent>}
   */
  private orderData(items: (IRaceGridMeetingTote | ISportEvent)[], order: Array<string>): (IRaceGridMeetingTote | ISportEvent)[] {
    return _.sortBy(items, (item: IRaceGridMeetingTote | ISportEvent) => {
      return this.getSortFields(item, order);
    });
  }

  /**
   * Returns property for sorting
   * @param {IRaceGridMeetingTote | ISportEvent} item
   * @param {Array<string>} order
   * @return {string}
   */
  private getSortFields(item: IRaceGridMeetingTote | ISportEvent, order: Array<string>): string {
    return _.reduce(order, (res, field) => {
      if (field === 'localTime' && item[field]) {
        item[field] = this.timeService.formatHours(item[field]);
      }
      return `${res}_${item[field]}`;
    }, '');
  }
}
