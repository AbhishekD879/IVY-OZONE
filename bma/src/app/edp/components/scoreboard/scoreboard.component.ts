import { map } from 'rxjs/operators';
import {
  Component,
  ElementRef,
  Input,
  OnInit,
  ChangeDetectorRef,
  OnDestroy,
  Output,
  EventEmitter
} from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { HttpClient, HttpResponse } from '@angular/common/http';

import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import * as _ from 'underscore';
import { Observable } from 'rxjs';

@Component({
  selector: 'scoreboard',
  templateUrl: 'scoreboard.component.html'
})
export class ScoreboardComponent implements OnInit, OnDestroy {

  @Input() eventId: string;
  @Input() scoreboardUrl: string;

  @Output() readonly isLoaded: EventEmitter<boolean> = new EventEmitter();

  public tplLoaded: boolean;
  public html: SafeHtml;
  private detectListener;

  private jqueryUrl = 'assets/jquery.min.js';
  private scoreBoardUrl: string;

  constructor(
    private pubSubService: PubSubService,
    private asyncScriptLoaderService: AsyncScriptLoaderService,
    private windowRefService: WindowRefService,
    private elementRef: ElementRef,
    private http: HttpClient,
    private changeDetectorRef: ChangeDetectorRef,
  ) {
    this.changeDetectorRef.detach();
    this.detectListener = this.windowRefService.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
    }, 500);
  }

  ngOnInit() {
    this.scoreBoardUrl = `${this.windowRefService.nativeWindow.location.protocol}//${this.scoreboardUrl}${this.eventId}/scoreboard`;
    if (!this.windowRefService.nativeWindow.$ && !_.isFunction(this.windowRefService.nativeWindow.$)) {
      this.asyncScriptLoaderService.loadJsFile(this.jqueryUrl)
        .subscribe(() => {
          this.loadScoreboard();
        });
    } else {
      this.loadScoreboard();
    }
  }

  ngOnDestroy() {
    this.windowRefService.nativeWindow.clearInterval(this.detectListener);
  }

  /**
   * load scoreboard when jQuery initialized
   */
  loadScoreboard(): void {
    this.getGPScoreboard()
      .subscribe(response => {
        this.elementRef.nativeElement.firstChild.innerHTML = response;
        this.onGPScoreboardLoad();
        this.pubSubService.publish(this.pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
      }, () => {
        this.tplLoaded = true;
        // it's needed for emitting after view rendered
        this.windowRefService.nativeWindow.setTimeout(() => this.isLoaded.emit(true), 500);
      });
  }

  /**
   * get scoreboard content
   */
  getGPScoreboard(): Observable<SafeHtml> {
    return this.http.get(`${this.scoreBoardUrl}`, {
      responseType: 'text',
      observe: 'response'
    }).pipe(map((data: HttpResponse<SafeHtml>) => data.body));
  }

  /**
   * On Load Function
   */
  onGPScoreboardLoad(): void {
    const scripts: HTMLScriptElement[] = this.elementRef.nativeElement.querySelectorAll('script');
    _.each(scripts, el => {
      eval.call(null, el.text);
    });
    this.tplLoaded = true;
    // Check if Scoreboard is loaded
    const isScoreboardLoaded = this.elementRef.nativeElement.firstChild.hasChildNodes();
    this.pubSubService.publish(this.pubSubService.API.SCOREBOARD_VISIBILITY, isScoreboardLoaded);
    // it's needed for emitting after view rendered
    this.windowRefService.nativeWindow.setTimeout(() => this.isLoaded.emit(true), 500);
  }
}
