import { Component, ElementRef, HostListener, Input, OnInit, ViewChild } from '@angular/core';
import * as _ from 'underscore';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import environment from '@environment/oxygenEnvConfig';
import IBGScoreboard from '../../models/bet-genius-scoreboard';
import IConfig from '../../models/config';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'bet-genius-scoreboard',
  // eslint-disable-next-line
  template: `<iframe #bgsIframe
  [id]="iframeId"
  [src]="scoreboardUrl"
  scrolling="no"
  frameborder="0"
  border="0"
  width="100%"
  (load)="handleScoreboardLoad()"
  height="282"></iframe>`
})
export class BetGeniusScoreboardComponent implements OnInit {

  @Input() config: IConfig;
  @ViewChild('bgsIframe', {static: true}) iframeElement: ElementRef<HTMLIFrameElement>;

  iframeApiLoaded: boolean = false;
  iframeId: string = 'betgenius-iframe';
  iframeVisible: boolean;
  IFRAME_URL: string;
  scoreboardUrl: SafeResourceUrl;

  private BET_GENIUS_SCOREBOARD: IBGScoreboard = environment.BET_GENIUS_SCOREBOARD;

  constructor(
    private domSanitizer: DomSanitizer,
    private asyncScriptLoaderFactory: AsyncScriptLoaderService,
    private windowRef: WindowRefService,
    private hostElement: ElementRef<HTMLIFrameElement>,
    private rendererService: RendererService,
    private pubSubService: PubSubService
  ) {}

  ngOnInit(): void {
    this.adjustScoreboardWidth = this.adjustScoreboardWidth.bind(this);
    this.hideScoreboard = this.hideScoreboard.bind(this);
    this.IFRAME_URL = `${this.BET_GENIUS_SCOREBOARD.scorecentre}?eventId=${this.config.eventId}`;
    this.scoreboardUrl = this.domSanitizer.bypassSecurityTrustResourceUrl(this.IFRAME_URL);
    this.loadScorecentreApi();
  }

  /**
   * Handles loading of scoreboard iframe.
   * @private
   */
  public handleScoreboardLoad(): void {
    if (_.isFunction(this.windowRef.nativeWindow.IFrameApi)) {
      // eslint-disable-next-line @typescript-eslint/no-unused-expressions
      new this.windowRef.nativeWindow.IFrameApi(this.iframeId);
    }
    this.pubSubService.publish(this.pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
  }

  /**
   * Adjusts scoreboard iframe width - sets iframe width to current .
   * @return {Node}
   * @public
   */
  @HostListener('window:resize')
  public adjustScoreboardWidth(): void {
    const scoreboardParentWidth = this.hostElement.nativeElement.offsetWidth;
    if (this.iframeElement) {
      this.rendererService.renderer.setStyle(this.iframeElement.nativeElement, 'width', `${scoreboardParentWidth}px`);
    }
  }

  /**
   * Hides BetGenius scoreboard if scorecentre API failed to load or for any reason.
   * @private
   */
  private hideScoreboard(): void {
    this.config.available = false;
  }

  /**
   * Loads BetGenius Scorecentre API.
   * @private
   */
  private loadScorecentreApi(): void {
    this.asyncScriptLoaderFactory.loadJsFile(this.BET_GENIUS_SCOREBOARD.api)
      .subscribe(() => {
        const scoreboardIframe = this.iframeElement;

        if (scoreboardIframe) {
          this.adjustScoreboardWidth();
          this.iframeVisible = true;
        } else {
          this.hideScoreboard();
        }
      });
  }
}
