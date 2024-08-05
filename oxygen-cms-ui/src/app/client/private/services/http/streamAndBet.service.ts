import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {StreamAndBet} from '../../models/streamandbet.model';
import {SABChildElement} from '../../models/SABChildElement.model';

@Injectable()
export class StreamAndBetService extends AbstractService<StreamAndBet[]> {

  brandUri: string;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `stream-and-bet`;
    this.brandUri = `${this.uri}/brand/${this.brand}`;
  }

  public postNewStreamAndBet(): Observable<HttpResponse<StreamAndBet>> {
    const entity = {
      brand: `${this.brand}`,
      children: []
    };
    return this.sendRequest<StreamAndBet>('post', this.uri, entity);
  }

  public findAllByBrand(): Observable<HttpResponse<StreamAndBet[]>> {
    const uri = `${this.brandUri}`;
    return this.sendRequest<StreamAndBet[]>('get', uri, null);
  }

  public postNewCategoryByBrand(streamAndBet: SABChildElement): Observable<HttpResponse<SABChildElement>> {
    const uri = `${this.brandUri}/category`;
    return this.sendRequest<SABChildElement>('post', uri, streamAndBet);
  }

  public putCategoryUpdateByBrand(streamAndBet: SABChildElement): Observable<HttpResponse<SABChildElement>> {
    const uri = `${this.brandUri}/category/${streamAndBet.siteServeId}`;
    return this.sendRequest<SABChildElement>('put', uri, streamAndBet);
  }

  public deleteCategoryByBrand(categoryId: number): Observable<HttpResponse<any>> {
    const uri = `${this.brandUri}/category/${categoryId}`;
    return this.sendRequest<any>('delete', uri, {});
  }

  public fetchAllCategories(): Observable<HttpResponse<any>> {
    const uri = `stream-and-bet/brand/${this.brand}/fetch/category`;
    return this.sendRequest<any>('get', uri, null);
  }

  public fetchEventsCategoryTreeById(categoryId: number): Observable<HttpResponse<SABChildElement[]>> {
    const uri = `stream-and-bet/brand/${this.brand}/fetch/category/${categoryId}`;
    return this.sendRequest<SABChildElement[]>('get', uri, null);
  }
}
