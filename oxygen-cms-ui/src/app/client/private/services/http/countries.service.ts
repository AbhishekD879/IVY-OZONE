import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Country } from '../../models/country.model';

@Injectable()
export class CountriesService extends AbstractService<Country[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `country`;
  }

  public findAllByBrand(): Observable<HttpResponse<Country[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<Country[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(league: Country): Observable<HttpResponse<Country>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<Country>('post', uri, league);
  }

  public getById(id: string): Observable<HttpResponse<Country>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<Country>('get', uri, null);
  }

  public edit(league: Country): Observable<HttpResponse<Country>> {
    const uri = `${this.uri}/${league.id}`;
    return this.sendRequest<Country>('put', uri, league);
  }
}
