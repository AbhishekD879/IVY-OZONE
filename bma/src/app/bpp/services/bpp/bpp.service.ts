import { shareReplay, delay, switchMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { Observer, Observable } from 'rxjs';

import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { BppErrorService } from '../bppError/bpp-error.service';
import { BppProvidersService } from '../bppProviders/bpp-providers.service';
import { IErrorResponse } from '../bppError/bpp-error.model';
import { IBppRequest, IBppResponse, IBet, IBetError, ILegPart } from '../bppProviders/bpp-providers.model';
import { IError } from './bpp.model';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { AuthService } from '@authModule/services/auth/auth.service';
import { IConstant } from '@core/services/models/constant.model';
import { ERROR_DICTIONARY } from '@core/constants/error-dictionary.constant';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { IAnalyticsParams } from '@lazy-modules/awsFirehose/model/analytics-params.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Injectable()
export class BppService {

  BPP_RETRY_TIMEOUT: number = 2000;

  private static getDuration(milliseconds): string {
    return (milliseconds / 1000).toFixed(2);
  }

  constructor(
    private authService: AuthService,
    private infoDialogService: InfoDialogService,
    private bppErrorService: BppErrorService,
    private awsService: AWSFirehoseService,
    private bppProviders: BppProvidersService,
    private user: UserService,
    private device: DeviceService,
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private maintenanceService: MaintenanceService,
    private windowRef: WindowRefService
  ) { }

  /**
   * Wrapper for every BPP request
   * @param {string} serviceName // list of possible services could be found in bpp-providers.service.ts
   * @param {object} data // data object to pass in request
   * @return {object} promise(success, error)
   */
  send(serviceName: string, data?: IBppRequest, url?: string): Observable<IBppResponse> {
    const timestamp = Date.now();

    return Observable.create((observer: Observer<IBppResponse>) => {
      if (!this.bppProviders[serviceName]) {
        console.warn(`BPP service with name ${serviceName} does not exist.`);
        observer.error(`BPP service with name ${serviceName} does not exist.`);
        observer.complete();
      } else if (!this.isOnlineOrNot()) {
        this.infoDialogService.openConnectionLostPopup();
        observer.error(ERROR_DICTIONARY.OFFLINE);
        observer.complete();
      } else {
        this.bppProviders[serviceName](data, url).subscribe(
          response => {
            if (response.token) {
              this.user.set({ bppToken: response.token });
            }
            this.pubSubService.publish('BETSLIP_BET_DATA', response);
            this.trackAction('success', serviceName, data, response, timestamp);
                if (response.betError && response.betError[0] && response.betError[0].subErrorCode === 'DUPLICATED_BET') {
                  observer.error('betPlacementTimeoutError');
                  observer.complete();
                  this.implicitBalanceRefresh(serviceName, false);
                  return;
                } else if (response.betError && response.betError[0] && response.betError[0].code === '4016') {
              observer.error(response.betError[0]);
              observer.complete();
              this.implicitBalanceRefresh(serviceName, false);
              return;
            } else if (response.betError && response.betError[0] && response.betError[0].subErrorCode === 'EXTERNAL_FUNDS_UNAVAILABLE') {
              this.retryTrigger(serviceName, data, { data: { status: response.betError[0].subErrorCode } }, observer);
              this.implicitBalanceRefresh(serviceName, false);
            } else {
              observer.next(response);
              observer.complete();
              this.implicitBalanceRefresh(serviceName, true);
            }
          },
            error => {
              this.trackAction('error', serviceName, data, error, timestamp);
              this.retryTrigger(serviceName, data, error, observer);
              this.implicitBalanceRefresh(serviceName, false);
          });
      }
    }).pipe(
      shareReplay(1)
    );
  }

  isOnlineOrNot() {
    let isOnlineFallback: boolean;
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config && config.isOnlineFallback && config.isOnlineFallback.enabled) {
        isOnlineFallback = true;
      }
    });
    if (isOnlineFallback) {
      return this.windowRef.nativeWindow.navigator.onLine;
    } else {
      return this.device.isOnline();
    }
  }

  showErrorPopup(error: IErrorResponse | string): void {
    // Show BPP service error pop-up only for logged in user.
    if (this.user.status && this.device.isOnline()) {
      this.bppErrorService.showPopup(error);
    }
  }

  /**
   * Retry mechanism for BPP
   * @param {string} serviceName // list of possible services could be found in bpp-providers.service.ts
   * @param {object} data // data object to pass in request
   * @return {object} promise(success, error)
   */
  private retry(serviceName: string, data?: IBppRequest): Observable<IBppResponse> {
    return Observable.create((observer: Observer<IBppResponse>) => {
      let timestamp;
      this.authService.reLoginBpp().pipe(
        delay(serviceName === 'placeBet' ? this.BPP_RETRY_TIMEOUT : 0),
        switchMap(() => {
          timestamp = Date.now();
          return this.bppProviders[serviceName](data);
        }),
        delay(this.device.isWrapper ? this.BPP_RETRY_TIMEOUT : 0)
      ).subscribe((result: IBppResponse) => {
        this.trackAction('success', serviceName, data, result, timestamp);
        observer.next(result);
        observer.complete();
      }, err => {
        this.trackAction('error', serviceName, data, err, timestamp);
        observer.error(err);
        observer.complete();
      });
      }).pipe(shareReplay(1));
  }

  /**
   * In case when user receive UNAUTHORIZED_ACCESS/LOGGED_OUT/EXTERNAL_FUNDS_UNAVAILABLE errors
   *  we try to reauthenticate him and make service call again.
   * @param {string} serviceName // list of possible services could be found in bpp-providers.service.ts
   * @param {object} data // data object to pass in request
   * @param {object} error // object with error data
   * @param {object} promise // object with defer promise
   */
  private retryTrigger(serviceName: string, data: IBppRequest, error: IError, observer: Observer<IBppResponse>): void {
    this.awsService.addAction('bppService=>retryTrigger()', { serviceName, data, error });

    if (this.checkLogoutErrorStatus(error)) {
      this.retry(serviceName, data).subscribe(response => {
          observer.next(response);
          observer.complete();
          this.implicitBalanceRefresh(serviceName, true);
        }, err => {
          this.bppErrorService.errorHandler(err);
          observer.error(error);
          observer.complete();
          this.implicitBalanceRefresh(serviceName, false);
        });
    } else {
      observer.error(error);
      observer.complete();

      if (this.isMaintenanceError(error)) {
        this.maintenanceService.checkForMaintenance().subscribe();
      }
    }
  }

  private trackAction(action = '', serviceName = '', request: IBppRequest, response: IConstant, timestamp: number = 0): void {
    const servicesToTrack = ['buildBet', 'buildBetLogged', 'buildComplexLegs'];
    const apiKey = this.awsService.API[`BPP_${serviceName.toUpperCase()}_${action.toUpperCase()}`] || serviceName;
    const duration = BppService.getDuration(Date.now() - timestamp);
    const analyticsParams: IAnalyticsParams = _.extend({
      serviceName,
      request,
      duration
    }, response, this.getErrorDebug(response));

    if (serviceName === 'placeBet') {
      this.placeBetTracked(action === 'success', response, analyticsParams, apiKey);
    } else if (serviceName === 'readBet') {
      this.readBetTracked(action === 'success', response, analyticsParams, apiKey);
    } else if (_.contains(servicesToTrack, serviceName)) {
      this.buildBetTrack(action === 'success', response, analyticsParams, apiKey);
    } else if (action === 'error') {
      this.awsService.addAction(`${serviceName}Error`, analyticsParams);
    }
  }

  private placeBetTracked(successTracking: boolean, response: IConstant, analyticsParams: IAnalyticsParams, actionName: string): void {
    analyticsParams.betTypeIDs = [];
    analyticsParams.selectionIDs = [];

    _.each(analyticsParams.request.bet, (bet: IBet) => {
      analyticsParams.betTypeIDs.push(bet.betTypeRef.id);
    });

    _.each(analyticsParams.request.leg, (leg: IConstant) => {
      if (leg && leg.sportsLeg && leg.sportsLeg.legPart) {
        _.each(leg.sportsLeg.legPart, (legPart: ILegPart) => {
          analyticsParams.selectionIDs.push(legPart.outcomeRef.id);
        });
      }
    });
    analyticsParams.betTypeIDs = _.uniq(analyticsParams.betTypeIDs);

    if (successTracking) {
      analyticsParams.eventIDs = [];
      analyticsParams.marketIDs = [];
      _.each(response.bet, (bet: IBet) => {
        _.each(bet.leg, (leg: IConstant) => {
          if (leg && leg.sportsLeg && leg.sportsLeg.legPart) {
            _.each(leg.sportsLeg.legPart, (legPart: IConstant) => {
              if (legPart.outcomeRef.marketId) {
                analyticsParams.marketIDs.push(legPart.outcomeRef.marketId);
              }
              if (legPart.outcomeRef.eventId) {
                analyticsParams.eventIDs.push(legPart.outcomeRef.eventId);
              }
            });
          }
        });
      });
      if (response.betError) {
        this.getBetErrors(response.betError, analyticsParams);
      }
    }
    this.awsService.addAction(actionName, analyticsParams);
  }

  private readBetTracked(successTracking: boolean, response: IConstant, analyticsParams: IAnalyticsParams, actionName: string): void {
    if (successTracking) {
      analyticsParams.betTypeIDs = [];
      analyticsParams.selectionIDs = [];
      analyticsParams.eventIDs = [];
      analyticsParams.marketIDs = [];
      _.each(response.bet, (bet: IBet) => {
        analyticsParams.betTypeIDs.push(bet.betTypeRef.id);
        _.each(bet.leg, (leg: IConstant) => {
          if (leg && leg.sportsLeg && leg.sportsLeg.legPart) {
            _.each(leg.sportsLeg.legPart, (legPart: IConstant) => {
              analyticsParams.selectionIDs.push(legPart.outcomeRef.id);
              if (legPart.outcomeRef.marketId) {
                analyticsParams.marketIDs.push(legPart.outcomeRef.marketId);
              }
              if (legPart.outcomeRef.eventId) {
                analyticsParams.eventIDs.push(legPart.outcomeRef.eventId);
              }
            });
          }
        });
      });
      analyticsParams.betTypeIDs = _.uniq(analyticsParams.betTypeIDs);
      analyticsParams.selectionIDs = _.uniq(analyticsParams.selectionIDs);

      if (Array.isArray(analyticsParams.bet)) {
        const betsArrayCopy = [];
        analyticsParams.bet.forEach(bet => {
          const betCopy = Object.assign({}, bet);
          delete betCopy.leg;
          betsArrayCopy.push(betCopy);
        });
        analyticsParams.bet = betsArrayCopy;
      }

      if (response.betError) {
        const errors = _.isArray(response.betError) ? response.betError : [response.betError];
        this.getBetErrors(errors, analyticsParams);
      }
    }
    this.awsService.addAction(actionName, analyticsParams);
  }

  /**
   * AWS Firehose tracking for buildBet/buildBetLogged/buildComplexLegs
   * @param {boolean} successTracking
   * @param {Object} response
   * @param {Object} analyticsParams
   * @param {string} actionName
   */
  private buildBetTrack(successTracking: boolean, response: IConstant, analyticsParams: IAnalyticsParams, actionName: string): void {
    if (analyticsParams.serviceName === 'buildBet' || analyticsParams.serviceName === 'buildBetLogged') {
      analyticsParams.selectionIDs = _.uniq(_.map(_.pluck(analyticsParams.request.leg, 'sportsLeg'),
        leg => leg['legPart'][0].outcomeRef.id));
      analyticsParams.betTypeIDs = _.uniq(_.map(response.bets, bet => bet['betTypeRef'].id));
    } else if (analyticsParams.serviceName === 'buildComplexLegs') {
      analyticsParams.selectionIDs = _.pluck(analyticsParams.request.outcomeRef, 'id');
      analyticsParams.betTypeIDs = response.complexLeg ? _.pluck(response.complexLeg[0].outcomeCombiRef, 'id') : [];
    }

    if (response.betError) {
      const errors = _.isArray(response.betError) ? response.betError : [response.betError];
      this.getBetErrors(errors, analyticsParams);
    }

    if (successTracking) {
      const outcomeRefs = _.map(_.flatten(_.map(response.bet, b => b[ 'leg' ])), leg => leg[ 'sportsLeg' ].legPart[ 0 ].outcomeRef);
      _.each(outcomeRefs, ref => {
        if (ref.marketId) {
          analyticsParams.marketIDs = _.uniq(_.pluck(outcomeRefs, 'marketId'));
        }
        if (ref.eventId) {
          analyticsParams.eventIDs = _.uniq(_.pluck(outcomeRefs, 'eventId'));
        }
      });
    }

    this.awsService.addAction(actionName, analyticsParams);
  }

  private getBetErrors(betErrors: IBetError[], analyticsParams: IConstant): void {
    analyticsParams.errorCode = _.chain(betErrors)
      .pluck('code')
      .compact()
      .uniq()
      .value();
    analyticsParams.subErrorCode = _.chain(betErrors)
      .pluck('subErrorCode')
      .compact()
      .uniq()
      .value();
  }

  private checkLogoutErrorStatus(error: IError): boolean {
    const logoutTriggers: string[] = ['UNAUTHORIZED_ACCESS', 'EXTERNAL_FUNDS_UNAVAILABLE'];
    const status = error && ((error.error && error.error.status) || (error.data && error.data.status));
    return _.contains(logoutTriggers, status);
  }

  private implicitBalanceRefresh (serviceName: string, success: boolean): void {
    this.cmsService.getSystemConfig()
      .subscribe((systemConfig: ISystemConfig) => {
        const balanceRefreshConfig = systemConfig.BalanceUpdate && (success ? systemConfig.BalanceUpdate.BppSuccess :
          systemConfig.BalanceUpdate.BppError);

        if (balanceRefreshConfig && balanceRefreshConfig.includes(serviceName)) {
          this.pubSubService.publish(this.pubSubService.API.IMPLICIT_BALANCE_REFRESH);
        }
      });
  }

  /**
   * Check if bpp got an 503 with maintenance message
   *
   * @param error
   */
  private isMaintenanceError(error: IError): boolean {
    return error
      && error.error
      && error.error.message
      && error.error.message.toLowerCase().includes('maintenance');
  }

  private getErrorDebug(errorResponse: IAnalyticsParams): IAnalyticsParams {
    return errorResponse && errorResponse.error ? {
      debugCode: errorResponse.error.code,
      debugStatus: errorResponse.error.status,
      debugMessage: errorResponse.error.message,
      debugDescription: errorResponse.error.error
    } : {};
  }
}
