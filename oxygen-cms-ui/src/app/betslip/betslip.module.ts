import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { BetSlipRoutingModule } from './betslip-routing.module';
import { BetslipMainComponent } from './betslip/betslip-main.component';
import { BetslipOddsBoostEditComponent } from './betslip-odds-boost-edit/betslip-odds-boost-edit.component';
import { BetslipAccaInsuranceEditComponent } from './betslip-acca-insurance-edit/betslip-acca-insurance-edit.component';

 

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BetSlipRoutingModule
  ],
  declarations: [
   BetslipMainComponent,
   BetslipOddsBoostEditComponent,
   BetslipAccaInsuranceEditComponent
  ],
   providers: [],
     
  entryComponents: [
    BetslipMainComponent,
    BetslipOddsBoostEditComponent,
    BetslipAccaInsuranceEditComponent
  ]
})
export class BetslipModule { }
