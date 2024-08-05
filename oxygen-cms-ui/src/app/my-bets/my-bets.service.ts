import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AbstractService } from '../client/private/services/http/transport/abstract.service';
import { Configuration } from '../client/private/models';
import { myBetsPayload } from './my-bets.modal';

@Injectable({
  providedIn: 'root'
})
export class MyBetsService extends AbstractService<Configuration> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }
  getmyBetsData(brand: string,page:string): Observable<HttpResponse<myBetsPayload>> {
    return this.sendRequest<myBetsPayload>('get', `${brand}/my-bets/${page}`, null);
  }
  postmyBetsData(brand: string, data:myBetsPayload,page:string ): Observable<HttpResponse<myBetsPayload>> {
    console.log(data)
    return this.sendRequest<myBetsPayload>('post', `${brand}/my-bets/${page}`, data);
  }
  putmyBetsData(brand: string, id: string, data: myBetsPayload,page:string): Observable<HttpResponse<myBetsPayload>> {
    return this.sendRequest<myBetsPayload>('put', `${brand}/my-bets/${page}/${id}`, data);
  }
  deletemyBetsData(brand: string, id: string,page:string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${brand}/my-bets/${page}/${id}`, null);
  }
}
