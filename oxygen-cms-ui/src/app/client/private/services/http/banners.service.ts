import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Banner } from '../../models/banner.model';
import { Order } from '../../models/order.model';

@Injectable()
export class BannersService extends AbstractService<Configuration> {
  bannersByBrandUrl: string = `banner/brand/${this.brand}`;
  bannersUrl: string = 'banner';
  bannersOrderUrl: string = 'banner/ordering';
  bannersUploadImageUrl: string = 'banner/uploadImage';
  bannersRemoveImageUrl: string = 'banner/removeImage';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getBanners(): Observable<HttpResponse<Banner[]>> {
    return this.sendRequest<Banner[]>('get', this.bannersByBrandUrl, null);
  }

  public getSingleBanner(id: string): Observable<HttpResponse<Banner>> {
    const url = `${this.bannersUrl}/${id}`;
    return this.sendRequest<Banner>('get', url, null);
  }

  public postNewBanner(banner: Banner): Observable<HttpResponse<Banner>> {
    return this.sendRequest<Banner>('post', this.bannersUrl, banner);
  }

  public postNewBannerImage(bannerId: string, file: FormData): Observable<HttpResponse<Banner>> {
    const apiUrl = `${this.bannersUploadImageUrl}/${bannerId}`;

    return this.sendRequest<Banner>('post', apiUrl, file);
  }

  public removeBannerImage(bannerId: string, params: any): Observable<HttpResponse<Banner>> {
    const apiUrl = `${this.bannersRemoveImageUrl}/${bannerId}`;

    return this.sendRequest<Banner>('get', apiUrl, params);
  }


  public putBannerChanges(id: string, bannerData: Banner): Observable<HttpResponse<Banner>> {
    const apiUrl = `${this.bannersUrl}/${id}`;

    return this.sendRequest<Banner>('put', apiUrl, bannerData);
  }

  public postNewBannersOrder(bannersOrder: Order): Observable<HttpResponse<Banner[]>> {
    return this.sendRequest<Banner[]>('post', this.bannersOrderUrl, bannersOrder);
  }

  public deleteBanner(id: string): Observable<HttpResponse<void>> {
    const url = `${this.bannersUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
