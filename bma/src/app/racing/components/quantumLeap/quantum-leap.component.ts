import { Component, Input, OnDestroy, OnInit, ViewEncapsulation, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import * as _ from 'underscore';
import { forkJoin, Subscription } from 'rxjs';

import { ISportEvent } from '@core/models/sport-event.model';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { ISpinner } from '@racing/components/quantumLeap/spinner.model';
import { StreamTrackingService } from '@sb/services/streamTracking/stream-tracking.service';

@Component({
  selector: 'quantum-leap',
  styleUrls: ['./quantum-leap.component.scss'],
  template: '<div class="quantum" [innerHtml]="html"></div>',
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class QuantumLeapComponent implements OnInit, OnDestroy {

  @Input() eventEntity: ISportEvent;
  @Input() spinner: ISpinner;

  html: SafeHtml;
  isUKorIRE: boolean;

  private jqueryUrl: string = 'assets/jquery.min.js';
  private quantumLeapBookmaker: string = environment.QUANTUMLEAP_BOOKMAKER;
  private quantumLeapScriptEndpoint: string = environment.QUANTUMLEAP_SCRIPT_ENDPOINT;
  private quantumLeapId: string = 'QL_goingDown';
  private quantumLeapElement: string;
  private isVideoTracked: boolean = false;
  private interval: number;
  private loadScriptSubscription: Subscription;

  constructor(
    private sanitizer: DomSanitizer,
    private windowRef: WindowRefService,
    private asyncScriptLoaderService: AsyncScriptLoaderService,
    private streamTrackingService: StreamTrackingService,
    private changeDetectorRef: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.isUKorIRE = this.eventEntity.isUKorIRE;
    // eslint-disable-next-line max-len
    this.quantumLeapElement = `<div id="${this.quantumLeapId}" bookmaker="${this.quantumLeapBookmaker}" bookmaker_id="${this.eventEntity.id}">`;
    this.html = this.sanitizer.bypassSecurityTrustHtml(this.quantumLeapElement);

    if (this.isUKorIRE) {
      this.spinner.isActive = true;
      this.changeDetectorRef.detectChanges();
      this.loadScriptSubscription = forkJoin(
        this.asyncScriptLoaderService.loadJsFile(this.jqueryUrl),
        this.asyncScriptLoaderService.loadJsFile(this.quantumLeapScriptEndpoint)
      ).subscribe(() => {
        this.spinner.isActive = false;
        this.initQuantumLeap();
      }, () => {
        this.spinner.isActive = false;
      });
    }
  }

  ngOnDestroy() {
    this.windowRef.nativeWindow.clearInterval(this.interval);
    this.loadScriptSubscription && this.loadScriptSubscription.unsubscribe();
    this.changeDetectorRef.detach();

    this.stopLiveSim();
  }

  initQuantumLeap(): void {
    if (this.windowRef.nativeWindow['_QLGoingDown']) {
      try {
        this.windowRef.nativeWindow._QLGoingDown.populateGoingDown();
        this.setObserverForJwPlayer();
      } catch (error) {
        console.warn(error);
      }
    }
  }

  setObserverForJwPlayer(): void {
    if (this.interval || this.isVideoTracked) {
      return;
    }

    this.interval = this.windowRef.nativeWindow.setInterval(() => {
      if (this.windowRef.nativeWindow['_QLGoingDown']
        && this.windowRef.nativeWindow['_QLGoingDown']['jwplayer']
        && this.windowRef.nativeWindow['_QLGoingDown']['jwplayer']['_events']) {
        const player = this.windowRef.nativeWindow['_QLGoingDown']['jwplayer'],
          playerId = `${player.id}_${this.eventEntity.id}`;

        _.extend(player, { id_: playerId });

        this.streamTrackingService.setTrackingForPlayer(player, this.eventEntity);

        this.windowRef.nativeWindow.clearInterval(this.interval);
        this.interval = null;
        this.isVideoTracked = true;
      }
    }, 50, false);
  }

  /**
   * Checks if _QLGoingDown API is present on window and stops LiveSim video via it's method.
   */
  private stopLiveSim(): void {
    if (this.isVideoTracked) {
      // @ts-ignore
      this.streamTrackingService.resetTimer({});
    }

    if (this.windowRef.nativeWindow['_QLGoingDown'] &&
      this.windowRef.nativeWindow['_QLGoingDown'].videoJSplayer &&
      typeof this.windowRef.nativeWindow['_QLGoingDown'].videoJSplayer.dispose === 'function') {
      try {
        this.windowRef.nativeWindow['_QLGoingDown'].videoJSplayer.dispose();
      } catch (error) {
        console.warn(error);
      }
    }
  }
}
