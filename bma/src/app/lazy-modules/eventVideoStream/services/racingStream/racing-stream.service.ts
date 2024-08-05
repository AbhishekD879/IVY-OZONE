
import { of as observableOf, Observable, throwError } from 'rxjs';

import { map, concatMap, catchError } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as md5 from 'blueimp-md5';
import * as _ from 'underscore';
import { DatePipe } from '@angular/common';

import { TimeService } from '@core/services/time/time.service';
import { UserService } from '@core/services/user/user.service';
import {
  IStreamResponse,
  IStreamResponseObject,
  IPerformGroupConfig,
  IStreamProvidersResponse,
  IStreamMediaFormat,
  IPerformIframeDimensions,
  IStreamRequestConfig
} from '@lazy-modules/eventVideoStream/models/video-stream.model';

import { ISportEvent } from '@core/models/sport-event.model';
import { PerformGroupService } from '@lazy-modules/eventVideoStream/services/performGroup/perform-group.service';
import { PerformGroupProviderService } from '@lazy-modules/eventVideoStream/services/performGroup/perform-group.provider.service';

@Injectable({ providedIn: 'root' })
export class RacingStreamService {
  constructor(
    private timeService: TimeService,
    private userService: UserService,
    private performGroupService: PerformGroupService,
    private performGroupProviderService: PerformGroupProviderService,
    private datePipe: DatePipe
  ) {
  }

  /**
   * Checks if event is started
   * @param  {Object} eventEntity
   * @return {Boolean}
   */
  public isEventStarted(eventEntity: ISportEvent): boolean {
    const startTime = new Date(eventEntity.startTime),
      currentTime = new Date(new Date().getTime() + this.timeService.threeMinutsInMiliseonds);

    return startTime < currentTime;
  }

  /**
   * Gets native urls for different devices.
   * @param  {Object} providerInfo - providers info.
   * @param  {Object} config - cms config with params.
   * @param  {Bool} config - is RUK for Connect App.
   * @return {Observable}
   */
  public getVideoUrl(providerInfo: IStreamProvidersResponse,
                     performConfig: IPerformGroupConfig): Observable<string> {
    const {
      performGroupId: eventId,
      key,
      isNormalInteger,
      partnerId,
      userId
    } = this.generateRequestConfig(providerInfo, performConfig);

    if (!isNormalInteger) {
      return throwError(eventId);
    }

    return this.performGroupProviderService.getNativeUrls({ key, userId, partnerId, eventId })
      .pipe(
        concatMap((response: IStreamResponse) => this.parseResponse(response)),
        catchError((reason) => throwError(reason || 'servicesCrashed'))
      );
  }

  /**
   * return url for CSB iframe (perform)
   * @param providerInfo
   * @param performConfig
   * @param iframeSizes
   */
  getVideoCSBUrl(providerInfo: IStreamProvidersResponse,
                 performConfig: IPerformGroupConfig,
                 iframeDimensions?: IPerformIframeDimensions): string {
    const {
      performGroupId: eventId,
      isNormalInteger,
      partnerId,
      userId
    } = this.generateRequestConfig(providerInfo, performConfig, false);

    if (!isNormalInteger) {
      return null;
    }

    return this.performGroupProviderService.getNativeCSBUrl({ userId, partnerId, eventId }, iframeDimensions);
  }

  generateRequestConfig(providerInfo: IStreamProvidersResponse,
                        performConfig: IPerformGroupConfig,
                        generateKey: boolean = true): IStreamRequestConfig {
    const performGroupId: string = this.performGroupService.getPerformGroupId(providerInfo);
    const key: string = generateKey && this.generateKeyURLS(performGroupId, performConfig);
    const isNormalInteger: boolean = this.isNormalInteger(performGroupId);
    const partnerId: string = performConfig.partnerId;

    const userId: string = this.userService.username;

    return { performGroupId, key, isNormalInteger, partnerId, userId };
  }
  /**
   * @param  {string} eventId  cms config
   * @param  {Object} config  cms config
   * @return {String}         Key sting
   */
  generateKeyURLS(eventId: string, config: IPerformGroupConfig): string {
    const userId: string = this.userService.username,
      partherId: string = config.partnerId,
      date: Date = new Date(),
      gmtDate: Date = new Date(date.valueOf() + (date.getTimezoneOffset() * 60000)),
      begin: string = this.datePipe.transform(gmtDate, 'yyyyMMdd'),
      // The problem is that we need time in +1 timezone to pass validation
      hours: string = this.datePipe.transform(gmtDate, 'HH'), // hours      = $filter('date')(gmtDate, 'HH') * 1 + 1,
      toEncrypt: string = `${begin + hours + this.datePipe.transform(gmtDate, 'mm')}_${partherId}_${userId}_${eventId}`,
      seed: string = config.seed,
      md5String: string = md5(toEncrypt + seed, null, true),
      base64: string = btoa(md5String),
      key: string = encodeURIComponent(base64);

    return key;
  }

  /**
   * Reject defer and thorow exception to console.
   * @param  {string} error
   */
  rejectAndThrowError(error: string): Observable<string> {
    console.error('Unhandled response from perform service. No iphonewab or ipnoe or web ' +
      'stream were found, Or service return unexpected response.');
    return throwError(error);
  }

  /**
   * Checks if string is normal integer.
   * @param  {string} str
   * @return {Boolean}
   */
  isNormalInteger(str) {
    return /^\+?(0|[1-9]\d*)$/.test(str);
  }

  /**
   * Parses response from perform.
   * @param  {Object} response - response from perform.
   * @return {Object} - this promise.
   */
  parseResponse(response: IStreamResponse): Observable<string> {
    if (response && _.isString(response)) { // Unhappy path
      return this.parseResponseDataString(response).pipe(
        map(data => data));
    } else if (this.getMediaFormats(response as IStreamResponseObject)) { // Happy path
      return this.parseResponseDataObject(response as IStreamResponseObject).pipe(
        map(data => data));
    } else {
      return this.rejectAndThrowError('servicesCrashed');
    }
  }

  /**
   * @param response
   * @returns IStreamMediaFormat[]
   */
  getMediaFormats(response: IStreamResponseObject): IStreamMediaFormat[] {
    return response &&
      response.eventInfo &&
      response.eventInfo.availableMediaFormats &&
      response.eventInfo.availableMediaFormats[0].mediaFormat;
  }

  /**
   * Parse response if it is string
   * @param response - IStreamResponse
   *
   * @return Observable<string>
   */
  parseResponseDataString(response: IStreamResponse): Observable<string> {
    const respondDataStatuses = ['eventnotstarted', 'eventover', 'geoblocked', 'fairusebreach'];
    const errorMessages = ['eventNotStarted', 'eventFinished', 'geoBlocked', 'fairUseBreach'];
    let errorMessage;

    const foundResponse = _.some(respondDataStatuses, (status, i) => {
      let res = false;
      if ((response as string).indexOf(status) !== -1) {
        errorMessage = errorMessages[i];
        res = true;
      }

      return res;
    });

    if (errorMessage) {
      return this.rejectAndThrowError(errorMessage);
    }

    if (!foundResponse) {
      return this.rejectAndThrowError('servicesCrashed');
    }
  }

  /**
   * Parse response if it is object
   * @param response
   */
  parseResponseDataObject(response: IStreamResponseObject): Observable<string> {
    const mediaFormats = this.getMediaFormats(response);
    const playerAliases = ['iPhonesec', 'iPhonewabsec', 'iPhonewab', 'iPhone', 'iPhone3', 'videomed', 'hlslo', 'hlsmed'];

    let stream;

    _.some(playerAliases, alias => {
      stream = _.find(mediaFormats, (format) => {
        return format.playerAlias.indexOf(alias) > -1;
      });

      return stream;
    });

    if (stream) {
      return observableOf(stream.stream[0].streamLaunchCode[0].trim());
    } else {
      return this.rejectAndThrowError('servicesCrashed');
    }
  }
}
