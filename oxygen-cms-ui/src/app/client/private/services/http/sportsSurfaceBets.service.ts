import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Order } from '@app/client/private/models/order.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { ActiveSurfaceBets, SurfaceBet, SurfaceBetTitle } from '@app/client/private/models/surfaceBet.model';

@Injectable()
export class SportsSurfaceBetsService extends AbstractService<SurfaceBet> {

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `surface-bet`;
  }

  public findAll(): Observable<HttpResponse<SurfaceBet[]>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SurfaceBet[]>('get', uri, null);
  }

  public findAllByBrand(brand: string): Observable<HttpResponse<SurfaceBet[]>> {
    const uri = `${this.uri}/brand/${brand}`;
    return this.sendRequest<SurfaceBet[]>('get', uri, null);
  }

  /**
  * relatedTo - sport, edp or eventhub
  */
  public findAllByBrandAndSport(brand: string, relatedTo: string, sportCategoryId: number, segment: string): Observable<HttpResponse<SurfaceBet[]>> {
    const uri = `${this.uri}/brand/${brand}/segment/${segment}/${relatedTo}/${sportCategoryId}`;
    return this.sendRequest<SurfaceBet[]>('get', uri, null);
  }

  public findById(id: string): Observable<HttpResponse<SurfaceBet>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<SurfaceBet>('get', uri, null);
  }

  public save(bet: SurfaceBet): Observable<HttpResponse<SurfaceBet>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SurfaceBet>('post', uri, bet);
  }

  public update(bet: SurfaceBet): Observable<HttpResponse<SurfaceBet>> {
    const uri = `${this.uri}/${bet.id}`;
    return this.sendRequest<SurfaceBet>('put', uri, bet);
  }

  /**
  * relatedTo - active bets checks
  */
  public updateActiveBets(bet: ActiveSurfaceBets[]): Observable<HttpResponse<ActiveSurfaceBets[]>> {
    const uri = `surface-bets`;
    return this.sendRequest<ActiveSurfaceBets[]>('put', uri, bet);
  }

  public delete(betId: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${betId}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(order: Order): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<void>('post', uri, order);
  }

  public uploadIcon(betId: string, file: FormData): Observable<HttpResponse<SurfaceBet>> {
    const uri = `${this.uri}/${betId}/image`;
    return this.sendRequest<SurfaceBet>('post', uri, file);
  }

  public deleteIcon(betId: string): Observable<HttpResponse<SurfaceBet>> {
    const uri = `${this.uri}/${betId}/image`;
    return this.sendRequest<SurfaceBet>('delete', uri, null);
  }

  public hasActiveBets(brand: string, relatedTo: string, sportCategoryId: number): Observable<HttpResponse<boolean>> {
    const uri = `${this.uri}/has-active-bets/${brand}/${relatedTo}/${sportCategoryId}`;
    return this.sendRequest<boolean>('get', uri, null);
  }

  public enableBetsForSport(brand: string, relatedTo: string, sportCategoryId: number): Observable<HttpResponse<boolean>> {
    const uri = `${this.uri}/enable/${brand}/${relatedTo}/${sportCategoryId}`;
    return this.sendRequest<boolean>('post', uri, null);
  }

  public disableBetsForSport(brand: string, relatedTo: string, sportCategoryId: number): Observable<HttpResponse<boolean>> {
    const uri = `${this.uri}/disable/${brand}/${relatedTo}/${sportCategoryId}`;
    return this.sendRequest<boolean>('post', uri, null);
  }

  public getSurfaceBetTitle(brand: string): Observable<HttpResponse<SurfaceBetTitle[]>> {
    const uri = `${this.uri}/brand/${brand}/title`;
    return this.sendRequest<[]>('get', uri, null);
  }

  public deleteSurfaceBetTitle(brand,id): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/brand/${brand}/id/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
}
