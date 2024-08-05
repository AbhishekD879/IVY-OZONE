import { DomSanitizer } from '@angular/platform-browser';
import {
  Component,
  OnInit,
  Input,
  Output,
  ElementRef,
  OnDestroy,
  EventEmitter,
  ComponentFactoryResolver,
  ChangeDetectorRef
} from '@angular/core';

import { RendererService } from '@shared/services/renderer/renderer.service';
import { DeviceService } from '@core/services/device/device.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { SessionService } from '@authModule/services/session/session.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StreamTrackingService } from '@sb/services/streamTracking/stream-tracking.service';
import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import { IStreamProvidersResponse, IPerformGroupConfig } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { PerformGroupService } from '@lazy-modules/eventVideoStream/services/performGroup/perform-group.service';
import { AtTheRacesService } from '@lazy-modules/eventVideoStream/services/atTheRaces/at-the-races.service';
import { RacingStreamService } from '@lazy-modules/eventVideoStream/services/racingStream/racing-stream.service';
import { ImgService } from '@lazy-modules/eventVideoStream/services/imgService/img.service';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { LoadVideoJSService } from '@lazy-modules/eventVideoStream/services/loadVideojs/load-videojs.service';
import { ConvivaService } from '@lazy-modules/eventVideoStream/services/conviva/conviva.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { IGameMediaService } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-game-media.service';
import { StreamBetProviderComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers/stream-bet-provider.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { StorageService } from '@core/services/storage/storage.service';

@Component({
  selector: 'stream-bet-ios-provider',
  templateUrl: './stream-bet-ios-provider.component.html',
  styleUrls: ['./stream-bet-ios-provider.component.scss']
})
export class StreamBetIOSProviderComponent extends StreamBetProviderComponent implements OnInit, OnDestroy {

  @Input() eventEntity: ISportEvent;
  @Input() autoPlay: boolean;
  @Input() colorSchema: string;
  @Input() providerInfo?: IStreamProvidersResponse;
  @Input() streamCache?: Map<string | number, IStreamProvidersResponse>;
  @Input() performConfig: IPerformGroupConfig;
  @Input() streamUniqueId: string;
  @Input() isMyBets: boolean;
  @Input() streamUrl: any;
  @Input() showCSBIframe: boolean ;
  
  @Output() readonly playStreamError = new EventEmitter();
  @Output() readonly liveStreamStarted = new EventEmitter();

  constructor(
    public performGroupService: PerformGroupService,
    public sanitizer: DomSanitizer,
    public elementRef: ElementRef<HTMLElement>,
    public userService: UserService,
    public windowRefService: WindowRefService,
    public cmsService: CmsService,
    public commandService: CommandService,
    public atTheRacesService: AtTheRacesService,
    public watchRulesService: WatchRulesService,
    public imgService: ImgService,
    public racingStreamService: RacingStreamService,
    public nativeBridgeService: NativeBridgeService,
    public localeService: LocaleService,
    public loadVideoJsService: LoadVideoJSService,
    public streamTrackingService: StreamTrackingService,
    public gtmService: GtmService,
    public sessionService: SessionService,
    public deviceService: DeviceService,
    public liveStreamService: LiveStreamService,
    public eventVideoStreamProvider: EventVideoStreamProviderService,
    public rendererService: RendererService,
    public convivaService: ConvivaService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected quickbetService: QuickbetService,
    protected pubsub: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected remoteBetslipService: RemoteBetslipService,
    protected clientUserAgentService: ClientUserAgentService,
    protected iGameMediaService: IGameMediaService,
    protected storageService: StorageService
  ) {
    super(performGroupService,
      sanitizer,
      elementRef,
      userService,
      windowRefService,
      cmsService,
      commandService,
      atTheRacesService,
      watchRulesService,
      imgService,
      racingStreamService,
      nativeBridgeService,
      localeService,
      loadVideoJsService,
      streamTrackingService,
      gtmService,
      sessionService,
      deviceService,
      liveStreamService,
      eventVideoStreamProvider,
      rendererService,
      convivaService,
      dialogService,
      componentFactoryResolver,
      quickbetService,
      pubsub,
      changeDetectorRef,
      remoteBetslipService,
      clientUserAgentService,
      iGameMediaService, 
      storageService
      );
  }
 
  private renderLandscapeVideoMode():void {
    this.tutorialPlayer && this.isWrapper && !this.tutorialPlayer.isDisposed_  && this.tutorialPlayer.enterFullWindow();
    this.tutorialPlayer &&  !this.tutorialPlayer.isDisposed_ && !this.isWrapper && this.renderLandscapeErrorScreen(true);
    if(this.desktopPlayer && !this.isFullScreen && this.isWrapper){
      if (this.desktopPlayer.requestFullscreen) {
        this.desktopPlayer.requestFullscreen();
      } else if (this.desktopPlayer.webkitRequestFullscreen) {
        this.desktopPlayer.webkitRequestFullscreen();
      }
    }
    if(!this.isWrapper){
      const homeBody = this.windowRefService.document.querySelector('html, body');
      if (homeBody) {
      this.rendererService.renderer.removeStyle(homeBody, 'overflow');
      this.rendererService.renderer.setStyle(homeBody, 'height','500%');
      }
    }
    this.appendOverlayElement();
  }

  protected handleStreamEnd() {
    this.desktopPlayer.dispose();
    const homeBody = this.windowRefService.document.querySelector('html, body');
    homeBody && !this.isWrapper && this.rendererService.renderer.removeStyle(homeBody, 'height');
    this.renderLandscapeErrorScreen(this.isLandscapeMode());
    this.setExitScreenFlags();
    this.exitFullScreen();
    this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'snb-video-container');
    this.showVideoPlayer = false;
    this.isPlayerVisible = false;
    this.handleVideoPlayerPlaceholder(false);
    this.pubsub.publish(this.pubsub.API.PIN_TOP_BAR, false);
    this.showSnBOverlay = false;
  }

  protected checkOrientationMode(isPlaying: boolean = false):void {
    const homeBody = this.windowRefService.document.querySelector('html, body');
    if (this.isLandscapeMode()) {
      if(isPlaying && this.deviceService.isWrapper) {
        this.hideLandscapeErrorScreen();
      }
      this.renderLandscapeVideoMode();
      this.handleDesktopPlayerVisibility();
    } else {
      if(this.isWrapper){
        this.desktopPlayer && this.desktopPlayer.exitFullWindow();
        homeBody && this.rendererService.renderer.removeStyle(homeBody, 'overflow');
        this.tutorialPlayer && !this.tutorialPlayer.isDisposed_  && this.tutorialPlayer.exitFullWindow();
      }
      homeBody && !this.isWrapper && this.rendererService.renderer.removeStyle(homeBody, 'height');
      this.isFullScreen && this.openFullScreen();
      this.quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
      this.handleVideoPlayerPlaceholder(true);
    }
  }
}
