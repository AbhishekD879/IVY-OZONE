import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { HttpClient, HttpResponse } from '@angular/common/http';


import { IBCData, ICompetitionModules } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import { IParticipants } from '../participants/participants.model';

@Injectable()
export class BigCompetitionsProvider {
  BIG_COMPETITION_MS: string;

  constructor(
    private http: HttpClient
  ) {
    this.BIG_COMPETITION_MS = environment.BIG_COMPETITION_MS;
  }

  tabs(name: string): Observable<IBCData> {
    return this.getData('', name).pipe(
      map((response: HttpResponse<IBCData>) => response.body));
  }
  tab(id: string): Observable<IBCData> {
    return this.getData('/tab', id).pipe(
      map((response: HttpResponse<IBCData>) => response.body));
  }
  subtab(id: string): Observable<IBCData> {
    return this.getData('/subtab', id).pipe(
      map((response: HttpResponse<IBCData>) => response.body));
  }
  module(id: string): Observable<ICompetitionModules> {
    return this.getData('/module', id).pipe(
      map((response: HttpResponse<ICompetitionModules>) => response.body));
  }
  participants(id: string): Observable<IParticipants[]> {
    return this.getData(id, 'participant').pipe(
      map((response: HttpResponse<IParticipants[]>) => response.body));
  }

  private getData<T>(url: string, params: string): Observable<HttpResponse<T>> {
    return this.http.get<T>( `${this.BIG_COMPETITION_MS}${url}/${params}`, {
      observe: 'response'
    });
  }
}
