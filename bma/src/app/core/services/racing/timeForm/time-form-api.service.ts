import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { ITimeFormData } from '@core/models/time-form-data.model';
import { Observable, of } from 'rxjs';
import { map, timeout, catchError } from 'rxjs/operators';

import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class TimeFormApiService {

  private readonly timeFormEndpoint;

  // Max amount of time to wait response form time form
  private readonly TIMEOUT: number = 10000;

  constructor(private http: HttpClient) {
    this.timeFormEndpoint = environment.TIMEFORM_ENDPOINT;
  }

  /**
   * getGreyhoundRaceDetails
   * @param {string} openBetIds
   * @returns {Promise<any>}
   */
  getGreyhoundRaceDetails(openBetIds: string): Observable<ITimeFormData> {
    const url = `${this.timeFormEndpoint}/api/v1/greyhoundracing/race/${openBetIds}/openbet`,
      params = { isArray: true };

    return this.performRequest(url, params).pipe(
      map((data: HttpResponse<ITimeFormData>): ITimeFormData => data.body),
      timeout(this.TIMEOUT),
      catchError(() => {
        return of(null);
      })
    );
  }

  /**
   * PerformRequest()
   * @param url
   * @param params
   * @returns {Observable<HttpResponse<T>>}
   */
  private performRequest<T>(url, params: any = {}): Observable<HttpResponse<T>> {
    return this.http
      .get<T>(`${url}`, {
        observe: 'response',
        params: params,
        headers: {
          accept: 'application/json'
        }
      });
  }
}
