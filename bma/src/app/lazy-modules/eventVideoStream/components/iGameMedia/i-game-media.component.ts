import { Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output, ComponentFactoryResolver } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { Subscription } from 'rxjs';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { DeviceService } from '@core/services/device/device.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { IStreamProvidersResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import {
  IIGameMediaDesktopPropsModel,
  IIGameMediaDimensionsModel,
  IIGameMediaStream
} from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';
import { IGameMediaService } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-game-media.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { DialogService } from '@core/services/dialogService/dialog.service';

import {
  VideoStreamErrorDialogComponent
} from '@eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';

@Component({
    selector: 'i-game-media',
    templateUrl: './i-game-media.component.html'
})
export class IGameMediaComponent implements OnInit, OnDestroy {

  @Input() eventEntity: ISportEvent;
  @Input() providerInfo?: IStreamProvidersResponse;
  @Input() isMyBets: boolean;
  @Output() readonly playStreamError: EventEmitter<string> = new EventEmitter();
  @Output() readonly liveStreamStarted = new EventEmitter();

  streamUrl: SafeResourceUrl ;
  streamUrlNotSafe: string = '';
  iFrameDimensions: IIGameMediaDimensionsModel;
  streamError: string;
  isDesktop: boolean;
  streamShown: boolean = false;
  public isStreamActive: boolean = false;
  public desktopProperties: IIGameMediaDesktopPropsModel;
  public dataLayerObjError: {
    event: string;
    eventCategory: string;
    eventAction: string;
    liveStreamError: string;
  };
  public streamData: IIGameMediaStream;

  private dataLayerObj: {
    eventCategory: string;
    eventAction: string;
    eventLabel: string;
    sportID: string;
    typeID: string;
    eventId: number;
  };
  private orientationChangeListener: Function;
  private actionSubscriber: Subscription;
  private readonly RESIZE_TIMEOUT: number = 250;

  constructor(
    public iGameMediaService: IGameMediaService,
    public sanitizer: DomSanitizer,
    public gtmService: GtmService,
    public windowRefService: WindowRefService,
    public localeService: LocaleService,
    public commandService: CommandService,
    public elementRef: ElementRef,
    public rendererService: RendererService,
    public deviceService: DeviceService,
    public nativeBridgeService: NativeBridgeService,
    public eventVideoStreamProvider: EventVideoStreamProviderService,
    public domToolsService: DomToolsService,
    public watchRulesService: WatchRulesService,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver
  ) {
    this.isDesktop = this.deviceService.isDesktop;

    this.handleLiveStreamStatus = this.handleLiveStreamStatus.bind(this);
    this.onResizeAndOrientation = this.onResizeAndOrientation.bind(this);
    this.handlePlayingStream = this.handlePlayingStream.bind(this);
  }

  ngOnInit(): void {
    this.desktopProperties = {
      isDesktop: this.isDesktop,
      videoDimensions: {
        width: '100%',
        height: '100%'
      }
    };
    this.dataLayerObj = {
      eventCategory: 'streaming',
      eventAction: 'click',
      eventLabel: 'watch video stream',
      sportID: this.eventEntity.categoryId,
      typeID: this.eventEntity.typeId,
      eventId: this.eventEntity.id
    };
    this.dataLayerObjError = {
      event: 'trackEvent',
      eventCategory: 'Livestream',
      eventAction: 'error',
      liveStreamError: ''
    };

    this.orientationChangeListener = this.rendererService.renderer.listen(this.windowRefService.nativeWindow,
      'orientationchange', this.onResizeAndOrientation);

    this.actionSubscriber = this.eventVideoStreamProvider.showHideStreamListener.subscribe(this.handlePlayingStream);
    this.handlePlayingStream(this.deviceService.isWrapper ? !this.nativeBridgeService.playerStatus : true);
  }

  ngOnDestroy(): void {
    if (!this.isDesktop && this.orientationChangeListener) {
      this.orientationChangeListener();
    }

    if (this.actionSubscriber) {
      this.actionSubscriber.unsubscribe();
    }

    this.commandService.unregister(this.commandService.API.GET_LIVE_STREAM_STATUS);
  }

  get streamErrorKey(): string {
    return `sb.${this.streamError}`;
  }
set streamErrorKey(value:string){}
  private showError(error: string): void {
    if (!this.isDesktop) {
      this.dialogService.openDialog(DialogService.API.videoStreamError,
        this.componentFactoryResolver.resolveComponentFactory(VideoStreamErrorDialogComponent), true, {
          errorMsg: this.localeService.getString(`sb.${error}`),
          eventEntity: this.eventEntity,
          isInactivePopup: this.watchRulesService.isInactiveUser(error)
        });
    }

    this.streamError = error;
  }

  private handlePlayingStream(streamShown: boolean): void {
    this.streamShown = streamShown;

    if (this.streamShown) {
      this.init();
    } else {
      this.nativeBridgeService.hideVideoStream();
    }
  }

  private init(): void {
    this.iGameMediaService
      .getStream(this.eventEntity, this.providerInfo)
      .subscribe((streamData: IIGameMediaStream) => {
        // register method to share stream status
        // streamID currently always will be null, we do not receive this data
        this.isStreamActive = true;
        this.commandService.register(this.commandService.API.GET_LIVE_STREAM_STATUS, this.handleLiveStreamStatus);
        this.addStreamDataToGTM();

        if (!this.isMyBets && this.deviceService.isWrapper && streamData) {
          // Pass data to Native app
          this.nativeBridgeService.showVideoIfExist(streamData.streamLink, this.eventEntity.id, this.eventEntity.categoryCode,
            'iGameMedia');
        } else {
          this.streamData = streamData;
          this.streamUrlNotSafe = this.iGameMediaService.replaceAmps(this.streamData.streamLink);
          this.streamUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.streamUrlNotSafe);

          this.iFrameDimensions = this.iGameMediaService.getIFrameDimensions(
            this.desktopProperties,
            this.offsetWidth, this.streamData
          );
        }

        this.eventVideoStreamProvider.playSuccessErrorListener.next(true);
        this.liveStreamStarted.emit();
      }, (err: string) => {
        err = err === 'IGM streamservice.js not available' ? 'streamIsNotAvailable' : err;
        this.dataLayerObjError.liveStreamError = this.localeService.getString(`sb.${this.streamError}`);
        this.addStreamDataToGTM();

        if (this.deviceService.isWrapper && !this.watchRulesService.isInactiveUser(err)) {
          this.nativeBridgeService.showErrorForNative(err);
        } else {
          this.showError(err);
        }

        this.playStreamError.emit(err);
        this.eventVideoStreamProvider.playSuccessErrorListener.next(false);
      });
  }

  private onResizeAndOrientation(): void {
    setTimeout(() => {
      this.iFrameDimensions = this.iGameMediaService.getIFrameDimensions(this.desktopProperties,
        this.offsetWidth, this.streamData);
    }, this.RESIZE_TIMEOUT);
  }

  private addStreamDataToGTM(): void {
    if (this.streamData) {
      this.onResizeAndOrientation();
    }
    this.gtmService.push('trackEvent', this.streamError ? this.dataLayerObjError : this.dataLayerObj);
  }

  private get offsetWidth(): number {
    const parentElement = this.elementRef.nativeElement.parentElement;
    const element = parentElement && parentElement.parentElement ?
      parentElement.parentElement.parentNode : this.elementRef.nativeElement.parentNode;
    return this.domToolsService.getWidth(<HTMLElement>element);
  }
  private set offsetWidth(value:number){}
  private handleLiveStreamStatus(): Promise<{ streamID: string; streamActive: boolean; }> {
    return Promise.resolve({
      streamID: null,
      streamActive: this.isStreamActive
    });
  }
}
