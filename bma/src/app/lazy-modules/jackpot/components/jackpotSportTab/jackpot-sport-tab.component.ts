import { Component, ElementRef, ViewChild, Input, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { BetPlacementErrorTrackingService } from '@core/services/betPlacementErrorTracking/bet-placement-error-tracking';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { JackpotReceiptPageService } from '@lazy-modules/jackpot/services/jackpot-receipt-page.service';
import { JackpotSportTabService } from '@lazy-modules/jackpot/services/jackpot-sport-tab.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { HowToPlayDialogComponent } from '@lazy-modules/jackpot/components/howToPlayDialog/how-to-play-dialog.component';
import { LuckyDipDialogComponent } from '@lazy-modules/jackpot/components/luckyDipDialog/lucky-dip-dialog.component';
import { IBetsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IPoolEntity } from '@core/models/pool.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { AccountUpgradeLinkService } from '@app/vanillaInit/services/accountUpgradeLink/account-upgrade-link.service';

@Component({
  selector: 'jackpot-sport-tab',
  styleUrls: [ 'jackpot-sport-tab.component.scss'],
  templateUrl: 'jackpot-sport-tab.component.html'
})
export class JackpotSportTabComponent implements OnInit, OnDestroy {
  @Input() sport: { jackpot: Function };
  @ViewChild('errorElm', {static: true}) errorElm: ElementRef;

  initialDataByTimeOrder: ISportEvent[] = [];
  initialData: ISportEvent[] = [];
  isLoaded: boolean = false;
  isResponseError: boolean = false;
  internalError: boolean = false;
  insuficientFoundsError: boolean = false;
  betRejectedError: boolean = false;
  placeJackpotPending: boolean = false;
  confirm: boolean = false;
  totalLines: number | any = 0;
  headerMessage: string;
  stakePerLineOptions: number[];
  stakePerLine: { value: number | any };

  numberOfSelections: number;
  private confirmPromise: any;
  private isLoginAndPlaceBets: boolean = false;
  private document: HTMLDocument;
  private window: any;

  private readonly tagName: string = 'JackpotSportTabComponent';

  constructor(
    private betPlacementErrorTrackingService: BetPlacementErrorTrackingService,
    private jackpotReceiptPageService: JackpotReceiptPageService,
    private sbFiltersService: SbFiltersService,
    private filtersService: FiltersService,
    private domToolsService: DomToolsService,
    private dialogService: DialogService,
    private jackpotSportTabService: JackpotSportTabService,
    private localeService: LocaleService,
    private windowRef: WindowRefService,
    private timeService: TimeService,
    private router: Router,
    private pubsub: PubSubService,
    private userService: UserService,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
  ) {
    this.window = this.windowRef.nativeWindow;
    this.document = this.windowRef.document;
  }

  ngOnInit(): void {
    this.subscribe();

    this.loadJackpotData();
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.tagName);
  }

  get betsArray(): string[] {
    return this.jackpotSportTabService.betsArray;
  }
  set betsArray(value:string[]){}

  /**
   * Check if outcome is selected
   * @param {string} outcomeId
   * @returns {boolean}
   */
  isSelected(outcomeId: string): boolean {
    return this.jackpotSportTabService.isSelected(outcomeId);
  }

  /**
   * Open how to play dialog window
   * Football jackpot
   */
  openHowToPlayDialog(): void {
    this.dialogService.openDialog(
      DialogService.API.howToPlay,
      HowToPlayDialogComponent,
      false, {
        dialogClass: 'new-dialog dialog-no-overlay jackpot-dialog'
      });
  }

  addStake(newStake: number): void {
    this.jackpotSportTabService.addStake(newStake);
    this.hideJackpotErrors();
  }

  /**
   * Jackpot Add Bet
   * @param {string} outcomeId
   * @param {ISportEvent} eventEntity
   */
  addBet(outcomeId: string, eventEntity: ISportEvent): void {
    eventEntity.selected = eventEntity.selected || 0;
    this.jackpotSportTabService.addBet(outcomeId, eventEntity);
    this.calculateLines();
    this.hideJackpotErrors();
  }

  /**
   * Clears all selections
   */
  removeAllBets(): void {
    this.hideJackpotErrors();
    this.jackpotSportTabService.removeAllBets();
    _.each(this.initialData, (item: ISportEvent) => {
      item.selected = 0;
    });
    this.jackpotSportTabService.removeStake();
    this.calculateLines();

    this.confirm = false;

    if (this.confirmPromise) {
      clearTimeout(this.confirmPromise);
    }
  }

  /**
   * Set Currency
   * @param {number} value
   * @param {boolean} isToFixed
   */
  setCurrency(value: number, isToFixed: boolean = false): void {
    const val: number | string = isToFixed ? value.toFixed(2) : value;
    return this.filtersService.setCurrency(val, '£');
  }

  /**
   * Set Button Title
   * @param {string} text
   * @returns {string}
   */
  setButtonText(text: string): string {
    return this.localeService.getString(this.sbFiltersService.outcomeMinorCodeName(text) as string);
  }

  /**
   * Confirm clearing all bets
   */
  confirmClear(): void {
    this.confirm = true;

    if (this.confirmPromise) {
      clearTimeout(this.confirmPromise);
    }

    this.confirmPromise = setTimeout(() => {
      this.confirm = false;
    }, this.timeService.fiveSeconds);
  }

  /**
   * Makes Lucky Dip if no selections added
   */
  makeLuckyDipClicked(): void {
    if (this.betsArray.length) {
      this.openLuckyDipDialog();
      return;
    }
    this.makeLuckyDip(this.initialData);
  }

  /**
   * Place bat on Jackpot
   */
  placeJackpotBets(): void {
    if (this.userService.isInShopUser()) {
      this.windowRef.nativeWindow.location.href = this.accountUpgradeLinkService.inShopToMultiChannelLink;
      return;
    }

    this.hideJackpotErrors();

    const amount: number = this.totalLines * this.jackpotSportTabService.getStake();
    const stakePerLine: number = this.jackpotSportTabService.getStake();
    const outcomeIds: string[] = this.betsArray;
    const pool: IPoolEntity = this.initialData[0].pool;
    const linesNumber: number = this.totalLines;

    this.placeJackpotPending = true;
    this.jackpotSportTabService.placeJackpotBet(amount, stakePerLine, outcomeIds, pool, linesNumber)
      .subscribe((response: IBetsResponse) => {
      this.placeJackpotPending = false;
      this.jackpotReceiptPageService.setReceiptData(
        this.initialData, this.betsArray,
        this.totalLines * this.jackpotSportTabService.getStake(),
        this.totalLines, response.bet[0].receipt
      );

      this.router.navigate(['football-jackpot-receipt']);
      this.removeAllBets();
    }, error => {
      this.placeJackpotPending = false;
      if (error.code) {
        switch (error.code) {
          case 'NOT_LOGGEDIN':
            this.pubsub.publish(this.pubsub.API.OPEN_LOGIN_DIALOG, {
              placeBet: 'jackpot',
              moduleName: 'footballjackpot'
            });
            break;
          case 'INSUFFICIENT_FUNDS':
            this.insuficientFoundsError = true;
            break;
          case 'BET_REJECTED':
            this.betRejectedError = true;
            break;
          case 'status.CountryBanned':
            this.betRejectedError = true;
            this.pubsub.publish(this.pubsub.API.SHOW_LOCATION_RESTRICTED_BETS_DIALOG);
            break;
          default:
            this.internalError = true;
            break;
        }
        if (this.betRejectedError || this.internalError || this.insuficientFoundsError) {
          this.scrollToError();
        }
        // sending errors to betPlacementErrorTracking service
        this.betPlacementErrorTrackingService.sendJackpot(error.code, error.errorDesc || error.code);
      }
    });
  }

  /**
   * Subscribe Events
   */
  private subscribe(): void {
    this.pubsub.subscribe(this.tagName, this.pubsub.API.LOGIN_POPUPS_END, () => {
      if (this.isLoginAndPlaceBets) {
        this.isLoginAndPlaceBets = false;
        this.placeJackpotBets();
      }
    });

    this.pubsub.subscribe(this.tagName, this.pubsub.API.SUCCESSFUL_LOGIN, placeBet => {
      this.isLoginAndPlaceBets = placeBet === 'jackpot';
    });

    // stop placing bet if notification popup is displayed after logged in
    this.pubsub.subscribe(this.tagName, this.pubsub.API.USER_INTERACTION_REQUIRED, () => {
      this.isLoginAndPlaceBets = false;
    });
  }

  /**
   * Load Jackpot Data
   */
  public loadJackpotData(): void {
    this.isLoaded = false;
    this.isResponseError = false;

    this.sport.jackpot().then((events: ISportEvent[]) => {
      this.initialData = this.jackpotSportTabService.sortJackpotData(events) || [];
      if (this.initialData.length) {
        this.headerMessage = this.localeService.getString('fb.headerMessage', [this.initialData.length]);
        this.initialDataByTimeOrder = this.initialData;
        _.each(this.initialDataByTimeOrder, (eventEntity: ISportEvent) => {
          eventEntity.markets[0].outcomes = _.sortBy(eventEntity.markets[0].outcomes, 'name');
          eventEntity.filteredStartTime = this.timeService.formatByPattern(new Date(eventEntity.startTime), 'EEEE, d-MMM-yy. h:mm a');
        });
      }
      // Ranges
      const ranges: number[] = _.range(1, 21); // array [1 .. 20]
      this.stakePerLine = { value: ranges[0] };
      this.stakePerLineOptions = ranges;
      this.countSelections();
      this.isLoaded = true;
      this.isResponseError = false;
    }).catch(error => {
      this.initialData = [];
      this.isLoaded = true;
      this.isResponseError = true;
      console.warn('Jackpot Data:', error && error.error || error);
    });
  }

  /**
   * Make lucky dip selection
   * @param {ISportEvent[]} data
   */
  private makeLuckyDip(data: ISportEvent[]): void {
    this.jackpotSportTabService.makeLuckyDip(data);
    this.calculateLines();
  }

  /**
   * Сalculation of lines for jackpot
   */
  private calculateLines(): void {
    this.totalLines = 1;
    _.each(this.initialData, (event: ISportEvent) => {
      if (!event.unavailable) {
        this.totalLines *= event.selected || 0;
      }
    });
    this.updateStakePerLineSelection();
  }

  /**
   * Updates Stake Per Line Options to allow user place bets with stake of 0.25 (when 4 lines) and 0.50 (for 2 lines)
   */
  private updateStakePerLineSelection(): void {
    // the customer should be able to place 0.50 stake FJ bet when 2 lines are selected
    if (this.totalLines > 1 && this.stakePerLineOptions.length < 21) {
      this.stakePerLineOptions.unshift(0.5);
    }
    // the customer should be able to place 0.25 stake FJ bet when 4 lines are selected
    if (this.totalLines > 3 && this.stakePerLineOptions.length < 22) {
      this.stakePerLineOptions.unshift(0.25);
    }

    if (this.totalLines < 4 && this.stakePerLineOptions.length > 21) {
      this.shiftOption();
    }

    if (this.totalLines < 2 && this.stakePerLineOptions.length > 20) {
      this.shiftOption();
    }
  }

  /**
   * If outcomes are selected it will add property selected for events
   * required for counting of lines and stakes in jackpot
   */
  private countSelections(): void {
    if (this.initialData) {
      // Number of possible selections
      this.numberOfSelections = this.initialData.length;

      _.each(this.initialData, (event: ISportEvent) => {
        let selected = 0;

        if (this.isUnavailable(event)) {
          event.unavailable = true;
          --this.numberOfSelections;
        }

        _.each(event.markets[0].outcomes, (outcome: IOutcome) => {
          if (this.isSelected(outcome.id)) {
            if (event.unavailable || outcome.outcomeStatusCode === 'S') {
              this.addBet(outcome.id, event);
            } else {
              selected++;
            }
          }
        });
        event.selected = selected;
      });
      this.calculateLines();
      this.stakePerLine.value = this.jackpotSportTabService.getStake();
    }
  }

  /**
   * Opens lucky dip dialog window
   */
  private openLuckyDipDialog(): void {
    this.dialogService.openDialog(
      DialogService.API.luckyDip,
      LuckyDipDialogComponent,
      false, {
        makeLuckyDip: () => this.makeLuckyDip(this.initialData),
        closeByEsc: false,
        closeByDocument: false
      });
  }

  /**
   * Returns true if event/market/outcomes are suspended
   * @param {ISportEvent} event
   * @returns {boolean}
   */
  private isUnavailable(event: ISportEvent): boolean {
    const market = event.markets[0];
    return event.eventStatusCode === 'S' || market.marketStatusCode === 'S' || _.every(market.outcomes, outcome => {
      return outcome.outcomeStatusCode === 'S';
    });
  }

  /**
   * Deletes first option and resets stake per line value if it was equal the deleted one
   */
  private shiftOption(): void {
    if (this.stakePerLine.value === this.stakePerLineOptions.shift()) {
      this.stakePerLine.value = this.stakePerLineOptions[0];
      this.addStake(this.stakePerLine.value); // save value to the localStarage
    }
  }

  /**
   * Hide all jackpot errors
   */
  private hideJackpotErrors(): void {
    this.internalError = false;
    this.insuficientFoundsError = false;
    this.betRejectedError = false;
  }

  /**
   * Scroll to Error
   */
  private scrollToError(): void {
    const errorElm = this.errorElm && this.errorElm.nativeElement;

    if (errorElm) {
      const top = this.domToolsService.getOffset(errorElm).top;
      const position = top - ((this.window.innerHeight / 2) + errorElm.offsetHeight);
      this.document.body.scrollTop = position; // For Safari
      this.document.documentElement.scrollTop = position; // For Chrome, Firefox, IE and Opera
    }
  }
}
