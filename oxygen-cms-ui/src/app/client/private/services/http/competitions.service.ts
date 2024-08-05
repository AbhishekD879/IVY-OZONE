import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Competition, CompetitionUpdate, OBEvents} from '../../models';

@Injectable()
export class CompetitionsService extends AbstractService<Competition> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'competition';
  }

  findAllCompetitions(): Observable<HttpResponse<Competition[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<Competition[]>('get', uri, null);
  }

  createCompetition(competition: Competition): Observable<HttpResponse<Competition>> {
    return this.sendRequest<Competition>('post', this.uri, competition);
  }

  getSingleCompetition(id: string): Observable<HttpResponse<Competition>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<Competition>('get', uri, null);
  }

  getSiteServeEvents(options): Observable<HttpResponse<OBEvents>> {
    const uri = `${this.uri}/brand/${this.brand}/ss/event`;
    return this.sendRequest<OBEvents>('get', uri, options);
  }

  getSiteServeEventsByType(options): Observable<HttpResponse<OBEvents>> {
    const uri = `${this.uri}/brand/${this.brand}/ss/type`;
    return this.sendRequest<OBEvents>('get', uri, options);
  }

  editCompetition(updateData: CompetitionUpdate): Observable<HttpResponse<Competition>> {
    const uri = `${this.uri}/${updateData.id}`;
    return this.sendRequest<Competition>('put', uri, updateData);
  }

  deleteCompetition(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
}
