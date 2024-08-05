
import { throwError as observableThrowError,  Observable ,  Observer } from 'rxjs';

import { map, concatMap } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import * as md5 from 'blueimp-md5';

import {
  IAtrStreamModel,
  IAtrRequestParamsModel,
  IAtrResponseModel
} from './at-the-races.models';
import { UserService } from '@core/services/user/user.service';
import { TimeService } from '@core/services/time/time.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IStreamProvider, IStreamProvidersResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import environment from '@environment/oxygenEnvConfig';
import { DeviceService } from '@core/services/device/device.service';

@Injectable({ providedIn: 'root' })
export class AtTheRacesService {

  private partnerCode: string;
  private secretKey: string;
  private readonly EVENT_TYPE = 'L';

  constructor(
    private http: HttpClient,
    private timeService: TimeService,
    private user: UserService,
    private device: DeviceService,
  ) {}

  setConfigParams(atrPartnerCode: string, atrSectetKey: string): void {
    this.partnerCode = atrPartnerCode;
    this.secretKey = atrSectetKey;
  }

  isEventStarted(eventEntity: ISportEvent): boolean {
    const startTime = new Date(eventEntity.startTime);
    const currentTime = new Date(new Date().getTime() + this.timeService.fiveMinutsInMiliseonds);

    return startTime < currentTime;
  }

  getVideoUrl(providerInfo: IStreamProvidersResponse): Observable<string> {
    return this.getStreamUrl(providerInfo).pipe(concatMap((response) => {
      return this.parseStreamResponse(response);
    }));
  }

  private getStreamUrl(providerInfo: IStreamProvidersResponse): Observable<IAtrResponseModel> {
    const atrEventid = this.getATREventId(providerInfo);
    const isDesktop = this.device.isDesktop;
    const isDesktopSafari = this.device.isDesktopSafari;
    const partnerCode = this.partnerCode;
    let key: string;

    if (atrEventid) {
      key = this.createAccessKey(atrEventid);

      return this.getATRStriaminUrls({
        eventId: atrEventid,
        userId: this.userId,
        key,
        partnerCode,
        mediaFormat: (isDesktop && !isDesktopSafari) ? 'FLV' : 'HLS'
      });
    } else {
      return observableThrowError('servicesCrashed');
    }
  }

  private parseStreamResponse(response: IAtrResponseModel): Observable<string> {
    const errorCodesMap = {
      EVENT_OVER: 'eventFinished',
      EVENT_NOT_STARTED: 'eventNotStarted',
      USAGE_LIMITS_BREACHED: 'usageLimitsBreached'
    };

    return Observable.create((observer: Observer<string>) => {
      if (response.Error && !response.IsOK) {
        if (errorCodesMap[response.Error.ErrorCode]) {
          observer.error(errorCodesMap[response.Error.ErrorCode]);
        } else {
          observer.error('servicesCrashed');
        }
      } else {
        if (response.EventInfo && response.EventInfo.Streams && response.EventInfo.Streams.length > 0) {
          const stream = this.getAtrStream(response.EventInfo.Streams);

          if (stream.Url) {
            observer.next(stream.Url);
          } else {
            observer.error('servicesCrashed');
          }
        } else {
          observer.error('servicesCrashed');
        }
      }
      observer.complete();
    });
  }

  private get userId(): string {
    return this.user.username;
  }
  private set userId(value:string){}

  private getAtrStream(streams): IAtrStreamModel {
    let stream: IAtrStreamModel = _.findWhere(streams, { BitrateLevel: 'Adaptive' });

    if (!stream) {
      stream = _.findWhere(streams, { BitrateLevel: 'High' });
    }

    if (!stream) {
      stream = _.findWhere(streams, { BitrateLevel: 'Medium' });
    }

    if (!stream) {
      stream = _.findWhere(streams, { BitrateLevel: 'Low' });
    }

    if (!stream) {
      stream = streams[0];
    }

    return stream;
  }

  private getATREventId(response: IStreamProvidersResponse): string {
    let eventId: string;

    if (response.SSResponse && response.SSResponse.children) {
      _.each(response.SSResponse.children, (provider) => {
        if (provider.mediaProvider && provider.mediaProvider.name === 'At The Races') {
          _.each(provider.mediaProvider.children, (media) => {
            eventId = this.getEventId(media);
          });
        }
      });
    } else {
      _.each(response.listOfMediaProviders, (provider) => {
        if (provider.children.length > 0) {
          _.each(provider.children, (media) => {
            eventId = this.getEventId(media);
          });
        }
      });
    }

    return eventId;
  }

  /**
   * Get Event id
   * @param {IStreamProvider} media
   */
  private getEventId(media: IStreamProvider): string {
    if (media.media && media.media.accessProperties && media.media.accessProperties.length > 0) {
      const accessProperty = media.media.accessProperties;
      return accessProperty.substring(accessProperty.indexOf(':') + 1);
    }
    return '';
  }

  private createAccessKey(atrEventId: string): string {
    const hashSeparator = ':',
        stringWhichNeedToBeHashed = this.partnerCode + hashSeparator + atrEventId + hashSeparator +
          this.EVENT_TYPE + hashSeparator + this.userId + hashSeparator + this.secretKey;

      return md5(stringWhichNeedToBeHashed);
  }

  private getATRStriaminUrls(params: IAtrRequestParamsModel): Observable<IAtrResponseModel> {
    const endpointUrl: string = `${environment.ATR_END_POINT}/GetStreamingURLs?outputMode=basic&format=json` +
      `&MediaFormat=${params.mediaFormat}` +
      `&EventId=${params.eventId}` +
      `&UserID=${params.userId}` +
      `&PartnerCode=${params.partnerCode}` +
      `&key=${params.key}`;

    return this.http.get<IAtrResponseModel>(endpointUrl, {
      observe: 'response'
    }).pipe(map((data: HttpResponse<IAtrResponseModel>) => {
      return data.body;
    }));
  }
}
