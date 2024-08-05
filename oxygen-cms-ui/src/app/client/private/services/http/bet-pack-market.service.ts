import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { BannerModel, BetPackModel, FilterModel, StaticFieldModel } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { Order } from '../../models/order.model';

@Injectable()
export class BetPackMarketService extends AbstractService<Configuration> {
  betPackBannerUrl: string = 'bet-pack/banner';
  betPackBackgroundUploadUrl: string = 'bet-pack/label/uploadImage';
  betPackBackgroundRemoveUrl: string = 'bet-pack/label/remove-image';
  betPackFilterUrl: string = 'bet-pack/filter';
  betPackLabelUrl: string = 'bet-pack/label';
  betPackUrl: string = 'bet-pack';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }
  postBannerData(data: FormData): Observable<HttpResponse<BannerModel>> {
    return this.sendRequest<BannerModel>('post', this.betPackBannerUrl, data);
  }
  getBannerData(): Observable<HttpResponse<BannerModel>> {
    return this.sendRequest<BannerModel>('get', `bet-pack/banner/brand/${this.brand}`, null);
  }
  putBannerData(data: FormData, id: string): Observable<HttpResponse<BannerModel>> {
    const url = `${this.betPackBannerUrl}/${id}`;
    return this.sendRequest<BannerModel>('put', url, data);
  }
  getFilters(): Observable<HttpResponse<FilterModel[]>> {
    return this.sendRequest<FilterModel[]>('get', `bet-pack/filters/brand/${this.brand}`, null);
  }
  postFilter(data: FilterModel): Observable<HttpResponse<FilterModel>> {
    return this.sendRequest<FilterModel>('post', this.betPackFilterUrl, data);
  }
  public deleteFilter(id: string): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('delete', `${this.betPackFilterUrl}/${id}`, null);
  }
  public getFilterById(id: string): Observable<HttpResponse<FilterModel>> {
    return this.sendRequest<FilterModel>('get', `${this.betPackFilterUrl}/${id}`, null);
  }
  public putFilter(filter: FilterModel): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('put', `${this.betPackFilterUrl}/${filter.id}`, filter);
  }
  public reorderFilter(obj: Order): Observable<HttpResponse<FilterModel[]>> {
    const uri = `${this.betPackFilterUrl}/ordering`;
    return this.sendRequest<FilterModel[]>('post', uri, obj);
  }
  public getBetPackData(): Observable<HttpResponse<BetPackModel[]>> {
    return this.sendRequest<BetPackModel[]>('get', `bet-packs/brand/${this.brand}`, null);
  }
  public deleteBetPack(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.betPackUrl}/${id}`, null);
  }
  public reorderBetPack(obj: Order): Observable<HttpResponse<BetPackModel[]>> {
    const uri = `${this.betPackUrl}/ordering`;
    return this.sendRequest<BetPackModel[]>('post', uri, obj);
  }
  postBetPack(data: BetPackModel): Observable<HttpResponse<BetPackModel>> {
    return this.sendRequest<BetPackModel>('post', this.betPackUrl, data);
  }
  putBetPack(data: BetPackModel): Observable<HttpResponse<BetPackModel>> {
    return this.sendRequest<BetPackModel>('put', `${this.betPackUrl}/${data.id}`, data);
  }
  public getBetPackById(id: string): Observable<HttpResponse<BetPackModel>> {
    return this.sendRequest<BetPackModel>('get', `${this.betPackUrl}/${id}`, null);
  }
  getLabelsData(): Observable<HttpResponse<StaticFieldModel>> {
    return this.sendRequest<StaticFieldModel>('get', `bet-pack/label/brand/${this.brand}`, null);
  }
  postLabelsData(data: StaticFieldModel): Observable<HttpResponse<StaticFieldModel>> {
    return this.sendRequest<StaticFieldModel>('post', this.betPackLabelUrl, data);
  }
  putLabelsData(data: StaticFieldModel): Observable<HttpResponse<StaticFieldModel>> {
    return this.sendRequest<StaticFieldModel>('put', `${this.betPackLabelUrl}/${data.id}`, data);
  }
  deleteLabelsData(id: string): Observable<HttpResponse<StaticFieldModel>> {
    return this.sendRequest<StaticFieldModel>('delete', `${this.betPackLabelUrl}/${id}`, null);
  }
  postBackgroundData(data: FormData, id: string): Observable<HttpResponse<BannerModel>> {
    return this.sendRequest<BannerModel>('post', `${this.betPackBackgroundUploadUrl}/${id}`, data);
  }
  deleteBackgroundData(id: string): Observable<HttpResponse<BannerModel>> {
    return this.sendRequest<BannerModel>('delete', `${this.betPackBackgroundRemoveUrl}/${id}`, null);
  }
}
