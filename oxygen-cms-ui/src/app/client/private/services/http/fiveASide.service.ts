import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Order } from '../../models/order.model';
import {FiveASideFormation} from '@app/client/private/models/fiveASideFormation.model';

@Injectable()
export class FiveASideService extends AbstractService<FiveASideFormation> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'fiveASide-formation';
  }

  findAllFormations(): Observable<HttpResponse<FiveASideFormation[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<FiveASideFormation[]>('get', uri, null);
  }

  createFormation(league: FiveASideFormation): Observable<HttpResponse<FiveASideFormation>> {
    return this.sendRequest<FiveASideFormation>('post', this.uri, league);
  }

  getSingleFormation(id: string): Observable<HttpResponse<FiveASideFormation>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<FiveASideFormation>('get', uri, null);
  }

  editFormation(league: FiveASideFormation): Observable<HttpResponse<FiveASideFormation>> {
    const uri = `${this.uri}/${league.id}`;
    return this.sendRequest<FiveASideFormation>('put', uri, league);
  }

  deleteFormation(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewFormationsOrder(formationsOrder: Order): Observable<HttpResponse<FiveASideFormation[]>> {
    return this.sendRequest<FiveASideFormation[]>('post', `${this.uri}/ordering`, formationsOrder);
  }
}
