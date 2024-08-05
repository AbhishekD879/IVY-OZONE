import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';

import { MaintenanceRoutingModule } from './maintenance-routing.module';
import { MaintenanceListComponent } from './maintenance-list/maintenance-list.component';
import { AddMaintenancePageComponent } from './add-maintenance-page/add-maintenance-page.component';
import { MaintenanceEditPageComponent } from './maintenance-edit-page/maintenance-edit-page.component';

@NgModule({
  imports: [
    SharedModule,
    MaintenanceRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    MaintenanceListComponent,
    MaintenanceEditPageComponent,
    AddMaintenancePageComponent
  ],
  entryComponents: [
    AddMaintenancePageComponent
  ]
})
export class MaintenanceModule { }
