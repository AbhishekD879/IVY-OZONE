import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';
import { Observable } from 'rxjs';

import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class LocaleInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {

    if (req.url.indexOf(environment.SITESERVER_ENDPOINT) !== -1 || req.url.indexOf(environment.SITESERVER_COMMENTARY_ENDPOINT) !== -1) {
      const secureReq = req.clone({
        url: req.url.indexOf('?') !== -1 ? `${req.url}&translationLang=en&responseFormat=json` :
          `${req.url}?translationLang=en&responseFormat=json`
      });
      return next.handle(secureReq);
    }
    return next.handle(req);
  }
}
