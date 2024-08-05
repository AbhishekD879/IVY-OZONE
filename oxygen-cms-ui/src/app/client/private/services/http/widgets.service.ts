import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Widget} from '../../models/widget.model';
import { Order } from '../../models/order.model';

@Injectable()
export class WidgetsService extends AbstractService<Configuration> {
  widgetsUrl: string = 'widget';
  widgetsByBrandUrl: string = `widget/brand/${this.brand}`;
  widgetsOrderUrl: string = 'widget/ordering';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getWidgets(): Observable<HttpResponse<Widget[]>> {
    return this.sendRequest<Widget[]>('get', this.widgetsByBrandUrl, null);
  }

  public getSingleWidget(id: string): Observable<HttpResponse<Widget>> {
    const url = `${this.widgetsUrl}/${id}`;
    return this.sendRequest<Widget>('get', url, null);
  }

  public putWidgetChanges(id: string, prmotionData: Widget): Observable<HttpResponse<Widget>> {
    const apiUrl = `${this.widgetsUrl}/${id}`;

    return this.sendRequest<Widget>('put', apiUrl, prmotionData);
  }

  public postNewWidgetsOrder(widgetsOrder: Order): Observable<HttpResponse<Widget[]>> {
    return this.sendRequest<Widget[]>('post', this.widgetsOrderUrl, widgetsOrder);
  }
}
