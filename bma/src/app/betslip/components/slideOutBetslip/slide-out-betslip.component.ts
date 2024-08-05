import { Component, ElementRef, HostListener, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';

import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { UserService } from '@core/services/user/user.service';
import { IFreeBetState } from '@core/services/freeBets/free-bets.model';
import { BetslipService } from '@betslip/services/betslip/betslip.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'slide-out-betslip',
  templateUrl: 'slide-out-betslip.component.html',
  styleUrls: ['slide-out-betslip.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class SlideOutBetslipComponent implements OnInit, OnDestroy {
  betslipLabel: string;
  onReceipt: boolean;
  betslipStatus: boolean;
  successLoginHandler: boolean;
  freeBetsState: IFreeBetState;
  user: UserService;
  isDropDownMenuHidden: boolean = true;
  isBalanceHidden: boolean = true;
  balanceText: string;
  elementRef: ElementRef;

  constructor(
    private freeBetsService: FreeBetsService,
    private nativeBridgeService: NativeBridgeService,
    protected pubSubService: PubSubService,
    protected commandService: CommandService,
    private userService: UserService,
    private betslipService: BetslipService,
    protected router: Router,
    private localeService: LocaleService,
    private deviceService: DeviceService
  ) {

    this.user = this.userService;
    /**
     * Betslip Button Label
     * @type {string}
     */

    this.betslipLabel = 'bs.betslipBtn';

    /**
     * Check if bet receipt active
     * @type {bool}
     */
    this.onReceipt = false;

    /**
     * Check if betslip is empty
     * @type {bool}
     * TEMPORARY FEATURE, WILL BE REMOVED
     */
    this.betslipStatus = this.betslipService.count() > 0;

    /**
     * Login context checker
     * @type {bool}
     */
    this.successLoginHandler = false;

    /**
     * Check if free bets are available
     * @return {object}
     */
    this.freeBetsState = this.freeBetsService.getFreeBetsState();
  }

  ngOnInit(): void {
    this.pubSubService.subscribe('slideOutBetslip', this.pubSubService.API['show-slide-out-betslip-false'], (message: string) => {
      if (message !== 'prevent') {
        this.onReceipt = false;
        this.nativeBridgeService.onCloseBetSlip();
      }
    });

    this.pubSubService.subscribe('slideOutBetslip', this.pubSubService.API.BETSLIP_LABEL, (name: string) => {
      this.betslipLabel = name === 'Bet Slip' ? 'bs.betslipBtn' : 'bs.betReceipt';
    });

    /**
     * Change QuickDeposit logic on Bet Receipt section
     */
    this.pubSubService.subscribe('slideOutBetslip', this.pubSubService.API.BET_RECEIPT, () => {
      this.onReceipt = true;
    });

    /**
     * Get betslip selections count
     * TEMPORARY FEATURE, WILL BE REMOVED
     */
    this.commandService.executeAsync(this.commandService.API.BETSLIP_READY, undefined, { betsCount: 0 })
      .then(res => {
        if (res) {
          this.betslipStatus = res.betsCount && res.betsCount > 0;
        }
      });

    this.pubSubService.subscribe('slideOutBetslip', this.pubSubService.API.BETSLIP_COUNTER_UPDATE, (count: number) => {
      this.betslipStatus = count > 0;
    });

    this.pubSubService.subscribe('slideOutBetslip', this.pubSubService.API.BETSLIP_BALANCE_DROPDOWN_HIDE, () => {
      this.isDropDownMenuHidden = true;
    });

    this.pubSubService.subscribe('slideOutBetslip', this.pubSubService.API.REUSE_OUTCOME, () => {
      this.onReceipt = false;
    });

    this.balanceText = this.localeService.getString('bs.balance');
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('slideOutBetslip');
  }

  toggleDropDownMenu(): void {
    if (this.isDropDownMenuHidden && this.deviceService.isWrapper) {
      this.nativeBridgeService.onRightMenuClick();
    }

    this.isDropDownMenuHidden = !this.isDropDownMenuHidden;
  }

  toggleBalance(state: boolean): void {
    this.pubSubService.publish(this.pubSubService.API.USER_BALANCE_SHOW, state);
    this.isDropDownMenuHidden = true;
  }

  /**
   * Click outside the dropdown balance menu close it
   */
  @HostListener('document:mousedown', ['$event', '$event.target'])
  onClick(event: MouseEvent, target: HTMLElement): void {
    if (!target || target['name'] === 'btnBalance' || target.parentElement['name'] === 'btnBalance') {
      return;
    }
    this.isDropDownMenuHidden = true;
  }

  /**
   * Add quick deposit
   * @public
   */
  quickDeposit(): void {
    this.onReceipt = false;
    this.isDropDownMenuHidden = true;
    this.hideSidebar();
    this.router.navigate(['/deposit']);
  }

  protected hideSidebar(): void {
    this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
  }
}
