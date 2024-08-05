
import { of as observableOf,  Observable, throwError } from 'rxjs';
import { map, concatMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import * as md5 from 'blueimp-md5';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { TimeService } from '@core/services/time/time.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { IStreamProvidersResponse, IStreamProvider } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IImgQueryParams, IImgServerData, IStreamingUrlResponse } from '@lazy-modules/eventVideoStream/services/imgService/img.model';

@Injectable({ providedIn: 'root' })
export class ImgService {
  private IMGOperatorId;
  private IMGSecretKey;
  private IMGEventId;

  constructor(
    private http: HttpClient,
    private timeService: TimeService,
    private timeSyncService: TimeSyncService
  ) { }

  /**
   * Initialize img class with configuration defined on cms part.
   *
   * @param operatorId - img operator id config
   * @param secret - secret key of img streaming config
   */
  setConfigParams(operatorId: string, secret: string): void {
    this.IMGOperatorId = operatorId;
    this.IMGSecretKey = secret;
  }

  /**
   * Determine if event is started according to img logic
   *
   * @param eventEntity an event instance
   * @returns the event started or no
   */
  isEventStarted(eventEntity: ISportEvent): boolean {
    const startTime = new Date(eventEntity.startTime),
      currentTime = new Date(new Date().getTime() + this.timeService.fiveMinutsInMiliseonds);

    return startTime < currentTime;
  }

  /**
   * Encrypt IMG auth information
   *
   * @param providerInfo information about a streaming provider
   * @returns the streaming url as observable
   */
   getVideoUrl(providerInfo: IStreamProvidersResponse): Observable<string> {
    return this.getIMGEventId(providerInfo).pipe(
      concatMap(() => {
        return this.timeSyncService.getUserSessionTime(true, false);
      }), concatMap((data) => {
        return this.prepareQueryParams(data);
      }), concatMap((queryParams) => {
        return this.getIMGStreamingUrls(queryParams);
      }));
  }

  /**
   * Gets img event id
   *
   * @param response information about a streaming provider
   * @returns the event id as observable or throw error
   */
   private getIMGEventId(response: IStreamProvidersResponse): Observable<string> {
    let eventId: string;

    if (response.SSResponse && response.SSResponse.children) {
      _.each(response.SSResponse.children, provider => {
        if (provider.mediaProvider && provider.mediaProvider.name === 'IMG Video Streaming') {
          eventId = this.getEventId(provider.mediaProvider.children);
        }
      });
    } else {
      _.each(response.listOfMediaProviders, provider => {
        if (provider.children.length) {
          eventId = this.getEventId(provider.children);
        }
      });
    }

    if (eventId) {
      this.IMGEventId = eventId;
      return observableOf(eventId);
    } else {
      return throwError('servicesCrashed');
    }
  }

  /**
   * Find and prepare event id
   *
   * @param childs a data array of streaming provider;
   * @returns the event id or undefined
   */
  private getEventId(childs: IStreamProvider[]): string {
    let eventId: string;
    _.each(childs, media => {
      if (media.media && media.media.accessProperties && media.media.accessProperties.length > 0) {
        const accessProperty = media.media.accessProperties;

        eventId = accessProperty.substring(accessProperty.indexOf(':') + 1);
      }
    });
    return eventId;
  }

  /**
   * Prepare data for authentication.
   *
   * @param serverData - serverIpData and serverTimestampObj.
   * @returns a set of params
   */
  private prepareQueryParams(serverData: IImgServerData): Observable<IImgQueryParams> {
    const timestamp = serverData.timestamp,
      userIP = serverData['x-forward-for'],
      accessString = `${this.IMGSecretKey}:${userIP}:${timestamp}`;

    return observableOf({
      eventId: this.IMGEventId,
      operatorId: this.IMGOperatorId,
      auth: md5(accessString, this.IMGSecretKey),
      timeStamp: timestamp
    });
  }

  /**
   * Generate a streaming URL according to parameters
   *
   * @param queryParams params for URL generating
   * @returns HLS URL as observable
   */
  private getIMGStreamingUrls(queryParams: IImgQueryParams): Observable<string> {
    const endpointUrl = `${environment.IMG_END_POINT}/events/${queryParams.eventId}/stream?` +
    `operatorId=${queryParams.operatorId}&auth=${queryParams.auth}&timestamp=${queryParams.timeStamp}&page.page=2&page.size=1`;
    return this.http.get(endpointUrl, {
      observe: 'response'
    }).pipe(map((response: HttpResponse<IStreamingUrlResponse>) => {
      const hlsUrl = response && response.body.hlsUrl;
      return hlsUrl;
    }));
  }
}
