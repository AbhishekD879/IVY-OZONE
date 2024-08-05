import { Injectable } from '@angular/core';
import { EMPTY, Observable } from 'rxjs';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { DeviceService } from '@core/services/device/device.service';
import { UserService } from '@core/services/user/user.service';
import { conviva } from '@lazy-modules/eventVideoStream/constants/conviva';
import environment from '@environment/oxygenEnvConfig';
import { mergeMap, map, catchError } from 'rxjs/operators';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IConstant } from '@core/services/models/constant.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IAnalyticsInstance, IConviva, IAnalytics, IPlayer, IVideoAnalytics, IVideoJsPlayer } from './conviva.models';

@Injectable({
  providedIn: 'root'
})
export class ConvivaService {

  protected config: IConstant;
  protected testMode: boolean;
  protected initialized: boolean = false;
  protected renderer;
  protected instances: { [key: string]: IAnalyticsInstance } = {};

  constructor(
    protected asyncScriptLoader: AsyncScriptLoaderService,
    protected deviceService: DeviceService,
    protected userService: UserService,
    protected windowRef: WindowRefService,
    rendererService: RendererService
  ) {
    this.renderer = rendererService.renderer;
    this.setConfig();
  }

  /**
   * set service config
   * @param config
   */
  setConfig(config?: IConstant): void {
    this.testMode = config && (typeof config.testMode !== 'undefined') ? config.testMode : !environment.production;
    this.config = this.testMode ? conviva.test : conviva.prod;
    if (config) {
      Object.assign(this.config, config);
    }
  }

  /**
   * Load conviva library scripts on demand, before video player play event
   */
  preload(): void {
    this.initAnalytics().subscribe();
  }

  /**
   * Init analytics for html5 <video> element
   * @param videoElement
   * @param eventEntity
   */
  initVideoAnalytics(videoElement: HTMLVideoElement, eventEntity: ISportEvent): void {
    const id = eventEntity.id;
    const state = this.getState(id);
    state.player = videoElement;
    state.eventEntity = eventEntity;

    state.subscription = this.initAnalytics().subscribe(() => {
      this.getVideoAnalytics(state);
      state.listeners.push(this.renderer.listen(state.player, 'play', () => {
        this.startReporting(state);
      }));
      state.listeners.push(this.renderer.listen(state.player, 'ended', () => {
        this.stopReporting(state);
      }));
    });
  }

  /**
   * Init analytics for videojs player
   * @param videoJsPlayer
   * @param eventEntity
   */
  initVideoJsAnalytics(videoJsPlayer: IVideoJsPlayer, eventEntity: ISportEvent): void {
    const id = eventEntity.id;
    const state = this.getState(id);
    state.player = videoJsPlayer;
    state.eventEntity = eventEntity;

    state.subscription = this.initAnalytics().subscribe(() => {
      const events = this.getVideoJsEvents(videoJsPlayer, state);
      Object.keys(events).forEach(event => {
        videoJsPlayer.on(event, events[event]);
        state.listeners.push((() => { videoJsPlayer.off(event, events[event]); }));
      });
    });
  }

  /**
   * Set device metadata
   * @param metaData
   */
  setDeviceMetadata(metaData: IConstant): void {
    this.Analytics.setDeviceMetadata(metaData);
  }

  /**
   * release and cleanup analytics.
   * should be invoked in component onDestroy
   * @param id
   */
  release(id: string|number): void {
    const state = this.getState(id);
    this.stopReporting(state);
    state.listeners.forEach(fn => fn());
    state.videoAnalytics && state.videoAnalytics.release();
    state.subscription && state.subscription.unsubscribe();
    delete this.instances[id];
  }

  private get Conviva(): IConviva {
    return this.windowRef.nativeWindow.Conviva;
  }
private set Conviva(value:IConviva){}
  private get Analytics(): IAnalytics {
    try {
      return this.Conviva.Analytics;
    } catch(e) {
      console.warn('Conviva library not loaded', e);
      return null;
    }
  }
 private set Analytics(value:IAnalytics){}
  /**
   * Get video analytics configuration for specific player
   * @param id
   * @return IAnalyticsInstance
   */
  private getState(id: string|number): IAnalyticsInstance {
    this.instances[id] = this.instances[id] || {
      id: id as string,
      listeners: [],
      requested: false
    };
    return this.instances[id];
  }

  /**
   * get videoAnalytics instance
   * @param state
   * @return IVideoAnalytics
   */
  private getVideoAnalytics(state: IAnalyticsInstance): IVideoAnalytics {
    if (!state.videoAnalytics) {
      state.videoAnalytics = this.Analytics.buildVideoAnalytics();
      if (state.player) {
        state.videoAnalytics.setPlayer(state.player);
      }
    }
    return state.videoAnalytics;
  }

  /**
   * get metadata of the video
   * @param state
   * @return IConstant
   */
  private getContentInfo(state: IAnalyticsInstance): IConstant {
    return {
      [this.Conviva.Constants.STREAM_URL]: this.getStreamUrl(state.player),
      [this.Conviva.Constants.ASSET_NAME]: this.getAssetName(state.eventEntity),
      [this.Conviva.Constants.PLAYER_NAME]: this.playerName,
      [this.Conviva.Constants.IS_LIVE]: this.Conviva.Constants.StreamType.LIVE,
      [this.Conviva.Constants.VIEWER_ID]: this.userService.username,
      isLive: 'true',
      App_Type_Version: environment.version,
      Connection_Type: this.connectionType,
      Channel_Type: this.channelType,
      Sport_Type: state.eventEntity.categoryName,
      League_Type: state.eventEntity.typeName,
      Event_Streamed: state.eventEntity.originalName,
      Brand: this.brand,
      Page_URL: this.windowRef.nativeWindow.location.href,
      Stream_Provider: this.getStreamProvider(state.eventEntity)
    };
  }

  /**
   * Get asset name stream provider id
   * @param eventEntity
   * @return string;
   */
  private getAssetName(eventEntity: ISportEvent): string {
    return `[${eventEntity.id}] ${eventEntity.originalName}`;
  }

  /**
   * Get event stream provider id
   * @param eventEntity
   * @return string;
   */
  private getStreamProvider(eventEntity: ISportEvent): string {
    const providers = eventEntity.streamProviders || {};
    return Object.keys(providers).find(id => providers[id]) || 'UNKNOWN';
  }

  /**
   * Get channel type
   * @return string;
   */
  private get channelType(): string {
    return this.deviceService.isDesktop ? 'Desktop' : 'Mobile';
  }
private set channelType(value:string){}
  /**
   * Get device platform
   * @return string;
   */
  private get platform(): string {
    const device = this.deviceService;
    switch (true) {
      case (device.isDesktop): return 'Desktop';
      case (device.isAndroid): return 'Android';
      case (device.isIos): return 'iOS';
      default: return 'Mobile';
    }
  }
private set platform(value:string){}
  /**
   * Get connection type
   * @return string;
   */
  private get connectionType(): string {
    const connection = this.windowRef.nativeWindow.navigator.connection;
    return connection && connection.effectiveType || 'UNKNOWN';
  }
private set connectionType(value:string){}
  /**
   * Get current video url
   * @param player
   * @return string;
   */
  private getStreamUrl(player: IPlayer): string {
    return typeof player.currentSrc === 'function' ? player.currentSrc() : player.currentSrc;
  }

  /**
   * Get brand
   * @return string;
   */
  private get brand(): string {
    return environment.brand === 'bma' ? 'Coral' : 'Ladbrokes';
  }
private set brand(value:string){}
  /**
   * Get player name for contentInfo object
   * @return string
   */
  private get playerName(): string {
    return `${this.brand} ${this.platform}`;
  }
private set playerName(value:string){}
  /**
   * loads Conviva scripts
   * @return Observable<string>
   */
  private load(): Observable<string> {
    return this.asyncScriptLoader.loadJsFile(conviva.SDK).pipe(
      mergeMap(() => this.asyncScriptLoader.loadJsFile(this.deviceService.isDesktop ? conviva.VIDEOJS : conviva.HTML5))
    );
  }

  /**
   * Load and initialize analytics
   * @return Observable<boolean>
   */
  private initAnalytics(): Observable<boolean> {
    return this.load().pipe(
      map(() => {
        if (!this.initialized) {
          let settings;
          if (this.testMode) {
            settings = {
              [this.Conviva.Constants.GATEWAY_URL]: this.config.gatewayUrl,
              [this.Conviva.Constants.LOG_LEVEL]: this.Conviva.Constants.LogLevel.DEBUG
            };
          }
          this.Analytics.init(this.config.customerKey, null, settings);
          this.initialized = true;
        }
        return true;
      }),
      catchError((error: Error) => {
        console.warn(error.message);
        return EMPTY;
      })
    );
  }

  /**
   * Get array of videojs event callbacks
   * @param player
   * @param state
   * @return IConstant
   */
  private getVideoJsEvents(player: IVideoJsPlayer, state: IAnalyticsInstance): { [key: string]: Function } {
    return {
      'playing': () => {
        this.startReporting(state);
      },
      'play': () => {
        this.startReporting(state);
      },
      'ended': () => {
        this.stopReporting(state);
      }
    };
  }

  /**
   * start playback reporting
   * @param state
   */
  private startReporting(state: IAnalyticsInstance): void {
    if (!state.requested) {
      this.getVideoAnalytics(state).reportPlaybackRequested(this.getContentInfo(state));
      state.requested = true;
    }
  }

  /**
   * stop playback reporting
   * @param state
   */
  private stopReporting(state: IAnalyticsInstance): void {
    if (state.videoAnalytics) {
      state.videoAnalytics.reportPlaybackEnded();
    }
  }
}
