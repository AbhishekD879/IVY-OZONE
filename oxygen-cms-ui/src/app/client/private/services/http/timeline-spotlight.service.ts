import {Injectable} from '@angular/core';
import {
  HttpClient,
  HttpResponse
} from '@angular/common/http';

import {Observable} from 'rxjs/Observable';
import {TimelineSystemConfig} from '@app/client/private/models/timelineSystemConfig';
import {AbstractService} from '@app/client/private/services/http/transport/abstract.service';
import {Configuration} from '@app/client/private/models';


@Injectable()
export class TimelineSpotlightService extends AbstractService<Configuration> {
  byBrandUrl: string = `timeline/spotlight/brand/${this.brand}`;
  byBrandRefreshUrl: string = `timeline/spotlight/brand/${this.brand}/related-events`;
  byBrandFetchSpotlightDataUrl: string = `timeline/spotlight/brand/${this.brand}`;
  rootUrl: string = 'timeline/spotlight';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOneByBrand(): Observable<HttpResponse<TimelineSystemConfig>> {
    return this.sendRequest<TimelineSystemConfig>('get', this.byBrandUrl, null);
  }

  public getSiteServeEvents(refreshEventsFrom: string, refreshEventsClassesString: string,
                            restrictToUkAndIre: boolean, isFreeRide: boolean = false): Observable<HttpResponse<TimelineSystemConfig>> {
    return this.sendRequest<TimelineSystemConfig>('post', this.byBrandRefreshUrl, {
      refreshEventsFrom,
      refreshEventsClassesString,
      restrictToUkAndIre,
      isFreeRide
    });
  }

  public getSpotlightDataForEventId(eventId, campaignId): Observable<HttpResponse<TimelineSystemConfig>> {
    return this.sendRequest<TimelineSystemConfig>('get',
      `${this.byBrandFetchSpotlightDataUrl}/campaignId/${campaignId}/spotlight-data/${eventId}`, {});
  }
}
