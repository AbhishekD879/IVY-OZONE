import { forkJoin as observableForkJoin, of as observableOf,  Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { IBetslipData } from '@betslip/models/betslip-bet-data.model';
import { IConstant } from '@core/services/models/constant.model';
import * as _ from 'underscore';

import { IBetOffer } from '@betslip/services/acca/acca.models';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { IBppResponse, IFreeBetOfferResponseBetslip, IFreeBetTriggerBetslip } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { UserService } from '@core/services/user/user.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Bet } from '@betslip/services/bet/bet';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { IAnalyticsParams } from '@lazy-modules/awsFirehose/model/analytics-params.model';


@Injectable({ providedIn: BetslipApiModule })
export class AccaService {
  /**
   * TBL - treble - is a multiple bet buit from 3 legs.
   * betTypeRef and reqFreebetGetOffersResponse give us types like TBL, ACC6 AC10 etc.
   * To calculate difference between offer's type and trigger's type we have to convert them to numbers.
   * @type {number}
   */
  private readonly TBL: number = 3;

  constructor(
    private bppService: BppService,
    private userService: UserService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private router: Router,
    private pubSubService: PubSubService,
    private awsService: AWSFirehoseService
  ) {

  }

  /**
   * Search betOffer id and get offer by this id. Find offer by bet type and add to this bet.
   *
   * @param data
   * @return {object} object with bets and legs
   */
  getFreeBetOffer(data: IBetslipData): Observable<IBetslipData> {
    const observables: Observable<any>[] = [],
      allowedCurrencies: string[] = ['EUR', 'GBP', 'USD'],
      isMoreThen3Legs: boolean = data.legs && data.legs.length > 2;

    // Requirements - User should be login and User adds minimum of three selections
    if (isMoreThen3Legs && allowedCurrencies.indexOf(this.userService.currency) !== -1) {
      _.each(<IBetOffer[]>data.betOffers, (betOfferRef: IBetOffer) => {
        const betOffer$: Observable<any> = Observable.create(observer => {
          this.getBetOffer(betOfferRef.id).subscribe((offer: IFreeBetOfferResponseBetslip) => {
            const freeBetTrigger: IFreeBetTriggerBetslip[] = this.getFreeBetTriggers(offer),
              betOffer: IFreeBetTriggerBetslip = _.find(freeBetTrigger,
                  trigger => trigger.freebetTriggerId === betOfferRef.trigger.id);

            if (betOffer) {
              const bet: IConstant = _.find(data.bets, { type: betOfferRef.betTypeRef.id });
              if (bet) {
                bet.betOffer.offer = betOffer;
                bet.betOffer.isAccaValid = true;
                bet.betOffer.additionalLegsCount = this.additionalLegs(betOfferRef.betTypeRef.id, betOffer.freebetTriggerBetType);
                bet.betOffer.offerType = betOfferRef.offerType;
              }
            }

            observer.next();
            observer.complete();
          }, err => {
            console.warn('An error occured when retrieving free bet offer', err);
            observer.error(err);
            observer.complete();
          });
        });

        observables.push(betOffer$);
      });
    } else {
      observables.push(observableOf(null));
    }

    return Observable.create(observer => {
      if (observables.length) {
        observableForkJoin(observables).subscribe(() => {
          observer.next(data);
          observer.complete();
        }, err => {
          console.warn('An error occured when retrieving free bets offers', err);
          observer.error();
          observer.complete();
        });
      } else {
        observer.next(data);
        observer.complete();
      }
    });
  }

  /**
   * Open dialog with acca insurance info
   * @param textContent
   */
  accaInsurancePopup(textContent: string): void {
    this.awsService.addAction('AccaInsurance=>InfoIconClick', {});

    this.infoDialogService.openInfoDialog(
      this.localeService.getString('bs.accaInsuranceTitle'),
      textContent,
      'bs-selection-info-dialog acca-insurance-dialog',
      undefined,
      undefined,
      [
        {
          caption: this.localeService.getString('bs.more'),
          cssClass: 'btn-style4',
          handler: this.handleAccaMoreClick.bind(this)
        },
        {
          caption: this.localeService.getString('bs.ok'),
          cssClass: 'btn-style2',
          handler: () => {
            this.infoDialogService.closePopUp();
          }
        }
      ]
    );
  }

  /**
   * Get acca insurance offer max bonus for static block dynamic parameter
   */
  getAccaOfferMaxBonus(bet: Bet): string {
    return this.isBetOffer(bet) && bet.betOffer.offer && bet.betOffer.offer.freebetTriggerMaxBonus;
  }

  /**
   * Check if acca insurance is enabled in cms and offer is suggested for user
   */
  isAccaInsuranceSuggested(bet: Bet): boolean {
    return this.isBetOffer(bet) && bet.betOffer.offerType === 'suggested';
  }

  /**
   * Check if acca insurance is enabled in cms and offer is eligible for user
   */
  isAccaInsuranceEligible(bet: Bet): boolean {
    return this.isBetOffer(bet) && bet.betOffer.offerType === 'eligible';
  }

  /**
   * Check if acca betOffer is available
   */
  isBetOffer(bet: Bet): boolean {
    return bet && bet.betOffer;
  }

  private handleAccaMoreClick(): void {
    this.router.navigateByUrl('/promotions/all').then(
      () => {
        const analitycsParams: IAnalyticsParams = { redirectURL: '/promotions/all', redirect: 'success'};
        this.handleAWSTracking('AccaInsurance=>MoreClickRedirectSuccess', analitycsParams);
        },
      () => {
        const analitycsParams = { redirectURL: '/promotions/all', redirect: 'failed'};
        this.handleAWSTracking('AccaInsurance=>MoreClickRedirectFailed', analitycsParams);
      });
    this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
    this.infoDialogService.closePopUp();
  }

  private handleAWSTracking(actionName: string, analyticsParams: IAnalyticsParams): void {
    this.awsService.addAction(actionName, analyticsParams);
  }

  /**
   * Returns difference between betTypeRef.id and betOffer.freebetTriggerBetType
   * @param betTypeRef {string}
   * @param reqFreebetGetOffersResponse {string}
   * @returns {number}
   */
  private additionalLegs(betTypeRef: string, reqFreebetGetOffersResponse: string): number {
    return this.getCount(reqFreebetGetOffersResponse) - this.getCount(betTypeRef);
  }

  /**
   * Gets count of legs for acca insurance
   * @param BetType - example: acc4 or TBL
   * @returns {number}
   */
  private getCount(val: string): number {
    if (val === 'TBL') {
      return this.TBL;
    } else if (val.indexOf('ACC') !== -1) {
      return Number(val.substr(this.TBL));
    }
    return Number(val.substr(this.TBL - 1));
  }

  private getBetOffer(offerId: string): Observable<IBppResponse> {
    return this.bppService.send('freeBetOffer', { freebetOfferId: offerId });
  }

  /**
   * Retrieves "freebetTrigger" field from bet offer response.
   *
   * @param {Object} offerData
   * @return {Array}
   */
  private getFreeBetTriggers(offerData: IFreeBetOfferResponseBetslip): IFreeBetTriggerBetslip[] {
    const response = offerData && offerData.response,
      respFreebetGetOffers = response && response.respFreebetGetOffers,
      freebetOffer = respFreebetGetOffers && respFreebetGetOffers.freebetOffer[0];

    if (freebetOffer && freebetOffer.freebetTrigger) {
      return freebetOffer.freebetTrigger;
    }

    return [];
  }
}
