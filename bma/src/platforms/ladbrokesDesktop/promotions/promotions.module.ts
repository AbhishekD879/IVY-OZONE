import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { PromotionDetailsComponent } from '@promotions/components/promotionDetails/promotion-details.component';
import { PromotionConfirmDialogComponent } from '@promotions/components/promotionConfirmDialog/promotion-confirm-dialog.component';
import { RetailPromotionsPageComponent } from '@promotions/components/retailPromotionsPage/retail-promotions-page.component';
import {
  DesktopRetailPromotionsPageComponent
} from '@ladbrokesDesktop/promotions/components/retailPromotionsPage/retail-promotions-page.component';
import { PromotionsRoutingModule } from './promotionsl-routing.module';

// Overridden
import {
  DesktopSinglePromotionPageComponent
} from '@ladbrokesDesktop/promotions/components/singlePromotionPage/single-promotion-page.component';
import { DesktopAllPromotionsPageComponent } from '@ladbrokesDesktop/promotions/components/allPromotionsPage/all-promotions-page.component';
import { LadbrokesDesktopPromotionsComponent } from '@ladbrokesDesktop/promotions/components/promotion/promotions.component';
import { DesktopModule } from '@desktop/desktop.module';
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
    DesktopSinglePromotionPageComponent,
    LadbrokesDesktopPromotionsComponent
  ],
  schemas: [
    NO_ERRORS_SCHEMA
  ],
  providers: [
    PromotionsNavigationService
  ]
})
export class PromotionsModule {}
