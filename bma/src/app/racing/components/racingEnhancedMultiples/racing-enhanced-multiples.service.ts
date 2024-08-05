/**
 * Service is used for getting and handling enhanced events data.
 */

import { Injectable } from '@angular/core';
import { EnhancedMultiplesService } from '@sb/services/enhancedMultiples/enhanced-multiples.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { TimeService } from '@core/services/time/time.service';
import { FiltersService } from '@app/core/services/filters/filters.service';

@Injectable()
export class RacingEnhancedMultiplesService {

  constructor(
    private enhancedMultiplesFactory: EnhancedMultiplesService,
    private filtersService: FiltersService,
    private timeService: TimeService
  ) { }

  /**
   * Returns all enhanced multiples events for a sport.
   * @param sportName {string}
   * @returns {*|observable}
   */
  getEnhancedMultiplesEvents(sportName: string): Observable<ISportEvent[]> {
    return this.enhancedMultiplesFactory.getRacingEnhancedMultiplesEvents(sportName)
      .pipe(
        catchError(error => {
          console.warn(error);
          return of(error);
        })
      );
  }

  /**
   * Sort outcomes array by date and name;
   * @param events {array}
   * @returns {array} of sorted events
   * @private
   */
  sortOutcomesByDate(events: ISportEvent[]): ISportEvent[] {
    return this.filtersService.chainSort(events, [
      'startTime'
    ]);
  }

  /**
   * Set event to outcome and add additional properties to outcome based on event.
   * @param event {object}
   * @param events {array}
   * @private
   */
  setEventDate(events: ISportEvent[]): void {
    events.forEach((event: ISportEvent) => {
      event.time = this.timeService.getEventTime(`${new Date(event.startTime)}`);
      event.dateTime = new Date(event.startTime).toLocaleString();
    });
  }
}
