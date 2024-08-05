import { Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { fromEvent, of as observableOf, Observable, Subscription } from 'rxjs';
import { concatMap, debounceTime } from 'rxjs/operators';

import {
  IPerformGroupConfig,
  IStreamProvidersResponse
} from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PerformGroupService } from '@lazy-modules/eventVideoStream/services/performGroup/perform-group.service';
import { RacingStreamService } from '@lazy-modules/eventVideoStream/services/racingStream/racing-stream.service';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';

@Component({
  selector: 'csb-player',
  templateUrl: './csb-player.component.html',
  styleUrls: ['./csb-player.component.scss']
})
export class CSBPlayerComponent implements OnInit, OnDestroy {
  // It is based on initial value taken from perform group
  static readonly HEIGHT_COEFFICIENT: number = 1.37;
  static readonly MAX_FRAME_WIDTH: number = 600;

  @Input() eventEntity: ISportEvent;
  @Input() providerInfo: IStreamProvidersResponse;
  @Input() streamCache: Map<string | number, IStreamProvidersResponse>;
  @Input() performConfig: IPerformGroupConfig;

  @Output() readonly playStreamError = new EventEmitter<string>();
  @Output() readonly liveStreamStarted = new EventEmitter();

  streamingUrl: SafeUrl;
  streamingClearUrl: string;
  frameWidth: number;
  frameHeight: number;
  private resizeListener: Subscription;
  private watchPerformStreamSubscription: Subscription;

  constructor(public performGroupService: PerformGroupService,
              public deviceService: DeviceService,
              public racingStreamService: RacingStreamService,
              public elementRef: ElementRef<HTMLElement>,
              public eventVideoStreamProvider: EventVideoStreamProviderService,
              public windowRefService: WindowRefService,
              public watchRulesService: WatchRulesService,
              public sanitizer: DomSanitizer) {

  }

  ngOnInit(): void {
    const streamNotStartedMsg: string = this.performGroupService.isPerformStreamStarted(this.eventEntity)
      ? null
      : 'eventNotStarted';

    if (streamNotStartedMsg) {
      this.onError(streamNotStartedMsg);
      return;
    }

    this.watchPerformStreamSubscription = this.watchRulesService.canWatchEvent(this.providerInfo,
      this.eventEntity.categoryId,
      this.eventEntity.id).pipe(
      concatMap(() => this.showStream(this.providerInfo))
    ).subscribe((url: string) => {
      if (!url) {
        this.onError();
        return;
      }
      this.streamingClearUrl = url;
      this.streamCache.get(this.eventEntity.id).stream = url;
      this.setPlayerDimensions();
      this.eventVideoStreamProvider.playSuccessErrorListener.next(true);

      if (this.deviceService.isMobile) {
        return;
      }

      this.addWindowListener();
    }, (error: string) => this.onError(error));
  }

  onIframeLoad(){
    this.liveStreamStarted.emit();
  }
  showStream(providerInfo: IStreamProvidersResponse): Observable<string> {
    const eventId = this.eventEntity.id;
    if ((this.streamCache.get(eventId) && this.streamCache.get(eventId).error) || !this.performConfig) {
      return observableOf(null);
    }

    // Gets perform group id from coral ip
    return this.performGroupService.performGroupId(providerInfo, this.performConfig, this.eventEntity.id).pipe(
      concatMap(() => observableOf(this.racingStreamService.getVideoCSBUrl(providerInfo, this.performConfig)))
    );
  }

  onError(reason?: string): void {
    this.playStreamError.emit(reason);
  }

  ngOnDestroy(): void {
    this.resizeListener && this.resizeListener.unsubscribe();
    this.watchPerformStreamSubscription && this.watchPerformStreamSubscription.unsubscribe();
  }

  private addWindowListener(): void {
    this.resizeListener = fromEvent(this.windowRefService.nativeWindow as any, 'resize')
      .pipe(debounceTime(300))
      .subscribe(() => this.setPlayerDimensions());
  }

  private generateStreamingUrl(url: string = this.streamingClearUrl): void {
    const urlWithDimensions: string = url.concat(`&width=${this.frameWidth}&height=${this.frameHeight}`);
    this.streamingUrl = this.sanitizer.bypassSecurityTrustResourceUrl(urlWithDimensions);
  }

  private setPlayerDimensions(): void {
    const elWidth: number = this.performGroupService.getElementWidth(this.elementRef);
    const updatedFrameWidth: number = elWidth > CSBPlayerComponent.MAX_FRAME_WIDTH
      ? CSBPlayerComponent.MAX_FRAME_WIDTH
      : elWidth;

    if (updatedFrameWidth === this.frameWidth) {
      return;
    }

    // Initial size of iframe
    this.frameWidth = updatedFrameWidth;
    this.frameHeight = Math.round(this.frameWidth / CSBPlayerComponent.HEIGHT_COEFFICIENT);

    // update iframe's content dimensions by change props in url
    this.generateStreamingUrl();
  }
}
