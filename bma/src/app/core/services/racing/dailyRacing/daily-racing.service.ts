import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent } from '@core/models/sport-event.model';
import { EventService } from '@sb/services/event/event.service';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { TemplateService } from '@shared/services/template/template.service';

interface IDailyRacingDataObject {
  modules: {
    dailyRacing: {
      classIds?: string | Array<string>;
      typeNames: Array<string>;
      collapsedSections: string | Array<string>;
      eventsBySections?: ITypeSegment;
    }
  };
  selectedTab: string;
  events?: ISportEvent[];
}

@Injectable()
export class DailyRacingService {

  private readonly dailyRacingConfig = {
    allowedTabs: ['today'],
    date: 'today',
    classIds: [],
    isRacing: true, // flag for request
    siteChannels: 'M', // means get events with reffering to siteChanels
    eventStatusCode: 'A', // exclude suspended outcomes - and as result - Non/Runners (N/R)
    isNotFinished: true, // exclude finished events
    isNotStarted: true, // exclude started events
    typeFlagCodes: 'SP',
    isNotResulted: true,
    limitOutcomesCount: 1,
    limitMarketCount: 1
  };

  constructor(
    private eventFactory: EventService,
    private templateService: TemplateService
  ) { }

  getDailyRacingEvents(classIds: string | Array<string>): Promise<ISportEvent[]> {
    this.dailyRacingConfig.classIds = Array.isArray(classIds) ? classIds : [classIds];
    return this.eventFactory.getDailyRacingEvents(this.dailyRacingConfig)
      .then(this.templateService.filterEventsWithoutMarketsAndOutcomes);
  }

  /**
   * Filters Sections, return whitelist (sectionsList)
   *
   * @param eventsBySections
   * @param sectionsList
   * @returns {object}
   */
  filterBySectionsList(eventsBySections: Object, sectionsList: Array<string>): ITypeSegment {
    return sectionsList ? _.pick(eventsBySections, Array.prototype.slice.call(sectionsList)) : eventsBySections;
  }

  /**
   * Modifying/Adds Data Structure for Daily Racing Module work
   *
   * @param publicArguments
   * @returns {promise}
   */
  addEvents(publicArguments: IDailyRacingDataObject): Promise<any> {
    if (_.contains(this.dailyRacingConfig.allowedTabs, publicArguments.selectedTab)) {
      return this.getDailyRacingEvents(publicArguments.modules.dailyRacing.classIds).then(data => {
        if (_.has(publicArguments, 'groupedRacing')) {
          publicArguments.modules.dailyRacing.eventsBySections = this.filterBySectionsList(
            this.templateService.groupEventsByTypeName(data),
            publicArguments.modules.dailyRacing.typeNames
          );

          _.each(publicArguments.modules.dailyRacing.eventsBySections, (section: any) => {
            _.each(section, (sport: any, id) => {
              if (sport.isStarted || sport.rawIsOffCode === 'Y') {
                section.splice(id, 1);
              }

              if (!section.length) {
                publicArguments.modules.dailyRacing.eventsBySections = null;
              }
            });
          });
        } else {
          _.each(data, eventEntity => {
            publicArguments.events && publicArguments.events.push(eventEntity);
          });
        }
      });
    }

    return Promise.resolve(publicArguments);
  }

}
