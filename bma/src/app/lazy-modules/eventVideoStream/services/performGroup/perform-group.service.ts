import { Observable, throwError } from 'rxjs';
import { ElementRef, Injectable } from '@angular/core';
import { catchError, map } from 'rxjs/operators';
import * as _ from 'underscore';
import * as md5 from 'blueimp-md5';

import { UserService } from '@core/services/user/user.service';
import { TimeService } from '@core/services/time/time.service';
import { IStreamProvidersResponse, IStreamProvider,
  IPerformGroupConfig } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PerformGroupProviderService } from '@lazy-modules/eventVideoStream/services/performGroup/perform-group.provider.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({ providedIn: 'root' })
export class PerformGroupService {

  constructor(
    private userService: UserService,
    private timeService: TimeService,
    private performGroupProviderService: PerformGroupProviderService,
    private domToolsService: DomToolsService,
    private awsService: AWSFirehoseService
  ) {
  }

  /**
   * Check if event started
   *
   * return {boolean}
   */
  isEventStarted(event: ISportEvent): boolean {
    const startTime = this.getTime(event.startTime),
      currentTime = new Date(new Date().getTime() + this.timeService.additionalTimeForSteamStartEnd);

    return startTime < currentTime;
  }

  isPerformStreamStarted(event: ISportEvent): boolean {
    const startTime = this.getTime(event.startTime);
    const dayBefore8pm = new Date(startTime.getTime() - this.timeService.oneDayInMiliseconds).setUTCHours(20, 0, 0);
    const currentTime = this.timeService.getCurrentTime();

    return currentTime >= dayBefore8pm;
  }

  /**
   * Gets Perform group id by coral id
   * @param {IStreamProvidersResponse} providerInfo
   * @param config
   * @param eventId
   * @return {Observable<any>}
   */
  performGroupId(providerInfo: IStreamProvidersResponse, config: IPerformGroupConfig, eventId: number): Observable<string> {
    const performGroupId = this.getPerformGroupId(providerInfo);
    const key = this.generateMD5(performGroupId, config);

    if (performGroupId && this.isNormalInteger(performGroupId)) {
      return this.performGroupProviderService.addPerformUserToPull({
        key,
        userId: this.userService.username,
        partnerId: config.partnerId,
        eventId: performGroupId
      }).pipe(map((responseData: string) => {
          const response = _.reduce(responseData, (predicate, value) => {
            return _.isString(value) ? predicate.concat(value) : predicate;
          }, '');

          if (response.indexOf('success') !== -1) {
            return performGroupId;
          } else {
            this.sendAwsData(eventId, performGroupId, response);
            console.error(response, 'Application was not able to validate user on perform side.');
            return '';
          }
        }), catchError(() => {
          this.sendAwsData(eventId, performGroupId);
          return throwError('servicesCrashed');
        }));
    } else if (!this.isNormalInteger(performGroupId)) {
      // Reject promise with error which is set in perform group
      return throwError(performGroupId);
    }
  }

  /**
   * Gets perform group id
   *
   * @param providerInfo - original response from data provider
   * @return {number} performEventid - perform group id of this event
   */
  getPerformGroupId(providerInfo: IStreamProvidersResponse): string {
    let performGroupString;

    if (providerInfo.SSResponse && providerInfo.SSResponse.children) {
      _.each(providerInfo.SSResponse.children, child => {
        if (child.mediaProvider && child.mediaProvider.children && child.mediaProvider.children.length > 0) {
          _.each(child.mediaProvider.children, mediaChild => {
            performGroupString = this.getPerformGroupString(mediaChild);
          });
        }
      });
    } else {
      _.each(providerInfo.listOfMediaProviders, provider => {
        if (provider.children.length) {
          _.each(provider.children, mediaChild => {
            performGroupString = this.getPerformGroupString(mediaChild);
          });
        }
      });
    }

    if (performGroupString) {
      return performGroupString.substring(performGroupString.indexOf(':') + 1, performGroupString.indexOf(','));
    } else if (!performGroupString) {
      // That mean that event is not mapped
      //
      return 'servicesCrashed';
    }

    return null;
  }

  getElementWidth(elementRef: ElementRef<HTMLElement>): number {
    const element = <HTMLElement>elementRef.nativeElement.parentNode;
    this.domToolsService.css(element, 'display', 'block');

    return this.domToolsService.getWidth(element);
  }

  /**
   * Send AWS Firehose data
   * @param eventId
   * @param performGroupId
   * @param response
   * @returns void
   */
  private sendAwsData(eventId: number, performGroupId: string, response?: string): void {
    const awsParams = {
      eventId,
      performEventId: performGroupId,
      response: response || 'servicesCrashed'
    };
    this.awsService.addAction('STREAM_TOKENISATION_ERROR', awsParams);
  }

  /**
   * Get Perform Group String
   * @param {IStreamProvider} mediaChild
   * @returns {string}
   */
  private getPerformGroupString(mediaChild: IStreamProvider): string {
    if (mediaChild.media && mediaChild.media.accessProperties && mediaChild.media.accessProperties.length) {
      return mediaChild.media.accessProperties;
    }
    return '';
  }

  /**
   * Check if string is proper integer number
   *
   * @param str - string
   */
  private isNormalInteger(str: string): boolean {
    return /^\+?(0|[1-9]\d*)$/.test(str);
  }

  /**
   * Gets time from coral string
   */
  private getTime(dateString: string): Date {
    return new Date(dateString);
  }

  /**
   * Generate md5 string
   */
  private generateMD5(eventId: string, config): string {
    const userId = this.userService.username;
    const partherId = config.partnerId;
    const toEncrypt = `${userId + partherId + eventId}L`;
    const seed = config.seed;
    const md5String = md5(toEncrypt + seed, null, true);
    const base64 = btoa(md5String);

    return encodeURIComponent(base64);
  }
}
