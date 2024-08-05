import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as xml2js from 'xml2js';

import environment from '@environment/oxygenEnvConfig';

import { DeviceService } from '@core/services/device/device.service';
import {
  IPerformGroupParams,
  IPerformIframeDimensions, IStreamRequestParams,
  IStreamResponse
} from '@lazy-modules/eventVideoStream/models/video-stream.model';

@Injectable({ providedIn: 'root' })
export class PerformGroupProviderService {

  constructor(
    private http: HttpClient,
    private deviceService: DeviceService
  ) {}

  addPerformUserToPull(requestParams: IPerformGroupParams): Observable<string> {
    const { userId, partnerId, eventId, key } = requestParams;
    const baseUrl = this.deviceService.performProviderIsMobile() ?
                      environment.PERFORM_GROUP_END_POINT : environment.PERFORM_GROUP_END_POINT_DESKTOP;
    const queryString = `userId=${userId}&partnerId=${partnerId}&eventId=${eventId}&key=${key}`;
    const endpointUrl = `${baseUrl}/validation/addUser/index.html?${queryString}`;

    return this.http.get<any>(endpointUrl, { responseType: 'text' as 'json'}).pipe(
      map((response: string) => {
        return response;
      }));
  }

  getNativeUrls(requestParams: IPerformGroupParams): Observable<IStreamResponse> {
    const { baseUrl, queryString } = this.generateRequestParams(requestParams);
    const endpointUrl: string = `${baseUrl}/wab/multiformat/index.html?${queryString}`;

    return this.http.get<any>(endpointUrl, { responseType: 'text' as 'json' }).pipe(  // type issue in angular get method description.
      map((response: string) => {
        let result: string = response;

        xml2js.parseString(response, (err, parseResult) => {
          if (!err) {
            result = parseResult;
          }
        });

        return result;
      }));
  }

  getNativeCSBUrl(requestParams: IPerformGroupParams, iframeDimensions?: IPerformIframeDimensions): string {
    const { baseUrl, queryString } = this.generateRequestParams(requestParams);
    const clearUrl: string = `${baseUrl}/watch/event/index.html?${queryString}&rmg=true`;

    if (iframeDimensions) {
      const { width, height } = iframeDimensions;
      return clearUrl.concat(`&width=${width}&height=${height}`);
    }

    return clearUrl;
  }

  private generateRequestParams(requestParams: IPerformGroupParams): IStreamRequestParams {
    const queries: string[] = ['userId', 'partnerId', 'eventId', 'key'];

    const baseUrl: string = this.deviceService.performProviderIsMobile()
      ? environment.PERFORM_GROUP_END_POINT
      : environment.PERFORM_GROUP_END_POINT_DESKTOP;

    const queryString: string = queries.reduce((acc: string, query: string) => requestParams[query]
      ? acc.concat(`${acc.length > 0 ? '&' : ''}${query}=${requestParams[query]}`)
      : acc, '');
    return { baseUrl, queryString };
  }
}
