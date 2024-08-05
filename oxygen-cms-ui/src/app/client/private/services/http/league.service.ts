import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { League } from '../../models/league.model';

@Injectable()
export class LeagueService extends AbstractService<League[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `league`;
  }

  public findAllByBrand(): Observable<HttpResponse<League[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;

    return this.sendRequest<League[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(league: League): Observable<HttpResponse<League>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<League>('post', uri, league);
  }

  public getById(id: string): Observable<HttpResponse<League>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<League>('get', uri, null);
  }

  public edit(league: League): Observable<HttpResponse<League>> {
    const uri = `${this.uri}/${league.id}`;
    return this.sendRequest<League>('put', uri, league);
  }
}
