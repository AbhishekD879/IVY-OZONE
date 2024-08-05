import { from as observableFrom, of as observableOf, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

import { SessionService } from '@authModule/services/session/session.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { UserService } from '@core/services/user/user.service';
import { CashOutMapService } from '../../services/cashOutMap/cash-out-map.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { CashoutBetsStreamService } from '@app/betHistory/services/cashoutBetsStream/cashout-bets-stream.service';

import { CashOutBetsMap, IMapState } from '../../betModels/cashOutBetsMap/cash-out-bets-map.class';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { IDateRangeErrors } from '@app/betHistory/models/date-range-errors.model';
import { IDatePickerDate, IDatePickerMinMaxDates } from '@app/betHistory/models/date-picker-date.model';
import { DatepickerValidatorService } from '@app/betHistory/services/datePickerValidator/datepicker-validator.service';
import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import { BetsLazyLoadingService } from '@app/betHistory/services/betsLazyLoading/bets-lazy-loading.service';
import environment from '@environment/oxygenEnvConfig';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { BET_HISTORY_CONFIG } from '@app/betHistory/constants/bet-promotions.constant';
import { MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'cash-out-page',
  templateUrl: 'cash-out-page.component.html'
})
export class CashOutPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() area?: string;

  title: string;
  data: CashOutBetsMap;
  /**
   * Current state for cash out map (isEmpty | isUserLogOut | isSpinnerActive)
   * @member {object}
   */
  mapState: IMapState;
  datePickerErrors: IDateRangeErrors;
  startDate: IDatePickerDate;
  endDate: IDatePickerDate;
  isLoading = false;
  errorMsg: string;
  contactUsMsg: string;
  isMyBetsInCasino: boolean = false;
  minDate: string;
  maxDate: string;
  private betsStreamOpened: boolean = false;
  private cashoutDataSubscription: Subscription;
  private lazyLoadedBets: IBetDetail[];
  readonly helpSupportUrl: string = environment.HELP_SUPPORT_URL;
  readonly BETHISTORYCONFIG = BET_HISTORY_CONFIG;
  readonly MYBETS_WIDGET = MYBETS_AREAS.WIDGET;

  constructor(private cashOutMapService: CashOutMapService,
              private userService: UserService,
              private maintenanceService: MaintenanceService,
              private sessionService: SessionService,
              private liveServService: LiveServConnectionService,
              private pubsubService: PubSubService,
              private localeService: LocaleService,
              private deviceService: DeviceService,
              private infoDialogService: InfoDialogService,
              private cashoutBetsStreamService: CashoutBetsStreamService,
              private datepickerValidatorService: DatepickerValidatorService,
              private cashoutWsConnectorService: CashoutWsConnectorService,
              private betsLazyLoading: BetsLazyLoadingService,
              private betHistoryMainService: BetHistoryMainService,
              private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
              private sessionStorageService: SessionStorageService,
              private windowRef: WindowRefService) {
    super();
  }

  ngOnInit(): void {
    this.cashoutBetsStreamService.clearCashoutBetsObservable();
    this.title = this.area || 'cashout-area';
    this.contactUsMsg = this.localeService.getString('bethistory.openBetsOverLimitPeriodMessage', [this.helpSupportUrl]);
    const dateRanges = this.cashoutWsConnectorService.getFormattedDateObject();
    this.startDate = dateRanges.startDate;
    this.endDate = dateRanges.endDate;
    this.datepickerValidatorService.initSystemConfig('cashout').subscribe((dateObj: IDatePickerMinMaxDates) => {
      if(dateObj?.minDate && dateObj.maxDate) {
        this.minDate = dateObj.minDate;
        this.maxDate = dateObj.maxDate;
      }
    });
    this.datePickerErrors = this.datepickerValidatorService.getDefaultErrorsState();
    
    this.loadCashOutBetsData();

    this.pubsubService.subscribe(this.title, 'EDIT_MY_ACCA', () => {
      this.reloadSegment();
    });
    this.pubsubService.subscribe(this.title,
      [this.pubsubService.API.LOAD_CASHOUT_BETS,
      this.pubsubService.API.RELOAD_COMPONENTS],
      () => this.reload());
    this.isMyBetsInCasino = this.casinoMyBetsIntegratedService.isMyBetsInCasino;

    this.displayFirstBet();
  }

  /**
   * loads bets data
   */
  loadCashOutBetsData(isDateChanged: boolean  = false): void {
    if (!this.deviceService.isOnline()) {
      this.infoDialogService.openConnectionLostPopup();
      this.errorHandler();
    } else {
      this.isLoading = true;
      this.lazyLoadedBets = [];
      this.cashoutDataSubscription = this.maintenanceService.siteServerHealthCheck(true).pipe(
        switchMap(() => {
          return observableFrom(this.sessionService.whenProxySession());
        }),
        switchMap(() => {
          if (this.userService.isInShopUser()) {
            return observableOf([]);
          }
          this.betsStreamOpened = true;
          return isDateChanged ? this.cashoutWsConnectorService.dateChangeBet(this.startDate, this.endDate)
            : this.cashoutBetsStreamService.getCashoutBets();
        })
      ).subscribe((data: IBetDetail[]) => {
        const bets = this.handleBetsData(data);
        if(!this.sessionStorageService.get('tutorialCompleted') && this.sessionStorageService.get('betPlaced')) {
          this.sessionStorageService.set('tutorialCompleted', true);
          const activeType = bets && bets.length? 'cashOut' : 'defaultContent';
          const storedOnboardingData = this.sessionStorageService.get('firstBetTutorial');
          this.pubsubService.publish(this.pubsubService.API.FIRST_BET_PLACEMENT_TUTORIAL,
            {step:'myBets', tutorialEnabled: storedOnboardingData && storedOnboardingData.firstBetAvailable, type: activeType});
        }
        this.data = this.extendCashOutDataWithMap(bets);
        this.hideSpinner();
        this.isLoading = false;
        this.betsLazyLoading.initialize({
          initialData: { bets: this.data, pageToken: this.cashoutWsConnectorService.pagingToken },
          addLazyLoadedBets: this.addLazyLoadedBets.bind(this),
          betfilter: this.BETHISTORYCONFIG.sportsTab,
          loadMoreCallBack: () => this.cashoutWsConnectorService.nextCashoutBet(this.betsLazyLoading.setData.bind(this.betsLazyLoading))
        });
      }, () => {
        this.errorHandler();
        this.isLoading = false;
      });
    }
  }

  /**
   * handles the bet data
   */
  handleBetsData(data: IBetDetail[]): IBetDetail[] {
    this.betHistoryMainService.extendCashoutBets(data);
    const bets = this.filterCashoutBets(data);
    this.mapState = this.cashOutMapService.cashoutBetsMap.mapState;
    this.mapState.isUserLogOut = false;
    return bets;
  }
  
  ngOnDestroy(): void {
    this.pubsubService.publish(this.pubsubService.API.EMA_UNSAVED_IN_WIDGET, false);
    this.pubsubService.publish(this.pubsubService.API.CASHOUT_CTRL_STATUS, { ctrlName: 'fullCashout', isDestroyed: true });
    this.pubsubService.unsubscribe(this.title);

    this.cashoutBetsStreamService.clearCashoutBetsObservable();

    if (this.cashoutDataSubscription) {
      this.cashoutDataSubscription.unsubscribe();
    }

    if (this.betsStreamOpened) {
      this.cashoutBetsStreamService.closeBetsStream();
      this.betsStreamOpened = false;
    }
  }

  get userStatus(): boolean {
    return this.userService.status;
  }
  set userStatus(value:boolean){}
  /**
   * Reloads cash out segment
   * @private
   */
  reloadSegment(): void {
    this.showSpinner();
    this.ngOnDestroy();
    this.ngOnInit();
  }

  /**
   * Filter bets with cashout available
   * @param {IBetDetail[]} bets - Open Bets  array
   * @returns {BetDetail[]} bets with cashut abailable
   */
  private filterCashoutBets(bets: IBetDetail[]) {
    return (bets || []).filter((bet: IBetDetail) => !isNaN(Number(bet.cashoutValue)) || bet.cashoutValue === 'CASHOUT_SELN_SUSPENDED');
  }

  /**
   * reload component when subscribe triggered.
   * @private
   */
  private reload(): void {
    this.sessionService.whenProxySession().then(() => {
      this.liveServService.connect().subscribe(() => this.reloadSegment());
    });
  }

  /**
   * Assign cash out map to cash out data object to be used for directives
   * @param {Array} bets
   * @private
   */
  private extendCashOutDataWithMap(bets: IBetDetail[]): CashOutBetsMap {
    return this.cashOutMapService.createCashoutBetsMap(bets, this.userService.currency, this.userService.currencySymbol);
  }

  /**
   * handles date picker changes
   * @param errorObject 
   */
  processDateRangeData(errorObject: IDateRangeErrors): void {
    this.datepickerValidatorService.updateErrorsState(
      this.datePickerErrors,
      errorObject,
      this.startDate,
      this.endDate
    );
    if (this.isDatePickerError()) { return; }

    this.loadCashOutBetsData(true);
  }


  /**
   * add lazy loaded bets on scroll
   */
  private addLazyLoadedBets(lazyLoadedBets: IBetDetail[] = []): void {
    const bets = this.handleBetsData(lazyLoadedBets);
    this.lazyLoadedBets = lazyLoadedBets;
    const previousBets = { ...this.data } as CashOutBetsMap;
    const lazyLoadedBetsData = this.extendCashOutDataWithMap(bets);
    this.data = { ...previousBets, ...lazyLoadedBetsData } as CashOutBetsMap;
  }

  /**
 * Check if datepicker error
 * @return {boolean}
 */
  isDatePickerError(): boolean {
    return this.datepickerValidatorService.isFourYearsDatePickerError(this.datePickerErrors);
  }

  private errorHandler(): void {
    const page: string = this.localeService.getString('app.betslipTabs.cashout').toLowerCase();

    this.errorMsg = this.localeService.getString('app.loginToSeePageMessage',
      { page: `${page} bets` });
    this.showError();
  }

  private displayFirstBet(): void {
    const firstBetElement = this.windowRef.document.getElementsByClassName('firstBet');
    if (!firstBetElement.length) {
      return;
    }
    if (firstBetElement[0].classList.contains('display-none')) {
      firstBetElement[0].classList.remove('display-none');
    }
  }
}
