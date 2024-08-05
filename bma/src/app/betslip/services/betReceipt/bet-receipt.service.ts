import { from as observableFrom, Observable, Subscription, of as observableOf, throwError } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, switchMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';
import * as _ from 'underscore';
import { StorageService } from '@core/services/storage/storage.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { DeviceService } from '@core/services/device/device.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import environment from '@environment/oxygenEnvConfig';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { ISportEvent } from '@core/models/sport-event.model';
import { IBetReceiptEntity } from './bet-receipt.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import {
  IBetDetail,
  IBetDetailLeg,
  IBetDetailLegPart,
  IBetOdds,
  IBetTermsChange,
  IClaimedOffer,
  IRequestTransGetBetDetail,
  IResponseTransGetBetDetail,
  IBetsResponse
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IGtmOrigin } from '@core/services/gtmTracking/models/gtm-origin.model';
import { AddToBetslipByOutcomeIdService } from '@betslip/services/addToBetslip/add-to-betslip-by-outcome-id.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { TemplateService } from '@app/shared/services/template/template.service';
import { TimeService } from '@core/services/time/time.service';
import { BetDetailUtils } from '@app/bpp/services/bppProviders/bet-detail.utils';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportInstance, ISportConfig } from '@core/services/cms/models';
import { UNNAMED_FAVOURITES } from '@core/services/raceOutcomeDetails/race-outcome.constant';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';
import { Bet } from '@betslip/services/bet/bet';
import { VanillaApiService } from '@frontend/vanilla/core';
import { IBetslipReceiptBanner } from '@app/betslip/models/betslip-receipt-banner-data.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { LUCKY_TYPES } from '@betslip/constants/bet-slip.constant';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';
interface IMessage {
  type?: string;
  msg?: string;
}

@Injectable({ providedIn: BetslipApiModule })
export class BetReceiptService {
  ids: string[];
  message: IMessage = {
    type: undefined,
    msg: undefined
  };
  maxPayOutFlag: boolean = false;
  betReceipt: boolean = false;
  horseRacingReceiptCheck: boolean = true;
  placeBetResponse: IBetsResponse;
  placeBetSub: Subscription;
  isLuckyInfo: any;
  isBetSlipShown: any;
  isBetReceiptShown: any;
  private receipts: IBetDetail[];
  private env: any = environment;
  private footballConfig: ISportConfig;
  isbetSlipHaveEst = false;
  private isBetCanceled: (stake: IBetDetail) => boolean = BetDetailUtils.isCanceled;
  private readonly PATH: string = 'content/teasers?path=betReceipt';
  // Fall Back Special Type Id's
  private specialsTypeIds: Array<number> = [2297, 2562];
  currencySymbol: string;
  isLuckyBonusAvailable: boolean = false;
  private betList = ['L15', 'L31', 'L63'];
  constructor(
    private storageService: StorageService,
    private bppService: BppService,
    private siteServerService: SiteServerService,
    private pubSubService: PubSubService,
    private fracToDecService: FracToDecService,
    private filtersService: FiltersService,
    private deviceService: DeviceService,
    private betslipStorageService: BetslipStorageService,
    private addToBetslipService: AddToBetslipByOutcomeIdService,
    private coreToolsService: CoreToolsService,
    private gtmTrackingService: GtmTrackingService,
    private betslipDataService: BetslipDataService,
    private user: UserService,
    private localeService: LocaleService,
    private templateService: TemplateService,
    private timeService: TimeService,
    private sportsConfigService: SportsConfigService,
    private awsService: AWSFirehoseService,
    protected gtmService: GtmService,
    private http: HttpClient,
    private nativeBridgeService: NativeBridgeService,
    private betslipService: BetslipService,
    private vanillaApiService: VanillaApiService,
    protected cmsService: CmsService,
    private scorecastDataService: ScorecastDataService,
  ) {
    this.getEWTerms = this.getEWTerms.bind(this);
    this.getLinesPerStake = this.getLinesPerStake.bind(this);
    this.placeBetSub = this.betslipService.placeBetResponse.subscribe(response => this.placeBetResponse = response);
    this.sportsConfigService.getSport('football').subscribe((footballConfig: ISportInstance) => {
      this.footballConfig = footballConfig.sportConfig;
      this.awsLogs(footballConfig);
    });
    this.isLuckyInfo = this.cmsService.systemConfiguration['LuckyBonus'];
    this.isBetSlipShown = this.isLuckyInfo && this.isLuckyInfo['BetSlipPopUpHeader'] && this.isLuckyInfo['BetSlipPopUpHeader'].trim().length > 0 && this.isLuckyInfo['BetSlipPopUpMessage'] && this.isLuckyInfo['BetSlipPopUpMessage'].trim().length > 0;
    this.isBetReceiptShown = this.isLuckyInfo && this.isLuckyInfo['BetReceiptPopUpHeader'] && this.isLuckyInfo['BetReceiptPopUpHeader'].trim().length > 0 && this.isLuckyInfo['BetReceiptPopUpMessage'] && this.isLuckyInfo['BetReceiptPopUpMessage'].trim().length > 0;
  }

  get freeBetStake(): string {
    return _.reduceRight(this.receipts, (sum: number, betReceipt: IBetDetail) => {
      return sum + Number(betReceipt.tokenValue);
    }, 0).toFixed(2);
  }
  set freeBetStake(value:string){}

  get totalStake(): string {
    return this.getTotalStake();
  }
  set totalStake(value:string){}

  get totalEstimatedReturns(): string {
    return this.getTotalReturns();
  }

  set totalEstimatedReturns(value:string){}

  awsLogs(footballConfig: ISportInstance): void {
    const categoryId = footballConfig.sportConfig && footballConfig.sportConfig.config.request.categoryId;
    if (!categoryId) {
      this.awsService.addAction('betRecieptService=>sportsConfig=>Fail', { categoryId });
    }
  }

  /**
   * Gets bets receipts.
   * @return {Promise}
   */
  getBetReceipts(): Observable<IBetReceiptEntity[] | void> {
    const placedBets = this.betslipDataService.placedBets && this.betslipDataService.placedBets.bets;
    let isOveraskScenario = false;
    let isPrePlay = false;
    placedBets.some((bet: Bet) => {
      if (bet.isReferred === 'Y') {
        isOveraskScenario = true;
      }
      if (bet.isConfirmed === 'Y') {
        isPrePlay = true;
      }
    });
    if (isOveraskScenario) {
      return this.ids
        ? this.bppService.send('getBetDetail',
          <IRequestTransGetBetDetail>{
            betId: this.ids,
            returnPartialCashoutDetails: 'Y'
          }).pipe(
            // extract receipt bets only
            map((receiptData: IResponseTransGetBetDetail): IBetDetail[] => receiptData.response.respTransGetBetDetail.bet),
            switchMap((receiptBets: IBetDetail[]) => {
              return this.mergeAndModifyResponseData(receiptBets);
            }))
        : observableOf(null);
    } else if (isPrePlay) {
      return this.mergeAndModifyResponseData(placedBets);
    } else if (!isPrePlay) {
      const readBets = this.betslipDataService.readBets && this.betslipDataService.readBets.bets;
      return this.mergeAndModifyResponseData(readBets);
    }
  }

  getGtmObject(receipt: IBetReceiptEntity, totalStake: number) {
    const products = this.parseBetsFromReceipt(receipt);
        return {
      ecommerce: {
        purchase: {
          actionField: {
            id: `${products.map(i => i.id).sort((a, b) => a < b ? -1 : a > b ? 1 : 0)[0]}:${products.length}`,
            revenue: totalStake
          },
          products
        }
      }
    };
  }

  /**
   * Reuse outcome and build the same betslip.
   * @params {number[]} outcomesIdsList
   * @return {Promise<boolean | void>} - promise
   */
  reuse(outcomesIdsList?: string[]): Promise<boolean | void | string[] | unknown> {
    const outcomesIds = outcomesIdsList || this.getOutcomeIds();
    let selections$: Observable<boolean | void |  string[] | unknown>;

    if (outcomesIds.length > 0) {
      this.siteServerService.isValidFzSelection = true;
      selections$ = observableFrom(this.siteServerService.getEventsByOutcomeIds({ outcomesIds })).pipe(
        map(this.sortByOutcomeIds(outcomesIds)),
        switchMap(() => {
          return this.addToBetslipService.reuseSelections(outcomesIds, this.receipts, 'betslip');
        }),
        map(() => {
          this.gtmTrackingService.restoreGtmTracking(outcomesIds);
          return outcomesIds;
        }),
        map(() => {
          this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
          return outcomesIds;
        }),
        catchError(err => {
          console.warn('Error while getEventsByOutcomeIds (BetReceiptService.getEventsByOutcomeIds)', err);
          this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
          return observableOf(null);
        }));
    } else {
      this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
      selections$ = observableOf(true);
    }
    this.pubSubService.publish(this.pubSubService.API.REUSE_OUTCOME);
    this.message = { type: undefined, msg: undefined };
    return selections$.toPromise();
  }

  getBetReceiptSiteCoreBanners(): Observable<IBetslipReceiptBanner[]> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(this.PATH, '', APIOPTIONS);
  }
  /**
   * Action on receipt 'Done' btn
   * - On done suspended outcomes saved in BetSlip
   * - Redirect to home page (close BetSlip)
   */
  done(): void {
    if (this.deviceService.isMobile) {
      // sync to `show-${this.sideClass}` in sidebar.component
      this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
    } else {
      this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
    }

    const outcomesIds = this.getSuspendedOutcomeIds();

    if (outcomesIds.length > 0) {
      observableFrom(this.siteServerService.getEventsByOutcomeIds({ outcomesIds })).pipe(
        map(this.sortByOutcomeIds(outcomesIds)),
        switchMap(() => this.addToBetslipService.addToBetSlip(outcomesIds.join(','), true, true, false)),
        catchError(err => {
          console.error('Error while getEventsByOutcomeIds (BetReceiptService.getEventsByOutcomeIds)', err);
          return observableOf(null);
        }));
    }

    this.clearMessage();
  }

  /**
   * Add all football events to favourites from receipts.
   * @return array of football events
   */
  getActiveFootballEvents(receiptsEntity: IBetReceiptEntity): ISportEvent[] {
    const arr: ISportEvent[] = [];
    // adding all football events from singles to array

    _.each(receiptsEntity.singles, (receipt: IBetDetail): void => {
      receipt.isFootball && arr.push(receipt.leg[0].part[0].event);
    });
    // adding all football events from multuples to array
    _.each(receiptsEntity.multiples, (receipt: IBetDetail): void => {
      _.each(receipt.leg, (leg: IBetDetailLeg): void => {
        leg.part && leg.part[0].isFootball && arr.push(leg.part[0].event);
      });
    });
    // return all events from singles and multiples without duplicates
    return _.uniq(arr);
  }

  /**
   * Add all events to favourites from receipts.
   * @return array of football events
   */
  getActiveSportsEvents(receiptsEntity: IBetReceiptEntity): ISportEvent[] {
    const arr: ISportEvent[] = [];

    _.each(receiptsEntity.singles, (receipt: IBetDetail): void => {
      if(receipt.leg[0].part) {
        const event = this.coreToolsService.deepClone(receipt.leg[0].part[0].event);
        event.selectionId = receipt.leg[0].part[0].outcome;
        event.marketId = receipt.leg[0].part[0].marketId;
        arr.push(event);
      }
    });
    _.each(receiptsEntity.multiples, (receipt: IBetDetail): void => {
      _.each(receipt.leg, (leg: IBetDetailLeg): void => {
        if(leg.part) {
        const event = this.coreToolsService.deepClone(receipt.leg[0].part[0].event);
        event.selectionId = leg.part[0].outcome;
        event.marketId = leg.part[0].marketId;
        arr.push(event);
        }
      });
    });
    // return all events from singles and multiples without duplicates
    return _.uniq(arr);
  }

  hasStake(receipt: IBetDetail): boolean {
    return Number(receipt.tokenValue) > 0 && Number(receipt.stake) - Number(receipt.tokenValue) > 0;
  }

  getStake(receipt: IBetDetail): number {
    return Number(receipt.stake) - Number(receipt.tokenValue);
  }

  getReceiptOdds(item: IBetDetail): string {
    return item.odds[this.user.oddsFormat];
  }

  setToggleSwitchId(receipt: IBetDetail): string {
    return `toggle-switch-betslip-${receipt.betId}`;
  }

  hasStakeMulti(receipt: IBetDetail): boolean {
    return Number(receipt.tokenValue) > 0 && Number(receipt.stakePerLine) * Number(receipt.numLines) - Number(receipt.tokenValue) > 0;
  }

  getStakeMulti(receipt: IBetDetail): number {
    return Number(receipt.stakePerLine) * Number(receipt.numLines) - Number(receipt.tokenValue);
  }

  getStakeTotal(receipt: IBetDetail): number {
    return Number(receipt.stakePerLine) * Number(receipt.numLines);
  }

  getEWTerms(legPart: IBetDetailLegPart): string {
    return this.localeService.getString('bs.oddsAPlaces', {
      num: legPart.eachWayNum,
      den: legPart.eachWayDen,
      arr: this.templateService.genEachWayPlaces(legPart, true)
    });
  }

  getLinesPerStake(receipt: IBetDetail): string {
    return this.localeService.getString('bs.linesPerStake', {
      lines: receipt.numLines,
      currency: this.user.currencySymbol,
      stake: Number(receipt.stakePerLine).toFixed(2)
    });
  }

  /**
   * Make price format according to User settings
   * @returns {String}
   */
  getFormattedPrice(receipt: IBetDetail): string {
    const potentialPayout = this.getMultiplePotentialPayout(receipt);

    return this.convertPotentialPayout(potentialPayout);
  }

  /**
   * Clear message
   */
  clearMessage(): void {
    this.message = { type: undefined, msg: undefined };
  }

  /**
   * Exclude extra place promo label for race unnamed favourites
   * @param selectionName
   */
  getExcludedDrillDownTagNames(selectionName: string): string {
    if (selectionName && UNNAMED_FAVOURITES.indexOf(selectionName.toLowerCase()) >= 0) {
      return 'MKTFLAG_EPR, EVFLAG_EPR';
    }

    return '';
  }

  readUpCellBets(url, body): Observable<any> {
    const headers = new HttpHeaders({
      token: this.user.bppToken
    });
    return this.http.post<any[]>(url, body, { headers });
  }

  /**
   * merges event data with bet data from response of placeBet/readBet/getBetDetail call
   * @return {Observable}
   */
   private mergeAndModifyResponseData(bets): Observable<IBetReceiptEntity[]> {
    const filters = {
      includeUndisplayed: true,
      outcomesIds: this.getEventIds(bets)
    };
    this.checkMaxPayOut(bets);
    // get events for receipts
    return observableFrom(this.siteServerService.getEventsByOutcomeIds(filters, false)).pipe(
      map((events: ISportEvent[]) => {
        this.mergeEventsWithReceipts(events, bets);
        this.markFootballReceipts(bets);
        this.markBoostedReceipts(bets);
        this.extendWithAccaInsuranceData(bets);
        this.markForeCastTricastReceipts(bets);
        this.updateVirtualEventNames(bets);
        this.markBogReceipts(bets);
        this.setFreebetOfferCategory(bets);
        _.each(bets, (betReceipt: IBetDetail): void => {
          let eventCategoryNames = '';
          _.each(betReceipt.leg, (leg: IBetDetailLeg, index: number): void => {
            if(leg.part) {
              eventCategoryNames += leg.part[0].event.categoryName + (index === (betReceipt.leg.length - 1) ? '' : ', ');
            }
          });
          this.nativeBridgeService.betPlaceSuccessful(betReceipt.receipt, eventCategoryNames, betReceipt.betTypeName);
        });
        this.checkForHorseRacingReceipts(bets);
        return this.divideOnSinglesAndMultiples(bets);
      }),
      catchError(error => {
        this.awsService.addAction('betRecieptService=>siteservercall=>EventToOutcomeForEvent=>Fail', { 'url': error.url });
        console.warn(error);
        return throwError(error);
      })
    );
  }

  /**
   * Check for horse racing events from receipts.
   */
  checkForHorseRacingReceipts(receiptsEntity: IBetDetail[]): void {
      const arr = [];
      receiptsEntity.forEach((bet: IBetDetail): void => {
        bet.leg.forEach((leg: IBetDetailLeg): void => {
          leg.part && arr.push(leg.part[0].eventCategoryId);
        });
      });
      this.horseRacingReceiptCheck = arr.includes(environment.HORSE_RACING_CATEGORY_ID);
  }

  private convertPotentialPayout(potentialPayout: string | number): string {
    if (this.user.oddsFormat === 'frac') {
      return this.fracToDecService.decToFrac(potentialPayout, true);
    } else {
      return Number(potentialPayout).toFixed(2);
    }
  }

  /**
   * Calculate potentialPayout for ACCA and Double,
   * it's made by multiplying all related singles dec prices
   * @param betslipStake {object}
   * @return potentialPayout {number}
   */
  private getMultiplePotentialPayout(receipt: IBetDetail): number {
    const newSinglesPrices = [];
    receipt.leg.forEach((leg: IBetDetailLeg) => {
      newSinglesPrices.push(Number(leg.odds.frac.split('/')[0]) / Number(leg.odds.frac.split('/')[1]) + 1);
    });

    return newSinglesPrices.reduce((prev: number, current: number) => prev * current);
  }

  private extendWithAccaInsuranceData(receiptBets: IBetDetail[]): void {
    const accaInsuranceBetsMap = {};

    _.each(this.betslipDataService.placedBets.bets, (placedBet: any) => {
      if (_.has(placedBet, 'claimedOffers') && this.isQualifiedAccaInsurance(placedBet.claimedOffers)) {
        accaInsuranceBetsMap[String(placedBet.id)] = placedBet;
      }
    });

    _.each(receiptBets, (bet: IBetDetail) => {
      const insuranceBet = accaInsuranceBetsMap[bet.betId];
      if (insuranceBet) {
        _.extend(bet, { claimedOffers: insuranceBet.claimedOffers });
      }
    });
  }

  private isQualifiedAccaInsurance(offers: IClaimedOffer[]): boolean {
    return _.some(offers, (offer: IClaimedOffer) => offer.status === 'qualified' && offer.offerCategory === 'Acca Insurance');
  }

  private parseBetsFromReceipt(receipt: IBetReceiptEntity) {
    const singles = receipt.singles && receipt.singles.length ? this.buildGtmObject(receipt.singles) : [];
    const multiples = receipt.multiples && receipt.multiples.length ? this.buildGtmObject(receipt.multiples, true) : [];
    this.betslipService['_betKeyboardData'] = [];
    this.storageService.remove('betKeyboardData');
    this.storageService.remove('reuseBetSelections');
    return singles.concat(multiples);
  }

  private buildGtmObject(bets: IBetDetail[], isMultiple?: boolean) {
    const multText: string = 'multiple';
    let isSameCategory: boolean;
    let isSameType: boolean;
    let isSameMarket: boolean;
    return _.map(bets, (bet: IBetDetail) => {
      const outcomeIds = this.getOutcomeIds([bet]);

      let betOrigin: IGtmOrigin;
      let odds;

      if (isMultiple) {
        isSameCategory = this.isSameCategory(bet);
        isSameType = this.isSameType(bet);
        isSameMarket = this.isSameMarket(bet);
      }

      if (isSameCategory || isSameType || isSameMarket) {
        betOrigin = this.compareAndSetBetOrigin(outcomeIds, multText);
        isSameMarket && (bet.eventMarket = this.getEventMarket(bet.leg[0], bet.numLines));
      } else {
          betOrigin = !isMultiple ? this.gtmTrackingService.getBetOrigin(outcomeIds[0]) : this.compareAndSetBetOrigin(outcomeIds, multText);
      }

      if (isMultiple || !bet.odds) {
        if (typeof(bet.stake) === 'object' && bet.stake.amount && bet.potentialPayout && !isNaN(+bet.potentialPayout)) {
          odds = +(Number(bet.potentialPayout) / Number(bet.stake.amount)).toFixed(2);
        } else {
          odds = 'SP';
        }
      } else {
        odds = bet.odds.dec === 'SP' ? 'SP' : +bet.odds.dec;
      }
      
      return this.getBetGtmObject({
        bet, isMultiple, multText, outcomeIds, betOrigin, odds, isSameCategory, isSameType, isSameMarket
      });
    });
  }

  private getBetGtmObject({
    bet, isMultiple, multText, outcomeIds, betOrigin, odds, isSameCategory, isSameType, isSameMarket
  }): { [key: string]: any } {
    const isStarted = _.some(bet.leg, (leg: IBetDetailLeg) => _.some(leg.part, (part: IBetDetailLegPart) =>
      part.event && part.event.isStarted));
    const isBuildYourBet = this.env.BYB_CONFIG && this.env.BYB_CONFIG.HR_YC_EVENT_TYPE_ID === Number(bet.leg[0].part[0].event.typeId);
    const gtmObject = {
      name: isMultiple ? bet.betTypeName : String(bet.leg[0].part[0].event.name),
      id: bet.receipt,
      price: Number(bet.stake?.amount || 0),
      dimension60: isMultiple ? multText : String(bet.leg[0].part[0].event.id),
      dimension61: outcomeIds.join(','),
      dimension62: isStarted ? 1 : 0,
      dimension63: isBuildYourBet ? 1 : 0,
      dimension64: isMultiple && !betOrigin.betType ? multText : betOrigin.location,
      dimension65: isMultiple ? multText : betOrigin.module,
      dimension66: Number(bet.numLines),
      dimension67: odds,
      dimension86: bet.oddsBoosted ? 1 : 0,
      dimension166: betOrigin.betType? betOrigin.betType : 'normal',
      dimension180: bet.leg[0].part[0].event.categoryId == '39' ? 'virtual' : 'normal',
      metric1: Number(bet.tokenValue || 0),
      category: isMultiple && !isSameCategory ? multText : bet.leg[0].part[0].event.categoryId,
      variant: isMultiple && !isSameType ? multText : bet.leg[0].part[0].event.typeId,
      brand: isMultiple && !isSameMarket ? multText : bet.eventMarket,
      quantity: 1
    };
    const betInfo = this.gtmService.getSBTrackingData();
    const selectionObj = betInfo.find(res => res.outcomeId && res.outcomeId.length && outcomeIds && outcomeIds.length && outcomeIds[0] == res.outcomeId[0]);
    if(selectionObj && selectionObj.GTMObject.betData.dimension94) {
      Object.assign(gtmObject, {
        dimension90: bet.betId,
        dimension94: selectionObj.GTMObject.betData.dimension94
      });

      this.gtmService.removeSBTrackingItem(selectionObj);
    }
    if(this.betslipService.betKeyboardData.filter((x) => !x.includes('All_single_quickStake')).some(outcomes=>outcomes.split('-')[1]===outcomeIds.join(','))){
      Object.assign(gtmObject, {
        dimension181:'keyboard predefine stake',
      });
     }
     if(this.isLuckyBonusAvailable){
      gtmObject.name=gtmObject.name+" - bonuses"
     }
     const plData = this.scorecastDataService.getScorecastData();
     if(plData && plData.eventLocation   === 'scorecast') {
      Object.assign(gtmObject, {
        dimension180: `scorecast;${plData.teamname};${plData.playerName};${plData.result}`,
        brand: 'Match Betting',
        name: plData.name,
        dimension64: plData.dimension64,
        dimension65: 'edp',
      });
  }
  return gtmObject;
  }
  private isSameCategory(bet: IBetDetail): boolean {
    const categoryId = bet.leg[0].part[0].event.categoryId;

    return bet.leg.every(legInstance => {
      return categoryId === legInstance.part[0].event.categoryId;
    });
  }

  private isSameType(bet: IBetDetail): boolean {
    const typeId = bet.leg[0].part[0].event.typeId;

    return bet.leg.every(legInstance => {
      return typeId === legInstance.part[0].event.typeId;
    });
  }

  private isSameMarket(bet: IBetDetail): boolean {
    const eventMarketDesc = bet.leg[0].part[0].eventMarketDesc;

    return bet.leg.every(legInstance => {
      return eventMarketDesc === legInstance.part[0].eventMarketDesc;
    });
  }

  private compareAndSetBetOrigin(outcomeIds: string[], multText: string): IGtmOrigin {
    const originsArr = [];
    outcomeIds.forEach(id => {
      originsArr.push(this.gtmTrackingService.getBetOrigin(id));
    });
    const locationNames = originsArr.map(a => a.location);
    const moduleName = originsArr[0].module;
    const betType = originsArr.length > 1 ?
                    (originsArr.findIndex(a => a.betType && a.betType.toLowerCase() === 'reuse') ? 'reuse' : originsArr[0].betType)
                    : originsArr[0].betType;
    const isOneLocation = originsArr.every(betOrigin => {
      return locationNames[0] === betOrigin.location;
    });
    const isOneModule = originsArr.every(betOrigin => {
      return moduleName === betOrigin.module;
    });

    return {
      location: isOneLocation ? locationNames[0] : this.removeDuplicates(locationNames),
      module: isOneModule ? moduleName : multText,
      betType: betType
    };
  }

  /**
   * removes duplicates items in an array
   * @param {Array} [locations]
   * @returns {array}
   */
  private removeDuplicates(locations): string {
    const filteredArray =  locations.filter((item,
        index) => locations.indexOf(item) === index);
    return filteredArray.toString();
  }

  /**
   * Calculate total stake
   * @param {Array} [betReceipts]
   * @returns {String}
   */
  private getTotalStake(betReceipts: IBetDetail[] = this.receipts): string {
    return _.reduceRight(betReceipts, (sum: number, betReceipt: IBetDetail | any ): number => {
      const isLottoBet = betReceipt && betReceipt.provider && betReceipt.provider.includes('Lottery');
      const lottoTotalStake = Number(betReceipt && betReceipt.lines && betReceipt.lines.number || 0.00) * 
      Number(betReceipt.leg.length && betReceipt.leg[0].lotteryLeg && betReceipt.leg[0].lotteryLeg.subscription &&betReceipt.leg[0].lotteryLeg.subscription.number || 0.00);
      return isLottoBet ? sum + (Number(betReceipt.stakePerLine || betReceipt.stake.stakePerLine)) * lottoTotalStake : sum + (Number(betReceipt.stakePerLine || betReceipt.stake.stakePerLine) * Number(betReceipt.numLines ));
    }, 0).toFixed(2);
  }

  /**
   * Calculate total estimated returns
   * @param {Array} [betReceipts]
   * @returns {String}
   */
  private getTotalReturns(betReceipts: IBetDetail[] = this.receipts): string {
    const isAnyNA = _.some(betReceipts, (betReceipt: IBetDetail): boolean => {
      return _.isNaN(Number(betReceipt.potentialPayout));
    });
    if (isAnyNA || (!this.checkForStraightMultiples(betReceipts) && !this.isbetSlipHaveEst)) {
      return 'N/A';
    }

    const result = _.reduceRight(betReceipts, (sum: number, betReceipt: IBetDetail): number => {
      const isLottoBet = betReceipt && betReceipt.provider && betReceipt.provider.includes('Lottery');
      const lottoEstReturns = sum + (Number(betReceipt.potentialPayout || 0.00) * 
      Number(betReceipt.leg && betReceipt.leg.length && betReceipt.leg[0].lotteryLeg && betReceipt.leg[0].lotteryLeg.subscription && betReceipt.leg[0].lotteryLeg.subscription.number || 0.00));
      return isLottoBet ? lottoEstReturns : sum + Number(betReceipt.potentialPayout);
    }, 0);

    return result > 0 ? result.toFixed(2) : 'N/A';
  }

  /**
   * @param bets {IBetslipBetData[]}
   * @returns {boolean}
   */
   private checkForStraightMultiples(bets: IBetDetail[] | any): boolean {
    if(bets.some(bet => bet.provider && bet.provider.includes('Lottery'))) {
      return true;
    }
    if(bets.length === 1 && bets[0].betType === 'SGL') {
      return true;
    }

    const multiBets = bets.filter(bet => bet.betType !== 'SGL');
    if (multiBets.length === 0) {
      return false;
    }

    return multiBets.some((bet: IBetDetail) => ['DBL', 'TBL', 'AC'].some(type => bet.betType.includes(type)) && (bet.numLines == '1' || (bet.legType === 'E' && bet.numLines == '2')));
  }

  private getEventIds(receiptBets: IBetDetail[]): string[] {
    const arr = [];
    _.each(receiptBets, (bet: IBetDetail): void => {
      _.each(bet.leg, (leg: IBetDetailLeg): void => {
        _.each(leg.part, (part: IBetDetailLegPart): void => {
          arr.push(part.outcome);
        });
      });
    });
    return arr;
  }

  /**
   * Extend betreceipt with full event data
   * @return object of event
   */
  private mergeEventsWithReceipts(events: ISportEvent[], receiptBets: IBetDetail[]): void {
    _.each(receiptBets, (receipt: IBetDetail): void => {
      // extending event from single receipt with all corresponding event data
      if (receipt.betType === 'SGL') {
        _.each(events, (event: ISportEvent): void => {
          if (Number(receipt.leg[0].part[0].eventId) === Number(event.id)) {
            receipt.leg[0].part[0].event = event;
          }
        });
        // extending events from multiple receipt with all corresponding events data
      } else {
        _.each(events, (event: ISportEvent): void => {
          _.each(receipt.leg, (leg: IBetDetailLeg): void => {
            _.each(leg.part, (part: IBetDetailLegPart): void => {
              if (Number(part.eventId) === Number(event.id)) {
                part.event = event;
              }
            });
          });
        });
      }
    });
  }

  private setFreebetOfferCategory(receiptBets: IBetDetail[]){
    _.each(receiptBets, (betReceipt: IBetDetail): void => {     
          if( typeof(betReceipt.stake)=='object' && betReceipt.stake.freebetOfferCategory){
            betReceipt.freebetOfferCategory =betReceipt.stake.freebetOfferCategory;
          }
    });
  }

  /**
   * Check for football events from receipts.
   * @return Boolean (true for football).
   */
  private markFootballReceipts(receiptsEntity: IBetDetail[]): void {
    _.each(receiptsEntity, (receipt: IBetDetail): void => {
      // check for football events from singles
      if (receipt.betType === 'SGL') {
        if (receipt.leg[0].part?.length && receipt.leg[0].part[0].event.categoryId === (this.footballConfig && this.footballConfig.config.request.categoryId
          || environment.CATEGORIES_DATA.footballId) &&
          !this.isSpecialEvent(receipt.leg[0].part[0].event)) {
          receipt.isFootball = true;
        }
        // check for football events from multiples
      } else {
        _.each(receipt.leg, (leg: IBetDetailLeg): void => {
          if (leg.part && leg.part[0].event.categoryId === (this.footballConfig && this.footballConfig.config.request.categoryId
            || environment.CATEGORIES_DATA.footballId)
            && !this.isSpecialEvent(leg.part[0].event)) {
            leg.part[0].isFootball = true;
          }
        });
      }
    });
  }

  private markBoostedReceipts(receiptsEntity: IBetDetail[]): void {
    _.each(receiptsEntity, (receipt: IBetDetail): void => {
      receipt.oddsBoosted = _.some(receipt.betTermsChange, (terms: IBetTermsChange) => terms.reasonCode === 'ODDS_BOOST');
    });
  }

  /**
   * Check for specials events (outrights and enchanced multiples)
   */
  private isSpecialEvent(event: ISportEvent): boolean {
    // Checks if event - Enhance Multiples.
    let isEnhanceMultiples;
    if (this.footballConfig && this.footballConfig.specialsTypeIds) {
      isEnhanceMultiples = _.contains(this.footballConfig.specialsTypeIds, Number(event.typeId));
    } else {
      // FallBack Option
      isEnhanceMultiples = _.contains(this.specialsTypeIds, Number(event.typeId));
    }
    // Checks if event - OutRight.
    const sortCodeList = _.indexOf(OUTRIGHTS_CONFIG.outrightsSports, event.categoryCode) !== -1
      ? OUTRIGHTS_CONFIG.outrightsSportSortCode : OUTRIGHTS_CONFIG.sportSortCode,
      isOutRight = sortCodeList.indexOf(event.eventSortCode) !== -1;

    // check if event special (Enhance Multiples or OutRight).
    return isEnhanceMultiples || isOutRight;
  }

  /**
   * Puts outcomes in order by they ids, same as in outcomesIds.
   *
   * @param outcomesIds
   * @returns {Function}
   */
  private sortByOutcomeIds(outcomesIds: string[]): (data: ISportEvent[]) => ISportEvent[] {
    return (data: ISportEvent[]): ISportEvent[] => {
      _.each(data, (event: ISportEvent): void => {
        _.each(event.markets, (market: IMarket) => {
          market.outcomes.sort((a: IOutcome, b: IOutcome): number => {
            const aIndex = outcomesIds.indexOf(a.id),
              bIndex = outcomesIds.indexOf(b.id);

            if (aIndex !== -1 && bIndex !== -1) {
              if (aIndex < bIndex) {
                return -1;
              } else if (aIndex > bIndex) {
                return 1;
              }
            }

            return 0;
          });
        });
      });

      return data;
    };
  }

  /**
   * Split bet receipts into 2 array and prepare data
   *  keeps only placed bets to work with (within this service),
   *  passes 2 entities with placed and all (including canceled) bets further
   *
   * @param  {Array} betsReceipts - array with bet receipts
   * @return {Object[]} - array of objects with singles and multiples
   */
  private divideOnSinglesAndMultiples(betsReceipts: IBetDetail[]): IBetReceiptEntity[] {
    betsReceipts = this.setOutcomeNames(betsReceipts);

    const
      allReceipts: IBetReceiptEntity = {
        singles: this.filterReceipts('filter', betsReceipts),
        multiples: this.filterReceipts('reject', betsReceipts)
      },
      activeReceipts: IBetReceiptEntity = {
        singles: allReceipts.singles.filter((bet: IBetDetail) => !this.isBetCanceled(bet)),
        multiples: allReceipts.multiples.filter((bet: IBetDetail) => !this.isBetCanceled(bet))
      };

    this.receipts = [].concat(activeReceipts.singles).concat(activeReceipts.multiples);

    return [allReceipts, activeReceipts];
  }

  /**
   * Add handicap values to names if available
   * @prams {array} receipts
   * @return {array} receipts
   */
  private setOutcomeNames(receiptsEntity: IBetDetail[]): IBetDetail[] {
    _.each(receiptsEntity, (receipt: IBetDetail): void => {
      _.each(receipt.leg, (leg: IBetDetailLeg): void => {
        _.each(leg.part, (part: IBetDetailLegPart): void => {
          if (part.handicap.length) {
            part.description = part.description + this.filtersService.makeHandicapValue(part.handicap, part);
            receipt.name = receipt.name + this.filtersService.makeHandicapValue(part.handicap, part);
          }
        });
      });
    });
    return receiptsEntity;
  }

  /**
   * Gets outcome ids which is already in betslip.
   * @return {[type]} [description]
   */
  private getOutcomesInBetSlip(): string[] {
    const betslip: IBetSelection[] = this.betslipStorageService.restore();

    return _.reduceRight(betslip, (ids: string[], outcome: IBetSelection): string[] => {
      return ids.concat(outcome.outcomesIds);
    }, []);
  }

  /**
   * Get suspended outcome ids
   */
  private getSuspendedOutcomeIds(): string[] {
    return this.storageService.get('betSuspendedSelections') || [];
  }

  /**
   * Gets outcome ids from bet receipts, betslip, suspended ids
   * @return {Array} - array with outcome ids.
   * @return {boolean} - falg to get outcomesIds only from source.
   */
  private getOutcomeIds(source?: IBetDetail[], sourceOnly: boolean = false): string[] {
    let outcomeIds = [];
    const receipts = source || this.receipts;

    _.each(receipts, (betReceipt: IBetDetail): void => {
      _.each(betReceipt.leg, (leg: IBetDetailLeg): void => {
        _.each(leg.part, (part: IBetDetailLegPart): void => {
          outcomeIds.push(part.outcome);
        });
      });
    });

    if (sourceOnly) {
      return _.uniq(outcomeIds);
    }
    const outComesFromBetSlip: string[] = this.getOutcomesInBetSlip();
    outcomeIds = _.uniq(_.difference(outcomeIds, outComesFromBetSlip));
    return _.union(outcomeIds, this.getSuspendedOutcomeIds());
  }

  private getNameOfEvent(leg: IBetDetailLeg): string {
    return _.reduce(leg.part, (names: string[], part: IBetDetailLegPart): string[] => {
      names.push(part.description);
      return names;
    }, []).join(', ');
  }

  private getEventDesc(leg: IBetDetailLeg): string {
    return _.uniq(_.reduce(leg.part, (names: string[], part: IBetDetailLegPart): string[] => {
      names.push(part.eventDesc);
      return names;
    }, [])).join(', ');
  }

  private getEventMarket(leg: IBetDetailLeg, lines: string): string {
    const complexBet = this.addLegSortName(leg, lines);

    if (complexBet) {
      return complexBet;
    }

    return _.uniq(_.reduce(leg.part, (names: string[], part: IBetDetailLegPart): string[] => {
      names.push(part.eventMarketDesc);
      return names;
    }, [])).join(', ');
  }

  private addLegSortName(leg: IBetDetailLeg, lines: string): string {
    return {
      SF: 'Forecast',
      RF: 'Reverse Forecast 2',
      CF: `Combination Forecast ${lines}`,
      TC: 'Tricast',
      CT: `Combination Tricast ${lines}`
    }[leg.legSort];
  }

  /**
   * Odds converter
   * @param part
   * @returns {string}
   */
  private getOdds(part): IBetOdds {
    let frac = '',
      dec = '';

    if (part) {
      const isLP = part.priceNum && part.priceNum.length > 0;

      if (isLP) {
        frac = `${part.priceNum}/${part.priceDen}`;
        dec = this.fracToDecService.getDecimal(part.priceNum, part.priceDen).toString();
      } else {
        frac = 'SP';
        dec = 'SP';
      }
    }

    return { frac, dec };
  }

  /**
   * Gets clean bet.
   * @param  {Array} betsReceipts - response from service
   * @return {Array}              - array with bet receipts.
   */
  private getCleanBet(betsReceipts: IBetDetail[]): IBetDetail[] {
    return betsReceipts.reduce((array: IBetDetail[], rec: IBetDetail): IBetDetail[] => {
      if (rec.leg.length === 1) {
        if(rec.leg[0].part) {
         const part = rec.leg[0].part[0];
         this.cleanPartEventData(rec.leg[0]);

         rec.name = this.getNameOfEvent(rec.leg[0]);
         rec.eventName = this.getEventDesc(rec.leg[0]);
         rec.eventMarket = this.getEventMarket(rec.leg[0], rec.numLines);
         rec.odds = this.getOdds(part);

         rec.startTime = part.startTime;
        }
      } else if (rec.leg.length) {
        _.each(rec.leg, (item: IBetDetailLeg) => {
          if(item.part) {
          this.cleanPartEventData(item);
          item.odds = this.getOdds(item.part[0]);
          }
        });
      }

      if (Number(rec.potentialPayout) === 0) {
        rec.potentialPayout = 'N/A';
      }

      array.push(rec);
      return array;
    }, []);
  }

  /**
   * Filter receipts on multiples and singles
   * @param  {String} method       - method which have to be used for filtering should be reject or filter
   * @param  {Array} betsReceipts  - array with bet receipts
   * @return {Array}               - singles or multiples bet receipts only
   */
  private filterReceipts(method: string, betsReceipts: IBetDetail[]): IBetDetail[] {
    return _[method](this.getCleanBet(betsReceipts), (receipt: IBetDetail): boolean => {
      return receipt.betType === 'SGL';
    });
  }

  /**
   * Best odds are guarantied when priceTypeCodes include GP (for Ladbrokes brand) or G (for Coral) and it is not a Greyhounds event
   * @param {IBetDetail[]} receiptBets
   */
  private markBogReceipts(receiptBets: IBetDetail[]): void {
    _.each(receiptBets, (betReceipt: IBetDetail): void => {
      _.each(betReceipt.leg, (leg: IBetDetailLeg): void => {
        _.each(leg.part, (part: IBetDetailLegPart): void => {
          part.isBog = (part && part.priceType && (part.priceType.includes('G') || part.priceType.includes('GP')))
            && !this.filtersService.isGreyhoundsEvent(part.eventCategoryId);
        });
      });
    });
  }

  private markForeCastTricastReceipts(receiptBets: IBetDetail[]): void {
    _.each(receiptBets, (receipt: IBetDetail) => {
      receipt.isFCTC = /^(SF|RF|CF|TC|CT)$/.test(receipt.leg[0].legSort);
    });
  }

  private updateVirtualEventNames(receiptBets: IBetDetail[]): void {
    _.each(receiptBets, (receipt: IBetDetail) => {
      _.each(receipt.leg, (leg: IBetDetailLeg) => {
        if (leg.part && leg.part[0].event.sportId === environment.CATEGORIES_DATA.virtuals[0].id) {
          const cleanEventName = this.filtersService.clearEventName(leg.part[0].eventDesc);
          leg.part[0].eventDesc = `${this.timeService.formatByPattern(new Date(leg.part[0].event.startTime), 'HH:mm')} ${cleanEventName}`;
        }
      });
    });
  }

  /**
   * Removes a particular character from a string
   * @returns string
   */
   private removeCharFromString(inputString: string, charToRemove: string): string {
    while (inputString.indexOf(charToRemove) > -1) {
      inputString = inputString.replace(charToRemove, '');
    }
    return inputString;
  }
  
  /**
   * Removes pipe(|) character from the data in the leg.part
   * @returns void
   */
  private cleanPartEventData(leg: IBetDetailLeg): void {
    leg.part.forEach(part => {
      part.description = this.removeCharFromString(part.description, '|');
      part.eventDesc = this.removeCharFromString(part.eventDesc, '|');
      part.eventMarketDesc = this.removeCharFromString(part.eventMarketDesc, '|')
    });
  }

  /**
   * Send data to GTM if tooltip appears Bet Receipt
   * @returns void
   */
  private sendGTMData(): void {
    const gtmData = {
      'eventAction': 'rendered',
      'eventCategory': 'maximum returns',
      'eventLabel': 'bet receipt'
    };
    this.gtmService.push('trackEvent', gtmData);
  }

  /**
   * check for Max Payout
   * @param receiptBets
   * @returns void
   */

  private checkMaxPayOut(receiptBets): void {
    receiptBets.forEach((bet: IBetDetail) => {
      if(bet.receipt !== null) {
        this.betReceipt = true;
       }
      if(bet.betTags && bet.betTags.betTag && bet.betTags.betTag[0].tagName === 'CAPPED'){
        this.maxPayOutFlag = true;
        this.sendGTMData();
      }
    });
  }

  /**
   * Calculate allwinners bonus value at betslip & bet receipt
   * @param betResponseData
   * @returns string, number
   */
  luckyAllWinnersBonus(betData:any, estReturn?: number): string {
    let luckytype: any;
    let estimateReturns: number;
    if(betData.bets){
      luckytype = this.isLuckyAvailable(betData);
      estimateReturns = estReturn;
    }else{
      luckytype = this.isLuckyAvailable(betData)
      estimateReturns = luckytype.response.potentialPayout;
    }
    const x:any = luckytype.type[0].multiplier && Number(luckytype.type[0].multiplier).toFixed(2);
    const allWinnerReturns = (estimateReturns && ((estimateReturns*x)-estimateReturns));
    return _.isNumber(allWinnerReturns) ? this.filtersService.setCurrency(allWinnerReturns, this.currencySymbol) : allWinnerReturns;
  }

  isLuckyAvailable(betData): any{
    const bets = (betData.bets) ? betData.bets : betData;
    let luckbonus;
    if(!bets.eventSource){
      luckbonus = bets.filter(element=>{
        return (this.betList.includes(element.betTypeRef.id) || this.betList.includes(element.betType)) && element.availableBonuses;
      });
    }else{
      luckbonus = bets.eventSource;
    }
    
    const luckyResponse = (luckbonus[0]) ? luckbonus[0] : luckbonus;
    const type = (luckyResponse.betType || luckyResponse.betTypeRef.id);
    if(luckyResponse.availableBonuses?.availableBonus){
      this.isLuckyBonusAvailable = true
    }
    const luckyObj = luckyResponse.availableBonuses.availableBonus.filter(list=>{
      if(type == LUCKY_TYPES.L15.TYPE){
        return (list.num_win === LUCKY_TYPES.L15.ALL_WIN);
      }else if(type == LUCKY_TYPES.L31.TYPE){
        return (list.num_win === LUCKY_TYPES.L31.ALL_WIN);
      }else{
        return (list.num_win === LUCKY_TYPES.L63.ALL_WIN);
      }
      //return (list.type === "LUCKYX_ALL_CORRECT");  
    })
    return {response: luckyResponse, type:luckyObj}
  }

  /**
   * Check luckysignpost type
   * @param luckyReceipt
   * @returns boolean
   */
  isLuckySignType(luckyReceipt): boolean {
    if(luckyReceipt && luckyReceipt[0]){
      const luckyMultiple = luckyReceipt.filter(selection => {
        return this.betList.includes(selection.betTypeRef.id) && selection.availableBonuses && this.isBonusApplicable(selection.availableBonuses);
      });
      return luckyMultiple.length !== 0;
    } else if(luckyReceipt && luckyReceipt.betTypeRef){
      return this.betList.includes(luckyReceipt.betTypeRef.id) && luckyReceipt.availableBonuses && this.isBonusApplicable(luckyReceipt.availableBonuses);
    }
  }
/**
   * Check isSP available for selection
   * @param betReceipt
   * @returns boolean
   */
  isSP(selection): boolean{
    let leg;
    if(selection[0]){
      leg = selection.filter((bet) => this.betList.includes(bet.betTypeRef.id) && bet.availableBonuses);
      leg = leg[0].leg;
    }else{
      leg = (selection && selection.leg) ? selection.leg : (selection && selection.legs) ? selection.legs : [];
    }
    return !!leg.some((item: any) => item.sportsLeg.price.priceTypeRef.id === 'SP');
  }

  returnAllWinner(bonusValue){
    bonusValue = (typeof(bonusValue) === 'string' ? bonusValue : bonusValue.toString());
    bonusValue = (bonusValue.replace('£', '')).replace(',', '');
    if(Number(bonusValue) > 0){
      return bonusValue;
    }else{
      return 0;
    }
  }

  isBonusApplicable(bonuses): boolean{
    return !bonuses.availableBonus.every(item => Number(item.multiplier) == 1)
  }
  
  isAllWinnerOnlyApplicable(luckydata): boolean{
    const type = (luckydata.betType || luckydata.betTypeRef.id);
    return luckydata.availableBonuses.availableBonus.filter(list=>{
      if(type == LUCKY_TYPES.L15.TYPE){
        return (list.num_win === LUCKY_TYPES.L15.ALL_WIN && Number(list.multiplier) !== 1);
      }else if(type == LUCKY_TYPES.L31.TYPE){
        return (list.num_win === LUCKY_TYPES.L31.ALL_WIN && Number(list.multiplier) !== 1);
      }else{
        return (list.num_win === LUCKY_TYPES.L63.ALL_WIN && Number(list.multiplier) !== 1);
      }
    }).length !== 0;
  }
}
