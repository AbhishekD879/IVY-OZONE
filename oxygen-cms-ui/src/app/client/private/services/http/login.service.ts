import { AbstractService} from './transport/abstract.service';
import { Login} from '../../models/login.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AuthTokens } from '../../models/authTokens.model';

@Injectable()
export class LoginService extends AbstractService<Login> {
  refreshSessionUrl: string = `token`;
  uri: string = 'login';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public logIn(username: string, password: string): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.uri, {
      username, password
    });
  }

  /**
   * Get updated tokens from server to renew login session
   * @return {Observable<HttpResponse<AuthTokens>>}
   */
  public refreshToken(): Observable<HttpResponse<AuthTokens>> {
    return this.sendRequest<AuthTokens>('post', this.refreshSessionUrl, {
      refreshToken: localStorage.getItem('refreshToken') || ''
    });
  }
}
