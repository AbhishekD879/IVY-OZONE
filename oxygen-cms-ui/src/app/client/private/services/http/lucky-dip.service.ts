import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { catchError, map } from 'rxjs/operators';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { LuckyDip } from '@app/lucky-dip/lucky-dip.model';
import { ILuckyDipMapping, LuckyDipV2 } from '@root/app/lucky-dip/lucky-dip-v2.model';
import { Order } from '@app/client/private/models/order.model';

@Injectable()
export class LuckyDipService extends AbstractService<LuckyDip[]> {
  luckyDip: string = `lucky-dip/brand/${this.brand}`;
  luckyDipCreateUri: string;
  luckyDipMappingUri: string;
  luckyDipMappingUpdateUri: string;

  constructor(
    http: HttpClient,
    domain: string,
    brand: string) {
    super(http, domain, brand);
    this.uri = `lucky-dip/brand/${brand}`;
    this.luckyDipCreateUri = `${brand}/lucky-dip`;
    this.luckyDipMappingUpdateUri = `${brand}/lucky-dip-mapping`;
    this.luckyDipMappingUri = `lucky-dip-mapping/brand/${brand}`;
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate) {
    return observableDate
      .map(res => {
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse && response.status !== 400) {
          console.warn(response.error);
        }
        return Observable.throw(response);
      }, catchError(response => {
        return Observable.throw(this.generateErrorMsg(response));
      }));
  }

  /**
 * Get lucky dip data.
 * @returns {Observable<HttpResponse<LuckyDip>>}
 */
  getLuckyDipData(): Observable<LuckyDip> {
    const data = this.sendRequest('get',  `luckydip/brand/${this.brand}`, null).pipe(
      map(((res: HttpResponse<LuckyDip>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
   * gets the LuckyDip data based on ID
   * @param id  { id }
   * @returns { HttpResponse<LuckyDipV2> }
   */
  public getLuckyDipV2Data(id: string): Observable<LuckyDipV2> {
    const data = this.sendRequest('get', `${this.brand}/lucky-dip/${id}`, null).pipe(
      map(((res: HttpResponse<LuckyDipV2>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
   * gets all the LuckyDip
   * @returns { HttpResponse<LuckyDipV2[]> }
   */
  public getAllLuckyDipData(): Observable<LuckyDipV2> {
    const data = this.sendRequest('get', `${this.uri}`, null).pipe(
      map(((res: HttpResponse<LuckyDip>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
 * gets the LuckyDipMapping data based on ID
 * @param id  { id }
 * @returns { HttpResponse<Fanzone> }
 */
  public getLuckyDipMappingData(id: string): Observable<ILuckyDipMapping> {
    const data = this.sendRequest('get', `${this.luckyDipMappingUpdateUri}/${id}`, null).pipe(
      map(((res: HttpResponse<ILuckyDipMapping>) => res.body)));
    return this.wrappedObservable(data);
  }


  /**
 * gets all the LuckyDipMapping
 * @returns { HttpResponse<ILuckyDipMapping[]> }
 */
  public getAllLuckyDipMappingData(): Observable<ILuckyDipMapping> {
    const data = this.sendRequest('get', `${this.luckyDipMappingUri}`, null).pipe(
      map(((res: HttpResponse<ILuckyDipMapping>) => res.body)));
    return this.wrappedObservable(data);
  }
  /**
    * Save/Update lucky dip data.
    * @returns {Observable<HttpResponse<LuckyDip>>}
    */
  luckyDipData(luckyDipData: LuckyDip, id: string): Observable<LuckyDip> {
    const data = id
      ? this.updateSplashData(luckyDipData, id)
      : this.postSplashData(luckyDipData);
    return this.wrappedObservable(data);
  }

  /**
   * Update lucky dip data.
   * @returns {Observable<HttpResponse<LuckyDip>>}
   */
  postSplashData(luckyDipData: LuckyDip): Observable<HttpResponse<LuckyDip>> {
    const data = this.sendRequest('post', 'luckydip', luckyDipData).pipe(
      map(((res: HttpResponse<LuckyDip>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
   * Create lucky dip data.
   * @returns {Observable<HttpResponse<LuckyDip>>}
   */
  updateSplashData(luckyDipData: LuckyDip, id: string): Observable<HttpResponse<LuckyDip>> {
    const url = `luckydip/${id}`;
    const data = this.sendRequest<LuckyDip>('put', url, luckyDipData).pipe(
      map(((res: HttpResponse<LuckyDip>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
   * saves luckyDipMapping information
   * @param method, popUp, id  { method, luckyDipMapping, id }
   * @returns { HttpResponse<ILuckyDipMapping> }
   */
  public saveluckyDipMapping(method: string, luckyDipMapping: ILuckyDipMapping, id: string): Observable<HttpResponse<ILuckyDipMapping>> {
    const url = id ? `${this.luckyDipMappingUpdateUri}/${id}` : `${this.luckyDipMappingUpdateUri}`;
    return this.sendRequest<ILuckyDipMapping>(method, url, luckyDipMapping).pipe(
      catchError(response => {
        return Observable.throw(this.generateErrorMsg(response));
      }));
  }

  /**
 * Create LuckyDip for the new entry
 * @param {LuckyDip} formData
 * @returns {Observable<HttpResponse<LuckyDip>>}
 */
  public createLuckyDip(luckyDipData: LuckyDip): Observable<HttpResponse<LuckyDip>> {
    return this.sendRequest<LuckyDip>("post", this.luckyDipCreateUri, luckyDipData);
  }

    /**
 * Create LuckyDipV2 for the new entry
 * @param {LuckyDip} formData
 * @returns {Observable<HttpResponse<LuckyDipV2>>}
 */
    public createLuckyDipV2(luckyDipData: LuckyDipV2): Observable<HttpResponse<LuckyDipV2>> {
      return this.sendRequest<LuckyDipV2>("post", this.luckyDipCreateUri, luckyDipData);
    }

  /**
   * deletes the LuckyDip based on ID's
   * @param id  { id }
   * @returns { void}
   */
  public deleteLuckyDip(id: string | string[]): Observable<void> {
    const data = this.sendRequest('delete', `${this.brand}/lucky-dip/${id}`, null).pipe(
      map(((res: HttpResponse<LuckyDip>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
   * to delete LuckyDipMapping
   * @param id  { id }
   * @returns { void }
   */
  public deleteLuckyDipMapping(id: string | string[]): Observable<void> {
    const data = this.sendRequest('delete', `${this.luckyDipMappingUpdateUri}/${id}`, null).pipe(
      map(((res: HttpResponse<LuckyDip>) => res.body)));
    return this.wrappedObservable(data);
  }

  /**
 * Save/Update lucky dip V2 data.
 * @returns {Observable<HttpResponse<LuckyDipV2>>}
 */
  luckyDipV2Data(luckyDipV2Data: LuckyDipV2, id: string): Observable<LuckyDipV2> {
    const data = id
      ? this.updateSplashV2Data(luckyDipV2Data, id)
      : this.postSplashV2Data(luckyDipV2Data);
    return this.wrappedObservable(data);
  }

  /**
   * Update lucky dip data.
   * @returns {Observable<HttpResponse<LuckyDipV2>>}
   */
  postSplashV2Data(luckyDipV2Data: LuckyDipV2): Observable<HttpResponse<LuckyDipV2>> {
    const data = this.sendRequest('post', this.luckyDipCreateUri, luckyDipV2Data).pipe(
      map(((res: HttpResponse<LuckyDipV2>) => res.body)),
      catchError(response => {
        return Observable.throw(this.generateErrorMsg(response));
      }));
    return this.wrappedObservable(data);
  }

  /**
   * Create lucky dip data.
   * @returns {Observable<HttpResponse<LuckyDipV2>>}
   */
  updateSplashV2Data(luckyDipV2Data: LuckyDipV2, id: string): Observable<HttpResponse<LuckyDipV2>> {
    const url = `${this.brand}/lucky-dip/${id}`;
    const data = this.sendRequest<LuckyDipV2>('put', url, luckyDipV2Data).pipe(
      map(((res: HttpResponse<LuckyDipV2>) => res.body)),
      catchError(response => {
        return Observable.throw(this.generateErrorMsg(response));
      }));
    return this.wrappedObservable(data);
  }

  private generateErrorMsg(response): string {
    let message = '';
    if (response && response.error && response.error.errors) {
      response.error.errors.forEach(function (error) {
        message += `${error.field || ''} ${error.defaultMessage}. \n`;
      });
    }
    else {
      message = response.error;
    }
    return message || 'Unknown error';
  }

  public reOrder(request: Order): Observable<HttpResponse<LuckyDipV2>> {
    let uri = `lucky-dip-mapping/ordering`;
    return this.sendRequest<LuckyDipV2>('post', uri, request);
  }
}
