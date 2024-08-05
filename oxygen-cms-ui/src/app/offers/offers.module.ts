import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { OffersRoutingModule } from './offers-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { OffersPageComponent } from './offers/offers-list/offers.page.component';
import { OfferPageComponent } from './offers/offer-edit/pageComponent/offer.page.component';
import { OfferCreateComponent } from './offers/offer-create/offer.create.component';
import { OffersAPIService } from './service/offers.api.service';
import { OfferModuleAPIService } from './service/offer-module.api.service';
import { OfferModulesPageComponent } from './offers-modules/offers-modules-list/offer-modules.page.component';
import { OfferModuleCreateComponent } from './offers-modules/offers-module-create/offer-module.create.component';
import { OfferModulePageComponent } from './offers-modules/offers-module-edit/pageComponent/offer-module.page.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    OffersRoutingModule
  ],
  declarations: [
    OffersPageComponent,
    OfferPageComponent,
    OfferCreateComponent,
    OfferModulesPageComponent,
    OfferModuleCreateComponent,
    OfferModulePageComponent
  ],
  providers: [
    OffersAPIService,
    OfferModuleAPIService
  ],
  entryComponents: [
    OfferCreateComponent,
    OfferModuleCreateComponent
  ]
})
export class OffersModule { }
