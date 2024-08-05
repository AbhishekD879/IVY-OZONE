import { filter, map, catchError } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse, HttpResponse,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { TempStorageService } from '@core/services/storage/temp-storage.service';
import { DeviceService } from '@core/services/device/device.service';
import { ICrashDetails } from './crash-details.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
@Injectable()
export class MaintenanceInterceptor implements HttpInterceptor {
  private subscriberName: string = this.awsService.getUniqueSubscriberName();
  constructor(
    private device: DeviceService,
    private tempStorage: TempStorageService,
    private route: ActivatedRoute,
    private router: Router,
    private awsService: AWSFirehoseService
  ) { }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    const requestStartTime: number = Date.now();
    return next.handle(req).pipe(
      filter((event: HttpEvent<any>) => event instanceof HttpResponse),
      map((event: HttpEvent<any>) => {
        this.awsService.trackOxygenRequest(req, event, this.getResponseTime(requestStartTime),this.subscriberName );
        return event;
      }),
      catchError((err: any) => {
        if (err instanceof HttpErrorResponse) {
          this.awsService.trackOxygenRequest(req, err, this.getResponseTime(requestStartTime), this.subscriberName);
          if ((err.url && err.url.indexOf(environment.SITESERVER_ENDPOINT) >= 0) &&
            err.url.indexOf('connect/banners') === -1) {
            const crashDetails = _.extend(this.getCrashDetails(), {
              url: err.url,
              status: err.status,
              statusText: err.statusText
            });
            this.tempStorage.set('crashDetails', crashDetails);

            if (err.url.indexOf(environment.CMS_ENDPOINT) !== -1 && navigator.onLine && err.status !== -1) {
              this.router.navigate(['/under-maintenance']);
            }

            return throwError(err);
          }
          return throwError(err);
        }
      }));
  }

  private getResponseTime(startTime: number): number {
    return Date.now() - startTime;
  }
  /**
   * Gets crash details object.
   * @return {Object} - crash details object.
   */
  private getCrashDetails(): ICrashDetails {
    const now = new Date();
    return {
      params: _.assign({}, this.route.params),
      segment: this.route.snapshot.url,
      date: now.toString(),
      timestamp: now.getTime(),
      url: 'Internet Connection Lost',
      method: null,
      status: null,
      statusText: 'Internet connnection lost',
      device: this.device,
      environment: environment.ENVIRONMENT
    };
  }
}
