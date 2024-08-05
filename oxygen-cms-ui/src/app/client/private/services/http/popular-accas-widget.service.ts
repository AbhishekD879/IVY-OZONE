import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PopularAccasWidget } from '@app/popular-bets/popular-accas-widget/popular-accas-widget.model';
import { Observable } from 'rxjs';
import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Order } from '../../models/order.model';


@Injectable({
  providedIn: 'root'
})
export class PopularAccasWidgetService extends AbstractService<Configuration> {

  popularAccasWidgetUrl: string = `popular-acca-widget`;
  popularAccasWidgetDataUrl: string = `popular-acca-widget-data`;
  popularAccasWidgetByBrandUrl: string = `${this.popularAccasWidgetUrl}/brand/${this.brand}`;
  popularAccasWidgetDataByBrandUrl: string = `${this.popularAccasWidgetDataUrl}/brand/${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getPopularAccasWidgetData(): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('get', this.popularAccasWidgetByBrandUrl, null);
  }

  public postPopularAccasWidgetData( data: PopularAccasWidget): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('post', this.popularAccasWidgetUrl, data);
  }

  public putPopularAccasWidgetData( data: PopularAccasWidget): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('put', `${this.popularAccasWidgetUrl}/${data.id}`, data);
  }


  public getPopularAccasWidgetCardData(id: string): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('get', `${this.popularAccasWidgetDataUrl}/${id}`, null);
  }

  public putPopularAccasWidgetCardData(data: PopularAccasWidget): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('put', `${this.popularAccasWidgetDataUrl}/${data.id}`, data);
  }
    
  public postPopularAccasWidgetCardData(data: PopularAccasWidget): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('post', this.popularAccasWidgetDataUrl, data);
  }

  public reorderPopularAccasWidgetcardData(order: Order): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('post', `${this.popularAccasWidgetDataUrl}/ordering`, order);
  }

  public getsegmentdata(status: any): Observable<HttpResponse<PopularAccasWidget[]>> {
    const uri = `${this.popularAccasWidgetDataByBrandUrl}/status`;
    return this.sendRequest<[PopularAccasWidget]>('get', uri, status);
  }
  
  public deletePopularAccasWidgetCardData(id: string): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('delete', `${this.popularAccasWidgetDataUrl}/${id}`, null);
  }

  public getPopularAccasWidgetCardDataByBrand(): Observable<HttpResponse<PopularAccasWidget>> {
    return this.sendRequest<PopularAccasWidget>('get', this.popularAccasWidgetDataByBrandUrl, null);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<any>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<any>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<PopularAccasWidget>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<PopularAccasWidget>('delete', uri, null);
  }

}
