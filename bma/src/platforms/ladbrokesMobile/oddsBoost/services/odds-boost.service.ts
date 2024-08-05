import { Injectable } from '@angular/core';

import {
  LadbrokesOddsBoostInfoDialogComponent
} from '@ladbrokesMobile/shared/components/ladbrokesMobileOddsBoostDialog/odds-boost-info-dialog.component';

import { OddsBoostService as AppOddsBoostService } from '@app/oddsBoost/services/odds-boost.service';

@Injectable()
export class OddsBoostService extends AppOddsBoostService {
  get updateCountListeners(): string {
    return 'show-my-account-slide-up';
  }
  set updateCountListeners(value:string){}

  get dialogComponent(): typeof LadbrokesOddsBoostInfoDialogComponent {
    return LadbrokesOddsBoostInfoDialogComponent;
  }
  set dialogComponent(value:typeof LadbrokesOddsBoostInfoDialogComponent){}
}
