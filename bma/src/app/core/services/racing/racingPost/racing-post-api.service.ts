import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { map, timeout, catchError } from 'rxjs/operators';

import environment from '@environment/oxygenEnvConfig';
import {
  IRacingPostGHResponse,
  IRacingPostHRResponse
} from '@coreModule/services/racing/racingPost/racing-post.model';

@Injectable({
  providedIn: 'root'
})
export class RacingPostApiService {

  private readonly racingPostApiEndpoint;
  private readonly racingPostOneApiEndpoint;
  private readonly racingPostApiKey;
  private readonly TIMEOUT: number = 10000;

  constructor(private http: HttpClient) {
    this.racingPostApiEndpoint = environment.RACING_POST_API_ENDPOINT;
    this.racingPostOneApiEndpoint = environment.RACING_POST_ONE_API_ENDPOINT;
    this.racingPostApiKey = environment.RACING_POST_API_KEY;
  }

  /**
   * getHorseRaceDetails
   * @param {string} openBetIds - comma-separated string
   * @returns {Observable<IRacingPostHRResponse>}
   */
  getHorseRaceDetails(openBetIds: string): Observable<IRacingPostHRResponse> {
    if (!openBetIds) {
      of({} as IRacingPostHRResponse);
    } else {
      const url = `${this.racingPostApiEndpoint}/categories/21/events/${openBetIds}/content?locale=en-GB&api-key=${this.racingPostApiKey}`;
      return this.performRequest(url);
    }
  }
  
  /**
   * getHorseRaceDetailsFromOne-Api
   * @param {string} openBetIds - comma-separated string
   * @returns {Observable<IRacingPostHRResponse>}
   */
  getHorseRaceOneApiResultDetails(openBetIds: string): Observable<IRacingPostHRResponse> {
    if (!openBetIds) {
      of({} as IRacingPostHRResponse);
    } else {
      const url = `${this.racingPostOneApiEndpoint}/categories/21/events/${openBetIds}/content?locale=en-GB&api-key=${this.racingPostApiKey}`;
      return this.performRequest(url);
    }
  }

  /**
   * getGreyhoundRaceDetails
   * @param {string} openBetIds - comma-separated string
   * @returns {Observable<IRacingPostHRResponse>}
   */
  getGreyhoundRaceDetails(openBetIds: string): Observable<IRacingPostGHResponse> {
    if (!openBetIds) {
      of({} as IRacingPostGHResponse);
    } else {
      const url = `${this.racingPostApiEndpoint}/categories/19/events/${openBetIds}/content?locale=en-GB&api-key=${this.racingPostApiKey}`;
      return this.performRequest(url);
    }
  }

  /**
   * getGreyhoundRaceDetailsFromOne-Api
   * @param {string} openBetIds - comma-separated string
   * @returns {Observable<IRacingPostGHResponse>}
   */
  getGreyhoundRaceOneApiResultDetails(openBetIds: string): Observable<IRacingPostGHResponse> {
    if (!openBetIds) {
      of({} as IRacingPostGHResponse);
    } else {
      const url = `${this.racingPostOneApiEndpoint}/categories/19/events/${openBetIds}/content?locale=en-GB&api-key=${this.racingPostApiKey}`;
      return this.performRequest(url);
    }
  }

  /**
   * PerformRequest()
   * @param url
   * @param params
   * @returns {Observable<HttpResponse<T>>}
   */
  private performRequest<T>(url, params: any = {}): Observable<T> {
    return this.http
      .get<T>(`${url}`, {
        observe: 'response',
        params: params,
        headers: {
          accept: 'application/json'
        }
      }).pipe(
        timeout(this.TIMEOUT),
        map((data: HttpResponse<T>) => data.body),
        catchError(() => {
          return of(<any>{});
        })
      );
  }
}
