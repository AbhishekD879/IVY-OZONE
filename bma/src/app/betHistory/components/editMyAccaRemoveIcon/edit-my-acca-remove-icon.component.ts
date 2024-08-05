import { Component, Input } from '@angular/core';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { IBetHistoryLeg, IBetHistoryBet } from '@app/betHistory/models/bet-history.model';

@Component({
  selector: 'edit-my-acca-remove-icon',
  templateUrl: './edit-my-acca-remove-icon.component.html',
  styleUrls: ['./edit-my-acca-remove-icon.component.scss']
})
export class EditMyAccaRemoveIconComponent {
  @Input() bet: { eventSource: IBetHistoryBet, location: string };
  @Input() leg: IBetHistoryLeg;

  constructor(private editMyAccaService: EditMyAccaService) {}

  removeLeg(event: MouseEvent): void {
    event.stopPropagation();

    if (!this.removingDisabled()) {
      this.editMyAccaService.removeLeg(this.bet.eventSource, this.leg);
    }
  }

  undoRemoveLeg(event: MouseEvent): void {
    event.stopPropagation();

    if (!this.isUndoDisabled()) {
      this.editMyAccaService.undoRemoveLegs(this.bet.eventSource, [this.leg]);
    }
  }

  removingDisabled(): boolean {
    return !this.editMyAccaService.canRemoveLegs(this.bet.eventSource);
  }

  isUndoDisabled(): boolean {
    return !this.editMyAccaService.canUndoRemoveLegs(this.bet.eventSource);
  }

  isShown(): boolean {
    return !this.leg.removedLeg &&
      !this.editMyAccaService.isLegResulted(this.leg) &&
      !this.editMyAccaService.hasLegsWithLostStatus(this.bet.eventSource) &&
      this.leg.status !== 'suspended';
  }
}
