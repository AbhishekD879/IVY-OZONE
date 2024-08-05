import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { AutoSeolistComponent} from './auto-seo-list/auto-seo-list.component';

import {SeoPagesListPageComponent} from './seo-list-page/pageComponent/seo.page.component';
import {SingleSeoPageComponent} from './single-seo-page/pageComponent/seo.page.component';

const promotionsRoutes: Routes = [
  {
    path: 'manual',
    component: SeoPagesListPageComponent,
    children: [
   ]
  },{
    path: 'auto',
    component: AutoSeolistComponent,
    children: [

    ]
  },
  { path: 'manual/:id',  component: SingleSeoPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(promotionsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class WidgetsRoutingModule { }
