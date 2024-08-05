import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StreamAndBetComponent } from './stream-and-bet.component';

const streamAndBetConfigurationRoutes: Routes = [
  {
    path: '',
    component: StreamAndBetComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(streamAndBetConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class StreamAndBetConfigurationRoutingModule { }
