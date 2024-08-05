import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EuroLoyaltyDashboardComponent } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euro-loyalty-dashboard.component';
import { SpecialPagesComponent } from '@app/special-pages/special-pages.component';

const specialPagesRoutes: Routes = [
  {
    path: '',
    component: SpecialPagesComponent,
    children: [
      {
        path: '',
        children: [
          { path: 'matchDayRewards',  component: EuroLoyaltyDashboardComponent }
        ]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(specialPagesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class SpecialPagesRoutingModule { }
