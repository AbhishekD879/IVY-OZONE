import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SportsSurfaceBetsDetailsComponent } from '@app/sports-modules/surface-bets/surface-bets-details/surface-bets-details.component';
import { SurfaceBetModuleComponent } from '@app/sports-modules/surface-bets/surface-bet-module/surface-bet-module.component';

const routes: Routes = [
  {
    path: ':moduleId',
    component: SurfaceBetModuleComponent,
    children: []
  },
  {
    path: ':moduleId/bet/edit/:betId',
    component: SportsSurfaceBetsDetailsComponent,
    children: []
  },
  {
    path: ':moduleId/bet/create',
    component: SportsSurfaceBetsDetailsComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class SportsSurfaceBetsRoutingModule {
}
