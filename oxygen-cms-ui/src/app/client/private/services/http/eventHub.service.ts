import {Configuration} from '../../models/configuration.model';
import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Order} from '../../models/order.model';
import {IEventHub} from '@app/sports-pages/event-hub/models/event-hub.model';

@Injectable()
export class EventHubService extends AbstractService<Configuration> {
  baseUrl: string = 'event-hub';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getAllEventHubs(): Observable<IEventHub[]> {
    return this.sendRequest<IEventHub[]>('get', `${this.baseUrl}/brand/${this.brand}`, null)
      .map(response => response.body);
  }

  public getEventHubById(hubId: string): Observable<IEventHub> {
    return this.sendRequest<IEventHub>('get', `${this.baseUrl}/${hubId}`, null)
      .map(response => response.body);
  }

  public postNewEventHub(eventHub: IEventHub): Observable<IEventHub> {
    eventHub.brand = this.brand;

    return this.sendRequest<IEventHub>('post', this.baseUrl, eventHub)
      .map(response => response.body);
  }

  public updateEventHub(eventHub: IEventHub): Observable<IEventHub> {
    return this.sendRequest<IEventHub>('put', `${this.baseUrl}/${eventHub.id}`, eventHub)
      .map(response => response.body);
  }

  public removeEventHub(hubId: string): Observable<IEventHub> {
    return this.sendRequest<IEventHub>('delete', `${this.baseUrl}/${hubId}`, null)
      .map(response => response.body);
  }

  public reorder(obj: Order): Observable<HttpResponse<IEventHub[]>> {
    const uri = `${this.baseUrl}/ordering`;
    return this.sendRequest<IEventHub[]>('post', uri, obj);
  }
}
