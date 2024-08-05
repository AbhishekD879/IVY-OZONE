
import { map } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { Observable } from 'rxjs';


import {
  IStatsAreas,
  IStatsCompetitions,
  IStatsSeasons,
  IStatsResults,
  IStatsRequestParams,
  IStatsBRCompetitionSeason,
  IStatsSeasonMatch,
  IStatsPlayer
} from '../models';
import { IWidgetParams } from '@desktop/models/wigets.model';

@Injectable()
export class StatsPointsProvider {
  private STATS_CENTRE_ENDPOINT: string;

  constructor(private http: HttpClient) {
    this.STATS_CENTRE_ENDPOINT = environment.STATS_CENTRE_ENDPOINT;
  }

  leagueTableAreas(params: IStatsRequestParams): Observable<IStatsAreas[]> {
    return this.getData(`areas/${params.sportId}`).pipe(
      map((data: HttpResponse<IStatsAreas[]>) => data.body));
  }

  leagueTableCompetitions(params: IStatsRequestParams): Observable<IStatsCompetitions[]> {
    return this.getData(`competitions/${params.sportId}/${params.areaId}`).pipe(
      map((data: HttpResponse<IStatsCompetitions[]>) => data.body));
  }

  leagueTableSeasons(params: IStatsRequestParams): Observable<IStatsSeasons[]> {
    return this.getData(`seasons/${params.sportId}/${params.areaId}/${params.competitionId}`).pipe(
      map((data: HttpResponse<IStatsSeasons[]>) => data.body));
  }

  leagueTableResults(params: IStatsRequestParams): Observable<IStatsResults[]> {
    return this.getData(`resultstables/${params.sportId}/${params.areaId}/${params.competitionId}/${params.seasonId}`).pipe(
      map((data: HttpResponse<IStatsResults[]>) => data.body));
  }

  leagueTableCompetitionSeason(params: IStatsRequestParams | IWidgetParams): Observable<IStatsBRCompetitionSeason> {
    return this.getData(`brcompetitionseason/${params.sportId}/${params.classId}/${params.typeId}`).pipe(
      map((data: HttpResponse<IStatsBRCompetitionSeason>) => {
        data.body.allCompetitions.forEach((competition,index) => {
          index == 0 ? competition['type']='parent' : competition['type']='child'; 
        })
        return data.body;
      }));
  }

  seasonMatches(seasonId: string, skip: number, limit: number): Observable<IStatsSeasonMatch[]> {
    return this.getData(`season/${seasonId}/matches/?skip=${skip}&limit=${limit}`).pipe(
      map((data: HttpResponse<IStatsSeasonMatch[]>) => data.body));
  }

  matchesByDate(params: { startdate: string, enddate: string }): Observable<IStatsSeasonMatch[]> {
    return this.getData(`matches/bydate?startdate=${params.startdate}&enddate=${params.enddate}`).pipe(
      map((data: HttpResponse<IStatsSeasonMatch[]>) => data.body));
  }

  statsCentrePlayers(ids: string[]): Observable<IStatsPlayer[]> {
    return this.postData(`player`, ids);
  }

  private getData<T>(url: string, params: { [key: string]: string } = {}): Observable<HttpResponse<T>> {
    const endpoint = `${this.STATS_CENTRE_ENDPOINT}/${url}`;
    return this.http.get<T>(endpoint, {
      observe: 'response',
      params
    });
  }

  private postData(url: string, params: string[]): Observable<IStatsPlayer[]> {
    const endpoint = `${this.STATS_CENTRE_ENDPOINT}/${url}`;
    return this.http.post<any[]>(endpoint, params);
  }
}
