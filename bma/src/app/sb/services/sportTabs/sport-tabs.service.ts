import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { TemplateService } from '@shared/services/template/template.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { GamingService } from '@core/services/sport/gaming.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { ISportViewTypes } from '@core/models/sports-view-types.model';
import { IGroupedByDateItem, ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { OUTRIGHTS_CONFIG } from '@app/core/constants/outrights-config.constant';

@Injectable()
export class SportTabsService {
  constructor(
    private templateService: TemplateService,
    private filtersService: FiltersService
  ) {}

  /**
   * Delete resulted or undisplayed event, additional delete section if there is no events left
   *
   * @param {ITypeSegment[]} sections
   * @param {string} eventId
   */
  deleteEvent(eventId: string, sections: ITypeSegment[]): void {
    sections.forEach((sportSection: ITypeSegment, index: number) => {
      if (sportSection) {
        const eventIndex = sportSection.events.findIndex((event: ISportEvent) => event.id === parseInt(eventId, 10));

        if (eventIndex !== -1) {
          sportSection.events.splice(eventIndex, 1);
          if (!sportSection.events.length) {
            sections.splice(index, 1);
          }
        }

        // check that we have grouped data and it is an array
        const isGroupedDataArray = sportSection.groupedByDate && Array.isArray(sportSection.groupedByDate);

        if (isGroupedDataArray) {
          // remove event also from grouped by date data.
          sportSection.groupedByDate.forEach((group: IGroupedByDateItem, groupIndex: number) => {
            const groupEventIndex = group.events.findIndex((event: ISportEvent) => event.id === parseInt(eventId, 10));

            if (groupEventIndex !== -1) {
              group.events.splice(groupEventIndex, 1);
              if (!group.events.length) {
                sportSection.groupedByDate.splice(groupIndex, 1);
              }
            }
          });
        }
      }
    });
  }

  /**
   * Create and sort Events By Sections
   * @param {ISportEvent[]} events
   * @return {ITypeSegment[]}
   */
  eventsBySections(events: ISportEvent[], sportInstance: GamingService): ITypeSegment[] {
    const eventsBySections: ITypeSegment[] = sportInstance.arrangeEventsBySection(events, true);
    const sportsViewTypes = this.templateService.getSportViewTypes(events[0].categoryName.toLowerCase().replace(' ', ''));

    eventsBySections.forEach((section: ITypeSegment) => {
      section.events = this.sortSportEventsData(section.events);
      section.sectionTitle = this.sectionTitle(sportsViewTypes, section);
    });

    return this.filtersService.orderBy(eventsBySections, ['typeDisplayOrder', 'classDisplayOrder', 'sectionTitle']);
  }

  /**
   * Forms sections title for section
   * @param {ISportViewTypes} sportsViewTypes
   * @param {ITypeSegment} section
   * @returns {string}
   * @private
   */
  private sectionTitle(sportsViewTypes: ISportViewTypes, section: ITypeSegment): string {
    return sportsViewTypes.className
      ? `${this.filtersService.clearSportClassName(section.className, section.categoryName)} - ${section.typeName}`
      : `${section.categoryName} - ${section.typeName}`;
  }

  /**
   * Sort Sport Events data
   * @param {ISportEvent[]} data
   * @returns {ISportEvent[]}
   */
  private sortSportEventsData(data: ISportEvent[]): ISportEvent[] {
    const onlyMatches = data.filter(event => !OUTRIGHTS_CONFIG.sportSortCode.includes(event.eventSortCode));
    const onlyOutrights = data.filter(event => OUTRIGHTS_CONFIG.sportSortCode.includes(event.eventSortCode));

    if(data[0].categoryId === '18') { // for 'golf'
      return [...this.sortEvents(onlyOutrights), ...this.sortEvents(onlyMatches)];
    }
    return [...this.sortEvents(onlyMatches), ...this.sortEvents(onlyOutrights)];
  }

  private sortEvents(events: ISportEvent[]): ISportEvent[] {
    return _(events).chain().sortBy((event: ISportEvent) => {
      return event.name.toLowerCase();
    }).sortBy((event: ISportEvent) => {
      return event.startTime;
    }).sortBy((event: ISportEvent) => {
      return event.displayOrder;
    }).value();
  }
}
