import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Order } from '@app/client/private/models/order.model';
import { IFAQ } from '@app/five-a-side-showdown/models/frequently-asked-questions';

@Injectable()
/**
 * Contest Manager service for creation removal, editing , uploading of contests
 * and prizes
 */
export class FAQService extends AbstractService<Configuration> {
  private readonly FAQURL: string = `faq`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get the list of FAQs created in cms for the brand
   * @returns {Observable<HttpResponse<IFAQ[]>>}
   */
  public getFAQs(): Observable<HttpResponse<IFAQ[]>> {
    return this.sendRequest<IFAQ[]>(
      'get',
      `${this.FAQURL}/brand/${this.brand}`, null
    );
  }

  /**
   * Get the FAQ details according to the id
   * @param {string} id
   * @returns {Observable<HttpResponse<IFAQ>>}
   */
  public getFAQForId(
    id: string
  ): Observable<HttpResponse<IFAQ>> {
    return this.sendRequest<IFAQ>(
      'get', `${this.FAQURL}/${id}`, null);
  }

  /**
   * Create contest for the new entry
   * @param {IFAQ} request
   * @returns {Observable<HttpResponse<IContest>>}
   */
  public createFAQ(request: IFAQ): Observable<HttpResponse<IFAQ>> {
    return this.sendRequest<IFAQ>('post', `${this.FAQURL}`, request);
  }

  /**
   * Edit the faq by id
   * @param {string} id
   * @param {IFAQ} faq
   * @returns {Observable<HttpResponse<IFAQ>>}
   */
  public editFAQById(
    id: string,
    faq: IFAQ
  ): Observable<HttpResponse<IFAQ>> {
    return this.sendRequest<IFAQ>('put',`${this.FAQURL}/${id}`, faq);
  }

  /**
   * Api to re order the faqs
   * @param {Order} newOrder
   * @returns {Observable<HttpResponse<IFAQ[]>>}
   */
  public postNewOrder(
    newOrder: Order
  ): Observable<HttpResponse<IFAQ[]>> {
    return this.sendRequest<IFAQ[]>('post', `${this.FAQURL}/ordering`, newOrder);
  }

  /**
   * Remove FAQ for the id
   * @param {string} id
   * @returns {Observable<HttpResponse<void>>}
   */
  public removeFAQForId(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete',`${this.FAQURL}/${id}`, null);
  }
}
