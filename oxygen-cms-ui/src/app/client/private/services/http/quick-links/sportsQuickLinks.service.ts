import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { SportsQuickLink } from '../../../models/sportsquicklink.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class SportsQuickLinksService extends AbstractService<SportsQuickLink> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `sport-quick-link`;
  }

  public findAllByBrand(sportId?: string, pageType?: string): Observable<HttpResponse<SportsQuickLink[]>> {
    let uri = `${this.uri}/brand/${this.brand}`;

    if (sportId) {
      uri += `/${pageType ? pageType : 'sport'}/${sportId}`;
    }

    return this.sendRequest<SportsQuickLink[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<SportsQuickLink>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<SportsQuickLink>('get', uri, null);
  }

  public save(sportsQuickLink: SportsQuickLink): Observable<HttpResponse<SportsQuickLink>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SportsQuickLink>('post', uri, sportsQuickLink);
  }

  public update(sportsQuickLink: SportsQuickLink): Observable<HttpResponse<SportsQuickLink>> {
    const uri = `${this.uri}/${sportsQuickLink.id}`;
    return this.sendRequest<SportsQuickLink>('put', uri, sportsQuickLink);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<SportsQuickLink[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<SportsQuickLink[]>('post', uri, obj);
  }

  public uploadIcon(id: string, file: FormData): Observable<HttpResponse<SportsQuickLink>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<SportsQuickLink>('post', uri, file);
  }

  public removeIcon(id: string): Observable<HttpResponse<SportsQuickLink>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<SportsQuickLink>('delete', uri, null);
  }

  /**
   * retrieve the list of sports quick links items based on segment selection
   * @param segment value seelcted via dropdown selection
   * @returns 
   */
  public getSportsQuickLinksBySegment(segment: String, sportId?: string, pageType?: string): Observable<HttpResponse<SportsQuickLink[]>> {
    let uri = `${this.uri}/brand/${this.brand}/segment/${segment}`;
    if (sportId) {
      uri += `/${pageType ? pageType : 'sport'}/${sportId}`;
    }
    return this.sendRequest<SportsQuickLink[]>('get', uri, null);
  }
}
