import { NgModule } from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import { MaintenanceListComponent } from './maintenance-list/maintenance-list.component';
import { MaintenanceEditPageComponent } from './maintenance-edit-page/maintenance-edit-page.component';

const routes: Routes = [
  { path: '',  component: MaintenanceListComponent },
  { path: ':id',  component: MaintenanceEditPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class MaintenanceRoutingModule { }
