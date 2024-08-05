import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SystemConfigComponent} from '@app/timeline/system-config/system-config.component';

const routes: Routes = [
  {
    path: '',
    component: SystemConfigComponent,
    children: []
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SystemConfigRoutingModule { }
