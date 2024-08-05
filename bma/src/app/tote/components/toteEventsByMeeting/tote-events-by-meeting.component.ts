import { Component, Input, OnInit } from '@angular/core';

import { TOTE_CONFIG } from '../../tote.constant';

import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';

import { IRaceGridMeeting } from '@core/models/race-grid-meeting.model';
import { IToteEvent } from './../../models/tote-event.model';

@Component({
  selector: 'tote-events-by-meeting',
  templateUrl: './tote-events-by-meeting.component.html'
})
export class ToteEventsByMeetingComponent implements OnInit {
  @Input() meetings: IRaceGridMeeting[];

  meetingsOrder: string[];
  eventsOrder: string[];

  constructor(
    private lpAvailability: LpAvailabilityService,
  ) { }

  ngOnInit(): void {
    this.meetingsOrder = TOTE_CONFIG.order.BY_MEETINGS_ORDER;
    this.eventsOrder = TOTE_CONFIG.order.EVENTS_ORDER;
    this.meetings = this.meetings || [];
  }

  /**
   * Check if Live Price available
   * @param event
   * @returns {boolean} true or false
   */
  isLpAvailable(event: IToteEvent): boolean {
    return this.lpAvailability.check(event);
  }
}
