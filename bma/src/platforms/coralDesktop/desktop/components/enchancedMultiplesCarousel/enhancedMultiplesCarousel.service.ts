import { Injectable } from '@angular/core';

import { EnhancedMultiplesService } from '@app/sb/services/enhancedMultiples/enhanced-multiples.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { TimeService } from '@core/services/time/time.service';
import { Observable } from 'rxjs';

@Injectable()
export class EnhancedMultiplesCarouselService {

  constructor(private enhancedMultiplesService: EnhancedMultiplesService,
              private filtersService: FiltersService,
              private timeService: TimeService) {
  }

  /**
   * Returns all enhanced multiples events for a sport.
   * @param sportName {string}
   * @returns Observable<ISportEvent[]>
   */
  getEnhancedMultiplesEvents(sportName: string): Observable<ISportEvent[]> {
    return this.enhancedMultiplesService.getEnhancedMultiplesEvents(sportName);
  }

  /**
   * Build events for different sports
   * @param events {array}
   * @returns {array} of sorted events
   */
  buildEnhancedMultiplesData(events: ISportEvent[], sportName: string): ISportEvent[] {
    return sportName === 'horseracing'
      ? this.sortOutcomesByDateAndName(events).filter((event: ISportEvent) =>
        event.eventStatusCode !== 'S')
      : this.sortOutcomesByDateAndName(events);
    }

  /**
   * Set event to outcome and add additional properties to outcome based on event.
   * @param event {object}
   * @param events {array}
   * @private
   */
  setEventDate(events: ISportEvent[]): void {
    events.forEach((event: ISportEvent) => {
      event.time = this.parseTime(event.startTime);
      event.dateTime = new Date(event.startTime).toLocaleString();
    });
  }

  /**
   * Sort outcomes array by date and name;
   * @param events {array}
   * @returns {array} of sorted events
   * @private
   */
  private sortOutcomesByDateAndName(events: ISportEvent[]): ISportEvent[] {
    return this.filtersService.chainSort(events, [
      'categoryDisplayOrder',
      'startTime',
      'markets[0].outcomes[0].name',
      'name'
    ]);
  }

  /**
   * Transform timestamp to time string e.g. 5:14 pm.
   * @param timestamp {timestamp}
   * @returns {string}
   * @private
   */
  private parseTime(timestamp: string): string {
    return this.timeService.getEventTime(`${new Date(timestamp)}`);
  }
}
