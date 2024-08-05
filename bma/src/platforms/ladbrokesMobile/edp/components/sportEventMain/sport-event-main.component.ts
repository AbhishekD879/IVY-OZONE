import { ChangeDetectorRef, Component } from '@angular/core';
import { SportEventMainComponent as AppSportEventMainComponent } from '@edp/components/sportEventMain/sport-event-main.component';
import { SCOREBOARDS_LOAD_ORDER } from '@ladbrokesMobile/edp/components/sportEventMain/sport-event-main.constant';
import { ActivatedRoute, Router } from '@angular/router';
import { DeviceService } from '@core/services/device/device.service';
import { VisEventService } from '@core/services/visEvent/vis-event.service';
import { VisDataHandlerService } from '@core/services/visDataHandler/vis-data-handler.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { SportEventPageProviderService } from '@edp/components/sportEventPage/sport-event-page-provider.service';
import { SportEventMainProviderService } from '@edp/components/sportEventMain/sport-event-main-provider.service';
import { TimeService } from '@core/services/time/time.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { forkJoin, Observable } from 'rxjs';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { CashOutMapService } from '@app/betHistory/services/cashOutMap/cash-out-map.service';
import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { SportEventHelperService } from '@app/core/services/sportEventHelper/sport-event-helper.service';

@Component({
  selector: 'sport-event-main',
  templateUrl: './sport-event-main.component.html',
  styleUrls: ['./sport-event-main.component.scss']
})
export class SportEventMainComponent extends AppSportEventMainComponent {
  protected scoreboardsLoadOrder = SCOREBOARDS_LOAD_ORDER;
  protected scoreSports: string[] = ['BADMINTON', 'FOOTBALL'];

  constructor(deviceService: DeviceService,
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
              changeDetectorRef: ChangeDetectorRef,
              scoreParserService: ScoreParserService,
              sportsConfigService: SportsConfigService,
              // eslint-disable-next-line
              updateEventService: UpdateEventService, // for events subscription (done in service init)
              cashOutMapService: CashOutMapService,
              cashoutWsConnectorService: CashoutWsConnectorService,
              private router: Router,
              private routingHelperService: RoutingHelperService,
              public storageService: StorageService,
              sportEventHelperService: SportEventHelperService
              ) {
    super(deviceService,
      activatedRoute,
      visEventService,
      visDataHandler,
      pubSubService,
      cmsService,
      gtmService,
      localeService,
      commandService,
      nativeBridgeService,
      eventVideoStreamProviderService,
      coreTools,
      userService,
      windowRef,
      sportEventPageProviderService,
      sportEventMainProviderService,
      rendererService,
      timeService,
      changeDetectorRef,
      scoreParserService,
      sportsConfigService,
      // eslint-disable-next-line
      updateEventService,
      cashOutMapService,
      cashoutWsConnectorService,
      storageService,
      sportEventHelperService
      );
  }

  reloadComponent() {
    this.onPlayLiveStreamError();
    super.reloadComponent();
  }

  public goToCompetition(): void {
    const competitionUrl: string = this.routingHelperService.formCompetitionUrl({
      sport: this.eventEntity.categoryName,
      typeName: this.eventEntity.typeName,
      className: this.eventEntity.className
    });

    this.router.navigate([competitionUrl]);
  }

  getEventEntity(){
    if(!this.isMTASport()){
      return this.eventEntity;
    }
  }

  protected init(): Observable<any> {
    return forkJoin([
      this.getEventData(),
      this.setDS(),
      this.setEDPMarkets(),
      this.setSystemConfig(),
      this.setScoreBoards()
    ]);
  }

  // BMA-43784: My bets tab removed on ladbrokes. Override subscription for event bets updates.
  protected subscribeEditAccaChanges(): void {}
  protected subscribeForCahoutUpdates(): void {}
  protected subscribeForEventBetsUpdates(): void {}
}
