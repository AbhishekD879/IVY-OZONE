import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

import { UrlService, ProductService } from '@frontend/vanilla/core';

/**
 * Overrides the vanilla BrowserUrlInterceptor which sets the `x-bwin-browser-url` header on all outgoing requests.
 * This interceptor sets the header only on the requests going to the Openbet servers
 *
 * @export
 * @class BrowserUrlInterceptor
 * @implements {HttpInterceptor}
 */
@Injectable({
  providedIn: 'root'
})
export class BrowserUrlInterceptor implements HttpInterceptor {
    constructor(private urlService: UrlService,
                private productService: ProductService) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const requestUrl = this.urlService.parse(req.url);
        const portalProductMetadata = this.productService.getMetadata('portal');
        const portalHostname = portalProductMetadata && this.urlService.parse(portalProductMetadata.apiBaseUrl).hostname;
        if (requestUrl.isSameHost || requestUrl.hostname === portalHostname) {
            return next.handle(req);
        }

        req = req.clone({
            headers: req.headers.delete('X-Native-App').delete('x-bwin-browser-url').delete('x-xsrf-token').delete('X-From-Product').delete('X-App-Context')
        });

        return next.handle(req);
    }
}
