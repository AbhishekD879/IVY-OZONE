import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Event } from '../../models/event.model';

@Injectable()
export class EventsService extends AbstractService<Configuration> {
    gameEventGameId: string = 'game';
    gameEvent: string = 'game-event';
    gameEventByGameId: string = 'game-event/game-id/';


    constructor(http: HttpClient, domain: string, brand: string) {
      super(http, domain, brand);
    }

    public getEvent(eventId: string): Observable<HttpResponse<Object>> {
      return this.sendRequest<Event>('get', `${this.gameEventGameId + `/brand/${this.brand}/event-id/` + eventId}`, null);
    }
}
