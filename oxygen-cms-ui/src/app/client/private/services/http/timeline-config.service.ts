import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {
  HttpClient,
  HttpResponse
} from '@angular/common/http';

import {Observable} from 'rxjs/Observable';
import {TimelineSystemConfig} from '@app/client/private/models/timelineSystemConfig';


@Injectable()
export class TimelineConfigService extends AbstractService<Configuration> {
  byBrandUrl: string = `timeline/system-config/brand/${this.brand}`;
  rootUrl: string = 'timeline/system-config';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOneByBrand(): Observable<HttpResponse<TimelineSystemConfig>> {
    return this.sendRequest<TimelineSystemConfig>('get', this.byBrandUrl, null);
  }

  public saveConfig(timelineSystemConfig: TimelineSystemConfig): Observable<HttpResponse<TimelineSystemConfig>> {
    return this.sendRequest<TimelineSystemConfig>('post', this.rootUrl, timelineSystemConfig);
  }

  public updateConfig(timelineSystemConfig: TimelineSystemConfig): Observable<HttpResponse<TimelineSystemConfig>> {
    return this.sendRequest<TimelineSystemConfig>('put', `${this.rootUrl}/${timelineSystemConfig.id}`, timelineSystemConfig);
  }
}
