import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {AllSsoPageComponent} from './all-sso-page/pageComponent/all.sso.page.component';
import {SsoPageComponent} from './single-sso-page/pageComponent/sso.page.component';

const ssoPagesRoutes: Routes = [
  {
    path: '',
    component: AllSsoPageComponent,
    children: []
  },
  { path: ':id',  component: SsoPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(ssoPagesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class SsoPagesRoutingModule { }
