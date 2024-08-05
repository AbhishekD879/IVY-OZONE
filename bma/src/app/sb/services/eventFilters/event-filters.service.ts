import { Injectable } from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';

@Injectable()
export class EventFiltersService {

  private allFilters = {
    started: EventFiltersService.started,
    hasOutcomes: EventFiltersService.hasOutcomes,
    hasPrices: EventFiltersService.hasPrices
  };

  /**
   * started()
   * @param {ISportEvent} event
   * @returns {boolean}
   */
  private static started(event: ISportEvent): boolean {
    return event.eventIsLive;
  }

  /**
   * hasOutcomes()
   * @param {ISportEvent} event
   * @returns {number}
   */
  private static hasOutcomes(event: ISportEvent): number {
    return event.markets &&
      event.markets.length &&
      event.markets[0].outcomes.length;
  }

  /**
   * hasPrices()
   * @param {ISportEvent} event
   * @returns {number}
   */
  private static hasPrices(event: ISportEvent): number {
    return EventFiltersService.hasOutcomes(event) &&
      event.markets[0].outcomes[0].prices.length;
  }

  /**
   * applyFilters()
   * @param {string[]} filterNames
   * @returns {Function[]}
   */
  applyFilters(filterNames: string[]): Function {
    const filters = this.getFilters(filterNames);
    return this.filterEvents.bind(null, filters);
  }

  /**
   * filterEvents()
   * @param {Function[]} filters
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  filterEvents(filters: Function[], events: ISportEvent[]): ISportEvent[] {
    return events.filter(event => {
      return filters.every(filterFn => filterFn(event));
    });
  }

  /**
   * getFilters()
   * @param {string[]} keys
   * @returns {Function[]}
   */
  getFilters(keys: string[]): Function[] {
    return keys.map(key => this.allFilters[key]);
  }
}
