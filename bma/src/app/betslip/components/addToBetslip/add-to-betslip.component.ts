import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { AddToBetslipByOutcomeIdService } from '@betslip/services/addToBetslip/add-to-betslip-by-outcome-id.service';
import { CommandService } from '@core/services/communication/command/command.service';
import * as _ from 'underscore';

@Component({
  selector: 'add-to-betslip',
  template: '<outlet-status [state]="state"><incorrect-pattern></incorrect-pattern></outlet-status>'
})
export class AddToBetslipComponent extends AbstractOutletComponent implements OnInit {

  constructor(
    private addToBetslipByOutcomeIdService: AddToBetslipByOutcomeIdService,
    private route: ActivatedRoute,
    private commandService: CommandService
  ) {
    super();
  }

  ngOnInit(): void {
    this.commandService.executeAsync(this.commandService.API.BETSLIP_READY)
      .then(() => this.add());
  }

  private add(): void {
    const outcomeId = this.route.snapshot.params['outcomeId'];
    let filteredIds = [];
    this.addToBetslipByOutcomeIdService.isValidOutcome(outcomeId).subscribe((isValidOutcome: boolean) => {
      this.addToBetslipByOutcomeIdService.isValidSelection = isValidOutcome;
      filteredIds = _.uniq(outcomeId.split(','));
      const finalIds = filteredIds.filter((id) => !this.addToBetslipByOutcomeIdService.filteredOutcomeIds.includes(id));
      this.addToBetslipByOutcomeIdService.addToBetSlip(
          finalIds.join(),
          true,
          true,
          true,
        false,
        false,
        true
        )
        .subscribe(() => {
          this.hideSpinner();
        }, () => {
          this.showError();
        });
    })

  }
}
