import { Observable, of, from as observableFrom, Subscription } from 'rxjs';

import { finalize, mergeMap } from 'rxjs/operators';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';

import { CashoutBetsStreamService } from '@app/betHistory/services/cashoutBetsStream/cashout-bets-stream.service';
import { SessionService } from '@authModule/services/session/session.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { IBetHistoryBet, IPageBets } from '@app/betHistory/models/bet-history.model';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { BetsLazyLoadingService } from '../../services/betsLazyLoading/bets-lazy-loading.service';
import { UserService } from '@core/services/user/user.service';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { BET_HISTORY_CONFIG } from '@betHistoryModule/constants/bet-promotions.constant';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import { IDateRangeErrors } from '@app/betHistory/models/date-range-errors.model';
import { IDatePickerDate, IDatePickerMinMaxDates } from '@app/betHistory/models/date-picker-date.model';
import { DatepickerValidatorService } from '@app/betHistory/services/datePickerValidator/datepicker-validator.service';
import environment from '@environment/oxygenEnvConfig';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { ISystemConfig } from '@app/core/services/cms/models';

@Component({
  selector: 'open-bets',
  templateUrl: './open-bets.component.html'
})
export class OpenBetsComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  static COMPONENT_ID: number = 0;

  @Input() area?: string;

  contactUsMsg: string;
  bets: IBetHistoryBet[];
  regularType: ISwitcherConfig;
  lottoType: ISwitcherConfig;
  poolType: ISwitcherConfig;
  loadFailed: boolean;
  isLoading: boolean;
  betTypes: ISwitcherConfig[];
  filter: string;
  errorMsg: string;
  datePickerErrors: IDateRangeErrors;
  startDate: IDatePickerDate;
  endDate: IDatePickerDate;
  minDate: string;
  maxDate: string;
  showDatepicker = false;

  isMyBetsInCasino: boolean = false;
  isRetailBetAvailable: boolean = true;
  isSportIconEnabled: boolean;
  protected readonly TYPES: string[] = ['regularType', 'lottoType', 'poolType'];
  protected cmsSubscription: Subscription;
  readonly betType: string = 'open';
  readonly BETHISTORYCONFIG = BET_HISTORY_CONFIG;
  readonly helpSupportUrl: string = environment.HELP_SUPPORT_URL;
  readonly MYBETS_WIDGET = MYBETS_AREAS.WIDGET;
  private ctrlName: string;
  private betsStreamOpened: boolean = false;
  private loadDataSub: Subscription;
  private editMyAccaReload: boolean;
  private lazyLoadedBets: IBetHistoryBet[] = [];

  constructor(
    protected cmsService: CmsService,
    protected pubSubService: PubSubService,
    private cashoutBetsStreamService: CashoutBetsStreamService,
    private sessionService: SessionService,
    private liveServConnectionService: LiveServConnectionService,
    protected localeService: LocaleService,
    private maintenanceService: MaintenanceService,
    private betHistoryMainService: BetHistoryMainService,
    private userService: UserService,
    public betsLazyLoading: BetsLazyLoadingService,
    private editMyAccaService: EditMyAccaService,
    private cashoutWsConnectorService: CashoutWsConnectorService,
    private datepickerValidatorService: DatepickerValidatorService,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    protected sessionStorageService: SessionStorageService
  ) {
    super();
    this.changeFilter = this.changeFilter.bind(this);
  }

  ngOnInit(): void {
    this.ctrlName = `OpenBets_${OpenBetsComponent.COMPONENT_ID++}`;
    this.contactUsMsg = this.localeService.getString('bethistory.openBetsOverLimitPeriodMessage', [this.helpSupportUrl]);
    this.betTypes = this.betHistoryMainService.buildSwitchers(this.changeFilter);

    this.initTypes();

    this.filter = this.betTypes[0].viewByFilters;
    this.showFirstBet(this.filter);
    const dateRanges = this.cashoutWsConnectorService.getFormattedDateObject();
    this.startDate = dateRanges.startDate;
    this.endDate = dateRanges.endDate;

    this.datepickerValidatorService.initSystemConfig('openBets').subscribe((dateObj: IDatePickerMinMaxDates) => {
      if(dateObj?.minDate && dateObj.maxDate) {
        this.minDate = dateObj.minDate;
        this.maxDate = dateObj.maxDate;
      }
    });
    this.datePickerErrors = this.datepickerValidatorService.getDefaultErrorsState();

    this.betsLazyLoading.reset();
    this.maintenanceService.siteServerHealthCheck().pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe(() => {
        this.loadData(this.filter);
      });

    this.pubSubService.subscribe(this.ctrlName, ['RELOAD_OPEN_BETS'], () => {
      this.reloadComponent();
    });

    this.pubSubService.subscribe(this.ctrlName, this.pubSubService.API.EDIT_MY_ACCA, () => {
      this.reloadComponent(true);
    });

    this.pubSubService.subscribe(this.ctrlName, this.pubSubService.API.RELOAD_COMPONENTS, () => {
        observableFrom(this.sessionService.whenProxySession())
          .subscribe(() => this.reload());
      }
    );
    this.pubSubService.subscribe(this.BETHISTORYCONFIG.openInshopCount,
      this.pubSubService.API.OPEN_INSHOP_BETS_COUNT, (length: number) => {
      this.isRetailBetAvailable = !!length;
    });

    this.isMyBetsInCasino = this.casinoMyBetsIntegratedService.isMyBetsInCasino;
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isSportIconEnabled = config?.CelebratingSuccess?.displaySportIcon?.includes('openbets');
    });
  }

  /**
   * Unsubscribe
   */
  ngOnDestroy(): void {
    this.pubSubService.publish(this.pubSubService.API.EMA_UNSAVED_IN_WIDGET, false);
    this.pubSubService.unsubscribe(this.ctrlName);
    this.pubSubService.unsubscribe(this.BETHISTORYCONFIG.openInshopCount);
    this.betsLazyLoading.reset();

    this.closeBetsStream();

    if (this.loadDataSub) {
      this.loadDataSub.unsubscribe();
    }
    if(this.cmsSubscription) {
      this.cmsSubscription.unsubscribe();
    }
  }

  get userStatus(): boolean {
    return this.userService.status;
  }
set userStatus(value:boolean){}
  /**
   * Set error for error template
   * @param {boolean} state
   */
  setError(state: boolean = true): void {
    this.loadFailed = state;
    if (!state) { return; }
    this.showError();
  }

  /**
   * Reloads component
   * @protected
   */
  reloadComponent(editMyAcca: boolean = false): void {
    this.editMyAccaReload = editMyAcca;
    super.reloadComponent();
    this.editMyAccaReload = false;
  }

  /**
   * Tab click handler
   * @param {string} filter The switcher/tab selected viewByFilters value
   * @returns {void}
   */
  protected changeFilter(filter: string): void {
    this.showFirstBet(filter);

    if (this.canEditCancelMessageShow()) {
      this.editMyAccaService.showEditCancelMessage();
    } else {
      if (filter !== this.BETHISTORYCONFIG.digitalSportBet && filter !== this.BETHISTORYCONFIG.shopBet) {
        this.loadData(filter);
      }
      const dateRanges = this.cashoutWsConnectorService.getFormattedDateObject();
      this.startDate = dateRanges.startDate;
      this.endDate = dateRanges.endDate;
      this.datePickerErrors = this.datepickerValidatorService.getDefaultErrorsState();
      this.updateDatePickerErrorState(this.datePickerErrors);
      this.filter = filter;
      this.isRetailBetAvailable = filter === this.BETHISTORYCONFIG.shopBet ? false : true;
      this.pubSubService.publish('UPDATE_ITEM_HEIGHT',  !this.isRetailBetAvailable);
    }
  }

  /**
   * check if Edit cancel message can be show
   * @returns {boolean}
   */
  private canEditCancelMessageShow(): boolean {
    const OPENBETSAREA = 'open-bets-page';
    return (this.editMyAccaService.isUnsavedInWidget() && this.area !== OPENBETSAREA) || this.area === OPENBETSAREA &&
    !this.editMyAccaService.canChangeRoute();
  }

  /**
   * Init components types
   */
  private initTypes(): void {
    this.TYPES.forEach((type: string) => this[type] = this.betHistoryMainService.getSwitcher(type));
  }

  /**
   * reload component when LS MS socket is reestablised
   * @private
   */
  private reload(): void {
    this.liveServConnectionService
      .connect()
      .subscribe(() => {
        this.reloadComponent();
      });
  }

  private addLazyLoadedBets(lazyLoadedBets: IBetHistoryBet[] = []) {
    this.lazyLoadedBets = lazyLoadedBets;
    this.bets = [...this.bets, ...lazyLoadedBets];
  }

  /**
   * If CO 2.0 enabled get bets from CO stream, otherwise get bets from BPP accountHistory
   * @returns {() => Observable<any>}
   */
  private loadBetsFromCashoutStream(): Observable<IPageBets | any> {
    return this.cashoutBetsStreamService.openBetsStream()
      .pipe(
        mergeMap((data: IBetHistoryBet[] | any) => {
          this.betsStreamOpened = true;
          return of({ bets: data });
      }));
  }

  /**
   * Close CO stream if it is opened
   */
  private closeBetsStream(): void {
    if (this.betsStreamOpened) {
      this.cashoutBetsStreamService.closeBetsStream();
      this.betsStreamOpened = false;
    }
  }

  private getOpenBets(filter: string): Observable<IPageBets> {
    if (filter === this.betTypes[0].viewByFilters) {
      return this.loadBetsFromCashoutStream();
    }
    this.closeBetsStream();

    return this.betHistoryMainService.getHistoryForYear(filter, this.betType);
  }

  showFirstBet(filter: string): void {
    this.betHistoryMainService.showFirstBet(filter);
  }

  private loadData(filter: string, isDateChanged: boolean  = false): void {
    if (this.userService.isInShopUser()) {
      this.bets = [];
      return;
    }

    this.isLoading = true;
    this.betsLazyLoading.reset();
    this.lazyLoadedBets = [];

    if (this.loadDataSub) {
      this.loadDataSub.unsubscribe();
    }

    this.loadDataSub = observableFrom(this.sessionService.whenProxySession())
      .pipe(
        mergeMap(() => this.userService.isInShopUser() ? of({ bets: [] }) : 
        isDateChanged ? this.dateChange() : this.getOpenBets(filter)),
        mergeMap((bets: IPageBets) => this.betHistoryMainService.getEditMyAccaHistory(bets))
      ).subscribe((data: IPageBets) => {
        this.betHistoryMainService.extendCashoutBets(data.bets);
        this.bets = data.bets;
        if(this.bets && !this.sessionStorageService.get('tutorialCompleted') && this.sessionStorageService.get('betPlaced')) {
          this.sessionStorageService.set('tutorialCompleted', true);
          const activeType = this.bets.find((bet) => !isNaN(Number(bet.cashoutValue)))? 'cashOut' : 'defaultContent';
          const storedOnboardingData = this.sessionStorageService.get('firstBetTutorial');
          this.pubSubService.publish(this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL,
            {step:'myBets', tutorialEnabled: storedOnboardingData && storedOnboardingData.firstBetAvailable, type: activeType});
        }
        this.pubSubService.publish('UPDATE_SETTLED_BETS_HEIGHT', this.bets.length);
        if (!this.editMyAccaReload) {
          this.pubSubService.publish(this.pubSubService.API.BETS_COUNTER_OPEN_BETS, { data, filter: this.filter });
        }
        this.isLoading = false;
        if (this.filter === this.BETHISTORYCONFIG.sportsTab) {
          data.pageToken = this.cashoutWsConnectorService.pagingToken;
        }
        this.betsLazyLoading.initialize({
          initialData: data,
          addLazyLoadedBets: this.addLazyLoadedBets.bind(this),
          betType: this.betType,
          betfilter: this.filter,
          loadMoreCallBack: () => this.cashoutWsConnectorService.nextCashoutBet(this.betsLazyLoading.setData.bind(this.betsLazyLoading))
        });
      }, () => {
        const page: string = this.localeService.getString('app.betslipTabs.openbets').toLowerCase();

      this.errorMsg = this.localeService.getString(
        'app.loginToSeePageMessage', { page }
      );
      this.showError();
      this.isLoading = false;
    });
  }

  /**
   * handles the date changes
   */
  dateChange(): Observable<IPageBets | any> {
    return this.cashoutWsConnectorService.dateChangeBet(this.startDate, this.endDate).pipe(
      mergeMap((data: IBetHistoryBet[] | any) => {
        this.betsStreamOpened = true;
        return of({ bets: data });
    }));
  }
  /**
   * updates date picker errorState
   * @param errorObject 
   */
  updateDatePickerErrorState(errorObject: IDateRangeErrors): void{
    this.datepickerValidatorService.updateErrorsState(
      this.datePickerErrors,
      errorObject,
      this.startDate,
      this.endDate
    );
  }
  /**
   * handles date picker changes
   * @param errorObject 
   */
  processDateRangeData(errorObject: IDateRangeErrors): void {
    this.updateDatePickerErrorState(errorObject)
    if (this.isDatePickerError()) { return; }

    this.loadData(this.filter, true);
  }

  /**
   * Check if datepicker error
   * @return {boolean}
   */
  isDatePickerError(): boolean {
    return this.datepickerValidatorService.isFourYearsDatePickerError(this.datePickerErrors);
  }

}
