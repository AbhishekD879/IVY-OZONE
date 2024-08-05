import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Offer} from '../../models/offer.model';
import { Order } from '../../models/order.model';

@Injectable()
export class OffersService extends AbstractService<Configuration> {
  offersByBrandUrl: string = `offer/brand/${this.brand}`;
  offersUrl: string = 'offer';
  offersOrderUrl: string = `offer/ordering`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOffers(): Observable<HttpResponse<Offer[]>> {
    return this.sendRequest<Offer[]>('get', this.offersByBrandUrl, null);
  }

  public getSingleOffer(id: string): Observable<HttpResponse<Offer>> {
    const url = `${this.offersUrl}/${id}`;
    return this.sendRequest<Offer>('get', url, null);
  }

  public postNewOffer(offer: Offer): Observable<HttpResponse<Offer>> {
    return this.sendRequest<Offer>('post', this.offersUrl, offer);
  }

  public postNewOfferImage(id: string, file: FormData): Observable<HttpResponse<Offer>> {
    const apiUrl = `${this.offersUrl}/${id}/image`;

    return this.sendRequest<Offer>('post', apiUrl, file);
  }

  public removeOfferImage(id: string): Observable<HttpResponse<Offer>> {
    const apiUrl = `${this.offersUrl}/${id}/image`;

    return this.sendRequest<Offer>('delete', apiUrl, null);
  }

  public putOfferChanges(id: string, prmotionData: Offer): Observable<HttpResponse<Offer>> {
    const apiUrl = `${this.offersUrl}/${id}`;

    return this.sendRequest<Offer>('put', apiUrl, prmotionData);
  }

  public postNewOfferOrder(offersOrder: Order): Observable<HttpResponse<Offer[]>> {
    return this.sendRequest<Offer[]>('post', this.offersOrderUrl, offersOrder);
  }


  public deleteOffer(id: string): Observable<HttpResponse<void>> {
    const url = `${this.offersUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
