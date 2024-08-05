import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';


import { SharedModule } from '@sharedModule/shared.module';
import { FreebetsRoutingModule } from '@freebetsModule/freebets-routing.module';
import { FreebetsComponent } from '@freebetsModule/components/freebets/freebets.component';
import { FreebetDetailsComponent } from '@freebetsModule/components/freebetDetails/freebet-details.component';
import { FreeBetToggleComponent } from '@freebetsModule/components/freeBetToggle/free-bet-toggle.component';
import { FreeBetSelectDialogComponent } from '@freebetsModule/components/freeBetSelectDialog/free-bet-select-dialog.component';
import { LpSpDropdownComponent } from '@freebetsModule/components/lpSpDropdown/lp-sp-dropdown.component';
import { ToteFreeBetsToggleComponent } from '@freebetsModule/components/tote-free-bets-toggle/tote-free-bets-toggle.component';
import { ToteFreeBetSelectDialogComponent } from '@freebetsModule/components/tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';
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
    LpSpDropdownComponent,
    ToteFreeBetsToggleComponent,
    ToteFreeBetSelectDialogComponent
  ],
  exports: [],
  providers: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FreebetsModule {
  static entry = { FreeBetToggleComponent, LpSpDropdownComponent, ToteFreeBetsToggleComponent };
}
