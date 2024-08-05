import { Component } from '@angular/core';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';

import { IComponentCanDeactivate } from '@app/core/models/component-can-deactivate.model';

@Component({
  selector: 'open-bets-page-wrapper',
  templateUrl: 'open-bets-page-wrapper.component.html'
})
export class OpenBetsPageWrapperComponent implements IComponentCanDeactivate {
  constructor(private editMyAccaService: EditMyAccaService) {}

  canChangeRoute(): boolean {
    return this.editMyAccaService.canChangeRoute();
  }

  onChangeRoute(): void {
    this.editMyAccaService.showEditCancelMessage();
  }
}
