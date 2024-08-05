import { Component } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';

@Component({
  selector: 'odds-boost-info-icon',
  templateUrl: './odds-boost-info-icon.component.html',
  styleUrls: ['./odds-boost-info-icon.component.scss']
})
export class OddsBoostInfoIconComponent {

  constructor(
    private localeService: LocaleService,
    private infoDialogService: InfoDialogService
  ) {}

  showInfoDialog(): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('oddsboost.infoDialog.title'),
      this.localeService.getString('oddsboost.infoDialog.oddsBoostUnavailable'),
    );
  }

}
