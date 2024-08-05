import { Injectable } from '@angular/core';
import {Configuration} from '../../models/configuration.model';
import {AbstractService} from './transport/abstract.service';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { Order } from '../../models/order.model';
import { ILotto, ILottos, ILottoUpdate } from '@root/app/lotto/lotto.model';
@Injectable({
  providedIn: 'root'
})
export class LottosService extends AbstractService<Configuration> {
  lottoBaseUrl: string = 'lotto-config';
  lottoByBrandUrl: string = `lotto-config/brand/${this.brand}`;
  
  constructor(http: HttpClient, domain: string, brand: string) { 
    super(http, domain, brand);
    this.uri = `footer-menu`;
  }
  public saveLotto(lotto: ILottos): Observable<HttpResponse<ILottos>> {
    return this.sendRequest<any>('post', this.lottoBaseUrl, lotto);
  }
  public getLottery(id: string): Observable<HttpResponse<ILottos>> {
    const url = `${this.lottoBaseUrl}/${id}`;
    return this.sendRequest<ILottos>('get', url, null)
  }
  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<ILotto>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<ILotto>('post', uri, file);
  }
  public updateLottoDetails(request: ILotto): Observable<HttpResponse<ILotto>> {
    return this.sendRequest<ILotto>('put', `${this.lottoBaseUrl}/${request.id}`, request);
  }
  public reorder(obj: Order): Observable<HttpResponse<ILotto[]>> {
    const uri = `${this.lottoBaseUrl}/ordering`;
    return this.sendRequest<ILotto[]>('post', uri, obj);
  }
  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.lottoBaseUrl}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
  public findAllByBrand(): Observable<HttpResponse<ILotto>> {
    const uri = `${this.lottoBaseUrl}/brand/${this.brand}`;
    return this.sendRequest<ILotto>('get', uri, null);
  }
  public putAllByBrand(obj: ILottoUpdate): Observable<HttpResponse<ILottoUpdate[]>> {
    const uri = `${this.lottoBaseUrl}/banner-link/brand/${this.brand}`;
    return this.sendRequest<ILottoUpdate[]>('put', uri, obj);
  }
}
