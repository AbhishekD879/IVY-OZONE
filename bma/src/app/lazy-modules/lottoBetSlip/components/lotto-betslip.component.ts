import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';
import { DeviceService } from '@core/services/device/device.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { BetInfoDialogService } from '@app/betslip/services/betInfoDialog/bet-info-dialog.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { BetslipStakeService } from '@betslip/services/betslip/betslip-stake.service';

@Component({
  selector: 'lotto-betslip',
  templateUrl: './lotto-betslip.component.html',
  styleUrls: ['./lotto-betslip.component.scss']
})
export class LottoBetslipComponent implements OnInit {
  @Input() lottobetslipData;
  @Input() betSlipSingles;
  @Output() lottoBetsEmitter: EventEmitter<any> = new EventEmitter<any>();
  @Output() onStakeInput: EventEmitter<any> = new EventEmitter<any>();
  @Output() removeFrombetList: EventEmitter<any> = new EventEmitter<any>();
  @Output() removeErrorMsg: EventEmitter<string> = new EventEmitter();
  lottoStakeInput;
  dsBetsCounter: number = 0;
  changedFromAllStakeField: boolean = false;
  isDidigitKeyboardInit: any = false;
  currencySymbol: string;
  count: number = 0;
  allStakes: { value: string | any } = { value: '' };
  lottoBetsContainerEl: HTMLElement;
  lottoPayoutArray: boolean[][]= [];

  @ViewChild('lottoBetsContainer', { static: false }) set lottoBetsContainer(elementRef: ElementRef) {
    if (elementRef && elementRef.nativeElement) {
      this.lottoBetsContainerEl = elementRef.nativeElement;
    }
  }

  constructor(
    private pubSubService: PubSubService,
    private betslipService: BetslipService,
    private deviceService: DeviceService,
    protected storageService: StorageService,
    private userService: UserService,
    private filterService: FiltersService,
    private betInfoDialogService: BetInfoDialogService,
    private localeService: LocaleService,
    public betSlipStakeService: BetslipStakeService) {
  }

  ngOnInit(): void {
    this.currencySymbol = this.userService.currencySymbol;
    this.betSlipStakeService['checkIndex'](0); // added to reset the maxpay error message in lotto page init
    this.updateBetslipData();
    this.setAmount();
    this.pubSubService.subscribe('betslip data', this.pubSubService.API.ADDTOBETSLIP_PROCESS_FINISHED, () => { this.updateBetslipData() });
  }


  updateBetslipData() {
      this.lottobetslipData && this.lottobetslipData.forEach((data, index) => {
        this.lottoPayoutArray.push([]);
        data.accaBets.forEach(accaBet => {
          if (!accaBet.id) { accaBet.id = data.id + '|' + index }
        });
      });
  }

  onExpandSummary(lottoIndex, event) {
    this.lottobetslipData[lottoIndex].details.draws.expanded = event.currentTarget.innerText.toLowerCase() === 'show summary' ? false : true;
  }

  public trackById(index: number, betslipStake: any) {
    return `${betslipStake.id}_${index}`;
  }


  public trackByDrawId(index: number, draw: any) {
    return `${draw.id}_${index}`;
  }

  onExpandMultiples(lottoIndex, event) {
        this.lottobetslipData[lottoIndex].expanded = event.currentTarget.innerText.toLowerCase() === 'hide multiples' ? false : true
  }

  removeFromBetslip(lottoIndex) {
    this.removeFrombetList.emit(lottoIndex);
  }

  setAmount() {
    if (this.deviceService.isMobileOnly && !this.isDidigitKeyboardInit) {
      return;
    }
    this.changedFromAllStakeField = true;
    this.betSlipSingles.forEach((bet) => {
      this.betslipService.setAmount(bet);
    })
    this.onStakeInput.emit({ lottoData: this.lottobetslipData });
  }

  /*
  * on DidigitKeyboardInput initialized
  */
  onDidigitKeyboardInit(): void {
    this.isDidigitKeyboardInit = true;
  }

  /**
   * Calculate Estimated Returns for Singles
   * @param {number} index
   * @return {string}
   */
  calculateEstReturns(index, multiplesIndex?: number): number | string {
    const betDataObj = this.lottobetslipData[index];
    this.onStakeInput.emit({ lottoData: this.lottobetslipData });
    return this.returnStakeValue(this.calculateReturns(index, betDataObj, multiplesIndex));
  }

  calculateReturns(rowIndex, betData, ind) {
    const empty_stake = 0.00,
    stake = Number(betData.accaBets[ind].stake),
    winningAmt = Number(betData.accaBets[ind].winningAmount),
    lineNumbers = betData.accaBets[ind].lines.number;
    let payoutValue = empty_stake;
    if(stake > 0) {
      const value = (stake * lineNumbers) + (winningAmt * stake);
      const maxPayOut = betData.accaBets[ind].betType == "SGL_S" ? (betData.accaBets[ind].lines.number * betData.details.maxPayOut) : betData.details.maxPayOut;
      this.lottoPayoutArray[rowIndex][ind] = value > maxPayOut ? true : false;
      payoutValue = (this.betSlipStakeService['maxPayoutCheck'](value, maxPayOut));
      payoutValue = payoutValue * betData.details.draws.length.toFixed(2);
    } 
    else {
      this.lottoPayoutArray[rowIndex][ind] = false;
    }
    betData.accaBets[ind].estReturns = payoutValue;
    this.betSlipStakeService.maxFlag = this.lottoPayoutArray.flat().includes(true);
    return payoutValue;
  }

  openSelectionMultiplesDialog(multipleBetslipStake): void {
    this.betInfoDialogService.multiple(multipleBetslipStake.betTypeRef.id, multipleBetslipStake.lines.number);
  }

  getTypeLocale(multipleBetslipStake): string {
    return multipleBetslipStake && this.localeService.getString(`bs.${multipleBetslipStake.betTypeRef.id}`);
  }

  getTypeinfo(multipleBetslipStake) {
    const  typeInfo = multipleBetslipStake && this.localeService.getString(`bs.${multipleBetslipStake.betTypeRef.id}_info`);
    if (typeInfo === 'KEY_NOT_FOUND') {
      return '';
    }
    return typeInfo;
  }

  setFocusMultipleIndex(stake, index, multiplesIndex) {
    this.lottobetslipData[index].accaBets[multiplesIndex].stake = stake;
  }

  trackByAccaBets(index: number, accaBet) {

    return `${accaBet.id}_${index}`;
  }

  returnStakeValue(stake) {
   return this.filterService.setCurrency(stake? stake :'0.00', this.currencySymbol);
  }

  getSelectionTotalEstimate(rowIndex, bet) {
    const accaEstimates = bet && bet.accaBets && bet.accaBets.reduce((sum: number, betType, index) => {
      const accasEstReturns = this.calculateReturns(rowIndex, bet, index);
      if (Number(accasEstReturns) > 0) {
        sum += Number(accasEstReturns);
      } return sum;
    }, 0);
    return this.returnStakeValue(accaEstimates);
  }

  
  clearErrorMessage() {
    this.removeErrorMsg.emit('removeErrorMsg');
  }
  ngAfterViewChecked() {
    if (this.lottoBetsContainerEl) {
      this.lottoBetsEmitter.emit(this.lottoBetsContainerEl);
    }
  }

  ngOnDestroy() {
    this.betSlipStakeService['checkIndex'](0); // added to reset the maxpay error message in lotto page destroy
  }
}