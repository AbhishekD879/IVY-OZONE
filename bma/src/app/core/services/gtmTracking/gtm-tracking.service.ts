import { Injectable } from '@angular/core';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { StorageService } from '@core/services/storage/storage.service';
import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IVirtualSportEventEntity } from '@app/vsbr/models/virtual-sports-event-entity.model';
import { IGtmOrigin } from '@core/services/gtmTracking/models/gtm-origin.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { IBet } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { GamingService } from '@app/core/services/sport/gaming.service';

@Injectable()
export class GtmTrackingService {

  private locationPrefix: string;
  private location: string;
  private subLocation: string;
  private module: string;
  private gtmObject: IGtmOrigin;
  private placedBetsOrigins;

  constructor(private locationService: Location,
    private sportTabsService: SportTabsService,
    private storageService: StorageService,
    private gamingService: GamingService) {
  }

  /**
   * Get location and module for GTM
   *
   * @returns {object | null}
   */
  getTracking(): IGtmOrigin | null {
    if(this.gtmObject && this.gtmObject.location){
      this.gtmObject.location = this.gtmObject.location === 'NOW & NEXT' ? 'Fanzone' : this.gtmObject.location
    }
    return this.gtmObject;
  }

  /**
   * Restores trace object of bet (eg after page refresh)
   *
   * @param {IGtmOrigin} betTrace
   */
  restoreTracking(betTrace: IGtmOrigin): void {
    if (betTrace) {
      this.gtmObject = betTrace;
    }
  }

  /**
   * Detects liocation and module for GTM
   * @param {string} moduleTitle - current GTM module
   * @param {string} segment - current route segment
   * @param {ISportEvent} event -  event of bet wich was added
   * @param {IMarket} market -  market of bet wich was added
   * @returns {object}
   */
  detectTracking(moduleTitle: string, segment: string, event: ISportEvent, market: IMarket, placedLocation?: string): IGtmOrigin {
    this.module = moduleTitle || '';
    this.locationPrefix = '';

    if (!this.module) {
      const segmentParts = segment.split('.');
      // event page
      if (segmentParts.some((el) => el === 'eventMain')) {
        this.module = 'edp';
      }

      // Sport matches tab
      if (segment === 'sport.matches.tab') {
        const section = this.sportTabsService.eventsBySections([event], this.gamingService);
        this.module = section.length ? section[0].sectionTitle : '';
      }
    }

    const currentPath = this.locationService.path().toLowerCase();
    // Home page prefix
    if (currentPath === '' || currentPath.indexOf('/home') === 0) {
      this.locationPrefix = 'HOME';
    }

    // If location was not detected - no switchers on page which set location/sublocation
    if (!this.location) {
      switch (true) {
        case (['horseracing.eventMain', 'greyhound.eventMain'].includes(segment)):
          this.location = event.localTime;
          break;
        case (segment === 'eventMain'):
          this.location = event.categoryName;
          break;
        case (segment === 'favourites'):
          this.location = 'FAVOURITES';
          break;
      }
    }

    let location = [this.locationPrefix, this.location, this.subLocation];
    location = _.filter(location, (el) => Boolean(el));
    if (placedLocation) {
      location = [placedLocation];
    }
    this.gtmObject = {
      location: location.join('. '),
      module: this.module
    };
    return this.getTracking();
  }

  detectVirtualSportTracking(module: string, virtualSportEvent: IVirtualSportEventEntity): IGtmOrigin {
    this.gtmObject = {
      location: virtualSportEvent.title,
      module: module
    };
    return this.getTracking();
  }

  /**
   * Set location and sublocation values according current switcher value and current route
   * @param {string} name - new location/sublocation value
   * @param {string} type - 'location' or 'sublocation'
   */
  setLocation(name: string, type: string): void {
    if (type === 'location') {
      this.location = name.toUpperCase();
    }
    if (type === 'sublocation') {
      this.subLocation = name.toUpperCase();
    }
  }

  /**
   * Clear current locatio & sublocation when switcher is destroyed
   * @param {string} type - 'location' or 'sublocation'
   * @return void
   */
  clearLocation(type: string): void {
    if (type === 'location') {
      this.location = '';
    }
    if (type === 'sublocation') {
      this.subLocation = '';
    }
  }

  /**
   * Collect placed bet origins
   * @param {IBet[]} bets
   * @return void
   */
  collectPlacedBets(bets: IBet[]): void {
    this.placedBetsOrigins = {};
    const selections = <IBetSelection[]>this.storageService.get('betSelections');
    selections.forEach((betSelection: IBetSelection) => {
      if(betSelection.outcomesIds?.length && betSelection.GTMObject) {
        this.placedBetsOrigins[betSelection.outcomesIds[0]] = betSelection.GTMObject.tracking;
      }
    });
  }

  /**
   * Get collected bets origins by outcomeId
   * @param {string} outcomeId
   * @return IGtmOrigin
   */
  getBetOrigin(outcomeId): IGtmOrigin {
    const origin: IGtmOrigin = {
      location: '',
      module: '',
      betType: ''
    };
    const reuseBetOrigin = <IGtmOrigin[]>this.storageService.get('reuseBetSelections');
    if (reuseBetOrigin && reuseBetOrigin[outcomeId]) { 
      origin.location = reuseBetOrigin[outcomeId].location
      origin.module = reuseBetOrigin[outcomeId].module;
      origin.betType = reuseBetOrigin[outcomeId].betType;
    }
    else if (this.placedBetsOrigins && this.placedBetsOrigins[outcomeId]) {
      origin.location = this.placedBetsOrigins[outcomeId].location === 'NOW & NEXT' ? 'Fanzone' : this.placedBetsOrigins[outcomeId].location;
      origin.module = this.placedBetsOrigins[outcomeId].module;
      origin.betType = this.placedBetsOrigins[outcomeId].betType;
    }
    return origin;
  }

  /**
   * Restore bet GTM origin after reuse selection
   * @param {string[]} outcomesIds - outcomes which were reused
   * @return void
   */
  restoreGtmTracking(outcomesIds: string[]): void {
    const selections = <IBetSelection[]>this.storageService.get('betSelections');
    _.each(selections, (betSelection: IBetSelection) => {
      if (betSelection.outcomesIds.length === 1) {
        const outcomeId = betSelection.outcomesIds[0];
        if (this.placedBetsOrigins &&
          this.placedBetsOrigins[outcomeId] &&
          outcomesIds.includes(outcomeId)) {
          betSelection.GTMObject.tracking = this.placedBetsOrigins[outcomeId];
        }
      }
    });
    this.storageService.set('betSelections', selections);
  }

}
