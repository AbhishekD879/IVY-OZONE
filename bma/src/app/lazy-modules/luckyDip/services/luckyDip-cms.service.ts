import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { ILuckyDip } from '@lazy-modules/luckyDip/models/luckyDip';
import { IQuickbetReceiptDetailsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class LuckyDipCMSService {
  CMS_ENDPOINT: string;
  brand: string = environment.brand;
  public isLuckyDipReceipt: BehaviorSubject<IQuickbetReceiptDetailsModel> = new BehaviorSubject({} as IQuickbetReceiptDetailsModel);

  constructor(
    protected http: HttpClient
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
   * call to get LuckyDip Page data
   * @returns {Observable<[ILuckyDip]>}
   */
  public getLuckyDipCMSData(): Observable<ILuckyDip> {
    return this.getData(LUCKY_DIP_CONSTANTS.LUCKY_DIP)
      .pipe(
        map((luckyDip: HttpResponse<any>) => {
          return luckyDip.body[0];
        }
        ));
  }

    /**
   * call to get LuckyDipAnimation config data
   * @returns {Observable<[ILuckyDip]>}
   */
    public getLuckyDipCMSAnimationData(animationData): Observable<string> {
      return this.http.get(animationData, {responseType: 'text'});
      
    }
}