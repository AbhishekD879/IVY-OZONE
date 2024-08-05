import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { FooterLogo } from '../../../models/footerlogo.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class FooterLogoService extends AbstractService<FooterLogo> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `footer-logo`;
  }

  public findAllByBrand(): Observable<HttpResponse<FooterLogo[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<FooterLogo[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<FooterLogo>('get', uri, null);
  }
  public save(footerLogo: FooterLogo): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}`;
    return this.sendRequest<FooterLogo>('post', uri, footerLogo);
  }

  public update(footerLogo: FooterLogo): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}/${footerLogo.id}`;
    return this.sendRequest<FooterLogo>('put', uri, footerLogo);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<FooterLogo[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<FooterLogo[]>('post', uri, obj);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<FooterLogo>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<FooterLogo>('delete', uri, null);
  }

  public uploadPng(id: string, file: FormData): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<FooterLogo>('post', uri, file);
  }

  public removePng(id: string): Observable<HttpResponse<FooterLogo>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<FooterLogo>('delete', uri, null);
  }
}
