import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { SportsNextEventCarousel } from '@app/client/private/models/sportsNextEventCarousel.model';
import { Order } from '@app/client/private/models/order.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { HttpClient, HttpResponse } from '@angular/common/http';

@Injectable()

export class SportsNextEventCarouselsService extends AbstractService<SportsNextEventCarousel> {

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `virtual-next-event`;
  }

  public findAll(): Observable<HttpResponse<SportsNextEventCarousel[]>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SportsNextEventCarousel[]>('get', uri, null);
  }

  public findAllByBrand(brand): Observable<HttpResponse<SportsNextEventCarousel[]>> {
    const uri = `${this.uri}/brand/${brand}`;
    return this.sendRequest<SportsNextEventCarousel[]>('get', uri, null);
  }

  public findAllByBrandAndSport(brand, pageId, pageType = 'sport'): Observable<HttpResponse<SportsNextEventCarousel[]>> {
    const uri = `${this.uri}/brand/${brand}/${pageType}/${pageId}`;
    return this.sendRequest<SportsNextEventCarousel[]>('get', uri, null);
  }

  public findById(id: string): Observable<HttpResponse<SportsNextEventCarousel>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<SportsNextEventCarousel>('get', uri, null);
  }

  public save(carousel: SportsNextEventCarousel): Observable<HttpResponse<SportsNextEventCarousel>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SportsNextEventCarousel>('post', uri, carousel);
  }

  public update(carousel: SportsNextEventCarousel): Observable<HttpResponse<SportsNextEventCarousel>> {
    const uri = `${this.uri}/${carousel.id}`;
    return this.sendRequest<SportsNextEventCarousel>('put', uri, carousel);
  }

  public delete(carouselId: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${carouselId}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(order: Order): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<void>('post', uri, order);
  }
  /**
  * retrieve the list of Highlights Carousel items based on segment selection
  * @param segment value seelcted via dropdown selection
  * @returns 
  */
  public getNextEventCarouselBySegment(segment: String, pageId:number, pageType:string): Observable<HttpResponse<SportsNextEventCarousel[]>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}/${pageType}/${pageId}`;
    return this.sendRequest<SportsNextEventCarousel[]>('get', uri, null);
  }

  public getTypeIds(classIds): Observable<HttpResponse<SportsNextEventCarousel[]>> {
    const uri = `${this.uri}/${this.brand}/${classIds}`;
    return this.sendRequest<SportsNextEventCarousel[]>('get', uri, null);
  }
}
