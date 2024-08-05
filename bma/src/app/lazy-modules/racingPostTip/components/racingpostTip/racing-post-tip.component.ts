import {
  Component,
  OnInit,
  Input,
  ChangeDetectionStrategy,
  ChangeDetectorRef, OnDestroy, Output, EventEmitter, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { TimeService } from '@core/services/time/time.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportEvent, IEventMostTipData } from '@core/models/sport-event.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { IOutcome } from '@core/models/outcome.model';
import { IPrice } from '@core/models/price.model';
import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';
import { AddToBetslipByOutcomeIdService } from '@betslip/services/addToBetslip/add-to-betslip-by-outcome-id.service';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IMarket } from '@core/models/market.model';
import { DeviceService } from '@coreModule/services/device/device.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { UserService } from '@app/core/services/user/user.service';
import { FracToDecService } from '@app/core/services/fracToDec/frac-to-dec.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { IRacingPostQuickbetReceipt } from '@app/betslip/services/betReceipt/bet-receipt.model';
import { IGtmOrigin } from '@app/core/services/gtmTracking/models/gtm-origin.model';
import { HandleLiveServeUpdatesService } from '@app/core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { IOutcomePrice } from '@app/core/models/outcome-price.model';
@Component({
  selector: 'racing-post-tip',
  templateUrl: 'racing-post-tip.component.html',
  styleUrls: ['./racing-post-tip.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RacingPostTipComponent implements OnInit, OnDestroy {
  @Input() mainBetReceipts: IBetDetail[] = [];
  @Input() quickBetReceipt: IQuickbetSelectionModel;
  @Input() racingPostTipTime: string;
  @Input() multiReceipts: IBetDetail[];
  @Input() racingPostData: ISportEvent[];
  @Input() racingPostToggle: IRacingPostQuickbetReceipt;
  @Input() isNextRacesData:boolean;
  @Output() readonly closeFn: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly racingPostGTM: EventEmitter<IGtmOrigin> = new EventEmitter();
  @ViewChild('priceOddsBtn') priceOddsBtn: ElementRef;

  priceOutCome: IOutcome;
  currentPrice: string;
  mostTippedRace: IEventMostTipData;
  mostTippedHorseEvents: IEventMostTipData[] = [];
  edpPageUrl: string;
  isGeneralSilk: boolean = false;
  isSilkLoaded: boolean = false;
  eventEntity: object = {};
  showRacePostTip: boolean = false;
  silkStyle: ISilkStyleModel;
  addBetSlip: Subscription;
  tipTimeout: number;
  silkImgLoad: number;
  toggleOddsColor: number;
  betData = [];
  isSuspended: ISportEvent[] = [];
  uniqueId: string;
  cssClass: string = '';
  filteredHorses;
  showTipBetReciept: boolean = false;
  liveServeChannels: any = [];
  historicPrices: any = [];
  private mostRecentTipsData: ISportEvent[];
  private dimensionData = {};
  private prices: IPrice[] = [];
  private eventCategory: string;
  private rPhorseName: string;
  private isBetPlacedOnHR: boolean = false;
  private readonly DECIMAL_VALUE = 'dec';
  private readonly FRAC_VALUE = 'frac';
  private readonly BET_PLACED_ON_HR = environment.HORSE_RACING_CATEGORY_ID;
  private racingPostEnv = environment;
  private readonly hideOddsColorTime: number = 2000;
  constructor(
    private timeService: TimeService,
    private routingHelperService: RoutingHelperService,
    private commandService: CommandService,
    private deviceService: DeviceService,
    private raceOutcomeDetails: RaceOutcomeDetailsService,
    private addToBetslipByOutcomeIdService: AddToBetslipByOutcomeIdService,
    private racingPostTipService: RacingPostTipService,
    private changeDetectorRef: ChangeDetectorRef,
    private locale: LocaleService,
    private router: Router,
    private windowRef: WindowRefService,
    private betSlipService: BetslipService,
    private pubsubService: PubSubService,
    private userService: UserService,
    private fracToDecService: FracToDecService,
    private gtmService: GtmService,
    private liveServeHandleUpdatesService: HandleLiveServeUpdatesService
  ) { }

  ngOnInit(): void {
    this.betData = this.betSlipService.betData;
    !this.isNextRacesData && this.getRacingPostData();
    this.pubsubService.subscribe('priceOddsFormatChange', this.pubsubService.API.SET_ODDS_FORMAT, () => {
      this.currentPrice = this.getPrice(this.prices);
      this.changeDetectorRef.detectChanges();
    });
    this.pubsubService.subscribe('RPTipPresent', this.pubsubService.API.IS_TIP_PRESENT, (nextRaces) => {
      this.showTipBetReciept = nextRaces.isTipPresent;
      this.changeDetectorRef.detectChanges();
    });
    this.dimensionData = this.commandService.executeAsync(this.commandService.API.GET_LIVE_STREAM_STATUS, undefined, false)
      .then(streamData => {
        this.dimensionData = {
          dimension86: 0,
          dimension87: streamData && streamData.streamActive ? 1 : 0,
          dimension88: streamData && streamData.streamID || null,
          quantity: 1
        };
      });
  }

  ngOnDestroy(): void {
    this.addBetSlip && this.addBetSlip.unsubscribe();
    this.windowRef.nativeWindow.clearTimeout(this.tipTimeout);
    this.windowRef.nativeWindow.clearTimeout(this.toggleOddsColor)
    this.betSlipService.betData = [];
    this.betData = [];
    this.pubsubService.unsubscribe('RPTipPresent');
    this.pubsubService.unsubscribe('priceOddsFormatChange');
    this.pubsubService.unsubscribe('racingpriceOddsUpdate');
    this.liveServeHandleUpdatesService.unsubscribe(this.liveServeChannels);
  }

  redirectEdpUrl(): void {
    this.closeFn.emit(true);
    this.router.navigateByUrl(this.edpPageUrl);
    this.pubsubService.publish(this.pubsubService.API.QUICKBET_PANEL_CLOSE);
    this.gaTrack();
  }

  /**
   * after click price button redirect to betslip
   */
  addToBetSlip(): void {
    this.commandService.executeAsync(this.commandService.API.BETSLIP_READY)
      .then(() => this.add());
  }

  /**
   * Google tag manager(gtm)
   * @returns {object} eventEntity
   */
  private gaTrack(): void {
    this.gtmService.push('trackEvent', {
      eventAction: 'navigation',
      eventCategory: 'bet receipt',
      eventLabel: 'view full racecard'
    });
  }

  private tipShownGaTrack(event: IEventMostTipData): void {
    const GTMEvent = {
      'ecommerce': {
        'detail': {
          'actionField': { 'list': 'Bet Receipt - RP Tip' },
          'products': [{
            'name': event.name, // OpenBet Game
            'brand': event.markets[0].name, // Event_Market_Name
            'category': event.categoryId, // OpenBet Category_ID
            'variant': event.typeId, // OpenBet Type_ID
            'dimension60': event.id, // OpenBet Product_ID
            'dimension61': this.priceOutCome.id, // OpenBet Selection_ID
            'dimension62': event.eventIsLive ? 1 : 0, // Pre-Event = 0, In-Play = 1
            'dimension63': this.isByB(event) ? 1 : 0,// Customer Built No: 0, Yes: 1
            'dimension64': 'Bet Receipt', // Location
            'dimension65': 'RP Tip', // Module
          }]
        }
      },
      eventAction: 'rendered',
      eventCategory: 'bet receipt',
      eventLabel: 'racing post tip'
    };
    this.gtmService.push('trackEvent', GTMEvent);
  }

  private isByB(event): boolean {
    return event && this.racingPostEnv.BYB_CONFIG
      && String(this.racingPostEnv.BYB_CONFIG.HR_YC_EVENT_TYPE_ID) === String(event.typeId);
  }

  /**
   * To redirect to betslip
   */
  private add(): void {
    this.addBetSlip && this.addBetSlip.unsubscribe();
    const racingPostGA: IGtmOrigin = {
      location: 'Bet Receipt',
      module: 'RP Tip',
      ...this.dimensionData
    };
    this.addBetSlip = this.addToBetslipByOutcomeIdService.addToBetSlip(
      this.priceOutCome.id, true, true, false, false, false, true, racingPostGA
    ).subscribe(() => {
      this.pubsubService.publish(this.pubsubService.API.QUICKBET_PANEL_CLOSE);
    });
    this.racingPostGTM.emit(racingPostGA);
  }

  /**
   * getting odd price
   * @param - prices array
   * @return - string
   */
  private getPrice(prices: IPrice[]): string {
    let priceValue = this.locale.getString('racingposttip.startingPrice');
    if (this.userService.oddsFormat === this.DECIMAL_VALUE && prices && prices.length) {
      priceValue = this.fracToDecService.getDecimal(prices[0].priceNum, prices[0].priceDen).toString();
    } else if (this.userService.oddsFormat === this.FRAC_VALUE && prices && prices.length) {
      priceValue = this.fracToDecService.getFracTional(prices[0].priceNum, prices[0].priceDen);
    }
    return priceValue;
  }

  /**
   * Get all tip most tip race events & horses through upcell
   */
  private getRacingPostData(): void {
    this.checkForBetsData(this.betData);
    if (this.racingPostData.length &&
      ((this.multiReceipts && !this.multiReceipts.length && this.mainBetReceipts.length === 1) ||
        Object.keys(this.quickBetReceipt).length) && this.isBetPlacedOnHR) {
      this.mostRecentTipsData = this.racingPostData;
      this.mostTippedHorseEvents = this.mainBetReceipts && this.mainBetReceipts.length
        ? this.showMainbet()
        : this.showQuickbet();
      this.checkForSuspendedRaces(this.racingPostData);
      if (this.mostTippedHorseEvents && this.mostTippedHorseEvents.length) {
        this.mostTippedRace = this.isSuspended[0];
        this.getTopTipFromTips();
        this.getSilkAndEdpUrl(this.mostTippedRace);
        this.tipShownGaTrack(this.mostTippedRace);
        this.checkForTipExpired(this.mostTippedRace.time);
        const indexToSplit = this.mostTippedRace.name.indexOf(' ');
        this.mostTippedRace.time = this.mostTippedRace.name.slice(0, indexToSplit);
        this.mostTippedRace.name = this.mostTippedRace.name.slice(indexToSplit + 1);
      }
      this.changeDetectorRef.markForCheck();
    }
  }
  private checkForSilkLoaded() {
      if (this.priceOutCome && this.priceOutCome.racingFormOutcome
        && this.priceOutCome.racingFormOutcome.silkName) {
        this.isSilkLoaded = true;
        this.changeDetectorRef.detectChanges();
      }
  }

  private showReceipt(): void {
    if (this.togglePresent()) {
      this.showTipBetReciept = true;
    }
  }

  private togglePresent(): boolean {
    const togglePresent = this.racingPostToggle && this.racingPostToggle.enabled;
    return (togglePresent && this.racingPostToggle.quickBetReceipt) ||
      (togglePresent && this.racingPostToggle.mainBetReceipt);
  }

  private showMainbet(): IEventMostTipData[] {
    this.showReceipt();
    return this.racingPostTipService.getMostTipThroughMainBet(this.mostRecentTipsData, this.mainBetReceipts,
      this.racingPostToggle.enabled, this.racingPostToggle.mainBetReceipt);
  }
  private showQuickbet(): IEventMostTipData[] {
    this.showReceipt();
    return this.racingPostTipService.getMostTipThroughQuickBet(this.mostRecentTipsData, this.quickBetReceipt,
      this.racingPostToggle.enabled, this.racingPostToggle.quickBetReceipt);
  }

  private checkForTipExpired(time: string): void {
    const raceStartTime = new Date(time.split('.')[0]).getTime();
    let betPlaceTime: number;
    if (this.racingPostTipTime) {
      betPlaceTime = new Date(this.racingPostTipTime.split('.')[0]).getTime();
    } else {
      const betSlipTime = new Date().toJSON({ timeZone: 'Europe/London' });
      betPlaceTime = new Date(betSlipTime.split('.')[0]).getTime();
    }
    this.tipTimeout = this.windowRef.nativeWindow.setTimeout(() => {
      this.showRacePostTip = false;
      this.changeDetectorRef.detectChanges();
      this.liveServeHandleUpdatesService.unsubscribe(this.liveServeChannels);
    }, ((raceStartTime - betPlaceTime) - 20000));
  }

  private getTopTipFromTips(): void {
    this.eventCategory = this.deviceService.isMobile ? 'Mobile' : 'Desktop';
    this.mostTippedRace.startTime =
      this.timeService.formatByPattern(new Date(this.mostTippedRace.startTime), 'HH:mm');
    this.rPhorseName = this.mostTippedRace.powerHorse.horseName;
    if(this.mostTippedRace.markets.length) {
      let powerHorse = [];
      powerHorse = this.mostTippedRace.markets[0].children.filter(otc =>
        otc.outcome.name.includes(this.rPhorseName)
      );
      if(powerHorse.length) {
        this.priceOutCome = powerHorse.pop().outcome;
        this.prices = this.priceOutCome.prices;
        if (this.priceOutCome.prices && this.priceOutCome.prices.length) {
          this.historicPrices.push(this.priceOutCome.prices[0]);
        }
        this.currentPrice = this.getPrice(this.prices);
        this.priceOutCome.racingFormOutcome = {
          silkName: this.mostTippedRace.powerHorse.silk,
          isBeatenFavourite: this.mostTippedRace.powerHorse.isBeatenFavourite
        };
        this.checkForSilkLoaded();
        const horseSilkImg = this.mostTippedRace.markets[0].outcomes.findIndex((outcome) =>
          outcome.id === this.priceOutCome.id
        );
    
        this.mostTippedRace.markets[0].outcomes.splice(horseSilkImg, 1, this.priceOutCome);
        this.liveServeUpdateSubscription(horseSilkImg);
        this.changeDetectorRef.detectChanges();
      }
    }
  }
  private liveServeUpdateSubscription(outComeIndex: number) {
    this.formLiveChannels(outComeIndex);
    this.liveServeHandleUpdatesService.subscribe(this.liveServeChannels, (update) => {
      if (update && update.payload) {
        const channelType: string = update.type;
        if (channelType === 'sSELCN') {
          if (update.payload.lp_num || update.payload.lp_den) {
            const delta = {
              priceDec: Number(this.fracToDecService.getDecimal(Number(update.payload.lp_num), Number(update.payload.lp_den), 6)),
              priceDen: Number(update.payload.lp_den),
              priceNum: Number(update.payload.lp_num),
              isDisplayed: true,
              priceType: 'LP'
            };
            const market = { prices: [delta] };
            this.checkForPriceUpdate(market);
          }
        } else if (channelType === 'sEVENT') {
          const statusObj = {
            isStarted: update.payload.started == 'Y',
            eventStatusCode: update.payload.status
          };
          if (statusObj.eventStatusCode == 'S' || statusObj.isStarted) {
            this.showRacePostTip = false;
            this.changeDetectorRef.detectChanges();
            this.liveServeHandleUpdatesService.unsubscribe(this.liveServeChannels);
          }
        }
      }
    });
  }
  private formLiveChannels(outComeIndex: number) {
    this.liveServeChannels.push(this.mostTippedRace.liveServChannels.split(',')[0]);
    this.liveServeChannels.push(this.mostTippedRace.markets[0].liveServChannels.split(',')[0]);
    this.liveServeChannels.push(this.mostTippedRace.markets[0].outcomes[outComeIndex].liveServChannels.split(',')[0]);
  }
  private getSilkAndEdpUrl(event: ISportEvent): void {
    this.edpPageUrl = this.genEventDetailsUrl(event);
    this.isGeneralSilk = this.isGenericSilk(event, this.priceOutCome);
    this.silkStyle = this.getSilkStyle(event.markets[0], this.priceOutCome);
    this.isHorseExists(this.racingPostData);
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Generate URL for event race card page or event page
   * @returns {object} eventEntity
   */
  private genEventDetailsUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }

  /**
   * get silk image
   * @params eventEntity
   * @params outcomeEntity
   */
  private isGenericSilk(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
    return this.raceOutcomeDetails.isGenericSilk(eventEntity, outcomeEntity);
  }

  /**
   * get silk style
   * @params eventEntity
   * @params outcomeEntity
   */
  private getSilkStyle(raceData: IMarket, outcomeEntity: IOutcome): ISilkStyleModel {
    return this.raceOutcomeDetails.getSilkStyle(raceData, outcomeEntity);
  }

  /**
   * To Check if horse exists or not
   * @param {ISportEvent[]} racingPostData
   */
  private isHorseExists(racingPostData: ISportEvent[]): void {
    if (racingPostData && racingPostData.some(horseData => {
      return horseData.horses && horseData.horses.length > 0;
    })) {
      this.showRacePostTip = true;
    }
  }

  /**
   * To Check bet placed on HR or not
   * @param {} betsData
   */
  private checkForBetsData(betPlacedOnHR): void {
    if (betPlacedOnHR.length) {
      betPlacedOnHR.forEach(betsData => {
          this.checkForBetType(betsData);
      });
    } else {
      this.isBetPlacedOnHR = true;
    }
  }

  /**
   * To Check bet placed on HR or not
   * @param {} betsData
   */
  private checkForSuspendedRaces(suspendedRaces): void {
    if (suspendedRaces && suspendedRaces.length) {
      suspendedRaces.forEach(element => {
        if (element.eventStatusCode === 'A' && element.markets[0].marketStatusCode === 'A' &&
          element.powerHorses && element.powerHorses.length) {
          [this.filteredHorses] = element.markets[0].outcomes.filter(outcome =>
            outcome.name.includes(element.powerHorse.horseName)
          );
          if (this.filteredHorses && this.filteredHorses.outcomeStatusCode === 'A'
            && this.filteredHorses.isActive === true) {
            this.isSuspended.push(element);
          }
        }
      });
    } else {
      this.showRacePostTip = false;
    }
  }

  /**
   * To Check bet placed on HR tricast and forecast
   * @param {} betsData
   */
  private checkForBetType(betData): void {
    if (betData.combiType === 'TRICAST') {
      this.isBetPlacedOnHR = false;
    } else if (betData.combiType === 'FORECAST') {
      this.isBetPlacedOnHR = false;
    } else {
      this.isBetPlacedOnHR = true;
    }
  }

  /**
   * Return active button class and classes of up/down price changes.
   * @private
   * @return {Array}
   */
  private get oddsClasses(): string {
    const classes = ['btn-bet'];
    if (this.cssClass) {
      classes.push(this.cssClass);
    }
    return classes.toString().replace(/,/g, ' ');
  }

  private checkForPriceUpdate(market) {
    if (this.historicPrices.length == 2) {
      this.historicPrices.shift();
    }

    this.historicPrices.push(market.prices[0]);
    this.currentPrice = this.getPrice(market.prices);
    this.getCssClass(this.historicPrices[0], this.historicPrices[1]);
    this.priceOddsBtn.nativeElement.setAttribute('class', this.oddsClasses);
    this.changeDetectorRef.detectChanges();
    this.toggleOddsColor = this.windowRef.nativeWindow.setTimeout(() => {
      this.priceOddsBtn.nativeElement.classList.remove(this.cssClass);
    }, this.hideOddsColorTime);
  }

  private getCssClass(currentPrices: IOutcomePrice, updatedPrices: IOutcomePrice) {
    if (!currentPrices || !updatedPrices) {
      return '';
    }
    
    if ((currentPrices.priceNum / currentPrices.priceDen) < (updatedPrices.priceNum / updatedPrices.priceDen)) {
      this.cssClass = 'bet-up';
    } else if ((currentPrices.priceNum / currentPrices.priceDen) > (updatedPrices.priceNum / updatedPrices.priceDen)) {
      this.cssClass = 'bet-down';
    }else{
      this.cssClass = '';
    }
  }
}
