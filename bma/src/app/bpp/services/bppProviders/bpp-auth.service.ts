import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';

import { Observable } from 'rxjs';
import { IPostBody, IRespAccountValidate } from './bpp-providers.model';

@Injectable()
export class BppAuthService {

  private readonly apiEndpoint: string;

  constructor(
    private http: HttpClient
  ) { this.apiEndpoint = environment.BPP_ENDPOINT; }

  validate(body: IPostBody): Observable<IRespAccountValidate> {
    return this.postData(`auth/user`, body);
  }

  private postData<T>(url: string, body: IPostBody): Observable<IRespAccountValidate> {
    return this.http.post<IRespAccountValidate>( `${this.apiEndpoint}/${url}`, body, {
      withCredentials: true
    });
  }
}
