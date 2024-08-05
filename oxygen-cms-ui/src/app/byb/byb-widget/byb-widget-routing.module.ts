import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BybWidgetComponent } from './BYB-Widget/byb-widget.component';

const BybWidgetRoutes: Routes = [
  {
    path: '',
    component: BybWidgetComponent,
    // children: []
  },
];

@NgModule({
  imports: [
    RouterModule.forChild(BybWidgetRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class BybWidgetRoutingModule { }
