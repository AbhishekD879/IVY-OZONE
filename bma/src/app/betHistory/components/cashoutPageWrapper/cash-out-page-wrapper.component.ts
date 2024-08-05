import { Component } from '@angular/core';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';

import { IComponentCanDeactivate } from '@app/core/models/component-can-deactivate.model';

@Component({
  selector: 'cash-out-page-wrapper',
  templateUrl: 'cash-out-page-wrapper.component.html'
})
export class CashOutPageWrapperComponent implements IComponentCanDeactivate {
  constructor(private editMyAccaService: EditMyAccaService) {}

  canChangeRoute(): boolean {
    return this.editMyAccaService.canChangeRoute();
  }

  onChangeRoute(): void {
    this.editMyAccaService.showEditCancelMessage();
  }
}
