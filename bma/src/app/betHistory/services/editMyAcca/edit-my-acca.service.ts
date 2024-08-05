import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of, from, throwError } from 'rxjs';
import { mergeMap, map, delay, catchError } from 'rxjs/operators';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { DeviceService } from '@core/services/device/device.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';

import { handicapByMarketCode } from '@betslip/constants/bet-slip.constant';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISystemConfig } from '@core/services/cms/models';
import { IBetHistoryOutcome, IOutcome  } from '@core/models/outcome.model';
import { IBetHistoryLeg, IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import {
  IBetsResponse, IBetsRequest, IValidateBetResponse, IValidateParams, IPrice, ILeg, ILegPart, ILegRef, IBetError
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import environment from '@environment/oxygenEnvConfig';
import { IAccaGtmInfo } from '@app/betHistory/models/acca-gtm-info.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { StorageService } from '@app/core/services/storage/storage.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class EditMyAccaService {
  bet: IBetsRequest;
  initialStake: string;
  initialReturns: string;
  emaInProcess: boolean;
  unsavedAcca: IBetHistoryBet;
  savedAccas: {[key: string]: string} = {};
  isAccaEdit: boolean = false;
  removedBetLegs = [];

  emaConfig: {
    enabled: boolean;
    genericErrorTitle: string;
    genericErrorText: string;
  };

  public activeBet: IBetHistoryBet;
  private gtmLocation: string;

  private readonly statusOpen: string = 'open';
  private readonly statusSuspendedLeg: string = 'suspended';
  private readonly env = environment;

  constructor(
    private pubSubService: PubSubService,
    private bppService: BppService,
    private clientUserAgentService: ClientUserAgentService,
    private deviceService: DeviceService,
    private cmsService: CmsService,
    private betHistoryMainService: BetHistoryMainService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private windowRef: WindowRefService,
    private siteServerService: SiteServerService,
    private domToolsService: DomToolsService,
    private awsService: AWSFirehoseService,
    private gtm: GtmService,
    private timeSyncService: TimeSyncService,
    private storageService: StorageService,
  ) {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.emaConfig = config.EMA || {};
    });

    this.waitAndMakeReadBet = this.waitAndMakeReadBet.bind(this);
    this.betLiveUpdateHandler = this.betLiveUpdateHandler.bind(this);
    this.showEditCancelMessage = this.showEditCancelMessage.bind(this);

    this.subscribeToEvents();
  }

  get EMAEnabled(): boolean {
    return this.emaConfig.enabled;
  }
  set EMAEnabled(value:boolean){}
  get isEmaInProcess(): boolean {
    return this.emaInProcess;
  }
  set isEmaInProcess(value:boolean){}
  removeLeg(bet: IBetHistoryBet, leg: IBetHistoryLeg): void {
    this.storeRemovedLegs(bet.betId, leg);
    const betLegs = _.filter(bet.leg, (_leg: IBetHistoryLeg) => !_leg.removing && _leg !== leg && !this.isLegResulted(_leg));
    bet.emaPriceError = false;
    this.bet.leg = this.createLegs(betLegs);
    this.makeValidateBetRequest(bet, [leg]);
    this.trackRemoveLeg(bet, leg);

    if (this.isUnsavedInWidget()) {
      this.pubSubService.publish(this.pubSubService.API.EMA_UNSAVED_IN_WIDGET, true);
    } else if (this.isUnsavedOnEdp()) {
      this.pubSubService.publish(this.pubSubService.API.EMA_UNSAVED_ON_EDP, true);
    }
  }
  /**
   * storing removed Legs data when doing edi my acca
   * */
  storeRemovedLegs(betId:string, leg: IBetHistoryLeg) {
    if(!this.removedBetLegs || (this.removedBetLegs && !this.removedBetLegs.length) || 
    (this.removedBetLegs && this.removedBetLegs.findIndex(removedLeg => Number(removedLeg.betId) === Number(betId)) === -1)) {
      this.removedBetLegs.push({
        betId: betId,
        eventIds: [leg.part[0].eventId]
      })
    } else {
      const index = this.removedBetLegs.findIndex(removedLeg => Number(removedLeg.betId) === Number(betId))
      this.removedBetLegs[index].eventIds.push(leg.part[0].eventId)
    }
  }
  /**
   * undoing removed Legs data when doing edi my acca
   * */
  undoStoredRemovedLegs(betId, legs: IBetHistoryLeg[]) {
    legs.forEach(leg => {
      const betIndex = this.removedBetLegs.findIndex(removedLeg => Number(removedLeg.betId) === Number(betId))
      const eventIndex = this.removedBetLegs[betIndex].eventIds.findIndex(removedEventId => Number(removedEventId) === Number(leg.part[0].eventId));
      this.removedBetLegs[betIndex].eventIds.splice(eventIndex, 1)
    })
  }
  /**
   * Deleteing event id and bet id when doing edit My acca bet
   * */
  setSignPostData(bet: IBetHistoryBet, newBetId: string) {
    const signPostData = this.storageService.get('myBetsSignPostingData');
    const removedLegIndex = this.removedBetLegs && this.removedBetLegs.length && this.removedBetLegs.findIndex(removeBet => Number(removeBet.betId) === Number(bet.betId))
    if(signPostData && removedLegIndex > -1){
      this.removedBetLegs[removedLegIndex].eventIds.forEach(eventId=> {
        const eventIdIndex = signPostData.findIndex(eventData => Number(eventData.eventId) === Number(eventId));
        const betIndex = signPostData[eventIdIndex].betIds.findIndex(betid => Number(betid) === Number(bet.betId));
        if(betIndex > -1){
          signPostData[eventIdIndex].betIds.splice(betIndex,1);
        }
      })
      signPostData.forEach(eventData => {
        const betIndex = eventData.betIds.findIndex(betId => Number(betId) === Number(bet.betId));
        if(betIndex > -1) {
          eventData.betIds[betIndex] = newBetId;
        }
      });
      this.storageService.set('myBetsSignPostingData', signPostData);
    }
  }
  

  undoRemoveLegs(bet: IBetHistoryBet, legs: IBetHistoryLeg[]): void {
    if(bet.betId) {
      this.undoStoredRemovedLegs(bet.betId, legs);
    }
    const betLegs = _.filter(bet.leg, (leg: IBetHistoryLeg) => !leg.removing || _.contains(legs, leg));
    const openLegs = _.filter(betLegs, (leg: IBetHistoryLeg) => !this.isLegResulted(leg));
    bet.emaPriceError = false;

    this.bet.leg = this.createLegs(openLegs);

    if (betLegs.length === bet.leg.length) {
      this.setInitialState(bet);
    } else {
      this.makeValidateBetRequest(bet, legs);
    }
  }

  canRemoveLegs(bet: IBetHistoryBet): boolean {
    if (bet.validateBetStatus === 'pending') {
      return false;
    }

    if (this.hasSuspendedLegs(bet)) {
      return false;
    }

    return _.filter(bet.leg, (leg: IBetHistoryLeg) => !leg.removedLeg && leg.status === this.statusOpen && !leg.removing).length > 1;
  }

  canUndoRemoveLegs(bet: IBetHistoryBet): boolean {
    return bet.validateBetStatus !== 'pending' &&
      !this.hasSuspendedLegs(bet) && !this.isEmaInProcess;
  }

  editMyAcca(bet: IBetHistoryBet): Observable<IBetsResponse> {
    this.emaInProcess = true;
    bet.emaPriceError = false;

    const betWithPrices = this.getBetWithPrices(bet);

    this.awsService.addAction('EditMyAccaService=>placeBet=>Start', { request: this.bet });
    return this.bppService.send('placeBet', betWithPrices).pipe(
      mergeMap(this.waitAndMakeReadBet),
      map((res: IBetsResponse | any) => {
        this.awsService.addAction('EditMyAccaService=>placeBet=>Success', { result: res });

        if (res.betError) {
          this.placeBetErrorHandler(res.betError, bet);
        } else {
          this.setSignPostData(bet, res.bet[0].id);
          this.showEditSuccessMessage(bet, res.bet[0].id, res.bet[0].payout[0].potential);
        }
        this.trackConfirmEditMyAcca(bet, true);

        return res;
      }),
      catchError((err: IBetError | IBetError[]) => {
        this.awsService.addAction('EditMyAccaService=>placeBet=>Error', { error: err });
        this.placeBetErrorHandler(err, bet);
        this.trackConfirmEditMyAcca(bet, false);
        return throwError(err);
      })
    );
  }

  getBetWithPrices(bet: IBetHistoryBet): IBetsRequest {
    _.each(this.bet.leg, (leg: ILeg) => {
      const id = leg.sportsLeg.legPart[0].outcomeRef.id;
      leg.sportsLeg.price.num = bet.outcomes[id].lp_num;
      leg.sportsLeg.price.den = bet.outcomes[id].lp_den;
    });
    return this.bet;
  }

  isLegResulted(leg: IBetHistoryLeg): boolean {
    const resultedStatuses = ['won', 'lost', 'void'];
    return _.contains(resultedStatuses, leg.status);
  }

  isLegSuspended(leg: IBetHistoryLeg): boolean {
    return (leg.status === this.statusSuspendedLeg) && !leg.removedLeg;
  }

  isBetOpen(bet: IBetHistoryBet): boolean {
    return this.betHistoryMainService.getBetStatus(bet) === this.statusOpen;
  }

  hasSuspendedLegs(bet: IBetHistoryBet): boolean {
    return _.some(bet.leg, (leg: IBetHistoryLeg) => this.isLegSuspended(leg));
  }

  hasLegsWithLostStatus(bet: IBetHistoryBet): boolean {
    return _.some(bet.leg, (leg: IBetHistoryLeg) => leg.status === 'lost' && !leg.removedLeg);
  }

  canEditBet(bet: IBetHistoryBet): boolean {
    return !!this.EMAEnabled && this.isAccaBet(bet) && this.isBetOpen(bet) && (this.hasOpenLegs(bet) || this.hasSuspendedLegs(bet));
  }

  toggleBetEdit(bet: IBetHistoryBet, gtmLocation?: string): void {
    bet.isAccaEdit = !bet.isAccaEdit;
    bet.emaPriceError = false;
    bet.validateBetStatus = null;
    bet.initialReturns = <string>bet.potentialPayout;

    this.clearBetLegsRemoving(bet);

    if (!bet.isAccaEdit) {
      _.each(bet.leg, (leg: IBetHistoryLeg, index: number) => {
        const price = leg.part[0].price && leg.part[0].price[0];
        if (price) {
          this.setPrices(index, price.priceNum, price.priceDen);
        }
      });
      this.pubSubService.publish(this.pubSubService.API.UPDATE_EMA_ODDS);

      if (this.initialStake) {
        this.setStakeAndPayout(bet, this.initialStake, this.initialReturns);
      }
      this.pubSubService.publish(this.pubSubService.API.EMA_UNSAVED_IN_WIDGET, false);
      this.pubSubService.publish(this.pubSubService.API.EMA_UNSAVED_ON_EDP, false);
    }

    if (bet.isAccaEdit) {
      this.activeBet = bet;
      this.bet = this.createValidateRequest({
        currency: bet.currency,
        stake: bet.stake,
        leg: [],
        cashoutBetId: bet.betId
      });
      this.initialStake = <string>bet.stake;
      this.initialReturns = <string>bet.potentialPayout;

      this.trackStartEditMyAcca(bet, gtmLocation);
    } else {
      this.bet = null;
      this.activeBet = null;
    }
  }

  cancelActiveEdit(bet: IBetHistoryBet): void {
    if (this.activeBet && this.activeBet !== bet) {
      this.toggleBetEdit(this.activeBet);
    }
  }

  isAccaBet(bet: IBetHistoryBet): boolean {
    return Number(bet.numLines) === 1 && Number(bet.numLegs) > 1;
  }

  showEditCancelMessage(): void {
    const pageTop = this.domToolsService.getPageScrollTop();
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('ema.editCancel.caption'),
      this.localeService.getString('ema.editCancel.text'),
      undefined,
      undefined,
      () => this.domToolsService.scrollPageTop(pageTop),
      [{
        caption: 'Cancel edit',
        cssClass: 'btn-style4',
        handler: () => {
          this.toggleBetEdit(this.unsavedAcca);
          this.infoDialogService.closePopUp();
        }
      }, {
        caption: 'Continue editing'
      }]
    );
  }

  canChangeRoute(): boolean {
    return this.unsavedAcca ? !(this.unsavedAcca.isAccaEdit && !this.isUnsavedInWidget() &&
      this.unsavedAcca.leg.some((leg: IBetHistoryLeg) => leg.removing)) :
      true;
  }

  clearAccas(): void {
    if (this.isAccaEdit) {
      this.isAccaEdit = false;
    } else {
      this.savedAccas = {};
      delete this.unsavedAcca;
    }
  }

  removeSavedAcca(betId: string): void {
    if (this.savedAccas[betId]) {
      delete this.savedAccas[betId];
    }
  }

  isUnsavedInWidget(): boolean {
    return !!this.windowRef.document.querySelector('.my-bets-content edit-my-acca-confirm');
  }

  isUnsavedOnEdp(): boolean {
    return !!this.windowRef.document.querySelector('my-bets edit-my-acca-confirm');
  }

  private hasOpenLegs(bet: IBetHistoryBet): boolean {
    return _.filter(bet.leg, (leg: IBetHistoryLeg) =>
      !leg.removedLeg && leg.status === this.statusOpen && !!leg.part[0].priceNum).length > 1;
  }

  private showEditSuccessMessage(bet?: IBetHistoryBet, newBetId?: number, payout?: string): void {
    this.emaInProcess = false;
    this.toggleBetEdit(bet);
    this.pubSubService.publishSync(this.pubSubService.API.EDIT_MY_ACCA);
    this.savedAccas[newBetId] = 'success';
    this.windowRef.nativeWindow.scrollTo(0, 0);
    this.isAccaEdit = true;
  }

  private makeValidateBetRequest(
    bet: IBetHistoryBet,
    legs: IBetHistoryLeg[],
    isErrorHandler?: boolean,
    considerPriceError?: boolean
  ): void {
    this.setLegRefs();
    this.setBetType(this.bet.leg.length);

    bet.validateBetStatus = 'pending';

    this.awsService.addAction('EditMyAccaService=>validateBet=>Start', { request: this.bet });

    this.bppService.send('validateBet', this.bet)
      .subscribe((res: IValidateBetResponse) => {
        if (res.betError) {
          this.awsService.addAction('EditMyAccaService=>validateBet=>Error', { error: res });
          this.validateBetErrorHandler(res.betError, bet);
        } else {
          this.awsService.addAction('EditMyAccaService=>validateBet=>Success', { result: res });

          /*
          Show error the EMA PRICW ERROR message here and NOT on placeBetErrorHandler level because there is a possible
          situation when the Validation could also fail (in this case we need to show error message onlny from CMS).
          Fix for BMA-52488 - [Ladbrokes][EMA] Two messages are displayed in the 'EMA' mode on the 'Open Bets' tab
          after tapping 'Confirm' button and in same time change price in TI for one of selections.
           */
          bet.emaPriceError = considerPriceError;

          this.validateBetSuccessHandler(res, bet, legs, isErrorHandler);
        }
      }, (err: HttpErrorResponse) => {
        this.awsService.addAction('EditMyAccaService=>validateBet=>Error', { error: err });
        this.validateBetErrorHandler(err, bet);
      });
  }

  private setStakeAndPayout(bet: IBetHistoryBet, stake: string, payout?: string): void {
    bet.stake = stake;
    if (payout) {
      bet.potentialPayout = payout;
    }
  }

  private createValidateRequest(reqData: IValidateParams): IBetsRequest {
    const { stake, currency, leg, cashoutBetId } = reqData;
    const stakeObj = {
      amount: Number(stake).toFixed(2),
      stakePerLine: Number(stake).toFixed(2),
      currencyRef: { id: currency }
    };

    return {
      betslip: {
        clientUserAgent: this.clientUserAgentService.getId(),
        documentId: '1',
        stake: stakeObj,
        slipPlacement: _.extend(
          { IPAddress: this.timeSyncService.ip },
          this.deviceService.channel
        ),
        betRef: [{
          documentId: '1'
        }]
      },
      bet: [{
        documentId: '1',
        betTypeRef: {
          id: null
        },
        stake: stakeObj,
        legRef: [],
        lines: { number: 1 },
        newBetStake: Number(stake).toFixed(2),
        cashoutBetId,
      }],
      leg
    };
  }

  private setLegRefs(): void {
    this.bet.bet[0].legRef = _.map(this.bet.leg, (legItem: IBetHistoryLeg) => ({
      documentId: legItem.documentId
    })) as unknown as ILegRef[];
  }

  private setBetType(legCount: number): void {
    let type;
    switch (legCount) {
      case 1:
        type = 'SGL';
        break;
      case 2:
        type = 'DBL';
        break;
      case 3:
        type = 'TBL';
        break;
      default:
        const accaPrefix = legCount > 9 ? 'AC' : 'ACC';
        type = `${accaPrefix}${legCount}`;
    }
    this.bet.bet[0].betTypeRef.id = type;
  }

  private createLegs(legs: IBetHistoryLeg[]): ILeg[] {
    const excludeRemovedLegs = _.filter(legs, (leg: IBetHistoryLeg) => !leg.removedLeg);

    return _.map(excludeRemovedLegs, (leg: IBetHistoryLeg) => {
      const { priceNum, outcome, handicap } = leg.part[0];
      return {
        documentId: leg.legNo,
        sportsLeg: {
          price: {
            priceTypeRef: {
              id: priceNum ? 'LP' : 'SP'
            }
          },
          legPart: [this.createLegPart(outcome, <string>handicap, _.isString(leg.legSort) ? leg.legSort : leg.legSort.code)],
          winPlaceRef: {
            id: 'WIN'
          }
        }
      };
    }) as ILeg[];
  }

  private createLegPart(outcome: string | IBetHistoryOutcome, handicap: string, code: string): ILegPart {
    const hCode = handicapByMarketCode[code];
    const part = {
      outcomeRef: {
        id: _.isString(outcome) ? outcome : outcome[0].id
      }
    } as ILegPart;

    if (hCode) {
      const handicapToSend = handicap.replace(/\+/, '');
      part.range = {
        high: handicapToSend,
        low: handicapToSend,
        rangeTypeRef: {
          id: hCode
        }
      };
    }

    return part;
  }

  private validateBetSuccessHandler(
    res: IValidateBetResponse,
    bet: IBetHistoryBet,
    legs: IBetHistoryLeg[],
    isErrorHandler?: boolean
  ): void {
    if (!bet.isAccaEdit) {
      return;
    }

    const stake = res.bet[0].subjectToCashout.newBetStake;
    this.setStakeAndPayout(bet, stake, res.bet[0].betPotentialWin);
    this.bet.bet[0].newBetStake = stake;
    this.emaInProcess = false;

    if (!isErrorHandler) {
      _.each(legs, (leg: IBetHistoryLeg) => leg.removing = !leg.removing);
    }
    bet.validateBetStatus = 'ok';
  }

  private validateBetErrorHandler(
    error: IBetError[] | HttpErrorResponse,
    bet: IBetHistoryBet
  ): void {
    if (!bet.isAccaEdit) {
      return;
    }

    bet.validateBetStatus = error[0] && error[0].subErrorCode === 'PRICE_CHANGED' ? 'ok' : 'fail';

    this.savedAccas[bet.id || bet.betId] = 'error';
    this.emaInProcess = false;
  }

  private placeBetErrorHandler(error: IBetError[] | IBetError, bet: IBetHistoryBet): void {
    if (error[0] && this.isPriceError(error)) {
      from(this.siteServerService.getEventsByOutcomeIds({ outcomesIds: bet.outcome }, true))
        .pipe(map((res: ISportEvent[]) => {
          _.each(res, (event: ISportEvent) => this.setSiteServerResponse(event.markets[0].outcomes[0], bet));

          if (error[0].price.length) {
            this.setSiteServerResponse({
              id: error[0].outcomeRef.id,
              prices: [{
                priceNum: error[0].price[0].priceNum,
                priceDen: error[0].price[0].priceDen
              }]
            } as IOutcome, bet);
          }

          this.getBetWithPrices(bet);
          this.makeValidateBetRequest(bet, bet.leg, true, true);
        })).subscribe();
    } else {
      this.savedAccas[bet.betId] = 'error';
      this.emaInProcess = false;
    }
  }

  private isPriceError(error: IBetError | IBetError[]): boolean {
    const errorObj = _.isArray(error) ? error[0] : error || {};
    const { subErrorCode, failureDescription } = errorObj;
    return subErrorCode === 'PRICE_CHANGED' || subErrorCode === 'CASHOUT_VALUE_CHANGE' || failureDescription === 'CASHOUT_VALUE_CHANGE';
  }

  private setSiteServerResponse(outcome: IOutcome, bet: IBetHistoryBet): void {
    const newPrice = outcome.prices[0];
    const outcomeMap = bet.outcomes[outcome.id];

    if (outcomeMap) {
      outcomeMap.lp_num = newPrice.priceNum;
      outcomeMap.lp_den = newPrice.priceDen;
      this.setPrices(_.indexOf(bet.outcome, outcome.id), +newPrice.priceNum, +newPrice.priceDen);
      this.pubSubService.publish(this.pubSubService.API.UPDATE_EMA_ODDS);
    }
  }

  private waitAndMakeReadBet(res: IValidateBetResponse): Observable<IValidateBetResponse> {
    const bet = res.bet ? res.bet[0] : null;
    const confirmNeeded = !!(bet && bet.isConfirmed === 'N' && bet.confirmationExpectedAt);

    if (!confirmNeeded) {
      return of(res);
    }

    const seconds = +bet.confirmationExpectedAt + 1;
    this.pubSubService.publish(this.pubSubService.API.EMA_CONFIRM_NEEDED, seconds);

    return of(null).pipe(
      delay(seconds * 1000),
      mergeMap(() => {
        return this.bppService.send('readBet', { betRef: [{ id: bet.id, provider: 'OpenBetBir' }] }) as Observable<IValidateBetResponse>;
      })
    );
  }

  private getRemovedResultedLegs(bet: IBetHistoryBet): IBetHistoryLeg[] {
    return _.filter(bet.leg, (leg: IBetHistoryLeg) => (leg.status === 'won' || leg.status === 'void') && leg.removing);
  }

  private setInitialState(bet: IBetHistoryBet): void {
    this.clearBetLegsRemoving(bet);

    if (this.initialStake) {
      this.setStakeAndPayout(bet, this.initialStake, this.initialReturns);
    }
  }

  private betLiveUpdateHandler(updObj): void {
    if (!this.activeBet || this.emaInProcess) {
      return;
    }

    const removedResultedLegs = this.getRemovedResultedLegs(this.activeBet);
    const priceUpdateIndex = _.indexOf(this.activeBet.outcome, updObj.id);
    const isEdit = this.activeBet.leg.some((leg: IBetHistoryLeg) => leg.removing);

    if (priceUpdateIndex >= 0 && !this.activeBet.leg[priceUpdateIndex].removedLeg && isEdit) {
      this.updatePrices(priceUpdateIndex, updObj.updatePayload);
    } else if (removedResultedLegs.length && isEdit) {
      this.undoRemoveLegs(this.activeBet, removedResultedLegs);
    }
  }

  private updatePrices(id: number, prices: IPrice): void {
    this.setPrices(id, prices.lp_num, prices.lp_den);

    const betLegs = _.filter(this.activeBet.leg, (leg: IBetHistoryLeg) => !leg.removing && !this.isLegResulted(leg));
    this.bet.leg = this.createLegs(betLegs);

    this.makeValidateBetRequest(this.activeBet, this.activeBet.leg, true);
    this.pubSubService.publish(this.pubSubService.API.UPDATE_EMA_ODDS);
  }

  private setPrices(id: number, num: string | number, den: string | number): void {
    const updatedLegPart = this.activeBet.leg[id].part[0];
    updatedLegPart.priceNum = +num;
    updatedLegPart.priceDen = +den;
  }

  private subscribeToEvents(): void {
    this.pubSubService.subscribe(
      'EditMyAccaService', this.pubSubService.API.EMA_HANDLE_BET_LIVE_UPDATE, this.betLiveUpdateHandler
    );

    this.pubSubService.subscribe(
      'EditMyAccaService', this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG, this.showEditCancelMessage
    );
  }

  /**
   * track acca edit start;
   * set gtm location for leg remove and confirm edit events;
   * extends general GA info with event specific data and push gtm event;
   * @param {IBetHistoryBet} bet
   * @param {string} gtmLocation
   */
  private trackStartEditMyAcca(bet: IBetHistoryBet, gtmLocation: string): void {
    this.gtmLocation = gtmLocation;
    const gtmObj = {
      eventAction: 'start',
      eventLabel: 'success'
    };

    Object.assign(gtmObj, this.getGtmInfo(bet));
    this.gtm.push('trackEvent', gtmObj);
  }

  /**
   * track leg removing by user;
   * extends general GA info with event specific data and push gtm event;
   * @param {IBetHistoryBet} bet
   * @param {IBetHistoryLeg} leg
   */
  private trackRemoveLeg(bet: IBetHistoryBet, leg: IBetHistoryLeg): void {
    const event = leg.eventEntity;
    const gtmObj = {
      eventAction: 'remove',
      eventLabel: 'success',
      eventName: event.originalName || event.name,
      categoryID: event.categoryId,
      typeID: event.typeId,
      eventID: event.id,
      eventMarket: event.markets[0].name,
      selectionID: event.markets[0].outcomes[0].id
    };

    Object.assign(gtmObj, this.getGtmInfo(bet));
    this.gtm.push('trackEvent', gtmObj);
  }

  /**
   * track edit acca confirmation;
   * extends general GA information with event specific data and push gtm event;
   * @param {IBetHistoryBet} bet
   * @param {boolean} status
   */
  private trackConfirmEditMyAcca(bet: IBetHistoryBet, status: boolean): void {
    const numberOfLegsLeft = bet.leg.filter((leg: IBetHistoryLeg) => {
      return !leg.removing && !leg.removedLeg;
    }).length;

    const numberOfLegsWas = bet.leg.filter((leg: IBetHistoryLeg) => {
      return !leg.removedLeg;
    }).length;

    const gtmObj = {
      eventAction: 'confirm',
      eventLabel: status ? 'success' : 'failure',
      emaStartLegs: numberOfLegsWas,
      emaEndLegs: numberOfLegsLeft
    };

    Object.assign(gtmObj, this.getGtmInfo(bet));
    this.gtm.push('trackEvent', gtmObj);
  }

  /**
   * generate general info for edit acca GA tracking;
   * @param {IBetHistoryBet} bet
   */
  private getGtmInfo(bet: IBetHistoryBet): IAccaGtmInfo {
    return {
      eventCategory: 'edit acca',
      betType: bet.betType as string,
      location: this.gtmLocation || 'unknown',
      betInPlay: this.getBetLiveStatus(bet),
      customerBuilt: this.isBuildYourBet(bet)
    };
  }

  /**
   * get isLive status for bet events;
   * returns Yes/No/Both;
   * @param {IBetHistoryBet} bet
   */
  private getBetLiveStatus(bet: IBetHistoryBet): string {
    return bet.leg.reduce((res: string, leg: IBetHistoryLeg) => {
      if (!leg.eventEntity) {
        return res;
      }
      const isEventLive = leg.eventEntity.isStarted || leg.eventEntity.eventIsLive ? 'Yes' : 'No';
      if (res === '') {
        return isEventLive;
      }
      return res === isEventLive ? res : 'Both';
    }, '');
  }

  /**
   * gets build your bet status by event type ID;
   * returns 1 - true, 0 - false;
   * customer build cannot be mixed so we can set customer build by first leg with event;
   * @param {IBetHistoryBet} bet
   */
  private isBuildYourBet(bet: IBetHistoryBet): number {
    const legWithEvent = bet.leg && bet.leg.find((leg: IBetHistoryLeg) => {
      return !!leg.eventEntity;
    });

    const isBuildYourBet = this.env.BYB_CONFIG && legWithEvent
      && this.env.BYB_CONFIG.HR_YC_EVENT_TYPE_ID === Number(legWithEvent.eventEntity.typeId);
    return isBuildYourBet ? 1 : 0;
  }

  private clearBetLegsRemoving(bet: IBetHistoryBet): void {
    bet.leg.forEach((leg: IBetHistoryLeg, index: number) => {
      leg.removing = false;
    });
  }
}
