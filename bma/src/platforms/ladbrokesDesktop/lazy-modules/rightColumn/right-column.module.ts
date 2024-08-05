import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktop/desktop.module';

import {
  RightColumnWidgetComponent
} from '@rightColumnModule/components/rightColumnWidget/right-column-widget.component';
import {
  RightColumnWidgetItemComponent
} from '@rightColumnModule/components/rightColumnWidgetItem/right-column-widget-item.component';
import {
  RightColumnWidgetWrapperComponent
} from '@rightColumnModule/components/rightColumnWidgetWrapper/right-column-widget-wrapper.component';
import { WBetslipComponent } from '@rightColumnModule/components/wBetslip/w-betslip.component';
import { WMatchCentreComponent } from '@rightColumnModule/components/wMatchCentre/w-match-centre.component';
import { WMiniGamesIframeComponent } from '@rightColumnModule/components/wMiniGames/w-mini-games-iframe.component';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule
  ],
  declarations: [
    RightColumnWidgetWrapperComponent,
    RightColumnWidgetComponent,
    RightColumnWidgetItemComponent,
    WBetslipComponent,
    WMatchCentreComponent,
    WMiniGamesIframeComponent
  ],
  providers: [],
  exports: [
    RightColumnWidgetWrapperComponent,
    RightColumnWidgetComponent,
    RightColumnWidgetItemComponent,
    WBetslipComponent,
    WMatchCentreComponent,
    WMiniGamesIframeComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RightColumnModule {
  static entry = RightColumnWidgetWrapperComponent;
}
