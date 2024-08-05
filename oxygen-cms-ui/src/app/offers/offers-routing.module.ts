import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { OffersPageComponent } from './offers/offers-list/offers.page.component';
import { OfferPageComponent } from './offers/offer-edit/pageComponent/offer.page.component';
import { OfferModulesPageComponent } from './offers-modules/offers-modules-list/offer-modules.page.component';
import { OfferModulePageComponent } from './offers-modules/offers-module-edit/pageComponent/offer-module.page.component';

const offersRoutes: Routes = [
  {
    path: 'offers',
    component: OffersPageComponent,
    children: [

    ]
  },
  { path: 'offers/:id',  component: OfferPageComponent },
  {
    path: 'offer-modules',
    component: OfferModulesPageComponent,
    children: [

    ]
  },
  { path: 'offer-modules/:id',  component: OfferModulePageComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(offersRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class OffersRoutingModule { }
