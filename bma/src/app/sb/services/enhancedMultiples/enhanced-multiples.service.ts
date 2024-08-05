
import { from as observableFrom, of, Observable } from 'rxjs';

import { map, concatMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TimeService } from '@core/services/time/time.service';

import { IEnhancedConfig } from '@sb/models/enhanced-multiples.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ICategory } from '@core/models/category.model';
import { TemplateService } from '@shared/services/template/template.service';
import { EventService } from '@sb/services/event/event.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportInstance } from '@core/services/cms/models';
import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class EnhancedMultiplesService {
  constructor(
    private siteServerService: SiteServerService,
    private timeService: TimeService,
    private eventService: EventService,
    private templateService: TemplateService,
    private sportsConfigService: SportsConfigService
  ) {
    this.enhancedMultiplesEvents = this.enhancedMultiplesEvents.bind(this);
    this.enhancedMultiplesHomeEvents = this.enhancedMultiplesHomeEvents.bind(this);
  }

  /**
   * Gets enhanced multiples of exact sport and adds icons and correct day
   */
  getEnhancedMultiplesEvents(sportName: string, display?: string): Observable<ISportEvent[]> {
    return this.formConfig(sportName, display)
      .pipe(
        concatMap((enhancedConfig: IEnhancedConfig) => {
          return observableFrom(
            this.eventService.cachedEvents(this.enhancedMultiplesEvents)(enhancedConfig)
          );
        }),
        concatMap((events: ISportEvent[]) => {
          _.each(events, (event: ISportEvent) => {
            event.eventCorectedDay = this.templateService.getEventCorectedDay(event.startTime);
          });
          return of(events);
        })
      );
  }

  /**
   * Gets enhanced multiples of exact sport and adds icons and correct day
   */
  getRacingEnhancedMultiplesEvents(sportName: string): Observable<ISportEvent[]> {
    const enhancedConfig = {
      siteChannels: 'M',
      isNotStarted: true,
      eventStatusCode: 'A',
      typeName: '|Enhanced Multiples|',
      suspendAtTime: this.timeService.getSuspendAtTime(),
      classIds: environment.CATEGORIES_DATA.racing[sportName].specialsClassIds
    };

    return observableFrom(
      this.eventService.cachedEvents((requestParams: ISSRequestParamsModel) =>
        this.enhancedRacingMultiplesEvents(requestParams).toPromise())(enhancedConfig)
    ).pipe(concatMap((events: ISportEvent[]) => {
      events.forEach((event: ISportEvent) => {
        event.eventCorectedDay = this.templateService.getEventCorectedDay(event.startTime);
      });
      return of(events);
    }));
  }

  /**
   * Gets all enhanced multiples and adds icons and correct day
   */
  getAllEnhancedMultiplesEvents(): Observable<ICategory[]> {
    return this.formConfig()
      .pipe(
        concatMap((enhancedConfig: IEnhancedConfig) => {
          return observableFrom(
            this.eventService.cachedEventsByFn(this.enhancedMultiplesHomeEvents, 'multiplesEvents')(enhancedConfig)
          );
        }),
        concatMap((categories: ICategory[]) => {
          const events = _.map(categories, (category: ICategory) => {
            _.each(category.events, (event: ISportEvent) => {
              event.eventCorectedDay = this.templateService.getEventCorectedDay(event.startTime);
            });
            return category.events;
          });

          const flattenEvents = _.flatten(events);

          return observableFrom(this.templateService.addIconsToEvents(flattenEvents)).pipe(
            map(() => {
              return categories;
            }));
        }));
  }

  /**
   * Gets multiples events according to requested params
   */
  private enhancedRacingMultiplesEvents(requestParams: ISSRequestParamsModel): Observable<ISportEvent[]> {
    return this.siteServerService.getEventsByClass(requestParams).pipe(
      concatMap((events: ISportEvent[]) => {
        return of(events.filter((event: ISportEvent) => this.templateService.isMultiplesEvent(event)));
    }));
  }

  /**
   * Gets multiples events of all sports and group them by category
   */
  private enhancedMultiplesHomeEvents(requestParams: ISSRequestParamsModel): Promise<ICategory[]> {
    return this.enhancedMultiplesEvents(requestParams).then((events: ISportEvent[]) => {
      const categoryIds = _.uniq(_.map(events, (event: ISportEvent) => event.categoryId));
      if (categoryIds.length) {
        return this.siteServerService.getCategories(categoryIds).then((categories: ICategory[]) => {
          _.each(categories, (category: ICategory) => {
            category.events = _.filter(events, (event: ISportEvent) => Number(event.categoryId) === Number(category.id));
          });
          return categories;
        });
      } else {
        return Promise.resolve([]);
      }
    });
  }

  /**
   * Gets multiples events according to requested params
   */
  private enhancedMultiplesEvents(requestParams: ISSRequestParamsModel): Promise<ISportEvent[]> {
    const timeRange = this.timeService.createTimeRange(requestParams.display);

    if (!_.isEmpty(timeRange)) {
      requestParams.startTime = timeRange.startDate;
      requestParams.endTime = timeRange.endDate;
    }
    requestParams.suspendAtTime = this.timeService.getSuspendAtTime();

    return this.siteServerService.getEnhancedMultiplesEvents(requestParams).then((events: ISportEvent[]) => {
      return _.filter(events, event => this.templateService.isMultiplesEvent(event));
    });
  }

  /**
   * Config object for retrieving Enhanced Multiples events
   */
  private formConfig(sportName?: string, display?: string): Observable<IEnhancedConfig> {
    const enhancedConfig = {
      siteChannels: 'M',
      isNotStarted: true,
      typeName: '|Enhanced Multiples|',
      categoryId: '',
      display,
      date: `${display}Multiples`
    };

    if (!sportName || sportName === 'horseracing') {
      enhancedConfig.categoryId = environment.CATEGORIES_DATA.racing[sportName] && environment.CATEGORIES_DATA.racing[sportName].id;
      return of(enhancedConfig);
    }

    return this.sportsConfigService.getSport(sportName)
      .pipe(
        map((sportInstance: ISportInstance) => {
          enhancedConfig.categoryId = sportInstance.sportConfig.config.request.categoryId;
          return enhancedConfig;
        }, )
      );
  }
}
