import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { PromotionDetailsComponent } from '@promotions/components/promotionDetails/promotion-details.component';
import { RetailPromotionsPageComponent } from '@promotions/components/retailPromotionsPage/retail-promotions-page.component';
import { PromotionsRoutingModule } from './promotionsl-routing.module';
import { PromotionConfirmDialogComponent } from '@promotions/components/promotionConfirmDialog/promotion-confirm-dialog.component';
// Overridden
import {
  DesktopRetailPromotionsPageComponent
} from '@coralDesktop/promotions/components/retailPromotionsPage/retail-promotions-page.component';
import {
  DesktopSinglePromotionPageComponent
} from '@coralDesktop/promotions/components/singlePromotionPage/single-promotion-page.component';
import { DesktopAllPromotionsPageComponent } from '@coralDesktop/promotions/components/allPromotionsPage/all-promotions-page.component';
import { DesktopModule } from '@desktopModule/desktop.module';
import { PromotionsNavigationService } from '@promotions/services/promotions/promotions-navigation.service';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule,

    PromotionsRoutingModule
  ],
  exports: [
    PromotionDetailsComponent,
    PromotionConfirmDialogComponent
  ],
  declarations: [
    RetailPromotionsPageComponent,
    PromotionDetailsComponent,
    PromotionConfirmDialogComponent,

    // Overridden
    DesktopRetailPromotionsPageComponent,
    DesktopAllPromotionsPageComponent,
    DesktopSinglePromotionPageComponent
  ],
  schemas: [
    NO_ERRORS_SCHEMA
  ],
  providers: [
    PromotionsNavigationService
  ]
})
export class PromotionsModule {}
