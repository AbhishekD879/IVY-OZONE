import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Brand } from '../../models/brand.model';
import { Order } from '../../models/order.model';

@Injectable()
export class BrandsService extends AbstractService<Brand> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'brand';
  }

  findAllBrands(): Observable<HttpResponse<Brand[]>> {
    return this.findAll();
  }

  createBrand(brand: Brand): Observable<HttpResponse<Brand>> {
    return this.sendRequest<Brand>('post', this.uri, brand);
  }

  getSingleBrand(id: string): Observable<HttpResponse<Brand>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<Brand>('get', uri, null);
  }

  editBrand(brand: Brand): Observable<HttpResponse<Brand>> {
    const uri = `${this.uri}/${brand.id}`;
    return this.sendRequest<Brand>('put', uri, brand);
  }

  deleteBrand(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewBrandsOrder(order: Order): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('post', `${this.uri}/ordering`, order);
  }
}
