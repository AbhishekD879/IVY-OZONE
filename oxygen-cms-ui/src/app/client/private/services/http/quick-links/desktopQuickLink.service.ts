import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';

import {AbstractService} from '../transport/abstract.service';
import {DesktopQuickLink} from '../../../models/desktopquicklink.model';
import {Order} from '../../../models/order.model';

@Injectable()
export class DesktopQuickLinkService extends AbstractService<DesktopQuickLink> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `desktop-quick-link`;
  }

  public findAllByBrand(): Observable<HttpResponse<DesktopQuickLink[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<DesktopQuickLink[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<DesktopQuickLink>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<DesktopQuickLink>('get', uri, null);
  }
  public save(desktopQuickLink: DesktopQuickLink): Observable<HttpResponse<DesktopQuickLink>> {
    const uri = `${this.uri}`;
    return this.sendRequest<DesktopQuickLink>('post', uri, desktopQuickLink);
  }

  public update(desktopQuickLink: DesktopQuickLink): Observable<HttpResponse<DesktopQuickLink>> {
    const uri = `${this.uri}/${desktopQuickLink.id}`;
    return this.sendRequest<DesktopQuickLink>('put', uri, desktopQuickLink);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<DesktopQuickLink[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<DesktopQuickLink[]>('post', uri, obj);
  }

  public uploadIcon(id: string, file: FormData): Observable<HttpResponse<DesktopQuickLink>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<DesktopQuickLink>('post', uri, file);
  }

  public removeIcon(id: string): Observable<HttpResponse<DesktopQuickLink>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<DesktopQuickLink>('delete', uri, null);
  }
}
