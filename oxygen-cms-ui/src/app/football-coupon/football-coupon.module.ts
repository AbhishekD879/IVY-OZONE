import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';

import { FootballCouponRoutingModule } from './football-coupon-routing.module';
import { CouponSegmentListComponent } from './coupon-segment-list/coupon-segment-list.component';
import { CouponSegmentComponent } from './coupon-segment/coupon-segment.component';
import { MarketSelectorListComponent } from '@app/football-coupon/market-selector-list/market-selector-list.component';
import { MarketSelectorEditComponent } from '@app/football-coupon/market-selector-edit/market-selector-edit.component';
import { MarketSelectorCreateComponent } from '@app/football-coupon/market-selector-create/market-selector-create.component';
import { CouponMarketMappingListComponent } from './coupon-market-mapping/coupon-market-mapping-list/coupon-market-mapping-list.component';
import { CouponMarketMappingCreateComponent } from './coupon-market-mapping/coupon-market-mapping-create/coupon-market-mapping-create.component';
import { CouponMarketMappingEditComponent } from './coupon-market-mapping/coupon-market-mapping-edit/coupon-market-mapping-edit.component';

@NgModule({
  imports: [
    SharedModule,
    FootballCouponRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    CouponSegmentListComponent,
    CouponSegmentComponent,
    MarketSelectorListComponent,
    MarketSelectorEditComponent,
    MarketSelectorCreateComponent,
    CouponMarketMappingListComponent,
    CouponMarketMappingCreateComponent,
    CouponMarketMappingEditComponent
  ]
})
export class FootballCouponModule { }
