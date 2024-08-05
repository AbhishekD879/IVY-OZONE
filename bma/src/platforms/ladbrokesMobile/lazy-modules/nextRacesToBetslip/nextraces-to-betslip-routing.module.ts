import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NextRacesToBetslipComponent } from './components/nextraces-to-betslip.component';

const routes: Routes = [
  {
    path: '',
    component: NextRacesToBetslipComponent,
    data: {
      segment: 'nextRacesToBetslip'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NextRacesToBetslipRoutingModule { }
