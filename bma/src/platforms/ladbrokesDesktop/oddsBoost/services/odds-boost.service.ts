import { Injectable } from '@angular/core';

import {
  DesktopOddsBoostInfoDialogComponent
} from '@ladbrokesDesktop/shared/components/ladbrokesDesktopOddsBoostDialog/odds-boost-info-dialog.component';

import { OddsBoostService as AppOddsBoostService } from '@app/oddsBoost/services/odds-boost.service';

@Injectable()
export class OddsBoostService extends AppOddsBoostService {
  get dialogComponent(): typeof DesktopOddsBoostInfoDialogComponent {
    return DesktopOddsBoostInfoDialogComponent;
  }
  set dialogComponent(value:typeof DesktopOddsBoostInfoDialogComponent){}
}
