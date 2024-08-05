import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';

interface IGroupEvents extends ISportEvent {
  isExpandedEvent?: boolean;
}

@Component({
  selector: 'racing-specials-tab',
  templateUrl: 'racing-specials-tab.component.html'
})
export class RacingSpecialsTabComponent implements OnInit {
  @Input() racing: {events: ISportEvent[]; classesTypeNames: any};
  @Input() eventsOrder: string[];
  @Input() responseError: string;

  isExpandedType: boolean =  true;
  showSpecialEvents: boolean;
  eventsByType: Array<{typeName: string; events: IGroupEvents[]}> = [];
  limit: number = 4;

  constructor(
    private filterService: FiltersService,
    private sbFilters: SbFiltersService,
    private smartBoostsService: SmartBoostsService
  ) { }

  ngOnInit(): void {
    this.showSpecialEvents = !this.responseError && this.racing.events.length > 0;

    _.each(this.racing.events, (eventEntity: ISportEvent) => {
      const market = eventEntity.markets[0];
      eventEntity.startTimeFiltered = this.filterService.date(eventEntity.startTime, 'dd MMM');
      eventEntity.markets[0].filteredOutcomes = this.sbFilters.orderOutcomeEntities(market.outcomes,
        market.isLpAvailable, true);
      this.transformSmartBoostsMarket(eventEntity.markets[0]);
    });

    // by def: all Type tabs are expanded, only first Event in first Type tab is expanded
    const orderedEvents = this.filterService.orderBy(this.racing.events, this.eventsOrder);
    _.each(this.racing.classesTypeNames.default, (classesTypeName: any, groupIndex: number) => {
      const groupEvents = _.filter(orderedEvents, ev => ev.typeName === classesTypeName.name) as IGroupEvents[];

      if (groupEvents.length) {
        if (!groupIndex) { groupEvents[0].isExpandedEvent = true; }
        this.eventsByType.push({
          typeName: classesTypeName.name,
          events: groupEvents
        });
      }
    });
  }


  /**
   * @param {object} index
   * @param {object} val
   * @return {string}
   */
  trackById(index: number, val: ISportEvent): number {
    return val.id;
  }

  /**
   * @param {object} index
   * @param {object} val
   * @return {string}
   */
  trackByOrder(index: number, val: {typeDisplayOrder: string}): string {
    return val.typeDisplayOrder;
  }

  /**
   * @param {number} index1
   * @param {number} index2
   * @return {boolean}
   */
  isExpandedEvent(index1: number, index2: number): boolean {
    return index1 === 0 && index2 === 0;
  }

  formatSpecialTerms(str: string): string {
    const newStr = str
      .replace(/(odds)/ig, 'Odds')
      .replace(/(places)/ig, 'Places')
      .replace(/\d+\/\d+( odds)/ig, match => {
        return `<strong>${match}</strong>`;
      });

    return newStr.replace(/[0-9]+(?!.*[0-9])/, match => `<strong>${match}</strong>`);
  }

  /**
   * format smartBoosts markets
   * @param {IMarket[]} markets
   */
  private transformSmartBoostsMarket(market: IMarket): void {
    market.isSmartBoosts = this.smartBoostsService.isSmartBoosts(market);

    if (!market.isSmartBoosts) { return; }

    _.each(market.outcomes, (outcome: IOutcome) => {
      const parsedName = this.smartBoostsService.parseName(outcome.name);
      if (!parsedName.wasPrice) { return; }

      outcome.name = parsedName.name;
      outcome.wasPrice = parsedName.wasPrice;
    });
  }
}
