import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BetslipMainComponent } from './betslip/betslip-main.component';
import { BetslipAccaInsuranceEditComponent } from './betslip-acca-insurance-edit/betslip-acca-insurance-edit.component';
import { BetslipOddsBoostEditComponent } from './betslip-odds-boost-edit/betslip-odds-boost-edit.component';

const routes: Routes = [
  {
    path: '',
    component: BetslipMainComponent,
    children: []
  },
  {
    path: 'betslip-acca-insurance',
    component: BetslipAccaInsuranceEditComponent,
    children: []
  },
  {
    path: 'betslip-odds-boost',
    component: BetslipOddsBoostEditComponent,
    children: []
  },

];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class BetSlipRoutingModule { }
