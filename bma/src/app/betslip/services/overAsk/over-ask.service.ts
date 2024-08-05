import {
  from as observableFrom,
  Observable,
  of,
  Subject,
  Subscription,
  throwError,
  timer as observableTimer
} from 'rxjs';

import { catchError, map, switchMap, takeUntil } from 'rxjs/operators';
import { DOCUMENT, Location } from '@angular/common';
import { Inject, Injectable, OnDestroy } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';
import { Router } from '@angular/router';

import { SessionService } from '@authModule/services/session/session.service';
import { IError } from '@app/bpp/services/bpp/bpp.model';
import { IPrice } from '@core/models/price.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';
import { OverAskNotificationDialogComponent } from '@betslip/components/overaskNotificationDialog/over-ask-notification-dialog.component';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';

import {
  IBet,
  ILeg,
  IOfferBet,
  IOfferBetAction,
  IReadBetRequest,
  IReadBetResponse,
  IRespTransGetBetsPlaced, IStake
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetslipBetData, IBetslipLeg, IBetslipPairs, IBetslipState } from '../../models/betslip-bet-data.model';
import { UserService } from '@core/services/user/user.service';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { AuthService } from '@authModule/services/auth/auth.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { BetUtils } from '@app/bpp/services/bppProviders/bet.utils';
import { ERROR_DICTIONARY } from '@core/constants/error-dictionary.constant';
import { DeviceService } from '@core/services/device/device.service';

@Injectable({ providedIn: BetslipApiModule })
export class OverAskService implements OnDestroy {
  /**
   * Flags for overask state
   * @member {boolean}
   */
  isFreeBetToken: boolean = false;
  isInProcess: boolean = false;
  isInFinal: boolean = false; // the state is truthy when overask finishes at bet-receipt stage
  isNotInProcess: boolean = true;
  isOnTradersReview: boolean = false;
  hasTraderMadeDecision: boolean = false;
  hasCustomerActionTimeExpired: boolean = false; // this state sets only for a moment, so basically is 'false'
  isBPMPFreeBetTokenUsed: boolean = false;

  /**
   * Flags for bets state after trader has made decision
   * @member {boolean}
   */
  isAllBetsAccepted: boolean = false;
  isAllBetsDeclined: boolean = false;
  isAllBetsOffered: boolean = false;
  isNoBetsAccepted: boolean = true;
  isNoBetsDeclined: boolean = true;
  isNoBetsOffered: boolean = true;
  isSomeBetsAccepted: boolean = false;
  isSomeBetsDeclined: boolean = false;
  isSomeBetsOffered: boolean = false;
  userHasChoice: boolean = false; // overask phase 2, user's asked to cancel/confirm counter-offer, bs mode

  stateMessage: string = '';
  errorMessage: string = '';
  offerExpiresAt: string = '';
  bsMode: string; // indicates the stage (mode) of betslip [readonly]

  readonly states: IBetslipState = {
    off: 'off',
    onTradersReview: 'onTradersReview',
    traderMadeDecision: 'traderMadeDecision',
    customerActionTimeExpired: 'customerActionTimeExpired'
  };

  private modulePath: string = '@betslipModule/betslip.module#BetslipModule';
  private minDeclinedBetCountForEnableSorting = 2;

  private isBetsDataAssigned: boolean = false;
  private betsData: IBetslipBetData[] = []; // betsData model sets from betslip controller
  private placeBetsData: IRespTransGetBetsPlaced = null; // placeBetsData sets from BetSlip service
  private offerTimerSubscription: Subscription;
  private mainSubject: Subject<IRespTransGetBetsPlaced>;
  private readBetSubscribtion: Subscription;

  private state: string = this.states.off;
  private destroyed$ = new Subject();
  private hasUserMadeDecision: boolean = false;
  private suspendedIds: number[] = [];
  private deletedBetIds: string[] = [];
  private originalPlacedBets: {[key: number]: any} = {};
  private readonly tag = 'OverAskService';

  constructor(
    private windowRefService: WindowRefService,
    private location: Location,
    private bppService: BppService,
    private storageService: StorageService,
    private localeService: LocaleService,
    private fracToDecService: FracToDecService,
    private dialogService: DialogService,
    private domToolsService: DomToolsService,
    private command: CommandService,
    private betslipStorageService: BetslipStorageService,
    @Inject(DOCUMENT) private document,
    private userService: UserService,
    private sessionService: SessionService,
    private router: Router,
    private dynamicComponentLoader: DynamicLoaderService,
    private authService: AuthService,
    private pubSubService: PubSubService,
    private deviceService: DeviceService
  ) {
    this.triggerRestoreStateIfLoggedIn();

    this.pubSubService.subscribe(this.tag, this.pubSubService.API.SESSION_LOGOUT, () => {
      if (this.isInProcess) {
        this.betslipStorageService.clearStateInStorage();
        this.betslipStorageService.cleanBetslip(false, false);
      }

      this.setState(this.states.off);
      this.readBetSubscribtion && this.readBetSubscribtion.unsubscribe();
    });
    this.pubSubService.subscribe(this.tag, this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.triggerRestoreStateIfLoggedIn();
    });
  }

  ngOnDestroy(): void {
    this.destroyed$.next(null);
    this.destroyed$.complete();

    this.pubSubService.unsubscribe(this.tag);
  }

  /**
   * Clears betData model
   */
  clearBetsData(): void {
    this.betsData = [];
    this.isBetsDataAssigned = false;
  }

  /**
   * Sets betData model and update it if overask in progress
   * @param {betData[]} betsData
   */
  setBetsData(betsData: IBetslipBetData[]): void {
    this.betsData = betsData;
    this.isBetsDataAssigned = true;

    if (this.hasTraderMadeDecision) {
      this.updateBetsData();
    }

    this.resetInProcessErrors();
  }

  /**
   * Clears state message
   */
  clearStateMessage(): void {
    this.stateMessage = '';
    this.errorMessage = '';
  }

  /**
   * Mein method to start overask process
   * @param {placeBetsData} placeBetsData
   * @returns {Subject<placeBetsData>}
   */
  execute(placeBetsData: IRespTransGetBetsPlaced): Subject<IRespTransGetBetsPlaced> {
    return this.executeInternal(placeBetsData);
  }

  /**
   * Checks is overask process started
   * @param {placeBetsData} placeBetsData
   * @returns {boolean}
   */
  isOverask(placeBetsData: IRespTransGetBetsPlaced): boolean {
    return _.some(placeBetsData.bets, (bet: IBet) => bet.isReferred === 'Y');
  }

  /**
   * Sends acceptOffer request
   * @returns {Observable}
   */
  acceptOffer(): void {
    if (this.hasUserMadeDecision) {
      return;
    }

    this.clearOfferTimeout();
    const betIds = this.getBetIds();
    this.acceptOrRejectOffer(betIds, 'ACCEPT')
      .subscribe((res: IOfferBet | { message: string }) => {
        const error = this.checkError(res);

        if (error) {
          this.finisWithFailure(error);
        } else {
          this.processOveraskFlow(res);
        }
      }, err => {
        this.finisWithFailure(this.checkError(err) || err);
      });
  }

  /**
   * Sends rejectOffer request
   * @returns {Observable}
   */
  rejectOffer(reuseSelections: boolean = true, cleanBetslip: boolean = true): Observable<void> {
    this.clearOfferTimeout();
    const betIds = _.map(this.placeBetsData.bets, (bet: IBet) => bet.id);

    return this.acceptOrRejectOffer(betIds, 'REJECT').pipe(
      switchMap(() => {
        this.cancelOveraskProcess(!reuseSelections, true, cleanBetslip);

        if (!reuseSelections) { return observableFrom(null); }

        const outcomesIds = this.getSinglesOutcomesIds(false);
        return this.reuseSelections(outcomesIds);
      }),
      catchError(err => {
        this.finisWithFailure(err);
        return of(err);
      }),
    );
  }

  /**
   * Clears betslip and finish overask process with failure
   * @param {boolean} closeSlideOut
   * @param {boolean} isOveraskCanceled
   */
  cancelOveraskProcess(closeSlideOut: boolean = false, isOveraskCanceled: boolean = false, cleanBetslip: boolean = true): void {
    if (cleanBetslip) {
      this.betslipStorageService.cleanBetslip(closeSlideOut, isOveraskCanceled);
    }
    this.finisWithFailure();
  }

  /**
   * Sorts betsData
   * @private
   */
  sortDeclinedBetsOnTop(betsData: IBetslipBetData[]): IBetslipBetData[] {
    const declinedCount = _.filter(betsData, betData => betData.isTraderDeclined).length;

    return declinedCount >= this.minDeclinedBetCountForEnableSorting
      ? _.sortBy(betsData, (betData: IBetslipBetData) => betData.isTraderDeclined)
      : betsData;
  }

  /**
   * Sorts betsData for linked bets
   * @param {Array.<Object>} betsData
   * @returns {Array.<Object>} betsData
   */
  sortLinkedBets(betsData: IBetslipBetData[]): IBetslipBetData[] {
    this.defineParents(betsData);
    const notConnectedBets = betsData.filter(bd => !bd.children && !bd.dependsOn);
    const parents = betsData.filter(bd => bd.children && bd.children.length);
    const linked = betsData.filter(bd => bd.dependsOn);

    const sortedBetsData = [];

    sortedBetsData.push(...notConnectedBets);
    parents.forEach(parentBet => {
      sortedBetsData.push(parentBet);
      const children = linked.filter(lb => parentBet.children.includes(lb.betId));
      sortedBetsData.push(...children);
    });

    return sortedBetsData;
  }

  /**
   * Shows notification for desktop or navigates to betslip on mobile if overask in progress
   */
  showOveraskInProgressNotification(): void {
    console.warn('Overask', 'In progress');

    if (this.windowRefService.nativeWindow.view.mobile) {
      this.router.navigateByUrl(this.location.path());
      this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], true);
    } else {
      // TODO: @Oleh Vykhopen
      this.dynamicComponentLoader.loadModule(this.modulePath).then((moduleRef) => {
        const componentFactory = moduleRef.componentFactoryResolver.resolveComponentFactory(OverAskNotificationDialogComponent);
        this.dialogService.openDialog(DialogService.API.betslip.overAskNotificationDialog, componentFactory, true);
      });

      const bsTabsContainer = this.document.getElementById('bs-tabs-container');
      this.document.body.scrollTop = this.domToolsService.getOffset(bsTabsContainer).top;
    }
  }

  /**
   * Sets overask state and clear storage
   * @param {states} newState
   */
  setStateAndClearInStorage(newState: string): void {
    this.setState(newState);
    this.betslipStorageService.clearStateInStorage();
  }

  /**
   * Set array of suspended bets which are in the overask process
   *
   * @param {number[]}
   */
  setSuspended(suspendedIds: number[]): void {
    this.suspendedIds = suspendedIds;
  }

  /**
   * Check that all active bets are not suspended
   *
   * @returns boolean
   */
  isOveraskCanBePlaced(): boolean {
    const placedBets = this.placeBetsData && this.placeBetsData.bets;
    return Boolean(placedBets && placedBets.length &&
      placedBets.some((bet: IBet) => bet.isCancelled !== 'Y' && !this.suspendedIds.includes(bet.id)));
  }

  /**
   * Check if bet is in overask process are suspended
   *
   * @param {any} betToCheck - single or multiple bet
   * @returns boolean
   */
  isBetPlaced(betToCheck: any): boolean {
    const placedBets = this.placeBetsData && this.placeBetsData.bets;

    return Boolean(placedBets && placedBets.length && placedBets.some((bet: IBet) => bet.id === betToCheck.betId));
  }

  /**
   * Check whether bet ID in deleted list or not
   *
   * @param id
   */
  isNotDeletedFromTraderOffer(id: string): boolean {
    return this.deletedBetIds.findIndex(deletedID => deletedID === id) === -1;
  }

  /**
   * Add to deletedBetID list
   *
   * @param id
   */
  collectDeletedBetID(id: string): void {
      this.deletedBetIds.push(id);
  }

  /**
   * Remove from deletedBetID list
   *
   * @param id
   */
  removeDeletedBetID(id: string): void {
    const startIndex = this.deletedBetIds.findIndex(deletedId => deletedId === id);
    this.deletedBetIds.splice(startIndex, 1);
  }

  /**
   * Look though betData and find parents of linked bets
   * It adds to parent bet property `children` with ids of linked bets
   * @param betsData
   */
  private defineParents(betsData: IBetslipBetData[]): IBetslipBetData[] {
    return betsData.map((betData: IBetslipBetData) => {
      if (betData.dependsOn && Number.isInteger(betData.dependsOn)) {
        const parentBetData = betsData.find((parentData: IBetslipBetData) => parentData.betId === betData.dependsOn);

        if (!Array.isArray(parentBetData.children)) {
          parentBetData.children = [];
        }
        parentBetData.children.push(betData.betId);
        this.defineIsRemovable(parentBetData);
      }
      this.defineIsRemovable(betData);
      return betData;
    });
  }

  /**
   * Define property to check if offer can be removed
   * @param betData
   */
  private defineIsRemovable(betData: IBetslipBetData): void {
    betData.isOfferRemovable = betData.isTraderAccepted || betData.isTraderOffered && !betData.children;
  }

  /**
   * Restores overask process
   * @private
   */
  private restoreState(): void {
    if (this.storageService.get('overaskUsername') !== this.userService.username) { return; }

    this.isInProcess = this.storageService.get('overaskIsInProcess');

    if (this.isInProcess) {
      const storedPlaceBetsData: IRespTransGetBetsPlaced = this.storageService.get('overaskPlaceBetsData');

      this.executeInternal(storedPlaceBetsData)
        .subscribe(placeBetsData => {
          console.warn('Overask', 'State restored');
          this.pubSubService.publishSync(this.pubSubService.API.OVERASK_STATE_RESTORED, placeBetsData);
        }, error => {
          this.pubSubService.publishSync(this.pubSubService.API.OVERASK_STATE_RESTORE_FAILED, error);
        });
    } else {
      this.setStateAndClearInStorage(this.states.off);
    }
  }

  /**
   * Continue (switch to bet-receipt) overask process with accepted OR/AND declined bets
   * (ex finisWithSuccess)
   *
   * do keep some state flags, but clear storage data as 'bet receipt' is not restorable
   *
   * @param res
   */
  private processOveraskFlow(res?: IOfferBet | { message: string }): void {
    const statusMessage = res && (res as { message: string }).message;
    const offerHasError = res && _.some((res as IOfferBet).offerBetAction, (offer: IOfferBetAction) => offer.status === 'ERROR');

    if (statusMessage || offerHasError) {
      this.setState(this.states.off);
      this.finisWithFailure({ data : { status: 'overaskError' } });
      return;
    }

    this.userHasChoice = false;
    this.isInFinal = true;
    this.isInProcess = false;
    this.betslipStorageService.clearStateInStorage();

    const betIds = this.getBetIds(true);
    this.placeBetsData.bets = _.filter(this.placeBetsData.bets,
        (bet: IBet) => _.contains(betIds, bet.id));
    this.placeBetsData.ids = betIds; // 'bet receipt' will later use these ids to fetch data
    this.mainSubject.next(this.placeBetsData);
    this.mainSubject.complete();
  }

  /**
   * Finishes overask process with failure
   * @param {{}=} error - error data
   * @private
   */
  private finisWithFailure(error?: IError): void {
    if (this.userService.status) {
      this.setStateAndClearInStorage(this.states.off);

      if (error && error.data && (error.data.status === 'PT_ERR_AUTH' || error.data.status === 'LOW_FUNDS')) {
        this.errorMessage = error.data.message;
      }

      this.mainSubject.error(error);
    }
  }

  /**
   * Sets overask state and recalculate flags
   * @param {string} state
   * @private
   */
  private setState(state: string): void {
    this.state = state;
    this.isNotInProcess = state === this.states.off;
    this.isInProcess = !this.isNotInProcess;
    this.isInFinal = this.isInProcess && this.bsMode === 'Bet Receipt';
    this.isOnTradersReview = state === this.states.onTradersReview;
    this.hasTraderMadeDecision = state === this.states.traderMadeDecision;
    this.hasCustomerActionTimeExpired = state === this.states.customerActionTimeExpired;

    this.clearStateFlags();

    _.each(this.betsData, (betData: IBetslipBetData) => {
      this.clearBetFlags(betData);
    });

    this.clearOfferTimeout();
    this.calculateStateMessage();

    if (this.hasTraderMadeDecision || this.hasCustomerActionTimeExpired) {
      this.pubSubService.publishSync(this.pubSubService.API.OVERASK_BETS_DATA_UPDATED, this.stateMessage);
    } else if (this.isOnTradersReview) {
      this.pubSubService.publishSync(this.pubSubService.API.OVERASK_REVIEW_STARTED);
    }

    // If offer expired - process for expired offer and finish overask journey without removing bets
    if (this.hasCustomerActionTimeExpired) {
      this.state = this.states.off;
      this.isNotInProcess = true;
      this.isInProcess = !this.isNotInProcess;
      this.hasCustomerActionTimeExpired = false;
      this.mainSubject.error({ data : { offerTimeExpired: true } });
    }
  }

  /**
   * Clear flags for overask state
   */
  private clearStateFlags(): void {
    this.isAllBetsAccepted = false;
    this.isAllBetsDeclined = false;
    this.isAllBetsOffered = false;
    this.isNoBetsAccepted = true;
    this.isNoBetsDeclined = true;
    this.isNoBetsOffered = true;
    this.isSomeBetsAccepted = false;
    this.isSomeBetsDeclined = false;
    this.isSomeBetsOffered = false;
    this.userHasChoice = false;
    this.hasUserMadeDecision = false;
    this.suspendedIds = [];
    this.deletedBetIds = [];
  }

  /**
   * Clear overask flags in a single bet data
   * @param betData
   */
  private clearBetFlags(betData: IBetslipBetData): void {
    betData.isTraderAccepted = false;
    betData.isTraderDeclined = false;
    betData.isTraderOffered = false;
    betData.isSelected = false;
    betData.isTraderChanged = false;
    betData.isOfferRemovable = false;

    betData.traderChangedPriceType = false;
    betData.traderChangedLegType = false;
    betData.traderChangedOdds = false;
    betData.traderChangedStake = false;

    betData.overaskMessage = '';

    // flag needed only for overask for multiples bets
    if (betData.type !== 'SGL') {
      betData.disabled = false;
    }
  }

  /**
   * Save overask data to storage
   *
   * get view's overask data (bets, state) and replace bets by originals if we have splits,
   * save required data to storage
   *
   * @private
   */
  private saveStateToStorage(originalBets?: IBet[]): void {
    const betsData: IRespTransGetBetsPlaced = Object.assign({}, this.placeBetsData);

    if (originalBets) {
      betsData.bets = originalBets;
    }

    this.storageService.set('overaskPlaceBetsData', betsData);
    this.storageService.set('overaskIsInProcess', this.isInProcess);
    this.storageService.set('overaskUsername', this.userService.username);
  }

  /**
   * Clears Customer offer timeout
   * @private
   */
  private clearOfferTimeout(): void {
    if (this.offerTimerSubscription) {
      this.offerTimerSubscription.unsubscribe();
    }
  }

  /**
   * Calculates message for Customer hint according current state
   * @private
   */
  private calculateStateMessage(): void {
    this.clearStateMessage();

    if (this.state && this.state === this.states.customerActionTimeExpired) {
      this.stateMessage = this.localeService.getString(`bs.overaskMessages.${this.state}`);
    }
  }

  /**
   * Starts overask process
   * @param {placeBetsData} placeBetsData
   * @returns {Subject<IRespTransGetBetsPlaced>}
   */
  private executeInternal(placeBetsData: IRespTransGetBetsPlaced): Subject<IRespTransGetBetsPlaced> {
    this.placeBetsData = placeBetsData;
    this.mainSubject = new Subject();
    this.setState(this.states.onTradersReview);
    this.saveStateToStorage();
    this.runReadBetPolling(0).subscribe();
    return this.mainSubject;
  }

  /**
   * Returns time to offer expired
   * @param {IReadBetResponse} readBetResponse
   * @returns {int} time in millisecond
   * @private
   */
  private getTimeToOfferExpired(readBetResponse: IReadBetResponse): number {
    let offerTime = 0;
    const firstBet = _.find(readBetResponse.bet, bet => _.has(bet, 'offerExpiresAt'));

    if (firstBet) {
      offerTime = new Date(firstBet.offerExpiresAt).getTime() - Date.now();
      this.offerExpiresAt = firstBet.offerExpiresAt;
    }

    console.warn('Overask', 'Offer timeout in sec', Math.round(offerTime / 1000));
    return offerTime;
  }

  /**
   * Runs read bet polling iteration
   * @param {int} timeoutInSec
   * @private
   */
  private runReadBetPolling(timeoutInSec: number): Observable<void> {
    return observableTimer(timeoutInSec).pipe(
      switchMap(() => this.sendReadBetRequest()),
      map(readBetResponse => this.checkReadBetResponse(readBetResponse)),
      catchError(err => {
        if (err.errorCode !== ERROR_DICTIONARY.OFFLINE.errorCode && !this.deviceService.isOnline()) {
          this.finisWithFailure(err);
        }
        return of(err);
      }));
  }

  /**
   * Checks is Trader made decision
   * @param {IReadBetResponse} readBetResponse
   * @returns {boolean}
   * @private
   */
  private checkHasTraderMadeDecision(readBetResponse: IReadBetResponse): boolean {
    const outcomeGroups = _.chain(readBetResponse.bet)
      .filter((bet: IBet) => bet.isConfirmed !== 'Y' && bet.isCancelled !== 'Y')
      .groupBy((bet: IBet) => this.getBetKey(bet))
      .value();

    return !Object.keys(outcomeGroups).length || Object.values(outcomeGroups).some(outcomeGroup => outcomeGroup.length >= 2);
  }

  /**
   * Updates placeBetsData model with readBetResponse
   *
   * bets which have `isReferred` are original bets that were split during overask process
   * such bets should not be shown on UI but saved in storage
   *
   * @param {IReadBetResponse} readBetResponse
   * @private
   */
  private applyBetsChanges(readBetResponse: IReadBetResponse): IBet[] | null {
    const originalBets: IBet[] = [];
    const offeredBets: IBet[] = [];
    const betsIdsCounters: {[key: number]: number} = readBetResponse.bet.reduce((bets, bet: IBet) => {
      // Count bets with the same Id
      if (!bets.hasOwnProperty(bet.id)) {
        bets[bet.id] = 0;
      }

      bets[bet.id]++;

      return bets;
    }, {});

    this.originalPlacedBets = {};

    // filter unique bets from offer and store original bets for restore
    readBetResponse.bet.forEach((baseBet: IBet) => {
      if (baseBet.isReferred !== 'Y' || betsIdsCounters[baseBet.id] === 1) {
        offeredBets.push(baseBet);
      } else {
        originalBets.push(baseBet);
      }

      // Original bets which was requested for Overask (without any changes during journey)
      if (baseBet.isReferred === 'Y') {
        this.originalPlacedBets[baseBet.id] = baseBet;
      }
    });

    this.placeBetsData.bets = offeredBets;

    return originalBets.length ? originalBets : null;
  }

  /**
   * Calculates bets states after Trader offer
   * @private
   */
  private calculateBetsStates(isFreeBetToken: boolean): void {
    const
      stat = _.reduce(this.placeBetsData.bets,
        (memo, bet: IBet) => ({
          accepted: memo.accepted + (bet.isConfirmed === 'Y' ? 1 : 0),
          declined: memo.declined + (bet.isCancelled === 'Y' ? 1 : 0),
          offered: memo.offered + (bet.isOffer === 'Y' ? 1 : 0)
        }), {
          accepted: 0,
          declined: 0,
          offered: 0
        }),
      count = this.placeBetsData.bets.length;

    this.isNoBetsAccepted = stat.accepted === 0;
    this.isNoBetsDeclined = stat.declined === 0;
    this.isNoBetsOffered = stat.offered === 0;

    this.isSomeBetsAccepted = stat.accepted > 0 && stat.accepted < count;
    this.isSomeBetsDeclined = stat.declined > 0 && stat.declined < count;
    this.isSomeBetsOffered = stat.offered > 0 && stat.offered < count;

    this.isAllBetsAccepted = stat.accepted === count;
    this.isAllBetsDeclined = stat.declined === count;
    this.isAllBetsOffered = stat.offered === count;

    this.userHasChoice = this.isInProcess && this.hasTraderMadeDecision && !this.isNoBetsOffered && !isFreeBetToken;
  }

  /**
   * Apples trader decision
   * @param {IReadBetResponse} readBetResponse
   * @private
   */
  private applyTraderDecision(readBetResponse: IReadBetResponse): void {
    const originalBets = this.applyBetsChanges(readBetResponse);

    this.setStateAndClearInStorage(this.states.traderMadeDecision);
    this.isFreeBetToken = readBetResponse.bet.some((bet: IBet) => parseInt(bet.tokenValue, 10) > 0);
    this.calculateBetsStates(this.isFreeBetToken);
    this.calculateStateMessage();

    // trader made counter-offer - overask stays in betslip mode,
    // need to save data for restore flow
    if (this.isAllBetsOffered || this.isSomeBetsOffered) {
      this.saveStateToStorage(originalBets);
    }

    this.pubSubService.publishSync(this.pubSubService.API.OVERASK_BETS_DATA_UPDATED, this.stateMessage);

    if (this.isNoBetsOffered) {
      this.processOveraskFlow();
    } else if (this.isAllBetsOffered || this.isSomeBetsOffered) {
      this.offerTimerSubscription = observableTimer(this.getTimeToOfferExpired(readBetResponse)).subscribe(() => this.onOfferTimeout());
    }
  }

  /**
   * Checks readBet response and apples changes or runs pulling iteration
   * @param {IReadBetResponse} readBetResponse
   * @private
   */
  private checkReadBetResponse(readBetResponse: IReadBetResponse): void {
    if (!this.isInProcess) {
      return;
    }

    if (this.checkHasTraderMadeDecision(readBetResponse)) {
      this.applyTraderDecision(readBetResponse);
    } else {
      if (this.isBetsDataAssigned) {
        const betPairs = this.matchBetsToBetsData();
        if (this.checkIsMatchBetsToBetsDataNotSuccess(betPairs)) {
          return;
        }
      }

      this.readBetSubscribtion = this.runReadBetPolling(5000).subscribe();
    }
  }

  /**
   * Called on offer timeout. Updates betData model changes state
   * @private
   */
  private onOfferTimeout(): void {
    this.setStateAndClearInStorage(this.states.customerActionTimeExpired);
  }

  /**
   * Builds readBet request
   * @returns {readBetRequest}
   * @private
   */
  private buildReadBetRequest(): Partial<IReadBetRequest> {
    const betRef = _.map(this.placeBetsData.bets,
        (bet: IBet) => ({ id: bet.id, provider: 'OpenBetSports' }));
    return {
      betRef
    };
  }

  /**
   * Sends readBet request
   * @returns {Observable<any>}
   * @private
   */
  private sendReadBetRequest(): Observable<IReadBetResponse> {
    return (this.bppService.send('readBet', <IReadBetRequest>this.buildReadBetRequest()) as Observable<IReadBetResponse>).pipe(
      switchMap(res => (res.betError ? throwError(res.betError) : of(res))));
  }

  /**
   * Sends acceptOrRejectOffer request
   * @param {betId[]} betIds
   * @param {string} action
   * @returns {Observable}
   * @private
   */
  private acceptOrRejectOffer(betIds: number[], action: string): Observable<IOfferBet | { message: string }> {
    const offerBetAction = _.map(betIds, id => ({
          betRef: { id, provider: 'OpenBetSports' },
          offerBetActionRef: { id: action }
        })),
        request = {
          offerBetAction
        };

    this.hasUserMadeDecision = true;

    return (this.bppService.send('offerBet', request)).pipe(
      map((res: IOfferBet) => {
        const statusMessage = _.chain(res.offerBetAction)
          .filter((offerBet: IOfferBetAction) => offerBet.status === 'ERROR')
          .map((offerBet: IOfferBetAction) => offerBet.statusMessage)
          .uniq()
          .value()
          .join(', ');

        return statusMessage ? { message: statusMessage } : res;
      }));
  }

  /**
   * Returns OutcomesIds for singles betData
   * @param {bool} isSelectedOnly - is only for selected or all
   * @returns {number[]}
   * @private
   */

  private getSinglesOutcomesIds(isSelectedOnly: boolean): string[] {
    return _.chain(this.betsData)
        .filter((betData: IBetslipBetData) => betData.type === 'SGL' && !betData.combiType) // get only singles
        .filter((betData: IBetslipBetData) => isSelectedOnly ? betData.isSelected : true)
        .map((betData: IBetslipBetData) => betData.outcomeId)
        .uniq()
        .value();
  }

  /**
   * Returns array of betIds for placing bet and for bet receipt
   *
   * @param isReceiptData - include declined bets for BetReceipt
   * @returns {betId[]}
   * @private
   */
  private getBetIds(isReceiptData: boolean = false): number[] {
    return this.betsData.reduce((list: number[], betData: IBetslipBetData) => {
      if (betData.betId) {
        if (betData.isSelected || (isReceiptData && betData.isTraderDeclined)) {
          list.push(betData.betId);
        }
      }

      return list;
    }, []);
  }

  /**
   * Reuses selections by outcomesIds
   * @param {string[]} outcomesIds
   * @returns {Observable}
   * @private
   */
  private reuseSelections(outcomesIds: string[]): Observable<void> {
    /**
     * List of splitted outcome ids.
     * @type {Array}
     */
    const ids = _.chain(outcomesIds)
        .map(outcome => _.isString(outcome) ? outcome.split('|') : outcome)
        .flatten()
        .value();
    return observableFrom(
      this.command.executeAsync(
        this.command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS,
        [ids.join(','), false, true, false]
      )
    ).pipe(map(() => this.pubSubService.publishSync(this.pubSubService.API.REFRESH_BETSLIP)));
  }

  /**
   * gets an array of outcomes from bet leg
   * @param {object} bet
   * @returns {string[]}
   * @private
   */
  private getOutcomeIds(bet: IBet): Array<string> {
    return _.flatten((bet.leg as ILeg[]).map(leg => leg.sportsLeg.legPart.map(legPart => legPart.outcomeRef.id)));
  }

  /**
   * Represents and return bet's unique key
   * @param {object} bet
   * @returns {string}
   * @private
   */
  private getBetKey(bet: IBet): string  {
    const outcomeCombiRefIds = _.chain((bet.leg as ILeg[]))
        .map((leg: ILeg) => leg.sportsLeg.outcomeCombiRef.id)
        .compact()
        .value();
    return _.compact([
      bet.betTypeRef.id,
      outcomeCombiRefIds.length && outcomeCombiRefIds.join('_'),
      bet.lines.number,
      this.getOutcomeIds(bet).join('_')
    ]).join('_');
  }

  /**
   * Group by bets by key betType + firstOutcomeId
   * @private
   */
  private groupBetsByUniqueKey(): _.Dictionary<IBet[]> {
    return _.groupBy(this.placeBetsData.bets, (bet: IBet) => this.getBetKey(bet));
  }

  /**
   * Match bet to betData
   * @returns {{betData, bet}[]}
   * @private
   */
  private matchBetsToBetsData(): IBetslipPairs[] {
    const betsByKey = this.groupBetsByUniqueKey(),
        betPairs = [];
    _.each(betsByKey, (bets, key) => {
      const firstBet: IBet = bets[0],
          betDataIndex = this.betsData.findIndex((betData: IBetslipBetData) => {
            const marketType = betData.combiName === 'SCORECAST' ? betData.outcomeIds[0].split('|') : betData.outcomeIds;
            const outcomeIds = this.getOutcomeIds(firstBet),
                outcomeCombyIds = (firstBet.leg as ILeg[]).map(leg => leg.sportsLeg.outcomeCombiRef.id);

            outcomeCombyIds.forEach((id, index) => {
              if (id === 'REVERSE_FORECAST') {
                outcomeCombyIds[index] = 'FORECAST';
              }
            });

            return _.intersection(marketType, outcomeIds).length === outcomeIds.length &&
                betData.type === firstBet.betTypeRef.id &&
                betData.Bet.lines === firstBet.lines.number &&
                (betData.combiType === outcomeCombyIds[0] || betData.combiName === outcomeCombyIds[0]);
          }),
          betDataSource: IBetslipBetData = this.betsData[betDataIndex];

      if (betDataIndex === -1) {
        console.warn('Overask', 'Can not find betData', key);
        return;
      }

      _.each(bets, (bet: IBet, index: number) => {
        let betDataForBet: IBetslipBetData;
        if (index === 0) {
          betDataForBet = betDataSource;
        } else {
          // create clone for splited bet
          const newBet = betDataSource.Bet.clone();
          betDataForBet = newBet.info();
          betDataForBet.dependsOn = Number(bet.dependsOn);
          if (bet.masterBetId) {
            betDataForBet.masterBetId = Number(bet.masterBetId);
          }
          // it will be shown if freeBets available
          betDataForBet.freeBetText = this.localeService.getString('bs.freeBetsAvalaible');
          this.betsData.splice(betDataIndex + 1, 0, betDataForBet);
        }

        betPairs.push({ betData: betDataForBet, bet });
      });
    });
    return betPairs;
  }

  /**
   * Check if trader change prices
   * @param {Array} betData legs
   * @param {Array} offeredLegs legs
   * @private
   */
  private isPricesChanged(betData: IBetslipBetData, offeredLegs: IBetslipLeg[]): boolean {
    // Overask offer should not apply TI changes for prices
    const originalBetId = betData.masterBetId || betData.dependsOn || betData.betId;
    const requestedBetLegs = this.originalPlacedBets && this.originalPlacedBets[originalBetId]
      && this.originalPlacedBets[originalBetId].leg || [];
    const requestedBetLegsPriceMap = {};

    requestedBetLegs.forEach((requestedBetLeg: IBetslipLeg) => {
      requestedBetLegsPriceMap[requestedBetLeg.sportsLeg.legPart[0].outcomeRef.id] = requestedBetLeg.sportsLeg.price;
    });

    const offeredPricesMap = _.reduce(offeredLegs, (originalMap: IPrice[], leg: IBetslipLeg) => {
          originalMap[leg.sportsLeg.legPart[0].outcomeRef.id] = {
            priceDen: leg.sportsLeg.price.priceDen,
            priceNum: leg.sportsLeg.price.priceNum,
            priceType: leg.sportsLeg.price.priceTypeRef.id
          };
          return originalMap;
        }, []),
        oldLegs: IBetslipLeg[] = _.map(betData.Bet.legs, (leg: IBetslipLeg) => {
          const oldLegPrice = requestedBetLegsPriceMap[leg.firstOutcomeId] || leg.price.props;

          return {
            outcomeId: leg.firstOutcomeId,
            price: {
              priceDen: oldLegPrice.priceDen,
              priceNum: oldLegPrice.priceNum,
              priceType: oldLegPrice.priceType || oldLegPrice.priceTypeRef && oldLegPrice.priceTypeRef.id.toString()
            },
            outcome: leg.parts[0].outcome
          };
        });

    oldLegs.forEach((leg: IBetslipLeg) => {
      const offeredLeg = offeredPricesMap[leg.outcomeId];

      if (offeredLeg && (this.isPriceTypeChange(leg, offeredLeg) || this.isPriceChange(leg, offeredLeg))) {
        leg.traderChangedPrice = true;
        leg.changedPrice = offeredLeg;
      }

      if (betData.outcomeIds && betData.outcomeIds.length) {
        leg.betData = this.betsData.find((betsDataItem: IBetslipBetData) => betsDataItem.outcomeId === leg.outcomeId);
      }
    });

    betData.oldLegs = oldLegs;

    return _.some(betData.oldLegs, (leg: IBetslipLeg) => leg.traderChangedPrice);
  }

  /**
   * Is price number change
   * @private
   * @param  {object}  leg        The leg object
   * @param  {object}  offeredLeg The offered leg object
   * @return {Boolean}            [description]
   */
  private isPriceChange(leg: IBetslipLeg, offeredLeg: IPrice): boolean {
      return this.isNumbersDifferent(offeredLeg.priceDen, leg.price.priceDen) ||
          this.isNumbersDifferent(offeredLeg.priceNum, leg.price.priceNum);
  }

  /**
   * Is price type change
   * @private
   * @param  {IBetslipLeg}  leg        The leg object
   * @param  {object}  offeredLeg The offered leg object
   * @return {Boolean}            [description]
   */
  private isPriceTypeChange(leg: IBetslipLeg, offeredLeg: Partial<IPrice>): boolean {
    return (leg.price.priceType === 'SP' || offeredLeg.priceType === 'SP') &&
      leg.price.priceType !== offeredLeg.priceType;
  }

  /**
   * Checks is two numbers different
   * @param {Number|String} v1
   * @param {Number|String} v2
   * @returns {boolean}
   * @private
   */
  private isNumbersDifferent(v1: number | string, v2: number | string): boolean {
    return (Number(v1) || 0) !== (Number(v2) || 0);
  }
  /**
   * Updates price data in bet
   * @param {object} offeredBet
   * @private
   */
  private updateBetPriceData(offeredBet: IBet): { price: IPrice, priceDec: string } {
    const { priceNum, priceDen, priceTypeRef }: Partial<IPrice> = (offeredBet.leg as ILeg[]).map(leg => leg.sportsLeg.price)[0];
    const priceType = priceTypeRef.id.toString();
    const priceDec = <string>this.fracToDecService.getDecimal(priceNum, priceDen);
    return {
      price: { priceNum, priceDen, priceDec, priceType }, priceDec
    };
  }

  /**
   * Updates betData with bet
   * @param {{betData, bet}} betPair
   * @private
   */
  private updateBetData({ betData, bet }): void {
    betData.betId = bet.id;

    if (bet.isCancelled === 'Y') { // Cancelled
      betData.isTraderDeclined = true;
    } else if (bet.isConfirmed === 'Y') { // Confirmed
      this.updateConfirmedBetData({ betData, bet });
    } else if (bet.isOffer === 'Y') { // Offer
      betData.isTraderOffered = true;

      const originalBet = this.originalPlacedBets[bet.masterBetId || bet.id];
      const offeredBet = bet.offer || bet,
          offeredBetLegs = offeredBet.leg,
          potentialPayout = offeredBet.payout && offeredBet.payout.length && offeredBet.payout[0].potential;

      this.updateOfferedBetData({ betData, originalBet, potentialPayout, offeredBet });

      if (offeredBetLegs.length && this.isPricesChanged(betData, offeredBet.leg)) {
        betData.traderChangedOdds = true;
      }

      const requestedBetLegs = originalBet.leg || [];

      const baseBetType = requestedBetLegs.length && requestedBetLegs[0].sportsLeg.winPlaceRef.id;
      const isBaseEW = ['E', 'EACH_WAY'].includes(baseBetType);

      const offeredBetType = offeredBetLegs[0].sportsLeg.winPlaceRef.id;
      const isOfferedEW = ['E', 'EACH_WAY'].includes(offeredBetType);

      betData.Bet.isEachWay = isOfferedEW;
      betData.traderChangedLegType = isOfferedEW !== isBaseEW;

      if (betData.price) {
        betData.price.priceType = offeredBetLegs[0].sportsLeg.price.priceTypeRef.id;
      }

      betData.isTraderChanged =
          betData.traderChangedPriceType ||
          betData.traderChangedLegType ||
          betData.traderChangedOdds ||
          betData.traderChangedStake;
      betData.isSelected = this.isNotDeletedFromTraderOffer(betData.id);

      betData.overaskMessage = this.localeService.getString('bs.overaskMessages.acceptOffer');
    }
  }

  private updateConfirmedBetData({ betData, bet }): void {
    betData.isTraderAccepted = true;
    betData.isSelected = this.isNotDeletedFromTraderOffer(betData.id);

    if (this.isNoBetsOffered) {
      betData.overaskMessage = this.localeService.getString('bs.overaskMessages.betAccepted');
    }

    if (betData.price) {
      Object.assign(betData, this.updateBetPriceData(bet));
    }
  }

  private updateOfferedBetData({ betData, originalBet, potentialPayout, offeredBet }): void {
    betData.tokenValue = originalBet && originalBet.tokenValue;
    betData.tokenValue = Number(betData.tokenValue) || 0;

    // in the overask freebet value is included to potentialPayout
    betData.potentialPayout = potentialPayout ? Number(potentialPayout) : 'N/A';

    // update bet price anyway to get actual data from OB

    if (betData.price) {
      Object.assign(betData, this.updateBetPriceData(offeredBet));
    }

    betData.traderChangedStake = this.isNumbersDifferent(originalBet.stake.stakePerLine || 0, offeredBet.stake.stakePerLine);
    betData.Bet.stake = Number(offeredBet.stake.stakePerLine) || 0;

    const isOfferedSP = offeredBet.leg.map(leg => leg.sportsLeg.price.priceTypeRef.id).includes('SP');
    betData.isSP = originalBet.leg.map(leg => leg.sportsLeg.price.priceTypeRef.id).includes('SP');

    if (!isOfferedSP && betData.isSP) {
      betData.isSP = false;
      betData.isSPLP = false;
      betData.traderChangedPriceType = true;
    } else if (isOfferedSP && !betData.isSP) {
      betData.isSP = true;
      betData.isSPLP = false;
      betData.traderChangedPriceType = true;
    }
  }

  /**
   * Checks is bet has freebet and changed stake
   * @param {{betData, bet}}
   * @returns {boolean}
   * @private
   */
  /**
   * Checks is bet has freebet and changed stake
   * @param {{betData, bet}}
   * @returns {boolean}
   * @private
   */
  private isBetDataWithFreeBetAndChangedStake({ betData, bet }: IBetslipPairs): boolean {
    const originalBet = this.originalPlacedBets[bet.masterBetId || bet.id];
    return BetslipBetDataUtils.isFreeBetUsed(betData)
      && BetUtils.isOffer(bet)
      && this.isNumbersDifferent(originalBet.stake.stakePerLine, (bet.stake as IStake).stakePerLine);
  }

  /**
   * Checks is any bet has freebet and changed stake
   * @param {{betData, bet}[]} betPairs
   * @returns {boolean}
   * @private
   */
  private isBetsDataWithFreeBetAndChangedStake(betPairs: IBetslipPairs[]): boolean {
    return _.some(betPairs, betPair => this.isBetDataWithFreeBetAndChangedStake(betPair));
  }

  /**
   * Checks is match bets to betsData not success and stop overask process
   * @param betPairs
   * @returns {boolean}
   * @private
   */
  private checkIsMatchBetsToBetsDataNotSuccess(betPairs: IBetslipPairs[]): boolean {
    const result = this.isBetsDataAssigned &&
        betPairs.length !== this.placeBetsData.bets.length;

    if (result) {
      console.warn('Overask', 'Data not matched');
      this.setStateAndClearInStorage(this.states.off);
    }

    return result;
  }

  /**
   * Updates betsData model with placeBetsData
   * @private
   */
  private updateBetsData(): void {
    const betPairs = this.matchBetsToBetsData();
    if (this.checkIsMatchBetsToBetsDataNotSuccess(betPairs)) {
      return;
    }

    if (this.isBetsDataWithFreeBetAndChangedStake(betPairs)) {
      _.chain(betPairs) // clear freeBets
        .filter((betPair: IBetslipPairs) => this.isBetDataWithFreeBetAndChangedStake(betPair))
        .each((betPair: IBetslipPairs) => {
          betPair.betData.selectedFreeBet = null;
          betPair.betData.Bet.freeBet = null;
          betPair.betData.stake.freeBetAmount = undefined;
          betPair.betData.freeBetText = this.localeService.getString('bs.freeBetsAvalaible');
          this.betslipStorageService.setFreeBet(betPair.betData);
          this.pubSubService.publish(this.pubSubService.API.BETSLIP_CLEAR_STAKE, betPair.betData.id);
      });

      this.rejectOffer(true, false).subscribe(() => {
        this.stateMessage = this.localeService.getString('bs.overaskMessages.someBetsWithFreebet');
      });
      return;
    }

    _.each(betPairs, betPair => this.updateBetData(betPair));
  }

  /**
   * If overask is in progress
   *  Some type of errors are ignored and cleared
   */
  private resetInProcessErrors(): void {
    const errorsToIgnore = [
      BETSLIP_VALUES.ERRORS.EVENT_STARTED,
      BETSLIP_VALUES.ERRORS.PRICE_CHANGED
    ];

    if (this.isInProcess) {
      this.betsData // TODO refactor?
        .filter((bet: IBetslipBetData) => _.contains(errorsToIgnore, bet.error) ||
            _.contains(errorsToIgnore.map(errKey => this.localeService.getString(`bs.${errKey}`)), bet.errorMsg)
        )
        .forEach((bet: IBetslipBetData) => {
          bet.disabled = false;
          bet.error = '';
          bet.errorMsg = '';
        });
    }
  }

  private triggerRestoreStateIfLoggedIn(): void {
    this.authService.sessionLoggedIn
      .pipe(takeUntil(this.destroyed$))
      .subscribe(() => {
        this.sessionService.whenProxySession()
          .then(() => { this.restoreState(); })
          .catch(err => console.warn(err));
      });
  }

  /**
   * Check '9516 - PT_ERR_AUTH coral::bet::pre_place_bets_callback: funds reservation failed: PT_ERR_AUTH' error
   * Check '508 - LOW_FUNDS ob_bet::resolve_async_bets: Failed to resolve async bets' error
   *
   * @param err
   * @returns IError | undefined
   */
  private checkError(err): IError | undefined {
    if (err && err.error && typeof err.error.error === 'string' &&
      ((err.error.error.includes('PT_ERR_AUTH')) || (err.error.error.includes('LOW_FUNDS')))) {
      const status = err.error.error.includes('PT_ERR_AUTH') ? 'PT_ERR_AUTH' : 'LOW_FUNDS';
      return {
        data: {
          status,
          message: this.localeService.getString(`bs.overaskMessages.${status}`)
        }
      };
    }
  }
}
