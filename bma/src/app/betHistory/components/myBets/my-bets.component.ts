import { Component, HostListener, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { of, Subscription } from 'rxjs';
import { concatMap, distinct } from 'rxjs/operators';
import * as _ from 'underscore';

import { cashoutConstants } from '../../constants/cashout.constant';
import { LocaleService } from '@core/services/locale/locale.service';
import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IBetHistoryBet, IMatchCmtryData } from '@app/betHistory/models/bet-history.model';
import { ICashOutData, IPayoutUpdate, PayoutResponse } from '@app/betHistory/models/cashout-section.model';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { PlacedBet } from '@app/betHistory/betModels/placedBet/placed-bet.class';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetTrackingService } from '@lazy-modules/bybHistory/services/betTracking/bet-tracking.service';
import {
  HandleScoreboardsStatsUpdatesService
} from '@lazy-modules/bybHistory/services/handleScoreboardsStatsUpdates/handle-scoreboards-stats-updates.service';
import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IBetHistoryLeg } from '@app/betHistory/models/bet-history.model';
import { betLegConstants, MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { CASHOUT_SUSPENDED } from '@app/betHistory/components/cashOutMessaging/cash-out-message.constants';
import { DeviceService } from '@core/services/device/device.service';
@Component({
  selector: 'my-bets',
  templateUrl: '../cashOutBets/cash-out-bets.component.html',
  styleUrls: ['my-bets.component.scss']
})
export class MyBetsComponent implements OnInit, OnDestroy, OnChanges {

  @Input() cashoutIds: { id: number }[];
  @Input() placedBets: IBetHistoryBet[];
  @Input() cashoutBets: IBetDetail[];
  @Input() eventId: string;
  @Input() isUsedFromWidget: boolean;
  @Input() section: string;
  @Input() raceCardEventIds: number[] = []; // build race card
  // We have declared isUsedFromWidget in order to solve the strict mode issue.

  readonly helpSupportUrl: string = environment.HELP_SUPPORT_URL;
  noBetsMessage: string;
  ctrlName: string = cashoutConstants.controllers.MY_BETS_CTRL;
  betLocation: string = cashoutConstants.betLocation.MY_BETS;
  loadComplete: boolean = true;
  betsMap: { [key: string]: PlacedBet | CashoutBet };
  bets: ICashOutData[];
  isCashOutBets: boolean = false;
  openWhatIsCashOut?: Function;
  optaDisclaimer: string;
  betTrackingEnabled: boolean;
  contactUsMsg: string;
  isMyBetsInCasino: boolean = false;
  isSportIconEnabled: boolean;
  displayProfitIndicator: boolean;
  dataDisclaimer = { enabled: false, dataDisclaimer: '' };
  isMobile: boolean;
  private betReceipts = new Set();

  private betTrackingEnabledSubscription: Subscription;
  private getEventIdStatisticsSubscription: Subscription;
  private channels: string[];
  showDHMessage: boolean = true;

  constructor(
    public emaService: EditMyAccaService,
    private locale: LocaleService,
    private cashOutSectionService: CashoutSectionService,
    private pubsub: PubSubService,
    private betTrackingService: BetTrackingService,
    private handleScoreboardsStatsUpdatesService: HandleScoreboardsStatsUpdatesService,
    private cmsService: CmsService,
    private device: DeviceService
  ) {
    this.noBetsMessage = this.locale.getString('bethistory.noCashoutBets');
  }

  ngOnInit(): void {
    this.init();
    this.getEventIdStatisticsSubscription = this.handleScoreboardsStatsUpdatesService.getStatisticsEventIds().pipe(
      distinct()
    ).subscribe((eventId: string) => {
      this.bets.forEach((bet: ICashOutData) => {
        if (bet.eventSource.event.includes(eventId)) {
          bet.optaDisclaimerAvailable = true;
        }
      });
    });
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config && config.CelebratingSuccess) {
        this.displayProfitIndicator = config.CelebratingSuccess.displayCashoutProfitIndicator;
      }
      this.dataDisclaimer = config.ScoreboardsDataDisclaimer ? config.ScoreboardsDataDisclaimer :
        { enabled: false };
      this.isSportIconEnabled = config.CelebratingSuccess?.displaySportIcon?.includes('edpmybets');
    });
    this.contactUsMsg = this.locale.getString('bethistory.openBetsOverLimitPeriodMessage', [this.helpSupportUrl]);
    this.matchCommentaryUpdate();
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.BET_LEGS_LOADED, (betLocation: string) => {
      this.channels = betLocation === betLegConstants.mybets && this.cashOutSectionService.sendRequestForLastMatchFact(this.bets);
    });
    //Get updates for bet selection status.
    this.pubsub.subscribe('MyBetsComponent','LUCKY_BONUS', (bet: any) => {
      this.betReceipts.add(bet);
    });
    this.isMobile = this.device.isMobile;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.betsMap) {
      this.removeListeners();
      this.updateBets();
    }
  }
  @HostListener('window:beforeunload', ['$event'])
  ngOnDestroy(): void {
    this.removeListeners();
    this.betTrackingEnabledSubscription && this.betTrackingEnabledSubscription.unsubscribe();
    this.getEventIdStatisticsSubscription && this.getEventIdStatisticsSubscription.unsubscribe();
    this.channels?.length && this.cashOutSectionService.removeHandlers(this.channels);
  }

  trackByBet(index: number, bet: { eventSource: PlacedBet | CashoutBet, location: string }): string {
    return `${index}${bet.eventSource.betId}${bet.eventSource.receipt}`;
  }

  isCashoutError(bet: ICashOutData) {
    return this.cashOutSectionService.isCashoutError(bet.eventSource);
  }

  getCashoutError(bet: ICashOutData) {
    return this.cashOutSectionService.getCashoutError(bet.eventSource);
  }

  /**
   * data disclaimer shown/hide based below conditions
   * @param bet 
   * @returns 
   */
  isShownDisclaimer(bet: ICashOutData): boolean {
    return this.dataDisclaimer.enabled &&
      bet.eventSource.leg.filter((item: IBetHistoryLeg) => item.hasOwnProperty('eventEntity') &&
        item.eventEntity.eventIsLive && item.eventEntity.comments).length > 0;
  }

  private updateBets(): void {
    this.bets = this.cashOutSectionService.generateBetsArray(this.betsMap, this.betLocation).filter((bet: ICashOutData) => {
      if (this.raceCardEventIds.length) {
        return bet.eventSource.event.some((eventId: string) => this.raceCardEventIds.includes(+eventId));
      } else {
        return bet.eventSource.event.indexOf(this.eventId) > -1;
      }
    });
    this.cashOutSectionService.emitMyBetsCounterEvent(this.bets);
    this.registerEventListeners();
  }

  private init(): void {
    this.cashOutSectionService.registerController(this.ctrlName);
    const myBetsInstances = this.cashOutSectionService.createTempDataForMyBets(this.cashoutIds, this.placedBets);
    this.betsMap = this.cashOutSectionService.generateBetsMap(myBetsInstances, this.betLocation);
    const isByb = Object.values(this.betsMap).some((bet) => bet.bybType !== undefined);
    if (isByb) {
      this.betTrackingEnabledSubscription = this.betTrackingService.isTrackingEnabled().pipe(
        concatMap((res: boolean) => {
          this.betTrackingEnabled = res;
          return this.betTrackingEnabled ? this.betTrackingService.getStaticContent() : of(null);
        })
      ).subscribe((content) => {
        this.optaDisclaimer = content;
      });
    }

    this.updateBets();
  }

  private removeListeners(): void {
    this.cashOutSectionService.removeListeners(this.ctrlName);
    this.pubsub.unsubscribe(this.ctrlName);
  }

  private registerEventListeners(): void {
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.LIVE_BET_UPDATE, options => {
      this.cashOutSectionService.removeErrorMessageWithTimeout(this.bets, options);
    });


    this.pubsub.subscribe(this.ctrlName, [this.pubsub.API.CASH_OUT_MAP_UPDATED, this.pubsub.API.MY_BETS_UPDATED], () => {
      const myBetsInstances = this.cashOutSectionService.createTempDataForMyBets(this.cashoutIds, this.placedBets);
      this.betsMap = this.cashOutSectionService.generateBetsMap(myBetsInstances, this.betLocation);
      this.removeListeners();
      this.updateBets();
      this.init();
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.UPDATE_CASHOUT_BET, bet => {
      this.cashOutSectionService.updateBet(bet, this.bets);
      this.updateCashoutBetValue(bet);

      const placedBet = _.findWhere(this.placedBets, { betId: bet.betId });
      if (placedBet) {
        placedBet.isCashOutedBetSuccess = bet.isCashOutedBetSuccess;
        if (bet.isEWCashoutSuspend && bet.cashoutValue === CASHOUT_SUSPENDED) { // update these only when suspended and triggered from cashout-panel
          placedBet.cashoutValue = bet.cashoutValue;
          placedBet.isPartialCashOutAvailable = bet.isPartialCashOutAvailable;
          placedBet.isCashOutUnavailable = bet.isCashOutUnavailable;
        }
      }
    });

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.PAYOUT_UPDATE, (response: IPayoutUpdate) => {
      response.updatedReturns.forEach((update: PayoutResponse) => {
        const findBet = this.bets.find((bet: ICashOutData) => { return bet.eventSource?.betId === update.betNo });
        if (findBet && findBet.eventSource) {
          findBet.eventSource['potentialPayout'] = update.returns;
        }
      });
      this.bets = [...this.bets];
    });
  }

  private updateCashoutBetValue(newBet: IBetDetail): void {
    const bet = _.findWhere(this.cashoutBets, { betId: newBet.betId });
    if (bet) {
      bet.cashoutValue = newBet.cashoutValue;
    }
  }
  /**
  * Updates bet-leg with Match-commentary data when ever available by calling matchCmtryCommentaryDataUpdate
  */
  private matchCommentaryUpdate(): void {
    this.resetMatchCmtryData(this.bets);
    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.UPDATE_MATCHCOMMENTARY_DATA, (matchCmtryDataUpdate: IMatchCmtryData) => {
      matchCmtryDataUpdate && this.cashOutSectionService.matchCommentaryDataUpdate(this.bets, matchCmtryDataUpdate, MYBETS_AREAS.EDP);
    });
  }
  /**
   * sets the myBetsAreas[section].isMatchCmtryDataAvailable to false
   * @param bets 
   */
  private resetMatchCmtryData(bets: ICashOutData[]): void {
    bets.forEach((bet: ICashOutData) => {
      bet?.eventSource && bet.eventSource.leg.forEach((legitem: IBetHistoryLeg) => {
        if (legitem?.myBetsAreas && legitem.myBetsAreas[MYBETS_AREAS.EDP]) {
          legitem.myBetsAreas[MYBETS_AREAS.EDP].isMatchCmtryDataAvailable = false;
        }
      });
    });
  }
  // Display Allwinnerbonus and value
  isDisplayBonus(receipt){
    return this.betReceipts.has(receipt);
  }
}
