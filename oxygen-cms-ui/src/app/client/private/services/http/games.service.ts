import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Game } from '../../models/game.model';
import { Order } from '../../models/order.model';
import { GamesEvent } from '@app/client/private/models/existinggemesevent';
import { EventScore } from '@app/client/private/models/eventScore.model';
import { EventScoreResponse } from '@app/client/private/models/eventScoreResponse.model';
@Injectable()
export class GamesService extends AbstractService<Configuration> {
  gamesByBrandUrl: string = `game/brand/${this.brand}`;
  gamesUrl: string = 'game';
  gamesOrderUrl: string = 'game/ordering';
  gameEventSave: string = 'game-event';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getGames(): Observable<HttpResponse<Game[]>> {
    return this.sendRequest<Game[]>('get', this.gamesByBrandUrl, null);
  }

  public getSingleGame(id: string): Observable<HttpResponse<Game>> {
    const url = `${this.gamesUrl}/${id}`;
    return this.sendRequest<Game>('get', url, null);
  }

  public postNewGame(game: Game): Observable<HttpResponse<Game>> {
    return this.sendRequest<Game>('post', this.gamesUrl, game);
  }

  public putGameChanges(id: string, game: Game): Observable<HttpResponse<Game>> {
    const apiUrl = `${this.gamesUrl}/${id}`;
    return this.sendRequest<Game>('put', apiUrl, game);
  }

  public postNewGamesOrder(gamesOrder: Order): Observable<HttpResponse<Game[]>> {
    return this.sendRequest<Game[]>('post', this.gamesOrderUrl, gamesOrder);
  }

  public deleteGame(id: string): Observable<HttpResponse<void>> {
    const url = `${this.gamesUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }

  public uploadImage(id: string,
                     eventId: string,
                     teamType: string,
                     fileName: string, file: FormData): Observable<HttpResponse<GamesEvent>> {
    const url = `game/${id}/image/event/${eventId}/team/${teamType}?fileType=svg`;
    return this.sendRequest<GamesEvent>('post', url, file);
  }

  public deleteImage(id: string,
                     eventId: string,
                     teamType: string): Observable<HttpResponse<GamesEvent>> {
    const url = `game/${id}/image/event/${eventId}/team/${teamType}`;
    return this.sendRequest<GamesEvent>('delete', url, null);
  }

  public postScore(id: string, score: EventScore): Observable<HttpResponse<EventScoreResponse>> {
    const url = `${this.gamesUrl}/${id}/score`;
    return this.sendRequest<EventScoreResponse>('post', url, score);
  }

  public getScore(id: string): Observable<HttpResponse<number[]>> {
    const url = `${this.gamesUrl}/${id}/score`;
    return this.sendRequest<number[]>('get', url, null);
  }
}
