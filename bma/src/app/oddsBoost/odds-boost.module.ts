import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';


import { SharedModule } from '@sharedModule/shared.module';

import { OddsBoostService } from '@oddsBoost/services/odds-boost.service';
import { OddsBoostRunService } from '@oddsBoost/services/odds-boost-run.service';
import { OddsBoostPriceService } from '@oddsBoost/services/odds-boost-price.service';
import { OddsBoostRoutingModule } from '@oddsBoost/odds-boost-routing.module';

import { OddsBoostButtonComponent } from '@oddsBoost/components/oddsBoostButton/odds-boost-button.component';
import { OddsBoostBetslipHeaderComponent } from '@oddsBoost/components/oddsBoostBetslipHeader/odds-boost-betslip-header.component';
import { OddsBoostPriceComponent } from '@oddsBoost/components/oddsBoostPrice/odds-boost-price.component';
import { OddsBoostPageComponent } from '@oddsBoost/components/oddsBoostPage/odds-boost-page.component';
import { OddsBoostListComponent } from '@oddsBoost/components/oddsBoostList/odds-boost-list.component';
import { OddsBoostInfoIconComponent } from '@oddsBoost/components/odds-boost-info-icon/odds-boost-info-icon.component';
import { OddsBoostUpcomingHeaderComponent } from '@oddsBoost/components/oddsBoostUpcomingHeader/odds-boost-upcoming-header.component';
import {
  OddsBoostCountNotificationComponent
} from '@oddsBoost/components/oddsBoostCountNotification/odds-boost-count-notification.component';

@NgModule({
  imports: [
    SharedModule,

    OddsBoostRoutingModule
  ],
  exports: [OddsBoostPageComponent,OddsBoostListComponent],
  providers: [
    OddsBoostRunService,
    OddsBoostService,
    OddsBoostPriceService
  ],
  declarations: [
    OddsBoostButtonComponent,
    OddsBoostBetslipHeaderComponent,
    OddsBoostPriceComponent,
    OddsBoostPageComponent,
    OddsBoostListComponent,
    OddsBoostInfoIconComponent,
    OddsBoostUpcomingHeaderComponent,
    OddsBoostCountNotificationComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class OddsBoostModule {

  static entry = {
    OddsBoostBetslipHeaderComponent,
    OddsBoostButtonComponent,
    OddsBoostPriceComponent,
    OddsBoostInfoIconComponent,
    OddsBoostCountNotificationComponent
  };

  constructor(private oddsBoostRunService: OddsBoostRunService) {
    this.oddsBoostRunService.run();
  }
}
