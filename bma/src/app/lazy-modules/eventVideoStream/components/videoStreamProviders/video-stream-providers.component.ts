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
  ComponentFactoryResolver
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
import { IBetHistorySwitcherConfig } from '@app/betHistory/models/bet-history-switcher-config.model';
import { ActivatedRoute } from '@angular/router';
import { IStreamReplayUrls } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';

import {
  VideoStreamErrorDialogComponent
} from '@eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';

@Component({
  selector: 'video-stream-providers',
  templateUrl: './video-stream-providers.component.html',
  styleUrls: ['./video-stream-providers.component.scss']
})
export class VideoStreamProvidersComponent implements OnInit, OnDestroy {

  @Input() eventEntity: ISportEvent;
  @Input() autoPlay: boolean;
  @Input() colorSchema: string;
  @Input() providerInfo?: IStreamProvidersResponse;
  @Input() streamCache?: Map<string | number, IStreamProvidersResponse>;
  @Input() performConfig: IPerformGroupConfig;
  @Input() streamUniqueId: string;
  @Input() isMyBets: boolean;
  @Input() videoStreamData: IStreamReplayUrls;
  @Input() isReplayVideo: boolean;
  @Input() showCSBIframeReplay?: boolean;
  @Input() tabName?:string;
  @Input() eventName?: string;

  @Output() readonly playStreamError = new EventEmitter();
  @Output() readonly liveStreamStarted = new EventEmitter();

  streamingUrl: SafeUrl;
  frameWidth: number;
  frameHeight: number;
  showVideoPlayer: boolean = false;
  isWrapper: boolean;
  showPlayer: boolean = false;
  desktopPlayer;
  errorMessage: string = '';
  isDesktop: boolean;
  isInactiveUserError: boolean = false;
  isConvivaEnabled: boolean = false;
  isVideoBlock: boolean = true;
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
    fairUseBreach: false,
    eventCompleted: false
  };

  private actionSubscriber: Subscription;
  private streamFlowSubscriber: Subscription;
  private trackErrors: string[] = [];
  private resizeTimeFrame: number;
  private canWatchEvent: boolean = false;
  private resizeTimeout: number;
  private streamID: string = null;
  private streamActive: boolean = false;
  private html5VideoTag: HTMLMediaElement;

  private videJsTimeout: number;
  private streamingConfig: IImgConfigModel | IAtrRequestParamsModel;
  private resizeListerner: Function;

  fullRaceType: IBetHistorySwitcherConfig;
  closingStageType: IBetHistorySwitcherConfig;
  racingVideoTypes: IBetHistorySwitcherConfig[];
  filter: string = 'fullrace';
  showSwitcher: boolean;
  isMobile: boolean;
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
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private activatedRoute: ActivatedRoute,
  ) {
    this.isDesktop = this.deviceService.isDesktop;
    this.isMobile = this.deviceService.isMobile;
    this.handlePlayingStream = this.handlePlayingStream.bind(this);
    this.resizeView = this.resizeView.bind(this);
    this.setPlayerSize = this.setPlayerSize.bind(this);
    this.playStream = this.playStream.bind(this);
    this.ReplayStream = this.ReplayStream.bind(this);
  }

  ngOnInit(): void {
    const streamCache = this.streamCache && this.streamCache.get(this.eventEntity.id);
    this.showSwitcher=(this.isReplayVideo && this.videoStreamData && this.videoStreamData.closingStage)? true:false;
    if (!this.isReplayVideo && streamCache && streamCache.meta) {
      this.streamingConfig = streamCache.meta as (IImgConfigModel | IAtrRequestParamsModel);
    } else {
      console.warn('Please define on cms');
    }

    this.resizeTimeFrame = this.deviceService.isIos ? 500 : 2000;

    this.windowRefService.nativeWindow.setTimeout(() => {
      this.html5VideoTag = this.elementRef.nativeElement.querySelector('video');
      if (this.html5VideoTag) {
        // Event lister on event end.
        this.rendererService.renderer.listen(this.html5VideoTag, 'ended', () => {
          const msg=this.isReplayVideo?'eventCompleted':'eventFinished';
          console.warn('Event stream is over');
          this.showError(msg);
        });
        this.rendererService.renderer.listen(this.html5VideoTag, 'canplay', () => {
          this.isVideoBlock = false;
        });
        if (this.isConvivaEnabled && !this.isDesktop) {
          this.convivaService.initVideoAnalytics(this.html5VideoTag as HTMLVideoElement, this.eventEntity);
        }
        if (this.isDesktop) {
          this.disableContextMenu();
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

    if (this.deviceService.performProviderIsMobile()) {
      this.resizeListerner = this.rendererService.renderer.listen(this.windowRefService.nativeWindow,
        'orientationchange', this.resizeView);
    }

    if (this.isDesktop || this.replayStreamAvailablemobile()) {
      this.autoPlayStream();
    } else {
      this.handlePlayingStream();
    }
  }

  ngOnDestroy(): void {
    if (this.desktopPlayer  && !this.desktopPlayer.isDisposed_) {
      this.desktopPlayer.dispose();
    }

    this.actionSubscriber && this.actionSubscriber.unsubscribe();
    this.streamFlowSubscriber && this.streamFlowSubscriber.unsubscribe();
    this.windowRefService.nativeWindow.clearTimeout(this.videJsTimeout);
    this.commandService.unregister(this.commandService.API.GET_LIVE_STREAM_STATUS);
    if (this.resizeListerner) {
      this.resizeListerner();
    }
    this.isConvivaEnabled && this.convivaService.release(this.eventEntity.id);
    if (this.isDesktop && this.html5VideoTag) {
      this.html5VideoTag.removeEventListener('contextmenu', this.contextMenuListener);
    }
  }
  private isATRStream(replayFlag: boolean): boolean {
    return replayFlag === true ? this.providerInfo && this.providerInfo.priorityProviderName === 'At The Races'
      || this.eventEntity.streamProviders.ATR : this.videoStreamData.provider === 'ATR';

  }
  videoStream(streamOptions, flag) {
    this.windowRefService.nativeWindow.clearTimeout(this.videJsTimeout);
    const isVideoPlayer = this.elementRef.nativeElement.querySelector('#' + this.streamUniqueId);
    // Init desktop player using videojs
    this.isMobile && isVideoPlayer && isVideoPlayer.classList.remove("hidden");
    this.desktopPlayer =((this.isDesktop) || (this.replayStreamAvailablemobile())) && isVideoPlayer ? this.windowRefService.nativeWindow.videojs(this.streamUniqueId, streamOptions) : null;
    if (this.desktopPlayer) {
      const max_retryLimit: number = 10;
      let count: number = 0;
      this.desktopPlayer.on('error', () => {
        this.handlePlayerError();
      });
      this.desktopPlayer.on('ended', () => {
        this.desktopPlayer.dispose()
        const msg=this.isReplayVideo?'eventCompleted':'eventFinished';
        this.showError(msg);
      });
      const isATRStream = this.isATRStream(flag);      
      isATRStream && this.desktopPlayer.tech().on('retryplaylist', () => {
        count = count + 1;
        if (count === max_retryLimit) {
          this.desktopPlayer.dispose();
        }
      });
      this.desktopPlayer.on('ready', () => {
        this.streamTrackingService.setTrackingForPlayer(this.desktopPlayer, this.eventEntity);
      });
      this.isConvivaEnabled && this.convivaService.initVideoJsAnalytics(this.desktopPlayer, this.eventEntity);
      this.hideAllErrorMessage();
    }
  }
  ReplayStream($event?): void {
    if ($event) {
      $event.preventDefault();
    }
    this.createFilters();
    this.showPlayer = true;
    this.streamActive = true;
    const streamOptions = {
      muted: true, // major browsers do not support autoplay with sound.
      techOrder: ['html5', 'flash'],
      fluid: true,
      html5: {
        hls: {
          enableLowInitialPlaylist: true,
          smoothQualityChange: true,
          overrideNative: true,
        },
      },
      //playbackRates: [0.25, 0.5, 1, 1.5, 2],
      controlBar: {
        fullscreenToggle: false,
        pictureInPictureToggle: !this.isDesktop,
        remainingTimeDisplay: false,
        liveDisplay: false,
        progressControl: {
          seekBar: false
        },
     
      }
    }   
    this.videoStream(streamOptions, false);
    if (this.videoStreamData.status === 'ERROR') {
      if (this.desktopPlayer) {
        const errorString = this.videoStreamData.message;
        this.errorMessage = errorString;
        this.desktopPlayer.reset();
        // when error changed, error modal window should be reopened,
        // "open" function gather new errors when opened_ state is False.
        this.desktopPlayer.errorDisplay.opened_ = false;
        this.desktopPlayer.error(errorString);
        return ;
      }
    }
    const url = this.videoStreamData.streamInfo.streamUrl;
      this.desktopPlayer.src({
        type: this.getVideoType(url),
        src: url
      });
      this.desktopPlayer.ready(() => {
        this.showVideoPlayer = true;
        this.desktopPlayer.playsinline(true);

        this.desktopPlayer.play();
      });
      this.isMobile && this.setPlayerSize();

  }
  
  playStream($event?): void {
    if ($event) {
      $event.preventDefault();
    }
    
    const streamOptions={
      muted: true, // major browsers do not support autoplay with sound.
      techOrder: ['html5', 'flash'],
      fluid: true,
      controlBar: {
        fullscreenToggle: false,
        pictureInPictureToggle: !this.isDesktop
      }
    }
    
    this.videoStream(streamOptions,true);
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
    ).subscribe((stream: string) => {
        if (!stream) {
          this.onError();
          return;
        }

        this.onSuccess(stream);
        this.useCachedData();
        this.eventVideoStreamProvider.playSuccessErrorListener.next(true);
      }, (reason) => {
        this.onError(reason);
        this.eventVideoStreamProvider.playSuccessErrorListener.next(false);
      });
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

    if (this.isDesktop && this.desktopPlayer) {
      const errorString = this.localeService.getString(`sb.${errorMsgType}`);

      this.desktopPlayer.reset();
      // when error changed, error modal window should be reopened,
      // "open" function gather new errors when opened_ state is False.
      this.desktopPlayer.errorDisplay.opened_ = false;
      this.desktopPlayer.error(errorString);
    }

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

    if (!this.isDesktop) {
      this.dialogService.openDialog(DialogService.API.videoStreamError,
        this.componentFactoryResolver.resolveComponentFactory(VideoStreamErrorDialogComponent), true, {
          errorMsg: this.localeService.getString(`sb.${error}`),
          eventEntity: this.eventEntity,
          isInactivePopup: this.watchRulesService.isInactiveUser(error),
          isReplay: this.isReplayVideo
        });
    }
  }

  private contextMenuListener(e: PointerEvent): void {
    e.preventDefault();
  }

  /**
   * Disable context menu on videoJS <video> tag
   */
  private disableContextMenu(): void {
    this.html5VideoTag.addEventListener('contextmenu', this.contextMenuListener, false);
  }

  /**
   * Show or hide video stream logic
   */
  private handlePlayingStream(): void {
    this.showPlayer = this.deviceService.isWrapper ? this.nativeBridgeService.playerStatus : this.showPlayer;
    if (!this.showPlayer) {
      this.isReplayVideo?this.ReplayStream():this.playStream();
    } else {
      this.hideStream();
    }
  }

  private hideStream(): void {
    this.streamActive = false;
    this.streamID = null;
    this.showPlayer = false;

    if ((this.isDesktop || this.replayStreamAvailablemobile()) && this.desktopPlayer) {
      this.desktopPlayer.reset();
    } else if (!this.deviceService.isWrapper) {
      this.html5VideoTag.pause();
    }

    this.nativeBridgeService.hideVideoStream();
    this.hideAllErrorMessage();
    this.eventVideoStreamProvider.playSuccessErrorListener.next(false);
  }

  private onError(reason?: string): void {
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

  private onSuccess(stream: string): void {
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

  private useCachedData(): void {
    const eventId = this.eventEntity.id;
    if (this.streamCache.get(eventId).error) {
      this.showError(this.streamCache.get(eventId).error);
    } else if (this.streamCache.get(eventId).stream) {
      this.renderStream(this.streamCache.get(eventId).stream, eventId, this.eventEntity.categoryCode);
    }
  }

  private renderStream(url: string, eventId: number, categoryCode: string): void {
    if (this.isDesktop) {
      return this.runVideoJsPlayer(url);
    }

    if (!this.isMyBets && this.isWrapper && this.nativeBridgeService.supportsVideo() && url.indexOf('http') === 0) {
      const isDuplication = this.streamTrackingService.checkIdForDuplicates(this.eventEntity.id, 'liveStream');
      // Accept HTTP Live Stream only
      const providers = this.eventEntity.streamProviders || {};
      const providerName = Object.keys(providers).find(el => providers[el]) || 'UNKNOWN';
      this.nativeBridgeService.showVideoIfExist(url, eventId, categoryCode, providerName);
      if (!isDuplication) {
        this.pushToDataLayer();
        this.streamTrackingService.addIdToTrackedList(this.eventEntity.id, 'liveStream');
      }
    } else {
      const playerElement = this.windowRefService.document.getElementById(`${this.eventEntity.id}`);
      this.renderHtml5Stream(url);
      this.streamTrackingService.setTrackingForPlayer((playerElement as HTMLElement & { id_: string }), this.eventEntity);
    }
  }

  private renderHtml5Stream(url: string): void {
    if (this.deviceService.performProviderIsMobile()) {
       this.setPlayerSize();
      // Render video in html5
      this.streamingUrl = url;
    } else {
      this.showError('onlyForMobile');
    }
  }

  private setPlayerSize(): void {
    // It is based on initial value taken from perform group
    const heightCoeficient = 1.78;
    const elWidth: number = this.performGroupService.getElementWidth(this.elementRef);

    // Initial size of container
    const width = elWidth
      ? elWidth
      : this.frameWidth;

    this.frameWidth = width;
    this.frameHeight = Math.floor(width / heightCoeficient);
  }

  private runVideoJsPlayer(url: string): void {
    const eventId = this.eventEntity.id;

    if (this.desktopPlayer) {
      const isATRStream = this.providerInfo && this.providerInfo.priorityProviderName === 'At The Races'
        || this.eventEntity.streamProviders.ATR;
      this.streamCache.get(eventId).error = null;
      this.desktopPlayer.src({
        type: this.getVideoType(url),
        src: url,
        withCredentials: !isATRStream
      });
      this.desktopPlayer.ready(() => {
        this.showVideoPlayer = true;
        this.desktopPlayer.play();
      });
    }
  }

  private getVideoType(url: string): string {
    const result = url.match(/^(\w+):/),
      type = result ? result[1] : null,
      formats = {
        rtmp: 'rtmp',
        rtmpe: 'rtmpe'
      };

    return formats[type] || 'application/x-mpegURL';
  }

  private pushToDataLayer(): void {
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

  private showHideStream(providerInfo: IStreamProvidersResponse): Observable<string> {
    const eventId = this.eventEntity.id;

    this.showPlayer = true;
    if ((this.streamCache.get(eventId) && this.streamCache.get(eventId).error) || !this.performConfig) {
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
      return this.racingStreamService.getVideoUrl(providerInfo, this.performConfig);
    } else if (isATRStream) {
      // Init ATR stream with proper params.
      this.atTheRacesService.setConfigParams(
        (<IAtrRequestParamsModel>this.streamingConfig).partnerCode,
        (<IAtrRequestParamsModel>this.streamingConfig).secret
      );

      return this.atTheRacesService.getVideoUrl(providerInfo);
    } else if (isRUKorRPGTVstream) {
      return this.racingStreamService.getVideoUrl(providerInfo, this.performConfig);
    }

    return throwError('servicesCrashed');
  }

  private getStreamId(providerInfo: IStreamProvidersResponse): void {
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

  private checkCanWatch(): Observable<boolean> {
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

  private getStreamNotStartedMessage(): Observable<string> {
    return _.some([
      this.eventEntity.streamProviders.Perform && !this.performGroupService.isEventStarted(this.eventEntity),
      this.eventEntity.streamProviders.IMG && !this.imgService.isEventStarted(this.eventEntity),
      (this.eventEntity.streamProviders.RacingUK || this.eventEntity.streamProviders.RPGTV) &&
      !this.racingStreamService.isEventStarted(this.eventEntity),
      this.eventEntity.streamProviders.ATR && !this.atTheRacesService.isEventStarted(this.eventEntity)
    ]) ? throwError('eventNotStarted') : observableOf('');
  }

  private getStreamUnavailableMessage(): string {
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

  private hideAllErrorMessage(): void {
    _.each(this.ERROR_MESSAGES, (value, id) => {
      this.ERROR_MESSAGES[id] = false;
    });
    this.isInactiveUserError = false;
    this.errorMessage = this.parseErrorMessage();
  }

  private autoPlayStream(): void {
    // Loading videojs and videojs-contrib-hls
    // Loading in such way (using index), because videojs-contrib-hls is depend on videojs
    // files loading inconsistently, so error could appear
    if (this.isDesktop || this.replayStreamAvailablemobile()) {
      this.showVideoPlayer = false;
      this.loadVideoJsService.loadScripts().subscribe(() => {
        if (this.autoPlay) {
          this.windowRefService.nativeWindow.clearTimeout(this.videJsTimeout);
          this.videJsTimeout = this.windowRefService.nativeWindow.setTimeout(this.isReplayVideo?this.ReplayStream:this.playStream);
        }
      });
    }
  }

  private showError(errorType: string): void {
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
    if (this.nativeBridgeService.supportsVideo() && !this.isInactiveUserError && !this.isReplayVideo) {
      this.nativeBridgeService.showErrorForNative(reason);
    } else {
      // If there is reason show proper message for anothers show service crash error
      this.showErrorMessage(reason);
    }
  }

  private handlePlayerError(): void {
    const isRacing: boolean = this.liveStreamService.checkIfRacingEvent(this.eventEntity);
    const eventKey: string = _.findKey(this.ERROR_MESSAGES, (value) => value) || 'servicesCrashed';
    // First condition are for racing events.
    if (!(isRacing && this.isDesktop) && _.indexOf(this.trackErrors, eventKey) === -1) {
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

  private resizeView(): void {
    if (this.resizeTimeout) {
      this.windowRefService.nativeWindow.clearTimeout(this.resizeTimeout);
    }
    this.resizeTimeout = this.windowRefService.nativeWindow.setTimeout(this.setPlayerSize, this.resizeTimeFrame);
  }
  /**
  * Create filters, set initial filter.
  * Refs is a name of response data field for summary section related to specific filter/tab/switcher
  * @return {void}
  */
  protected createFilters(): void {
    this.fullRaceType = {
      viewByFilters: 'fullrace',
      name: this.localeService.getString('racing.fullRace'),
      refs: 'fullRace',
      onClick: filter => this.changeFilter(filter)
    };

    this.closingStageType = {
      viewByFilters: 'closingstage',
      name: this.localeService.getString('racing.closingStage'),
      refs: 'closingStage',
      onClick: filter => this.changeFilter(filter)
    };
    this.racingVideoTypes = [this.fullRaceType, this.closingStageType];
    this.filter = this.activatedRoute.snapshot.params['filter'] || this.racingVideoTypes[0].viewByFilters;
  }
  /**
   * set GA tracking object
   * @param gtmEventLabel string value
   */
  setGtmData(gaEventDetails: string): void {
    const eventDetails = gaEventDetails=='closingstage'?'closing replay':'full race replay';
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'horse racing',
      'component.LabelEvent': this.isMyBets?'my bets':'event details page',
      'component.ActionEvent': 'click',
      'component.PositionEvent': this.isMyBets?this.tabName:'not applicable',
      'component.LocationEvent': this.isMyBets ? this.eventName : this.eventEntity.name,
      'component.EventDetails': 'watch replay -'+eventDetails,
      'component.URLclicked': 'not applicable',
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
  /**
   * Tab click handler
   * @param {string} filter The switcher/tab selected viewByFilters value
   * @returns {void}
   */
  protected changeFilter(filter: string): void {
    this.filter = filter;
    this.setGtmData(filter);
    const currentTime = this.filter == 'closingstage' ? this.videoStreamData.startTime : 0;
    this.skipForwardVideo(currentTime);
  }
  /**
   * Foraward vdeo
   * @param {number} filter skip video to specified time
   * @returns {void}
   */
  public skipForwardVideo(currentTime:number): void {
    if (this.desktopPlayer) {
      this.desktopPlayer.currentTime(currentTime);
    }
    if(this.html5VideoTag){
      this.html5VideoTag.currentTime = currentTime;
      this.html5VideoTag.play();
    }   
  }
  /**
   * check replay stream avalable for mobile
   * @returns boolean
   */
  public replayStreamAvailablemobile(): boolean {
    return this.isReplayVideo && this.isMobile;
  }
  /**
   * css class for replayvideos
   * @returns boolean
   */
  public getVideoClass(): boolean {
    return this.isReplayVideo ? !(this.streamingUrl && this.showPlayer) : !(this.streamingUrl && this.showPlayer && !this.isWrapper);
  }

}