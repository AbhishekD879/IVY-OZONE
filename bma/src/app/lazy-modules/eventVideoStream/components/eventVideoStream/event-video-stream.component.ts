import { of as observableOf, Observable, Subscription, from as fromPromise, throwError } from 'rxjs';

import { concatMap, catchError, map } from 'rxjs/operators';
import {
  Component,
  OnInit,
  Input,
  Output,
  OnDestroy,
  EventEmitter,
  SimpleChanges,
  OnChanges,
  ChangeDetectorRef,
  ComponentFactoryResolver
} from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { UserService } from '@core/services/user/user.service';
import { SessionService } from '@authModule/services/session/session.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IGameMediaService } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-game-media.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { DialogService } from '@core/services/dialogService/dialog.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IStreamsCssClasses } from '@core/models/streams-css-classes.model';
import { IStreamReplayUrls } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';
import {
  IPerformGroupConfig,
  IStreamDetail,
  IStreamProvidersResponse
} from '@lazy-modules/eventVideoStream/models/video-stream.model';

import {
  VideoStreamErrorDialogComponent
} from '@eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IStreamBetWeb } from '@core/services/cms/models/system-config';

@Component({
  selector: 'event-video-stream',
  templateUrl: './event-video-stream.component.html'
})
export class EventVideoStreamComponent implements OnInit, OnDestroy, OnChanges {

  @Input() eventEntity: ISportEvent;
  // autoPlay needed ONLY for DESKTOP
  @Input() autoPlay?: boolean;
  @Input() colorSchema?: string;
  @Input() preloadStream?: boolean;
  @Input() cssClassesForStreams?: IStreamsCssClasses;
  @Input() streamUniqueId?: string = 'rtmpe-hls';
  @Input() isLiveStreamRefreshed: boolean;
  @Input() isMyBets: boolean;
  @Input() isReplayVideo?:boolean;
  @Input() isUsedFromWidget?: boolean = false;
  @Output() readonly playerLoadedStatus = new EventEmitter();
  @Input() tabName?:string;
  @Input() eventName?: string;
  @Output() readonly playStreamError = new EventEmitter();
  @Output() readonly liveStreamStarted = new EventEmitter();

  showPlayer: boolean = false;
  providerInfo: IStreamProvidersResponse = {} as IStreamProvidersResponse;
  providerInfoAvailable: boolean = false;
  iGameMediaCssClasses: string;
  videoStreamProvidersCssClasses: string;
  ERROR_MESSAGES = {
    loginRequired: false,
    servicesCrashed: false,
    eventFinished: false,
    onlyLoginRequired: false,
    deniedByWatchRules: false,
    deniedByInactiveWatchRules: false,
    geoBlocked: false,
    usageLimitsBreached: false,
    serverError: false
  };
  streamCache: Map<string | number, IStreamProvidersResponse> = new Map();
  isDesktop: boolean;
  errorMessage: string = '';
  showCSBIframe: boolean;
  performConfig: IPerformGroupConfig;
  showCSBIframeReplay: boolean;
  showPlayerReplay: boolean;
  replayUrl: IStreamReplayUrls;

  private actionSubscriber: Subscription;
  private systemConfigSubscription: Subscription;
  private controllerName: string = 'EventVideoStreamComponent';
  private showStream: boolean = false;
  private getProviderInfoInProgress: boolean = false;
  sbSportIds: string[] = [];
  sbStreamProviders: string[] = [];
  sbWebEnabled: boolean = false;
  private isMobile: boolean;
  isOnInitDone = false;
  private streamBetCmsConfig: IStreamBetWeb;

  constructor(
    public userService: UserService,
    public nativeBridge: NativeBridgeService,
    public localeService: LocaleService,
    public gtmService: GtmService,
    public sessionService: SessionService,
    public deviceService: DeviceService,
    public liveStreamService: LiveStreamService,
    public iGMediaService: IGameMediaService,
    public eventVideoStreamProvider: EventVideoStreamProviderService,
    public pubsubService: PubSubService,
    public windowRefService: WindowRefService,
    protected watchRulesService: WatchRulesService,
    protected changeDetectorRef: ChangeDetectorRef,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private cms: CmsService,
  ) {
    this.isDesktop = this.deviceService.isDesktop;
    this.isMobile = this.deviceService.isMobile;
    this.handleUserAuth = this.handleUserAuth.bind(this);
    this.handleReloadStream = this.handleReloadStream.bind(this);
    this.toggleStream = this.toggleStream.bind(this);
    this.setStreamShowFlag = this.setStreamShowFlag.bind(this);
  }

  ngOnInit(): void {
    this.actionSubscriber = this.eventVideoStreamProvider.playListener.subscribe(this.toggleStream);

    // Hides login error message if user is not logged in
    // Also if user sign out hide video stream.
    this.pubsubService.subscribe(this.controllerName,
      [this.pubsubService.API.SUCCESSFUL_LOGIN, this.pubsubService.API.SESSION_LOGOUT], this.handleUserAuth);

    // add listener for native player only on wrapper
    if (this.deviceService.isWrapper) {
      this.windowRefService.document.addEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', this.setStreamShowFlag as any);
    }

    this.showPlayer = false;
    this.showPlayerReplay = false;
    this.parseCssClasses();

    // Desktop, racing, tote logic
    if (this.preloadStream) {
      this.toggleStream();
    }
 
    this.eventVideoStreamProvider.getStreamBetCmsConfig().subscribe((streamBetWeb:IStreamBetWeb) => {
      this.streamBetCmsConfig = streamBetWeb;
    });

    this.isOnInitDone = true;
  }

  isStreamBetAvailable(): boolean {   
    const streamBetConfig = {
      streamBetCmsConfig: this.streamBetCmsConfig,
      providerInfoAvailable: this.providerInfoAvailable,
      isMobile: this.isMobile,
      isTablet: this.deviceService.isTabletOrigin,
      isDesktop: this.deviceService.isDesktop, 
      providerInfo: this.providerInfo,
      isMyBets: this.isMyBets,
      categoryId: this.eventEntity.categoryId
    }
    return this.eventVideoStreamProvider.isStreamBetAvailable(streamBetConfig,this.controllerName);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.isOnInitDone && (changes.eventEntity || changes.isLiveStreamRefreshed)) {
      this.handleReloadStream();
    }
  }

  ngOnDestroy(): void {
    this.actionSubscriber && this.actionSubscriber.unsubscribe();
    this.systemConfigSubscription && this.systemConfigSubscription.unsubscribe();
    this.pubsubService.unsubscribe(this.controllerName);
    this.unsubscribeOfWrapperListeners();
    this.ERROR_MESSAGES.serverError && this.dialogService.closeDialog(DialogService.API.videoStreamError);
  }

  onLiveStreamStarted() {
    this.liveStreamStarted.emit();
  }
  playStream(): void {
    // Hides all error messages
    this.hideAllErrorMessage();

    // If CMS fails or error message code is available, display proper error message.
    const streamErrorMessage = this.getUserLoggedOutMessage();

    if (streamErrorMessage) {
      this.onError(streamErrorMessage);
      return;
    }

    this.getProviderInfoInProgress = true;

    // streamFlow;
    this.getProviderInfo().pipe(
      concatMap((providerInfo: IStreamProvidersResponse) => {
        return this.showHideStream(providerInfo);
      })
    ).subscribe((stream: IStreamProvidersResponse) => {
      if (!stream) {
        this.onError();
        return;
      }

      const storedStream = this.streamCache.get(this.eventEntity.id);

      if (storedStream && storedStream.meta) {
        this.performConfig = storedStream.meta as IPerformGroupConfig;
      } else {
        console.warn(`Please define on cms.`);
      }

      this.showCSBIframe = this.watchRulesService.shouldShowCSBIframe(this.eventEntity, this.performConfig);

      if (this.showCSBIframe) {
        this.unsubscribeOfWrapperListeners();
      }
      this.showPlayer = true;
    }, (reason: string) => {
      this.onError(reason);
    }).add(() => {
      this.getProviderInfoInProgress = false;
    });
  }

  onPlayLiveStreamError(reason): void {
    this.showStream = false;
    this.playStreamError.emit(reason);
    if (this.showCSBIframe) {
      this.onError(reason);
    }
  }

  showErrorMessage(errorMessageType: string): void {
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

    if (!this.isDesktop) {
      this.dialogService.openDialog(DialogService.API.videoStreamError,
        this.componentFactoryResolver.resolveComponentFactory(VideoStreamErrorDialogComponent), true, {
          errorMsg: this.localeService.getString(`sb.${error}`),
          eventEntity: this.eventEntity,
          isInactivePopup: this.watchRulesService.isInactiveUser(error)
        });
    }
  }
  /**
   * Replay related errors HR
   * @param error 
   */
  private displayErrorReplay(error: string): void {
    this.errorMessage = error;
    this.showPlayerReplay = false;
    if (!this.isDesktop) {
      this.dialogService.openDialog(DialogService.API.videoStreamError,
        this.componentFactoryResolver.resolveComponentFactory(VideoStreamErrorDialogComponent), true, {
        errorMsg: error,
        eventEntity: this.eventEntity,
        isInactivePopup: this.watchRulesService.isInactiveUser(error)
      });
    }
  }
  private hideAllErrorMessage(): void {
    Object.keys(this.ERROR_MESSAGES).forEach((key: string) => {
      this.ERROR_MESSAGES[key] = false;
    });

    this.errorMessage = this.parseErrorMessage();
  }

  private unsubscribeOfWrapperListeners(): void {
    if (this.deviceService.isWrapper) {
      this.windowRefService.document.removeEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', this.setStreamShowFlag as any);
    }
  }

  /**
   * Show video stream(check if user is logged in and online;
   * request to optIn MS to detect stream provider, render corresponding nested component)
   * Hide video stream(destroy nested component if it is iGameMedia or
   * trigger showHideStreamListener in the nested component if it is another provider)
   */
  private handlePlayingStream(): void {
    this.showPlayer = this.nativeBridge.playerStatus || this.showPlayer;
    if (this.showStream) {
      !this.isReplayVideo?this.playStream():this.playReplayStream();
    } else {
      this.hideStream();
    }
  }

  private hideStream(): void {
    if (!this.providerInfoAvailable && this.nativeBridge.playerStatus) {
      // ToDo: this is another evidence streams MUST be refactored
      this.nativeBridge.hideVideoStream();
    }
    this.providerInfoAvailable = false;
    this.showPlayer = false;
    // Trigger showHideStreamListener in the nested video-stream-providers component
    // as this component has own logic to hide/show player
    this.eventVideoStreamProvider.showHideStreamListener.next(false);
  }

  private onError(reason?: string): void {
    const customReason = typeof reason === 'string' ? reason : 'servicesCrashed';

    this.showError(customReason);

    if (customReason === 'eventFinished' || customReason === 'usageLimitsBreached') {
      const storedStream = this.streamCache.get(this.eventEntity.id);

      if (storedStream) {
        storedStream.error = customReason;
      }
    }

    this.playStreamError.emit(customReason);
  }

  private showHideStream(providerInfo: IStreamProvidersResponse): Observable<IStreamProvidersResponse> {
    if (this.streamCache.get(this.eventEntity.id).error) {
      return observableOf(null);
    }

    this.providerInfo = Object.assign(this.providerInfo, providerInfo);
    // Set correct PROVIDER to eventEntity regarding to response from optIn(providerInfo)
    this.liveStreamService.prioritizeStream(this.eventEntity, providerInfo);
    this.providerInfoAvailable = true;

    return observableOf(providerInfo);
  }

  private getProviderInfo(): Observable<string | IStreamProvidersResponse> {
    const eventId = this.eventEntity.id;

    if (!this.deviceService.isOnline()) {
      return throwError('serverError');
    } else if (this.streamCache.get(eventId) && this.streamCache.get(eventId).stream) {
      return observableOf(this.streamCache.get(eventId));
    }

    if (this.streamCache.get(eventId)) {
      this.streamCache.delete(eventId);
    }

    return fromPromise(this.sessionService.whenProxySession()).pipe(
      concatMap(() => {
        if (this.userService.status) {
          return observableOf(null);
        }

        return throwError('streamIsNotAvailable');
      }),
      concatMap(() => {
        return this.iGMediaService.getStreamsForEvent(this.eventEntity);
      }),
      map((providerInfo: IStreamProvidersResponse) => {
        this.streamCache.set(eventId, providerInfo);
        return providerInfo;
      }),
      catchError(() => {
        if (!this.deviceService.isOnline()) {
          return throwError('serverError');
        }

        return throwError('streamIsNotAvailable');
      })
    );
  }

  private getUserLoggedOutMessage(): string {
    return !this.userService.status ? 'onlyLoginRequired' : '';
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
    this.showStream = false;
    this.showPlayerReplay =false;
    this.gtmService.push('trackEvent', errorNotification);

    if (reason === 'eventFinished') {
      this.eventEntity.isFinished = true;
    }

    if (this.nativeBridge.supportsVideo() && !this.watchRulesService.isInactiveUser(reason)) {
      this.nativeBridge.showErrorForNative(reason);
    } else {
      // If there is reason show proper message for anothers show service crash error
      this.showErrorMessage(reason);
    }
  }

  /**
   * Parse ccs classes for iGameMedia and videoStreamProviders components if exists
   */
  private parseCssClasses(): void {
    this.iGameMediaCssClasses = this.cssClassesForStreams ? this.cssClassesForStreams.iGameMedia : '';
    this.videoStreamProvidersCssClasses = this.cssClassesForStreams ? this.cssClassesForStreams.otherProviders : '';
  }

  private handleUserAuth(): void {
    if (this.userService.status) {
      this.ERROR_MESSAGES.loginRequired = false;
      this.ERROR_MESSAGES.onlyLoginRequired = false;
      this.showStream = this.isDesktop;
    } else {
      this.showStream = false;
      this.showPlayer = false;
      this.showPlayerReplay = false;
    }

    this.errorMessage = this.parseErrorMessage();
    this.changeDetectorRef.detectChanges();
    if (!this.getProviderInfoInProgress) {
      this.handlePlayingStream();
    }
  }

  private handleReloadStream(): void {
    // Call optIn to detect new stream provider for new event and re-init target stream component
    this.showPlayer = false;
    this.showStream = true;
    this.changeDetectorRef.detectChanges();

    this.handlePlayingStream();
  }

  private toggleStream(): void {
    this.showStream = !this.showStream;
    this.handlePlayingStream();
  }

  /**
   * Reset flags when native wrapper's player in closing
   * @param data
   */
  private setStreamShowFlag(data: IStreamDetail): void {
    this.showStream = data.detail.settingValue;
    this.showPlayer = data.detail.settingValue;

    if (!data.detail.settingValue) {
      this.playStreamError.emit();  // we don't need to stop streaming if Native player is enabled
    }
  }
  /**
   * Replay stream playing for finshed events HR
   */
  playReplayStream(): void {
    // Hides all error messages
    this.hideAllErrorMessage();
    // If CMS fails or error message code is available, display proper error message.
    const streamErrorMessage = this.getUserLoggedOutMessage();
    if (streamErrorMessage) {
      this.onError(streamErrorMessage);
      return;
    }
    this.getHRReplayUrls();
  }
  /**
   * For getting streaming details for finshed events
   */
  public getHRReplayUrls(): void {
    const eventId = this.eventEntity.id;
    this.iGMediaService.getHRReplayStreamUrls(eventId).subscribe((replayUrlResp: IStreamReplayUrls) => {
      if (!replayUrlResp) {
        this.onError();
        return;
      }
      if (replayUrlResp.status === 'ERROR') {
        this.displayErrorReplay(replayUrlResp.message);
        return;
      }
      if (replayUrlResp.status === 'SUCCESS') {
        this.replayUrl = replayUrlResp;
        this.showCSBIframeReplay = false;
        this.showPlayerReplay = true;
        this.providerInfoAvailable = true;
      }
    });

  }
}
