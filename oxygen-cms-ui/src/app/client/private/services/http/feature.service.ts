import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Feature } from '../../models/feature.model';
import { Order } from '../../models/order.model';

@Injectable()
export class FeatureService extends AbstractService<Feature[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `feature`;
  }

  public findAllByBrand(): Observable<HttpResponse<Feature[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;

    return this.sendRequest<Feature[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(league: Feature): Observable<HttpResponse<Feature>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<Feature>('post', uri, league);
  }

  public getById(id: string): Observable<HttpResponse<Feature>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<Feature>('get', uri, null);
  }

  public edit(league: Feature): Observable<HttpResponse<Feature>> {
    const uri = `${this.uri}/${league.id}`;
    return this.sendRequest<Feature>('put', uri, league);
  }

  public postNewFeatureOrder(order: Order): Observable<HttpResponse<Feature[]>> {
    const uri = `${this.uri}/order`;
    return this.sendRequest<Feature[]>('post', uri, order);
  }


  public postNewFeatureImage(id: string, file: FormData): Observable<HttpResponse<Feature>> {
    const apiUrl = `${this.uri}/${id}/image`;
    return this.sendRequest<Feature>('post', apiUrl, file);
  }

  public removeFeatureImage(id: string): Observable<HttpResponse<Feature>> {
    const apiUrl = `${this.uri}/${id}/image`;
    return this.sendRequest<Feature>('delete', apiUrl, null);
  }
}
