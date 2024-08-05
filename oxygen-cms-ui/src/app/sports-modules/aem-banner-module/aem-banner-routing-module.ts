import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {
  AemBannerComponent
} from '@app/sports-modules/aem-banner-module/editor/aem-banner.component';



const routes: Routes = [
  {
    path: ':moduleId',
    component: AemBannerComponent,
    children: []
  },

];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class AemBannerRoutingModule { }
