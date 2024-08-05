import { mergeMap, map, shareReplay, switchMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Observable, of as observableOf, Observer, from as fromPromise, Subject } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IGtmOrigin } from '@core/services/gtmTracking/models/gtm-origin.model';

import { QuickbetSelectionBuilder } from '@app/quickbet/services/quickbetSelectionBuilder/quickbet-selection-builder.service';
import { QuickbetUpdateService } from '@app/quickbet/services/quickbetUpdateService/quickbet-update.service';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IQuickbetRequestModel } from '@app/quickbet/models/quickbet-selection-request.model';
import { IQuickbetStoredStateModel } from '@app/quickbet/models/quickbet-stored-state.model';
import { IQuickbetRestoredDataModel } from '@app/quickbet/models/quickbet-restored-data.model';
import { IRemoteBetslipBet } from '@core/services/remoteBetslip/remote-betslip.constant';
import { IQuickbetReceiptDetailsModel,
         IQuickbetReceiptErrorModel,
         IQuickbetReceiptLegPartsModel,
         IQuickbetReceiptStakeModel } from '@app/quickbet/models/quickbet-receipt.model';
import { IQuickbetSelectionPriceModel } from '@app/quickbet/models/quickbet-selection-price.model';
import { TemplateService } from '@app/shared/services/template/template.service';
import { IOddsBoostConfig } from '@core/services/cms/models';
import { OB_BET_NOT_PERMITTED } from '@core/constants/error-dictionary.constant';
import { CHANNEL } from '@shared/constants/channel.constant';
import { StorageService } from '@core/services/storage/storage.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
export interface SbQbReceiptData {
  stake: string, 
  returns: string, 
  odds: string,
  freeBetData: SbQbFreeBetData
}

export interface SbQbFreeBetData {
  hasFreebet: boolean,
  selection: IQuickbetSelectionModel,
  betReceipt: IQuickbetReceiptDetailsModel
}
@Injectable({ providedIn: 'root' })
export class QuickbetService {
  /**
   * Selection data from remoteBetslip MS.
   * @type {null}
   */
  selectionData: IQuickbetSelectionModel = null;

  dynamicGtmObj: IGtmOrigin;

  quickBetOnOverlayCloseSubj: Subject<string> = new Subject<string>();

  qbReceiptDataSubj: Subject<SbQbReceiptData> = new Subject<SbQbReceiptData>();

  _racingPostGTM: IGtmOrigin;
  /**
   * Selection data returned after restoring session with BetslipMS.
   * @type {Object=}
   * @private
   */
  private restoredSelection: IQuickbetSelectionModel = null;
  private sessionStrUpdateTimeout: number = null;
  private currentPanelStateObj: IQuickbetStoredStateModel = null;
  private qbSessionStorageKey: string = 'quickbetSelection';
  private reboost: boolean = false;
  private _racingPostTip: IQuickbetSelectionModel;

  constructor(private pubSubService: PubSubService,
              private userService: UserService,
              private localeService: LocaleService,
              private deviceService: DeviceService,
              private quickbetSelectionBuilder: QuickbetSelectionBuilder,
              private quickbetUpdateService: QuickbetUpdateService,
              private sessionStorageService: SessionStorageService,
              private commandService: CommandService,
              private remoteBetslipService: RemoteBetslipService,
              private infoDialogService: InfoDialogService,
              private cmsService: CmsService,
              private awsService: AWSFirehoseService,
              private windowRefService: WindowRefService,
              private templateService: TemplateService,
              private storageService: StorageService,
              private http: HttpClient,
  ) { }

  set racingPostTip(value: IQuickbetSelectionModel) {
    this._racingPostTip = value;
  }

  get racingPostTip() {
    return this._racingPostTip;
  }

  /**
   * Method used for showing quickbet panel with selection by given outcome ID.
   * Used by command to lazyload and render quickbet.
   * @param {Object} selectionData
   * @return {Promise}
   */
  showQuickbet(selectionData: IQuickbetSelectionModel, dynamicGtmObj?: IGtmOrigin): Observable<void> {
    const observable = Observable.create((observer: Observer<{}>) => {
      if (!this.deviceService.isOnline()) {
        this.infoDialogService.openConnectionLostPopup();
        observer.error({});
        observer.complete();
      } else {
        this.renderComponent(selectionData);

        if(!!dynamicGtmObj) {
          this.dynamicGtmObj = dynamicGtmObj;
        }
        observer.next({});
        observer.complete();
      }
    });

    return observable.toPromise();
  }

  /**
   * Adds selection by outcome ID.
   * @param {IQuickbetRequestModel} requestData
   * @param {IQuickbetSelectionPriceModel} originalPrice
   * @returns {Observable}
   */
  makeAddSelectionRequest(requestData: IQuickbetRequestModel,
                          originalPrice?: IQuickbetSelectionPriceModel, isStreamBet: boolean = false): Observable<IQuickbetSelectionModel | IQuickbetRestoredDataModel> {
    const dataObject = {...requestData, isStreamBet}
    return this.remoteBetslipService.addSelection(dataObject).pipe(
      map((selection: IQuickbetRestoredDataModel = {}) => {
        const data = selection.data || {};
        let newPrice;

        if (data.error) {
          return selection;
        }

        if (originalPrice) {
          newPrice = Object.assign({}, data.selectionPrice);
          data.selectionPrice = originalPrice;
        }

        this.selectionData = this.quickbetSelectionBuilder.build(data, this.getStoredSelectionState());

        this.quickbetUpdateService.saveSelectionData(this.selectionData);

        if (originalPrice) {
          this.quickbetUpdateService.updateOutcomePrice(newPrice);
        }

        return this.selectionData;
      }));
  }

  /**
   * Wrap selection to lazyload oddsboost only if user is logged in.
   * @param {IQuickbetRequestModel} requestData
   * @param {IQuickbetSelectionPriceModel} originalPrice
   * @returns {Observable}
   */
  addSelection(requestData: IQuickbetRequestModel,
               originalPrice?: IQuickbetSelectionPriceModel,
               isLD ?: boolean, isStreamBet: boolean = false): Observable<IQuickbetSelectionModel | IQuickbetRestoredDataModel> {
    return this.canUseOddsBoost().pipe(
      mergeMap((oddsBoost: boolean) => {
        requestData.oddsBoost = isLD ? false : oddsBoost;
        if (this.userService.bppToken) {
          requestData.token = this.userService.bppToken;
        }
        return this.makeAddSelectionRequest(requestData, originalPrice, isStreamBet);
      })
    );
  }

  /**
   * Removes quickbet active selection.
   */
  removeSelection(selectionData: IQuickbetSelectionModel, isAddToBetslip: boolean = false): void {
    if (selectionData) {
      this.pubSubService.publish(this.pubSubService.API.REMOVE_FROM_QUICKBET, {
        outcomeId: `${selectionData.requestData.outcomeIds[0]}`,
        isAddToBetslip
      });
    }
    this.selectionData = null;
    this.remoteBetslipService.removeSelection();
  }

  /**
   * Stores previously selected selection returned after MS connection.
   * @param {Object} selection
   */
  restoreSelection(selection: IQuickbetRestoredDataModel = {}): void {
    const data = selection.data || {};
    const isLD = this.checkIfLdmarketExists(selection);
    if (!data.error && !isLD ) {
      this.restoredSelection = this.selectionData =
        this.quickbetSelectionBuilder.build(data, this.getStoredSelectionState());
      this.quickbetUpdateService.saveSelectionData(this.selectionData);

      this.renderComponent();
    }
  }

  /**
   * Returns re-stored selection from previous MS session
   * @return {Object}
   */
  getRestoredSelection(): IQuickbetSelectionModel {
    return this.restoredSelection;
  }

  /**
   * Place bet
   * @param {Object} bet
   * @returns {Observable<IQuickbetReceiptModel>}
   */
  placeBet(bet: IRemoteBetslipBet): Observable<IQuickbetReceiptDetailsModel[] | IQuickbetReceiptErrorModel> {
    const observable = Observable.create((observer: Observer<IQuickbetReceiptDetailsModel[] | IQuickbetReceiptErrorModel>) => {
      this.awsService.addAction('quickBetService=>placeBet=>Start', { date: new Date().getTime() });
      return this.placeBetRequest(bet)
        .subscribe(result => {
            this.awsService.addAction('quickBetService=>placeBet=>Success', { date: new Date().getTime() });
            const tooltipData = this.storageService.get('tooltipsSeen') || {};
            const receiptViewsCounter = (tooltipData[`receiptViewsCounter-${this.userService.username}`] || null);
            tooltipData[`receiptViewsCounter-${this.userService.username}`] = receiptViewsCounter === null ? 1 : receiptViewsCounter + 1;
            this.storageService.set('tooltipsSeen', tooltipData);
            observer.next(result);
            observer.complete();
          },
          (error: IQuickbetReceiptErrorModel) => {
            this.awsService.addAction('quickBetService=>placeBet=>error', error);
            if (error.code === 'UNAUTHORIZED_ACCESS' || error.subErrorCode === 'EXTERNAL_FUNDS_UNAVAILABLE') {
              this.awsService.addAction('quickBetService=>placeBet=>ErrorRetry', error);
              // TODO: substitute promise what command will be migrated to observable
              if (!_.isEmpty(this.getStoredSelectionState())) {
                fromPromise(this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE)).pipe(
                  switchMap(() => {
                    bet.token = this.userService.bppToken;
                    this.awsService.addAction('quickBetService=>placeBet=>Error=>bppTokenUpdate', { bet: error });
                    return this.placeBetRequest(bet);
                  }))
                  /* eslint-disable */
                  .subscribe((result) => {
                    observer.next(result);
                    observer.complete();
                    }, (err) => {
                    observer.error(err);
                    observer.complete();
                   });
                  /* eslint-enable */
              }
            } else {
              observer.error(error);
              observer.complete();
            }
          });
    });

    return observable.pipe(
      shareReplay(1)
    );
  }

  /**
   * Save quickbet selection state to session storage/
   * @param {Object} qbPanelValues
   */
  saveQBStateInStorage(qbPanelValues: IQuickbetStoredStateModel = { userEachWay: false, userStake: null }): void {
    this.currentPanelStateObj = qbPanelValues;
    if (!this.sessionStrUpdateTimeout) {
      const interval = 500;
      this.sessionStrUpdateTimeout = this.windowRefService.nativeWindow.setTimeout(() => {
        this.sessionStorageService.set(this.qbSessionStorageKey, this.currentPanelStateObj);
        this.sessionStrUpdateTimeout = null;
      }, interval);
    }
  }

  /**
   * Remove quickbet selection state from session storage
   */
  removeQBStateFromStorage(): void {
    this.windowRefService.nativeWindow.clearTimeout(this.sessionStrUpdateTimeout);
    this.sessionStrUpdateTimeout = null;
    this.sessionStorageService.remove(this.qbSessionStorageKey);
  }

  /**
   * Get odds in correct format
   * @param {Object} price
   * @param {string=} format
   * @returns {string}
   */
  getOdds(price: IQuickbetSelectionPriceModel, format: string = ''): string {
    return this.quickbetUpdateService.getOdds(price, format);
  }

  /**
   * Handle bet placement error and return proper error message
   * @param {Object} error
   * @param {Object} selection
   * @param {boolean} doUpdate
   * @returns {string}
   */
  getBetPlacementErrorMessage(error: IQuickbetReceiptErrorModel, selection: IQuickbetSelectionModel, doUpdate: boolean = false): string {
    const KEY_NOT_FOUND = 'KEY_NOT_FOUND';
    const errorCode = error.subErrorCode || error.code,
      specificErrorsHandling = {
        PRICE_CHANGED: this.handlePriceErrorMessage.bind(this),
        HANDICAP_CHANGED: this.handleHandicapErrorMessage.bind(this),
        STAKE_TOO_LOW: this.handleStakeTooLowErrorMessage.bind(this),
        STAKE_TOO_HIGH: this.handleStakeTooHighErrorMessage.bind(this),
        SERVICE_ERROR: this.handleTimeoutErrorMessage.bind(this),
        INTERNAL_PLACE_BET_PROCESSING: this.handleTimeoutErrorMessage.bind(this),
        BAD_FREEBET_TOKEN: this.handleBadFreebetTokenMessage.bind(this)
      }[errorCode],
      noCodeError = this.localeService.getString(`quickbet.betPlacementErrors.${error.description}`);

    let errorMessage: string = this.localeService.getString(`quickbet.betPlacementErrors.${errorCode}`);

    if (specificErrorsHandling) {
      errorMessage = specificErrorsHandling(error, selection, doUpdate);
    } else if (errorMessage === KEY_NOT_FOUND) {
      this.awsService.addAction('quickBetService=>placeBet=>undefined_errors', {
        error: JSON.stringify(error)
      });
      errorMessage = this.localeService.getString(`quickbet.betPlacementErrors.DEFAULT_PLACEBET_ERROR`);
    }

    if (noCodeError !== KEY_NOT_FOUND) {
      errorMessage = noCodeError;
    }

    if (this.isBetNotPermittedError(error)) {
      errorMessage = this.getBetNorPermittedError();
    }

    return errorMessage;
  }

  /**
   * Check if it is virtual sport
   * @param categoryName
   */
  isVirtualSport(categoryName: string): boolean {
    return categoryName === 'Virtual Sports';
  }

  acceptChangedBoost(): boolean {
    if (this.reboost) {
      this.reboost = false;
      return true;
    }
  }

  activateReboost(): void {
    this.reboost = true;
  }

  getEWTerms(legPart: IQuickbetReceiptLegPartsModel): string {
    return legPart.eachWayNum ? this.localeService.getString('quickbet.oddsAPlaces', {
      num: legPart.eachWayNum,
      den: legPart.eachWayDen,
      arr: this.templateService.genEachWayPlaces(legPart, true)
    }) : '';
  }

  getLinesPerStake(stake: IQuickbetReceiptStakeModel): string {
    return this.localeService.getString('quickbet.linesPerStake', {
      lines: Number(stake.amount) / Number(stake.stakePerLine),
      stake: this.userService.currencySymbol + Number(stake.stakePerLine).toFixed(2)
    });
  }

  isBetNotPermittedError(error: IQuickbetReceiptErrorModel): boolean {
    return (
      !error.code && !error.subErrorCode && error.description &&
      error.description.toLowerCase() === OB_BET_NOT_PERMITTED
    );
  }

  getBetNorPermittedError(): string {
    return this.localeService.getString('quickbet.betPlacementErrors.BET_NOT_PERMITTED');
  }

  getBybSelectionType(channel: string): string {
    if (channel === CHANNEL.fiveASide) {
      return this.localeService.getString('quickbet.bybType.fiveASide');
    } else if (channel === CHANNEL.byb) {
      return this.localeService.getString('quickbet.bybType.byb');
    } else {
      return '';
    }
  }

  /**
   * Perform request
   * @param {Object} bet
   * @returns {Observable<IQuickbetReceiptModel>}
   */
  private placeBetRequest(bet: IRemoteBetslipBet):
            Observable<IQuickbetReceiptDetailsModel[] | IQuickbetReceiptErrorModel> {
    return Observable.create((observer: Observer<IQuickbetReceiptDetailsModel[] | IQuickbetReceiptErrorModel>) => {
      this.remoteBetslipService.placeBet(bet)
        .subscribe(response => {
          const {receipt, error}: { receipt: IQuickbetReceiptDetailsModel[], error: IQuickbetReceiptErrorModel } = response.data;
          if (receipt) {
            observer.next(receipt);
            observer.complete();
            return;
          }

          observer.error(error);
          observer.complete();
        }, error => {
          observer.error(error.data.error);
          observer.complete();
        });
    }).pipe(
      shareReplay(1)
    );
  }

  /**
   * Renders Quickbet component after loading Quickbet sources and adding first selection to Quickbet
   * @private
   */
  private renderComponent(selectionData?: IQuickbetSelectionModel): void {
    if (selectionData) {
      this.pubSubService.publishSync(this.pubSubService.API.ADD_TO_QUICKBET, selectionData);
    }

    this.pubSubService.publishSync(this.pubSubService.API.RENDER_QUICKBET_COMPONENT, selectionData);
  }

  /**
   * Get Quickbet selection state from session storage.
   * @return {Object}
   * @private
   */
  private getStoredSelectionState(): IQuickbetStoredStateModel {
    return this.sessionStorageService.get(this.qbSessionStorageKey) || {};
  }

  /**
   * Handle handicap change error message.
   * @param {Object} error
   * @param {Object} selection
   * @param {boolean} doUpdate
   * @returns {string}
   * @private
   */
  private handleHandicapErrorMessage(error: IQuickbetReceiptErrorModel, selection: IQuickbetSelectionModel, doUpdate: boolean): string {
    const newHandicap = selection.formatHandicap(error.handicap);

    if (doUpdate) {
      selection.updateHandicapValue(newHandicap);
    }
    return this.localeService.getString('quickbet.betPlacementErrors.HANDICAP_CHANGED',
      [selection.oldHandicapValue, selection.handicapValue]);
  }

  /**
   * Handle handicap change error message (stake too low)
   * @param {Object} error
   * @returns {string}
   * @private
   */
  private handleStakeTooLowErrorMessage(error: IQuickbetReceiptErrorModel): string {
    return this.localeService
      .getString('quickbet.betPlacementErrors.STAKE_LOW', [this.userService.currencySymbol, error.stake.minAllowed]);
  }

  /**
   * Handle handicap change error message (stake too high)
   * @param {Object} error
   * @returns {string}
   * @private
   */
  private handleStakeTooHighErrorMessage(error: IQuickbetReceiptErrorModel): string {
    return this.localeService
      .getString('quickbet.betPlacementErrors.STAKE_HIGH', [this.userService.currencySymbol, error.stake.maxAllowed]);
  }

  /**
   * Handle price change error message
   * @param {Object} error
   * @param {Object} selection
   * @param {boolean} doUpdate
   * @returns {string}
   * @private
   */
  private handlePriceErrorMessage(error: IQuickbetReceiptErrorModel, selection: IQuickbetSelectionModel, doUpdate: boolean): string {
    if (doUpdate) {
      this.quickbetUpdateService.updateOutcomePrice(error.price);
    }
    const oldPrice = this.getOdds(selection.oldPrice || selection.price),
      newPrice = this.getOdds(error.price);

    return this.localeService.getString('quickbet.betPlacementErrors.PRICE_CHANGED', [oldPrice, newPrice]);
  }

  /**
   * Handle timeout error message
   * @returns {string}
   * @private
   */
  private handleTimeoutErrorMessage(): string {
    return this.localeService.getString('quickbet.betPlacementErrors.TIMEOUT_ERROR');
  }

  private handleBadFreebetTokenMessage(error: IQuickbetReceiptErrorModel, selection: IQuickbetSelectionModel): string {
    return this.localeService.getString(
      selection.isBoostActive ?
        'quickbet.oddsBoostExpiredOrRedeemed' : 'quickbet.betPlacementErrors.BAD_FREEBET_TOKEN'
    );
  }

  private canUseOddsBoost(): Observable<boolean> {
    // User might be logged into at Vanilla but BPP User call is failed
    if (!this.userService.status || !this.userService.bppToken) {
      return observableOf(false);
    }

    return this.cmsService.getOddsBoost().pipe(
      map((config: IOddsBoostConfig) => config.enabled)
    );
  }

  readUpCellBets(url, body): Observable<any>{
    const headers =  new HttpHeaders({
      token: this.userService.bppToken
    });
    return this.http.post<any[]>(url, body, { headers });
  }

  /**  To check if ld marlet tag is configures
  @returns {boolean} 
  */
private checkIfLdmarketExists(selection):boolean{
  return selection.data.event.markets.find(market => market && market.drilldownTagNames &&  market.drilldownTagNames.indexOf('MKTFLAG_LD') != -1);
}
}



