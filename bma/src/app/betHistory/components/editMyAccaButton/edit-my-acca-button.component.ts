import { Component, Input } from '@angular/core';

import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import { CashoutPanelService } from '@app/betHistory/components/cashoutPanel/cashout-panel.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';

@Component({
  selector: 'edit-my-acca-button',
  templateUrl: './edit-my-acca-button.component.html',
  styleUrls: ['./edit-my-acca-button.component.scss']
})
export class EditMyAccaButtonComponent {
  @Input() bet: IBetHistoryBet;
  @Input() gtmLocation: string;

  tooltipSeen: boolean;

  constructor(
    private editMyAccaService: EditMyAccaService,
    private cashoutPanelService: CashoutPanelService,
    private userService: UserService,
    private storageService: StorageService,
    private serviceClosureService: ServiceClosureService
  ) {
    this.isTooltipSeen();
  }

  getButtonLabel(): string {
    return this.bet.isAccaEdit ? 'ema.cancel' : 'ema.editMyBet';
  }

  toggleBetEdit(): void {
    this.bet.resetCashoutSuccessState();
    this.editMyAccaService.cancelActiveEdit(this.bet);
    this.editMyAccaService.unsavedAcca = null;

    if (this.bet.isPartialActive) {
      this.cashoutPanelService.setPartialState(<any>this.bet, false);
    }

    this.editMyAccaService.toggleBetEdit(this.bet, this.gtmLocation);

    if (this.bet.isAccaEdit) {
      this.editMyAccaService.unsavedAcca = this.bet;
    }

   this.editMyAccaService.removeSavedAcca(this.bet.betId.toString());
  }

  isEditButtonDisabled(): boolean {
    return (!this.bet.isAccaEdit && this.editMyAccaService.hasSuspendedLegs(this.bet)) ||
      (!this.bet.isAccaEdit && this.bet.cashoutValue as string === 'CASHOUT_SELN_SUSPENDED') ||
      (this.bet.inProgress && this.bet.isPartialActive) || this.serviceClosureService.userServiceClosureOrPlayBreak ||
      this.editMyAccaService.isEmaInProcess;
  }

  private isTooltipSeen(): void {
    const tooltipData = this.storageService.get('tooltipsSeen') || {};
    this.tooltipSeen = !!tooltipData[`editMyAccaTooltipSeen-${this.userService.username}`];
    tooltipData[`editMyAccaTooltipSeen-${this.userService.username}`] = true;
    this.storageService.set('tooltipsSeen', tooltipData);
  }
}
