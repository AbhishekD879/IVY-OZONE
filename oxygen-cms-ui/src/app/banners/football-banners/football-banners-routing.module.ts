import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BannersListComponent } from './banners-list/banners-list.component';
import { BannersEditComponent } from './banners-edit/banners-edit.component';

const BannersRoutes: Routes = [
  {
    path: '',
    component: BannersListComponent,
    children: []
  },
  { path: ':id',  component: BannersEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(BannersRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class FootballBannersRoutingModule { }
