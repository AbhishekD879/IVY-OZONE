import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {
  DesktopRetailPromotionsPageComponent
} from '@ladbrokesDesktop/promotions/components/retailPromotionsPage/retail-promotions-page.component';

import { DesktopAllPromotionsPageComponent } from '@ladbrokesDesktop/promotions/components/allPromotionsPage/all-promotions-page.component';
import {
  DesktopSinglePromotionPageComponent
} from '@ladbrokesDesktop/promotions/components/singlePromotionPage/single-promotion-page.component';
import { IRouteData } from '@app/core/models/route-data.model';
import { ILadbrokesRetailConfig } from '@ladbrokesMobile/core/services/cms/models/system-config';
import { RetailFeatureGuard } from '@core/guards/retail-feature-guard.service';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'all'
  },
  {
    path: 'all',
    component: DesktopAllPromotionsPageComponent,
    data: {
      segment: 'promotions'
    }
  },
  {
    path: 'retail',
    component: DesktopRetailPromotionsPageComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'promotionsRetail',
      feature: 'promotions'
    } as IRouteData<ILadbrokesRetailConfig>
  },
  {
    path: 'details/:promoKey',
    component: DesktopSinglePromotionPageComponent,
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
