import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AllPromotionsPageComponent } from '@promotions/components/allPromotionsPage/all-promotions-page.component';
import { RetailPromotionsPageComponent } from '@promotions/components/retailPromotionsPage/retail-promotions-page.component';
import { SinglePromotionPageComponent } from '@promotions/components/singlePromotionPage/single-promotion-page.component';
import { RetailFeatureGuard } from '@core/guards/retail-feature-guard.service';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';
import { IRouteData } from '@app/core/models/route-data.model';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'all'
  },
  {
    path: 'all',
    component: AllPromotionsPageComponent,
    data: {
      segment: 'promotions'
    }
  },
  {
    path: 'retail',
    component: RetailPromotionsPageComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'promotionsRetail',
      feature: 'promotions'
    } as IRouteData<IRetailConfig>
  },
  {
    path: 'details/:promoKey',
    component: SinglePromotionPageComponent,
    data: {
      segment: 'promotionsDetail'
    }
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class PromotionsRoutingModule {}
