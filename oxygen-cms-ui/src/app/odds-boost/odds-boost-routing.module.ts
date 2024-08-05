import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OddsBoostPageComponent } from './odds-boost-page/odds-boost.page.component';

const moduleOddsBoostConfigurationRoutes: Routes = [
  {
    path: '', component: OddsBoostPageComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(moduleOddsBoostConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class OddsBoostRoutingModule {}
