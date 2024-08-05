import { Component, Input, ViewEncapsulation } from '@angular/core';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportEvent } from '@core/models/sport-event.model';

@Component({
  selector: 'competitions-outrights-tab',
  templateUrl: 'competitions-outrights-tab.component.html',
  styleUrls: ['competitions-outrights-tab.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class CompetitionsOutrightsTabComponent {
  @Input() outrights: ISportEvent[];
  @Input() isLoaded: boolean;

  constructor(
    private routingHelper: RoutingHelperService
  ) {}

  /**
   * Track event
   * @param {ISportEvent} event
   * @returns {any}
   */
  trackById(event: ISportEvent): number {
    return event.id;
  }

  /**
   * Redirects to event details page
   * @param event
   * @returns {*}
   */
  eventURL(event: ISportEvent): string {
    return this.routingHelper.formEdpUrl(event);
  }
}
