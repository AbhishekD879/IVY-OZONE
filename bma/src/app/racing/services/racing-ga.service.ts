import { Injectable } from '@angular/core';

import { IRacingGaEvent } from '@racing/models/racing-ga.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { NEXT_RACES_HOME_CONSTANTS } from '@lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';

@Injectable({ providedIn: 'root' })
export class RacingGaService {

  readonly flag: Map<string, boolean>;

  readonly CONST = {
    FULL_RACE: 'full race card',
    COLLAPSE: 'collapse',
    NEXT_RACES: 'next 4 races',
    WIDGET: 'widget',
    HORSERACING: 'horseracing',
    HORSERACING_CATEGORY: 'horse racing',
    YOURCALL: 'your call',
    TWITTER: 'tweet now',
    YOURCALL_SPECIALS: 'more your call specials'
  };

  constructor(
    private gtm: GtmService,
    private locale: LocaleService,
    private pubsub: PubSubService
  ) {
    this.flag = new Map();
  }

  /**
   * track custom event
   * @param eventObj
   */
  trackEvent(eventObj: IRacingGaEvent): void {
    if (eventObj.eventCategory === this.CONST.HORSERACING) {
      this.normalizeCategory(eventObj);
      this.gtm.push('trackEvent', eventObj);
    }
  }

  /**
   * send GTM tracking, via pubsub
   * @param {String} eventLabel - event name
   * @param {String} eventCategory - sport name
   */
  sendGTM(eventLabel: string, eventCategory: string, isVirtual ?: boolean): void {
    this.pubsub.publish(this.pubsub.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory,
      eventAction: 'next races',
      eventLabel,
      ...(isVirtual && {positionEvent: 'virtual'})
    }]);
  }

  /**
   * Normalize GA tracking category for specific sport
   * @param obj
   * @private
   */
  normalizeCategory(obj: IRacingGaEvent): void {
    if (obj.eventCategory === this.CONST.HORSERACING) {
      obj.eventCategory = this.CONST.HORSERACING_CATEGORY;
    }
  }

  /**
   * Track once module collapse event
   * @param module
   */
  trackModule(module: string, sport: string): void {
    if (!this.flag.get(module)) {
      this.trackEvent({
        eventCategory: sport,
        eventAction: this.locale.getString(module),
        eventLabel: this.CONST.COLLAPSE
      });
      this.flag.set(module, true);
    }
  }

  /**
   * Track Next Races full race card click
   * @param sport
   */
  trackNextRace(sport: string): void {
    this.trackEvent({
      eventCategory: sport.toLowerCase().replace(/\s+/g, ''),
      eventAction: this.CONST.NEXT_RACES,
      eventLabel: this.CONST.FULL_RACE
    });
  }

  /**
   * Track Next Races widget collapse
   * @param sport
   */
  trackNextRacesCollapse(sport: string): void {
    if (!this.flag.get(this.CONST.NEXT_RACES)) {
      this.trackEvent({
        eventCategory: sport,
        eventAction: this.CONST.NEXT_RACES,
        eventLabel: this.CONST.COLLAPSE
      });
      this.flag.set(this.CONST.NEXT_RACES, true);
    }
  }

  /**
   * Track Yourcall Tweet button
   */
  trackYourcallTwitter(): void {
    const eventObj: IRacingGaEvent = {
      eventCategory: this.CONST.YOURCALL,
      eventAction: this.CONST.TWITTER,
      eventLabel: this.CONST.HORSERACING_CATEGORY
    };
    this.gtm.push('trackEvent', eventObj);
  }

  /**
   * Track more Yourcall specials
   */
  trackYourcallSpecials(): void {
    const eventObj: IRacingGaEvent = {
      eventCategory: this.CONST.HORSERACING_CATEGORY,
      eventAction: this.CONST.YOURCALL,
      eventLabel: this.CONST.YOURCALL_SPECIALS
    };
    this.gtm.push('trackEvent', eventObj);
  }

  /**
   * reset state
   */
  reset(): void {
    this.flag.clear();
  }

  /**
  * Updates GTMservice with greyhound data
  * @param raceData : ISportEvent
  * @param option: selected sortby option
  * @param isGreyhoundEdp: is greyhound edp
  */
  public updateGATracking(raceData: ISportEvent, option: string, isGreyhoundEdp: boolean): void {
    const gtmData = {
      event: NEXT_RACES_HOME_CONSTANTS.TRACKEVENT,
      eventAction: NEXT_RACES_HOME_CONSTANTS.RACE_CARD,
      eventCategory: isGreyhoundEdp ? NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE,
      eventLabel: option === NEXT_RACES_HOME_CONSTANTS.PRICE_CAMEL_CASE ? NEXT_RACES_HOME_CONSTANTS.SORT_BY_PRICE : NEXT_RACES_HOME_CONSTANTS.SORT_BY_RACECARD,
      categoryID: raceData.categoryId,
      typeID: raceData.typeId,
      eventID: raceData.id
    }
    this.gtm.push(gtmData.event, gtmData);
  }

  /**
  * Updates GTMservice with greyhound data
  * @param eventEntity : ISportEvent
  * @param showOption: selected sortby option
  * @param isGreyhoundEdp: is greyhound edp
  */
  public toggleShowOptionsGATracking(eventEntity: ISportEvent, showOption: boolean, isGreyhoundEdp: boolean): void {
    const gtmData = {
      event: NEXT_RACES_HOME_CONSTANTS.TRACKEVENT,
      eventAction: NEXT_RACES_HOME_CONSTANTS.RACE_CARD,
      eventCategory: isGreyhoundEdp ? NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE,
      eventLabel: showOption ? NEXT_RACES_HOME_CONSTANTS.SHOW_INFO : NEXT_RACES_HOME_CONSTANTS.HIDE_INFO,
      categoryID: eventEntity.categoryId,
      typeID: eventEntity.typeId,
      eventID: eventEntity.id
    }
    this.gtm.push(gtmData.event, gtmData);
  }
}
