import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {SportBannersListComponent} from './sport-banners-list/banners.list.component';
import {BannerPageComponent} from './sport-banner-edit/banner.page.component';

const BannersRoutes: Routes = [
  {
    path: '',
    component: SportBannersListComponent,
    children: []
  },
  { path: ':id',  component: BannerPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(BannersRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class SportBannersRoutingModule { }
