import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISplashPage } from '@lazy-modules/freeRide/models/free-ride';
import { FREE_RIDE_CONSTS } from '@lazy-modules/freeRide/constants/free-ride-constants';
import environment from '@environment/oxygenEnvConfig';

@Injectable({ providedIn: 'root' })
export class FreeRideCMSService {
  CMS_ENDPOINT: string;
  brand: string = environment.brand;

  constructor(
    protected pubsub: PubSubService,
    protected http: HttpClient,
  ) {
    this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
  }

  /**
   * makes get data to the provided url
   * @param {string} url
   * @param {any} params
   * @returns {Observable<HttpResponse<T>>}
   */
  protected getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
      observe: 'response',
      params: params
    });
  }

  /**
   * call to get splash page data
   * @returns {Observable<[ISplashPage]>}
   */
  public getFreeRideSplashPage(): Observable<ISplashPage> {
    return this.getData(FREE_RIDE_CONSTS.FREE_RIDE_SPLASH)
      .pipe(
        map((splashData: HttpResponse<any>) => {
          this.pubsub.publish(this.pubsub.API.FREE_RIDE_BET, true);
          return splashData.body[0];
      }
    ));
  }

}
