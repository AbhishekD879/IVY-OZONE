import { of as observableOf, throwError, Observable } from 'rxjs';
import { Injectable } from '@angular/core';

import environment from '@environment/oxygenEnvConfig';

import { ISportEvent } from '@core/models/sport-event.model';
import { IGM_CONSTANT } from '@lazy-modules/eventVideoStream/constants/iGameMedia';
import {
  IPerformGroupConfig,
  IStreamProvidersResponse
} from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { IIGameMediaStream } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({ providedIn: 'root' })
export class WatchRulesService {
  private readonly SPORTS_WITH_WATCH_RULES: any = environment.EVENT_CATEGORIES_WITH_WATCH_RULES;

  constructor(
    private awsService: AWSFirehoseService
  ) {}

  /**
   * Checks if user can watch event.
   * User can watch this event in case he has put a bet atleast 1 pound
   * @params providerInfo (IStreamProviderResponse or IGameMediaStream(only IGM stream)
   */
  canWatchEvent(providerInfo: IStreamProvidersResponse | IIGameMediaStream, categoryId: string, eventId: number):
    Observable<IStreamProvidersResponse | IIGameMediaStream>  {
      if (this.SPORTS_WITH_WATCH_RULES.indexOf(categoryId) !== -1) {
        if ((providerInfo as IStreamProvidersResponse).priorityProviderName || (providerInfo as IIGameMediaStream).streamLink) {
          return observableOf(providerInfo);
        }
        const failureCode: string = (providerInfo as IStreamProvidersResponse).details &&
          (providerInfo as IStreamProvidersResponse).details.failureCode,
          failureReason = this.getFailureReason(failureCode);
        this.sendAwsData(eventId, failureCode, failureReason);
        return throwError(failureReason);
      }
      return observableOf(null);
}

  /**
   * Check if user is inactive(valid only for racing when optIn MS returns qualification error code 4105)
   * @param errorCode
   */
  isInactiveUser(errorCode: string): boolean {
    return errorCode === 'deniedByInactiveWatchRules';
  }

  shouldShowCSBIframe(eventEntity: ISportEvent, performConfig: IPerformGroupConfig): boolean {
    return (eventEntity.streamProviders.Perform || eventEntity.streamProviders.RacingUK)
      && performConfig
      && performConfig.CSBIframeEnabled
      && performConfig.CSBIframeSportIds
      && String(performConfig.CSBIframeSportIds).split(',').includes(eventEntity.sportId);
  }

  /**
   * Get failure code to display proper message for user
   * @param failureCode
   */
  getFailureReason(failureCode: string): string {
    if (failureCode && IGM_CONSTANT.FAILURE_ERROR.indexOf(failureCode) > -1) {
      return 'deniedByWatchRules';
    } else if (failureCode && IGM_CONSTANT.INACTIVE_ERROR.indexOf(failureCode) > -1) {
      return 'deniedByInactiveWatchRules';
    }

    return 'streamIsNotAvailable';
  }

  /**
   * Send AWS Firehose data
   * @param eventId
   * @param errorCode
   * @param errorMsgCode
   * @returns void
   */
  sendAwsData(eventId: number, errorCode: string, errorMsgCode: string): void {
    const awsParams = {
      eventId,
      qualificationErrorCode: errorCode,
      errorMessageCode: errorMsgCode
    };
    this.awsService.addAction('STREAM_QUALIFICATION_ERROR', awsParams);
  }
}
