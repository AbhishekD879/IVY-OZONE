import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';


import { SharedModule } from '@sharedModule/shared.module';

import { OddsBoostService } from './services/odds-boost.service';
import { OddsBoostRunService } from '@oddsBoost/services/odds-boost-run.service';
import { OddsBoostPriceService } from '@oddsBoost/services/odds-boost-price.service';
import { OddsBoostRoutingModule } from '@ladbrokesMobile/oddsBoost/odds-boost-routing.module';

import { LadbrokesOddsBoostButtonComponent } from '@ladbrokesMobile/oddsBoost/components/oddsBoostButton/odds-boost-button.component';
import {
  LadbrokesOddsBoostBetslipHeaderComponent
} from '@ladbrokesMobile/oddsBoost/components/oddsBoostBetslipHeader/odds-boost-betslip-header.component';
import { LadbrokesOddsBoostPriceComponent } from '@ladbrokesMobile/oddsBoost/components/oddsBoostPrice/odds-boost-price.component';
import { OddsBoostInfoIconComponent } from '@oddsBoost/components/odds-boost-info-icon/odds-boost-info-icon.component';
import { OddsBoostUpcomingHeaderComponent } from '@oddsBoost/components/oddsBoostUpcomingHeader/odds-boost-upcoming-header.component';
import {
  OddsBoostCountNotificationComponent
} from '@oddsBoost/components/oddsBoostCountNotification/odds-boost-count-notification.component';
import { MobileOddsBoostPageComponent } from '@ladbrokesMobile/oddsBoost/components/odds-boost-page/odds-boost-page.component';
import { MobileOddsBoostListComponent } from '@ladbrokesMobile/oddsBoost/components/odds-boost-list/odds-boost-list.component';

@NgModule({
  imports: [
    SharedModule,

    OddsBoostRoutingModule
  ],
  exports: [],
  providers: [
    OddsBoostService,
    OddsBoostRunService,
    OddsBoostPriceService
  ],
  declarations: [
    LadbrokesOddsBoostButtonComponent,
    LadbrokesOddsBoostBetslipHeaderComponent,
    LadbrokesOddsBoostPriceComponent,
    MobileOddsBoostPageComponent,
    MobileOddsBoostListComponent,
    OddsBoostInfoIconComponent,
    OddsBoostUpcomingHeaderComponent,
    OddsBoostCountNotificationComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class OddsBoostModule {

  static entry = {
    LadbrokesOddsBoostBetslipHeaderComponent,
    LadbrokesOddsBoostPriceComponent,
    OddsBoostInfoIconComponent
  }
  constructor(private oddsBoostRunService: OddsBoostRunService) {
    this.oddsBoostRunService.run();
  }
}
