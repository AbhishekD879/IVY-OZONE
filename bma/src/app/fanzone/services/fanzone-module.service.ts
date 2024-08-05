import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { VanillaApiService } from '@frontend/vanilla/core';
import { IFanzoneTab } from '@app/fanzone/models/fanzone-tab.model';
import { IFanzoneSiteCoreBanner } from '@app/fanzone/models/fanzone.model';
import { FANZONE } from '@app/fanzone/constants/fanzoneconstants';
import { SiteServerRequestHelperService } from '@app/core/services/siteServerRequestHelper/site-server-request-helper.service';
import { TimeService } from '@app/core/services/time/time.service';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { IOutrightsConfig } from '@app/shared/models/outrights-config.model';
import { SiteServerUtilityService } from '@app/core/services/siteServerUtility/site-server-utility.service';
import { BuildUtilityService } from '@app/core/services/buildUtility/build-utility.service';
import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { ISportEventEntity } from '@app/core/models/sport-event-entity.model';
import { ISportEvent } from '@app/core/models/sport-event.model';

@Injectable()
export class FanzoneAppModuleService {
  readonly PATH: string = FANZONE.modulePath;
  OUTRIGHTS_CONFIG: IOutrightsConfig;

  constructor(private vanillaApiService: VanillaApiService,
    private siteServerRequestHelperService: SiteServerRequestHelperService,
    protected timeService: TimeService,
    private ssUtility: SiteServerUtilityService,
    protected buildUtility: BuildUtilityService,
    protected simpleFilters: SimpleFiltersService) {
    this.OUTRIGHTS_CONFIG = OUTRIGHTS_CONFIG;
  }

  /**
   * Retrieves list of fanzone banners from sitecore
   *  @return {Observable<IFanzoneSiteCoreBanner>}
   */
  getFanzoneImagesFromSiteCore(): Observable<IFanzoneSiteCoreBanner[]> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(this.PATH, '', APIOPTIONS);
  }

  /**
 * @param {string} tabName
 * @param {string} id
 * @param {string} url
 * @param {string} visible
 * @return {IFanzoneTab}
 */
  createTab(tabName: string, id: string, url: string = '', visible = true, newSignPostingIcon = false): IFanzoneTab {
    return {
      title: tabName,
      id: id,
      url: url,
      visible: visible,
      showTabOn: 'both',
      newSignPostingIcon 
    };
  }

  /**
  * Loads events by type ids and for events that are outrights events
  * @param {string} fanzoneCompetitionIds
  * @param {string} fanzoneTeamId
  * @returns {Promise<ISportEvent[]>}
  */
  getFanzoneOutrights(fanzoneCompetitionIds: string, fanzoneTeamId: string): Promise<ISportEvent[]> {
    const params = {
      siteChannels: 'M',
      isNotResulted: true,
      eventSortCode: this.OUTRIGHTS_CONFIG.sportSortCode,
      outcomeTeamExtIds: fanzoneTeamId,
      suspendAtTime: this.timeService.getSuspendAtTime()
      
    };

    const requestParams = {
      typeId: fanzoneCompetitionIds,
      simpleFilters: this.simpleFilters.genFilters(params)
    };

    return this.ssUtility.queryService(data => this.siteServerRequestHelperService.getOutrightsByTypeIds(data), requestParams)
      .then((data) => {
        const eventEntity = data;
        eventEntity.forEach((event: ISportEventEntity, index: number) => {
          eventEntity[index] = this.buildUtility.eventBuilder(event);
        });
        return eventEntity;
      });
  }

}
