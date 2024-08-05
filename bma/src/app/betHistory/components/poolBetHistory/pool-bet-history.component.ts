import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { UserService } from '@core/services/user/user.service';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { TimeService } from '@core/services/time/time.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import {
  CashOutLiveUpdatesSubscribeService
} from '@app/betHistory/services/cashOutLiveUpdatesSubscribeService/cashOutLiveUpdatesSubscribeService';
import { betHistoryConstants } from '@app/betHistory/constants/bet-history.constant';
import { IBetHistoryBet, IBetHistoryPoolBet, IBetHistoryLeg, ICelebration } from '@app/betHistory/models/bet-history.model';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';

import TotePotPoolBet from '../../betModels/totePotPoolBetClass/TotePotPoolBetClass';
import TotePoolBet from '../../betModels/totePoolBet/tote-pool-bet.class';
import FootballJackpotBet from '../../betModels/footballJackpotBet/football-jackpot-bet.class';
import { CurrencyPipe } from '@angular/common';
import { ToteBetsExtendingService } from '@app/betHistory/services/toteBetsExtending/tote-bets-extending.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISvgItem } from '@app/core/services/cms/models';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { DeviceService } from '@coreModule/services/device/device.service';

@Component({
  selector: 'pool-bet-history',
  templateUrl: './pool-bet-history.component.html',
  styleUrls: ['./pool-bet-history.component.scss']
})
export class PoolBetHistoryComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnChanges, OnDestroy {
  @Input() poolBets: IBetHistoryPoolBet[];
  @Input() isBetHistoryTab: boolean;
  @Input() isMyBetsInCasino: boolean;
  @Input() isSportIconEnabled: boolean;

  noBetsMessage: string;
  betModelsMap: { [key: string]: IBetHistoryPoolBet};
  poolHistory: IBetHistoryPoolBet[] = [];
  ctrlName: string = 'PoolBetHistoryComponent';
  sportIconSvgId: string = '';
  isBrandLadbrokes: boolean;
  celebration: ICelebration = {
    congratsBannerImage: '',
    displayCelebrationBanner: false,
    celebrationMessage: '',
    winningMessage: '',
    cashoutMessage: '',
    duration: 0
  };

  readonly env = environment;
  readonly LADBROKES: string = bma.brands.ladbrokes;
  private readonly cashoutStatus: string = betHistoryConstants.celebratingSuccess.cashoutStatus;

  constructor(
    private localeService: LocaleService,
    private userService: UserService,
    private betHistoryMainService: BetHistoryMainService,
    private timeService: TimeService,
    private cashoutMapIndexService: CashoutMapIndexService,
    private cashOutLiveUpdatesSubscribeService: CashOutLiveUpdatesSubscribeService,
    private sbFiltersService: SbFiltersService,
    private currencyPipe: CurrencyPipe,
    private toteBetsExtendingService: ToteBetsExtendingService,
    private pubsub: PubSubService,
    private cmsService: CmsService,
    protected deviceService: DeviceService,
  ) {
    super();
    this.betModelsMap = this.generateBetModelsMap();
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.RELOAD_COMPONENTS, () => {
        this.initializeBets();
      }
    );
  }

  ngOnInit(): void {
    if(this.isBetHistoryTab) {
      this.celebration = this.betHistoryMainService.getCelebrationBanner();
    }
    this.noBetsMessage = this.isBetHistoryTab
      ? this.localeService.getString('bethistory.noHistoryInfo')
      : this.localeService.getString('bethistory.noOpenBets');
    this.pubsub.publish('UPDATE_SETTLED_BETS_HEIGHT', this.poolBets.length);
    this.isBrandLadbrokes = this.env.brand === this.localeService.getString(this.LADBROKES).toLowerCase();
    this.deviceService.getDeviceViewType();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!changes.poolBets) { return; }
    this.initializeBets();
  }

  /**
   * Track by function
   * @param {number} index
   * @param {class} item
   * @returns {string}
   */
  trackByBet(index: number, item: IBetHistoryBet): string {
    return `${index}${item.id}${item.receipt}${item.isSuspended}`;
  }

  ngOnDestroy(): void {
    this.unsubcribeFromLiveUpdates();
    this.pubsub.unsubscribe(this.ctrlName);
  }

  /**
   * Generates bets objects and updates subscriptions to live updates
   */
  private initializeBets(): void {
    this.generatePoolHistory();
    this.unsubcribeFromLiveUpdates();
    this.subscirbeForLiveUpdates();
  }

  /**
   * Generate map: pool Type to pool Model
   * @returns Object - bet models map
   * @private
   */
  private generateBetModelsMap(): { [key: string]: IBetHistoryPoolBet} {
    const betModelsMap = {},
      TOTE_MULTIPLE_LEGS_BET_TYPES: string[] = betHistoryConstants.TOTE_MULTIPLE_LEGS_BET_TYPES,
      allToteBetTypes: string[] = betHistoryConstants.TOTE_ONE_LEG_BET_TYPES.concat(TOTE_MULTIPLE_LEGS_BET_TYPES);
    betModelsMap[betHistoryConstants.BET_TYPES.FOOTBALL_JACKPOT] = FootballJackpotBet;

    _.reduce(allToteBetTypes, (memo: IBetHistoryPoolBet, betType: string, index: number) => {
      memo[betType] = index < betHistoryConstants.TOTE_ONE_LEG_BET_TYPES.length
        ? TotePoolBet
        : TotePotPoolBet;
      return memo;
    }, betModelsMap);
    return betModelsMap;
  }

  /**
   * Generate Pool History
   * @private
   */
  private generatePoolHistory(): void {
    const tempData: IBetHistoryPoolBet[] = [];
    this.poolBets.forEach((item: IBetHistoryPoolBet) => {
      const PoolItemBetModel = this.betModelsMap[item.poolType];
      if (PoolItemBetModel) {
        const bet = new PoolItemBetModel(
          item,
          this.betHistoryMainService,
          this.userService,
          this.localeService,
          this.timeService,
          this.cashoutMapIndexService,
          this.currencyPipe,
          this.sbFiltersService
        );
        tempData.push(bet);
      }
    });
    this.poolHistory = tempData;
    this.setSportIcon();
  }

  /**
   * Subscribe for live updates
   * @private
   */
  private subscirbeForLiveUpdates(): void {
    const betsMap: { [key: string]: (TotePotPoolBet | TotePoolBet)}
      = (this.betHistoryMainService.generateBetsMap(this.poolHistory) as { [key: string]: (TotePotPoolBet | TotePoolBet)});

    this.toteBetsExtendingService.extendToteBetsWithEvents(betsMap)
      .subscribe(() => {
        this.cashOutLiveUpdatesSubscribeService.addWatch(betsMap);
      }, () => { }); // added error handling for BMA-41334
  }

  /**
   * Unsubscribe from live updates
   * @private
   */
  private unsubcribeFromLiveUpdates(): void {
    this.cashOutLiveUpdatesSubscribeService.unsubscribeFromLiveUpdates();
  }
  
  /**
   * Sets Sport icon svg id to leg
   */
  setSportIcon(): void {
    this.poolHistory.forEach((poolEntity: IBetHistoryPoolBet) => {
      poolEntity?.leg?.forEach((leg: IBetHistoryLeg) => {
        const categoryId = leg?.part[0]?.outcome?.eventCategory?.id;
        if(categoryId) {
          this.cmsService.getItemSvg('', Number(categoryId))
            .subscribe((icon: ISvgItem) => {
              leg.svgId = icon.svgId ? icon.svgId : "icon-generic";
            });
        }
      })
    });
  }
  /**
   * Tells whether to show congrats banner or not
   * @param bet 
   */
  isCongratsBannerShown(bet: TotePotPoolBet | TotePoolBet): boolean {
    const currentDate = new Date(),
      compareDateValue = new Date(this.timeService.getLocalDateFromString(bet.bet.settledAt)),
      timeDiff = Math.abs(currentDate.getTime() - compareDateValue.getTime());
    const hrs = timeDiff/(1000 * 3600);
    return this.celebration?.displayCelebrationBanner && hrs<=this.celebration.duration && Number(bet.stake)<Number(bet.bet.winnings.value);
  }
  /**
   * Returns the winning message with the totalreturns on the bet
   * @param bet 
   */
  getReturnValue(bet: TotePotPoolBet | TotePoolBet): string {
    return this.celebration?.winningMessage.replace("{amount}", this.currencyPipe.transform(bet.bet.winnings.value, bet.currency, 'code'));
  }
  /**
   * Returns the cashout message with the cashedout amount
   * @param bet
   */
  getCashoutReturnValue(bet: TotePotPoolBet | TotePoolBet): string {
    return this.celebration?.cashoutMessage.replace("{amount}", this.currencyPipe.transform(bet.bet.winnings.value, bet.currency, 'code'));
  }

  showFreeBetsToggle(value: string) {
    return Number(value) > 0;
  }

  getClassName(isDesktop, isSettledBet): string {
    if(!isDesktop || (isDesktop && !isSettledBet)) {
      return 'single-left single-left-inline';
    } else if(isDesktop) {
      return 'single-left';
    } 
  }
}
