import {AbstractService} from '@app/client/private/services/http/transport/abstract.service';
import {Configuration} from '@app/client/private/models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {OnBoardingGuide} from '@app/client/private/models/onBoardingGuide';
import {Order} from '@app/client/private/models/order.model';
import {Observable} from 'rxjs/Observable';

@Injectable()
export class OnBoardingGuideService extends AbstractService<Configuration> {
  onBoardingGuideByBrandUrl: string = `on-boarding-guide/brand/${this.brand}`;
  onBoardingGuideUrl: string = 'on-boarding-guide';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOnBoardingGuides(): Observable<HttpResponse<OnBoardingGuide[]>> {
    return this.sendRequest<OnBoardingGuide[]>('get', this.onBoardingGuideByBrandUrl, null);
  }

  public getSingleOnBoardingGuide(id: string): Observable<HttpResponse<OnBoardingGuide>> {
    const url = `${this.onBoardingGuideUrl}/${id}`;
    return this.sendRequest<OnBoardingGuide>('get', url, null);
  }

  public postNewOnBoardingGuide(onBoardingGuideUrl: OnBoardingGuide): Observable<HttpResponse<OnBoardingGuide>> {
    return this.sendRequest<OnBoardingGuide>('post', this.onBoardingGuideUrl, onBoardingGuideUrl);
  }

  public putOnBoardingGuideChanges(id: string, OnBoardingGuideData: OnBoardingGuide): Observable<HttpResponse<OnBoardingGuide>> {
    const url = `${this.onBoardingGuideUrl}/${id}`;
    return this.sendRequest<OnBoardingGuide>('put', url, OnBoardingGuideData);
  }

  public deleteOnBoardingGuide(id: string): Observable<HttpResponse<void>> {
    const url = `${this.onBoardingGuideUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }

  public postOnBoardingGuideImage(id: string, file: FormData): Observable<HttpResponse<OnBoardingGuide>> {
    const apiUrl = `on-boarding-guide/${id}/image`;

    return this.sendRequest<OnBoardingGuide>('post', apiUrl, file);
  }

  public removeOnBoardingGuideImage(id: string): Observable<HttpResponse<OnBoardingGuide>> {
    const apiUrl = `on-boarding-guide/${id}/image`;
    return this.sendRequest<OnBoardingGuide>('delete', apiUrl, null);
  }

  public postNewOnBoardingGuideOrder(onBoardingGuideOrder: Order): Observable<HttpResponse<OnBoardingGuide[]>> {
    return this.sendRequest<OnBoardingGuide[]>('post', 'on-boarding-guide/ordering', onBoardingGuideOrder);
  }
}
