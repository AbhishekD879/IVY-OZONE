import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { Order } from '@app/client/private/models/order.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { HttpClient, HttpResponse } from '@angular/common/http';

@Injectable()

export class SportsHighlightCarouselsService extends AbstractService<SportsHighlightCarousel> {

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `highlight-carousel`;
  }

  public findAll(): Observable<HttpResponse<SportsHighlightCarousel[]>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SportsHighlightCarousel[]>('get', uri, null);
  }

  public findAllByBrand(brand): Observable<HttpResponse<SportsHighlightCarousel[]>> {
    const uri = `${this.uri}/brand/${brand}`;
    return this.sendRequest<SportsHighlightCarousel[]>('get', uri, null);
  }

  public findAllByBrandAndSport(brand, pageId, pageType = 'sport'): Observable<HttpResponse<SportsHighlightCarousel[]>> {
    const uri = `${this.uri}/brand/${brand}/${pageType}/${pageId}`;
    return this.sendRequest<SportsHighlightCarousel[]>('get', uri, null);
  }

  public findById(id: string): Observable<HttpResponse<SportsHighlightCarousel>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<SportsHighlightCarousel>('get', uri, null);
  }

  public save(carousel: SportsHighlightCarousel): Observable<HttpResponse<SportsHighlightCarousel>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SportsHighlightCarousel>('post', uri, carousel);
  }

  public update(carousel: SportsHighlightCarousel): Observable<HttpResponse<SportsHighlightCarousel>> {
    const uri = `${this.uri}/${carousel.id}`;
    return this.sendRequest<SportsHighlightCarousel>('put', uri, carousel);
  }

  public delete(carouselId: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${carouselId}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public uploadIcon(carouselId: string, formData: FormData): Observable<HttpResponse<SportsHighlightCarousel>> {
    const uri = `${this.uri}/${carouselId}/image`;
    return this.sendRequest<SportsHighlightCarousel>('post', uri, formData);
  }

  public deleteIcon(carouselId: string): Observable<HttpResponse<SportsHighlightCarousel>> {
    const uri = `${this.uri}/${carouselId}/image`;
    return this.sendRequest<SportsHighlightCarousel>('delete', uri, null);
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
  public getHighlightCarouselBySegment(segment: String, pageId:number, pageType:string): Observable<HttpResponse<SportsHighlightCarousel[]>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}/${pageType}/${pageId}`;
    return this.sendRequest<SportsHighlightCarousel[]>('get', uri, null);
  }
}
