import * as _ from 'underscore';

import { Component, OnInit } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { EventService } from '@sb/services/event/event.service';
import { NextRacesHomeService } from '@ladbrokesMobile/lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import {
  NextRacesHomeComponent as CoralNextRacesHomeComponent
} from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.component';
import { ICombinedRacingConfig, ISystemConfig } from '@core/services/cms/models/system-config';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { Router } from '@angular/router';
import { DeviceService } from '@core/services/device/device.service';
import { ladbrokesGreyhoundConfig } from '@ladbrokesMobile/core/services/racing/config/greyhound.config';
import { ISportEvent } from '@core/models/sport-event.model';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service'; 
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service'; 
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'next-races-home',
  templateUrl: 'next-races-home.component.html'
})
export class NextRacesHomeComponent extends CoralNextRacesHomeComponent implements  OnInit {
  private schemaUrlsConfig = [
    '/greyhound-racing',
    ladbrokesGreyhoundConfig.tabs[0].url
  ];
  constructor(
    public pubSubService: PubSubService,
    public cmsService: CmsService,
    public nextRacesHomeService: NextRacesHomeService,
    public eventService: EventService,
    public racingPostService: RacingPostService,
    protected deviceService: DeviceService,
    protected routingHelperService: RoutingHelperService,
    protected router: Router,
    protected updateEventService: UpdateEventService,
    public horseRacingService: HorseracingService, 
    public greyhoundService: GreyhoundService,
    public routingState: RoutingState,
    protected windowRefService: WindowRefService
  ) {
    super(
      pubSubService,
      cmsService,
      nextRacesHomeService,
      eventService,
      racingPostService,
      deviceService,
      routingHelperService,
      router,
      updateEventService,
      horseRacingService,
      greyhoundService,
      routingState,
      windowRefService
      );
  }

  /**
   * Init function for(callbacks, watchers, scope destroying)
   * @private
   */
  ngOnInit(): void {
    super.ngOnInit();
    this.deviceService.isRobot() && this.schemaForGHNextRaces();
  }

  /**
   * Get data from Cms config
   */
  getCmsConfigs(): void {
    let storedConfig: ICombinedRacingConfig;

    /* eslint-disable-next-line */
    this.pubSubService.subscribe(this.MODULE_NAME, this.pubSubService.API.SYSTEM_CONFIG_UPDATED, (data: ISystemConfig) => {
      this.showFilter = false;
      if (this.moduleType === 'horseracing') {
        this.filterAccess = data.NextRacesFiltersHorseRacing || {};
      } else if (this.moduleType !== 'horseracing') {
        this.filterAccess = data.NextRacesFiltersGreyHounds || {};
        this.isNxtTabEnabled = data.GreyhoundNextRacesToggle && data.GreyhoundNextRacesToggle.nextRacesTabEnabled;
      }
     this.showFilter = this.filterAccess['EnableFilters'] || false;
      const updatedConfig: ICombinedRacingConfig = {
        NextRaces: data.NextRaces,
        RacingDataHub: data.RacingDataHub,
        GreyhoundNextRaces: data.GreyhoundNextRaces
      };

      if (updatedConfig.NextRaces && !_.isEqual(updatedConfig, storedConfig)) {
        storedConfig = updatedConfig;
        this.moduleTitle = updatedConfig.NextRaces.title;
        // All nextRacesModule configuration
        this.nextRacesModule = this.nextRacesHomeService.getNextRacesModuleConfig(this.moduleType, updatedConfig);
        this.leftTitleText = this.moduleTitle;
        this.getNextEvents();
      }
    });
  }
  /**
   * schema for Grey Hounds Next Races
   * @param nextRaces 
   */
  private schemaForGHNextRaces(): void {
    this.pubSubService.subscribe(this.MODULE_NAME, this.pubSubService.API.NEXT_RACES_DATA, (nextRaces: ISportEvent[])=>{
      this.schemaUrl = this.raceEvent === this.GREYHOUNDS && ladbrokesGreyhoundConfig.tabs[0].url.replace('/', '');
      if (this.schemaUrl === this.router?.url?.replace('/', '')) {
        nextRaces?.forEach((event: ISportEvent) => {
          const edpUrl: string = event && this.routingHelperService.formEdpUrl(event);
          event.url = edpUrl && edpUrl.replace('/', '');
        });
        nextRaces && this.pubSubService.publish(this.pubSubService.API.SCHEMA_DATA_UPDATED, [nextRaces, this.schemaUrl]);
      }
    });
  }
}
