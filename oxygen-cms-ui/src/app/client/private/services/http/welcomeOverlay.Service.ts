import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { IWelcomeOverlay } from '@app/five-a-side-showdown/models/welcome-overlay';

@Injectable()
/**
 * welcome overlay service for creation removal, editing , uploading of fields
 */
export class welcomeOverlayService extends AbstractService<Configuration> {
  private readonly WELCOME_OVERLAY_URL: string = `overlay`; // TO remove comment

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get the welcome overlay by brand
   * @returns {Observable<HttpResponse<IWelcomeOverlay>>}
   */
  public getDetailsByBrand(): Observable<HttpResponse<IWelcomeOverlay>> {
    return this.sendRequest<IWelcomeOverlay>('get', `${this.WELCOME_OVERLAY_URL}/brand/${this.brand}`, null);
  }

  /**
   * To Save welcome overlay
   * @param {IWelcomeOverlay} request
   * @returns {Observable<HttpResponse<IWelcomeOverlay>>}
   */
  public saveWelcomeOverlay(request: IWelcomeOverlay): Observable<HttpResponse<IWelcomeOverlay>> {
    return this.sendRequest<IWelcomeOverlay>('post', this.WELCOME_OVERLAY_URL, request);
  }

  /**
   * To Update welcome overlay
   * @param {IWelcomeOverlay} request
   * @returns {Observable<HttpResponse<IWelcomeOverlay>>}
   */
  public updateWelcomeOverlay(request: IWelcomeOverlay): Observable<HttpResponse<IWelcomeOverlay>> {
    return this.sendRequest<IWelcomeOverlay>('put', `${this.WELCOME_OVERLAY_URL}/${request.id}`, request);
  }
}
