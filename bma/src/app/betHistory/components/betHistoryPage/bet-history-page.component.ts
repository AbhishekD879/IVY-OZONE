import { from as observableFrom, Subscription } from 'rxjs';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { UserService } from '@core/services/user/user.service';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { TimeService } from '@core/services/time/time.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SessionService } from '@authModule/services/session/session.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { DatepickerValidatorService } from '@app/betHistory/services/datePickerValidator/datepicker-validator.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IBetHistorySwitcherConfig } from '../../models/bet-history-switcher-config.model';
import { IDatePickerDate, IDatePickerMinMaxDates } from '@app/betHistory/models/date-picker-date.model';
import { IDateRangeObject } from '@app/betHistory/models/date-object.model';
import { IBetHistoryBet, IPageBets } from '@app/betHistory/models/bet-history.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ResolveService } from '@core/services/resolve/resolve.service';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { IDateRangeErrors } from '@app/betHistory/models/date-range-errors.model';
import { BetsLazyLoadingService } from '../../services/betsLazyLoading/bets-lazy-loading.service';
import environment from '@environment/oxygenEnvConfig';
import * as _ from 'underscore';
import { mergeMap } from 'rxjs/operators';
import { BET_HISTORY_CONFIG } from '@betHistoryModule/constants/bet-promotions.constant';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';
import { ISystemConfig } from '@app/core/services/cms/models';

@Component({
  selector: 'bet-history-page',
  templateUrl: './bet-history-page.component.html',
  styleUrls: ['./bet-history-error-template.scss']
})
export class BetHistoryPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  static COMPONENT_ID: number = 0;

  @Input() area?: string;

  errorMsg: string;
  contactUsMsg: string;
  isExpandedSummary: boolean = false;
  poolType: IBetHistorySwitcherConfig;
  lottoType: IBetHistorySwitcherConfig;
  regularType: IBetHistorySwitcherConfig;
  betTypes: IBetHistorySwitcherConfig[];
  startDate: IDatePickerDate;
  endDate: IDatePickerDate;
  bets: IBetHistoryBet[];
  dateObject: IDateRangeObject;
  filter: string = 'bet';
  betType: string = 'settled';
  showDatepicker: boolean;
  datePickerErrors: IDateRangeErrors;
  loadFailed: boolean;
  isLoading: boolean;
  isMyBetsInCasino: boolean = false;
  protected cmsSubscription: Subscription;
  public isRetailBetAvailable: boolean = true;
  isSportIconEnabled: boolean;

  /**
   * Key for summaryTotals object related to selected tab/switcher
   */
  summarySelected: string;
  summaryTypes: string[];

  readonly helpSupportUrl: string = environment.HELP_SUPPORT_URL;
  readonly BETHISTORYCONFIG = BET_HISTORY_CONFIG;
  private readonly filteredBetsStatus: string = 'pending';
  private ctrlName: string;
  minDate: string;
  maxDate: string;

  constructor(
    protected cmsService: CmsService,
    protected pubSubService: PubSubService,
    private betHistoryMainService: BetHistoryMainService,
    private timeService: TimeService,
    private sessionService: SessionService,
    private liveServConnectionService: LiveServConnectionService,
    private datepickerValidatorService: DatepickerValidatorService,
    protected localeService: LocaleService,
    private resolveService: ResolveService,
    private maintenanceService: MaintenanceService,
    private route: ActivatedRoute,
    private userService: UserService,
    public betsLazyLoading: BetsLazyLoadingService,
    private windowRef: WindowRefService,
    private ezNavVanillaService: EzNavVanillaService
  ) {
    super();
    this.changeFilter = this.changeFilter.bind(this);
  }

  ngOnInit(): void {
    this.ctrlName = `BetHistory_${BetHistoryPageComponent.COMPONENT_ID++}`;

    this.betsLazyLoading.reset();
    this.createFilters();
    this.dateInit();
    this.assignListeners();
    this.summaryTypes = this.getSummarySwitcherRefs();

    const page: string = this.localeService.getString('app.betslipTabs.betHistory').toLowerCase();

    this.errorMsg = this.localeService.getString('app.loginToSeePageMessage', { page: page });

    this.contactUsMsg = this.localeService.getString('bethistory.overLimitPeriodErrorMessage', [this.helpSupportUrl]);
    this.maintenanceService
      .siteServerHealthCheck()
      .subscribe(() => {
        this.loadData();
      });

    this.pubSubService.subscribe(this.BETHISTORYCONFIG.settledInshopCount,
      this.pubSubService.API.SETTLED_INSHOP_BETS_COUNT, (length: number) => {
      this.isRetailBetAvailable = !!length;
    });

    this.isMyBetsInCasino = this.ezNavVanillaService.isMyBetsInCasino;

    this.datepickerValidatorService.initSystemConfig('settledBets').subscribe((dateObj: IDatePickerMinMaxDates) => {
      if(dateObj?.minDate && dateObj.maxDate) {
        this.minDate = dateObj.minDate;
        this.maxDate = dateObj.maxDate;
      }
    });
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isSportIconEnabled = config?.CelebratingSuccess?.displaySportIcon?.includes('settledbets');
    });
  }

  get isBetsTab(): boolean {
    return this.filter !== this.BETHISTORYCONFIG.digitalSportBet;
  }
  set isBetsTab(value: boolean) {}

  get userStatus(): boolean {
    return this.userService.status;
  }
  set userStatus(value:boolean) {}
  /**
   * Set error state from child component
   * @param {boolean} state
   */
  setError(state: boolean = true): void {
    if (!state) { return; }
    this.loadFailed = state;
    this.showError();
  }

  /**
   * Check if datepicker error
   * @return {boolean}
   */
  isDatePickerError(): boolean {
    return this.datepickerValidatorService.isDatePickerError(this.datePickerErrors);
  }
  /**
   * reload component when LS MS socket is reestablised
   */
  reload(): void {
    this.liveServConnectionService
      .connect()
      .subscribe(() => {
        this.reloadComponent();
      });
  }

  processDateRangeData(errorObject: IDateRangeErrors): void {
      this.datepickerValidatorService.updateErrorsState(
        this.datePickerErrors,
        errorObject,
        this.startDate,
        this.endDate
      );
      if (this.isDatePickerError()) { return; }

      if(this.filter === this.BETHISTORYCONFIG.shopBet) {
        this.windowRef.document.dispatchEvent(
          new CustomEvent('RELOAD_MY_BETS_WHEN_DATE_CHANGED', {
            detail: {
              fromDate: this.startDate,
              toDate: this.endDate
            }
          }));
      } else {
        this.loadData();
      }
  }

  ngOnDestroy(): void {
    this.betsLazyLoading.reset();
    this.pubSubService.unsubscribe(this.ctrlName);
    if(this.cmsSubscription) {
      this.cmsSubscription.unsubscribe();
    }
    this.pubSubService.unsubscribe(this.BETHISTORYCONFIG.settledInshopCount);
  }

  memorizeSummaryState(isExp: boolean): void {
    this.isExpandedSummary = isExp;
  }

  /**
   * Reloads component
   * @protected
   */
  reloadComponent(): void {
    this.loadFailed = false;
    super.reloadComponent();
  }

  /**
   * Create filters, set initial filter.
   * Refs is a name of response data field for summary section related to specific filter/tab/switcher
   * @return {void}
   */
  protected createFilters(): void {
    this.regularType = {
      viewByFilters: 'bet',
      name: this.localeService.getString('bethistory.sports'),
      refs: 'sb',
      onClick: filter => this.changeFilter(filter)
    };

    this.lottoType = {
      viewByFilters: 'lotteryBet',
      name: this.localeService.getString('bethistory.lotto'),
      refs: 'lotto',
      onClick: filter => this.changeFilter(filter)
    };

    this.poolType = {
      viewByFilters: 'poolBet',
      name: this.localeService.getString('bethistory.pool'),
      refs: 'pool',
      onClick: filter => this.changeFilter(filter)
    };

    this.betTypes = [this.regularType, this.lottoType, this.poolType];
    this.filter = this.route.snapshot.params['filter'] || this.betTypes[0].viewByFilters;
    this.showFirstBet(this.filter);
    this.summarySelected = this.betTypes[0].refs;
  }

  /**
   * Tab click handler
   * @param {string} filter The switcher/tab selected viewByFilters value
   * @returns {void}
   */
  protected changeFilter(filter: string): void {
      if (this.canDigitalDataLoad(filter)) {
        this.loadData();
        this.summarySelected = this.getSelectedSwitcher(filter).refs;
      }
      this.filter = filter;
      this.showFirstBet(this.filter);
      this.updateShowDatepicker();
      this.isRetailBetAvailable = filter === this.BETHISTORYCONFIG.shopBet ? false : true;
      this.pubSubService.publish('UPDATE_ITEM_HEIGHT',  !this.isRetailBetAvailable);
  }

  /**
   * check if Digital bets can be load
   * @param {string} filter
   * @returns {boolean}
   */
  private canDigitalDataLoad(filter: string): boolean {
    return filter !== BET_HISTORY_CONFIG.digitalSportBet && !this.isDatePickerError() && filter !== BET_HISTORY_CONFIG.shopBet;
  }

  private addLazyLoadedBets(lazyLoadedBets: IBetHistoryBet[] = []): void {
    this.bets = [...this.bets, ...this.filterBetHistory(lazyLoadedBets)];
  }

  /**
   * Do initial operations for date picker
   */
  private dateInit(): void {
    const days: number = this.timeService.oneDayInMiliseconds * 29;
     // today minus 6 days (BMA-47818)
    const startDate: number = new Date().getTime() - days;
    this.datePickerErrors = this.datepickerValidatorService.getDefaultErrorsState();
    this.startDate = { value: new Date(startDate) };
    this.endDate = { value: new Date() };
    this.dateObject = this.getDateObject();
    this.updateShowDatepicker();
  }

  /**
   * Assign needed listeners
   */
  private assignListeners(): void {
    this.pubSubService.subscribe(
      this.ctrlName,
      this.pubSubService.API.RELOAD_COMPONENTS,
      () => {
        observableFrom(this.sessionService.whenProxySession())
          .subscribe(() => this.reload());
      }
    );

    this.pubSubService.subscribe(this.ctrlName, this.pubSubService.API.SESSION_LOGIN, () => {
      this.reloadComponent();
    });

    this.pubSubService.subscribe(
      this.ctrlName,
      this.pubSubService.API.DATEPICKER_INVALID_RANGE,
      (errorObject: IDateRangeErrors) => this.processDateRangeData(errorObject)
    );
  }

  /**
   * check if to show picker
   */
  private updateShowDatepicker(): void {
    this.showDatepicker = this.filter !== 'digitalSportBet';
  }

  /**
   * Get date object based on values from datepicker
   * @return {Object}
   */
  private getDateObject(): IDateRangeObject {
    return {
      startDate: this.timeService.formatByPattern(this.startDate.value, 'yyyy-MM-dd 00:00:00'),
      endDate: this.timeService.formatByPattern(this.endDate.value, 'yyyy-MM-dd 23:59:59')
    };
  }

  /**
   * Loads data about user's bets and wins for selected date period
   */
  private loadData(): void {
    this.isLoading = true;
    this.betsLazyLoading.reset();
    this.dateObject = this.getDateObject();

    observableFrom(this.sessionService.whenProxySession()).pipe(
      mergeMap(() => {
        return observableFrom(
          this.resolveService.set(
            this.betHistoryMainService.makeSafeCall(
              this.betHistoryMainService.getHistoryForTimePeriod(this.filter, this.betType, this.dateObject)
            ).toPromise(),
            'initData'
          )
        );
      })
    ).subscribe(() => {
      const data: IPageBets = this.resolveService.get('initData');
      this.bets = this.filterBetHistory(data.bets);
      this.isLoading = false;
      this.hideSpinner();
      this.betsLazyLoading.initialize({
        initialData: data,
        addLazyLoadedBets: this.addLazyLoadedBets.bind(this),
        betType: this.betType
      });
      this.pubSubService.publish('UPDATE_SETTLED_BETS_HEIGHT', this.bets.length);
    }, () => this.setError(true));
  }

  private filterBetHistory(bets): IBetHistoryBet[] {
    return _.filter(bets, (bet: IBetHistoryBet) => !(this.filter === 'bet' &&
      this.filteredBetsStatus === this.betHistoryMainService.getBetStatus(bet)));
  }

  /**
   * Find switcher/tab object by filter in array of switcher/tabs data
   * @param {string} filter The viewByFilters property of IBetHistorySwitcherConfig object
   * @returns {IBetHistorySwitcherConfig} Switcher/tab object
   */
  private getSelectedSwitcher(filter: string): IBetHistorySwitcherConfig {
    return this.betTypes
      .find((item: IBetHistorySwitcherConfig) => item.viewByFilters === filter);
  }

  /**
   * Get refs array needed for parsing response data
   * @returns {string[]} The array of names related to switchers for further response data fields parsing
   * @example
   * [ sb, lotto, pool ]
   */
  private getSummarySwitcherRefs(): string[] {
    const refs = [];
    this.betTypes.forEach((item: IBetHistorySwitcherConfig) => {
      if (item.refs) {
        refs.push(item.refs);
      }
    });
    return refs;
  }

  private showFirstBet(filter: string): void {
    this.betHistoryMainService.showFirstBet(filter);
  }
}
