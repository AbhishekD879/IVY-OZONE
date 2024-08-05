import { Injectable } from '@angular/core';
import { forkJoin as observableForkJoin, Observable, of as observableOf } from 'rxjs';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class OptaScoreboardLoaderService {
  constructor(
    private windowRef: WindowRefService,
    private asyncScriptLoaderService: AsyncScriptLoaderService
  ) {}

  /**
   * download bundle from CDN
   * @returns {() => Observable<string[]>}
   */
  public loadBundle(): Observable<string[]> {
    return this.loadPolyfills().pipe(switchMap(() => observableForkJoin([
      this.asyncScriptLoaderService.loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.bundle.js`),
      this.asyncScriptLoaderService.loadCssFile(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.bundle.css`, true)
    ])));
  }

  private loadPolyfills(): Observable<any[]> {

    // polyfills needed for opta-scoreboards
    const polyfills = [];

    if (!this.windowRef.nativeWindow.fetch) {
      polyfills.push(this.asyncScriptLoaderService
        .loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/polyfill-fetch.js`));
    }
    if (!this.windowRef.nativeWindow.EventSource) {
      polyfills.push(this.asyncScriptLoaderService
        .loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/polyfill-event-source.js`));
    }
    if (!this.windowRef.nativeWindow.customElements) {
      polyfills.push(this.asyncScriptLoaderService
        .loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/polyfill-webcomponents.js`));
    }
    // for forkJoin, observables array should have at least one element
    // in case no polyfills are needed
    polyfills.push(observableOf(true));

    return observableForkJoin(polyfills);
  }
}
