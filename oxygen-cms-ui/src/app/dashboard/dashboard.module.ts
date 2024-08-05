import { NgModule } from '@angular/core';
import { DashboardListComponent } from './dashboard-list/dashboard-list.component';
import { DashboardViewComponent } from './dashboard-view/dashboard-view.component';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DashboardConfigurationRoutingModule } from './dashboard-configuration-routing.module';

@NgModule({
  imports: [
    DashboardConfigurationRoutingModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    DashboardListComponent,
    DashboardViewComponent
  ]
})
export class DashboardModule { }
