import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { TimeService } from '@core/services/time/time.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';

@Component({
  selector: 'regular-bet-header',
  templateUrl: './regular-bet-header.component.html',
  styleUrls: ['./regular-bet-header.component.scss']
})
export class RegularBetHeaderComponent implements OnInit {
  @Input() bet: any;
  @Input() betHistoryHeader: boolean;
  @Input() gtmLocation: string;
  @Input() showArrow: boolean;
  @Input() hasLeaderboardWidget: boolean;
  @Input() reuseLocation: string;

  @Output() reuseBet = new EventEmitter<{}>();

  reusePending: boolean = false;
  isMyBetsInCasino: boolean = false;
  public accaTime: string = '';

  public fullBetType: string;
  private readonly BYBTYPE_FIVEASIDE = '5-A-Side';
  private readonly BET_OPEN = "open";

  constructor(
    private locale: LocaleService,
    private editMyAccaService: EditMyAccaService,
    private timeService: TimeService,
    private serviceClosureService: ServiceClosureService,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService
  ) {}

  get isEMAEnabled(): boolean {
    return this.editMyAccaService.EMAEnabled;
  }
  set isEMAEnabled(value:boolean){}
  get showStatus() {
    return !['open', 'pending'].includes(this.bet.eventSource.totalStatus);
  }
  set showStatus(value:any){}

  get showFiveASideStatus() {
    return ['won','lost'].includes(this.bet.eventSource.totalStatus);
  }

  /**
   * To Validate fiveaside widget
   * @returns {boolean}l
   */
  get hasFiveASideWidget(): boolean {
    return (
      (this.hasLeaderboardWidget &&
        this.bet.eventSource.source === 'f' &&
        !this.showStatus) ||
      (this.hasLeaderboardWidget && this.fullBetType === this.BYBTYPE_FIVEASIDE && this.showFiveASideStatus)
    );
  }

  set hasFiveASideWidget(value: boolean) {}

  ngOnInit(): void {
    this.fullBetType = this.getFullBetType();
    if (this.bet.eventSource.accaHistory) {
      const date = new Date(this.bet.eventSource.accaHistory.time);
      this.accaTime = this.timeService.formatByPattern(date, 'HH:mm - dd MMM');
    }
    this.isMyBetsInCasino = this.casinoMyBetsIntegratedService.isMyBetsInCasino;
  }

  /**
   * Return full bet type
   * @return {string}
   */
  getFullBetType(): string {
    const bet = this.bet.eventSource;
    return bet.bybType
      ? bet.bybType
      : this.checkIfLdip(bet) ? this.locale.getString(`lucky Dip`) : this.locale.getString(`bethistory.betTypes.${bet.betType}`);
  }

  showEditAccaButton(): boolean {
    const bet = this.bet ? this.bet.eventSource : null;
    return (
      ((!this.betHistoryHeader &&
        bet &&
        this.availabilityPerCashOutValue() &&
        !bet.isCashOutedBetSuccess &&
        !(bet.isConfirmInProgress && !bet.isPartialActive) &&
        !(bet.inProgress && !bet.isPartialActive) &&
        this.editMyAccaService.canEditBet(bet) && !this.serviceClosureService.userServiceClosureOrPlayBreak) ||
      (bet && bet.isAccaEdit && !this.serviceClosureService.userServiceClosureOrPlayBreak)) && !this.is2UpMarketExists(bet.leg)
    );
  }
  /**
   * emits the re use flag to the parent when the button is clicked
   */
  reuse(): void {
   this.reuseBet.emit('reuse');
  }

  /**
   * to hide or show the re use button based on the event state
   * @returns {boolean}
   */
  checkIfAnyEventActive(): boolean {
    const isAnyEventActive: string[] = this.bet.eventSource.leg.map((eachLeg) => eachLeg.part[0].outcome[0].result && eachLeg.part[0].outcome[0].result.confirmed)
    const betStatusses: string[] = this.bet.eventSource.leg.map((eachLeg) => eachLeg.status);

    return isAnyEventActive.includes('N') ? betStatusses.includes(this.BET_OPEN) : false;
  }

  /**
   * to hide or show the re use button based on the EDP page
   * @returns {boolean}
   */
  checkEdpPage(): boolean{
    return this.reuseLocation ? this.reuseLocation.toLowerCase() !== 'hredp' && this.reuseLocation.toLowerCase() !== 'edp' : true
  }

  checkIfAnyEventDisplayed(): boolean {
    let anyEventDisplayed: boolean = true;
    if(Object.keys(this.bet.eventSource.events).length > 0) {
      const eventsDisplayed = Object.keys(this.bet.eventSource.events).map(key => this.bet.eventSource.events[key].displayed);
      const marketsDisplayed = Object.keys(this.bet.eventSource.markets).map(key => this.bet.eventSource.markets[key].displayed);
      const selectionOutcomesDisplayed = Object.keys(this.bet.eventSource.outcomes).map(key => this.bet.eventSource.outcomes[key].displayed);
      if(this.bet.eventSource.betType === 'SGL') {
        anyEventDisplayed = eventsDisplayed[0] === 'Y' && marketsDisplayed[0] === 'Y' && selectionOutcomesDisplayed[0] === 'Y'
      } else {
        anyEventDisplayed = eventsDisplayed.some((val,index) => (eventsDisplayed[index] === "Y" && marketsDisplayed[index] === "Y" && selectionOutcomesDisplayed[index] === "Y"))
      }
    }
    return anyEventDisplayed;
  }

  private availabilityPerCashOutValue(): boolean {
    return (
      (!isNaN(this.bet.eventSource.cashoutValue) &&
        Number(this.bet.eventSource.cashoutValue) > 0) ||
      (isNaN(this.bet.eventSource.cashoutValue) &&
        this.bet.eventSource.cashoutValue !== 'CASHOUT_SELN_NO_CASHOUT')
    );
  }

  private is2UpMarketExists(legs) {
    const twoUpMarketName: string = this.locale.getString('bma.twoUpMarketName');
    return legs && legs.length && legs.some(leg => {
      const isTwoUpMarket = leg.eventEntity && leg.eventEntity.categoryId == '16' && leg.part && leg.part.length && leg.part[0].eventMarketDesc == twoUpMarketName;
    return isTwoUpMarket;
    })
  }

  /**
   * Returns true if luckydip bet tags is available
   * @returns {boolean}
   */
  isLdipBetTag(bet: any):boolean{
    return !!bet.eventSource && bet.eventSource.betTags?.betTag.find((tag) => tag.tagName === LUCKY_DIP_CONSTANTS.LDIP);
  }

/**
   * to show the ldip header for luckydip
   * @returns {boolean}
   */
  private checkIfLdip(bet): boolean{
    return bet.betTags?.betTag[0]?.tagName === LUCKY_DIP_CONSTANTS.LDIP;
  }
}
