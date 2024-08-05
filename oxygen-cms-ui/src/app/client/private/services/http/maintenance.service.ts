import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from './transport/abstract.service';
import { MaintenancePage } from '../../models/maintenancepage.model';

@Injectable()
export class MaintenanceService extends AbstractService<MaintenancePage[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `maintenance-page`;
  }

  public findAllByBrand(): Observable<HttpResponse<MaintenancePage[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<MaintenancePage[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(maintenancePage: MaintenancePage): Observable<HttpResponse<MaintenancePage>> {
    const uri = `${this.uri}`;
    return this.sendRequest<MaintenancePage>('post', uri, maintenancePage);
  }

  public getById(id: string): Observable<HttpResponse<MaintenancePage>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<MaintenancePage>('get', uri, null);
  }

  public edit(maintenancePage: MaintenancePage): Observable<HttpResponse<MaintenancePage>> {
    const uri = `${this.uri}/${maintenancePage.id}`;
    return this.sendRequest<MaintenancePage>('put', uri, maintenancePage);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<MaintenancePage>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<MaintenancePage>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<MaintenancePage>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<MaintenancePage>('delete', uri, null);
  }
}
