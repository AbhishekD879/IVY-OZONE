import {
  from as observableFrom,
  of as observableOf,
  Subject,
  Observer,
  Observable,
  throwError
} from 'rxjs';
import { finalize, concatMap, switchMap, map, tap, catchError } from 'rxjs/operators';
import { Injectable, ComponentFactory } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { IErrorData } from '@app/bpp/services/bppError/bpp-error.model';
import { IBetslipBetData, IBetslipData } from '@betslip/models/betslip-bet-data.model';
import { IBetslipConfig } from '@betslip/models/betslip-config.model';
import { IBetInfo, IEventIdsObject, IBetDoc } from '@betslip/services/bet/bet.model';
import { IBetErrorDoc } from '@betslip/services/betError/bet-error.model';
import { AccaBets, IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { IBirResponse } from '@betslip/services/bir/bir.model';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';
import { IMultipleBet } from '@core/models/multiple-bet.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { ISingleBet } from '@core/models/single-bet.model';
import { IBetslipLeg, ILeg as IBetLeg } from '@betslip/services/models/bet.model';
import { ILiveUpdatePrice, ILiveUpdateResponseMessage } from '@betslip/services/betslipLiveUpdate/betslip-live-update.model';
import environment from '@environment/oxygenEnvConfig';
import {
  IBet, IBetError,
  IBetsResponse, IBppRequest, IBuildBetRequest, IBuildBetResponse, ILeg, ILegPart, ILegRef, IOutcomeDetailsResponse,
  IRespTransGetBetsPlaced
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetHistoryStake } from '@app/betHistory/models/bet-history.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISuspendedOutcomeError } from '../../models/suspended-outcome-error.model';
import { ISystemConfig } from '@core/services/cms/models';
import { ISSResponse } from '@core/models/ss-response.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { IMarketEntity } from '@core/models/market-entity.model';
import { IOutcomeEntity } from '@core/models/outcome-entity.model';
import { Bet } from '@betslip/services/bet/bet';
import { BetSelection } from '@betslip/services/betSelection/bet-selection';
import { BetStake } from '@betslip/services/betStake/bet-stake';
import { BetError } from '@betslip/services/betError/bet-error';

import { MaxStakeDialogComponent } from '@betslipModule/components/maxStakeDialog/max-stake-dialog.component';

import { LegFactoryService } from '@betslip/services/legFactory/leg-factory.service';
import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { SessionService } from '@authModule/services/session/session.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { UserService } from '@core/services/user/user.service';
import { AccaService } from '../acca/acca.service';
import { BetSelectionService } from '../betSelection/bet-selection.service';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { IStake } from '../betStake/bet-stake.model';
import { BetStakeService } from '../betStake/bet-stake.service';
import { BirService } from '../bir/bir.service';
import { BsDocService } from '../bsDoc/bs-doc.service';
import { BuildBetDocService } from '../buildBetDoc/build-bet-doc.service';
import { FreeBet } from '../freeBet/free-bet';
import { IFreeBet } from '../freeBet/free-bet.model';
import { FreeBetService } from '../freeBet/free-bet.service';
import { GetSelectionDataService } from '../getSelectionData/get-selection-data.service';
import { OverAskService } from '../overAsk/over-ask.service';
import { PlaceBetDocService } from '../placeBetDoc/place-bet-doc.service';
import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';
import { OB_BET_NOT_PERMITTED } from '@core/constants/error-dictionary.constant';
import { ToteBetslipService } from '../toteBetslip/tote-betslip.service';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { BetslipLimitationDialogComponent } from '@betslipModule/components/betslipLimitationDialog/betslip-limitation-dialog.component';
import { StorageService } from '@core/services/storage/storage.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { LottoBuildBetDocService } from '../buildBetDoc/lotto-build-bet-doc.service';
import { FreeBetType } from '@betslip/services/freeBet/free-bet.model';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';

@Injectable({ providedIn: BetslipApiModule })
export class BetslipService {

  readonly betSlipReady: Subject<any> = new Subject();
  private betSlipConfigs: IBetslipConfig;
  private placeBetsPending: boolean = false;
  private preventSystemCache: boolean = false;
  private isBPMPFreeBetTokenUsed: boolean = false;
  private modulePath: string = '@betslipModule/betslip.module#BetslipModule';
  private _betData;

  private readonly updating: boolean = false; // not chaanging anywhere
  public placeBetResponse: Subject<IBetsResponse> = new Subject();
  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  private _betKeyboardData:any[]=[]

  constructor(
    private bsDocService: BsDocService,
    private betSelectionService: BetSelectionService,
    private betSelectionsService: BetSelectionsService,
    private betStakeService: BetStakeService,
    private legFactoryService: LegFactoryService,
    private freeBetService: FreeBetService,
    private getSelectionDataService: GetSelectionDataService,
    private bppService: BppService,
    private placeBetDocService: PlaceBetDocService,
    private buildBetDocService: BuildBetDocService,
    private cmsServcie: CmsService,
    private birService: BirService,
    private localeService: LocaleService,
    private deviceService: DeviceService,
    private overAskService: OverAskService,
    private accaService: AccaService,
    private sessionService: SessionService,
    private pubsub: PubSubService,
    private fracToDecService: FracToDecService,
    private dialogService: DialogService,
    private toteBetSlipService: ToteBetslipService,
    private user: UserService,
    private betslipDataService: BetslipDataService,
    private betslipStorageService: BetslipStorageService,
    private awsService: AWSFirehoseService,
    private dynamicComponentLoader: DynamicLoaderService,
    private clientUserAgentService: ClientUserAgentService,
    private gtmTrackingService: GtmTrackingService,
    private commandService: CommandService,
    private timeSyncService: TimeSyncService,
    private nativeBridgeService: NativeBridgeService,
    private windowRefService: WindowRefService,
    private ssRequestHelper: SiteServerRequestHelperService,
    private storageService: StorageService,
    private fbService: FreeBetsService,
    private lottoBuildBetDocService: LottoBuildBetDocService,
    private fanzoneStorageService: FanzoneStorageService,
    private sessionStorageService: SessionStorageService
  ) {
    this.getStoredBets = this.getStoredBets.bind(this);
    this.sortOddsBoosts = this.sortOddsBoosts.bind(this);
    this.placeBetsResult = this.placeBetsResult.bind(this);
  }

  get getSelections(): IBetSelection[] | BetSelection[] {
    return this.betSelectionsService.data;
  }

  set getSelections(value: IBetSelection[] | BetSelection[] ){}

  get getPlaceBetPending(): boolean {
    return this.placeBetsPending;
  }

  set getPlaceBetPending(value: boolean) {
  }

  setPlaceBetPending(value: boolean): void {
    this.placeBetsPending = value;
  }

  get betData(): any {
    return this._betData;
  }

  set betData(betData: any) {
    this._betData = betData;
  } 
  
  set betKeyboardData(value){
    !this._betKeyboardData.includes(value)&&this._betKeyboardData.push(value)
    if(value.split('-')[0] === 'All_single_quickStake') {
      const outcomes = value.split('-')[1].split(',').map((x) => {
        if(!this._betKeyboardData.includes('singlestake-'+ x)){
          return 'singlestake-'+ x;
        }
      });
      this._betKeyboardData = [...this._betKeyboardData,...outcomes];
    }
    this.storageService.set('betKeyboardData',this._betKeyboardData);
  }

  get betKeyboardData():any{
   const storageData =  this.storageService.get('betKeyboardData')
   return this._betKeyboardData.length > 0 ?  this._betKeyboardData : storageData ? storageData : this._betKeyboardData;
  }

  set filterKyeBoardData(value){
    const betKeyboardData=this._betKeyboardData.filter(data=>data!=value);
    this._betKeyboardData=betKeyboardData;
    this.storageService.set('betKeyboardData',this._betKeyboardData);
  }

  /**
   * gets freeBet responce structure and converts to freebet betslip structure
   * @param {Object} freeBet
   */
  constructFreeBet(freeBet: IFreeBet): FreeBet {
    return this.freeBetService.construct(this.freeBetService.parseOne(freeBet));
  }

  /**
   * get bets amount
   * @return total sum of regular bets and ds bets
   */
  count(): number {
    const isToteBetSlipActive = this.toteBetSlipService.isToteBetPresent();
    let betsInBetslipCount;

    if (isToteBetSlipActive) {
      /**
       * Only one bet is allowed in tote Betslip
       */
      betsInBetslipCount = 1;
    } else {
      betsInBetslipCount = this.betSelectionsService.count();
    }
    return betsInBetslipCount;
  }

  toggleSelection(selectionData: IBetSelection, doNotRemove?: boolean, isSyncWithNative: boolean = true, isMultipleSelection: boolean = true): Observable<void> {
    const selection = this.betSelectionService.construct(selectionData),
      existing = <any>this.betSelectionsService.findById(selection.id, selection.isLotto, selection.data?.priceId),
      isLuckyDipMarket = selectionData?.details?.marketDrilldownTagNames?.includes('MKTFLAG_LD');
    //If selection is from lucky Dip invalidate and not allow to add in betslip  
    if(isLuckyDipMarket){
      console.warn(BETSLIP_VALUES.ERRORS.INVALID_LUCKYDIP_SELECTION);
      return throwError(BETSLIP_VALUES.ERRORS.INVALID_LUCKYDIP_SELECTION);
    }
    return this.whenCanBeAdded(!existing).pipe(
      catchError((error: number | any) => {
        if (_.isNumber(error)) {

          //build bet call need to be made here OZONE-6875
          //added isMultipleSelection to trigger only for the last bet added to betslip 
          // for array of bets in betList to avoid multiple buildbet calls for lottos.
          isMultipleSelection && this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED);
          // TODO: @Oleh Vykhopen
          this.maximumStakesDialog(error);
        }

        return throwError(error);
      }),
      map(() => {
        if (existing) {
          return this.isPriceTypeToggling(selection) ? this.edit(existing, selection) : !doNotRemove && this.remove(existing);
        }
        return this.add(selection);
      }),
      map(() => {
        if (isSyncWithNative) {
          this.betslipStorageService.syncWithNative();
        }
      }));
  }

  maximumStakesDialog(error: number) {
    this.dynamicComponentLoader.loadModule(this.modulePath).then((moduleRef) => {
      const componentFactory = moduleRef.componentFactoryResolver.resolveComponentFactory(MaxStakeDialogComponent);
      this.dialogService.openDialog(DialogService.API.betslip.maxStakeDialog, componentFactory, true, {
        text: error
      });
    });
  }
  setConfig(conf: IBetslipConfig): void {
    this.betSlipConfigs = conf;
  }

  /**
   * Main bet placemeelse if((bet.Bet && bet.Bet?.paramsnt flow
   */
  placeBets(lottoDataObj): Observable<IBetsResponse> {
    this.betslipDataService.checkPrices();
    return this.placeBetsRequest(lottoDataObj).pipe(
      map(response =>  response),
      tap(response => {
        this.placeBetResponse.next(response);
      })
    );
  }

  /**
   * Exucute Overask for manual data, used for quick bet fun-ty
   * @param {Object} overaskData
   * @returns {Promise<T>}
   */
  exucuteOverask(overaskData: IRespTransGetBetsPlaced): Observable<IRespTransGetBetsPlaced> {
    this.betslipDataService.checkPrices();
    return this.overAskService.execute(overaskData);
  }

  /**
   * Converts Place Bets Response into structure ready for overAsk
   * @param {Object} response
   */
  parsePlaceBetsResponse(response) {
    const errs = _.reduce(response.betError, (errsEntity: IErrorData, err: IBetError) => {
      return concat(errsEntity, {
        subCode: err.subErrorCode,
        code: err.code,
        errorDesc: err.errorDesc,
        price: err.price,
        handicap: err.handicap,
        outcomeRef: err.outcomeRef,
        betRef: err.betRef && err.betRef[0].documentId // there is only one betRef
      });
    }, []),
      total = _.reduce(response.bet, (aggr: IBirResponse, bet: any) => {
        bet.lines.number = Number(bet.lines.number);
        return _.extend({}, aggr, {
          providers: concat(aggr.providers, bet.provider),
          ids: concat(aggr.ids, bet.id),
          bets: concat(aggr.bets, bet)
        });
      }, {
          providers: [],
          ids: [],
          bets: [],
          errs
        });
    total.legs = response.leg;

    function concat(arr, arg) {
      return arg ? arr.concat([arg]) : arr;
    }

    return total;
  }

  /**
   * Set amount for bet selection stored in locale storage on change
   * @params {object} controller bet object
   */
  setAmount(bet: IBetslipBetData | any): void {
    if (!bet.disabled) {
      // clear error message
      if(bet.Bet.legs && bet.Bet.legs.length) bet.Bet.clearErr();

      _.each(<IBetSelection[]>this.betSelectionsService.data, (selection: IBetSelection) => {
        if (bet.combiName) {
          if (selection.id === `${bet.combiName}|${bet.outcomeId}`) {
            selection.userStake = <string>bet.stake.perLine;
          }
        } else if((bet.Bet && bet.Bet.params?.lottoData?.isLotto) && (bet.Bet && bet.Bet.params.lottoData.id === selection.id)){
          selection.userStake = <string>bet.Bet.params.lottoData.details.stake;
          bet.Bet.params.lottoData.accaBets.forEach((accaBet)=>{
            accaBet.userStake = accaBet.stake;
          });
        } 
        else {
          if (this.isIdsEqual(bet.outcomeIds, selection.params.outcomesIds)) {
            selection.userStake = <string>bet.stake.perLine;
          }
        }
      });
      this.betslipStorageService.store();
    }
  }

  fetch(preventCache): Observable<Bet[] | any> {
    let isSSCallNeeded: boolean = false;
    const storedSelections: IBetSelection[] = this.betslipStorageService.restore();
    const selections: BetSelection[] = [];

    this.preventSystemCache = preventCache;

    storedSelections.forEach((storedSelection: IBetSelection | any) => {
      if (isSSCallNeeded
        || !storedSelection.details
        || storedSelection.isVirtual
        || storedSelection.isFCTC
        || storedSelection.type === 'SCORECAST') {
        isSSCallNeeded = true;
        return;
      }

      if(!storedSelection.isLotto) {
        storedSelection.outcomes = storedSelection.outcomesIds.map((outcomesId: string) => {
          return {
            id: outcomesId,
            details: storedSelection.details
          } as IOutcome;
        });
      }
      selections.push(this.betSelectionService.construct(storedSelection));
    });

    if (isSSCallNeeded) {
      return this.fetchWithSS();
    }
    const legs = this.legFactoryService.constructLegs(<any>selections);

    return legs.length ?
      this.buildBetsRequestByStoredData(legs, storedSelections).pipe(
        map((data: IBetslipData) => {
          if(data.bets && data.bets.length && data.bets[0].params?.lottoData?.isLotto) {
            return data;
          }
          data.bets = _.sortBy(data.bets, (bet: Bet) => bet.legs[0].docId);
          return data;
        }),
        map((data: any) => {
          return this.filterNotRequestedScoreCast(data);
        }),
        switchMap((data: IBetslipData) => {
          return this.getAccaOffer(data);
        }),
        map(this.getStoredBets),
        switchMap(this.sortOddsBoosts),
        catchError(err => {
          console.warn('Error in Betslip.fetch', err);
          return throwError(err);
        }),
        finalize(() => {
          this.pubsub.publishSync(this.pubsub.API.BETSLIP_COUNTER_UPDATE, this.count());
          this.pubsub.publishSync(this.pubsub.API.ADDTOBETSLIP_PROCESS_FINISHED);
        })
      ) :
      this.cleanDataSync();
  }

  /**
   * General bet slip flow
   * @param {boolean} preventCache - not use cache for system request
   * @return {*}
   */
  fetchWithSS(): Observable<Bet[] | any> {
    const storedSelections = this.betslipStorageService.restore(),
      outcomesIds = this.betslipStorageService.getOutcomesIds(storedSelections);
    
    return outcomesIds.length
      ? this.getSelectionDataService.getOutcomeData(outcomesIds).pipe(
        map((data: IOutcome[]) => {
          return this.betslipStorageService.filterSelections(data);
        }),
        map((data: IOutcome[]) => {
          return this.extendSelections(data);
        }),
        map((params: BetSelection[]) => 
        this.legFactoryService.constructLegs(<any>params)
        ),
        concatMap((data: SportsLeg[]) => {

          return this.buildBetsRequest(data);
        }),
        map((data: IBetslipData) => {
          data.bets = _.sortBy(data.bets, (bet: Bet) => bet.legs[0].docId);
          this.pubsub.publish(this.pubsub.API.PUSH_TO_GTM, data);
          return data;
        }),
        map((data: any) => {
          return this.filterNotRequestedScoreCast(data);
        }),
        switchMap((data: IBetslipData) => {
          return this.getAccaOffer(data);
        }),
        map(this.handleNotAllowedBets),
        map(this.getStoredBets),
        switchMap(this.sortOddsBoosts),
        catchError(err => {
          console.warn('Error in Betslip.fetch', err);
          return throwError(err);
        }),
        finalize(() => {
          this.pubsub.publishSync(this.pubsub.API.BETSLIP_COUNTER_UPDATE, this.count());
          this.pubsub.publishSync(this.pubsub.API.ADDTOBETSLIP_PROCESS_FINISHED);
        }))
      : this.cleanDataSync();
  }

  /** W/E checkbox state defines type of stake and calculate related estimate amount
   * @params {number} index
   */
  winOrEachWay(bet: IBetslipBetData): void {
    if (bet.price) {
      this.updatePrice(bet);
    }

    bet.legType = bet.Bet.isEachWay ? 'E' : 'W';
    this.betslipStorageService.setFreeBet(bet);

    if(bet && bet.outcomeId) {
      const selectionIndex = this.betSelectionsService.data.findIndex((selection: BetSelection) => {
        return (selection.outcomes.length === 1 && bet.outcomeId === selection.outcomes[0].id);
      });

      if(selectionIndex >= 0) {
        this.betSelectionsService.data[selectionIndex].userEachWay = bet.Bet.isEachWay;
      }
    }

    this.betslipStorageService.store();
  }

  removeByOutcomeId(selection: IBetslipBetData | any): void {
    const selectionId = selection.isLotto ? selection.id : `${selection.combiName || 'SGL'}|${selection.outcomeId}`;
    this.pubsub.publish(this.pubsub.API.REMOVE_VS_STORAGE, selection.outcomeId || selectionId);
    this.removeReUseSelections(selection.outcomeId || selectionId);
    this.remove(<any>this.betSelectionsService.findById(selectionId));
    this.betslipStorageService.syncWithNative();
  }

  /**
   * @param {ISingleBet[]} selections
   * @memberof BetslipService
   */
  removeByOutcomeIds(selections: ISingleBet[]): void {
    const removeSelections = [];
    _.each(selections, selection => {
      this.pubsub.publish(this.pubsub.API.REMOVE_VS_STORAGE, selection.outcomeId);
      this.removeReUseSelections(selection.outcomeId);
      removeSelections.push(this.betSelectionsService.findById(`${selection.combiName || 'SGL'}|${selection.outcomeId}`));
    });
    this.removeMulti(removeSelections);
    this.betslipStorageService.syncWithNative();
  }

   /**
   * @param {string} selectionId
   * @memberof BetslipService
   */
  removeReUseSelections(selectionId): void {
    const reuseBetOriginData = this.storageService.get('reuseBetSelections');
    if (reuseBetOriginData && reuseBetOriginData[selectionId]) { 
      delete reuseBetOriginData[selectionId]
    }
    this.storageService.set('reuseBetSelections', reuseBetOriginData);
  }

  /**
   * Save data on priceType change
   * @param {number} bet
   */
  setPriceType(bet: IBetslipBetData): void {
    // Update price for outcome with ls,sp
    _.each(this.betSelectionsService.data, (selection: BetSelection) => {
      if (bet.outcomeId === selection.outcomes[0].id) {
        selection.price = <IOutcomePrice>bet.price;
      }
    });

    this.updatePrice(bet);
    this.betslipStorageService.store();
    this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED);

    bet.isSP = bet.price.priceType === 'SP';
    bet.errorMsg = '';

    if (bet.isSP) {
      this.pubsub.publish(this.pubsub.API.ODDS_BOOST_HANDLE_SP);
    }
  }

  /**
   * Update selection Facade
   * 1) updates one selection
   * 2) updates local storadge
   * 3) broadcasts update
   */
  updateSelection(index: number, update, type): void {
    const updateBet = this.betslipDataService.bets[index],
      outcomeId = updateBet.info().outcomeId;                  // get outcome id

    updateBet.update(update, type);                                // update one outcome
    this.betslipStorageService.updateStorage(update, outcomeId);                                            // update local storadge
    this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED, [this.betslipDataService.bets]); // broadcast update for controller

    this.pubsub.publishSync(this.pubsub.API.BS_SELECTION_LIVE_UPDATE, updateBet);
  }

  /**
   * Update live update history for betslip selection
   * @param {number} index  bet index
   * @param {object} msg    update message
   */
  updateSelectionLiveUpdateHistory(index: number, msg: ILiveUpdateResponseMessage): void {
    this.betslipDataService.bets[index].history.update(msg);
  }

  /**
   * Show  suspended outcome error msg if we have disable SGL outcome
   * @param {object} betSlipSingles
   * @param {object} betSlipMultiples
   * @return {object}
   */
  showSuspendedOutcomeErr(betSlipSingles, betSlipMultiples): ISuspendedOutcomeError {
    let placeMultiplesStakeErr = false,
      placeSinglesStakeErr = null,
      isStakeSet = false,
      amountOfSuspendedOutcomes = 0;

    const suspendedIds = [];

    betSlipMultiples.forEach((multiple: any) => {
      // Check if amount was set in Multiple bets stake field
      // depending on this, show different messages
      if (multiple.stake.perLine > 0) {
        isStakeSet = true;
      }
      multiple.disabled = false;
    });

    betSlipSingles.forEach((single: any) => {
      if((single.combiType==="FORECAST" && !(single.outcomes?.length>0 && single.outcomes[0].details?.markets[0]?.ncastTypeCodes?.match(/(?=.*CF)/))) || 
          (single.combiType==="TRICAST" && !(single.outcomes?.length>0 && single.outcomes[0].details?.markets[0]?.ncastTypeCodes?.match(/(?=.*CT)/)))) {
        single.disabled = true;
      }
      if (single.disabled) {
        // Check if disabled bet was placed
        if (this.overAskService.isInProcess) {
          if (this.overAskService.isBetPlaced(single)) {
            suspendedIds.push(single.betId);
            amountOfSuspendedOutcomes++;
          }
        } else {
          amountOfSuspendedOutcomes++;
        }

        // Find if multiples contains disabled single
        betSlipMultiples.forEach((multiple: any) => {
          const isMultipleDisabled = multiple.eventIds.outcomeIds.includes(single.eventIds.outcomeIds[0]);

          if (isMultipleDisabled) {
            if (this.overAskService.isInProcess) {
              if (this.overAskService.isBetPlaced(multiple)) {
                suspendedIds.push(multiple.betId);
                multiple.disabled = true;
                placeMultiplesStakeErr = true;
                amountOfSuspendedOutcomes++;
              }
            } else {
              placeMultiplesStakeErr = true;
            }
          }
        });
      }
    });

    if (amountOfSuspendedOutcomes) {
      // TODO use replace for string by param
      placeSinglesStakeErr = this.getSuspendedMessage(amountOfSuspendedOutcomes);
    }

    if (this.overAskService.isInProcess) {
      this.overAskService.setSuspended(suspendedIds);
    }

    return {
      multipleWithDisableSingle: placeMultiplesStakeErr,
      disableBet: isStakeSet && placeMultiplesStakeErr,
      msg: placeSinglesStakeErr
    };
  }

  getSuspendedMessage(suspendedOutcomesCount: number): string {
    const literalToken: string = suspendedOutcomesCount > 1 ? 'bs.multipleDisabled' : 'bs.singleDisabled';
    return this.localeService.getString(literalToken);
  }

  /**
   * Check if at least one bet has a stake.
   * @params{array} bets to check
   * @params{boolean} check mocked bets or not
   * @returns {boolean}
   */
  areBetsWithStakes(bets: any, checkMockedStakes?: boolean): boolean {
    return _.some(bets, (bet: any) => {
      if(!bet.isLotto){
        return checkMockedStakes ? (!bet.isMocked && Number(bet.stake.perLine) && !bet.disabled) ||
        bet.selectedFreeBet : (Number(bet.stake.perLine) && !bet.disabled) ||
        bet.selectedFreeBet;
      }else{
        const accaBetStake = bet.accaBets.some(betObj => betObj.stake);
      return  Number(bet.details.stake || accaBetStake);
      }
    });
  }

  /**
   * Return amount on suspended singles
   * @params {Array} betSlipSingles
   * @return {Number} suspendedOutcomesCounter
   */
  countSuspendedOutcomes(betSlipSingles: ISingleBet[]): number {
    let suspendedOutcomesCounter = 0;
    _.each(betSlipSingles, (single: ISingleBet) => {
      if (this.isSingleDisabled(single)) {
        suspendedOutcomesCounter++;
      }
    });
    return suspendedOutcomesCounter;
  }

  /**
   * @param {ISingleBet[]} betSlipSingles
   * @return {*}  {ISingleBet[]}
   * @memberof BetslipService
   */
  suspendedIndexFromSelection(betSlipSingles: ISingleBet[]): ISingleBet[] {
    const suspendedSeletions: ISingleBet[] = [];
    _.each(betSlipSingles, (single: ISingleBet) => {
      if (this.isSingleDisabled(single)) {
        suspendedSeletions.push(single);
      }
    });
    return suspendedSeletions;
  }

  /**
   * Check if error is kind of suspension
   * @params {String} error
   * @return {Boolean}
   */
  isSuspended(error: string): boolean {
    return error === BETSLIP_VALUES.ERRORS.OUTCOME_SUSPENDED || error === BETSLIP_VALUES.ERRORS.MARKET_SUSPENDED ||
      error === BETSLIP_VALUES.ERRORS.EVENT_SUSPENDED || error === BETSLIP_VALUES.ERRORS.SELECTION_SUSPENDED;
  }

  /**
   * Find and then store suspended single bets
   * @return {array}
   */
  findSuspendedBetsId(betSlipSingles): void {
    const suspendedSingles = _.filter(betSlipSingles, (single: any) => {
      return this.isSuspended(single.error) ? single : null;
    });
    this.betslipStorageService.storeSuspended(_.pluck(suspendedSingles, 'outcomeId'));
  }

  /**
   * Check if Multiple bets has selected free bet
   * @params {object} betSlipMultiples
   * @return {boolean}
   */
  isMultipleFreeBetSelected(betSlipMultiples: IMultipleBet[]): IMultipleBet {
    return _.find(betSlipMultiples, (bet: IMultipleBet): IMultipleBet => bet.selectedFreeBet);
  }

  /**
   * Get betslip bet by response bet and legs (compare type and all outcomes)
   * @params {object} bet - specific bet from bpp response
   * @params {Array} legs - legs from bpp response
   * @params {Array} allBetslipBets - all betslip bets
   * @return {Object}
   */
  getBetslipBetByResponseBet(bet: IBet, legs: ILeg[], allBetslipBets: IBetInfo[]): any {
    const betLegsIds = bet && bet.legRef.map((leg: ILegRef) => leg.documentId);
    const betLegs = _.filter(legs, (leg: ILeg) => betLegsIds.indexOf(leg.documentId) !== -1);
    const betOutcomeIds = _.flatten(betLegs.map((leg: ILeg) => leg.sportsLeg.legPart
      .map((p: ILegPart) => p.outcomeRef.id)));

    return _.find(allBetslipBets, (b: IBetInfo) => {
      if (bet && bet.betTypeRef.id !== b.type) {
        return false;
      }
      const outcomeIds = _.flatten(b.Bet.legs.map((leg: any) => leg.parts.map((p: any) => p.outcome.id)));
      return bet && outcomeIds.length === betOutcomeIds.length && !_.difference(outcomeIds, betOutcomeIds).length &&
        b.stake.placement === Number((bet.stake as IBetHistoryStake).stakePerLine);
    });
  }

  /**
   * Calculate potentialPayout for ACCA and Double,
   * it's made by multiplying all related singles dec prices
   * @param betslipStake {object}
   * @return potentialPayout {number}
   */
  getMultiplePotentialPayout(betslipStake: any): number {
    // Calculate odds value when trader changed price(s) for multiple bet(overask process)
    if (betslipStake.traderChangedOdds) {
      return betslipStake.potentialPayout / betslipStake.stake.perLine;
    }

    const newSinglesPrices = [];
    _.each(betslipStake.outcomes, (outcome: any) => {
      newSinglesPrices.push(1 + (outcome.price.priceNum / outcome.price.priceDen));
    });

    return newSinglesPrices.reduce((prev: number, current: number) => prev * current);
  }

  /**
   * Check if multiple singles has old prices
   * @param betslipStake {object}
   * @return {boolean}
   */
  isSinglesHasOldPrice(betslipStake: any): boolean {
    return _.some(betslipStake.Bet.legs, (leg: any) => {
      return _.has(leg.parts[0].outcome, 'oldModifiedPrice');
    });
  }

  /**
   * Set potentialPayout object
   * @param {number} oldPotentialPayout
   * @param {string} userOddsFormat
   * @param {number} newPotentialPayout
   * @return {object}
   */
  buildPotentialPayoutObj(oldPotentialPayout: number = NaN, userOddsFormat: string, newPotentialPayout: number) {
    let oldPrice;
    const isPriceChangeUp = oldPotentialPayout < newPotentialPayout;
    // Make old price format according to User settings (used for view)
    if (userOddsFormat === 'frac') {
      oldPrice = isNaN(oldPotentialPayout) ?
        oldPotentialPayout : this.fracToDecService.decToFrac(oldPotentialPayout.toFixed(3));
    } else {
      oldPrice = isNaN(oldPotentialPayout) ? oldPotentialPayout : oldPotentialPayout.toFixed(2);
    }
    return {
      oldPrice,                        // old price in user odds format (used for view)
      newPriceDec: newPotentialPayout, // new price in Dec format (using for comparison and then make it old price)
      isPriceChangeUp,
      isPriceChangeDown: !isPriceChangeUp
    };
  }

  /**
   * Get system configs and apply appropriate for betslip
   */
  getConfig(): Observable<IBetslipConfig> {
    return Observable.create((observer: Observer<any>) => {
      if (this.betSlipConfigs && !this.preventSystemCache) {
        observer.next(this.betSlipConfigs);
        observer.complete();
        return;
      }

      this.cmsServcie.getSystemConfig(this.preventSystemCache)
        .subscribe((config: ISystemConfig) => {
          this.betSlipConfigs = config.Betslip;
          observer.next(this.betSlipConfigs);
          observer.complete();

        }, err => {
          console.error('Error in Betslip.getConfig', err);
          observer.error(err);
        });
    });
  }

  /**
   * Update Win and Each way legs only with new price
   * @param liveUpdatePayload - update payload message
   * @param updatedOutcomeId - id of updated outcome
   */
  updateLegsWithPriceChange(liveUpdatePayload: ILiveUpdatePrice, updatedOutcomeId: number): void {
    const toNumber = stringNumber => parseInt(stringNumber, 10);

    _.forEach(this.betslipDataService.betslipData.legs, (leg: IBetslipLeg) => {
      const isWinOrEachWayBet = _.contains(['EACH_WAY', 'WIN'], leg.winPlace),
        legUpdated = toNumber(leg.firstOutcomeId) === toNumber(updatedOutcomeId);

      if (!isWinOrEachWayBet || !leg.price || !legUpdated) {
        return;
      }

      const numeratorChanged = toNumber(leg.price.num) !== toNumber(liveUpdatePayload.lp_num),
        denominatorChanged = toNumber(leg.price.den) !== toNumber(liveUpdatePayload.lp_den);

      if (numeratorChanged) {
        leg.price.props.priceNum = liveUpdatePayload.lp_num;
      }

      if (denominatorChanged) {
        leg.price.props.priceDen = liveUpdatePayload.lp_den;
      }
    });
  }

  updateAvailableFreeBets(betslipBets: IBetslipBetData[]): void {
    const usedFreeBets = betslipBets.filter(bet => !bet.disabled && bet.selectedFreeBet)
      .map(bet => bet.selectedFreeBet.id);
    const betPackKeyName = this.localeService.getString('bs.betPacks');
    const freeBetsKeyName = this.localeService.getString('bs.freeBets');
    const fanZoneKeyName = this.localeService.getString('bs.fanZone');

    betslipBets.forEach((bet: IBetslipBetData) => {
      const freeBets = bet.Bet.freeBets;
      const freeBetBetPackList = freeBets?.reduce((accumulativeBets, currentBet) => {
        const key = this.fbService.isBetPack(currentBet.freeBetOfferCategories?.freebetOfferCategory) ? betPackKeyName : this.fbService.isFanzone(currentBet.freeBetOfferCategories?.freebetOfferCategory) ? fanZoneKeyName : freeBetsKeyName;
        accumulativeBets[key] = [...accumulativeBets[key] || [], currentBet];
        return accumulativeBets;
      }, {});
      const freebetsList = freeBetBetPackList?.[freeBetsKeyName] ? freeBetBetPackList[freeBetsKeyName] : [];
      const betPackList = freeBetBetPackList?.[betPackKeyName] ? freeBetBetPackList[betPackKeyName] : [];
      const fanzoneList = freeBetBetPackList?.[fanZoneKeyName] ? freeBetBetPackList[fanZoneKeyName] : [];
      bet.availableFreeBets = (bet.disabled || !freebetsList) ? [] : this.filterAndSort(freebetsList, usedFreeBets);
      bet.availableBetTokens = (bet.disabled || !betPackList) ? [] : this.filterAndSort(betPackList, usedFreeBets, 1);
      bet.availableFanzone = (bet.disabled || !fanzoneList) ? [] : this.filterAndSort(fanzoneList, usedFreeBets, 2);
    });
  }
  /**
   * Check if freebet is valid to avoid case with freebet less than 0.01
   */
  isFreeBetValid(freebetAmount: number, bet: IBetslipBetData): boolean {
    const lines = bet.stake.lines;
    return (freebetAmount / lines) >= 0.01;
  }

  getOverlayLiveUpdateMessage(bet: Bet, isBoostActive: boolean): string {
    if (bet.history.isStarted()) {
      return this.localeService.getString('bs.EVENT_STARTED');
    }

    if (bet.history.isSuspended()) {
      const suspended = this.betslipDataService.bets.filter(
        (_bet: Bet) => this.isSingleDisabled(_bet.info() as any as ISingleBet)
      );
      return this.getSuspendedMessage(suspended.length);
    }

    if (
      bet.history.isPriceChanged() ||
      bet.history.isPriceChangedAndMarketUnsuspended()
    ) {
      return this.localeService.getString(
        isBoostActive ? 'bs.reboostPriceChangeOverlayMsg' : 'bs.priceChangeBannerMsg'
      );
    }

    return '';
  }

  findBetForFreeBetTooltip(
    singles: IBetslipBetData[], acca: IBetslipBetData[],  multiples: IBetslipBetData[]
  ): void {
    const bet = [...singles, ...acca, ...multiples].find(_bet => _bet.availableFreeBets.length > 0);
    if (bet) {
      bet.freeBetTooltipAvailable = true;
    }
  }

  /**
   * Close native betslip and wait when animation completed
   * @param  {Function} cb Callback function
   */
  closeNativeBetslipAndWaitAnimation(cb: Function): void {
    if (this.deviceService.isWrapper) {
      this.pubsub.publish(this.pubsub.API['show-slide-out-betslip'], false);
      this.windowRefService.nativeWindow.setTimeout(cb, this.nativeBridgeService.betSlipCloseAnimationDuration);
    } else {
      cb();
    }
  }

  isBetNotPermittedError(result: IBetsResponse): boolean {
    const err = result.errs[0];
    return err && !err.subCode && !err.code && err.errorDesc && err.errorDesc.toLowerCase() === OB_BET_NOT_PERMITTED;
  }

  getBetNotPermittedError(): string {
    return this.localeService.getString('bs.BET_NOT_PERMITTED');
  }

 /**
  * Show Betslip Limitation Popup BMA-28466
  */
  showBetslipLimitationPopup(): Observable<Object> {
    this.dynamicComponentLoader.loadModule(this.modulePath).then((moduleRef) => {
      /* eslint-disable max-len */
      const componentFactory: ComponentFactory<BetslipLimitationDialogComponent> = moduleRef.componentFactoryResolver.resolveComponentFactory(BetslipLimitationDialogComponent);
      /* eslint-enable max-len */
      this.dialogService.openDialog(DialogService.API.betslip.betslipLimitationDialog, componentFactory, true);
    });

    return observableOf(null);
  }

  private filterAndSort(freeBets: IFreeBet[], usedFreeBets: any[], betTokenType: number = 0): IFreeBet[] {
    return freeBets
      .filter((freeBet: IFreeBet) => !usedFreeBets.includes(freeBet.id))
      .filter((freeBet: IFreeBet) => betTokenType ===  FreeBetType.FREEBET ?this.fbService.isBetPack(freeBet.freeBetOfferCategories && freeBet.freeBetOfferCategories.freebetOfferCategory) :betTokenType === FreeBetType.FANZONE ? this.fbService.isFanzone(freeBet.freeBetOfferCategories && freeBet.freeBetOfferCategories.freebetOfferCategory):(!freeBet.freebetOfferCategories ||(!this.fbService.isBetPack(freeBet && freeBet.freeBetOfferCategories && freeBet.freeBetOfferCategories.freebetOfferCategory) &&!this.fbService.isFanzone(freeBet && freeBet.freeBetOfferCategories && freeBet.freeBetOfferCategories.freebetOfferCategory))))
      .sort((a, b) => {
        const aFb = Date.parse(a.freeBetExpireAt),
          bFb = Date.parse(b.freeBetExpireAt);
        return aFb - bFb;
      });
  }
  /**
   * Constructs a new BetSlip
   * @param  {Object} params configurations
   * @return {BetSlip}        BetSlip object
   */
  private construct(params: IBetslipData): IBuildBetRequest {
    const self = this;
    const stake = Object.create(
      this.betStakeService.construct(<IStake>({ currency: this.user.currency })), {
        amount: { get: this.getTotalAmount.bind(this, params.bets) }
      });
    const selections = this.betSelectionsService.data;
    const isSelectionVirual = selections.length ? selections[0].isVirtual : false;

    return {
      docId: params.docId || 1,
      stake,
      bets: this.filterPriceful(params.bets),
      legs: params.legs,
      errs: params.errs,
      doc() {
        return (
          self.bsDocService.el('betslip', {
            clientUserAgent: self.clientUserAgentService.getId(isSelectionVirual, false),
            isAccountBet: 'Y',
            documentId: this.docId,
            betRef: (() => {
              return _.reduce(this.bets, (result, bet: Bet) => {
                return (<BetStake>bet.stake).amount ? result.concat([{ documentId: bet.docId }]) : result;
              }, []);
            }).call(this)
          },
            _.union(
              [this.stake.doc()],
              [self.bsDocService.el('slipPlacement', { IPAddress: self.timeSyncService.ip }, [self.deviceService.channel])]
            )
          ));
      }
    };
  }

  /**
   * Returns total amount
   * @param {array} bets
   * @return {string}
   */
  private getTotalAmount(bets: Bet[]) {
    return bets.reduce((sum: number, bet: Bet) => {
      return (<BetStake>bet.stake).amount && !bet.disabled ? sum + (<BetStake>bet.stake).amount : sum;
    }, 0).toFixed(2);
  }

  private filterPriceful(bets) {
    return _.filter(bets, (bet: any) => {
      return !!bet.stake.amount || bet.stake.freeBetAmount;
    });
  }

  /**
   * Add, edit or remove selection
   * @params{object} selection data
   * @params{boolean} allow to remove selection
   */
  private isPriceTypeToggling(selection: IBetSelection) {
    return _.find(<IBetSelection[]>this.betSelectionsService.data, (sel: IBetSelection) => {
      if(selection.isLotto) {
       return selection.id.toString().includes(sel.id.toString());
      }
      return sel.id === selection.id &&
        sel.price.priceType !== selection.price.priceType;
    });
  }

  private whenCanBeAdded(isNew): Observable<any> {
    return this.getConfig().pipe(
      catchError(err => {
        return throwError(err);
      }),
      switchMap((config: ISystemConfig) => {
        if (isNew && this.betSelectionsService.count() > config.maxBetNumber - 1) {
          return throwError(Number(config.maxBetNumber));
        }

        return observableOf(null);
      }));
  }

  private edit(existing: BetSelection, selection: BetSelection | any) {
    if(selection.isLotto) {
     this.betSelectionsService.updateSelection(selection);
    } else {
     existing.price.priceType = selection.price.priceType;
    }
    this.betslipStorageService.store();
  }

  private add(selection: BetSelection): string {
    this.betSelectionsService.addSelection(<any>selection);
    this.betslipStorageService.store();
    this.pubsub.publish(this.pubsub.API.SELECTION_ADDED, selection);
    return 'SELECTION_ADDED';
  }

  private remove(selection: BetSelection) {
    this.betslipDataService.clearMultiplesStakes();
    this.betSelectionsService.removeSelection(<any>selection);
    this.betslipStorageService.store();
  }

  /**
   * @private
   * @param {BetSelection[]} selections
   * @memberof BetslipService
   */
  private removeMulti(selections: BetSelection[]) {
    this.betslipDataService.clearMultiplesStakes();
    this.betSelectionsService.removeMultiSelection(selections);
    this.betslipStorageService.store();
  }

  private getStoredBets(data: IBetslipData): Bet[] {
    return this.betslipDataService.storeBets(data);
  }

  private sortOddsBoosts(betsData: Bet[]): Observable<Bet[]|any> {
    if(betsData && betsData[0].params.lottoData?.isLotto) {
      return observableOf(betsData);
    }
    else if (betsData && !betsData[0].params.lottoData?.isLotto) {
      if (!this.user.status || !_.find(betsData, bet => bet.params.oddsBoosts && bet.params.oddsBoosts.length)) {
        this.pubsub.publish(this.pubsub.API.ODDS_BOOST_CHECK_BS_SELECTIONS);
        return observableOf(betsData);
      }
    } 

    return observableFrom(this.commandService.executeAsync(this.commandService.API.ODDS_BOOST_SETTLE_TOKEN, [betsData]));
  }

  /**
   * Get superAcca offer
   * @param betslipData object with bets
   * @return {Promise} bets with offer if user logged-in, if user isn't logged-in returns received data
   */
  private getAccaOffer(betslipData: IBetslipData): Observable<IBetslipData | {}> {
    return this.getConfig().pipe(
      switchMap((config: IBetslipConfig) => {
        if (config.superAcca) {
          return observableFrom(this.sessionService.whenProxySession() as PromiseLike<void>).pipe(
            switchMap(() => this.accaService.getFreeBetOffer(betslipData)),
            catchError(() => observableOf(betslipData)));
        }
        return observableOf(betslipData);
      }));
  }

  /**
   * Extend selection data that we store in localStorage with siteServe outcomes data,
   * create BetSelection instances on each selection that we store in localStorage,
   * filter selection that have outcomes
   * @param {Array} outcomes
   */
  private extendSelections(outcomes: IOutcome[] | any): BetSelection[] | any[] {
    this.betSelectionsService.data = this.betSelectionService.restoreSelections(this.betslipStorageService.restore(), outcomes);
    this.betslipStorageService.store();
    return _.filter(this.betSelectionsService.data, (selection: BetSelection | any) => {
      return selection.isLotto ? true : selection.outcomes.length > 0;
    });
  }


  private placeBetsResult(response: IRespTransGetBetsPlaced | any, lottoData, req) {
    this.awsService.addAction('BetSlip=>placeBetRequest=>Success', { result: response, device: this.deviceService.parsedUA });
    const tooltipData = this.storageService.get('tooltipsSeen') || {};
    const receiptViewsCounter = (tooltipData[`receiptViewsCounter-${this.user.username}`] || null);
    tooltipData[`receiptViewsCounter-${this.user.username}`] = receiptViewsCounter === null ? 1 : receiptViewsCounter + 1;
    this.storageService.set('tooltipsSeen', tooltipData);
    const total = this.parsePlaceBetsResponse(response);
    if (lottoData) {
      total.bets.forEach((placeBetObj) => {
        const betObj = lottoData.find((textObj, ind) => {
          return req.leg[ind].documentId == placeBetObj.leg[0].documentId.split("-")[0] && textObj.id.includes(placeBetObj.leg[0].lotteryLeg.gameRef.id) && 
          (textObj.details.draws.length === placeBetObj.leg[0].lotteryLeg.subscription.number);
       });
       placeBetObj.details = betObj.details;
      });
    }
    this.betslipDataService.placedBets.bets = total.bets;
    this.gtmTrackingService.collectPlacedBets(total.bets);

    if(this.isBPMPFreeBetTokenUsed){
      this.overAskService.isBPMPFreeBetTokenUsed = true;
    } else {
      this.overAskService.isBPMPFreeBetTokenUsed = false;
    }

    if (!!total.errs && total.errs.length > 0) {
      return observableOf(total);
    } else if (!!total.providers && total.providers.indexOf('OpenBetBir') !== -1) {
      return this.birService.exectuteBIR(total);
    } else if (this.overAskService.isOverask(total)) {
      this.awsService.addAction('BetSlip=>readBetRequest=>OVERASK', { result: response, device: this.deviceService.parsedUA });
      return this.overAskService.execute(total);
    }
    return observableOf(total);
  }

  
  private filterByLottoStake(data: IBetSelection[]) {
   return data.filter(res => {
      return res.accaBets.filter(resp=> {
           return resp.stake || resp.userStake;
       }).length;
   });
  }

  /**
   * place bet Request, constructs betSlip and sends bets with stakes and legs to placeBet service
   * if there where temporary bets that where unsuspended then we send two placeBet requests:
   * first one with bets that we got from betSlipTemp data object (unsuspended temp bets from there)
   * second one with all other bets
   * @returns{promise}
   */
  private placeBetsRequest(lottoDataObj?): Observable<IBetsResponse | any> {
    let req, lottoData;
    if(lottoDataObj && lottoDataObj.isLotto){
      const lottoMaxcount = 20,
      currency = this.betData[0].stake.currency,
       {count, betDataArray} = this.filterAndCountBetsForLottos(lottoDataObj.lottoData);
      if(count > lottoMaxcount) {
        this.maximumStakesDialog(lottoMaxcount);
        return Observable.create((observer) => {
          observer.error('Maximum number of bets limit reached');
          observer.complete();
        });
      }
      req = this.lottoBuildBetDocService.constructPlaceBetObj(betDataArray, currency);
      lottoData = this.filterByLottoStake(lottoDataObj.lottoData);
    } else {
      req = this.placeBetDocService.buildRequest(this.construct(this.betslipDataService.betslipData));
    }
    // check in req object if freebet used is BPMP free bet
    if(!lottoDataObj) this.checkBPMPFreeBetTokenIsUsed(req.bet);
    // Adding new arg lottoData to append extra properties to display in lotto betreceipt.
    return this.bppService.send('placeBet', req).pipe(
      catchError(error => {
        if (error && error.code === '4016') {
          this.pubsub.publish(this.pubsub.API.SHOW_LOCATION_RESTRICTED_BETS_DIALOG);
        } else {
          // To prevent two modal windows: 1 - Unknown error has occurred, 2 - No internet connection
          setTimeout(() => {
            if (this.deviceService.isOnline()) {
              this.bppService.showErrorPopup(error);
            }
          }, 0);
        }

        return throwError(error);
      }),
      switchMap((response) => { return this.placeBetsResult(response, lottoData, req)}));
  }

  filterAndCountBetsForLottos(lottoData) {
   let count =0;
   const betDataArray = lottoData.filter( bet => {
      const accaBetsData = bet.accaBets.filter(accaBet => {
       if(accaBet.stake) { accaBet.betType === 'SGL_S' ? count += accaBet.lines.number : count++ }
       return accaBet.stake;
      });
      return accaBetsData.length;
    });
    return {count, betDataArray};
  }
  /**
   * determine whether BPMP Tokens are used in bets
   * @param {bets} any
 */
  private checkBPMPFreeBetTokenIsUsed(bets): void {
    const freeBetsStorage: string = this.storageService.get(`freeBets-${this.user.username}`);
    const UserFreebetTokens = _.isString(freeBetsStorage) ? JSON.parse(freeBetsStorage) : []; //get data from localstorage as it will be upadted after bet is placed sucessfully.
    const placedbetsWithFreebet = bets.filter(perbet => perbet.freebet);
    this.isBPMPFreeBetTokenUsed = placedbetsWithFreebet.some(eachplacedbetwithFreeBet => UserFreebetTokens.find(usertoken => eachplacedbetwithFreeBet.freebet.id == usertoken.freebetTokenId && usertoken.freebetOfferCategories && usertoken.freebetOfferCategories.freebetOfferCategory == 'Bet Pack'));
  }

  /**
   * Sending Build bet request
   * @params {array} legs
   * @return {object} object with bets and legs
   * BuildBet responce is an object of arrays containing these keys:
   * legs - array of bets that we send for build bet request
   * betErr - array of bet errors that we receive if our leg comes out of a inactive, errored outcome
   * bets - bets array that we receive from buildBet
   * If we receive data in betErr array - we filter out legs that contain errored outcome id's and
   * send buildBet request again with valid legs. We construct temporaty bets with legs that contain errors -
   * look into bsDoc.setResponse method, this method returns array of mocked bets or real bets.
   *
   * If we received errors we send another request and after that we merge both arrays of bets (mocked bets and real bets)
   */
  private buildBetsRequest(legs: SportsLeg[]): Observable<IBetslipData |any[]> {
    if (!legs.length) {
      return this.cleanData();
    }
    const service = this.user.bppToken ? 'buildBetLogged' : 'buildBet';

    return this.bppService.send(service, <IBppRequest>this.buildBetDocService.buildRequest(legs)).pipe(
      switchMap((buildBetResponceData: IBuildBetResponse): Observable<IBetslipData> => {
        // here we will have real constructed bets or mocked bets
        const bets = this.buildBetDocService.setResponse(buildBetResponceData);
        this.setSelectionErrors(bets);
        this.pubsub.publish(this.pubsub.API.SET_RESTRICTED_RACECARD);
        return observableOf(bets);
      }),
      catchError((err) => {
        this.bppService.showErrorPopup('betPlacementError');
        return throwError(err);
      }));
  }

  private buildBetsRequestByStoredData(legs: SportsLeg[] | any, storedSelections: IBetSelection[] |any): Observable<any[] | IBetslipData> {
    if (!legs.length) {
      return this.cleanData();
    }
    let service = this.user.bppToken ? 'buildBetLogged' : 'buildBet';
        service = legs.length && legs[0].isLotto ? this.user.bppToken ? 'lottoBuildBetLogged' : 'lottoBuildBet' : service;
    return this.bppService.send(service, <IBppRequest>this.buildBetDocService.buildRequest(legs)).pipe(
      // TODO: Refactor and remove call after LCRCORE-15476 resolved
      switchMap((buildBetResponceData: IBuildBetResponse | any): Observable<IBuildBetResponse> => {
        if(service.includes('lotto')) {
          //@@ TODO added this for lotto buldbet
          storedSelections.forEach((selection : IBetSelection,index:number) => {
            const betData = buildBetResponceData.find(accaObj => {
             return selection.details.priceId === accaObj.priceId &&
              accaObj.lotteryIds.includes(selection.id);
            });
            if(!selection.accaBets){
            selection.accaBets = betData.bets;
            selection.accaBets.forEach((accaBet)=>{
              accaBet.id = selection.id + '|'+index;
            })
          }
          });
          this.storageService.set('betSelections',storedSelections);
         return observableOf(buildBetResponceData);
        }

        let errorOutcomesIds = [],
          racingOutcomeIds = [];
        const racingSelections = storedSelections
          .filter(selection => (selection.details.info.sportId === '21' || selection.details.info.sportId === '19'));

        if (racingSelections.length && !this.betslipStorageService.eventToBetslipObservable) {
          racingOutcomeIds = _.flatten(_.pluck(racingSelections, 'outcomesIds'));
          this.deviceService.isDesktop && this.updateEWFlagInStoredSelection(buildBetResponceData);
        }

        this.betslipStorageService.eventToBetslipObservable = null;

        if (buildBetResponceData.betErrors && buildBetResponceData.betErrors.length) {
          buildBetResponceData.betErrors.forEach((betError: IBetErrorDoc) => {
            if (betError.outcomeRef && betError.outcomeRef.id) {
              errorOutcomesIds.push(betError.outcomeRef.id);
            }
          });
          errorOutcomesIds = _.uniq(errorOutcomesIds);
        }
        const outcomeIdsToUpdate = _.uniq(errorOutcomesIds.concat(racingOutcomeIds));

        if (outcomeIdsToUpdate.length) {
          return this.getEventsByOutcomes(outcomeIdsToUpdate, buildBetResponceData);
        }
        else{
          this.pubsub.publish(this.pubsub.API.SET_RESTRICTED_RACECARD,buildBetResponceData.outcomeDetails);
        }

        return observableOf(buildBetResponceData);
      }),
      switchMap((buildBetResponceData: IBuildBetResponse | any): Observable<IBetslipData> | Observable<any[]> => {
        if(storedSelections.length && storedSelections[0].isLotto) {
          const lottoBetData = this.extendSelections([]);
          lottoBetData.forEach((selection,index:number) => {
            const betData = buildBetResponceData.find(accaObj => accaObj.picks === selection.details.selections);
            if(!selection.accaBets){
            selection.accaBets = betData.bets;
            selection.accaBets.forEach((accaBet:AccaBets) => { accaBet.id = selection.id + '|'+index});
            }
          });
          const bets = this.buildBetDocService.setResponse(lottoBetData);
          return observableOf(bets);
        }
        if (buildBetResponceData.outcomeDetails && buildBetResponceData.outcomeDetails.length) {
          const data: Partial<IOutcome>[] = [];
          buildBetResponceData.outcomeDetails.forEach((details: IOutcomeDetailsResponse) => {
            const selection = storedSelections.find((sel: IBetSelection) => {
              return sel.outcomesIds[0] === details.id;
            });
            data.push(this.getSelectionDataService.createOutcomeData(details, selection));
          });

          this.extendSelections(data as IOutcome[]);

          const bets = this.buildBetDocService.setResponse(buildBetResponceData);
          this.setSelectionErrors(bets);

          return observableOf(bets);
        }

        return this.cleanData();
      }),
      catchError((err) => {
        this.betslipStorageService.eventToBetslipObservable = null;
        this.bppService.showErrorPopup('betPlacementError');
        return throwError(err);
      }));
  }

  /**
   * This method overwrites the EW value stored in localstorage with latest value coming in BuildBet API response
   * @param buildBetResponseData buildBetresponse
   */
   private updateEWFlagInStoredSelection(buildBetResponseData: IBuildBetResponse): void {
    let isUpdated: boolean;
    this.betSelectionsService.data.forEach((selection: BetSelection) => {
      if (selection?.details?.info && this.HORSE_RACING_CATEGORY_ID === selection.details.info.sportId && buildBetResponseData && selection.outcomes?.length > 0){
        const outcome = buildBetResponseData.outcomeDetails?.find((outcomeRes: IOutcomeDetailsResponse) => selection.outcomes[0].id == outcomeRes.id);
        if (outcome?.categoryId === this.HORSE_RACING_CATEGORY_ID && buildBetResponseData.legs) {
          const documentIds = buildBetResponseData.legs.filter((obj: IBetLeg) => {
            if (obj?.sportsLeg?.legPart.length > 0 && obj.sportsLeg.legPart[0]?.outcomeRef.id === outcome.id) {
              return obj.documentId;
            }
          }).map(obj => obj.documentId);
          if (documentIds.length > 0) {
            const eachWayAvailable = buildBetResponseData.bets?.find((obj: IBetDoc) => {
              if (obj?.betTypeRef?.id === 'SGL' && obj.legRef?.length > 0 && documentIds.includes(obj.legRef[0].documentId)) {
                return obj.eachWayAvailable
              }
            })?.eachWayAvailable;
            if (eachWayAvailable) {
              selection.details.isEachWayAvailable = eachWayAvailable === 'Y';
              isUpdated = true;
            }
          }
        }
      } 
    });
    isUpdated && this.betslipStorageService.store();
  }

  /**
   * Method to Remove Fanzone selections
   */
  removeFzSelectionsOnLogout(): void {
    const storedSelections = this.betslipStorageService.restore(),
    outcomesIds = this.betslipStorageService.getOutcomesIds(storedSelections);
    
    const fzStorage = this.fanzoneStorageService.get('fanzone') || {};
    if (storedSelections.length) {
      observableFrom(this.ssRequestHelper.getEventsByOutcomes({
        outcomesIds, isValidFzSelection: true
      }).then((response: { SSResponse: ISSResponse }) => {
        const outcomes = this.mapOutComes(response);
        outcomes.forEach((outcome) => {
          if (outcome && outcome.teamExtIds && outcome.isFanzoneMarket) {
            //Betslip validation for logged out scenario for clearing of invalid selections
            if (!this.user.status || (Object.keys(fzStorage).length && outcome.teamExtIds.replace(',', '') !== fzStorage.teamId)) {
              const remoteBS = this.sessionStorageService.get('RemoteBS');
              if (this.getBSFzMarket(remoteBS) && ( !this.user.status ||
                remoteBS.outcomes[0].id !== outcome.id) ) {
                this.sessionStorageService.remove('RemoteBS');
              }
              this.betslipStorageService.removeFanzoneSelections(outcome.id);
              this.windowRefService.nativeWindow.location.reload();
            }
          }
        });
      }));
    }
  }

  private getBSFzMarket(remoteBS) {
    return remoteBS && remoteBS.details 
                && remoteBS.details.hasOwnProperty('marketDrilldownTagNames') 
                && remoteBS.details.marketDrilldownTagNames.replace(',', '') === "MKTFLAG_FZ";
  }


 /**
   * Method to map outcomes for fanzone selections
   * @param outcomesResponse 
   * @returns - outcomes
   */
 mapOutComes(outcomesResponse) {
  const outcomes = [];
  _.each(outcomesResponse && outcomesResponse.SSResponse && outcomesResponse.SSResponse.children, (eventObj:any) => {
    _.each(eventObj.event && eventObj.event.children, (marketObj: IMarketEntity) => {
        _.each(marketObj.market && marketObj.market.children, (outcomeObj: IOutcomeEntity) => {
          if (outcomeObj.hasOwnProperty('outcome')) {
            outcomeObj.outcome.isFanzoneMarket = (marketObj.market.hasOwnProperty('drilldownTagNames') && (marketObj.market['drilldownTagNames'].replace(',', '') === "MKTFLAG_FZ"));
            outcomes.push(outcomeObj.outcome);
          }
        });
    });
  });
  return outcomes;
}

  private getEventsByOutcomes(outcomesIds: Array<string>, buildBetResponceData: IBuildBetResponse) {
    return Observable.create(observer => {
      this.ssRequestHelper.getEventsByOutcomes({
        outcomesIds, isValidFzSelection: true
      })
        .then((response: { SSResponse: ISSResponse }) => {
          const events = {},
            markets = {},
            outcomes = {};
          this.pubsub.publish(this.pubsub.API.SET_RESTRICTED_RACECARD, response);
          response.SSResponse.children.forEach((eventObj: ISportEventEntity) => {
            if (eventObj.event) {
              events[eventObj.event.id] = eventObj.event;
              if (eventObj.event.children) {
                eventObj.event.children.forEach((marketObj: IMarketEntity) => {
                  if (marketObj.market) {

                    markets[marketObj.market.id] = marketObj.market;
                    if (marketObj.market.children) {
                      marketObj.market.children.forEach((outcomeObj: IOutcomeEntity) => {
                        if (outcomeObj.outcome) {
                          outcomes[outcomeObj.outcome.id] = outcomeObj.outcome;
                        }
                      });
                    }
                  }
                });
              }
            }
          });
          buildBetResponceData.outcomeDetails.forEach((details: IOutcomeDetailsResponse) => {
            if (outcomes[details.id]) {
              details.eventStatusCode = events[details.eventId].eventStatusCode;
              details.isStarted = events[details.eventId].isStarted === 'true';
              details.isMarketBetInRun = markets[details.marketId].isMarketBetInRun === 'true';
              details.marketStatusCode = markets[details.marketId].marketStatusCode;
              details.outcomeStatusCode = outcomes[details.id].outcomeStatusCode;
              details.priceType = markets[details.marketId].priceTypeCodes.includes('LP') ? 'LP' : 'SP';
              details.isLpAvailable = markets[details.marketId].isLpAvailable;
              details.isSpAvailable = markets[details.marketId].isSpAvailable;
              details.isGpAvailable = markets[details.marketId].isGpAvailable;
              details.outcomeMeaningMinorCode = outcomes[details.id].outcomeMeaningMinorCode;
              details.marketDrilldownTagNames = markets[details.marketId].drilldownTagNames;
              details.eventDrilldownTagNames = events[details.eventId].drilldownTagNames;
            }
          });

          observer.next(buildBetResponceData);
          observer.complete();
        })
        .catch((err) => {
          observer.error(err);
        });
    });
  }


  private setSelectionErrors(betslipData: IBetslipData): void {
    if (betslipData.errs && betslipData.errs.length) {
      const outcomeErrorsList = {};
      betslipData.errs.forEach((betError: BetError) => {
        if (!outcomeErrorsList[betError.outcomeId]) {
          outcomeErrorsList[betError.outcomeId] = [];
        }

        outcomeErrorsList[betError.outcomeId].push(betError);
      });

      betslipData.bets.forEach((bet: Bet) => {
        const outcomeId = bet.info().outcomeId;

        if (outcomeErrorsList[outcomeId]) {
          bet.errs = outcomeErrorsList[outcomeId];

          this.betSelectionsService.data.forEach((selection) => {
            if (outcomeId === _.pluck(selection.outcomes, 'id').join('|')) {
              selection.errs = bet.errs;
            }
          });
        }
      });
    }
  }

  private filterNotRequestedScoreCast(betslipData: IBetslipData): IBetslipData {
    if(betslipData.bets && betslipData.bets.length && betslipData.bets[0]['isLotto']) {
      return betslipData;
    }
    const selectionIds = _.reduce(this.betSelectionsService.data, (arr: string[], selection: BetSelection) => {
      arr.push(selection.id);
      return arr;
    }, []),
      betWithOutScoreCast = [],
      addedBets = [];

    _.each(betslipData.bets, (bet: Bet) => {
      const betInfo = bet.info();
      let scoreCastEventId;

      if (betInfo.combiName === 'SCORECAST') {
        scoreCastEventId = `SCORECAST|${(<IEventIdsObject>betInfo.eventIds).outcomeIds.join('|')}`;
        if (selectionIds.indexOf(scoreCastEventId) !== -1 &&
          addedBets.indexOf(scoreCastEventId) === -1) {
          addedBets.push(scoreCastEventId);
          betWithOutScoreCast.push(bet);
        }
      } else {
        betWithOutScoreCast.push(bet);
      }
    });

    betslipData.bets = betWithOutScoreCast;
    return betslipData;
  }

  /**
   * Trigger clean Data function and trigger add to betslip finished for deeplink correct workflow.
   * @returns {object}
   */
  private cleanDataSync(): Observable<any[]> {
    this.pubsub.publishSync(this.pubsub.API.ADDTOBETSLIP_PROCESS_FINISHED);
    return this.cleanData();
  }

  private cleanData(): Observable<any[]> {
    if (!this.updating) { // don't clear betSlipData while updating
      this.betslipDataService.setDefault();
    }
    if (!this.toteBetSlipService.isToteBetPresent()) {
      this.pubsub.publishSync(this.pubsub.API.BETSLIP_COUNTER_UPDATE, this.count());
    }
    return observableOf([]);
  }


  /**
   * Updates price of current Bet model
   * @param {object} bet
   */
  private updatePrice(bet: any): void {
    const price = _.clone(bet.price);
    if (price.priceType === 'SP') {
      price.priceNum = undefined;
      price.priceDen = undefined;
    }

    delete price.isActive;
    delete price.displayOrder;
    delete price.id;
    bet.Bet.price.props = price;
  }

  /**
   *  If overask - do not cover suspended
   *
   * @param {object} singleItem
   * @returns {boolean}
   */
  private isSingleDisabled(singleItem: ISingleBet): boolean {
    return singleItem.disabled && !this.overAskService.isInProcess;
  }

  /**
   * compare two arrays of strings if they contains same values
   * ignore items order
   * compare outcome ids in updated bet with ids in stored bet
   * @param sourceIds {string[]} - outcome ids from updated bet
   * @param targetIds {string[]} - outcome ids from bet, saved it data storage
   */
  private isIdsEqual(sourceIds: string[], targetIds: string[]): boolean {
    if (!Array.isArray(sourceIds) || !Array.isArray(targetIds)) {
      return false;
    }

    return [...sourceIds].sort((a, b) => a < b ? -1 : a > b ? 1 : 0).toString() === [...targetIds].sort((a, b) => a < b ? -1 : a > b ? 1 : 0).toString();
  }

  private handleNotAllowedBets = (res: IBetslipData) => {
    if (
      this.count() > 1 &&
      res.errs.some(err => err.desc && err.desc.toLowerCase() === OB_BET_NOT_PERMITTED)
    ) {
      this.pubsub.publish(this.pubsub.API.BS_BET_NOT_ALLOWED);
    }

    return res;
  }
}
