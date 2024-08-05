import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CreateRacingEdpMarketComponent } from './create-racing-edp-market/create-racing-edp-market.component';
import { EditRacingEdpMarketComponent } from './edit-racing-edp-market/edit-racing-edp-market.component';
import { RacingEdpListComponent } from './racing-edp-list/racing-edp-list.component';
import { RacingEdpMarketsRoutingModule } from './racing-edp-markets-routing.module';

@NgModule({
  declarations: [CreateRacingEdpMarketComponent,
    EditRacingEdpMarketComponent,
    RacingEdpListComponent],
  imports: [
    CommonModule,
    SharedModule,
    ReactiveFormsModule,
    FormsModule,
    RacingEdpMarketsRoutingModule
  ]
})
export class RacingEdpMarketsModule { }
