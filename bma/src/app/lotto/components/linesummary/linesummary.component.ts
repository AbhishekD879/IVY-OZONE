import * as _ from 'underscore';
import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { StorageService } from '@core/services/storage/storage.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { concatMap } from 'rxjs/operators';
import { ILottoNumber, ILottoNumberMap } from '../../models/lotto-numbers.model';
import { ILotto, ILottoCmsPage, ILottoDraw, ILottoLineSummary, ILottoPlaceBetObj, ILottoPrice } from '../../models/lotto.model';
import { MainLottoService } from '../../services/mainLotto/main-lotto.service';
import { DeviceService } from '@core/services/device/device.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { LottoNumberSelectorComponent } from '@lottoModule/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { SegmentDataUpdateService } from '@app/lotto/services/segmentDataUpdate/segment-data-update.service';

import { LocaleService } from '@core/services/locale/locale.service';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { LottoInfoDialogComponent } from '../lottoInfoDialog/lotto-info-dialog.component';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import environment from '@environment/oxygenEnvConfig';
import { LOTTO_TEMPLATES } from '../../services/mainLotto/main-lotto.constant';
import { TimeService } from '@core/services/time/time.service';
@Component({
  selector: 'linesummary',
  templateUrl: './linesummary.component.html',
  styleUrls: ['./linesummary.component.scss']
})
export class LinesummaryComponent implements OnInit {

  linesSummary: ILottoLineSummary[];
  lotteryData: ILotto;
  currentLottery: ILotto;
  currentLotto: ILotto;
  numbersData: ILottoNumber[];
  orderedDraws: ILottoDraw[];
  limitValue: number;
  showDays: number;
  boosterBall: boolean = false;
  favourite: boolean;
  weeks: ILottoNumber[];
  ballSelected: ILottoNumber[];
  luckyDipArr: number[];
  numbersSelected: ILottoNumberMap;
  selected: number;
  ballPicks: number[];
  selectionName: string;
  lotteryPrice: ILottoPrice[];
  prices: ILottoPrice;
  accumulatorPrices: string;
  numberData: ILottoNumber[];
  numberDataList: ILottoNumber[][] = [];
  potentialReturns: ILottoPrice[];
  activeMenuItem: { uri: string; };
  private isDone: boolean = false;
  days: number;
  hours: number;
  minutes: number;
  timeInterval;
  isLinesummary: boolean = true;
  lottoData: Subscription;
  maxLineWrapper: boolean;
  draws: ILottoDraw[];
  accumulatorAmount: number | any;
  sortedDateWiseKeys: string[];
  dateWiseDraws: {};
  datePipe: DatePipe;
  currentLottoname: string;
  currentLottoData: object | any;
  singleData: ILottoCmsPage;
  isBrandLadbrokes: boolean;
  lotto = LOTTO_TEMPLATES;
  
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private lottoService: MainLottoService,
    private storage: StorageService,
    private filterService: FiltersService,
    private device: DeviceService,
    private command: CommandService,
    protected infoDialogService: InfoDialogService,
    protected user: UserService,
    private fracToDecService: FracToDecService,
    protected pubSubService: PubSubService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private dialogService: DialogService,
    private segmentDataUpdateService: SegmentDataUpdateService,
    private locale: LocaleService,
    private changeDetectorRef: ChangeDetectorRef,
    private windowRef: WindowRefService,
    private timeService: TimeService) {
  }

  ngOnInit(): void {
    this.singleData = this.lottoService.getLottoDialog();
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.weeks = [
      { value: 1, selected: true },
      { value: 2, selected: false },
      { value: 3, selected: false },
      { value: 4, selected: false }
    ];
    this.route.params.pipe(
      concatMap((params) => {
        return this.lottoService.getLotteryData(params.lottery);
      }))
      .subscribe((lottoData: ILotto) => {
        if (!lottoData || !lottoData.uri) {
          this.router.navigate(['/404']);
        } else {
          this.lotteryData = lottoData;
          this.init()
        }
      }, () => {
      });

    this.pubSubService.subscribe('LinesummaryComponent', 'LOTTO_BET_PLACED', () => {
      this.orderedDraws.forEach((draw) => draw.checked = false);
      this.linesSummary.forEach(line => line.isBonusBall = false);
      this.weeks.forEach((week, ind) => week.selected = ind === 0 ? true : false);
    });
  }

  isWeeksSelected() {
   return this.weeks.some(res => res.selected);
  }
  setHeaderData(): void {
    if(!this.segmentDataUpdateService.headerTime) {
      this.router.navigate(['/lotto']);
      return;
    }
    this.currentLottoData = this.segmentDataUpdateService.headerTime;
    this.days = this.currentLottoData.days;
    this.hours = this.currentLottoData.hours;
    this.minutes = this.currentLottoData.minutes;
    this.currentLottoname = this.singleData.label;
  }
  init() {
    this.setHeaderData();
    this.showDays = 7;
    this.activeMenuItem = { uri: null };
    this.boosterBall = false;
    this.linesSummary = [];
    this.luckyDipArr = [3, 4, 5];
    if (this.lotteryData) {
      this.setLotto(this.lotteryData);

    }
  }
  setLotto(data): void {
    this.boosterBall = data.boosterBall;
    this.currentLotto = data;
    this.currentLottery = data.normal;
    this.numbersData = this.storage.get(this.currentLotto.name);
    this.linesSummary.push({ numbersData: this.numbersData, isBonusBall: false, isFavourite: false });

    this.numberData = _.chain(this.currentLottery.maxNumber)
      .range()
      .map(num => ({
        value: num + 1,
        selected: false,
        disabled: false
      }))

      .value();
    this.selected = 0;
    this.numberData = _.values(_.extend(
      _.indexBy(this.numberData, 'value'), _.indexBy(this.numbersData, 'value')

    ));
    this.numberDataList[0] = this.numberData;
    this.disabledBalls();
    this.lotteryPrice = this.currentLottery.lotteryPrice;
    this.potentialReturns = [...new Map(this.lotteryPrice.map((item) => [item.numberCorrect, item])).values()];
    this.currentLotto.shutAtTime = this.lottoService.getShutAtTime(this.currentLottery);
    this.activeMenuItem.uri = this.currentLotto.uri;
    this.setBallNumbers();
    this.drawsShow(this.showDays);
    this.updateDraws();
  }
  changeFavourite(id: number, event: any) {
    this.linesSummary[id].isFavourite = event.currentTarget.checked;
  }

  updateDraws(): void {
    this.draws = this.orderedDraws.filter((draw) => draw.checked);
  }

  openLottoInfoDialog(): void {
    if (!this.device.isOnline()) {
      this.infoDialogService.openConnectionLostPopup();
    } else {
      this.dialogService.openDialog(
        DialogService.API.lottoInfoDialog, this.componentFactoryResolver.resolveComponentFactory(LottoInfoDialogComponent),
        true, {
          info: this.singleData.infoMessage, label: this.singleData.label, helpLink: this.singleData.nextLink,
      }
      );
    }
  }

  drawsShow(days: number): void {
    this.currentLotto = this.lotteryData;
    const date = new Date();
    const lastDay = date.setDate(date.getDate() + days);
    const limitArray = _.each(this.filterService.orderBy(this.currentLottery.draw, ['drawAtTime', 'description']), (draw: ILottoDraw) => {
      draw.checked = false;
    });
    this.orderedDraws = [];
    _.each(limitArray, (draw: ILottoDraw) => {
      if (Date.parse(draw.shutAtTime) > Date.now() && Date.parse(draw.shutAtTime) < lastDay) {
        this.orderedDraws.push(draw);
      }
    });

    if (this.orderedDraws && this.orderedDraws.length) {
      const drawsObj = {};
      _.each([...this.orderedDraws], (draw: ILottoDraw) => {

        const localeDateString = new Date(draw.drawAtTime).toLocaleDateString();
        if (drawsObj.hasOwnProperty(localeDateString)) {
          drawsObj[localeDateString].draws.push(draw);
        } else {
          drawsObj[localeDateString] = {
            drawDate: draw.drawAtTime,
            draws: [draw]
          }
        }
      });
      this.dateWiseDraws = drawsObj;
      this.sortedDateWiseKeys = Object.keys(this.dateWiseDraws).sort((a: any, b: any) => a - b);
    }

    this.limitValue = this.currentLottery.limits ? this.currentLottery.limits : this.orderedDraws.length;
  }


  createLine() {
    this.linesSummary && this.linesSummary.length <= 19 ? this.linesSummary.push({ numbersData: this.numbersData, isBonusBall: false, isFavourite: false })
    : this.maxLineWrapper = true;
    this.numberDataList[this.linesSummary.length - 1] = this.numberData;
  }
  resetSelected(num: number): void {
    this.selected = num;
  }
  doneSelectedCreateNewLine(): void {
    const numbersDataSelected = _.where(this.numberData, { selected: true });
    this.numbersData = numbersDataSelected;
    this.createLine();
    this.changeDetectorRef.detectChanges();

  }
  numDialog(): void {
    this.numberData = _.chain(this.currentLottery.maxNumber)
      .range()
      .map(num => ({
        value: num + 1,
        selected: false,
        disabled: false
      }))
      .value();
    this.selected = 0;
    const selectedBackup: number = this.selected;
    this.openNumberDailog(selectedBackup);
  }
  luckyDip(value: number, id?: number): void {

    if (id === undefined || this.selected < 5) {
      this.ballSelected = [];

    }
    _.each(this.numberData, num => {
      num.selected = false;
    });

    this.ballSelected = _.each(_.sample(this.numberData, value), num => {

      num.selected = true;

    }) as ILottoNumber[];
    this.numberData = _.values(_.extend(
      _.indexBy(this.numberData, 'value'), _.indexBy(this.ballSelected, 'value')
    ));
    this.disabledBalls();

    this.segmentDataUpdateService.changes.next({
      numbersSelected: this.ballSelected,
      numbersData: this.numberData,
      selected: value
    });

  }
  setSelectedBallNumbers(data: ILottoNumberMap, id?: number): void {
    this.numbersSelected = this.storage.get(this.lotteryData.name) || [];
       _.each(_.range(this.currentLottery.maxPicks), (num, i) => {
      const dataValue = data[num] && data[num].value;
      this.numbersSelected[i] = {
        value: dataValue || '-',
        selected: _.isNumber(dataValue),
        disabled: false
      };
    });
  }

  editLine(id: number) {
    this.setBallNumbers(id);
    this.selected = this.linesSummary[id].numbersData.length;
    this.openNumberDailog(this.selected, id)

  }

  openNumberDailog(selectedBackup: number, id?: number) {
    let openData = [];
    const selectedBallNumber = [];
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(LottoNumberSelectorComponent);
    if (id === undefined) {
      openData = this.numberData
    }

    else {
      openData = this.numberDataList[id]
      this.ballSelected = this.linesSummary[id].numbersData;
      this.linesSummary[id].numbersData.forEach((line) => { selectedBallNumber.push(line.value);})
    }
    this.numberData = openData;

    this.storage.set('IsChooseNumber', 'True');
    this.dialogService.openDialog(
      DialogService.API.lottoNumberSelector,
      componentFactory,
      true,
      {
        numbersData: openData,
        luckyDipArr: this.luckyDipArr,
        selected: this.selected,
        lineSummary: this.linesSummary,
        selectNumbers: (value, index) => {
          this.selectNumbers({ value, index }, id);
        },

        luckyDip: (val) => {
          this.luckyDip(val, id);

        },
        resetNumbers: () => {
          this.resetNumbers(id);

        },
        doneSelected: () => {
          this.isDone = true;
          if (id === undefined) {
            this.doneSelectedCreateNewLine();
          }

          else {
            this.doneSelected(id)
          }

        },

        onBeforeClose: () => {
          if (!this.isDone) {
            this.resetSelected(selectedBackup);
            if (id === undefined) {
              openData = this.numberData
            } else {
              this.numberDataList[id].forEach(ball => {
                if (!selectedBallNumber.includes(ball.value)) {
                  ball.selected = false; ball.disabled = false;
                  ball.disabled =  this.selected === Number(this.currentLottery.maxPicks);       
                } else {
                  ball.selected = true; ball.disabled = false;
                }
              });
            }
          }
          this.isDone = false;
        }
      }
    );
  }

  doneSelected(id?: number): void {
    const numbersDataSelected = _.where(this.numberData, { selected: true });
    this.storage.set(this.currentLotto.name, numbersDataSelected);
    this.setSelectedBallNumbers(numbersDataSelected);
    this.numbersData = numbersDataSelected;
    this.changeDetectorRef.detectChanges();
    this.updateLinesData(id);
  }
  updateLinesData(id: number) {
    this.linesSummary[id].numbersData = this.numbersData;
  }
  selectNumbers(val, id?: number): void {

    if (this.numberData[val.index].selected) {
      _.each(this.numberData, num => {
        num.disabled = false;

      });
    } else if (this.selected && +this.selected >= this.currentLottery.maxPicks) {
      return;
    }
    this.numbersSelected = [];
    this.numberData[val.index].selected = !this.numberData[val.index].selected;
    this.disabledBalls();
    this.segmentDataUpdateService.changes.next({
      numbersSelected: this.numbersSelected,
      numbersData: this.numberData,
      selected: this.selected

    });
  }

  resetNumbers(id:number): void {
    if (id === undefined) {
      this.ballSelected = [];
      this.storage.remove(this.currentLotto.name);
      this.setBallNumbers();
      this.selected = 0;
    } else {
      const numbersDataSelected = this.numberDataList[id].filter((ball) => ball.selected === true);
      if (this.selected === Number(this.currentLottery.maxPicks)) {
        this.numberDataList[id].forEach((ball) => {
          ball.selected = false; ball.disabled = false; this.selected = 0;
        });
      }
      numbersDataSelected.forEach((ball) => {
        ball.selected = false; ball.disabled = false;
      });
    }
    this.segmentDataUpdateService.changes.next({
      numbersSelected: this.numbersSelected,
      numbersData: this.numberData,
      selected: this.selected
    });
  }

  selectDraw(draw: ILottoDraw) {
    draw.checked = draw.checked ? false : true;
    this.updateDraws();
  }

  removeLine(index: number) {
    this.numberDataList.splice(index,  1);
    this.linesSummary.splice(index, 1);
    this.maxLineWrapper = this.linesSummary.length > 19;

    if(this.linesSummary.length === 0){
      this.router.navigate(['/lotto']);
    }
  }

  selectWeek(index: number) {
    this.weeks.forEach(p => {
      p.selected = false;
    });
    this.weeks[index].selected = true;
  }

  addToBetslip(): void {
    const betsList = [];
    this.linesSummary.forEach((line, index) => {
      this.draws.forEach(draw => {
        betsList.push(this.getBetObject(index, draw, line.isBonusBall));
      });
    });
    const selectedWeek = Number(this.weeks.find(res => res.selected).value);
    if(selectedWeek) {
      // initialized i=2 to get next week draw details i=1 already exists
      for (let i = 2; i <= selectedWeek; i++) { 
          betsList.forEach(list => {
            // next n weeks array of current selected draw time;
            const filteredDrawDates = this.drawsFromSelectedWeeks(i, list.draws[0]); 
            if (filteredDrawDates && filteredDrawDates.length) {
              list.draws = [...list.draws, ...filteredDrawDates];
            }
          });
      }
    }

    if (this.device.isOnline()) {
      const shouldAddToBetslip = this.draws.length;
      if (shouldAddToBetslip) {
        this.scrollToTop();
        this.addLinesToBetSlip([...betsList]);
      }
    } else {
      this.infoDialogService.openConnectionLostPopup();
    }
  }

  scrollToTop() {
    this.windowRef.document.body.scrollTop = 0; // For Safari
    this.windowRef.document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }

  drawsFromSelectedWeeks(i, draw) {
    let selectedDrawDate = new Date(draw.drawAtTime);
    selectedDrawDate = new Date(selectedDrawDate.setDate(selectedDrawDate.getDate() + (7 * (i - 1))));
    return this.currentLottery.draw &&this.currentLottery.draw.length && this.currentLottery.draw.filter(currentDraw => {
      const currentDrawDate = new Date(currentDraw.drawAtTime).toLocaleDateString();
      return currentDrawDate == selectedDrawDate.toLocaleDateString() && currentDraw.description.toLowerCase() == draw.description.toLowerCase();
    });
  }

  addLinesToBetSlip(betsList) {
    betsList = betsList.map(bet => {
      return { isLotto: true, data: bet, goToBetslip: true,type: 'SGL' }
    });
    this.pubSubService.publish(this.pubSubService.API.ADD_TO_BETSLIP_BY_SELECTION, [
      betsList
    ]);
  }
  
  getBetObject(ind, draw, isBoosterBall): ILottoPlaceBetObj | any {
    const drawObj = isBoosterBall ? this.replaceDrawWithBoosterDraw(draw) : draw;
    const priceId = isBoosterBall && drawObj ? this.currentLotto.boosterBall.sort : this.currentLotto.normal.sort;
    const name = isBoosterBall && drawObj ? this.currentLotto.boosterBall.name : this.currentLotto.normal.name; // lottery name
    return {
      name: this.capitalizeText(name),
      priceId: priceId.slice(0,2) + (isBoosterBall && drawObj ? '|B' : ''),
      selectionName: 'SGL',
      selections: this.getSelected(ind).ballPicks.join('|'), // '1|3|5' ball selections
      draws: [this.lineSummaryDrawHandler(drawObj, draw)], // object with draw data
      multiplier: 1,
      odds: this.setAccumulatorPrices(isBoosterBall && drawObj).prices,
      currency: this.user.currency,  // 'GBP'
      frequency: this.weeks.find(res => res.selected).value.toString(),
      maxPayOut: this.singleData.maxPayOut
    };
  }

/*
  * @params{boosterDraw} 
  * @params{draw} 
  * boosterDraw, draw contains two objects with booster ball data and normal data.
*/

  lineSummaryDrawHandler(boosterDraw: ILotto, draw: ILotto): ILotto {
    const drawObj = boosterDraw ?? draw;
    drawObj.description = this.capitalizeText(drawObj.description);
    return drawObj;
  }

  capitalizeText(value: string): string {
    if (value) {
      let nameArray = value.split(/\s+/);
      const pattern = /[a-zA-Z0-9]+/;
      nameArray = nameArray.map((name) => {
        if (pattern.test(name[0])) {
          return name[0].toUpperCase() + name.substr(1).toLowerCase();
        } else {
          const charactersArray = name.split("");
          for (let i = 0; i < charactersArray.length; i++) {
            if (pattern.test(charactersArray[i])) {
              charactersArray[i] = charactersArray[i].toUpperCase();
              break;
            }
          }
          return charactersArray.join("");
        }
      });
      return nameArray.join(" ");
    }
    return value;
  }

  getSelected(ind): { selectionName: string, ballPicks: number[] } {
    const sglArray = ['SGL', 'DBL', 'TBL', 'ACC4', 'ACC5'];
    const ballPicks = _.without(_.map((this.linesSummary[ind].numbersData), num => num.value), '-') as number[];
    const selectionName = sglArray[ballPicks.length - 1];
    return { selectionName: selectionName, ballPicks: ballPicks };
  }

  replaceDrawWithBoosterDraw(draw) {
    return this.currentLotto.boosterBall.draw.find(res => {
      return res.description.toLowerCase() === draw.description.toLowerCase() && 
      new Date(res.drawAtTime).toLocaleDateString() === new Date(draw.drawAtTime).toLocaleDateString();
    });
  }
  /**
 * Set accumulator for prices
 */
  setAccumulatorPrices(isBoosterBall) {
    const lottoPrice = isBoosterBall ? this.currentLotto.boosterBall.lotteryPrice : this.currentLotto.normal.lotteryPrice;
    if (lottoPrice.length) {
      const prices = lottoPrice.filter((price: ILottoPrice) => {
        return price.numberPicks === price.numberCorrect;
      });
      return { prices: prices };
    }
    return;
  }

  setBallNumbers(id?: number): void {
     this.ballSelected = this.storage.get(this.currentLotto.name) || [];
    this.numberData = [];

    this.numberData = _.chain(this.currentLottery.maxNumber).range().map(num => ({
      value: num + 1,
      selected: false,
      disabled: false
    })).value();

    if (this.ballSelected.length) {
      this.selected = this.ballSelected.length;
      this.numberData = _.values(_.extend(
        _.indexBy(this.numberData, 'value'), _.indexBy(this.ballSelected, 'value')
      ));
      this.disabledBalls();
    }
    this.setSelectedBallNumbers(this.ballSelected, id);
  }

  disabledBalls(): void {
    this.selected = _.where(this.numberData, { selected: true }).length;
    _.each(this.numberData, num => {
      num.disabled = !num.selected && this.selected === Number(this.currentLottery.maxPicks);
    });
  }

  closeMaxLinesWrapper(): void {
    this.maxLineWrapper = false;
  }

  get selectAll() {
    let status = true;
    Object.keys(this.dateWiseDraws).forEach(key => {
      const hasUnChecked = this.dateWiseDraws[key].draws.some(item => !!item.checked === false);
      if(hasUnChecked) {
        status = false;
      }
    });
    return status;
  }

  handleSelectAll() {
    const status = this.selectAll;
    if (this.dateWiseDraws) {
      Object.keys(this.dateWiseDraws).forEach(key => {
        this.dateWiseDraws[key].draws.forEach(item => {
          item.checked = !status;
        });
      });
      this.updateDraws();
    }
  }

  getUTCHoursAndMinutes(dateStr) {
    const date = new Date(dateStr);
    return this.prependZero(date.getHours().toString()) + ":" + this.prependZero(date.getMinutes().toString());
  }

  prependZero(val) {
    return val.length > 1 ? val : '0'+val;
  }
}
