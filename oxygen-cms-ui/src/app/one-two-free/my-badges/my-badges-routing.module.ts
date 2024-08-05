import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MyBadgesDetailComponent } from './my-badges-detail/my-badges-detail.component';

const mybadgesRoutes: Routes = [
  {
    path: '',
    component: MyBadgesDetailComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(mybadgesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class MyBadgesRoutingModule { }
