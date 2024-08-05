import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {
  RacingModulePageComponent
} from '@app/sports-modules/racing-module/racing-module-page/racing-module-page.component';

const routes: Routes = [
  {
    path: ':moduleId',
    component: RacingModulePageComponent,
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
export class RacingRoutingModule { }
