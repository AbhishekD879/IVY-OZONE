import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { BankingMenu } from '../../../models/bankingmenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class BankingMenuService extends AbstractService<BankingMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `banking-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<BankingMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<BankingMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BankingMenu>('get', uri, null);
  }
  public save(bankingMenu: BankingMenu): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<BankingMenu>('post', uri, bankingMenu);
  }

  public update(bankingMenu: BankingMenu): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}/${bankingMenu.id}`;
    return this.sendRequest<BankingMenu>('put', uri, bankingMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<BankingMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<BankingMenu[]>('post', uri, obj);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<BankingMenu>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<BankingMenu>('delete', uri, null);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<BankingMenu>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<BankingMenu>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<BankingMenu>('delete', uri, null);
  }
}
