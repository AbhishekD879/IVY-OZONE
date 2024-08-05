import {Injectable, Injector} from '@angular/core';
import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse
} from '@angular/common/http';

import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/finally';
import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/take';
import {Router} from '@angular/router';
import { ErrorService } from '../../error.service';
import * as _ from 'lodash';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import {ApiClientService} from '../index';
import {AuthTokens} from '../../../models/authTokens.model';

@Injectable()
export class AllHttpInterceptor implements HttpInterceptor {
  constructor(
    private router: Router,
    private errorService: ErrorService,
    private injector: Injector
  ) {}

  tokenSubject: BehaviorSubject<string> = new BehaviorSubject<string>(null);

  /**
   * Clone request with updated Authorization token.
   * @param {HttpRequest<any>} req
   * @param {string} token
   * @return {HttpRequest<any>}
   */
  addToken(req: HttpRequest<any>, token: string): HttpRequest<any> {
    return req.clone({ setHeaders: { Authorization: token }});
  }

  private generateMultipleErrorsMessage(response): string {
    let message = '';

    if (!response.error.errors) {
      return '';
    }

    response.error.errors.forEach(function (error) {
      message += `${error.field || ''} ${error.defaultMessage}. \n`;
    });
    return message;
  }

  private showError(response: HttpErrorResponse): void {
    let message = '';

    if (typeof response.error === 'object') {
      message = _.isArray(response.error.errors) ? this.generateMultipleErrorsMessage(response) :  response.error.message;
     
      const teamMisMatchErr: string = 'teamMisMatch';
      const gamificationNotExistErr: string = 'gamificationNotExist';

      if (message?.includes(teamMisMatchErr)) {
        const err = message.substring(teamMisMatchErr.length + 1, message.length);
        message = `Team name mismatch ${err}`
      }
      else if (message?.includes(gamificationNotExistErr)) {
        const err = message.substring(gamificationNotExistErr.length + 1, message.length);
        message = `${err}`
      }
    } else {
      message = response.error || response.message;
    }

    this.errorService.emitError(message);
  }

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
  return next.handle(req)
    .catch((response: any) => {
      // handle 200 responce empty data. it causes error in angular.
      if (response.status >= 200 && response.status < 300) {
        const res = new HttpResponse({
          body: null,
          headers: response.headers,
          status: response.status,
          statusText: response.statusText,
          url: response.url
        });

        return Observable.of(res);
      }

      switch (response.status) {
        case 401: {
          // unauthorize response, try to refresh session.
          if (req.url.indexOf('/v1/api/token') !== -1) {
            this.redirectToLoginPage();
            return;
          }
          return this.refreshLoginSession(req, next, response);
        }
        case 404: {
          this.redirectToMainPage();
          break;
        }
        default: {
          this.showError(response);
        }
      }

      return Observable.throw(response);
    });
  }

  redirectToLoginPage(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.setItem('redirectedFrom', window.location.pathname);
    this.router.navigate(['/login']);
  }

  redirectToMainPage(): void {
    this.router.navigate(['/']);
  }

  /**
   * Refresh current login session
   * @param {HttpRequest<any>} req
   * @param {HttpHandler} next
   * @param response
   * @return {any}
   */
  refreshLoginSession(req: HttpRequest<any>, next: HttpHandler, response): Observable<HttpEvent<any>> {
    if (req.url.indexOf('/v1/api/token') === -1) {

      // Reset here so that the following requests wait until the token
      // comes back from the refreshToken call.
      this.tokenSubject.next(null);

      // use dynamic injection sue to circular dependency error on app init.
      const apiClientService: ApiClientService = this.injector.get(ApiClientService);

      return apiClientService.authorisation().refreshToken()
        .map((data: HttpResponse<AuthTokens>) => {
          return data.body;
        })
        .switchMap((newTokens: AuthTokens) => {
          if (newTokens) {
            localStorage.setItem('token', newTokens.token);
            localStorage.setItem('refreshToken', newTokens.refreshToken);

            this.tokenSubject.next(newTokens.token);
            return next.handle(this.addToken(req, newTokens.token));
          }
          // If we don't get a new token, we are in trouble so logout.
          this.redirectToLoginPage();
        })
        .catch(error => {
          // If there is an exception calling 'refreshToken', logout.
          this.redirectToLoginPage();
          return Observable.throw(response);
        });
    } else {
      return this.tokenSubject
        .filter(token => token != null)
        .take(1)
        .switchMap(token => {
          return next.handle(this.addToken(req, token));
        }).catch(() => {
          this.redirectToLoginPage();
          return Observable.throw(response);
        });
    }
  }
}
