import { Location } from '@angular/common';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';
import { BetslipService } from '@betslip/services/betslip/betslip.service';
import * as _ from 'underscore';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { CommandService } from '@core/services/communication/command/command.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { MaxStakeDialogComponent } from '@betslipModule/components/maxStakeDialog/max-stake-dialog.component';
import { AddToBetslipByOutcomeIdService } from '../addToBetslip/add-to-betslip-by-outcome-id.service';
import { OverAskService } from '../overAsk/over-ask.service';
import { ToteBetslipService } from '@betslip/services/toteBetslip/tote-betslip.service';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IToteBet } from '@betslip/services/toteBetslip/tote-betslip.model';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { StorageService } from '@core/services/storage/storage.service';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';

@Injectable({ providedIn: BetslipApiModule })
export class InitBetslipService {
  // TODO: @Oleh Vykhopen
  private modulePath: string = '@betslipModule/betslip.module#BetslipModule';
  private isQuickBetBlocked: boolean = false;

  constructor(private dialogService: DialogService,
              private windowRef: WindowRefService,
              private cmsService: CmsService,
              private addToBetslipService: AddToBetslipByOutcomeIdService,
              private overaskService: OverAskService,
              private gtmService: GtmService,
              private pubsub: PubSubService,
              private command: CommandService,
              private deviceService: DeviceService,
              private userService: UserService,
              private nativeBridgeService: NativeBridgeService,
              private location: Location,
              private toteBetslipService: ToteBetslipService,
              private betslipService: BetslipService,
              private betslipDataService: BetslipDataService,
              private betslipStorageService: BetslipStorageService,
              private dynamicComponentLoader: DynamicLoaderService,
              private infoDialogService: InfoDialogService,
              private localeService: LocaleService,
              private sessionStorage: SessionStorageService,
              private arcUserService: ArcUserService,
              private eventVideoStreamProviderService: EventVideoStreamProviderService,
              private storageService: StorageService,
              protected scorecastDataService: ScorecastDataService
            ) { }

  init(): void {
    _.once(this.bindEvents.bind(this))();
  }

  private bindEvents(): void {
    // TS down't allow to pass ...args
    this.command.register(this.command.API.SYNC_TO_BETSLIP,
        // @ts-ignore
        (...args) => this.addToBetslipService.syncToBetslip(...args).toPromise());

    this.command.register(this.command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS,
        // @ts-ignore
        (...args) => this.addToBetslipService.addToBetSlip(...args).toPromise());
    this.command.register(this.command.API.GET_EVENTS_BY_OUTCOME_IDS,
        // @ts-ignore
        (...args) => this.addToBetslipService.getEventsByOutcomeIds(...args).toPromise());

    this.command.register(this.command.API.BETSLIP_READY, () => {
      return this.betslipService.betSlipReady.toPromise();
    });
    this.command.register(this.command.API.IS_ADDTOBETSLIP_IN_PROCESS, () => {
      return Promise.resolve(this.addToBetslipService.isAddToBetslipInProcess());
    });

    this.pubsub.subscribe('initBetslip', this.pubsub.API.ADD_TO_BETSLIP_BY_SELECTION,
        (selectionData: IBetSelection) =>  this.addSingleOrMultipleBetsListener(selectionData));

    this.pubsub.subscribe('initBetslip', this.pubsub.API.ADD_TO_QUICKBET_BMA_STREAM_BET,
      (selectionData: IBetSelection) => this.addToStreamBetQuickBetListener(selectionData));

    this.pubsub.subscribe('initBetslip', this.pubsub.API.ADD_TO_QUICKBET_FROM_NATIVE,
      (selectionId: string) =>  this.addToQuickbetFromNative(selectionId));

    this.pubsub.subscribe('initBetslip', this.pubsub.API.BLOCK_QUICK_BET,
      (isQuickBetBlocked: boolean) =>  { this.isQuickBetBlocked = isQuickBetBlocked; });

    this.pubsub.subscribe('initBetslip', this.pubsub.API.SELECTION_ADDED,
      (selection: IBetSelection) => this.selectionAddedListener(selection));

    this.pubsub.subscribe('initBetslip', this.pubsub.API.SYNC_BETSLIP_FROM_NATIVE,
      (outcomesIds: string[]) => this.syncFromNative(outcomesIds));

    this.pubsub.subscribe('initBetslip', this.pubsub.API.SHOW_LOCATION_RESTRICTED_BETS_DIALOG, () => {
        this.infoDialogService.openInfoDialog(
          this.localeService.getString('bs.error'),
          this.localeService.getString('bs.betRestricted'),
          undefined,
          undefined,
          undefined,
          [{
            caption: 'OK',
            cssClass: 'btn-style2 okButton'
          }]);
    });
  }

  private syncFromNative(outcomesIds: string[]) {
    const existing = this.betslipStorageService.getOutcomesIds(),
        toAdd = _.difference(outcomesIds, existing),
        toRemove = _.difference(existing, outcomesIds);

    if (toAdd.length) {
      this.addToBetslipService.addToBetSlip(toAdd.join(','), false, true, false, false).subscribe();
    }
    if (toRemove.length) {
      this.addToBetslipService.addToBetSlip(toRemove.join(','), false, false, false, false, true).subscribe();
    }
  }

  private toggleSelection(selectionData: IBetSelection, isMultipleSelections: boolean) {
    const outcomeFilter = selectionData.outcomes && selectionData.outcomes.filter(x=>x.id===selectionData.GTMObject.selectionID)
    if(selectionData.details && selectionData.details.marketDrilldownTagNames && selectionData.details.marketDrilldownTagNames.includes('MKTFLAG_LD') && outcomeFilter[0] && outcomeFilter[0].isDisplayed){
      this.infoDialogService.openInfoDialog(
        "Bet Restricted",
        this.localeService.getString('bs.BET_NOT_PERMITTED'),
        undefined,
        undefined,
        undefined,
        [{
          caption: 'OK',
          cssClass: 'btn-style2 okButton'
        }]);
      return;
    }
    if ((this.shouldUseQuickBet(selectionData) || this.eventVideoStreamProviderService.isStreamAndBet) && !this.isQuickBetBlocked && !selectionData['isLotto']) {
      this.toggleQuickbetSelection(selectionData);
    } else {
      this.toggleBetslipSelection(selectionData, isMultipleSelections);
    }
  }

  private addToStreamBetQuickBetListener(selectionData: IBetSelection): void {
    if (this.overaskService.isInProcess) {
      this.overaskService.showOveraskInProgressNotification();
      return;
    }
    this.toggleSelection(selectionData, false);
  }

  private shouldUseQuickBet(selectionData: IBetSelection): boolean {
    const betSlipData = this.betslipDataService.betslipData,
      isQuickbetEnabled = this.userService.quickBetNotification && this.deviceService.isMobile && !this.deviceService.isDesktop;

    return !this.userService.isInShopUser() && !betSlipData.bets.length && !selectionData.reuseSelection
      && isQuickbetEnabled && !this.addToBetslipService.syncProcess.inProgress && !selectionData.isFCTC;
  }

  private addSingleOrMultipleBetsListener(selectionData: IBetSelection | any) {
    if (_.isArray(selectionData)) {
      _.each(selectionData, (bet, index) => {
          this.addToBetslipListener(bet, selectionData.length === index + 1);
      });
    } else {
      this.addToBetslipListener(selectionData);
    }
  }
  private addToBetslipListener(selectionData: IBetSelection | any, flag: boolean = true): void {
    if(this.sessionStorage.get(LUCKY_DIP_CONSTANTS.LUCKY_DIP_STORAGE_KEY)) {
      this.sessionStorage.remove(LUCKY_DIP_CONSTANTS.LUCKY_DIP_STORAGE_KEY)
    }
    this.saveSelectionData(selectionData);

    // if overask in progress we can not add/remove bets to betslip
    if (this.overaskService.isInProcess) {
      this.overaskService.showOveraskInProgressNotification();
      return;
    }

    if (selectionData.isTote) {
      if (this.betslipDataService.containsRegularBets() || this.toteBetslipService.isToteBetPresent() || this.isLottoBetPresent()) {
        this.betslipService.showBetslipLimitationPopup();
      } else {
        this.toteBetslipService.addToteBet(<IToteBet>selectionData);
        this.pubsub.publish(this.pubsub.API.CLEAR_BET_BUILDER);
        this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED);
      }
      return;
    } else if (selectionData.isLotto) {
      if(this.isLottoBetPresent() && this.isLottoBetIdExistsinBetslip(selectionData)) {
        return;
      } else if (!this.isLottoBetPresent() && (this.betslipDataService.containsRegularBets() 
              || this.toteBetslipService.isToteBetPresent()) ) {
                this.betslipService.showBetslipLimitationPopup();
                return;
      }
    } else if (this.isLottoBetPresent()) {
      this.betslipService.showBetslipLimitationPopup();
      return;
    }
    this.toggleSelection(selectionData, flag);
  }

  private isLottoBetPresent():boolean {
    const betData = this.storageService.get('betSelections');
    return betData && betData.some(res => res.isLotto);
  }

  private isLottoBetIdExistsinBetslip(selection) {
    const betData = this.storageService.get('betSelections');
    let drawExists = false;
    drawExists = betData.some(bet => {
      if(selection.data.priceId === bet.details.priceId && bet.details.selections === selection.data.selections) {
        const selectionIds = selection.data.draws.map(res => res.id);
        return bet.details.draws.some(draw => selectionIds.includes(draw.id)) && 
                bet.details.draws.length > selectionIds.length;
      }
      return false;
    });
    return drawExists;
  }

  /**
   * Save selection data to session storage.
   * @param {Object} selectionData
   */
  private saveSelectionData (selectionData: IBetSelection): void {
    const outcomesArrayCopy = [],
      selectionDataCopy = Object.assign({}, selectionData);

    (selectionData.outcomes || []).forEach(outcome => {
      const outcomeCopy = Object.assign({}, outcome);
      delete outcomeCopy.event;
      delete outcomeCopy.market;
      outcomesArrayCopy.push(outcomeCopy);
    });
    if (outcomesArrayCopy.length) {
      selectionDataCopy.outcomes = outcomesArrayCopy;
    }

    if(selectionDataCopy.outcomes) {
      const gtmObj = {GTMObject: selectionDataCopy.GTMObject, outcomeId:  selectionDataCopy.outcomes.map(res => res.id)};
      this.gtmService.setSBTrackingData(gtmObj);
    }
    this.sessionStorage.set(RemoteBetslipService.STORAGE_KEY, selectionDataCopy);
  }

  private selectionAddedListener(selection: IBetSelection): void {
    if (selection.params && selection.params.GTMObject) {
      this.command.executeAsync(this.command.API.GET_LIVE_STREAM_STATUS, undefined, false)
          .then(streamData => {
            let GTMObject = selection.params.GTMObject;
            let commonFields;
            // New Coral Mobile GTM
            if (GTMObject && GTMObject.tracking) {
              if (!GTMObject.betData) {
                return;
              }

              /**
               * dimension86 - isBoosted
               * when we add selection directly to betslip it cannot be boosted => 0
               */
              const betData =  Object.assign({
                dimension86: 0,
                dimension87: streamData && streamData.streamActive ? 1 : 0,
                dimension88: streamData && streamData.streamID || null,
                quantity: 1
              }, GTMObject.betData);

              commonFields = {
                eventCategory: 'betslip',
                eventAction: 'add to betslip',
                eventLabel: 'success',
                ecommerce: {
                  add: {
                    products: [betData]
                  }
                }
              };
              GTMObject = commonFields;
            } else {
              commonFields = {
                eventCategory: 'betslip',
                eventAction: 'add to betslip',
                eventLabel: 'success',
                inPlayStatus: selection.params.eventIsLive ? 'In Play' : 'Pre Event',
                location: this.location.path(),
                customerBuilt: selection.isYourCallBet ? 'Yes' : 'No',
                streamActive: streamData && streamData.streamActive ? 1 : 0,
                streamID: streamData && streamData.streamID || null,
              };
              GTMObject = _.extend(commonFields, selection.params.GTMObject);
            }
            const scData = this.scorecastDataService.getScorecastData();
            const ecommerseObject = {
              add: {
                products: [
                  {
                    dimension86: 0,
                    dimension87: 0,
                    dimension88: null,
                    quantity: 1,
                    name: scData.name,
                    category: 16,
                    variant: 1935,
                    brand: "Match Betting",
                    dimension60: scData.dimension60,
                    dimension61: scData.dimension61,
                    dimension62: scData.dimension62,
                    dimension63: 0,
                    dimension64: scData.dimension64,
                    dimension65: "edp",
                    dimension66: 1,
                    dimension67: 81,
                    dimension180: `scorecast;${scData.teamname};${scData.playerName};${scData.result}`,
                    metric1: 0,
                  },
                ],
              },
            }
            if(scData && scData['eventLocation'] == 'scorecast') {
              GTMObject['ecommerce'] = ecommerseObject;
              delete GTMObject['categoryID'];
            }
            this.gtmService.push('trackEvent', GTMObject);
          });
    }
  }

  /**
   * Toggles view of loading overlay
   * @param {boolean} state
   */
  private toggleLoadingOverlay(state: boolean): void {
    if (state) {
      this.nativeBridgeService.onOpenPopup('QuickBet');
    } else {
      this.nativeBridgeService.onClosePopup('QuickBet');
    }

    this.pubsub.publish(this.pubsub.API.TOGGLE_LOADING_OVERLAY, {
      overlay: state,
      spinner: state
    });
  }

  /**
   * Toggles selection to main betslip.
   * @param {Object} selection
   */
  private toggleBetslipSelection(selection: IBetSelection, isMultipleSelection: boolean = true): void {
    if (this.toteBetslipService.isToteBetPresent()) {
      this.betslipService.showBetslipLimitationPopup();
      return;
    }

    this.betslipService.toggleSelection(selection, selection.doNotRemove, true, isMultipleSelection)
      .subscribe(() => {
        /*
        * adding isMultipleSelection conditions for array of selections to trigger
        * buildbet api call after all bets are added to betselections to avoid multiple buildbet calls.
        */
        if (isMultipleSelection) {
          if (selection.GTMObject) {
            this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED, {
              selectionId: selection.GTMObject.selectionID
            });
          } else {
            this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED);
          }
          this.pubsub.publishSync(this.pubsub.API.BETSLIP_COUNTER_UPDATE, this.betslipService.count());

          if (selection.goToBetslip && this.windowRef.nativeWindow.view.mobile) {
            this.pubsub.publish(this.pubsub.API['show-slide-out-betslip'], true);
          }

          this.addToBetslipService.syncProcess.inProgress = false;
        }
      }, reason => {
        if (_.isNumber(reason)) {
          this.dynamicComponentLoader.loadModule(this.modulePath).then((moduleRef) => {
            const componentFactory = moduleRef.componentFactoryResolver.resolveComponentFactory(MaxStakeDialogComponent);
            this.dialogService.openDialog(DialogService.API.betslip.maxStakeDialog, componentFactory, true, {
              text: reason
            });
          });
        }
      });
  }

  /**
   * Checks if quickbet is enabled in CMS config and adds selection to quickbet if enabled.
   * @param {Object} selection
   */
  private toggleQuickbetSelection(selection: IBetSelection): void {
    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        const quickbetCmsConfig = config.quickBet || {};
        if (quickbetCmsConfig.EnableQuickBet ) {
          const failedCommandAttempt = 'error';
         this.checkArcUser();
          this.command.executeAsync(this.command.API.SHOW_QUICKBET, [selection], failedCommandAttempt)
              .then((result: string) => {
                if (result === failedCommandAttempt) {
                  this.toggleLoadingOverlay(false);
                  this.toggleBetslipSelection(selection);
                }
              })
              .catch(() => {
                this.toggleLoadingOverlay(false);
                this.toggleBetslipSelection(selection);
              });
        } else {
          this.toggleBetslipSelection(selection);
        }
      });
  }

  /**
   * Add selection to quickbet by given id from NHP.
   * @param {string} selectionId
   */
  private addToQuickbetFromNative(selectionId: string): void {
    // if overask in progress we can not add/remove bets to betslip
    if (this.overaskService.isInProcess) {
      this.overaskService.showOveraskInProgressNotification();
      return;
    }

    const failedCommandAttempt = 'error';

    this.toggleLoadingOverlay(true);
    this.command.executeAsync(this.command.API.SHOW_QUICKBET, [{
      outcomes: [{ id: selectionId }]
    }], failedCommandAttempt)
      .then((result: string) => {
        if (result === failedCommandAttempt) {
          this.toggleLoadingOverlay(false);
          this.addToBetslipService.addToBetSlip(selectionId, false, true, false, false).subscribe();
        }
      })
      .catch(() => {
        this.toggleLoadingOverlay(false);
        this.addToBetslipService.addToBetSlip(selectionId, false, true, false, false).subscribe();
      });
  }
  /**
   * Checking for Arc User
   */
  private checkArcUser():void {
    if(this.arcUserService.quickbet){
      this.toggleLoadingOverlay(false);
     } else {
      this.toggleLoadingOverlay(true);
     }
  }
}