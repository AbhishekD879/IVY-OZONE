import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { PromotionDetailsComponent } from '@promotions/components/promotionDetails/promotion-details.component';
import { AllPromotionsPageComponent } from '@promotions/components/allPromotionsPage/all-promotions-page.component';
import { RetailPromotionsPageComponent } from '@promotions/components/retailPromotionsPage/retail-promotions-page.component';
import { SinglePromotionPageComponent } from '@promotions/components/singlePromotionPage/single-promotion-page.component';
import { PromotionsRoutingModule } from '@promotions/promotionsl-routing.module';
import { PromotionConfirmDialogComponent } from '@promotions/components/promotionConfirmDialog/promotion-confirm-dialog.component';
import { PromotionsNavigationService } from '@promotions/services/promotions/promotions-navigation.service';


@NgModule({
  imports: [
    SharedModule,

    PromotionsRoutingModule
  ],
  exports: [
    PromotionDetailsComponent,
    PromotionConfirmDialogComponent
  ],
  declarations: [
    AllPromotionsPageComponent,
    RetailPromotionsPageComponent,
    SinglePromotionPageComponent,
    PromotionDetailsComponent,
    PromotionConfirmDialogComponent
  ],
  schemas: [
    NO_ERRORS_SCHEMA
  ],
  providers: [
    PromotionsNavigationService
  ]
})
export class PromotionsModule {}
