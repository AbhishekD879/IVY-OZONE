import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { IFilterParam } from '@core/models/filter-param.model';
import { ICombinedRacingConfig, INextRaces, IGreyhoundNextRaces } from '@core/services/cms/models/system-config';
import { ICategoriesData } from '@shared/models/categories-data.model';
import { IConstant } from '@core/services/models/constant.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { TemplateService } from '@shared/services/template/template.service';
import { IFeaturedModel } from '@featured/models/featured.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

export abstract class NextRacesAbstractService {

  racingData: ICategoriesData = environment.CATEGORIES_DATA.racing;

  abstract isNextRaces: boolean;
  abstract cacheKey: string;

  constructor(
    protected cacheEventsService: CacheEventsService,
    protected templateService: TemplateService,
    protected channelService: ChannelService,
    protected pubSubService: PubSubService
  ) {}

  /** Returns app next races module configs
   * @return {object}
   */
  getNextRacesModuleConfig(moduleName: string, cmsConfig: ICombinedRacingConfig): IFilterParam {
    return _.extend(this.getNextRacesModuleConfigStrict(moduleName),
      moduleName === 'horseracing' ? this.getHRNextRacesModuleConfigCMS(cmsConfig)
        : this.getGHNextRacesModuleConfigCMS(cmsConfig));
  }

  /**
   * Sets all necessary attributes for displaying events
   * and subscribes on live price updates
   * @params {object}
   * @params {object}
   * @returns {object}
   */
  getUpdatedEvents(data, moduleName: string): ISportEvent[] {
    return this.templateService.setCorrectPriceType(this.getEventsFromCache(moduleName) || data, false, this.isNextRaces);
  }

  /**
   * Get default next Races configs
   * @params{string} module name e.g. horseracing, greyhounds
   * @returns{object} config object
   */
  protected getNextRacesModuleConfigStrict(moduleName: string): IFilterParam {
    return {
      categoryId: this.racingData[moduleName].id, // specified category ID for HorseRasing
      siteChannels: 'M', // means get events with reffering to siteChanels
      // only for horseracing next races - means exclude outcomes with names - Unnamed Favorite & Unnamed 2nd Favorite;
      excludeUnnamedFavourites: true,
      isActive: true, // active event
      eventStatusCode: 'A', // exclude suspended events
      outcomeStatusCode: 'A', // exclude suspended outcomes - and as result - Non/Runners (N/R)
      marketStatusCodeExists: 'A', // exclude suspended markets - and as result - Non/Runners (N/R)
      marketStatusCode: 'A', // exclude suspended markets - and as result - Non/Runners (N/R)
      date: 'nextFour',
      priceHistory: true,
      isRawIsOffCodeNotY: true,
      hasOpenEvent: 'true'
    };
  }

  /**
   * Get type flag codes by CMS config
   * @params{object} CMS config
   * @params{boolean} choose value with what to compare,
   * if true - we will search for type flag code where cms config says -'Yes',
   * if false - we will search for type flag code where cms config says -'No',
   * @returns{string} string containing typeFlag codes
   */
  protected getTypeFlagInfo(cmsConfig: INextRaces, excludeCodes: boolean): string {
    const comparator = excludeCodes ? 'Yes' : 'No';
    if (!cmsConfig.typeID) {
      const info = [];
      if (cmsConfig.isInUK === comparator) {
        info.push('UK');
      }
      if (cmsConfig.isIrish === comparator) {
        info.push('IE');
      }
      if (cmsConfig.isInternational === comparator) {
        info.push('INT');
      }
      if (cmsConfig.isVirtualRacesEnabled === comparator) {
        info.push('VR');
      }
      return info.join();
    }

    return cmsConfig.typeID;
  }

  /**
   * Get amount of event that we need from SS to display
   * the amount specified in CMS.
   * @params{object} cms config
   * @returns{number} number of events needed
   */
  protected getEventsCount(cmsConfig: INextRaces | IGreyhoundNextRaces): number {
    if (parseInt(cmsConfig.numberOfEvents, 10) <= 3) {
      return 3;
    } else if (parseInt(cmsConfig.numberOfEvents, 10) <= 5) {
      return 5;
    } else if (parseInt(cmsConfig.numberOfEvents, 10) <= 7) {
      return 7;
    }
    return 12;
  }

  // Temporary solution, in future Greyhounds should get configs from CMS as
  // for now all values remain hard coded
  /**
   * Get Greyhounds Next races config
   * @params{object} cms config
   * @returns{object} ready configs
   */
  protected getGHNextRacesModuleConfigCMS(config: ICombinedRacingConfig): IFilterParam {
    const racingDataHubEnabled = config && config.RacingDataHub && config.RacingDataHub.isEnabledForGreyhound;
    const nextRacesConfig = config && config.GreyhoundNextRaces;
    const isVirtualRacesEnabled = this.isVirtualRacesEnabled(nextRacesConfig);
    const filterObject: IFilterParam = {
      racingFormOutcome: !racingDataHubEnabled || isVirtualRacesEnabled,
      siteServerEventsCount: nextRacesConfig && this.getEventsCount(nextRacesConfig) || 5,
      [isVirtualRacesEnabled ? 'marketTemplateMarketNameIntersects': 'templateMarketNameOnlyEquals']: this.getMarketsTemplates(isVirtualRacesEnabled),
      priceTypeCodes: 'SP,LP', // markets with SP (Starting Price) and LP (Live Price) bet types
      typeFlagCodes: isVirtualRacesEnabled ? 'NE,VR':'NE', // events with specific Flag Codes Types
      // events will be shown
      eventsCount: nextRacesConfig && parseInt(nextRacesConfig.numberOfEvents, 10) || 4,
      // outcomes (selections) will be shown
      limitOutcomesCount: nextRacesConfig && parseInt(nextRacesConfig.numberOfSelections, 10) || 4
    };
    if(isVirtualRacesEnabled){
      filterObject.isVirtualRacesEnabled = isVirtualRacesEnabled;
      filterObject.virtualRacesIncluded = nextRacesConfig && nextRacesConfig.virtualRacesIncluded;
    }
    return filterObject;
  }

  virtualTimesConfig(nextRacesConfig, trigger) {
    const timeconfig = [];
    for (const property in nextRacesConfig) {
      if(property.includes('VirtualsExcludeTimeRange')) {
        timeconfig.push(nextRacesConfig[property][trigger])
      }
    }
    return timeconfig;
  }

  protected isCurrentTimeAdded(startTimeRange, endTimeRange): boolean {
    const startTimeRanges = startTimeRange;
    const endTimeRanges =  endTimeRange;

    if(startTimeRanges && endTimeRanges) {
      return startTimeRanges.every((startTime, index) => 
      {
        const currDate = new Date();
        const startDate = startTime && new Date(currDate.getFullYear(), currDate.getMonth(), currDate.getDate(), parseInt(startTime.hh), parseInt(startTime.mm), parseInt(startTime.ss));
  
        const endTime = endTimeRanges[index];
        const endDate = endTime && new Date(currDate.getFullYear(), currDate.getMonth(), currDate.getDate(), parseInt(endTime.hh), parseInt(endTime.mm), parseInt(endTime.ss));
  
        if(endDate < startDate) {
          endDate.setDate(endDate.getDate() + 1)
        }
        return !(currDate >= startDate && currDate <= endDate)
      });
    }
    return true;
  }

  /**
   * to get market templates names based on virtual races enabled for both HR and GH
   * @params {boolean}
   * @return {string}
   */
  protected getMarketsTemplates(isVirtualRacesEnabled: boolean): string {
    if (isVirtualRacesEnabled) {
      return '|Win or Each Way|,|Win or each way|,|To-Win|,|Win|,|Win or EW|' //to get events for multiple market as known to virtuals
    } else return '|Win or Each Way|' // means get only events with market name AND ONLY 1 market with name
  }
  /**
  * to check whther next races are enabled or not
  * @returns{boolean} true if all values are there else false.
  */
  protected isVirtualRacesEnabled(nextRacesConfig: INextRaces | IGreyhoundNextRaces): boolean {
    if(nextRacesConfig && nextRacesConfig.isVirtualRacesEnabled){
      return nextRacesConfig.isVirtualRacesEnabled === "Yes"
      && this.isCurrentTimeAdded(this.virtualTimesConfig(nextRacesConfig, 'from'), this.virtualTimesConfig(nextRacesConfig, 'to'));
    } else {
      return false
    }
  }

  /**
   * Get Horse Racing Next races config from CMS
   * @params{object} cms config
   * @returns{object} ready configs
   */
  protected getHRNextRacesModuleConfigCMS(config: ICombinedRacingConfig): IFilterParam {
    const racingDataHubEnabled = config && config.RacingDataHub && config.RacingDataHub.isEnabledForHorseRacing;
    const nextRacesConfig = config && config.NextRaces;
    const range = this.getDatesRange();
    const isVirtualRacesEnabled = this.isVirtualRacesEnabled(nextRacesConfig);
    if(!isVirtualRacesEnabled) {
      nextRacesConfig.isVirtualRacesEnabled = 'No'
    }
    const filterObject: IFilterParam = {
      //means get only events with market name AND ONLY market with name
      [isVirtualRacesEnabled ? 'marketTemplateMarketNameIntersects': 'templateMarketNameOnlyEquals']: this.getMarketsTemplates(isVirtualRacesEnabled),
      // events with specific Flag Codes Types
      [nextRacesConfig.typeID ? 'typeId' : 'typeFlagCodes']: this.getTypeFlagInfo(nextRacesConfig, true),
      // silks, jockeys
      racingFormOutcome: !racingDataHubEnabled || isVirtualRacesEnabled,
      // outcomes (selections) count
      limitOutcomesCount: parseInt(nextRacesConfig.numberOfSelections, 10),
      // events can be delivered from SiteServer - only possible values 3/5/7/12
      siteServerEventsCount: this.getEventsCount(nextRacesConfig),
      // events count to show
      eventsCount: parseInt(nextRacesConfig.numberOfEvents, 10),
      // event start time (param valid when typeId is set)
      startTime: nextRacesConfig.typeID ? nextRacesConfig.typeDateRange.from : range.from,
      // event end time (param valid when typeId is set)
      endTime: nextRacesConfig.typeID ? nextRacesConfig.typeDateRange.to : range.to
    };

    if (nextRacesConfig.showPricedOnly === 'Yes') {
      // events with LP bet type market
      filterObject.priceTypeCodesExists = 'LP';
    }

    if(isVirtualRacesEnabled){
      filterObject.isVirtualRacesEnabled = isVirtualRacesEnabled;
      filterObject.virtualRacesIncluded = nextRacesConfig && nextRacesConfig.virtualRacesIncluded;
    }
    return filterObject;
  }

  /**
   * form required events from event data received from siteServ
   * @return {object}
   */
  protected getEventsFromCache(moduleName: string): IFeaturedModel {
    return this.cacheEventsService.stored(this.cacheKey, 'nextFour',
      this.getNextRacesModuleConfigStrict(moduleName).categoryId.toString());
  }

  /**
   * Get 25 hours range to display delayed races on Next Races
   */
  protected getDatesRange(): IConstant {
    const to = new Date();
    to.setHours(to.getHours() - 1);
    const from = new Date(to);
    to.setHours(to.getHours() + 25);

    return {
      from: from.toISOString(),
      to: to.toISOString()
    };
  }
}
