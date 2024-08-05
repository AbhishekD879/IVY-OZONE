import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { FooterMenu } from '../../../models/footermenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class FooterMenuService extends AbstractService<FooterMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `footer-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<FooterMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<FooterMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<FooterMenu>('get', uri, null);
  }
  public save(footerMenu: FooterMenu): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<FooterMenu>('post', uri, footerMenu);
  }

  public update(footerMenu: FooterMenu): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}/${footerMenu.id}`;
    return this.sendRequest<FooterMenu>('put', uri, footerMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<FooterMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<FooterMenu[]>('post', uri, obj);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<FooterMenu>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<FooterMenu>('delete', uri, null);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<FooterMenu>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<FooterMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<FooterMenu>('delete', uri, null);
  }

  /**
   * retrieve the list of footerMenu items based on segment selection
   * @param segment value seelcted via dropdown selection
   * @returns 
   */
  public getFooterMenusBySegment(segment: string): Observable<HttpResponse<FooterMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}`;
    return this.sendRequest<FooterMenu[]>('get', uri, null);
  }
}
