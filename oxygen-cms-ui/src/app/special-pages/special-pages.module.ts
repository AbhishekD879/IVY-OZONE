import {NgModule} from '@angular/core';
import {SharedModule} from '@app/shared/shared.module';
import { SpecialPagesRoutingModule } from '@app/special-pages/special-pages-routing.module';
import { EuroLoyaltyDashboardComponent } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euro-loyalty-dashboard.component';
import { SpecialPagesComponent } from '@app/special-pages/special-pages.component';

@NgModule({
  imports: [
    SharedModule,
    SpecialPagesRoutingModule
  ],
  declarations: [
    SpecialPagesComponent,
    EuroLoyaltyDashboardComponent
  ]
})
export class SpecialPagesModule { }
