import { of as observableOf, throwError, Observable, Observer, of } from 'rxjs';

import { catchError, map, mergeMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';

import {
  IAddSelectionData, IYourcallBetError, IYourcallBetFailure,
  IYourcallBetPlacement,
  IYourcallBYBBetPLacementResponce,
  IYourcallDSBetPLacementResponce, IYourcallFormattedOdds,
  IYourcallOddsData
} from '@yourcall/models/betslip-data.model';
import { DSBet } from '@yourcall/models/bet/ds-bet';
import { BYBBet } from '@yourcall/models/bet/byb-bet';
import { ISportEvent } from '@core/models/sport-event.model';

import { IRemoteBetslipBet } from '@core/services/remoteBetslip/remote-betslip.constant';

import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { Location } from '@angular/common';
import { CHANNEL } from '@shared/constants/channel.constant';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';

@Injectable({ providedIn: 'root' })
export class YourcallBetslipService {
  ERROR_CODES: { [key: string]: string; } = {
    UNAUTHORIZED_ACCESS: 'UNAUTHORIZED_ACCESS',
    INTERNAL_PLACE_BET_PROCESSING: 'INTERNAL_PLACE_BET_PROCESSING',
    PRICE_CHANGED: 'PRICE_CHANGED',
    SERVICE_ERROR: 'SERVICE_ERROR'
  };
  placeData: any;
  private digitKeyBoardStatus:boolean=false;
  private stakeFromQb:number=0;
  isBetPlaceClicked: boolean;

  constructor(
    private remoteBetslipService: RemoteBetslipService,
    private userService: UserService,
    private fracToDecService: FracToDecService,
    private coreToolsService: CoreToolsService,
    private commandService: CommandService,
    private pubsubService: PubSubService,
    private localeService: LocaleService,
    private gtmService: GtmService,
    private yourCallProviderService: YourcallProviderService,
    private awsService: AWSFirehoseService,
    private fiveASideService: FiveASideService,
    protected location: Location,
    private bybSelectedSelectionsService: BybSelectedSelectionsService) { 
      this.updateKeyboardStatus()
    }

    updateKeyboardStatus()
    {
      this.pubsubService.subscribe('yourcall_quickStake', this.pubsubService.API.QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD, () => {
        this.stakeFromQb = this.digitKeyBoardStatus?2:1;
      });
      this.pubsubService.subscribe('yourcall_keyBoardPress', this.pubsubService.API.DIGIT_KEYBOARD_KEY_PRESSED, () => {
        this.stakeFromQb = 0;
      });
      this.pubsubService.subscribe('yourcall_digit_status', this.pubsubService.API.LUCKY_DIP_KEYPAD_PRESSED, (status) => {
        this.digitKeyBoardStatus = this.isBetPlaceClicked?this.digitKeyBoardStatus:!status;
      });
    }

  /**
   * Get remote bestlip config depends on  data provider
   * @return {*}
   * @constructor
   */
  get BETSLIP_CONFIG() {
    return this.remoteBetslipService.configs[this.yourCallProviderService.API.toLowerCase()];
  }
  set BETSLIP_CONFIG(value:any){}

  /**
   * Adds selection by outcome ID.
   * @param {Object} ycData
   * @returns {Promise}
   */
  addSelection(ycData: IAddSelectionData): Promise<DSBet | BYBBet> {
    const yourCallSelectionsData = this.yourCallProviderService.helper.createSelectionData(ycData || []);

    if (!this.BETSLIP_CONFIG) {
      return Promise.reject('Remote betslip config not found');
    }

    return this.remoteBetslipService.addSelection(yourCallSelectionsData, this.BETSLIP_CONFIG).pipe(
      map((betOddsResponse: IYourcallOddsData) => {
        const odds = this.getOdds(betOddsResponse);

        return this.yourCallProviderService.helper.createBet({
          currencySymbol: this.userService.currencySymbol,
          currency: this.userService.currency,
          token: this.userService.bppToken,
          oddsFormat: this.userService.oddsFormat,
          dashboardData: ycData,
          oddsFract: odds.frac,
          odds: odds.dec,
          channel: this.location.path().includes('5-a-side') ? CHANNEL.fiveASide : CHANNEL.byb
        });
      })).toPromise();
  }

  /**
   * Places bet request wrapper
   * @param {Object} bet
   * @param {Object} eventEntity
   * @param {Object} selection
   * @return {Promise}
   */
  placeBet(bet: IRemoteBetslipBet, eventEntity: ISportEvent, selection: BYBBet | DSBet): Observable<any> {
    const betCopy = this.coreToolsService.deepClone(bet);
    if (betCopy.freeBet) {
      betCopy.freeBet.stake = betCopy.freeBet.stake.replace(/[^\d.-]/g, '');
    }
    this.placeData = { bet: betCopy, eventEntity, selection };
    this.isBetPlaceClicked=true;
    this.bybSelectedSelectionsService.isBetPlaceClicked=true;

    return Observable.create(observer => {
      this.awsService.addAction('yourcallBetslipService=>placeBet=>Start', {date: new Date().getTime()});
      this.remoteBetslipService.placeBet(betCopy, this.BETSLIP_CONFIG).pipe(
        map((response: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce) => {
          this.awsService.addAction('yourcallBetslipService=>placeBet=>Done', {date: new Date().getTime()});
          return response;
        }),
        mergeMap((response: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce) => {
          return this.betPlacementSuccess(response);
        }),
        catchError(errorResponse => {
          const errorFromResponse = this.coreToolsService.hasOwnDeepProperty(errorResponse, 'data.error') ?
            errorResponse.data.error : errorResponse;

          this.awsService.addAction('yourcallBetslipService=>placeBet=>Error',
            {date: new Date().getTime(), errCode: errorFromResponse.code, errDescription: errorFromResponse.description}
          );

          if (errorFromResponse.subErrorCode === this.ERROR_CODES.SERVICE_ERROR
            && errorFromResponse.description === 'Connection timeout') {
            const errorMessage: string = this.handleTimeoutErrorMessage();
            observer.error(errorMessage);
            observer.complete();
          }

          if (errorFromResponse.code === this.ERROR_CODES.UNAUTHORIZED_ACCESS) {
            this.authorizeAndPlaceBet(errorFromResponse)
              .subscribe((data: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce) => {
                observer.next(data);
                observer.complete();
              }, (error: string) => {
                observer.error(error);
                observer.complete();
              });
          } else {
            const message = typeof errorFromResponse === 'string' ? errorFromResponse
              : this.betPlacementError(errorFromResponse);

            observer.error(message);
            observer.complete();
          }
          return of();
        })
      ).subscribe((data: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce) => {
        observer.next(data);
        observer.complete();
      });
    });
  }

  /**
   * Removes selection from remote betslip
   */
  removeSelection(): void {
    this.remoteBetslipService.removeSelection(this.BETSLIP_CONFIG);
    this.isBetPlaceClicked=false;
  }


  /**
   * Get odds from get price requests response
   * @param betOdds
   * @return {*}
   * @private
   */
  private getOdds(betOdds: IYourcallOddsData): IYourcallFormattedOdds {
    const oddsData = betOdds && betOdds.data;
    const odds: IYourcallFormattedOdds = {};

    if (oddsData.odds) {
      odds.dec = oddsData.odds;
      odds.frac = this.fracToDecService.decToFrac(oddsData.odds);
    } else if (oddsData.priceNum && oddsData.priceDen) {
      odds.dec = this.fracToDecService.getDecimal(oddsData.priceNum, oddsData.priceDen) as string;
      odds.frac = `${oddsData.priceNum}/${oddsData.priceDen}`;
    }

    return odds;
  }

  private betPlacementSuccessHandler(
    response: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce,
    observer: Observer<any>
  ): void {
    this.betPlacementSuccess(response)
        .subscribe((data: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce) => {
          observer.next(data);
          observer.complete();
        }, (error: string) => {
          observer.error(error);
          observer.complete();
        });
  }

  /**
   * Re-init bpp token and place a bet again
   * @param {Object} authError
   * @private
   */
  private authorizeAndPlaceBet(authError: any): Observable<IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce> {
    return Observable.create(observer => {
      this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE)
        .then(() => {
          this.placeData.bet.token = this.userService.bppToken;
          this.remoteBetslipService.placeBet(this.placeData.bet, this.BETSLIP_CONFIG)
            .subscribe((response: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce) => {
              this.betPlacementSuccessHandler(response, observer);
            }, (errorResponse: any) => {
              const error = this.coreToolsService.hasOwnDeepProperty(errorResponse, 'data.error') ?
                errorResponse.data.error : errorResponse;
              observer.error(this.betPlacementError(error));
              observer.complete();
            });
        })
        .catch(() => {
          observer.error(this.betPlacementError(authError));
          observer.complete();
        });
    });
  }

  /**
   * Handle timeout error message
   * @returns {string}
   * @private
   */
  private handleTimeoutErrorMessage(): string {
    return this.localeService.getString('quickbet.betPlacementErrors.TIMEOUT_ERROR');
  }

  /**
   * Handle success response from betPlacement
   * @param {Object} response
   * @private
   */
  private betPlacementSuccess(
    response: IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce
  ): Observable<IYourcallBYBBetPLacementResponce | IYourcallDSBetPLacementResponce> {
    // handle OB errors
    const bybResponce = response as IYourcallBYBBetPLacementResponce;
    const dsResponce = response as IYourcallDSBetPLacementResponce;

    const error = (bybResponce.data.betFailure && bybResponce.data.betFailure.betError) || bybResponce.data.betError;

    if (error) {
      this.trackPlaceBetError({
        code: error[0].betFailureCode,
        message: error[0].betFailureReason
      }, this.placeData.bet);
      this.placeData = null;
      return throwError(this.getErrorMsg(error));
    } else {
      // Banach - betReceipt.data.betReceipt, DS - betReceipt.data
      const receiptData = bybResponce.data.betPlacement && bybResponce.data.betPlacement.length > 0
        ? bybResponce.data.betPlacement[0] : dsResponce.data;

      this.trackPlaceBetSuccess(receiptData, this.placeData.bet, this.placeData.eventEntity, this.placeData.selection);
      this.placeData = null;
      return observableOf({ data: receiptData });
    }
  }

  /**
   * Handle error from betPlacement
   * @param {Object} error
   * @private
   */
  private betPlacementError(error: IYourcallBetError): string {
    this.trackPlaceBetError(error, this.placeData.bet);

    if (error.subErrorCode === this.ERROR_CODES.PRICE_CHANGED) {
      this.priceChangeError(error);
    }

    this.placeData = null;
    return this.getErrorMsg(error);
  }

  /**
   * Handle price change error and notify user
   * @param error
   * @private
   */
  private priceChangeError(error: any): void {
    this.pubsubService.publish(this.pubsubService.API.YOURCALL_SELECTION_UPDATE, {
      odds: this.fracToDecService.getDecimal(error.price.priceNum, error.price.priceDen),
      skipMessage: true
    });
  }

  /**
   * Get error msg by error data
   * @param {Object} error
   */
  private getErrorMsg(error: IYourcallBetError): string {
    if (this.isBetNotAllowedError(error as IYourcallBetFailure[])) {
      return this.localeService.getString('yourCall.betNotAllowedError');
    }

    if (!(error && (error.code || error.subErrorCode))) {
      return this.localeService.getString('yourCall.generalPlaceBetError');
    }

    // Get provider specific error message
    const providerErrorMsg = this.yourCallProviderService.helper.getPlaceBetErrorMsg(error);
    if (providerErrorMsg) {
      return providerErrorMsg;
    }

    if (error.code === this.ERROR_CODES.INTERNAL_PLACE_BET_PROCESSING) {
      return this.localeService.getString('yourCall.serverError');
    } else {
      return this.localeService.getString('yourCall.generalPlaceBetError');
    }
  }

  private isBetNotAllowedError(error: IYourcallBetFailure[]): boolean {
    return error && error[0] && error[0].betFailureDesc === 'CUST_RULES_EXCLUDE';
  }

  /**
   * GA track succes YouCall bet placement
   * @param {Object} receiptData
   * @param {Object} bet
   * @param {Object} eventEntity
   * @param {Object} selection
   * @private
   */
  private trackPlaceBetSuccess(receiptData: IYourcallBetPlacement, bet: IRemoteBetslipBet, eventEntity, selection: BYBBet | DSBet): void {
    const obj = {
      eventCategory: 'quickbet',
      eventAction: 'place bet',
      eventLabel: 'success',
      betID: receiptData.receipt,
      betType: receiptData.events && receiptData.events.length === 1 ? 'Single' : 'Multiple',
      ecommerce: {
        purchase: {
          actionField: {
            id: receiptData.receipt,
            revenue: receiptData.totalStake
          },
        products: [{
          price: selection.stake,
          category: eventEntity.sportId,
          variant: eventEntity.typeId,
          brand: this.location.path().includes('5-a-side')  ? '5-A-Side' : 'Bet builder',
          metric1: selection.freebetValue ? selection.freebetValue : 0,
          dimension60: eventEntity.id,
          dimension62: eventEntity.eventIsLive ? '1' : '0',
          dimension63: selection.isYourCallBet ? '1' : '0',
          dimension64: 'EDP',
          dimension65: this.location.path().includes('5-a-side')  ? '5-A-Side' : 'Bet builder',
          dimension66: receiptData.numLines,
          dimension67: selection.betOdds,
          dimension89: this.location.path().includes('5-a-side')  ? this.fiveASideService.activeFormation : undefined,
          dimension90: receiptData.betId,
          quantity: 1
          }]
        }
      }
    };
    if(this.stakeFromQb){
      const dimVal=this.stakeFromQb==2?'keypad predefined stake':'predefined stake';
      obj.ecommerce.purchase.products[0]['dimension181']=dimVal
    }
      this.stakeFromQb=0;
      this.digitKeyBoardStatus=false
    if (this.location.path().includes('5-a-side')) {
      this.gtmService.push('trackEvent', obj);
    }
    else {
      this.bybSelectedSelectionsService.placeBet(receiptData, bet, eventEntity, selection);
    }
    this.bybSelectedSelectionsService.betPlacementSucess();
    this.bybSelectedSelectionsService.duplicateIdd = new Set();
    this.awsService.addAction('yourcallBetslipService=>placeBet=>Success',
      { date: new Date().getTime(), betID: obj.betID }
    );
  }

  /**
   * GA track error YouCall bet placement
   * @param error
   * @param bet
   * @private
   */
  private trackPlaceBetError(error: IYourcallBetError, bet: IYourcallBetPlacement): void {
    const obj = {
      eventCategory: 'quickbet',
      eventAction: 'place bet',
      eventLabel: 'failure',
      errorMessage: error.message ? error.message : error.description,
      errorCode: error.subErrorCode || error.code,
      betType: bet.events && bet.events.length > 1 ? 'Multiple' : 'Single',
      location: 'yourcall'
    };
    this.gtmService.push('trackEvent', obj);
    this.awsService.addAction('yourcallBetslipService=>placeBet=>Error',
      { date: new Date().getTime(), errCode: obj.errorCode }
      );
  }
}
