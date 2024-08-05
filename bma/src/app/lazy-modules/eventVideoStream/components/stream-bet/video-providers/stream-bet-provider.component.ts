import { of as observableOf, Observable, throwError, Subscription } from 'rxjs';

import { concatMap, take, map } from 'rxjs/operators';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
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
import * as _ from 'underscore';

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
import { IAtrRequestParamsModel } from '@lazy-modules/eventVideoStream/services/atTheRaces/at-the-races.models';
import { IImgConfigModel } from '@lazy-modules/eventVideoStream/services/imgService/img.model';
import { AtTheRacesService } from '@lazy-modules/eventVideoStream/services/atTheRaces/at-the-races.service';
import { RacingStreamService } from '@lazy-modules/eventVideoStream/services/racingStream/racing-stream.service';
import { ImgService } from '@lazy-modules/eventVideoStream/services/imgService/img.service';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { LoadVideoJSService } from '@lazy-modules/eventVideoStream/services/loadVideojs/load-videojs.service';
import { ConvivaService } from '@lazy-modules/eventVideoStream/services/conviva/conviva.service';
import { DialogService } from '@core/services/dialogService/dialog.service';

import {
  VideoStreamErrorDialogComponent
} from '@eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { IGameMediaService } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-game-media.service';
import {
  IIGameMediaStream
} from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';
import environment from '@environment/oxygenEnvConfig';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { StorageService } from '@app/core/services/storage/storage.service';
import { IStreamBetWeb } from '@core/services/cms/models/system-config';
@Component({
  selector: 'stream-bet-provider',
  templateUrl: './stream-bet-provider.component.html',
  styleUrls: ['./stream-bet-provider.component.scss']
})
export class StreamBetProviderComponent implements OnInit, OnDestroy {

  @Input() eventEntity: ISportEvent;
  @Input() autoPlay: boolean;
  @Input() colorSchema: string;
  @Input() providerInfo?: IStreamProvidersResponse;
  @Input() streamCache?: Map<string | number, IStreamProvidersResponse>;
  @Input() performConfig: IPerformGroupConfig;
  @Input() streamUniqueId: string;
  @Input() isMyBets: boolean;
  @Input() streamUrl: any;
  @Input() showCSBIframe: boolean;
  
  @Output() readonly playStreamError = new EventEmitter();
  @Output() readonly liveStreamStarted = new EventEmitter();

  streamingUrl: SafeUrl;
  frameWidth: number;
  frameHeight: number;
  showVideoPlayer: boolean;
  isWrapper: boolean;
  showPlayer: boolean;
  desktopPlayer;
  tutorialPlayer;
  playingTutorialVideo: boolean;
  errorMessage: string = '';
  isInactiveUserError: boolean;
  isConvivaEnabled: boolean;
  isVideoBlock: boolean = true;
  showtoaster: boolean = true;
  readonly HORSE_RACING_CATEGORY_ID = '21';
  public ERROR_MESSAGES = {
    loginRequired: false,
    servicesCrashed: false,
    eventNotStarted: false,
    eventFinished: false,
    onlyLoginRequired: false,
    onlyForMobile: false,
    deniedByWatchRules: false,
    deniedByInactiveWatchRules: false,
    geoBlocked: false,
    usageLimitsBreached: false,
    fairUseBreach: false
  };

  actionSubscriber: Subscription;
  streamFlowSubscriber: Subscription;
  trackErrors: string[] = [];
  resizeTimeFrame: number;
  canWatchEvent: boolean;
  resizeTimeout: number;
  streamID: string = null;
  streamActive: boolean;
  html5VideoTag: HTMLMediaElement;

  videJsTimeout: number;
  streamingConfig: IImgConfigModel | IAtrRequestParamsModel;
  resizeListerner: Function;
  selectionData: any;
  selection = {stake: 10};
  isFullScreen: boolean;
  outcomeSelected: boolean;
  betPlaced: boolean;
  selectedOutcome: any;
  showKeyboard;
  overlayButtonText = 'HIDE';
  filteredMarketGroups: any;
  marketCount;
  initialMarkets = 5;
  errorShown: boolean;
  isPlayerVisible: boolean;
  showSnBOverlay: boolean;
  tutorialStreaming: boolean;

  protected readonly DISPLAY_NONE_CLASS = 'd-none';
  protected readonly VANILLA_SLOT_HEADER_CLASS = 'slot-header';
  protected readonly VANILLA_SLOT_FOOTER_CLASS = 'slot-footer';
  protected readonly VANILLA_SLOT_BANNER_CLASS = 'slot-banner';
  protected readonly NETWORK_INDCIATIOR_CLASS = environment.brand === 'bma' ? '.network-indicator-parent' : '.network-indicator-parent-lads';
  isCoral: boolean = environment.brand === 'bma';
  streamBetCmsConfig: IStreamBetWeb;  

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
    this.handlePlayingStream = this.handlePlayingStream.bind(this);
    this.resizeView = this.resizeView.bind(this);
    this.setPlayerSize = this.setPlayerSize.bind(this);
    this.playStream = this.playStream.bind(this);
  }

  ngOnInit(): void {
    this.selectionData = this.quickbetService.getRestoredSelection();
    const streamCache = this.streamCache && this.streamCache.get(this.eventEntity.id);

    if (streamCache && streamCache.meta) {
      this.streamingConfig = streamCache.meta as (IImgConfigModel | IAtrRequestParamsModel);
    } else {
      console.warn('Please define on cms');
    }

    this.resizeTimeFrame = 500;

    this.windowRefService.nativeWindow.setTimeout(() => {
      this.html5VideoTag = this.elementRef.nativeElement.querySelector('#' + this.streamUniqueId);
      if (this.html5VideoTag) {
        // Event lister on event end.
        this.rendererService.renderer.listen(this.html5VideoTag, 'ended', () => {
          console.warn('Event stream is over');
          this.showError('eventFinished');
        });
        this.rendererService.renderer.listen(this.html5VideoTag, 'canplay', () => {
          this.isVideoBlock = false;
        });
        if (this.isConvivaEnabled) {
          this.convivaService.initVideoAnalytics(this.html5VideoTag as HTMLVideoElement, this.eventEntity);
        }
      }
    });

    this.actionSubscriber = this.eventVideoStreamProvider.showHideStreamListener.subscribe(this.handlePlayingStream);

    // register method to share stream status
    this.commandService.register(this.commandService.API.GET_LIVE_STREAM_STATUS, () => {
      return Promise.resolve({ streamID: this.streamID, streamActive: this.streamActive });
    });

    this.isWrapper = this.nativeBridgeService.supportsVideo();

    this.cmsService.getSystemConfig().subscribe((config) => {
      if (config.Conviva && config.Conviva.enabled) {
        this.isConvivaEnabled = true;
        this.convivaService.setConfig(config.Conviva);
        this.convivaService.preload();
      }
    });
    this.eventVideoStreamProvider.getStreamBetCmsConfig().subscribe((streamBetWeb:IStreamBetWeb) => {
      this.streamBetCmsConfig = streamBetWeb;
    });

    if (this.deviceService.performProviderIsMobile()) {
      this.resizeListerner = this.rendererService.renderer.listen(this.windowRefService.nativeWindow,
        'orientationchange', this.resizeView);
    }
    this.handlePlayingStream();
  }
  
  private onResizeOrOrientationChange(): void {
    if (this.deviceService.isAndroid && this.isLandscapeMode()) {
        this.appendOverlayElement();
      if(this.tutorialPlayer){
        this.isFullScreen = this.tutorialPlayer.isFullscreen();
      }
      if(this.desktopPlayer){
        this.isFullScreen = this.desktopPlayer.isFullscreen();
      }
    }
  }

  protected appendOverlayElement(): void {
    const isVideoPlayer = this.elementRef.nativeElement.querySelector('#' + this.streamUniqueId);

    const overlayElem = this.windowRefService.document.querySelector('#overlay-wrapper');
    const overlayHeaderElem = this.windowRefService.document.querySelector('.overlay-header-container');
    const html5VideoTag = this.elementRef.nativeElement.querySelectorAll('video');
    html5VideoTag?.forEach((videoElement:HTMLVideoElement)=>{
      videoElement && this.rendererService.renderer.addClass(videoElement, 'fit-screen');
     });
    if (overlayElem && overlayHeaderElem && isVideoPlayer && !isVideoPlayer.contains(overlayElem)) {
      (isVideoPlayer as any).appendChild(overlayElem as any);
      (isVideoPlayer as any).appendChild(overlayHeaderElem as any);
    }
  }

  ngOnDestroy(): void {
    if (this.desktopPlayer) {
      this.renderLandscapeErrorScreen(this.isLandscapeMode());
      this.desktopPlayer.exitFullWindow();
      this.exitFullScreen();
      !this.desktopPlayer.isDisposed_ && this.desktopPlayer.dispose();
    }
    this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'snb-video-container'); 
    this.tutorialPlayer && !this.tutorialPlayer.isDisposed_ && this.tutorialPlayer.dispose();
    this.handleVideoPlayerPlaceholder(false, false);
    this.showVideoPlayer = false;
    this.isPlayerVisible = false;
    this.pubsub.publish(this.pubsub.API.PIN_TOP_BAR, false);
    const homeBody = this.windowRefService.document.querySelector('html, body');
    if (homeBody) {
    this.rendererService.renderer.removeStyle(homeBody, 'overflow');
    this.rendererService.renderer.removeStyle(homeBody, 'height');
    }
    this.actionSubscriber && this.actionSubscriber.unsubscribe();
    this.streamFlowSubscriber && this.streamFlowSubscriber.unsubscribe();
    this.windowRefService.nativeWindow.clearTimeout(this.videJsTimeout);
    this.commandService.unregister(this.commandService.API.GET_LIVE_STREAM_STATUS);
    if (this.resizeListerner) {
      this.resizeListerner();
    }
    this.isConvivaEnabled && this.convivaService.release(this.eventEntity.id);
    const toasterElement = this.elementRef.nativeElement.querySelector('#toaster');
    toasterElement && toasterElement.classList.add('hide-element');
    this.showSnBOverlay = false;
    this.tutorialStreaming = false;
  }
  playtutorialvideo() {
    this.playingTutorialVideo = true;
    this.showtoaster = false;
    const tutorialVideo = this.elementRef.nativeElement.querySelector('#tutorial');
    this.tutorialPlayer = tutorialVideo ? this.windowRefService.nativeWindow.videojs('tutorial', {
      muted: true, // major browsers do not support autoplay with sound.
      techOrder: ['html5', 'flash'],
      preferFullWindow: true,
      fluid: true,
      html5: { nativeTextTracks: false },
      nativeControlsForTouch: false,
      controlBar: {
        fullscreenToggle: false,
        pictureInPictureToggle: false   
      }
    }) : null;
    if(this.tutorialPlayer) {
      this.tutorialPlayer.src({
        // ToDo: SnB
        type: 'video/mp4',
        src: this.streamBetCmsConfig.tutorialVideoUrl
      });
      this.tutorialPlayer.on('canplay', () => {
        const videoSpinner = this.windowRefService.document.querySelector('.vjs-loading-spinner');
        setTimeout(() => {
          videoSpinner && videoSpinner.classList.remove('snb-loading');
        });
        const isTutorialPlayer = this.elementRef.nativeElement.querySelectorAll('#tutorial');
        isTutorialPlayer && isTutorialPlayer[0].classList.remove('hide-tutorial');       
        if(this.isLandscapeMode() && this.deviceService.isWrapper) {
          this.hideLandscapeErrorScreen();
          this.rendererService.renderer.addClass(this.windowRefService.document.body, 'snb-video-container');
          this.openFullScreen();
          this.tutorialPlayer.enterFullWindow();
        } 
        this.handleDesktopPlayerVisibility();
        this.handleVideoPlayerPlaceholder(true);
      });
      this.tutorialPlayer.on('ready', () => {
        this.tutorialStreaming = true;
        this.tutorialPlayer.play();
        if(this.desktopPlayer){
          this.desktopPlayer.volume(0);
        }
      });
      this.tutorialPlayer.on('ended', () => {
        this.tutorialStreaming = false;
        if(this.desktopPlayer){
          this.desktopPlayer.volume(1);
        }
        this.playingTutorialVideo = false;
        this.tutorialPlayer.dispose();
        this.desktopPlayer.play();
        this.handleDesktopPlayerVisibility();
        this.displayStreamMessages();
        this.showSnBOverlay = true;
      });
    }
  }

  /**
   * Enable visibility of desktop player portion
   */
  handleDesktopPlayerVisibility(): void {
    const isVideoPlayer = this.elementRef.nativeElement.querySelectorAll('#' + this.streamUniqueId);
    if(!this.playingTutorialVideo && !this.errorMessage && this.showPlayer) {
      this.isPlayerVisible = true;
      isVideoPlayer && isVideoPlayer[0].classList.remove('hide-element');

      if(this.isLandscapeMode() && this.deviceService.isWrapper) {

        this.hideLandscapeErrorScreen();
        this.rendererService.renderer.addClass(this.windowRefService.document.body, 'snb-video-container');
        this.pubsub.publish(pubSubApi.STREAM_BET_VIDEO_MODE, true);

        if((this.desktopPlayer && !this.desktopPlayer.isDisposed_ && !this.desktopPlayer.isFullscreen()) || 
          (this.tutorialPlayer && !this.tutorialPlayer.isDisposed_ && !this.tutorialPlayer.isFullscreen())) {
          this.checkOrientationMode(true);
        }
      }     
      this.handleVideoPlayerPlaceholder(true, false);
    } else {
      isVideoPlayer && isVideoPlayer[0].classList.add('hide-element');
      this.isPlayerVisible = false;
    }
  }

  playStream($event?): void {
    if ($event) {
      $event.preventDefault();
    }
    this.windowRefService.nativeWindow.clearTimeout(this.videJsTimeout);
    const isVideoPlayer = this.elementRef.nativeElement.querySelector('#'+this.streamUniqueId);

    // not needed everything ned to load via videojs
    // Init desktop player using
    if(!this.desktopPlayer) {
    this.desktopPlayer = isVideoPlayer ? this.windowRefService.nativeWindow.videojs(this.streamUniqueId, {
      muted: this.deviceService.isIos, // major browsers do not support autoplay with sound.
      techOrder: ['html5', 'flash'],
      fluid: true,
      preferFullWindow: true,
      html5 : {nativeTextTracks:false}, // to remove cc in ios
      controlBar: {
        // TODO: SnB enabling FS and PIP for mobile
        fullscreenToggle: true,
        pictureInPictureToggle: false
      },
      suppressNotSupportedError: true,
      userActions: {
        click: false,
        doubleClick: false
     },
     inactivityTimeout: 0
    }) : null;

    if (this.desktopPlayer) {
      const max_retryLimit: number = 10;
      let count: number = 0;
      this.desktopPlayer.on('error', () => {
        this.handlePlayerError();
      });
      this.desktopPlayer.on('ended', () => {
        this.handleStreamEnd();
      });
      this.desktopPlayer.tech().on('retryplaylist', () => {
        count = count + 1;
        if (count === max_retryLimit) {
          this.handleStreamEnd();
        }
      });
      
      const videoSpinner = this.windowRefService.document.querySelector('.vjs-loading-spinner');
      this.desktopPlayer.on('canplay', () => {
        setTimeout(() => {
          videoSpinner && videoSpinner.classList.remove('snb-loading');
        });
      });
      this.desktopPlayer.on('waiting', () => {
        setTimeout(() => {
          videoSpinner && videoSpinner.classList.remove('snb-loading');
        });
      });

     this.desktopPlayer.on('fullscreenchange',  () => {
        this.isFullScreen = this.desktopPlayer.isFullscreen();
        if(this.isFullScreen) {
          if(this.deviceService.isIos && this.deviceService.isWrapper){
            this.handleDesktopPlayerVisibility();
          }
          else{
            this.rendererService.renderer.addClass(this.windowRefService.document.body, 'snb-video-container');
            this.hideLandscapeErrorScreen();
            this.pubsub.publish(pubSubApi.STREAM_BET_VIDEO_MODE,true); 
          }
          this.openFullScreen();
        } else {
         this.renderLandscapeErrorScreen(this.isLandscapeMode());
         this.setExitScreenFlags();
         this.exitFullScreen();
        }
      });
      this.isConvivaEnabled && this.convivaService.initVideoJsAnalytics(this.desktopPlayer, this.eventEntity);
    }
    if(this.streamBetCmsConfig.isAndroidStream) {
      const url = this.streamBetCmsConfig.isAndroidStreamURL;
      this.showPlayer = true;
      this.handleDesktopPlayerVisibility();
      return this.runVideoJsPlayer(url);
    }
    if(this.streamBetCmsConfig.isIOSStream) {
      const url = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8";
      this.showPlayer = true;
      this.handleDesktopPlayerVisibility();
      return this.runVideoJsPlayer(url);
    }
    // Hides all error messages
    this.hideAllErrorMessage();

    const streamUnavailableMessage = this.getStreamUnavailableMessage();

    // If CMS fails or error message code is available, display proper error message.
    if (streamUnavailableMessage) {
      this.onError(streamUnavailableMessage);
      return;
    }

    // streamFlow;

      this.streamFlowSubscriber = this.checkCanWatch().pipe(
        concatMap(() => this.getStreamNotStartedMessage()),
        concatMap(() => this.showHideStream(this.providerInfo)),
        take(1)
      ).subscribe((streamData: string|IIGameMediaStream) => {
          let stream;
          this.showPlayer = true;
          if(this.providerInfo.priorityProviderName === 'iGame Media') {
            stream = (streamData as IIGameMediaStream).streamLink;
          } else {
            stream = streamData;
          }
          if (!stream) {
            this.onError();
            return;
          }
          this.handleDesktopPlayerVisibility();
          this.onSuccess(stream);
          this.useCachedData();
          this.eventVideoStreamProvider.playSuccessErrorListener.next(true);
        }, (reason) => {
          this.onError(reason);
          this.eventVideoStreamProvider.playSuccessErrorListener.next(false);
        });
      } 
  }

  private displayStreamMessages(): void {
    this.changeDetectorRef.detectChanges();
    const streamMsgWrapper = this.elementRef.nativeElement.querySelector('.stream-msg-wrapper');
    streamMsgWrapper && streamMsgWrapper.classList.remove('hide-element');
    if (this.showtoaster) {
      const toasterElement = this.elementRef.nativeElement.querySelector('#toaster');
      toasterElement && toasterElement.classList.remove('hide-element');
      this.windowRefService.nativeWindow.setTimeout(() => {
        toasterElement && toasterElement.classList.add('hide-element');
        this.handleVideoPlayerPlaceholder(true, false);
      }, 3000);
    }
    this.handleVideoPlayerPlaceholder(true, false);
  }

  protected handleVideoPlayerPlaceholder(isVideoDisplayed: boolean, withDelay: boolean = true): void {
    const nativeVideoContainer = this.windowRefService.document.querySelector('.native-video-player-placeholder');
    if (nativeVideoContainer && this.deviceService.isWrapper) {
    if (((this.desktopPlayer && !this.desktopPlayer.isDisposed_ && this.desktopPlayer.isFullscreen()) || (this.tutorialPlayer && !this.tutorialPlayer.isDisposed_ && this.tutorialPlayer.isFullscreen())) || this.isLandscapeMode()) {
      nativeVideoContainer.classList.add('d-none');
      return;
    }
    nativeVideoContainer.classList.remove('d-none');
    if (withDelay) {
      setTimeout(() => {
        this.setVideoContainer(isVideoDisplayed, nativeVideoContainer as HTMLElement);
      },this.deviceService.isIos ? this.resizeTimeFrame : 0);
    } else {
      this.setVideoContainer(isVideoDisplayed, nativeVideoContainer as HTMLElement);
    }
  }
  }

  private setVideoContainer(isVideoDisplayed: boolean, nativeVideoContainer: HTMLElement): void {
    const videoContainer = this.elementRef.nativeElement.querySelector('.desktop-video-container');
    if (videoContainer && nativeVideoContainer) {
      nativeVideoContainer.style.height = `${isVideoDisplayed ? videoContainer.clientHeight : 0}px`;
      this.pubsub.publish(this.pubsub.API.IS_WEB_VIDEO_STICKED, nativeVideoContainer.style.height);
    }
    this.pubsub.publish(this.pubsub.API.PIN_TOP_BAR, this.showVideoPlayer);
  }

  protected handleStreamEnd() { 
    this.desktopPlayer.dispose();
    this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'snb-video-container');
    this.showVideoPlayer = false;
    this.isPlayerVisible = false;
    this.handleVideoPlayerPlaceholder(false);
    if(this.isLandscapeMode()) {
      this.renderLandscapeErrorScreen(true);
      this.errorShown = true;  
    }
    this.pubsub.publish(this.pubsub.API.PIN_TOP_BAR, false);
    this.showSnBOverlay = false;
  }

  public showErrorMessage(errorMessageType: string): void {
    // Check if there is not previously displayed messages
    let visibleErrorMessage;
    let errorMsgType;

    Object.keys(this.ERROR_MESSAGES).forEach((key: string) => {
      if (this.ERROR_MESSAGES[key]) {
        visibleErrorMessage = key;
      }
    });

    if (visibleErrorMessage && errorMessageType !== visibleErrorMessage) {
      this.ERROR_MESSAGES[visibleErrorMessage] = false;
    }

    // Shows proper error message
    if (this.ERROR_MESSAGES.hasOwnProperty(errorMessageType)) {
      errorMsgType = errorMessageType;
    } else {
      errorMsgType = 'servicesCrashed';
    }

    this.ERROR_MESSAGES[errorMsgType] = true;
    this.displayError(errorMsgType);
  }

  protected parseErrorMessage(): string {
    let error: string;
    Object.keys(this.ERROR_MESSAGES).forEach((key: string) => {
      if (this.ERROR_MESSAGES[key]) {
        error = key;
      }
    });

    return error ? this.localeService.getString(`sb.${error}`) : '';
  }

  private displayError(error: string): void {
    this.errorMessage = this.parseErrorMessage();     

      this.dialogService.openDialog(DialogService.API.videoStreamError,
        this.componentFactoryResolver.resolveComponentFactory(VideoStreamErrorDialogComponent), true, {
          errorMsg: this.localeService.getString(`sb.${error}`),
          eventEntity: this.eventEntity,
          isInactivePopup: this.watchRulesService.isInactiveUser(error)
        });
  }

  protected contextMenuListener(e: PointerEvent): void {
    e.preventDefault();
  }

  /**
   * Disable context menu on videoJS <video> tag
   */
  protected disableContextMenu(): void {
    this.html5VideoTag.addEventListener('contextmenu', this.contextMenuListener, false);
  }

  /**
   * Show or hide video stream logic
   */
  protected handlePlayingStream(): void {
      this.showPlayer = this.deviceService.isWrapper ? this.nativeBridgeService.playerStatus : this.showPlayer;
      if (!this.showPlayer) {
        this.autoPlayStream();
      } else {
        this.hideStream();
      }
  }

  protected hideStream(): void {
    this.streamActive = false;
    this.streamID = null;
    this.showPlayer = false;
    this.handleVideoPlayerPlaceholder(false, false);

    if (!this.deviceService.isWrapper && this.desktopPlayer) {
      this.desktopPlayer.reset();
    }

    this.nativeBridgeService.hideVideoStream();
    this.hideAllErrorMessage();
    this.eventVideoStreamProvider.playSuccessErrorListener.next(false);
  }

  protected onError(reason?: string): void {
    const eventId = this.eventEntity.id;
    const customReason = typeof reason === 'string' ? reason : 'servicesCrashed';

    this.showError(customReason);

    if (customReason === 'eventFinished' || customReason === 'usageLimitsBreached') {
      const storedStream = this.streamCache.get(eventId);

      if (storedStream) {
        storedStream.error = customReason;
      }
    }
    this.showVideoPlayer = false;

    this.playStreamError.emit(customReason);
    this.liveStreamStarted.emit();
  }

  protected onSuccess(stream: string): void {
    this.streamActive = true;
    const event = this.eventEntity,
      isDuplication = this.streamTrackingService.checkIdForDuplicates(event.id, 'liveStream');
    if (!isDuplication) {
      this.pushToDataLayer();
      this.streamTrackingService.addIdToTrackedList(event.id, 'liveStream');
    }
    this.streamCache.get(event.id).stream = stream || this.streamCache.get(event.id).stream;
    this.liveStreamStarted.emit();
  }

  protected useCachedData(): void {
    const eventId = this.eventEntity.id;
    if (this.streamCache.get(eventId).error) {
      this.showError(this.streamCache.get(eventId).error);
    } else if (this.streamCache.get(eventId).stream) {
      this.renderStream(this.streamCache.get(eventId).stream, eventId, this.eventEntity.categoryCode);
    }
  }

  protected renderStream(url: string, eventId: number, categoryCode: string): void {   
    
    if (!this.isMyBets && this.isWrapper && this.nativeBridgeService.supportsVideo() && url.indexOf('http') === 0) {
      const isDuplication = this.streamTrackingService.checkIdForDuplicates(this.eventEntity.id, 'liveStream');
      // Accept HTTP Live Stream only
      if (!isDuplication) {
        this.pushToDataLayer();
        this.streamTrackingService.addIdToTrackedList(this.eventEntity.id, 'liveStream');
      }
    } else {
      const playerElement = this.elementRef.nativeElement.querySelector('#'+this.streamUniqueId);
        this.streamTrackingService.setTrackingForPlayer((playerElement as HTMLElement & { id_: string }), this.eventEntity);
      }

      return this.runVideoJsPlayer(url);
  }

  protected renderHtml5Stream(url: string): void {
    if (this.deviceService.performProviderIsMobile()) {
      this.setPlayerSize();
      // Render video in html5
      this.streamingUrl = this.sanitizer.bypassSecurityTrustUrl(url);
    } else {
      this.showError('onlyForMobile');
    }
  }

  protected setPlayerSize(): void {
    // It is based on initial value taken from perform group
    const heightCoeficient = 1.78;
    const elWidth: number = this.performGroupService.getElementWidth(this.elementRef);

    // Initial size of container
    const width = elWidth
      ? elWidth
      : this.frameWidth;

    this.frameWidth = width;
    this.frameHeight = Math.floor(width / heightCoeficient);
    this.onResizeOrOrientationChange(); 
    if(this.isLandscapeMode()) {
      this.handleVideoPlayerPlaceholder(false, false);
    } else {
      this.handleVideoPlayerPlaceholder(true, false);
    }
  }

  protected runVideoJsPlayer(url: string): void {
    const eventId = this.eventEntity.id;

    if (this.desktopPlayer) {
      const isATRStream = this.providerInfo && this.providerInfo.priorityProviderName === 'At The Races'
        || this.eventEntity.streamProviders.ATR;
      this.streamCache.get(eventId).error = null;
      this.desktopPlayer.src({
        // ToDo: SnB
        type: this.streamBetCmsConfig.isAndroidStream || this.streamBetCmsConfig.isIOSStream ? 'application/x-mpegURL' : this.getVideoType(url),
        src: url,
        withCredentials: !isATRStream
      });
      this.desktopPlayer.ready(() => {
        const videoSpinner = this.windowRefService.document.querySelector('.vjs-loading-spinner');
        videoSpinner && videoSpinner.classList.add('snb-loading');     

        this.showVideoPlayer = true;
        const storedLimitValue = this.storageService.get('tutorialLimit') || 0;
        if(!storedLimitValue){
          this.storageService.set('tutorialLimit',1); 
        }
        if(storedLimitValue < this.streamBetCmsConfig.tutorialVideoLimit){
          this.storageService.set('tutorialLimit',storedLimitValue + 1);
          this.playtutorialvideo();
        }
        else{
           const tutorialVideo = this.elementRef.nativeElement.querySelector('#tutorial');
           tutorialVideo && this.rendererService.renderer.setStyle(tutorialVideo, 'display', 'none');           
           this.desktopPlayer.play();
           this.showSnBOverlay = true;
           this.displayStreamMessages();
        }
       this.streamTrackingService.setTrackingForPlayer(this.desktopPlayer, this.eventEntity);
      });
     this.handleFullScreenControl();
    }
  }

  private handleFullScreenControl() {
    this.elementRef.nativeElement.querySelector('.vjs-fullscreen-control')?.addEventListener('touchend', ()=> {
      if(screen.orientation.type === 'landscape-primary') {
        this.renderLandscapeErrorScreen(this.isLandscapeMode());
        this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'snb-video-container');         
        this.pubsub.publish(pubSubApi.STREAM_BET_VIDEO_MODE,false);
        if(!this.isLandscapeMode()) {
          this.exitFullScreen();
        }
      } else {
        if(this.deviceService.isWrapper && this.isFullScreen) {
          this.desktopPlayer.exitFullscreen();
        }
      }
    });
  }

  protected getVideoType(url: string): string {
    const result = url.match(/^(\w+):/),
      type = result ? result[1] : null,
      formats = {
        rtmp: 'rtmp',
        rtmpe: 'rtmpe'
      };

    return formats[type] || 'application/x-mpegURL';
  }

  protected pushToDataLayer(): void {
    const event = this.eventEntity;

    this.gtmService.push('trackEvent', {
      eventCategory: 'streaming',
      eventAction: 'click',
      eventLabel: 'watch video stream',
      sportID: event.categoryId,
      typeID: event.typeId,
      eventId: event.id
    });
  }

  protected showHideStream(providerInfo: IStreamProvidersResponse): any {
    const eventId = this.eventEntity.id;

    const isIGameMediaStream = providerInfo.priorityProviderName === 'iGame Media' || this.eventEntity.streamProviders.iGameMedia;
    // TODO: SnB Handle for igame media
    // existing code - start
    // if ((this.streamCache.get(eventId) && this.streamCache.get(eventId).error) || !this.performConfig) {
    //   return observableOf(null);
    // }
    // existing code - end
    // Handled for Igamemedia
    if((this.streamCache.get(eventId) && this.streamCache.get(eventId).error) || (!isIGameMediaStream && !this.performConfig))  {
      return observableOf(null);
    }
    

    this.getStreamId(providerInfo);

    const isIMGStream = providerInfo.priorityProviderName === 'IMG Video Streaming' || this.eventEntity.streamProviders.IMG;
    const isPerformStream = providerInfo.priorityProviderName === 'Perform' || this.eventEntity.streamProviders.Perform;
    const isATRStream = providerInfo.priorityProviderName === 'At The Races' || this.eventEntity.streamProviders.ATR;
    const isRUKorRPGTVstream = providerInfo.priorityProviderName === 'RacingUK' || providerInfo.priorityProviderName === 'RPGTV' ||
      (this.eventEntity.streamProviders.RacingUK || this.eventEntity.streamProviders.RPGTV);
    // Send request only when player is visible is another case do nothing
    if (isIMGStream) {
      // Init IMG stream with proper params.
      this.imgService.setConfigParams(
        (<IImgConfigModel>this.streamingConfig).operatorId,
        (<IImgConfigModel>this.streamingConfig).imgSecret
      );

      // Get video url
      return this.imgService.getVideoUrl(providerInfo);
    } else if (isPerformStream) {
      if (this.isWrapper) {
        // Gets perform group id from coral ip
        return this.performGroupService.performGroupId(providerInfo, this.performConfig, this.eventEntity.id).pipe(
          concatMap(() => {
            // Try to get mobile video stream
            return this.racingStreamService.getVideoUrl(providerInfo, this.performConfig);
          }));
      }
      if(this.showCSBIframe) {
        return this.performGroupService.performGroupId(providerInfo, this.performConfig, this.eventEntity.id).pipe(
          concatMap(() => observableOf(this.racingStreamService.getVideoCSBUrl(providerInfo, this.performConfig)))
        );
      }
      return this.racingStreamService.getVideoUrl(providerInfo, this.performConfig);
    } else if (isATRStream) {
      // Init ATR stream with proper params.
      this.atTheRacesService.setConfigParams(
        (<IAtrRequestParamsModel>this.streamingConfig).partnerCode,
        (<IAtrRequestParamsModel>this.streamingConfig).secret
      );

      return this.atTheRacesService.getVideoUrl(providerInfo);
    } else if (isIGameMediaStream) {
      return this.iGameMediaService.getStream(this.eventEntity, this.providerInfo, true);
    } else if (isRUKorRPGTVstream) {
      return this.racingStreamService.getVideoUrl(providerInfo, this.performConfig);
    }

    return throwError('servicesCrashed');
  }

  protected getStreamId(providerInfo: IStreamProvidersResponse): void {
    if (providerInfo && providerInfo.listOfMediaProviders &&
      providerInfo.listOfMediaProviders.length) {
      const priorityProvider = _.find(providerInfo.listOfMediaProviders,
        providerData => providerData.name === providerInfo.priorityProviderName);
      if (_.isArray(priorityProvider.children) && priorityProvider.children.length && priorityProvider.children[0].media) {
        const accessProperty = priorityProvider.children[0].media.accessProperties;
        let index = accessProperty.length;
        if (accessProperty.indexOf(',') !== -1) {
          index = accessProperty.indexOf(',');
        }
        const parseID = accessProperty.substring(accessProperty.indexOf(':') + 1, index);
        this.streamID = parseID === '0' ? null : parseID;
      }
    }
  }

  protected checkCanWatch(): Observable<boolean> {
    // reset stream status variables used for IGM
    this.streamID = null;
    this.streamActive = false;

    if (this.canWatchEvent) {
      return observableOf(true);
    } else {
      return this.watchRulesService
        .canWatchEvent(this.providerInfo, this.eventEntity.categoryId, this.eventEntity.id).pipe(map(() => {
          this.canWatchEvent = true;
      })) as any;
    }
  }

  protected getStreamNotStartedMessage(): Observable<string> {
    return _.some([
      this.eventEntity.streamProviders.Perform && !this.performGroupService.isEventStarted(this.eventEntity),
      this.eventEntity.streamProviders.IMG && !this.imgService.isEventStarted(this.eventEntity),
      (this.eventEntity.streamProviders.RacingUK || this.eventEntity.streamProviders.RPGTV) &&
      !this.racingStreamService.isEventStarted(this.eventEntity),
      this.eventEntity.streamProviders.ATR && !this.atTheRacesService.isEventStarted(this.eventEntity),
      this.eventEntity.streamProviders.iGameMedia && !this.iGameMediaService.isEventStarted(this.eventEntity)
    ]) ? throwError('eventNotStarted') : observableOf('');
  }

  protected getStreamUnavailableMessage(): string {
    let message = '';

    const isAtleastOneStreamAttached = _.find(this.eventEntity.streamProviders,
      streamAvalaible => streamAvalaible);

    if (!isAtleastOneStreamAttached) {
      message = 'servicesCrashed';
    } else if (this.eventEntity.isFinished) {
      message = 'eventFinished';
    }

    return message;
  }

  protected hideAllErrorMessage(): void {
    _.each(this.ERROR_MESSAGES, (value, id) => {
      this.ERROR_MESSAGES[id] = false;
    });
    this.isInactiveUserError = false;
    this.errorMessage = this.parseErrorMessage();
  }

  protected autoPlayStream(): void {
      this.showVideoPlayer = false;
      this.loadVideoJsService.loadScripts().subscribe(() => {
          this.windowRefService.nativeWindow.clearTimeout(this.videJsTimeout);
          this.videJsTimeout = this.windowRefService.nativeWindow.setTimeout(this.playStream);
      });
  }

  protected showError(errorType: string): void {
    const reason = errorType || 'servicesCrashed';
    const errorMsg = this.localeService.getString(`sb.${reason}`);
    const errorNotification = {
      event: 'trackEvent',
      eventCategory: 'Livestream',
      eventAction: 'error',
      liveStreamError: errorMsg
    };

    this.showPlayer = false;
    this.gtmService.push('trackEvent', errorNotification);

    // Is needed to avoid tracking errors duplication
    this.trackErrors.push(reason);
    if (reason === 'eventFinished') {
      this.eventEntity.isFinished = true;
    }
    this.isInactiveUserError = this.watchRulesService.isInactiveUser(reason);
    this.showErrorMessage(reason);
  }

  protected handlePlayerError(): void {
    const isRacing: boolean = this.liveStreamService.checkIfRacingEvent(this.eventEntity);
    const eventKey: string = _.findKey(this.ERROR_MESSAGES, (value) => value) || 'servicesCrashed';
    // First condition are for racing events.
    if (!isRacing && _.indexOf(this.trackErrors, eventKey) === -1) {
      const errorNotification = {
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error',
        liveStreamError: this.localeService.getString(`sb.${eventKey}`)
      };
      this.gtmService.push('trackEvent', errorNotification);
      this.trackErrors.push(eventKey);
    }
  }

  protected resizeView(): void {
    // Mobile-web
    if (!this.isFullScreen && !this.deviceService.isWrapper && this.isLandscapeMode()) {
      this.renderLandscapeErrorScreen(true);
      return;
    }
    else if(this.deviceService.isWrapper && this.isLandscapeMode() && 
    ((this.desktopPlayer && !this.desktopPlayer.isDisposed_ && !this.desktopPlayer.isFullscreen()) || 
    (this.tutorialPlayer && !this.tutorialPlayer.isDisposed_ && !this.tutorialPlayer.isFullscreen()))) {
      if (this.tutorialStreaming) {
        this.hideLandscapeErrorScreen();
        this.rendererService.renderer.addClass(this.windowRefService.document.body, 'snb-video-container');
      } else {
        this.renderLandscapeErrorScreen(true);
      }
    }
    if (this.resizeTimeout) {
      this.windowRefService.nativeWindow.clearTimeout(this.resizeTimeout);
    }
    this.checkOrientationMode();
    this.resizeTimeout = this.windowRefService.nativeWindow.setTimeout(this.setPlayerSize, this.resizeTimeFrame);
  }

  protected checkOrientationMode(isPlaying: boolean = false) {
    if (!this.isLandscapeMode()) {
      // Stream Ended via FS click and on orientation change
      // Exiting the screen and window to show event is Over message
      this.errorShown && this.exitFullScreen();
      if (this.deviceService.isWrapper) {
        this.tutorialPlayer && !this.tutorialPlayer.isDisposed_ &&this.tutorialPlayer.exitFullWindow();
        this.desktopPlayer.exitFullWindow();
        const homeBody = this.windowRefService.document.querySelector('html, body');
        if (homeBody) {
        this.rendererService.renderer.removeStyle(homeBody, 'overflow');
        }
      }
      // user turning device to Portrait mode.
      // Landing user to EDP portrait page
      !this.errorShown && this.exitFullScreen();
      this.quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
      this.pubsub.publish(pubSubApi.STREAM_BET_VIDEO_MODE, false);
      this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'snb-video-container');
      this.renderLandscapeErrorScreen(this.isLandscapeMode());
    }
    const tutorialPlayerContainer: any = this.elementRef.nativeElement.querySelector('#tutorial');
    const videoPlayerContainer: any = this.elementRef.nativeElement.querySelector('#' + this.streamUniqueId);
    if (this.isLandscapeMode()) {
      if(isPlaying && this.deviceService.isWrapper) {
        this.hideLandscapeErrorScreen();
      }
      this.tutorialPlayer && !this.tutorialPlayer.isDisposed_ && this.isWrapper && this.tutorialPlayer.enterFullWindow();
      this.tutorialPlayer &&  !this.tutorialPlayer.isDisposed_ && !this.isWrapper && this.renderLandscapeErrorScreen(true);
      if(this.deviceService.isWrapper){
        this.openFullScreen();
        this.desktopPlayer.enterFullWindow();
        if (videoPlayerContainer || tutorialPlayerContainer) {
          this.handleDesktopPlayerVisibility();
        }
      } else {
        videoPlayerContainer && videoPlayerContainer.classList.add('landscape-padding-top-zero');
        tutorialPlayerContainer && tutorialPlayerContainer.classList.add('landscape-padding-top-zero');
      }
    } else {
        if(videoPlayerContainer && videoPlayerContainer.classList.contains('landscape-padding-top-zero')) {
          videoPlayerContainer.classList.remove('landscape-padding-top-zero');
        }
        if(tutorialPlayerContainer && tutorialPlayerContainer.classList.contains('landscape-padding-top-zero')) {
          tutorialPlayerContainer.classList.remove('landscape-padding-top-zero');
        }
        this.handleVideoPlayerPlaceholder(true);
      }
  }

  protected openFullScreen():void {
    const homeBody = this.windowRefService.document.querySelector('html, body');
    const overlayForScroll = this.windowRefService.document.getElementById('overlay-edp');
    const footerWrapperElement = this.windowRefService.document.getElementsByClassName('footer-wrapper')[0];
    const timeLineElement = this.windowRefService.document.querySelectorAll('timeline')[0];
    const networkindicatior = this.windowRefService.document.querySelectorAll(this.NETWORK_INDCIATIOR_CLASS)[0];
    const topBarElement = this.windowRefService.document.querySelectorAll('.top-bar')[0];
    const myBetsHeaderElement = this.windowRefService.document.getElementsByClassName(this.VANILLA_SLOT_HEADER_CLASS);
    const myBetsFooterElement = this.windowRefService.document.getElementsByClassName(this.VANILLA_SLOT_FOOTER_CLASS);
    const myBetsBannerElement = this.windowRefService.document.getElementsByClassName(this.VANILLA_SLOT_BANNER_CLASS);
    footerWrapperElement && this.rendererService.renderer.setStyle(footerWrapperElement, 'display', 'none');
    timeLineElement && this.rendererService.renderer.setStyle(timeLineElement, 'display', 'none');
    topBarElement && this.rendererService.renderer.setStyle(topBarElement, 'display', 'none');
    myBetsHeaderElement && this.rendererService.renderer.removeClass(myBetsHeaderElement[0], 'd-block');
    myBetsFooterElement && this.rendererService.renderer.removeClass(myBetsFooterElement[0], 'd-block');
    myBetsBannerElement && this.rendererService.renderer.removeClass(myBetsBannerElement[0], 'd-block');
    myBetsHeaderElement && this.rendererService.renderer.addClass(myBetsHeaderElement[0], this.DISPLAY_NONE_CLASS);
    myBetsFooterElement && this.rendererService.renderer.addClass(myBetsFooterElement[0], this.DISPLAY_NONE_CLASS);
    myBetsBannerElement && this.rendererService.renderer.addClass(myBetsBannerElement[0], this.DISPLAY_NONE_CLASS);
    networkindicatior && this.rendererService.renderer.setStyle(networkindicatior, 'display', 'none');
    if(this.deviceService.isIos && overlayForScroll && homeBody && !this.isWrapper){
      this.rendererService.renderer.addClass(homeBody, 'tint-overlay-whole');
      this.rendererService.renderer.addClass(homeBody, 'stream-bet-overlay-black-edp');
      this.rendererService.renderer.addClass(overlayForScroll, 'stream-bet-overlay-black-edp');
    } 
    this.deviceService.isIos && this.removeOverlay();
  }

  protected setExitScreenFlags() {
    this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'snb-video-container');
    this.isFullScreen = this.desktopPlayer && this.desktopPlayer.isFullscreen();
    this.pubsub.publish(pubSubApi.STREAM_BET_VIDEO_MODE,false);
  }

  protected exitFullScreen(): void {
    const overlayForScroll = this.windowRefService.document.getElementById('overlay-edp');
    const homeBody = this.windowRefService.document.querySelector('html, body');
    const topBarElement = this.windowRefService.document.querySelectorAll('.top-bar')[0];
    const networkindicatior = this.windowRefService.document.querySelectorAll(this.NETWORK_INDCIATIOR_CLASS)[0];
    const footerWrapperElement = this.windowRefService.document.getElementsByClassName('footer-wrapper')[0];
    const timeLineElement = this.windowRefService.document.querySelectorAll('timeline')[0];
    const myBetsHeaderElement = this.windowRefService.document.getElementsByClassName(this.VANILLA_SLOT_HEADER_CLASS);
    const myBetsFooterElement = this.windowRefService.document.getElementsByClassName(this.VANILLA_SLOT_FOOTER_CLASS);
    const myBetsBannerElement = this.windowRefService.document.getElementsByClassName(this.VANILLA_SLOT_BANNER_CLASS);
    footerWrapperElement && this.rendererService.renderer.setStyle(footerWrapperElement, 'display', 'block');
    timeLineElement && this.rendererService.renderer.setStyle(timeLineElement, 'display', 'block');
    topBarElement && this.rendererService.renderer.removeStyle(topBarElement, 'display');
    myBetsHeaderElement && this.rendererService.renderer.removeClass(myBetsHeaderElement[0], this.DISPLAY_NONE_CLASS);
    myBetsFooterElement && this.rendererService.renderer.removeClass(myBetsFooterElement[0], this.DISPLAY_NONE_CLASS);
    myBetsBannerElement && this.rendererService.renderer.removeClass(myBetsBannerElement[0], this.DISPLAY_NONE_CLASS);
    myBetsFooterElement && this.rendererService.renderer.addClass(myBetsFooterElement[0], 'd-block');
    myBetsBannerElement && this.rendererService.renderer.addClass(myBetsBannerElement[0], 'd-block');
    networkindicatior && this.rendererService.renderer.setStyle(networkindicatior, 'display', 'block');
    if(this.deviceService.isIos && overlayForScroll && homeBody && !this.isWrapper){
      this.rendererService.renderer.removeClass(homeBody, 'tint-overlay-whole');
      this.rendererService.renderer.removeClass(homeBody, 'stream-bet-overlay-black-edp');
      this.rendererService.renderer.removeClass(overlayForScroll, 'stream-bet-overlay-black-edp');
    } 
    this.removeOverlay();
    this.handleVideoPlayerPlaceholder(true);
  }

  protected removeOverlay(): void {
    const overlayElem = this.windowRefService.document.querySelector('.overlay-wrapper');
    const overlayHeaderElem = this.windowRefService.document.querySelector('.overlay-header-container');
    const isVideoPlayer = this.elementRef.nativeElement.querySelector('#' + this.streamUniqueId);
    const html5VideoTag = this.elementRef.nativeElement.querySelectorAll('video');
    html5VideoTag?.forEach((videoElement: HTMLVideoElement) => {
      videoElement && this.rendererService.renderer.removeClass(videoElement, 'fit-screen');
    });
    if (isVideoPlayer && overlayElem && overlayHeaderElem) {
      const freebetdialog = document.querySelector('.modals');
      (isVideoPlayer as any).removeChild(overlayElem as any);
      (isVideoPlayer as any).removeChild(overlayHeaderElem as any);
      if (isVideoPlayer.contains(freebetdialog)) {
        (isVideoPlayer as any).removeChild(freebetdialog as any);
        this.eventVideoStreamProvider.snbVideoFullScreenExitSubj.next();
      }
      document.querySelector('oxygen-dialog')?.appendChild(freebetdialog);
    }
  }

  protected renderLandscapeErrorScreen(isLandscapeMode: boolean): void {
    if (isLandscapeMode) {
      this.rendererService.renderer
        .addClass(this.windowRefService.nativeWindow.document.querySelector('.landscape-mobile-overlay'), 'landscape-mode');
      this.rendererService.renderer
        .addClass(this.windowRefService.document.body, 'mobile-overlay-active');
      this.windowRefService.nativeWindow.document.activeElement.blur();
    }
  }

  protected hideLandscapeErrorScreen(): void {
    this.rendererService.renderer.removeClass(this.windowRefService.nativeWindow.document.querySelector('.landscape-mobile-overlay'), 'landscape-mode');
    this.rendererService.renderer.removeClass(this.windowRefService.document.body, 'mobile-overlay-active');
  }

  protected isLandscapeMode(): boolean {
    return (this.windowRefService.nativeWindow.orientation === 90 || this.windowRefService.nativeWindow.orientation === -90);
  }
 
}
