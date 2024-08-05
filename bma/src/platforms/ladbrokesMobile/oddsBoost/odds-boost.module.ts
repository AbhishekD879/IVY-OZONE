import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';

import { OddsBoostService } from './services/odds-boost.service';
import { OddsBoostRunService } from '@oddsBoost/services/odds-boost-run.service';
import { OddsBoostPriceService } from '@oddsBoost/services/odds-boost-price.service';
import { OddsBoostRoutingModule } from '@oddsBoostModule/odds-boost-routing.module';

import { LadbrokesOddsBoostButtonComponent } from '@oddsBoostModule/components/oddsBoostButton/odds-boost-button.component';
import {
  LadbrokesOddsBoostBetslipHeaderComponent
} from '@oddsBoostModule/components/oddsBoostBetslipHeader/odds-boost-betslip-header.component';
import { LadbrokesOddsBoostPriceComponent } from '@oddsBoostModule/components/oddsBoostPrice/odds-boost-price.component';
import { MobileOddsBoostPageComponent } from './components/odds-boost-page/odds-boost-page.component';
import { OddsBoostInfoIconComponent } from '@oddsBoost/components/odds-boost-info-icon/odds-boost-info-icon.component';
import { OddsBoostUpcomingHeaderComponent } from '@oddsBoost/components/oddsBoostUpcomingHeader/odds-boost-upcoming-header.component';
import {
  OddsBoostCountNotificationComponent
} from '@oddsBoost/components/oddsBoostCountNotification/odds-boost-count-notification.component';
import { MobileOddsBoostListComponent } from './components/odds-boost-list/odds-boost-list.component';

@NgModule({
  imports: [
    SharedModule,
    OddsBoostRoutingModule
  ],
  exports: [MobileOddsBoostPageComponent,MobileOddsBoostListComponent],
  providers: [
    OddsBoostRunService,
    OddsBoostService,
    OddsBoostPriceService
  ],
  declarations: [
    LadbrokesOddsBoostButtonComponent,
    LadbrokesOddsBoostBetslipHeaderComponent,
    LadbrokesOddsBoostPriceComponent,
    MobileOddsBoostListComponent,
    MobileOddsBoostPageComponent,
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
    LadbrokesOddsBoostButtonComponent,
    OddsBoostInfoIconComponent
  }
  constructor(private oddsBoostRunService: OddsBoostRunService) {
    this.oddsBoostRunService.run();
  }
}
