import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { IConstant } from '../models/constant.model';
import { IRoutingHelperEvent, IRoutingHelperCompetition } from './routing-helper.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Injectable()
export class RoutingHelperService {
  private racingCategories: IConstant;
  private racingIds: Array<number>;

  constructor(
    private sportsConfigHelperService: SportsConfigHelperService,
    private routingState: RoutingState
  ) {
    this.racingCategories = environment.CATEGORIES_DATA.racing;
    this.racingIds = _.map(this.racingCategories, category => Number(category.id));
  }

  /**
   * Encodes url part from unneeded symbols.
   * @param {string} part
   * @return {string}
   */
  encodeUrlPart(part: string|number): string {
    return `${part}`.replace(/([^a-zA-Z0-9])+/g, '-')
      .replace(/^-+|-+$/g, '') // remove one or more dashes at start of the sting or at end
      .toLowerCase();
  }

  /**
   * Forms URL for sport's event details page based on category, class, type and event names.
   * @param {string|number} options.categoryId
   * @param {string} options.categoryName
   * @param {string} options.className
   * @param {string} options.typeName
   * @param {string} options.name
   * @param {string} options.id
   * @param {string} extensionName
   * @return {string}
   */
  formEdpUrl(options: IRoutingHelperEvent | ISportEvent): string {
    const isRacing: boolean = _.contains(this.racingIds, Number(options.categoryId));
    const name = options.name || 'name';
    const eventName: string = isRacing ? (options.originalName || name) : name;
    const parts: Array<string|number> = [options.categoryName, options.className || 'class',
      options.typeName || 'type', eventName, options.id];
    const url: string = _.map(parts, part => `/${this.encodeUrlPart(part)}`).join('');
    const eventPrefix = isRacing ? '' : 'event';

    return `${eventPrefix}${url}`;
  }
/**
 * to form Five A Side URL
 * @param categoryName
 * @param className
 * @param typeName
 * @param name
 * @param id
 * @return {string}
 */
   formFiveASideUrl(categoryName: string, className: string, typeName: string, name: string, id: string): string {
    const parts: Array<string|number> = [categoryName, className, typeName,
     name, id];
     const url: string = parts.map((part: string | number) => `/${this.encodeUrlPart(part)}`).join('');
     return `${url}`;
  }

  /**
   * Forms URL for sport or racing page based on sport name and optional tab/sub-tab.
   * @param {string} sportName
   * @param {string=} location
   * @return {string}
   */
  formSportUrl(sportName: string, location?: string): Observable<string> {
    return this.sportsConfigHelperService.getSportPathByName(sportName)
      .pipe(
        map((sportPath: string) => {
          return `/${sportPath || sportName}${(location ? `/${location}` : '')}`;
        })
      );
  }

  /**
   * Forms event details page or sport results page based on event's "isResulted" property.
   * @param {Object} eventEntity
   * @param {string} origin
   * @param {boolean} isRacing
   * @return {string}
   */
  formResultedEdpUrl(eventEntity: IRoutingHelperEvent | ISportEvent, origin: string = ''): string {
    return `${this.formEdpUrl(eventEntity)}${origin}`;
  }

  /**
   * Forms URL for sport competition.
   * @param {string} options.sport
   * @param {string} options.className
   * @param {string} options.typeName
   * @return {string}
   */
  formCompetitionUrl(options: IRoutingHelperCompetition): string {
    return `/competitions${_.map([options.sport, options.className, options.typeName],
      part => `/${this.encodeUrlPart(part)}`).join('')}`;
  }

  formInplayUrl(sportName: string) {
    return `/in-play/${sportName}`;
  }

  formSportCompetitionsUrl(sportURI: string) {
    return `/${sportURI}/competitions`;
  }

  getLastUriSegment(uriPath: string): string {
    const validatedPath: string = /[^\/]$/.test(uriPath) ? uriPath : uriPath.replace(/[^\/]$/, '');
    const lastSegment: RegExpMatchArray = validatedPath.match('[^/]+(?=/$|$)');
    return lastSegment ? lastSegment[0] : uriPath;
  }

  getPreviousSegment(): string {
    return this.routingState.getPreviousSegment();
  }
}
