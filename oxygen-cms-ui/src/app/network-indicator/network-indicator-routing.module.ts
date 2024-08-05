import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NetworkIndicatorComponent } from './network-indicator.component';



const NetworkIndicatorRoutes: Routes = [
  {
    path: '',
    component: NetworkIndicatorComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(NetworkIndicatorRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class NetworkIndicatorRoutingModule { }
