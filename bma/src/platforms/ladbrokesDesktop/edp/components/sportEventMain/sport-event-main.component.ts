import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as _ from 'underscore';

import { DeviceService } from '@core/services/device/device.service';
import { VisEventService } from '@core/services/visEvent/vis-event.service';
import { VisDataHandlerService } from '@core/services/visDataHandler/vis-data-handler.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { SportEventPageProviderService } from '@app/edp/components/sportEventPage/sport-event-page-provider.service';
import { SportEventMainProviderService } from '@app/edp/components/sportEventMain/sport-event-main-provider.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';

import {
  SCOREBOARD_CONFIG, SCOREBOARDS_LOAD_ORDER
} from '@ladbrokesDesktop/edp/components/sportEventMain/sport-event-main.constant';
import { SportEventMainComponent } from '@ladbrokesMobile/edp/components/sportEventMain/sport-event-main.component';

import { ISportEvent } from '@core/models/sport-event.model';
import { TimeService } from '@app/core/services/time/time.service';
import { IStreamsCssClasses } from '@core/models/streams-css-classes.model';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { CashOutMapService } from '@app/betHistory/services/cashOutMap/cash-out-map.service';
import { Observable } from 'rxjs';
import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import { StorageService } from '@app/core/services/storage/storage.service';

@Component({
  selector: 'sport-event-main',
  templateUrl: './sport-event-main.component.html',
  styleUrls: ['./sport-event-main.component.scss']
})
export class DesktopSportEventMainComponent extends SportEventMainComponent implements OnInit {
  isOlympics: boolean;
  cssClassesForStreams: IStreamsCssClasses = {
    iGameMedia: '',
    otherProviders: 'live-column watch-live'
  };

  protected eventStartDatePattern: string = 'EEEE, d-MMM-yy, h:mm aaa';
  protected scoreboardsLoadOrder = SCOREBOARDS_LOAD_ORDER;

  constructor(
    deviceService: DeviceService,
    activatedRoute: ActivatedRoute,
    visEventService: VisEventService,
    visDataHandler: VisDataHandlerService,
    pubSubService: PubSubService,
    cmsService: CmsService,
    gtmService: GtmService,
    localeService: LocaleService,
    commandService: CommandService,
    nativeBridgeService: NativeBridgeService,
    eventVideoStreamProviderService: EventVideoStreamProviderService,
    coreTools: CoreToolsService,
    userService: UserService,
    windowRef: WindowRefService,
    sportEventPageProviderService: SportEventPageProviderService,
    sportEventMainProviderService: SportEventMainProviderService,
    rendererService: RendererService,
    timeService: TimeService,
    scoreParserService: ScoreParserService,
    sportEventHelperService: SportEventHelperService,
    changeDetectorRef: ChangeDetectorRef,
    sportsConfigService: SportsConfigService,
    updateEventService: UpdateEventService,
    cashOutMapService: CashOutMapService,
    cashoutWsConnectorService: CashoutWsConnectorService,
    router: Router,
    routingHelperService: RoutingHelperService,
    storageService: StorageService
  ) {
    super(deviceService, activatedRoute, visEventService, visDataHandler,
      pubSubService, cmsService, gtmService, localeService, commandService, nativeBridgeService,
      eventVideoStreamProviderService, coreTools, userService, windowRef,
      sportEventPageProviderService, sportEventMainProviderService, rendererService, timeService,
      changeDetectorRef, scoreParserService, sportsConfigService, updateEventService, cashOutMapService, cashoutWsConnectorService,
      router, routingHelperService,storageService, sportEventHelperService);
  }

  init(): Observable<any> {
    this.isOlympics = this.sport && this.sport.extension && this.sport.extension === 'olympics';
    return super.init();
  }

  /**
   * Specific method for desktop only. Check if scoreboard available for desktop and/or check if fallbackScoreboard are available.
   * @returns {boolean}
   */
  isDesktopScoreboardAvailable(): boolean {
    const isScoresAvailable = this.eventEntity.comments && this.eventEntity.comments.teams;
    const isAvailableInConfig = _.find(SCOREBOARD_CONFIG, (configSportName: string) => {
      return configSportName === this.sportName;
    });
    return (isAvailableInConfig && isScoresAvailable && this.eventEntity.eventIsLive) || this.isFallbackScoreboards;
  }

  isLiveStreamAvailable(): boolean {
    return (!this.showMatchLive || !this.isMatchLive) && this.eventEntity.liveStreamAvailable;
  }

  isOutrightEvent(event: ISportEvent): boolean {
    return this.sportEventHelperService.isOutrightEvent(event);
  }

  /**
   * Toggle Live Button between WatchLive && isMatchLive
   */
  toggleLive(event: MouseEvent): void {
    event.preventDefault();
    this.showMatchLive = !this.showMatchLive;
  }
}
