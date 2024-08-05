import { Component, OnInit, OnDestroy } from '@angular/core';

import { NextRacesModuleComponent as CoralNextRacesModuleComponent } from '@app/lazy-modules/nextRaces/component/next-races.component';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Location } from '@angular/common';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { NextRacesService } from '@app/core/services/racing/nextRaces/next-races.service';
import { EventService } from '@app/sb/services/event/event.service';
import { CommandService } from '@app/core/services/communication/command/command.service';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'next-races-module',
  templateUrl: 'next-races.component.html',
  styleUrls: ['./next-races.component.scss']
})

export class LadbrokesNextRacesModuleComponent extends CoralNextRacesModuleComponent implements OnInit, OnDestroy {

  isGermanUser: boolean = false;

  constructor(
    protected pubSubService: PubSubService,
    protected cmsService: CmsService,
    protected location: Location,
    protected routingHelperService: RoutingHelperService,
    protected nextRacesService: NextRacesService,
    protected eventService: EventService,
    protected commandService: CommandService,
    protected racingPostService: RacingPostService,
    private germanSupportService: GermanSupportService,
    protected windowRefService: WindowRefService,
    public horseRacingService: HorseracingService,
    public greyhoundService: GreyhoundService,
    public routingState: RoutingState,
    protected vEPService : VirtualEntryPointsService
  ) {
    super(pubSubService, cmsService, location, routingHelperService,
      nextRacesService, eventService, commandService, racingPostService, windowRefService,horseRacingService, greyhoundService, routingState,vEPService);
  }
  ngOnInit() {
    super.ngOnInit();
    this.isGermanUser = this.germanSupportService.isGermanUser();
    this.pubSubService.subscribe('LadbrokesNextRacesModuleComponent',
      [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
        this.isGermanUser = this.germanSupportService.isGermanUser();
      }
    );
  }

  ngOnDestroy() {
    super.ngOnDestroy();
    this.pubSubService.unsubscribe('LadbrokesNextRacesModuleComponent');
  }
}
