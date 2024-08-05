import {
  of as observableOf,
  forkJoin as observableForkJoin,
  Observable,
  Observer,
  throwError,
  defer,
  from
} from 'rxjs';
import { catchError, map, concatMap, switchMap, mergeMap, retryWhen, take } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders, HttpResponse } from '@angular/common/http';
import * as _ from 'underscore';
import { UserService } from '@core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';
import {
  IIGameMediaModel,
  IIGameMediaDesktopPropsModel,
  IIGameMediaDimensionsModel,
  IIGameMediaStream,
  IIGameMediaStreamQualities,
  IStream, IStreamData, IIGameMediaOptHeaders,IStreamReplayUrls
} from './i-gameMedia.model';
import { DeviceService } from '@core/services/device/device.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISystemConfig } from '@core/services/cms/models/system-config';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IStreamProvidersResponse, IPerformGroupConfig } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { IConstant } from '@core/services/models/constant.model';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { CommandService } from '@app/core/services/communication/command/command.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { IAnalyticsParams } from '@lazy-modules/awsFirehose/model/analytics-params.model';

@Injectable({ providedIn: 'root' })
export class IGameMediaService {

  private readonly STREAM_QUALITIES: IIGameMediaStreamQualities = {
    mobile: ['HLS-LOW'],
    wrapper: ['HLS-LOW-RAW'],
    tablet: ['HLS-HIGH', 'HLS-LOW'],
    desktop: ['HLS-WEB', 'DASH', 'RTMP-HIGH']
  };

  private readonly AUTH_ERROR_CODE = 1403;

  constructor(
    private http: HttpClient,
    private user: UserService,
    private device: DeviceService,
    private cmsService: CmsService,
    private asyncScriptLoaderService: AsyncScriptLoaderService,
    private windowRef: WindowRefService,
    private watchRulesService: WatchRulesService,
    private awsService: AWSFirehoseService,
    private commandService: CommandService
  ) {
  }

  /**
   * Get iGameMedia stream if mapped for requested event,
   * otherwise will return all other mapped stream providers with specified priority
   *
   * @params {ISportEvent} eventEntity data of the sport event
   * @params {IIGameMediaOptHeaders} optionalHeaders
   * @throws error during the HTTP request
   * @returns {IIGameMediaModel}
   */
  getStreamsForEvent(eventEntity: ISportEvent, optionalHeaders?: IIGameMediaOptHeaders): Observable<IIGameMediaModel> {
    const IG_MEDIA_ENDPOINT: string = environment.IG_MEDIA_ENDPOINT;
    const IG_MEDIA_TOTE_ENDPOINT: string = environment.IG_MEDIA_TOTE_ENDPOINT;

    const toteIGameMedia = eventEntity.categoryName === 'INTERNATIONAL_TOTE' && eventEntity.streamProviders.iGameMedia;
    const url = toteIGameMedia ? IG_MEDIA_TOTE_ENDPOINT : IG_MEDIA_ENDPOINT;

    return defer(() => {
      const headers: HttpHeaders = new HttpHeaders(_.extend({
        user: this.user.username,
        token: this.user.bppToken
      }, optionalHeaders));
      const queryParams = new HttpParams()
        .append('device', `${this.device.performProviderIsMobile() ? 'mobile' : 'desktop'}`);
      return this.http.get(`${url}/${eventEntity.id}`, {
        observe: 'response',
        params: queryParams,
        headers: headers
      }).pipe(
        map((data: HttpResponse<IConstant>) => {
          if (this.isAuthError(data)) {
            throw data;
          }
          const trackingData = {
            providerName: data.body.priorityProviderName,
            response: data.body
          };
          this.sendAwsData('getVideoStreamingSuccess', eventEntity, trackingData);

          this.processProviderConfig(data.body);

          return data.body;
        }),
        catchError((error: IConstant) => {
          const trackingData = {
            errorPayload: error
          };
          this.sendAwsData('getVideoStreamingError', eventEntity, trackingData);
          return throwError(error);
        }));
    }).pipe(
      retryWhen((errors: Observable<IConstant>) =>
        errors.pipe(
          take(2), // request will be retried only once - the second error will cancel flow
          mergeMap((error: IConstant) => {
            return this.isAuthError(error) ?
              from(this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE))
              : throwError(error);
          })
        )
      )
    );
  }

  /**
   * Get stream for event
   *
   * @param {ISportEvent} eventEntity
   * @param {IStreamProvidersResponse} providerInfo
   * @returns {Promise.<Object>} streamData
   */
  getStream(eventEntity: ISportEvent, providerInfo?: IStreamProvidersResponse, isStreamBet?: boolean): any {
    return this.cmsService.getSystemConfig().pipe(
      switchMap((config: ISystemConfig) => {
        const IGMOneLinkEnabled = (this.device.isWrapper && config && config.FeatureToggle && config.FeatureToggle.IGMOneLink) || isStreamBet;

        return observableForkJoin(
          this.isLoggedIn(),
          this.isEventFinished(eventEntity),
          this.getStreamsList(eventEntity, IGMOneLinkEnabled, providerInfo),
        ).pipe(
          concatMap((val) => this.filterStartedStreams((val[2] as IIGameMediaModel))),
          concatMap((val) => this.chooseStreamQuality(val, IGMOneLinkEnabled)),
          concatMap((val) => this.isStreamAvailable(eventEntity, val)),
          concatMap((val) => this.checkCanWatch(eventEntity, val))
        );
      }));
  }

  /**
   * Replaces '&amp;' to '&' globally in link
   *
   * @param {String} url
   * @returns {string}
   */
  replaceAmps(url: string): string {
    return url.replace(/&amp;/g, '&');
  }

  /**
   * Calculates iFrame height based on height/width proportion and iFrame parent container width!
   *
   * @param desktop {IIGameMediaDesktopPropsModel}
   * @param elementWidth {Number}
   * @param streamData {Object} with stream properties
   * @returns {IIGameMediaDimensionsModel}
   */
  getIFrameDimensions(desktop: IIGameMediaDesktopPropsModel, elementWidth: number, streamData): IIGameMediaDimensionsModel {
    return desktop.isDesktop ? desktop.videoDimensions : this.mobileDimensions(elementWidth, streamData);
  }

  /**
   * Send information to AWS Firehose
   *
   * @param pageActionName
   * @param {ISportEvent} eventEntity
   * @param {IConstant} trackingData
   * @returns void
   * @private
   */
  private sendAwsData(pageActionName, eventEntity: ISportEvent, trackingData: IConstant): void {
    const awsObject: IAnalyticsParams = {
      bppToken: this.user.bppToken.substr(0, 7),
      userBalance: this.user.sportBalance,
      eventId: eventEntity.id
    };
    this.awsService.addAction(pageActionName, Object.assign(awsObject, trackingData));
  }

  /**
   * Compute dimensions according to the element
   *
   * @param {number} elementWidth
   * @param streamData
   * @returns {IIGameMediaDimensionsModel}
   * @private
   */
  private mobileDimensions(elementWidth: number, streamData): IIGameMediaDimensionsModel {
    const proportion = Number((streamData.streamHeight / streamData.streamWidth).toFixed(2));

    return {
      width: '100%',
      height: parseFloat((elementWidth * proportion).toFixed(1))
    };
  }

  /**
   * Check user status
   *
   * @throws {string} error 'onlyLoginRequired'
   * @returns {Observable<boolean>}
   * @private
   */
  private isLoggedIn(): Observable<boolean> {
    return !this.user.status ? throwError('onlyLoginRequired') : observableOf(true);
  }

  /**
   * Check if the event has been finished
   *
   * @param {ISportEvent} eventEntity
   * @throws {string} error 'eventFinished'
   * @returns {Observable<boolean>}
   * @private
   */
  private isEventFinished(eventEntity: ISportEvent): Observable<boolean> {
    return eventEntity.isFinished ? throwError('eventFinished') : observableOf(false);
  }

  /**
   * Check stream availability
   *
   * @param {ISportEvent} eventEntity
   * @param stream
   * @throws {string} error 'streamIsNotAvailable' or 'eventNotStarted'
   * @returns {Observable<IIGameMediaStream>}
   * @private
   */
  private isStreamAvailable(eventEntity: ISportEvent, stream: any): Observable<IIGameMediaStream> {
    if (stream) {
      return observableOf(stream);
    }

    return throwError(this.isEventStarted(eventEntity) ? 'streamIsNotAvailable' : 'eventNotStarted');
  }

  /**
   * Gets stream list for event
   *
   * @param {ISportEvent} eventEntity
   * @param {boolean} IGMOneLinkEnabled
   * @param {IStreamProvidersResponse} providerInfo
   * @throws {string} error 'serverError'
   * @returns {Observable<IIGameMediaModel | IStreamData | number>}
   * @private
   */
  private getStreamsList(eventEntity: ISportEvent, IGMOneLinkEnabled: boolean,
                         providerInfo?: IStreamProvidersResponse): Observable<IIGameMediaModel | IStreamData | number> {
    let streamObservable;

    if (IGMOneLinkEnabled) {
      streamObservable = this.getNativeStreams(eventEntity);
    } else {
      streamObservable = providerInfo ? observableOf(providerInfo) : this.getStreamsForEvent(eventEntity);
    }

    return streamObservable.pipe(catchError(() => {
      return throwError('serverError');
    }));
  }

  /**
   * Get stream data
   *
   * @params {ISportEvent} eventEntity
   * @throws {string} error 'streamIsNotAvailable'
   * @returns {Observable<number | IStreamData>}
   * @private
   */
  private getNativeStreams(eventEntity: ISportEvent): Observable<number | IStreamData> {
    return this.getNativeIGMStreamForEvent(eventEntity).pipe(
      concatMap(streamData => {
        return this.decodeStreamLink(streamData);
      }),
      map((result) => {
        if (result === -1) {
          throwError('streamIsNotAvailable');
        }
        return result;
      }));
  }

  /**
   * Request IGM stream link with special encoded value for Native app
   *
   * @param {ISportEvent} params
   * @returns {Observable<IIGameMediaModel>}
   * @private
   */
  private getNativeIGMStreamForEvent(params: ISportEvent): Observable<IIGameMediaModel> {
    // ViewType: 'RAW' - flag for microservice to request stream link with special encoded value
    const headers = {
      ViewType: 'RAW'
    };

    return this.loadIGMStreamService().pipe(
      concatMap(() => {
        return this.getStreamsForEvent(params, headers);
      }));
  }

  /**
   * Load IGM streamservice.js library on demand
   *
   * @throws {string} error 'IGM streamservice.js not available'
   * @returns {Observable<string>}
   * @private
   */
  private loadIGMStreamService(): Observable<string> {
    return this.asyncScriptLoaderService.loadJsFile(environment.IGM_STREAM_SERVICE_ENDPOINT).pipe(
      catchError(() => throwError('IGM streamservice.js not available')));
  }

  /**
   * Decode IGM stream URL with IGM library streamservice.js
   *
   * @params {IIGameMediaModel} streamData
   * @throws {streamData} error
   * @returns {Observable<IIGameMediaModel | number>}
   * @private
   */
  private decodeStreamLink(streamData: IIGameMediaModel): Observable<IIGameMediaModel | number> {
    if (this.windowRef.nativeWindow.igm && streamData && streamData.streams && streamData.streams.length) {
      return Observable.create((observer: Observer<IIGameMediaModel>) => {
        Promise.all(_.map(streamData.streams, (stream: IStream) => {
          return stream.streamLink ? this.windowRef.nativeWindow.igm.getStreamUrl(stream.streamLink) : Promise.resolve();
        })).then((resp) => {
          _.each(streamData.streams, (stream, index) => {
            if (stream.streamLink && resp[index]) {
              stream.streamLink = resp[index];
            }
          });
          observer.next(streamData);
          observer.complete();
        }, () => {
          observer.error(streamData);
          observer.complete();
        });
      });
    } else if (streamData && streamData.details) {
      return observableOf(streamData);
    } else {
      return observableOf(-1);
    }
  }

  /**
   * Filter streams
   *
   * @param {IIGameMediaModel} response
   * @returns {Observable<IIGameMediaStream[] | IIGameMediaModel>}
   * @private
   */
  private filterStartedStreams(response: IIGameMediaModel): Observable<IIGameMediaStream[] | IIGameMediaModel> {
    if (response.streams) {
      return observableOf(_.where(response.streams, {eventStatusCode: 'O'}) || []);
    }

    return observableOf(response);
  }

  /**
   * Choose the quality of the stream
   *
   * @param {IIGameMediaModel | IIGameMediaStream[]} streamsList
   * @param {boolean} IGMOneLinkEnabled
   * @throws {string} error 'streamIsNotAvailable'
   * @returns {Observable<IIGameMediaStream | IIGameMediaModel>}
   * @private
   */
  private chooseStreamQuality(streamsList: IIGameMediaModel | IIGameMediaStream[], IGMOneLinkEnabled: boolean):
    Observable<IIGameMediaStream | IIGameMediaModel> {
    if ((streamsList as IIGameMediaModel).details) {
      return observableOf(streamsList as IIGameMediaModel);
    }
    const streamQualities = this.deviceQualities(IGMOneLinkEnabled),
      quality = this.preferredQuality(streamQualities, (streamsList as IIGameMediaStream[]));

    // if there is no streamQualities, it means that device was not recognized and stream isn't available
    return _.isEmpty(streamQualities) ? throwError('streamIsNotAvailable') : observableOf(quality);
  }

  /**
   * Choose stream quality (wrapper works only with 'HLS-LOW-RAW')
   *
   * @param IGMOneLinkEnabled {boolean} IGM service is enable
   * @returns {string[]} qualities
   * @private
   */
  private deviceQualities(IGMOneLinkEnabled: boolean): string[] {
    if (IGMOneLinkEnabled) {
      return this.STREAM_QUALITIES.wrapper;
    }
    return this.STREAM_QUALITIES[this.device.strictViewType] || [];
  }

  /**
   *
   * @param {string[]} streamQualities
   * @param {IIGameMediaStream[]} streamsList
   * @returns {IIGameMediaStream}
   * @private
   */
  private preferredQuality(streamQualities: string[], streamsList: IIGameMediaStream[]): IIGameMediaStream {
    let chosenQuality;
    for (let i = 0; i < streamQualities.length; i++) {
      const quality = this.quality(streamQualities[i], streamsList);
      if (quality) {
        chosenQuality = quality;
        break;
      }
    }
    return chosenQuality;
  }

  /**
   *
   * @param {string} uniqueStreamName
   * @param {IIGameMediaStream[]} streamsList
   * @returns {IIGameMediaStream}
   * @private
   */
  private quality(uniqueStreamName: string, streamsList: IIGameMediaStream[]): IIGameMediaStream {
    return _.findWhere(streamsList, { uniqueStreamName });
  }

  /**
   * Check stream availability for watching
   *
   * @param {ISportEvent} eventEntity
   * @param {IIGameMediaStream | IIGameMediaModel} streamsList
   * @throws {string} error or 'deniedByWatchRules' from watchRulesService, 'deniedByWatchRules', 'streamIsNotAvailable'
   * @returns {Observable<IIGameMediaStream | IIGameMediaModel>}
   * @private
   */
  private checkCanWatch(eventEntity: ISportEvent, streamsList: IIGameMediaStream | IStreamProvidersResponse):
    Observable<IIGameMediaStream | IIGameMediaModel> {
    // For tote streams watch rules should be checked
    if (eventEntity.categoryName === 'INTERNATIONAL_TOTE') {
      // @ts-ignore
      return this.watchRulesService.canWatchEvent(streamsList, eventEntity.categoryId, eventEntity.id);
    }

    if ((streamsList as IIGameMediaModel).streams) {
        return observableOf(streamsList as IIGameMediaModel);
    } else if ((streamsList as IIGameMediaModel).details) {
      const failureReason = this.watchRulesService.getFailureReason((streamsList as IIGameMediaModel).details.failureCode);
      this.watchRulesService.sendAwsData(eventEntity.id, (streamsList as IIGameMediaModel).details.failureCode, failureReason);

      return throwError(failureReason);
    }
    return observableOf(streamsList as IIGameMediaStream);
  }

  /**
   * Check if event is started
   *
   * @param eventEntity
   * @returns {boolean}
   * @private
   */
  isEventStarted(eventEntity: ISportEvent): boolean {
    const startTime = new Date(eventEntity.startTime);
    const currentTime = new Date(new Date().getTime());

    return startTime < currentTime;
  }

  private isAuthError(data: IConstant): boolean {
    return data && data.body && data.body.code && data.body.code === this.AUTH_ERROR_CODE;
  }

  private processProviderConfig(data: IIGameMediaModel): void {
    if (data.priorityProviderName === 'Perform') {
      const meta = data.meta as IPerformGroupConfig;
      meta.CSBIframeEnabled = meta['csbIframeEnabled'];
      meta.CSBIframeSportIds = meta['csbIframeSportIds'];
    }
  }
  public getHRReplayStreamUrls(eventId:number): Observable<IStreamReplayUrls>{   
    const body = {
      user: this.user.username,
      token: this.user.bppToken,
      eventId:eventId,
      device:`${this.device.performProviderIsMobile() ? 'mobile' : 'desktop'}`
    };
    const url = `${environment.OPT_IN_ENDPOINT}/api/video/vod`;   
    return this.http.post<any>(url, body);    
  }
}
