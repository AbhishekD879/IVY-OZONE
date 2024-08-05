import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { HttpEvent, HttpRequest, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { DeviceService } from '@core/services/device/device.service';
import environment from '@environment/oxygenEnvConfig';
import { IAnalyticsParams, IRecordData } from '@lazy-modules/awsFirehose/model/analytics-params.model';
import { ACTIONS, AWSCONSTANTS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@core/services/cms/cms.service';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';

@Injectable({
  providedIn: 'root'
})

export class AWSFirehoseService {
  recordData: IRecordData;
  readonly API = ACTIONS;
  readonly APP_VERSION: string = environment.version;
  private isInterceptAjax: boolean;
  private deliveryEnv: string;
  constructor(
    private windowRef: WindowRefService,
    private userService: UserService,
    private cmsService: CmsService,
    private deviceService: DeviceService,
    private pubsubService: PubSubService,
    private router: RoutingState
  ) {
    this.cmsService.getSystemConfig().subscribe((config) => {
      this.isInterceptAjax = config.awsLog && config.awsLog.interceptAjax;
    });
  }
  /**
   * call Add Action to push the record to firehose..
   * @params {actionName} string
   * @params {analyticsParams} Object of IAnalyticsParams type
   * @returns void
   * JSON.stringify is being used as firehose expects data in that particular format
   */
  performAddAction(actionName: string, analyticsParams?: IAnalyticsParams): void {
    if(analyticsParams){
      this.checkActionName(actionName, analyticsParams);
      const params = {
        ...analyticsParams,
        bppToken: this.userService.bppToken && this.userService.bppToken.substr(0, 7),
        token: this.userService.sessionToken && this.userService.sessionToken.substr(0, 7),
        username: this.userService.username,
        isWrapper: this.deviceService.isWrapper,
        appVersion: this.APP_VERSION,
        actionName: actionName,
        currentUrl: this.router.getCurrentUrl(),
        referralUrl: this.router.getPreviousUrl(),
        product: this.windowRef.nativeWindow.location.host,
        logTime: new Date().getTime(),
        userAgent: this.windowRef.nativeWindow.navigator.userAgent
      };
      this.recordData = { Data: JSON.stringify(params) };
      this.firehosePutRecord();
    }
  }
   /**
    * Pushes data to queue and calls performaddaction
    * @params {actionName} string
    * @params {analyticsParams} Object of IAnalyticsParams type
    * @returns void
    */
  addAction(actionName: string, analyticsParams?: IAnalyticsParams, subscriberName?: string): void {
    if (this.checkAWS()) {
      this.performAddAction(actionName, analyticsParams);
    } else {
      this.pubsubService.subscribe(
        subscriberName,
        this.pubsubService.API.INIT_AWS,
        () => this.performAddAction(actionName, analyticsParams)
      );
    }
  }
  /**
   * Push error log to firehose
   * @params {error} Error Type
   * @returns void
   */
  errorLog(error: Error): void {
    this.recordData = { Data: JSON.stringify(error) };
    this.firehosePutRecord();
  }
  /**
   * Tracks Interceptor requests
   * @params {req} HttpRequest Type
   * @params {res} HttpEvent Type
   * @params {responseTime} number
   * @returns void
   * The datatype is left as any as its being received from the interceptor in the same format
   */
  trackOxygenRequest(req: HttpRequest<any>, res: HttpEvent<any> | HttpErrorResponse, responseTime: number, subscriberName?: string): void {
    if (this.isInterceptAjax) {
      const payload: any = res instanceof HttpErrorResponse ? res.error : (<HttpResponse<any>>res).body;
      let payloadLength;
      // getting circular object parse errors when stringifying payload with HttpErrorResponse.
      try {
        payloadLength = JSON.stringify(payload).length;
      } catch (e) {
        // payload empty or circular HttpErrorResponse
      }
      this.addAction('Ajax Call', {
        url: req.url,
        level: res instanceof HttpErrorResponse ? 'error' : 'success',
        time: responseTime,
        requestMethod: req.method,
        cookiesLength: this.windowRef.nativeWindow.document.cookie.length,
        status: (<HttpResponse<any>>res).status || 200,
        payloadSize: payload && payloadLength ? payloadLength : 0,
      }, subscriberName
      );
    }
  }

  /**
   * Adding log for Roulette Journey
   * @params {actionName} string
   * @params {analyticsParams} Object of IAnalyticsParams type
   * @returns void
   */
  addRouletteJourneySpecificPageAction(actionName: string, analyticsParams?: IAnalyticsParams): void {
    if (this.userService.isRouletteJourney()) {
      this.addAction(actionName, analyticsParams);
    }
  }

  /**
   * Get the unique subscription for the aws fire hose connection
   * @returns { string }
   */
  getUniqueSubscriberName(): string {
    return `awsFirSubscr_${new Date().getTime()}`;
  }

  /**
   * Check whether action name present
   * @params {actionName} string
   * @params {analyticsParams} Object of IAnalyticsParams type
   * @returns void
   */
  public checkActionName(actionName: string, analyticsParams?: IAnalyticsParams): void {
    const message = 'ui_message';
    const betslip = 'betslip';
    if (analyticsParams && actionName && actionName.toLowerCase().includes(message) || actionName.toLowerCase().includes(betslip)) {
      analyticsParams.device = this.deviceService.parsedUA;
    }
  }
  /**
   * Pushes Data to AWS Firehose one record at a time
   * @returns void
   */
  private firehosePutRecord(): void {
    const firehose = new this.windowRef.nativeWindow.AWS.Firehose();
    this.deliveryEnv = this.getEnvironment(environment.ENVIRONMENT);
    if (!Object.keys(this.recordData).length) {
      return;
    } else {
      firehose.putRecord({
        Record: this.recordData,
        DeliveryStreamName: `${environment.brand}-${this.deliveryEnv}`
      }, () => {
      });
    }
    this.recordData = { Data: '' };
  }
  /**
   * Check if the Aws connection has been expired or not
   * @returns { boolean }
   */
  private checkAWS(): boolean {
    return this.windowRef.nativeWindow.AWS && this.windowRef.nativeWindow.AWS.config && this.windowRef.nativeWindow.AWS.config.credentials
      && !this.windowRef.nativeWindow.AWS.config.credentials.expired;
  }
  /**
   * Check the environment and return the value
   * @params {env} string
   * @returns { string }
   */
  private getEnvironment(env: string): string {
  return env === AWSCONSTANTS.ENV_PROD ? AWSCONSTANTS.ENV_PROD : AWSCONSTANTS.ENV_NONPROD;
  }
}
