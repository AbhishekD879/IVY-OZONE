import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabNameConfigurationComponent } from './tab-name-configuration.component';

const myTabNameConfigurationRoutes: Routes = [
  {
    path: '',
    component: TabNameConfigurationComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(myTabNameConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class TabNameConfigurationRoutingModule { }
