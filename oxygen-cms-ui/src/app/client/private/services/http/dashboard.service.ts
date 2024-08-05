import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Dashboard } from '../../models/dashboard.model';

@Injectable()
export class DashboardService extends AbstractService<[Dashboard]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `dashboard`;
  }

  public findAllByBrand(brand: string, date: string): Observable<HttpResponse<Dashboard[]>> {
    const uri = `${this.uri}/brand/${brand}?date=${date}`;
    return this.sendRequest<Dashboard[]>('get', uri, null);
  }

  public getById(id: string): Observable<HttpResponse<Dashboard>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<Dashboard>('get', uri, null);
  }
}
