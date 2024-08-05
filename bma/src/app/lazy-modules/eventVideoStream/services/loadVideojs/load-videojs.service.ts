import { forkJoin as observableForkJoin,  Observable } from 'rxjs';

import { mergeMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { videoJSUrls } from '@lazy-modules/eventVideoStream/constants/videoJS-urls';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@Injectable({ providedIn: 'root' })
export class LoadVideoJSService {

  constructor(
    private asyncScriptLoader: AsyncScriptLoaderService
  ) {}

  loadScripts(): Observable<string> {
    const subscriptions = [
      this.asyncScriptLoader.loadJsFile(videoJSUrls.js[0]), // ToDo: Rafactor to Observables
      this.asyncScriptLoader.loadCssFile(videoJSUrls.css)
    ];
    return observableForkJoin(subscriptions).pipe(
      mergeMap(() => this.asyncScriptLoader.loadJsFile(videoJSUrls.js[1]))
      /*
      Deleted 'assets/videojs/videojs-contrib-hls.min.js'
      from videoJS-urls.ts file, in js Array.
      As it's supported in video JS v7(previous version used v6)
      Refer: https://github.com/videojs/videojs-contrib-hls*/
      // mergeMap(() => this.asyncScriptLoader.loadJsFile(videoJSUrls.js[2]))
      );
  }
}
