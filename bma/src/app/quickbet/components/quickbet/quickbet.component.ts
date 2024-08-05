import { switchMap } from 'rxjs/operators';
import { Component, Input, OnDestroy, OnInit, ChangeDetectorRef, Output, EventEmitter } from '@angular/core';
import { Subscription, from as fromPromise } from 'rxjs';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { DeviceService } from '@core/services/device/device.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetOveraskService } from '@app/quickbet/services/quickbetOveraskService/quickbet-overask.service';
import { QuickbetDataProviderService } from '@app/core/services/quickbetDataProviderService/quickbet-data-provider.service';

import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IBetslipSelection, IQuickbetOverlayStateModel } from '@app/quickbet/models/quickbet-common.model';
import { IGtmEventModel } from '@app/quickbet/models/quickbet-gtm-event.model';
import { IQuickbetRequestModel } from '@app/quickbet/models/quickbet-selection-request.model';
import { IQuickbetReceiptDetailsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { IQuickbetSelectionResponseModel } from '@app/quickbet/models/quickbet-selection-response.model';
import { IQuickbetOveraskResponseModel } from '@app/quickbet/models/quickbet-overask-response.model';
import { IQuickbetRestoredDataModel } from '@app/quickbet/models/quickbet-restored-data.model';
import { IRemoteBetslipBet, BETSLIP } from '@core/services/remoteBetslip/remote-betslip.constant';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { QuickbetDepositService } from '@quickbetModule/services/quickbetDepositService/quickbet-deposit.service';
import { UserService } from '@core/services/user/user.service';
import { IQuickbetSelectionPriceModel } from '@app/quickbet/models/quickbet-selection-price.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { IConstant } from '@core/services/models/constant.model';
import { IClaimedOffer } from '@bpp/services/bppProviders/bpp-providers.model';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';
import { IGtmOrigin } from '@app/core/services/gtmTracking/models/gtm-origin.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { GA_TRACKING } from '@app/shared/constants/channel.constant';
import { ILuckyDipFieldsConfig } from '@app/lazy-modules/luckyDip/models/luckyDip';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';
import { StorageService } from '@core/services/storage/storage.service';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';

@Component({
  selector: 'quickbet',
  templateUrl: 'quickbet.component.html'
})
export class QuickbetComponent implements OnInit, OnDestroy {
  @Input() selection?: IQuickbetSelectionResponseModel;
  @Input() quickDepositFormExpandedInput?: boolean;
  @Input() isLuckyDip?: boolean;
  @Input() luckyDipCmsData?: ILuckyDipFieldsConfig;
  @Input() luckyDipMarketName?: string;
  @Output() readonly placeBetFn: EventEmitter<any> = new EventEmitter();
  @Output() readonly closePanelFn: EventEmitter<any> = new EventEmitter();
  @Input() luckyDipData?: any;
  @Input() betslipType: string;
  selectionData: IQuickbetSelectionModel = null;
  panelTitle: string;
  trackObj;
  _racingPostGA: IGtmOrigin;
  isWSdisabled: boolean = false;
  categoryName: string = '';
  ecommerceObj;
  scorecastData;
  tag = 'Quickbet';
  readonly claimedOffers = 'claimedOffers';
  readonly claimed = 'claimed';
  private stakeFromQb:number=0
  private quickbetPlaceBetSubscriber: Subscription;
  private betIsPlaced: boolean;
  private loadingSelection: boolean = false;
  private betplacementProcess: boolean = false;
  private isUnauthorizedError: boolean = false;  
  private digitKeyBoardStatus:boolean=false
  isBetPlaceClicked: boolean;
  // scorecastData: any

  constructor(private locale: LocaleService,
    protected pubsub: PubSubService,
    private gtm: GtmService,
    public quickbetService: QuickbetService,
    private remoteBsService: RemoteBetslipService,
    private quickbetOverAskService: QuickbetOveraskService,
    protected command: CommandService,
    protected dialogService: DialogService,
    protected infoDialogService: InfoDialogService,
    public device: DeviceService,
    private nativeBridgeService: NativeBridgeService,
    private location: Location,
    private quickbetDataProviderService: QuickbetDataProviderService,
    private rendererService: RendererService,
    private windowRef: WindowRefService,
    private gtmTrackingService: GtmTrackingService,
    private quickbetDepositService: QuickbetDepositService,
    private quickbetNotificationService: QuickbetNotificationService,
    private awsService: AWSFirehoseService,
    private changeDetectorRef: ChangeDetectorRef,
    private userService: UserService,
    private sessionStorage: SessionStorageService,
    private racingPostTipService: RacingPostTipService,
    private arcUserService: ArcUserService,
    protected storageService: StorageService,
    protected betslipService:BetslipService,
    protected scorecastDataService: ScorecastDataService
    ) {
    this.addSelectionHandler = this.addSelectionHandler.bind(this);
  }

  ngOnInit(): void {
    this.setTagforLd();
    this.panelTitle = this.locale.getString('quickbet.quickbetTitle');
    this.pubsub.subscribe(this.tag, this.pubsub.API.REMOTE_BETSLIP_OVERASK_TRIGGERED, (responseData: IQuickbetOveraskResponseModel) => {
      const selectionData = this.quickbetService.selectionData;
      this.closePanel();
      this.quickbetOverAskService.execute(responseData, selectionData);
    });

    this.pubsub.subscribe(this.tag, this.pubsub.API.DEVICE_VIEW_TYPE_CHANGED_NEW, (deviceType: string) => {
      if (this.selectionData && deviceType !== 'mobile') {
        this.addToBetslip();
      }
    });

    // Remove active focus when keyboard is hidden
    this.pubsub.subscribe(this.tag, this.pubsub.API.DIGIT_KEYBOARD_HIDDEN, () => {
      const element = this.windowRef.document.querySelector('.quickbet-content .stake-input');
      if (element) {
        this.rendererService.renderer.removeClass(element, 'dk-active-input');
      }
    });

    this.pubsub.subscribe(this.tag, this.pubsub.API.GET_QUICKBET_SELECTION_STATUS, (...args) => {
      if (this.selectionData) {
        this.selectionData.setStatus(args[0], args[1]);

        if (!this.selectionData.disabled) {
          this.quickbetDepositService.update(this.selectionData.stake);
        }
        this.changeDetectorRef.detectChanges();
      }
    });

    this.pubsub.subscribe(this.tag, this.pubsub.API.RELOAD_COMPONENTS, () => {
      this.remoteBsService.disconnect();
      this.dialogService.closeDialogs();

      if (this.selectionData) {
        this.remoteBsService.connect()
          .subscribe(() => {
            if (this.betplacementProcess) {
              this.betplacementProcess = false;
              this.extendSelectionDataWithError('SERVER_ERROR', this.selectionData.requestData, 'TIMEOUT_ERROR');
            } else {
              this.reuseSelection(this.selectionData.requestData);
            }
          }, () => {
            this.selectionData = _.extend({}, {
              error: { code: 'SERVER_ERROR' },
              requestData: this.selectionData.requestData
            });
          });
      } else {
        this.closePanel();
      }
    });

    this.pubsub.subscribe(this.tag, this.pubsub.API.REMOTE_BS_RECONNECT, () => {
      if (!this.selection.skipOnReconnect) {
        this.addSelectionHandler(this.selection);
      }
    });

    this.pubsub.subscribe(this.tag, this.pubsub.API.REUSE_QUICKBET_SELECTION, requestData => {
      this.reuseSelection(requestData);
    });
    this.pubsub.subscribe(this.tag, this.pubsub.API.ADD_TO_QUICKBET, (selection: IQuickbetSelectionResponseModel) => {
      if (selection && !selection.isStreamBet) {
        this.addSelectionHandler(selection);
      }
    });
    if(!this.selection || (this.selection && !this.selection.isStreamBet)) {
      
      this.placeBetListener();
      
      if (this.selection) {
        this.addSelectionHandler(this.selection);
      } else {
        this.restoreSelection();
      }
    }
    this.pubsub.subscribe('quickbet_quickStake', this.pubsub.API.QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD, () => {
      this.stakeFromQb = this.digitKeyBoardStatus?2:1;
    });
    this.pubsub.subscribe('quickbet_keyBoardPress', this.pubsub.API.DIGIT_KEYBOARD_KEY_PRESSED, () => {
      this.stakeFromQb = 0;
    });
    this.pubsub.subscribe('qucikbet_digit_status', this.pubsub.API.LUCKY_DIP_KEYPAD_PRESSED, (status) => {
      this.digitKeyBoardStatus =this.isBetPlaceClicked?this.digitKeyBoardStatus:!status;
    })

    this.quickbetService.quickBetOnOverlayCloseSubj.subscribe((qbStatusMsg: string) => {
      if (this.selection && this.selection.isStreamBet && qbStatusMsg === 'fullscreen exit') {
        this.closePanel();
      }
    });
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.tag);
    this.removeSubscribers();
  }

  get SIMPLE_SELECTION_TYPE(): string {
    return 'simple';
  }
  set SIMPLE_SELECTION_TYPE(value: string) { }

  addSelectionHandler(selection: IQuickbetSelectionResponseModel) {
    const requestParams = {
      outcomeIds: _.pluck(selection.outcomes, 'id'),
      selectionType: this.getSelectionType(selection.type),
      additional: selection.additional,
      gtmTracking: selection.GTMObject && selection.GTMObject.tracking
    };
    const originalPrice = this.getOriginalPrice(selection);

    const isLd = selection &&  selection.details && selection.details.marketDrilldownTagNames && selection.details.marketDrilldownTagNames.includes('MKTFLAG_LD');
    this.addSelection(requestParams, originalPrice, isLd, selection.isStreamBet);
  }

  /**
   * Place regular bet handler.
   * @returns {void}
   */
  placeBet(): void {
    this.isBetPlaceClicked=true;
  this.scorecastData = this.scorecastDataService.getScorecastData();
    this._racingPostGA = this.racingPostTipService.racingPostGTM;
    const inPlayStatus = this.selectionData.isStarted ? 'yes' : 'no',
      isFreebetUsed = this.selectionData.freebetValue > 0;
    this.quickbetService.racingPostTip = this.selectionData;
    this.ecommerceObj = {
      ecommerce: {
      add: {
        products: [
          {
            dimension86: 0,
            dimension87: 0,
            dimension88: null,
            quantity: 1,
            name: this.scorecastData.name,
            category: 16,
            variant: 1935,
            brand: "Match Betting",
            dimension60: this.scorecastData.dimension60,
            dimension61: this.scorecastData.dimension61,
            dimension62: this.scorecastData.dimension62,
            dimension63: 0,
            dimension64:  this.scorecastData.dimension64,
            dimension65: "edp",
            dimension66: 1,
            dimension67: 81,
            dimension180: `scorecast;${this.scorecastData.teamname};${this.scorecastData.playerName};${this.scorecastData.result}`,
            metric1: 0,
          },
        ],
      },
      
    }
   
  }
    this.command.executeAsync(this.command.API.GET_LIVE_STREAM_STATUS, undefined, false)
      .then((streamData: { streamID: string; streamActive: boolean; }) => {
        let tracking = this.gtmTrackingService.getTracking();
        if (this._racingPostGA && Object.keys(this._racingPostGA).length) {
          Object.assign(tracking, {
            location: this._racingPostGA.location,
            module: this._racingPostGA.module
          });
        }
        if (!tracking && !!this.quickbetService.dynamicGtmObj) {
          tracking = {
            location: this.quickbetService.dynamicGtmObj.location,
            module: this.quickbetService.dynamicGtmObj.module
          }
        }
        else if (!!tracking && !!this.quickbetService.dynamicGtmObj) {
          tracking.location = this.quickbetService.dynamicGtmObj.location;
          tracking.module = this.quickbetService.dynamicGtmObj.module
        }
        if (tracking) {
          this.trackObj = {
            eventAction: 'place bet',
            ecommerce: {
              purchase: {
                   actionField: {},
                products: [{
                  dimension64: tracking.location,
                  dimension65: tracking.module
                }]
              }
            }
          };
        } else {
          this.trackObj = {
            eventAction: 'place bet',
            betType: 'single',
            betCategory: this.selectionData.categoryName.toLowerCase(),
            betInPlay: inPlayStatus,
            bonusBet: `${isFreebetUsed}`,
            location: this.location.path(),
            customerBuilt: this.selectionData.isYourCallBet ? 'Yes' : 'No',
          };
        }
        if (streamData.streamID) {
          _.extend(this.trackObj, {
            streamActive: streamData.streamActive,
            streamID: streamData.streamID
          });
        }
      });

    // subscribe to place bet listener when err has occurred during bet placement
    if (this.betIsPlaced) {
      this.placeBetListener();
      this.betIsPlaced = false;
    }
  }

  /**
   * Closes quickbetPanel
   * {boolean} isAddToBetslip
   */
  closePanel(isAddToBetslip: boolean = false): void {
    const isAddToBetslip1 = this.isLuckyDip ? false : isAddToBetslip;
    if(!this.selection || (this.selection && !this.selection.isStreamBet)) {
      this.quickbetService.removeSelection(this.selectionData, isAddToBetslip1);
    } else {
      this.selection = null;
    }
    this.selectionData = null;
    if (this.selection) {
      this.selection.skipOnReconnect = true;
    }
    this.toggleLoadingOverlay({ spinner: false, overlay: false });
    this.pubsub.publish(this.pubsub.API.QUICKBET_PANEL_CLOSE, isAddToBetslip1);
    this.quickbetService.removeQBStateFromStorage();
    this.removeSubscribers();
    this.changeDetectorRef.detectChanges();
    this.isUnauthorizedError = false;
    this.closePanelFn.emit();
  }

  /**
   * Reuse selection handler.
   * @param {Object} requestData
   */
  reuseSelection(requestData: IQuickbetRequestModel): void {
    this.toggleLoadingOverlay({ spinner: true, overlay: true });

    setTimeout(() => {
      requestData.gtmTracking = this.gtmTrackingService.getTracking();
      this.addSelection(requestData);
    }, 0);
    this.isUnauthorizedError = false;
  }

  /**
   * Emits event to add selection to main betslip.
   * @param isReceipt:
   *   true - QB closed in state "receipt"
   *   false - QB closed in state "initial"
   *   undefined - legacy, manual "add" flow
   */
  addToBetslip(isReceipt?: boolean): void {
    if (this.device.isOnline()) {
      const shouldAddToBetslip = !isReceipt && !!this.selectionData && this.selectionData.disabled === false;

      if (shouldAddToBetslip && !this.isLuckyDip) {
        const selectionState = this.formBetslipSelection();
        if(this.stakeFromQb){
          this.betslipService.betKeyboardData=`singlestake-${selectionState.outcomeId.join(',')}`
        }
        this.command.executeAsync(this.command.API.SYNC_TO_BETSLIP, [selectionState]);
        this.trackAddBetToQB(this.selectionData, true);
      }
      this.closePanel(shouldAddToBetslip);
    } else {
      this.infoDialogService.openConnectionLostPopup();
    }
  }

  get selectionVisible(): boolean {
    return !!this.selectionData && !this.loadingSelection;
  }
  set selectionVisible(value: boolean) { }

  /**
   * Determines selection type parameter needed for add selection request.
   * @param {string} type
   * @return {string}
   */
  private getSelectionType(type: string): string {
    return _.isString(type) ? type.toLowerCase() : this.SIMPLE_SELECTION_TYPE;
  }

  /**
   * Restores selection if it was returned in restored MS session.
   * @private
   */
  private restoreSelection(): void {
    let restoredSelection = this.quickbetService.getRestoredSelection();

    if(restoredSelection && restoredSelection.markets && restoredSelection.markets.length && !this.userService.status
      && restoredSelection.markets[0].drilldownTagNames && restoredSelection.markets[0].drilldownTagNames.replace(',', '') === "MKTFLAG_FZ"){
        restoredSelection =  null;
        this.sessionStorage.remove('RemoteBS');
    }

    if (restoredSelection) {
      this.selectionData = restoredSelection;
      this.toggleLoadingOverlay({ overlay: true, spinner: false });
      this.pubsub.publish(this.pubsub.API.QUICKBET_OPENED, this.selectionData);
    }
  }

  private getErrorDescription(code: string): string {
    if (code) {
      return this.locale.getString(`quickbet.${code}`);
    } else {
      return this.locale.getString('quickbet.SERVER_ERROR');
    }
  }

  /**
   * Emits global pubsub event to show/hide loading overlay.
   * @param {Object} state
   */
  private toggleLoadingOverlay(state: IQuickbetOverlayStateModel): void {
    if (state && state.overlay) {
      this.nativeBridgeService.onOpenPopup('QuickBet');
    } else {
      this.nativeBridgeService.onClosePopup('QuickBet', {});
    }
    this.loadingSelection = state && state.spinner;
    //ToDo for back btn color
    if (!this.isLuckyDip) {
      this.pubsub.publish(this.pubsub.API.TOGGLE_LOADING_OVERLAY, state);
    }
  }

  private addLuckyDipSelectionData() {
    this.selectionData = <IQuickbetSelectionModel>{};
    this.selectionData.potentialPayout = this.selection.selectionInfo.potentialOdds;
    this.selectionData.eventName = this.selection.selectionInfo.eventName;
      this.selectionData.marketName = this.selection.selectionInfo.outcomeName;
    this.selectionData.oldOddsValue = this.selection.selectionInfo.newOdds;
    this.selectionData.outcomeId = this.selection.outcomes && this.selection.outcomes[0].id;
    this.isWSdisabled = true;
    this.loadingSelection = false;
  }

  /**
   * Adds selection to quickbet.
   * @param {Object} requestData
   * @param {IQuickbetSelectionPriceModel} originalPrice
   */
  private addSelection(requestData: IQuickbetRequestModel, originalPrice?: IQuickbetSelectionPriceModel, isLD?: boolean, isStreamBet:boolean = false): void {
    this.removeSubscribers();
    this.placeBetListener();
    if(this.isLuckyDip && this.selection && this.selection.selectionInfo) {
      this.addLuckyDipSelectionData();
    }
    this.quickbetService.addSelection(requestData, originalPrice, isLD, isStreamBet)
      .subscribe((selection: IQuickbetRestoredDataModel | IQuickbetSelectionModel | any) => {

        if(selection && selection.markets && selection.markets.length && !this.userService.status
          && selection.markets[0].drilldownTagNames && selection.markets[0].drilldownTagNames.replace(',', '') === "MKTFLAG_FZ"){
          this.addSelectionErrorHandler(<IQuickbetRestoredDataModel>selection, requestData);
        }


        const errorData = <IQuickbetRestoredDataModel>selection;

        if (errorData.data && errorData.data.error) {
          this.addSelectionErrorHandler(<IQuickbetRestoredDataModel>selection, requestData);
        } else {
          if (this.selectionData) {
            (<IQuickbetSelectionModel>selection).freebet = this.selectionData.freebet;
          }
          this.selectionData = <IQuickbetSelectionModel>selection;
          this.selectionData.isOutright = this.selection.isOutright;
          this.isWSdisabled = false;
          this.trackAddBetToQB(<IQuickbetSelectionModel>selection);
          this.checkArcUser();
        }
        this.changeDetectorRef.detectChanges();
      }, (errorData: IQuickbetRestoredDataModel) => {
        this.addSelectionErrorHandler(errorData, requestData);
        this.toggleLoadingOverlay({ spinner: false, overlay: true });
      });
  }

  private addSelectionErrorHandler(errorData: IQuickbetRestoredDataModel, requestData: IQuickbetRequestModel): void {
    const error = (errorData && errorData.data && errorData.data.error) || _.extend({}, errorData),
      code = error.code || 'SERVER_ERROR',
      description = error.description || this.getErrorDescription(code);
    this.awsService.addAction('quickBetService=>addSelection=>error', error);

    this.sendEventToGTM({
      eventAction: 'add to betslip',
      eventLabel: 'failure',
      errorMessage: description.toLowerCase(),
      errorCode: code.toLowerCase()
    });
    if (error.code === 'UNAUTHORIZED_ACCESS') {
      if (!this.isUnauthorizedError) {
        this.isUnauthorizedError = true;
        this.awsService.addAction('quickBetService=>addSelection=>ErrorRetry', error);
        fromPromise(this.command.executeAsync(this.command.API.BPP_AUTH_SEQUENCE))
          .subscribe(() => {
            if (!this.userService.bppToken) {
              this.extendSelectionDataWithError(code, requestData, 'SERVER_ERROR');
            } else {
              requestData.token = this.userService.bppToken;
              this.awsService.addAction('quickBetService=>addSelection=>Error=>bppTokenUpdate', { bet: error });
              this.addSelection(requestData);
            }
          }, () => this.extendSelectionDataWithError(code, requestData, 'SERVER_ERROR'));
      } else {
        this.extendSelectionDataWithError(code, requestData, '');
      }
    } else if (this.quickbetService.isBetNotPermittedError(error)) {
      this.extendSelectionDataWithError(code, requestData, 'BET_NOT_PERMITTED');
    } else if (code === 'EVENT_NOT_FOUND') {
      this.extendSelectionDataWithError(code, requestData, 'EVENT_NOT_FOUND');
    } else {
      this.extendSelectionDataWithError(code, requestData, 'SERVER_ERROR');
    }
  }

  private extendSelectionDataWithError(code: string, requestData: IQuickbetRequestModel, status: string) {
    this.selectionData = _.extend({}, {
      error: {
        code,
        selectionUndisplayed: status
      },
      requestData
    });
  }

  /**
   * Send event to GTM
   * @param event {object}
   */
  private sendEventToGTM(event: IGtmEventModel): void {
    this.gtm.push('trackEvent', _.extend({}, {
      event: 'trackEvent',
      eventCategory: 'quickbet'
    }, event));
  }

  /**
   * Formats selection data in needed for betslip format.
   * @return {Object}
   */
  protected formBetslipSelection(): IBetslipSelection {
    const price = this.selectionData.isLP && !this.selectionData.hasSP ? _.extend({
      priceType: 'LP'
    }, this.selectionData.price) : { priceType: 'SP' },
      outcomeIds = _.has(this.selectionData.requestData, 'outcomeIds')
        ? this.selectionData.requestData.outcomeIds : [];

    let GTMObject = null,
      eventId,
      isOutright,
      isSpecial;
    const tracking = this.gtmTrackingService.getTracking();

    if (tracking) {
      GTMObject = {
        tracking
      };
    }

    if (this.selection) {
      eventId = Number(this.selectionData.eventId);
      isOutright = this.selection.isOutright;
      isSpecial = this.selection.isSpecial;
      if (this.selection.GTMObject && this.selection.GTMObject['betData'] && this.selection.GTMObject['betData']['dimension94']) {
        GTMObject['betData'] = {};
        GTMObject['betData'] = this.selection.GTMObject['betData'];
      }
    } else {
      const data: IConstant = this.sessionStorage.get(RemoteBetslipService.STORAGE_KEY);
      eventId = data && data.selectionData && Number(data.selectionData.eventId);
      isOutright = data && data.selectionData && data.selectionData.isOutright;
      isSpecial = data && data.selectionData && data.selectionData.isSpecial;
    }

    const betSlipSelection = {
      outcomeId: outcomeIds,
      userEachWay: this.selectionData.isEachWay,
      userStake: this.selectionData.stake,
      type: this.getSelectionType(this.selectionData.selectionType),
      price,
      isVirtual: this.quickbetService.isVirtualSport(this.selectionData.categoryName),
      eventId,
      isOutright,
      isSpecial,
      GTMObject
    };
    const gtmObj = { GTMObject: GTMObject, outcomeId: outcomeIds };
    this.gtm.setSBTrackingData(gtmObj);
    return betSlipSelection;
  }

  /**
   * Tracks selection add to betslip.
   * @param {Object} eventData
   * @param {boolean} toBetslip
   */
  protected trackAddBetToQB(eventData: IQuickbetSelectionModel, toBetslip?: boolean): void {
    // get stream status during adding selection to BS
    this.command.executeAsync(this.command.API.GET_LIVE_STREAM_STATUS, undefined, false)
      .then((streamData: { streamID: string, streamActive: boolean; } | null) => {
        const scorecastData = this.scorecastDataService.getScorecastData();
        let gtmObj:any = {
          eventAction: toBetslip ? 'add to betslip' : 'add to quickbet',
          eventLabel: 'success',
        };
        if(scorecastData['eventLocation'] ==='scorecast') {
          const ecommerceGtmObj = {
           event: "trackEvent",
           eventCategory: "betslip",
          //  eventLabel: "add to betslip",
          //  eventAction: "success",
           ecommerce: {
             add: {
               products: [
                 {
                   dimension86: 0,
                   dimension87: 0,
                   dimension88: null,
                   quantity: 1,
                   name: scorecastData.name,
                   category: 16,
                   variant: 1935,
                   brand: "Match Betting",
                   dimension60: scorecastData.dimension60,    
                   dimension61: scorecastData.dimension61,
                   dimension62: scorecastData.dimension62,
                   dimension63: 0,
                   dimension64:  scorecastData.dimension64,
                   dimension65: "edp",
                   dimension66: 1,
                   dimension67: 81,
                   dimension180: `scorecast;${scorecastData.teamname};${scorecastData.playerName};${scorecastData.result}`,
                   metric1: 0,
                 },
               ],
             },
           },
         };

         gtmObj = {...gtmObj,...ecommerceGtmObj}
        } 
        this.categoryName = eventData.categoryName;

        let tracking = this.gtmTrackingService.getTracking();

        if (!tracking && !!this.quickbetService.dynamicGtmObj) {
          tracking = {
            location: this.quickbetService.dynamicGtmObj.location,
            module: this.quickbetService.dynamicGtmObj.module
          }
        } else if (!!tracking && !!this.quickbetService.dynamicGtmObj) {
          tracking.location = this.quickbetService.dynamicGtmObj.location;
          tracking.module = this.quickbetService.dynamicGtmObj.module
        }

        if (tracking) {
          _.extend(gtmObj, {
            ecommerce: {
              add: {
                products: [{
                  name: eventData.eventName + (this.selection.isStreamBet ? ` - ${eventData.outcomeName}` : ''),
                  category: String(eventData.categoryId),
                  variant: String(eventData.typeId),
                  brand: eventData.marketName,
                  metric1: Number(eventData.freebetValue),
                  dimension60: String(eventData.eventId),
                  dimension61: eventData.outcomeId,
                  dimension62: eventData.isStarted ? 1 : 0,
                  dimension63: eventData.isYourCallBet ? 1 : 0,
                  dimension64: this.selection.isStreamBet ? this.categoryName : tracking.location,
                  dimension65: this.selection.isStreamBet ? "stream and bet" : tracking.module,
                  dimension86: eventData.isBoostActive ? 1 : 0,
                  dimension87: streamData && streamData.streamActive ? 1 : 0,
                  dimension88: streamData && streamData.streamID || null,
                  dimension166: 'normal',
                  dimension180: tracking.module === 'next races' && eventData.categoryId == '39' ? 'virtual' : 'normal'
                }]
              }
            }
          });
          if(this.stakeFromQb){
            const dimVal=this.stakeFromQb==2?'keypad predefined stake':'predefined stake';
            gtmObj['ecommerce']['add']['products'][0]['dimension181']=dimVal;        
          }
          this.stakeFromQb=0;
          this.digitKeyBoardStatus=false;
          const betData = this.selection.GTMObject && this.selection.GTMObject['betData'];
          if (betData && betData['dimension94'] && tracking.module == GA_TRACKING.surfaceBet.eventCategory) {
            gtmObj['ecommerce']['add']['products'][0]['dimension94'] = betData['dimension94'];
          }
          if (betData && betData['dimension177']) {
            gtmObj['ecommerce']['add']['products'][0]['dimension177'] = betData['dimension177'];
          }
        }
        this.sendEventToGTM(gtmObj);
        
      });
  }

  /**
   * Fire success bet placement event to Google Analytics
   * @param receipt {object}
   * @param trackingInfo {object}
   */
  private trackPlaceBetSuccess(receipt: IQuickbetReceiptDetailsModel[], trackingInfo: any): void {
    if (receipt && receipt[0]) {
      if (trackingInfo.hasOwnProperty('ecommerce')) {
        const price = Number(this.selectionData.stake || 0);
        const bonus = Number(this.selectionData.freebetValue || 0);
        const odds = this.quickbetService.getOdds(receipt[0].price, 'dec');

        trackingInfo.eventLabel = 'success';
        trackingInfo.ecommerce.purchase.actionField = {
          id: receipt[0].receipt.id,
          revenue: price + bonus
        };

        this.command.executeAsync(this.command.API.GET_LIVE_STREAM_STATUS, undefined, false)
          .then((streamData: { streamID: string; streamActive: boolean; }) => {
            trackingInfo.ecommerce.purchase.products[0] = _.extend(trackingInfo.ecommerce.purchase.products[0], {
              name: this.selection.isStreamBet ? `${this.selectionData.eventName} - ${this.selectionData.outcomeName}` : 'single',
              id: receipt[0].receipt.id,
              price: price + bonus,
              category: String(this.selectionData.categoryId),
              variant: String(this.selectionData.typeId),
              brand: this.selectionData.marketName,
              dimension60: String(this.selectionData.eventId),
              dimension61: String(this.selectionData.outcomeId),
              dimension62: this.selectionData.isStarted ? 1 : 0,
              dimension63: this.selectionData.isYourCallBet ? 1 : 0,
              dimension66: Number(receipt[0].legParts.length),
              dimension67: odds === 'SP' ? odds : +odds,
              dimension86: this.isPlacedBetBoosted(receipt[0]) ? 1 : 0,
              dimension87: streamData && streamData.streamActive ? 1 : 0,
              dimension88: streamData && streamData.streamID || null,
              dimension166: 'normal',
              dimension180: this.selectionData.categoryId == '39' ? 'virtual' : 'normal',
              metric1: bonus
            });
            if(this.stakeFromQb){
              const dimVal=this.stakeFromQb==2?'keypad predefined stake':'predefined stake';
              trackingInfo.ecommerce.purchase.products[0]['dimension181']=dimVal
            }
              this.stakeFromQb=0;
              this.digitKeyBoardStatus=false;
            if(this.selection.isStreamBet){
              const trackingObj = {
                dimension65: "stream and bet",
                dimension64: this.categoryName
              }
              trackingInfo.ecommerce.purchase.products[0] = { ...trackingInfo.ecommerce.purchase.products[0], ...trackingObj };
            }
            if (this.selection.GTMObject['betData'] && this.selection.GTMObject['betData']['dimension94']) {
              const trackingObj = {
                dimension90: receipt[0].bet.id,
                dimension94: this.selection.GTMObject['betData']['dimension94']
              }
              trackingInfo.ecommerce.purchase.products[0] = { ...trackingInfo.ecommerce.purchase.products[0], ...trackingObj };
            }
            if(this.scorecastData['eventLocation'] === 'scorecast') {
              trackingInfo = {...trackingInfo, ...this.ecommerceObj}
            }
            this.sendEventToGTM(trackingInfo);
            setTimeout(()=> {
              this.scorecastDataService.setScorecastData({})
          
            }, 2000)
          });

      } else {
        if(this.scorecastData['eventLocation'] === 'scorecast') {
          trackingInfo = {...trackingInfo, ...this.ecommerceObj}
        }
        this.sendEventToGTM(_.extend({}, { eventLabel: 'success', betID: receipt[0].receipt.id }, trackingInfo));
        setTimeout(()=> {
          this.scorecastDataService.setScorecastData({})
        }, 2000)
      }
    }
  }

  /**
   * Fire unsuccessful bet placement event to Google Analytics
   * @param error {object}
   * @param trackingInfo {object}
   * @param errorMessage {string}
   */
  private trackPlaceBetError(error, trackingInfo: any, errorMessage: string): void {
    if (error) {
      this.sendEventToGTM(_.extend({}, {
        eventLabel: 'failure',
        errorMessage: errorMessage.toLowerCase(),
        errorCode: error.code && error.code.replace(/_/g, ' ').toLowerCase()
      }, trackingInfo));

      if(this.selection.isStreamBet && trackingInfo.hasOwnProperty('ecommerce')) {
        const trackingObj = {
          name: `${this.selectionData.eventName} - ${this.selectionData.outcomeName}`,
          dimension65: "stream and bet",
          dimension64: this.categoryName          
        };
        trackingInfo.ecommerce.purchase.products[0] = { ...trackingInfo.ecommerce.purchase.products[0], ...trackingObj };
      }
    }
  }

  private isPlacedBetBoosted(receipt: IQuickbetReceiptDetailsModel): boolean {
    return _.has(receipt, 'oddsBoost') ? receipt.oddsBoost : false;
  }

  private isPlaceBetSubscribetExist(): void {
    if (this.quickbetPlaceBetSubscriber) {
      this.quickbetPlaceBetSubscriber.unsubscribe();
    }
  }

  public placeBetListener(): void {
    this.isPlaceBetSubscribetExist();
    this.quickbetPlaceBetSubscriber = this.quickbetDataProviderService.quickbetPlaceBetListener.pipe(
      switchMap((bet: IRemoteBetslipBet) => {
        this.betplacementProcess = true;
        return this.quickbetService.placeBet(bet);
      }))
      .subscribe((result: IQuickbetReceiptDetailsModel[]) => {
        const myBets: any = result[0].bet;
        myBets.isquickbet = true;
        if (result[0].isBir || (!result[0].isBir && this.hasClaimedOffers(result[0]))) {
          this.pubsub.publish(this.pubsub.API.STORE_FREEBETS);
        }

        this.trackPlaceBetSuccess(result, this.trackObj);
        this.quickbetService.removeQBStateFromStorage();

        this.quickbetDataProviderService.quickbetReceiptListener.next(result);
        this.quickbetNotificationService.clear();
        this.removeSubscribers();
        this.pubsub.publishSync(this.pubsub.API.BET_PLACED, BETSLIP.QUICKBET);
        !this.isLuckyDip && this.pubsub.publishSync(this.pubsub.API.MY_BET_PLACED, myBets);
        this.isLuckyDip && this.pubsub.publishSync(this.pubsub.API.MY_BET_PLACED_LD, myBets);
        this.pubsub.publish(this.pubsub.API.BETS_COUNTER_PLACEBET);
        this.pubsub.publish('PRIVATE_MARKETS_TAB');
        if (this.storageService.get('toteFreeBets') && this.storageService.get('toteFreeBets').length > 0) {
          this.storageService.set('toteFreeBets', this.storageService.get('toteFreeBets').filter(x => Number(result[0].freebetId) !== Number(x.freebetTokenId)));
        }
        if (this.storageService.get('toteBetPacks') && this.storageService.get('toteBetPacks').length > 0) {
          this.storageService.set('toteBetPacks', this.storageService.get('toteBetPacks').filter(x => Number(result[0].freebetId) !== Number(x.freebetTokenId)));
        }
        if (this.selection) {
          this.selection.skipOnReconnect = true;
        }
        const placeBetReceipt = result && result[0];
        this.placeBetFn.emit(placeBetReceipt);
        this.isBetPlaceClicked=false;
         /**
          * set event id to Local storage when placed a bet
          */
          let signPostingData = this.storageService.get('myBetsSignPostingData');
            if (this.selectionData.eventId && signPostingData?.length > 0) {
              const eventIndex = signPostingData.findIndex(data => Number(data.eventId) === Number(this.selectionData.eventId));
              if(eventIndex > -1) {
                const betIndex = signPostingData[eventIndex].betIds.findIndex(id => Number(id) == Number(result[0].bet.id));
                if(betIndex < 0) {
                  signPostingData[eventIndex].betIds.push(result[0].bet.id);
                }
              } else {
                const eventObj = {'eventId' : this.selectionData.eventId, 'betIds': [result[0].bet.id]};
                signPostingData.push(eventObj);
              }
              this.storageService.set('myBetsSignPostingData', signPostingData);
            } else {
              signPostingData = [{'eventId' : this.selectionData.eventId, 'betIds': [result[0].bet.id]}];
              this.storageService.set('myBetsSignPostingData', signPostingData);
            }
      }, (error = {}) => {
        this.removeSubscribers();
        this.betIsPlaced = true;
        // Overask placebet response is sent to main betslip and should be handled as error
        if (error.subErrorCode === 'ODDS_BOOST_PRICE_INVALID') {
          this.quickbetService.activateReboost();
          this.reuseSelection(this.selectionData.requestData);
          return;
        }
        if (error.code !== 'OVERASK') {
          const errorMessage = this.quickbetService.getBetPlacementErrorMessage(error, this.selectionData, true);
          this.trackPlaceBetError(error, this.trackObj, errorMessage);

          this.quickbetDataProviderService.quickbetReceiptListener.next(<IQuickbetReceiptDetailsModel[]>
            [{ error: errorMessage, errorCode: error.subErrorCode }]);
        }
        if (error.code === '4016') {
          this.pubsub.publish(this.pubsub.API.SHOW_LOCATION_RESTRICTED_BETS_DIALOG);
        }
      });
  }

  private removeSubscribers(): void {
    this.betplacementProcess = false;
    this.quickbetPlaceBetSubscriber && this.quickbetPlaceBetSubscriber.unsubscribe();
  }

  private getOriginalPrice(selection: IQuickbetSelectionResponseModel): IQuickbetSelectionPriceModel {
    const price = selection.price || {};

    return price.priceType === 'LP' ? Object.assign({}, price) : null;
  }

  /**
   * Check the claimedOffer status is equal 'claimed'
   * @param {IQuickbetReceiptDetailsModel} receiptDetails receipt which can contain claimedOffers
   * @returns {boolean} true if the receipt has at least one claimedOffer status equals 'claimed'
   */
  private hasClaimedOffers(receiptDetails: IQuickbetReceiptDetailsModel): boolean {
    if (receiptDetails.hasOwnProperty(this.claimedOffers)) {
      return receiptDetails.claimedOffers.some((claimedOffer: IClaimedOffer) => claimedOffer.status === this.claimed);
    }
    return false;
  }
  /**
  * Check for Arc user and disable quickbet
  */
  private checkArcUser(): void {
    if (this.arcUserService.quickbet) {
      this.addToBetslip();
    } else {
      this.pubsub.publish(this.pubsub.API.QUICKBET_OPENED, this.selectionData);
      this.toggleLoadingOverlay({ spinner: false, overlay: true });
    }
  }
  /**
   * set tag for ld mobile disable quickbet
   * @returns {void}
   */
   setTagforLd(): void {
    if (this.isLuckyDip) {
      this.tag = LUCKY_DIP_CONSTANTS.LUCKY_DIP;
    }
  }
}
