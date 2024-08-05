
import { concatMap } from 'rxjs/operators';
import { Location, DatePipe } from '@angular/common';
import { Component, ChangeDetectorRef, OnInit, OnDestroy, HostListener, ComponentFactoryResolver } from '@angular/core';
import { ActivatedRoute, NavigationStart, Event as EventRouter, Router } from '@angular/router';
import { combineLatest, Subscription } from 'rxjs';
import * as _ from 'underscore';
import { FiltersService } from '@core/services/filters/filters.service';
import { MainLottoService } from '@lottoModule/services/mainLotto/main-lotto.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { AccountUpgradeLinkService } from '@app/vanillaInit/services/accountUpgradeLink/account-upgrade-link.service';
import { WindowRefService } from '@coreModule/services/windowRef/window-ref.service';

import {
  ILottonMenuItem,
  ILotteryMap,
  ILottoDraw,
  ILotto,
  ILottoPrice,
  ILottoTab,
  ILottoCms,
  ILottoCmsPage
} from '../../models/lotto.model';
import { UserService } from '@core/services/user/user.service';
import { SegmentDataUpdateService } from '@app/lotto/services/segmentDataUpdate/segment-data-update.service';
import { ILottoNumber, ILottoNumberMap } from '../../models/lotto-numbers.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LottoNumberSelectorComponent } from '@lottoModule/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { LottoInfoDialogComponent } from '@lottoModule/components/lottoInfoDialog/lotto-info-dialog.component';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { InfoDialogService } from '@app/core/services/infoDialogService/info-dialog.service';
import { IDateRangeObject, IPreviousResults } from '@app/betHistory/models/date-object.model';
import { TimeService } from '@core/services/time/time.service';
import { IDatePickerDate } from '@app/betHistory/models/date-picker-date.model';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { LOTTO_TEMPLATES } from '../../services/mainLotto/main-lotto.constant';
@Component({
  selector: 'lotto-segment-page',
  templateUrl: './lotto-segment-page.component.html',
  styleUrls: ['./lotto-segment-page.component.scss']
})
export class LottoSegmentPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  lotteryData: ILotto;
  isExpended: boolean;
  boosterBall: boolean;
  confirm: boolean;
  orderedDraws: ILottoDraw[];
  ballPicks: number[];
  ballSelected: ILottoNumber[];
  numbersSelected: ILottoNumberMap;
  luckyDipArr: number[];
  showDays: number;
  activeMenuItem: { uri: string; };
  currentLotto: ILotto;
  currentLottery: ILotto;
  limitValue: number;
  draws: ILottoDraw[];
  drawMultiplier: number;
  lotteryPrice: ILottoPrice[];
  potentialReturns: ILottoPrice[];
  numbersData: ILottoNumber[];
  selected: number;
  lottoTabs: ILottoTab[];
  tab: string;
  activeTab: ILottoTab;
  menuItems: ILottonMenuItem[];
  selectionName: string;
  prices: ILottoPrice;
  accumulatorPrices: string;
  days: number;
  hours: number;
  minutes: number;
  timeInterval;
  totalStake: number;
  accumulatorAmount: number | any;
  lottoError: { type: string, msg: string } = { msg: '', type: '' };
  placeBetPending: boolean;
  helpSupportUrl = environment.HELP_LOTTO_RULES;
  private routeChangeListener: Subscription;
  private isDone: boolean;
  previousResults :IPreviousResults[] =[]
  defaultResultData :IPreviousResults[] =[]
  lotteryPrices: ILottoPrice[];
  lottoCmsBanner: ILottoCms;
  singleData: ILottoCmsPage;
  filter: string;
  lottoData: any;
  dateObject: IDateRangeObject;
  startDate: IDatePickerDate;
  endDate: IDatePickerDate;
  drawAtTime1: any[] = [];
  ballsArray: any[] = [];
  drawAtTime2: any;
  isShowMore: boolean = false;
  dateTimeFormat: 'dd/MM/yyyy HH:mm';
  isBrandLadbrokes: boolean;
  lotto = LOTTO_TEMPLATES;
  handleAccordian: boolean;

  constructor(
    private filterService: FiltersService,
    private locale: LocaleService,
    private lottoService: MainLottoService,
    private storage: StorageService,
    private location: Location,
    private datePipe: DatePipe,
    private route: ActivatedRoute,
    private router: Router,
    protected user: UserService,
    private segmentDataUpdateService: SegmentDataUpdateService,
    private pubSubService: PubSubService,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
    private windowRefService: WindowRefService,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private changeDetectorRef: ChangeDetectorRef,
    public userService: UserService,
    private device: DeviceService,
    private infoDialog: InfoDialogService,
    private timeService: TimeService,
    private filtersService: FiltersService,

  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.route.params.pipe(
      concatMap((params) => {
        return this.lottoService.getLotteryData(params.lottery);
      }))
      .subscribe((lottoData: ILotto) => {
        if (!lottoData || !lottoData.uri) {
          this.router.navigate(['/404']);
        } else {
          this.lotteryData = lottoData;
          const previousResultId = this.lotteryData.hasOwnProperty('boosterBall') ?
          [this.lotteryData.boosterBall && this.lotteryData.boosterBall.id] : [this.lotteryData.normal && this.lotteryData.normal.id];
          this.getHistoryOf(previousResultId);
          this.initLotto();
          this.lottoService.setLottoDialog(this.singleData);
          this.hideSpinner();
        }
      }, () => {
        this.showError();
      });
  }

  openLottoInfoDialog(): void {
    if (!this.device.isOnline()) {
      this.infoDialog.openConnectionLostPopup();
    } else {
      const component = this.componentFactoryResolver.resolveComponentFactory(LottoInfoDialogComponent);
      this.dialogService.openDialog(
        DialogService.API.lottoInfoDialog, component, true, 
        { info: this.singleData.infoMessage, label: this.singleData.label, helpLink: this.singleData.nextLink }
      );
    }
  }

  getDipTranslations(luckyNumber: number) {
    return this.filterService.getComplexTranslation('lotto.lucky', '%num', luckyNumber.toString());

  }

  ngOnDestroy(): void {
    clearInterval(this.timeInterval);
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
  }

  setLotto(data, boosterBall): void {
    this.boosterBall = boosterBall;
    this.currentLotto = data;

    this.currentLottery = boosterBall || !data.normal ? data.boosterBall : data.normal;
    this.currentLotto.shutAtTime = this.lottoService.getShutAtTime(this.currentLottery);
    this.activeMenuItem.uri = this.currentLotto.uri;
    this.updateDraws();
    this.lotteryPrice = this.currentLottery.lotteryPrice;
    this.potentialReturns = [...new Map(this.lotteryPrice.map((item) => [item.numberCorrect, item])).values()];
    this.setBallNumbers();
    this.setLottoTabs();
    this.getSelected();
    this.initializeTimer(this.currentLotto.shutAtTime);
    this.setHeaderData()  //lineSummaryPage HeadertagData
    this.pubSubService.publish('ballsUpdate');
  }


  updateDraws(): void {
    this.draws = this.orderedDraws.filter((draw) => draw.checked);
    this.drawMultiplier = this.draws.length || 1;
  }

  setBallNumbers(): void {
    this.numbersData = [];
    // It creates data for balls from 1 to max ball number. (For example, [1,2,...,49])
    this.numbersData = _.chain(this.currentLottery.maxNumber)
      .range()
      .map(num => ({
        value: num + 1,
        selected: false,
        disabled: false
      }))
      .value();
  }

  disabledBalls(): void {
    this.selected = _.where(this.numbersData, { selected: true }).length;
    _.each(this.numbersData, num => {
      num.disabled =
        this.selected === Number(this.currentLottery.maxPicks)
          ? num.selected === false
          : false;
    });
  }

  resetDraws(): void {
    _.each(this.orderedDraws, item => {
      item.checked = false;
    });
    this.storage.remove(`${this.currentLotto.name}Draw`);
  }

  selectNumbers(val): void {
    if (this.numbersData[val.index].selected) {
      _.each(this.numbersData, num => {
        num.disabled = false;
      });
    } else if (this.selected && +this.selected >= this.currentLottery.maxPicks) {
      return;
    }

    this.numbersData[val.index].selected = !this.numbersData[val.index].selected;
    this.disabledBalls();

    this.segmentDataUpdateService.changes.next({
      numbersSelected: this.numbersSelected,
      numbersData: this.numbersData,
      selected: this.selected
    });
  }

  /**
   * Event handler on event emitted in number-selector.component.onBeforeClose
   * @param {number} num - selected value before dialog opened to restore
   */
  resetSelected(num: number): void {
    this.selected = num;
    this.selected= 0;
  }

  doneSelected(): void {
    const numbersDataSelected = _.where(this.numbersData, { selected: true });
    this.storage.set(this.currentLotto.name, numbersDataSelected);
    this.setSelectedBallNumbers(numbersDataSelected);
    this.getSelected();
    this.changeDetectorRef.detectChanges();
    this.router.navigate(['/lotto', 'linesummary', this.route.snapshot.params.lottery || '']);
  }

  numDialog(): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(LottoNumberSelectorComponent);
    const numberBackup: ILottoNumber[] = JSON.parse(JSON.stringify(this.numbersData));
    const selectedBackup: number = this.selected;
    this.storage.set('IsChooseNumber', 'False');
    this.dialogService.openDialog(
      DialogService.API.lottoNumberSelector,
      componentFactory,
      true,
      {
        numbersData: this.numbersData,
        //  luckyDipArr: this.luckyDipArr,
        selected: this.selected,
        selectNumbers: (value, index) => {
          this.selectNumbers({ value, index });
        },
        luckyDip: (val) => {
          //this.isDone = false;
          this.luckyDip(val);
        },
        resetNumbers: () => {
          this.resetNumbers();
        },
        doneSelected: () => {
          this.isDone = true;
          this.doneSelected();
        },
        onBeforeClose: () => {
          if (!this.isDone) {
            this.clearNumberOnClose(numberBackup);
            this.resetSelected(selectedBackup);
            this.setBallNumbers();
          }
          this.isDone = false;
        }
      }
    );
  }
  luckyDip(value: number): void {
    this.ballSelected = [];
    _.each(this.numbersData, num => {
      num.selected = false;
    });
    this.ballSelected = _.each(_.sample(this.numbersData, value), num => {
      num.selected = true;
    }) as ILottoNumber[];

    // It merges data from numbers data (numbersData) and selected balls data (ballSelected)
    this.numbersData = _.values(_.extend(
      _.indexBy(this.numbersData, 'value'), _.indexBy(this.ballSelected, 'value')
    ));
    this.disabledBalls();
  }

  resetNumbers(): void {
    this.ballSelected = [];
    this.storage.remove(this.currentLotto.name);
    this.setBallNumbers();
    this.selected = 0;
    this.getSelected();

    this.segmentDataUpdateService.changes.next({
      numbersSelected: this.numbersSelected,
      numbersData: this.numbersData,
      selected: this.selected
    });
  }

  setTotalStake(): void {
    const pow = Math.pow(10, 2);
    const fixTwoDecimalVal = Math.floor(this.accumulatorAmount * pow) / pow;
    this.totalStake = fixTwoDecimalVal;
  }

  confirmation(event: Event): void {
    if (this.user.status) {
      this.displayPopupForInShopUser(event);
    } else {
      this.confirm = false;
      this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'lottobet' });
    }
  }

  @HostListener('document:click')
  documentClick(): void {
    this.confirm = false;
  }

  protected displayPopupForInShopUser(event: Event): void {
    event.stopPropagation();
    this.confirm = false;
    if (this.user.isInShopUser()) {
      this.windowRefService.nativeWindow.location.href = this.accountUpgradeLinkService.inShopToMultiChannelLink;
      return;
    }

    this.confirm = true;
  }


  private setSelectedBallNumbers(data: ILottoNumberMap): void {
    _.each(_.range(this.currentLottery.maxPicks), (num, i) => {
      const dataValue = data[num] && data[num].value;
      this.numbersSelected[i] = {
        value: dataValue || '-',
        selected: _.isNumber(dataValue),
        disabled: false
      };
    });
  }

  private getTimeLeft(endTime: Date): {
    total: number;
    days: number;
    hours: number;
    minutes: number;
  } {
    const time = endTime.getTime() - new Date().getTime();
    const minutes = Math.floor((time / 1000 / 60) % 60);
    const hours = Math.floor((time / (1000 * 60 * 60)) % 24);
    const days = Math.floor(time / (1000 * 60 * 60 * 24));

    return {
      total: time,
      days,
      hours,
      minutes
    };
  }

  private initializeTimer(time): void {
    const endTime = new Date(time);
    const updateClock = () => {
      const { total, days, hours, minutes } = this.getTimeLeft(endTime);
      const zeroify = value => value <= 0 ? 0 : value;

      this.days = zeroify(days);
      this.hours = zeroify(hours);
      this.minutes = zeroify(minutes);

      if (total <= 0) {
        clearInterval(this.timeInterval);
        this.updateLotto(this.currentLotto);
      }
    };

    clearInterval(this.timeInterval);

    updateClock();
    this.timeInterval = setInterval(updateClock, 1000);

    this.routeChangeListener = this.router.events.subscribe((event: EventRouter) => {
      if (event instanceof NavigationStart) {
        clearInterval(this.timeInterval);
      }
    });
  }

  private getSelected(): void {
    const sglArray = ['SGL', 'DBL', 'TBL', 'ACC4', 'ACC5'];
    this.ballPicks = _.without(_.map((this.numbersSelected as ILottoNumber[]), num => num.value), '-') as number[];
    this.selectionName = sglArray[this.ballPicks.length - 1];
  }

  private setLottoTabs(): void {
    const tabUri = this.router.url;
    this.lottoTabs = [
      {
        title: this.locale.getString('lotto.straight'),
        name: 'Straight',
        hidden: false,
        id: 0,
        url: tabUri
      },
      {
        title: this.locale.getString('lotto.combo'),
        name: 'Combo',
        hidden: true,
        id: 1,
        url: `${tabUri}/combo`
      },
      {
        title: this.locale.getString('lotto.results'),
        name: 'Results',
        hidden: true,
        id: 2,
        url: `${tabUri}/results`
      }
    ];

    this.activeTab = _.findWhere(this.lottoTabs, { url: tabUri });
    this.pubSubService.publish('MENU_UPDATE', this.activeMenuItem.uri);
  }

  /**
   * Initial for lotto segment page
   */
  private initLotto(): void {
    this.activeMenuItem = { uri: null };
    this.isExpended = true;
    this.boosterBall = false;
    this.confirm = false;
    this.orderedDraws = this.ballPicks = this.ballSelected = [];
    this.numbersSelected = {};
    this.luckyDipArr = [3, 4, 5]; // Lucky Dip options for the straight bet type
    this.showDays = 7;  // Days quantity (shows data for those days)
    this.menuItems = this.lottoService.getMenuItems(this.lottoService.cmsLotto());

    if (this.lotteryData && (Date.parse(this.lotteryData.shutAtTime) < Date.now())) {
      this.updateLotto(this.lotteryData);
    } else if (this.lotteryData) {
      this.setLotto(this.lotteryData, this.boosterBall);
    }

    const tabId = this.lotteryData.hasOwnProperty('boosterBall') ? this.lotteryData.boosterBall['id'] : this.lotteryData.normal['id'];
    this.singleData = this.lottoService.lottoCmsBanner.lottoConfig.find((cmsData) => cmsData.ssMappingId.split(",").includes(tabId));
  }

  /**
   * Update current lotto
   * @param {Object} currentLotto
   */
  private updateLotto(currentLotto: ILotto): void {
    this.pubSubService.publish('MSG_UPDATE', {
      type: 'normal',
      msg: currentLotto.name + this.locale.getString('lotto.finished') +
        this.datePipe.transform(currentLotto.shutAtTime, 'HH:mm dd/MM/yyyy')
    });

    this.lottoService.getLotteriesByLotto().subscribe((data: ILotteryMap) => {
      const activeLotto: ILottonMenuItem = _.findWhere(_.toArray(data), { active: true });
      const uri = this.filterService.filterLink(`lotto/${activeLotto.uri}`);
      this.pubSubService.publish('MENU_UPDATE', this.lottoService.getMenuItems(data));
      if (this.location.path() !== uri) {
        setTimeout(() => this.router.navigateByUrl(uri));
      } else {
        this.setLotto(activeLotto, this.boosterBall);
      }
    });
  }
  public clearNumberOnClose(numberBackup: ILottoNumber[]): void {
    _.each(this.numbersData, (numberValue, key) => {
      numberValue.selected = numberBackup[key].selected;
      numberValue.disabled = numberBackup[key].disabled;
      numberValue.value = numberBackup[key].value;
    });
  }
  setHeaderData(): void {
    const time = {
      days: this.days,
      hours: this.hours,
      minutes: this.minutes,
      currentLotto: this.currentLotto.name,
    }
    this.segmentDataUpdateService.headerTime = time;

  }


  filterPreviousResults(previousResultSummary) {
    const previousResults = previousResultSummary.sort((a, b) => {
      return new Date(b.drawAtTime).valueOf() - new Date(a.drawAtTime).valueOf();
    });
    this.handleAccordian = previousResults.length > 2;
    this.defaultResultData = previousResults.map(item => {
      const balls = item.results.toString().split('|');
      const noOfBonusBalls =  item && item.resultsBonus ? 1 : 0
      const preResults : IPreviousResults ={
      id : item.id,
      balls  : balls,
      noOfBalls : Number(balls.length) + noOfBonusBalls,
      drawAt : item.drawAtTime,
      bonusBall :  item && item.resultsBonus,
      drawName :  this.filtersService.removeLineSymbol(item.description), //ex : LunchTimeDraw
      };
      return preResults ;
  
    });
    this.handleToggle(true);
  }
  

  getHistoryOf(lottoId: string[]) {
    const previousDayscount = this.lottoService.getLottoCmsBanner().dayCount || 30;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - previousDayscount);
    this.startDate = { value: startDate };
    this.endDate = { value: new Date() };
    this.dateObject = this.getDateObject();
    const obs$ = lottoId.map(item => this.lottoService.getPreviousResult(this.dateObject, item));
    combineLatest(
      obs$
    )
    .subscribe(data => {
      this.lottoData = data.reduce((current, item) => [...current, ...item], []);
      const resultedDraws =  this.lottoData.reduce((current, item) => {
        return item.resultedDraw ? [...current, ...item.resultedDraw] : current;
      }, []);

      this.filterPreviousResults(resultedDraws);
    });
     
  }

  handleToggle(isInital = false)  {
    if(!isInital) {
      this.isShowMore = !this.isShowMore;
    }
    if(!this.isShowMore){
      this.previousResults = this.defaultResultData.length ? this.defaultResultData.slice(0, 2) : this.defaultResultData ;
    }
    else {
      this.previousResults = this.defaultResultData.slice(0, 10);
    }
  }
  private getDateObject(): IDateRangeObject {
    this.timeService.getLocalDate(this.startDate.value);
    const StartDate = new Date(this.startDate.value);
    StartDate.setUTCHours(0, 0, 0, 0);
    const EndDate = new Date(this.endDate.value);
    EndDate.setUTCHours(24, 0, 0, 0);

    return {
      startDate: StartDate.toISOString().replace('00.0', ''),
      endDate: EndDate.toISOString().replace('00.0', '')
    };
  }
}
