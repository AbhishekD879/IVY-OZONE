import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { LeagueLink } from '../../models/leagueLink.model';

@Injectable()
export class LeagueLinksService extends AbstractService<LeagueLink> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'statistics-links/league-links';
  }

  findAllLeagueLinks(): Observable<HttpResponse<LeagueLink[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<LeagueLink[]>('get', uri, null);
  }

  createLeagueLink(link: LeagueLink): Observable<HttpResponse<LeagueLink>> {
    return this.sendRequest<LeagueLink>('post', this.uri, link);
  }

  getSingleLeagueLink(id: string): Observable<HttpResponse<LeagueLink>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<LeagueLink>('get', uri, null);
  }

  editLeagueLink(link: LeagueLink): Observable<HttpResponse<LeagueLink>> {
    const uri = `${this.uri}/${link.id}`;
    return this.sendRequest<LeagueLink>('put', uri, link);
  }

  deleteLeagueLink(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
}
