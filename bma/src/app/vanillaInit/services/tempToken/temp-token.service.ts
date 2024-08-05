import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { ITempTokenResponse } from '@vanillaInitModule/models/temp-token-reponse.interface';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TempTokenService {
  temporaryToken: string;

  constructor(private http: HttpClient) {}

  // return response with Temporary Token.
  fetchTemporaryToken(): Observable<ITempTokenResponse> {
    // Disable cache
    const timestamp = `?_${new Date().getTime()}`;

    return this.http.get<ITempTokenResponse>(`en/coralsports/api/temporarytoken${timestamp}`);
  }

  // needs a callback function to be passed within to perform after http call actions.
  getTemporaryToken(callback: Function = null): void {
    this.fetchTemporaryToken().subscribe((response: ITempTokenResponse) => {
      this.temporaryToken = response && response.sessionToken;

      if (callback) {
        callback(response);
      }
    }, (error) => {
      // eslint-disable-next-line no-console
      console.log(`Error occurred while generating temporary token: ${error}`);
      return error;
    });
  }
}
