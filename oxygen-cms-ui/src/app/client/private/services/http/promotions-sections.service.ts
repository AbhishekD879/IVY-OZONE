import { Order } from '@app/client/private/models/order.model';
import { PromotionsSections } from '../../models/promotions-sections.model';
import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';

@Injectable()
export class PromotionsSectionsService extends AbstractService<PromotionsSections[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `promotion/brand/${this.brand}/section`;
  }

  public findAllByBrand(): Observable<HttpResponse<PromotionsSections[]>> {
    return this.sendRequest<PromotionsSections[]>('get', this.uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(promotionSection: PromotionsSections): Observable<HttpResponse<PromotionsSections>> {
    return this.sendRequest<PromotionsSections>('post', this.uri, promotionSection);
  }

  public getById(id: string): Observable<HttpResponse<PromotionsSections>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<PromotionsSections>('get', uri, null);
  }

  public postNewPromotionsSectionsOrder(order: Order): Observable<HttpResponse<PromotionsSections[]>> {
    return this.sendRequest<PromotionsSections[]>('post', `${this.uri}/ordering`, order);
  }

  public edit(promotionSection: PromotionsSections): Observable<HttpResponse<PromotionsSections>> {
    const uri = `${this.uri}/${promotionSection.id}`;
    return this.sendRequest<PromotionsSections>('put', uri, promotionSection);
  }
}
