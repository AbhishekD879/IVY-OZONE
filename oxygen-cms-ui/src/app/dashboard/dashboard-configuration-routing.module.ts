import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardListComponent } from './dashboard-list/dashboard-list.component';
import { DashboardViewComponent } from './dashboard-view/dashboard-view.component';

const dashboardConfigurationRoutes: Routes = [
  {
    path: '',
    component: DashboardListComponent
  },
  { path: ':id',  component: DashboardViewComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(dashboardConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class DashboardConfigurationRoutingModule { }
