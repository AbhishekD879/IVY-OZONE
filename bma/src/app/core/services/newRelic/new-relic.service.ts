import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '../windowRef/window-ref.service';
import { IAnalyticsParams } from './analytics-params.model';
import { actions } from './new-relic.constant';
import environment from '@environment/oxygenEnvConfig';
import { HttpEvent, HttpRequest, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DeviceService } from '@core/services/device/device.service';

@Injectable()
export class NewRelicService {

  readonly API = actions;
  readonly APP_VERSION: string = environment.version || 'not-defined';

  private isInterceptAjax: boolean;

  constructor(
    private windowRef: WindowRefService,
    private userService: UserService,
    private cmsService: CmsService,
    private deviceService: DeviceService
  ) {
    this.cmsService.getSystemConfig().subscribe((config) => {
      this.isInterceptAjax = config.newRelic && config.newRelic.interceptAjax;
    });
  }

  /**
   * Safely dispatch New Relic addPageAction event.
   * @param {String} actionName
   * @param {Object} analyticsParams
   */
  addPageAction(actionName: string, analyticsParams: IAnalyticsParams = {}): void {
    if (actionName.toLowerCase().includes('ui_message') || actionName.toLowerCase().includes('betslip')) {
      analyticsParams.device = this.deviceService.parsedUA;
    }

    const params = _.extend({}, analyticsParams, {
      bppToken: this.userService.bppToken && this.userService.bppToken.substr(0, 7),
      token: this.userService.sessionToken && this.userService.sessionToken.substr(0, 7),
      username: this.userService.username,
      isWrapper: this.deviceService.isWrapper,
      appVersion: this.APP_VERSION
    });

    if (this.windowRef.nativeWindow.newrelic) {
      this.windowRef.nativeWindow.newrelic.addPageAction(actionName, params);
    }

    if (this.windowRef.nativeWindow.newRelicEvents) {
      // Save action to new relic events list.
      this.windowRef.nativeWindow.newRelicEvents[actionName] = this.windowRef.nativeWindow.newRelicEvents[actionName] ?
        [...this.windowRef.nativeWindow.newRelicEvents[actionName], params] : [params];
    }
  }

  trackOxygenRequest(req: HttpRequest<any>, res: HttpEvent<any> | HttpErrorResponse, responseTime: number): void {
    if (this.isInterceptAjax) {
      const payload: any = res instanceof HttpErrorResponse ? res.error : (<HttpResponse<any>>res).body;
      let payloadLength;

      // getting circular object parse errors when stringifying payload with HttpErrorResponse.
      try {
        payloadLength = JSON.stringify(payload).length;
      } catch (e) {
        // payload empty or circular HttpErrorResponse
      }

      this.addPageAction('Ajax Call', {
        url: req.url,
        level: res instanceof HttpErrorResponse ? 'error' : 'success',
        time: responseTime,
        requestMethod: req.method,
        cookiesLength: this.windowRef.nativeWindow.document.cookie.length,
        status: (<HttpResponse<any>>res).status || 200,
        payloadSize: payload && payloadLength ? payloadLength : 0
      });
    }
  }

  /**
   * noticeError
   * @param {Error} error
   */
  noticeError(error: Error): void {
    if (this.windowRef.nativeWindow.newrelic) {
      this.windowRef.nativeWindow.newrelic.noticeError(error);
    }
  }

  /**
   * Dispatch New Relic addPageAction event only if RouletteJourney
   * @param actionName
   * @param analyticsParams
   */
  addRouletteJourneySpecificPageAction(actionName: string, analyticsParams?: IAnalyticsParams): void {
    if (this.userService.isRouletteJourney()) {
      this.addPageAction(actionName, analyticsParams);
    }
  }
}
