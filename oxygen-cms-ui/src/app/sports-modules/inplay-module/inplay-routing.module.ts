import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InplaySportEditComponent } from './inplay-sport-edit/inplay-sport-edit.component';
import {InplayModuleComponent} from './module-page/inplay-module.component';


const routes: Routes = [
  {
    path: ':moduleId',
    component: InplayModuleComponent,
    children: []
  },
  {
    path: ':moduleId/:linkId',
    component: InplaySportEditComponent,
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
export class InplayRoutingModule { }
