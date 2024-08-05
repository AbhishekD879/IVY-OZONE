import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { GamingService } from '@core/services/sport/gaming.service';
import { TemplateService } from '@shared/services/template/template.service';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { ITypeSegment, IGroupedByDateItem } from '@app/inPlay/models/type-segment.model';
import { ILevels } from './big-competitions.specials.model';
import { ISportViewTypes } from '@core/models/sports-view-types.model';
@Injectable()
export class BigCompetitionsSpecialsService {

  private BY_LEAGUE_ORDER: string[];
  private BY_LEAGUE_EVENTS_ORDER: string[];
  constructor(
    private gamingService: GamingService,
    private templateService: TemplateService,
    private srvUtil: SiteServerUtilityService,
    private filtersService: FiltersService
  ) {
    this.BY_LEAGUE_ORDER = ['classDisplayOrder', 'typeDisplayOrder'];
    this.BY_LEAGUE_EVENTS_ORDER = ['startTime', 'displayOrder', 'name'];
  }

  getEventsBySections(eventsArray: ISportEvent[]): ITypeSegment[] {
    if (eventsArray && eventsArray.length) {
      const events = this.srvUtil.filterEventsWithPrices(eventsArray);
      const eventsBySections = this.gamingService.arrangeEventsBySection(events, true);
      const orderedEventsBySections = this.filtersService.orderBy(eventsBySections, this.BY_LEAGUE_ORDER);
      const sportsViewTypes = this.templateService.getSportViewTypes(events[0].categoryName.toLowerCase().replace(' ', ''));

      _.each(orderedEventsBySections, section => {
        section.events = this.filtersService.orderBy(section.events, this.BY_LEAGUE_EVENTS_ORDER);
        section.showAll = false;
        section.sectionTitle = this.sectionTitle(sportsViewTypes, section);
      });

      return orderedEventsBySections;
    }

    return [];
  }

  /**
   * Check whether show all button should be shown for grouped by date selections section (Enhanced Multiples)
   * @param groupedByDate
   * @param showLimit
   * @returns {*|boolean}
   */
  isShowButtonForGroupedByDateEnabled(groupedByDate: IGroupedByDateItem[], showLimit: number): boolean {
    const datesLength: number = Object.keys(groupedByDate).length;

    return showLimit && this.eGbDSelectionsCount(groupedByDate, datesLength) > showLimit;
  }

  /**
   * Remove event and section (if needed) *** NOTICE: Functions run order should be kept! ***
   * @param eventsBySections
   * @param eventId
   * @returns {Array}
   */
  removeEvent(eventsBySections: ITypeSegment[], eventId): ITypeSegment[] {
    const deletedEventIndexes: ILevels = this.getRemovedEventLevels(eventsBySections, eventId.toString());

    if (deletedEventIndexes.section !== null) {
      this.removeEventFromLevel(eventsBySections, deletedEventIndexes);
      this.removeEventFromGropedByDate(eventsBySections, deletedEventIndexes);
      this.removeEmptyGropedByDateSection(eventsBySections, deletedEventIndexes);
      this.removeEmptySection(eventsBySections, deletedEventIndexes);
    }
    return eventsBySections;
  }

  /**
   * Forms sections title for section
   * @param sportsViewTypes
   * @param section
   * @returns {string}
   * @private
   */
  private sectionTitle(sportsViewTypes: ISportViewTypes, section: ITypeSegment): string {
    return sportsViewTypes.className
      ? `${this.filtersService.clearSportClassName(section.className, section.categoryName)} - ${section.typeName}`
      : `${section.categoryName} - ${section.typeName}`;
  }

  /**
   * Events GroupedByDate Selections Counter - needed for show more button inside GroupedByDate events
   * @param groupedByDate
   * @param headerIndex
   * @private
   */
  private eGbDSelectionsCount(groupedByDate: IGroupedByDateItem[], headerIndex: number): number {
    const keysArray: string[] = Object.keys(groupedByDate).slice(0, headerIndex + 1);

    return this.selectionsCount(keysArray, groupedByDate);
  }

  /**
   * returns selections count in GroupedByDate structure by keys(dates) list
   * @param keysArray
   * @param groupedByDate
   * @returns {*}
   * @private
   */
  private selectionsCount(keysArray: string[], groupedByDate: IGroupedByDateItem[]): number {
    return keysArray.reduce((sumK: number, currK: string) => sumK + groupedByDate[currK].events
      .reduce((sumE: number, currE) => sumE + currE.markets[0].outcomes.length, 0), 0);
  }

  /**
   * Removes event from array by provided level(index)
   * @param eventsBySections
   * @param deletedEventIndexes
   * @private
   */
  private removeEventFromLevel(eventsBySections: ITypeSegment[], deletedEventIndexes: ILevels): void {
    eventsBySections[deletedEventIndexes.section].events.splice(deletedEventIndexes.event, 1);
  }

  private removeEventFromGropedByDate(eventsBySections: ITypeSegment[], indexes: ILevels): void {
    eventsBySections[indexes.section].groupedByDate[indexes.groupedByDateKey].events.splice(indexes.groupedByDateEvent, 1);
  }

  /**
   * Remove empty section from array by provided level(index)
   * @param eventsBySections
   * @param deletedEventIndexes
   * @private
   */
  private removeEmptySection(eventsBySections: ITypeSegment[], deletedEventIndexes: ILevels): void {
    if (!eventsBySections[deletedEventIndexes.section].events.length) {
      eventsBySections.splice(deletedEventIndexes.section, 1);
    }
  }

  private removeEmptyGropedByDateSection(eventsBySections: ITypeSegment[], deletedEventIndexes: ILevels): void {
    if (!eventsBySections[deletedEventIndexes.section].groupedByDate[deletedEventIndexes.groupedByDateKey].events.length) {
      eventsBySections[deletedEventIndexes.section].groupedByDate.splice(deletedEventIndexes.groupedByDateKey, 1);
    }
  }

  /**
   * Searches event in 2 levels arrays by event id and return object with found levels indexes
   * @param eventsBySections
   * @param eventId
   * @returns {{section: null, event: null}}
   * @private
   */
  private getRemovedEventLevels(eventsBySections: ITypeSegment[], eventId: number): ILevels {
    const levels: ILevels = { section: null, event: null, groupedByDateKey: null, groupedByDateEvent: null };

    eventsBySections.forEach((section: ITypeSegment, sectionIndex: number) => {
      const deletedEventIndex = _.findIndex(section.events, (event: ISportEvent) => event.id === eventId);
      if (deletedEventIndex !== -1) {
        levels.section = sectionIndex;
        levels.event = deletedEventIndex;
        _.each(section.groupedByDate, (group: IGroupedByDateItem, key: number) => {
          const deletedEventIndexInGroupedByDate = _.findIndex(group.events, (event: ISportEvent) => event.id === eventId);
          if (deletedEventIndexInGroupedByDate !== -1) {
            levels.groupedByDateKey = key;
            levels.groupedByDateEvent = deletedEventIndexInGroupedByDate;
          }
        });
      }
    });

    return levels;
  }
}
