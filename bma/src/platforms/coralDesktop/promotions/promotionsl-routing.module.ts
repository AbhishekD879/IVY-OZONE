import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {
  DesktopRetailPromotionsPageComponent
} from '@coralDesktop/promotions/components/retailPromotionsPage/retail-promotions-page.component';

import { DesktopAllPromotionsPageComponent } from '@coralDesktop/promotions/components/allPromotionsPage/all-promotions-page.component';
import {
  DesktopSinglePromotionPageComponent
} from '@coralDesktop/promotions/components/singlePromotionPage/single-promotion-page.component';
import { IRouteData } from '@app/core/models/route-data.model';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';

export const routes: Routes = [
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
    data: {
      segment: 'promotionsRetail',
      feature: 'promotions'
    } as IRouteData<IRetailConfig>
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
