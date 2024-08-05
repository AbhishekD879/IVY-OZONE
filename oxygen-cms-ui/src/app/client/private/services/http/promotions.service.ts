import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Promotion} from '../../models/promotion.model';
import { Order } from '../../models/order.model';

@Injectable()
export class PromotionsService extends AbstractService<Configuration> {
  promotionsByBrandUrl: string = `promotion/brand/${this.brand}`;
  promotionsUrl: string = 'promotion';
  promotionsOrderUrl: string = 'promotion/ordering';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getPromotions(): Observable<HttpResponse<Promotion[]>> {
    return this.sendRequest<Promotion[]>('get', this.promotionsByBrandUrl, null);
  }

  public getSinglePromotion(id: string): Observable<HttpResponse<Promotion>> {
    const url = `${this.promotionsUrl}/${id}`;
    return this.sendRequest<Promotion>('get', url, null);
  }

  public postNewPromotion(promotion: Promotion): Observable<HttpResponse<Promotion>> {
    return this.sendRequest<Promotion>('post', this.promotionsUrl, promotion);
  }

  public postNewPromotionImage(id: string, file: FormData): Observable<HttpResponse<Promotion>> {
    const apiUrl = `promotion/${id}/image`;

    return this.sendRequest<Promotion>('post', apiUrl, file);
  }

  public removePromotionImage(id: string): Observable<HttpResponse<Promotion>> {
    const apiUrl = `promotion/${id}/image`;

    return this.sendRequest<Promotion>('delete', apiUrl, null);
  }

  public putPromotionChanges(id: string, prmotionData: Promotion): Observable<HttpResponse<Promotion>> {
    const apiUrl = `promotion/${id}`;

    return this.sendRequest<Promotion>('put', apiUrl, prmotionData);
  }

  public postNewPromotionsOrder(promotionsOrder: Order): Observable<HttpResponse<Promotion[]>> {
    return this.sendRequest<Promotion[]>('post', this.promotionsOrderUrl, promotionsOrder);
  }


  public deletePromotion(id: string): Observable<HttpResponse<void>> {
    const url = `${this.promotionsUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
