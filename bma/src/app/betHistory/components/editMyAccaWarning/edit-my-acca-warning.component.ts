import { Component, Input } from '@angular/core';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';

@Component({
  selector: 'edit-my-acca-warning',
  templateUrl: './edit-my-acca-warning.component.html',
  styleUrls: ['./edit-my-acca-warning.component.scss']
})
export class EditMyAccaWarningComponent {
  @Input() bet: IBetHistoryBet;

  constructor(private editMyAccaService: EditMyAccaService) {}

  getMessage(): string {
    if (this.editMyAccaService.hasLegsWithLostStatus(this.bet)) {
      return 'ema.noActiveWarning';
    }

    return this.editMyAccaService.hasSuspendedLegs(this.bet) ? 'ema.suspensionWarning' : 'ema.editWarning';
  }
}
