import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import environment from '@environment/oxygenEnvConfig';
import { Observable } from "rxjs/internal/Observable";

@Injectable({
  providedIn: 'root'
})
export class UserPreferenceProvider {
  UPMS: string;
  brand: string = environment.brand;
  constructor(
    private http: HttpClient
  ) {
    this.UPMS = environment.UPMS;
  }
  getOddsPreference(token): Observable<any> {
     const headers = new HttpHeaders({
      token: token
    });
    return this.http.get(`${this.UPMS}/${this.brand}`, { headers });
  }
  setOddsPreference(pref, token): Observable<any> {
    pref.brand = this.brand;
    return this.http.put<number[]>(`${this.UPMS}`, pref, {
      headers: { token }
    });
  }
}