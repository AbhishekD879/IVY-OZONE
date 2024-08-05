import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CouponSegmentListComponent } from './coupon-segment-list/coupon-segment-list.component';
import { CouponSegmentComponent } from './coupon-segment/coupon-segment.component';
import { MarketSelectorEditComponent } from '@app/football-coupon/market-selector-edit/market-selector-edit.component';
import { MarketSelectorCreateComponent } from '@app/football-coupon/market-selector-create/market-selector-create.component';
import { MarketSelectorListComponent } from '@app/football-coupon/market-selector-list/market-selector-list.component';
import { CouponMarketMappingEditComponent } from '@app/football-coupon/coupon-market-mapping/coupon-market-mapping-edit/coupon-market-mapping-edit.component';

const routes: Routes = [
  { path: '',  component: CouponSegmentListComponent },
  { path: 'coupon-segments',  component: CouponSegmentListComponent },
  { path: 'coupon-segments/add',  component: CouponSegmentComponent },
  { path: 'coupon-segments/:id',  component: CouponSegmentComponent },
  { path: 'coupon-market-selectors',  component: MarketSelectorListComponent },
  { path: 'coupon-market-selectors/add',  component: MarketSelectorCreateComponent },
  { path: 'coupon-market-selectors/:id',  component: MarketSelectorEditComponent },
  { path: 'coupon-market-selectors/mapping/:id',  component: CouponMarketMappingEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class FootballCouponRoutingModule { }
