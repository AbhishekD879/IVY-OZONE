import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { ICouponStatWidget } from '@root/app/on-boarding-overlay/onboarding-coupon-stat-widgets/onboarding-coupon-stat-widgets.model';


@Injectable()
/**
 * onboarding overlay service for creation removal, editing , uploading of fields
 */
export class couponStatWidgetService extends AbstractService<Configuration> {


  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

   /**
   * Get the onboarding coupon stat widget by brand
   * @returns {Observable<HttpResponse<ICouponStatWidget>>}
   */
    public getDetailsByBrand(apiUrl): Observable<HttpResponse<ICouponStatWidget>> {
        return this.sendRequest<ICouponStatWidget>('get', `${apiUrl}/brand/${this.brand}`, null);
      }


   /**
   * To Save onboarding coupon stat widget
   * @param {ICouponStatWidget} request
   * @returns {Observable<HttpResponse<ICouponStatWidget>>}
   */
    public saveOnBoardingCouponStat(request: ICouponStatWidget, apiUrl): Observable<HttpResponse<ICouponStatWidget>> {
        return this.sendRequest<ICouponStatWidget>('post', apiUrl, request);
      }

    public postNewCouponStatImage(id: string, file: FormData, url): Observable<HttpResponse<ICouponStatWidget>> {
        const apiUrl = `${url}/${id}/image`;

        return this.sendRequest<ICouponStatWidget>('post', apiUrl, file);

      }

    public removeCouponStatImage(id: string, url): Observable<HttpResponse<ICouponStatWidget>> {
        const apiUrl = `${url}/${id}/image`;
        return this.sendRequest<ICouponStatWidget>('delete', apiUrl, null);
      }

      /**
   * To Update onboarding coupon stat widget
   * @param {ICouponStatWidget} request
   * @returns {Observable<HttpResponse<ICouponStatWidget>>}
   */
    public updateOnBoardingCouponStat(request: ICouponStatWidget, url): Observable<HttpResponse<ICouponStatWidget>> {
    return this.sendRequest<ICouponStatWidget>('put', `${url}/${request.id}`, request);
  }


}