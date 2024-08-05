import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';

@Injectable()
export class TimelineTemplateService extends AbstractService<Configuration> {
  pageBaseUrl: string = 'timeline/template';
  pageByBrandUrl: string = `timeline/template/brand/${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getTemplatesByBrand(): Observable<HttpResponse<TimelineTemplate[]>> {
    return this.sendRequest<TimelineTemplate[]>('get', this.pageByBrandUrl, null);
  }

  public getSingleTemplate(id: string): Observable<HttpResponse<TimelineTemplate>> {
    const url = `${this.pageBaseUrl}/${id}`;
    return this.sendRequest<TimelineTemplate>('get', url, null);
  }

  public saveTemplate(template: TimelineTemplate): Observable<HttpResponse<TimelineTemplate>> {
    return this.sendRequest<TimelineTemplate>('post', this.pageBaseUrl, template);
  }

  public updateTemplate(id: string, template: TimelineTemplate): Observable<HttpResponse<TimelineTemplate>> {
    const apiUrl = `${this.pageBaseUrl}/${id}`;
    return this.sendRequest<TimelineTemplate>('put', apiUrl, template);
  }

  public deleteTemplate(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.pageBaseUrl}/${id}`, null);
  }

  public uploadImage(id: string, imageType: string, file: FormData): Observable<HttpResponse<TimelineTemplate>> {
    const uri = `${this.pageBaseUrl}/${id}/image?imageType=${imageType}`;
    return this.sendRequest<TimelineTemplate>('post', uri, file);
  }

  public deleteImage(id: string, imageType: string): Observable<HttpResponse<TimelineTemplate>> {
    const uri = `${this.pageBaseUrl}/${id}/image?imageType=${imageType}`;
    return this.sendRequest<TimelineTemplate>('delete', uri, null);
  }

}
