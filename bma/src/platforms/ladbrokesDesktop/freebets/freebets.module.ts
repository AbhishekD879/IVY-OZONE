import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';


import { SharedModule } from '@sharedModule/shared.module';
import { FreeBetToggleComponent } from '@ladbrokesMobile/freebets/components/freeBetToggle/free-bet-toggle.component';
import {
  FreeBetSelectDialogComponent
} from '@ladbrokesMobile/freebets/components/freeBetSelectDialog/free-bet-select-dialog.component';
import { LadbrokesLpSpDropdownComponent } from '@ladbrokesMobile/freebets/components/lpSpDropdown/lp-sp-dropdown.component';
import { FreebetsRoutingModule } from '@freebets/freebets-routing.module';
import { FreebetsComponent } from '@freebetsModule/components/freebets/freebets.component';
import { FreebetDetailsComponent } from '@freebets/components/freebetDetails/freebet-details.component';
import { ToteFreeBetsToggleComponent } from '@ladbrokesMobile/freebets/components/tote-free-bets-toggle/tote-free-bets-toggle.component';
import { ToteFreeBetSelectDialogComponent } from '@ladbrokesMobile/freebets/components/tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';

@NgModule({
  imports: [
    SharedModule,

    FreebetsRoutingModule
  ],
  declarations: [
    FreebetsComponent,
    FreebetDetailsComponent,
    FreeBetToggleComponent,
    FreeBetSelectDialogComponent,
    LadbrokesLpSpDropdownComponent,
    ToteFreeBetsToggleComponent,
    ToteFreeBetSelectDialogComponent
  ],
  exports: [],
  providers: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FreebetsModule {
  static entry = { FreeBetToggleComponent, LadbrokesLpSpDropdownComponent, ToteFreeBetsToggleComponent };
}
