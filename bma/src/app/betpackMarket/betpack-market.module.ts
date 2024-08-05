import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BetpackMarketRoutingModule } from '@app/betpackMarket/betpack-market.routing.module';
import { SharedModule } from '@sharedModule/shared.module';
import { BetpackHomepageComponent } from '@app/betpackMarket/components/betpackHomePage/betpack-homepage.component';

import { CommonModule } from '@angular/common';
import { BetPackTabComponent } from '@app/betpackMarket/components/betpack-tab/betpack-tab.component';
import { BetpackCmsModule } from '@app/lazy-modules/betpackPage/betpack-cms.module';
import { BetpackContentPageComponent } from '@app/betpackMarket/components/betpackContentPage/betpack-content-page.component';
import { BetpackCardComponent } from '@app/betpackMarket/components/betpackCard/betpack-card.component';
import { BetpackBannerComponent } from '@app/betpackMarket/components/betpackBanner/betpack-banner.component';
import { BannersModule } from '@app/lazy-modules/banners/banners.module';
import { FormsModule } from '@angular/forms';
import { BetpackFeaturepageComponent } from '@app/betpackMarket/components/betpackFeaturePage/betpack-featurepage.component';
import { BetpackContentComponent } from '@app/betpackMarket/components/betpackContent/betpack-content.component';

@NgModule({
  imports: [
    SharedModule,
    BetpackMarketRoutingModule,
    BetpackCmsModule,
    FormsModule,

    CommonModule,
    BannersModule
  ],
  exports: [
    BetpackHomepageComponent,
    BetpackContentPageComponent,
    BetpackContentComponent,
    BetPackTabComponent,
    BetpackFeaturepageComponent
  ],
  declarations: [
    BetpackHomepageComponent,
    BetpackContentPageComponent,
    BetpackCardComponent,
    BetPackTabComponent,
    BetpackContentComponent,
    BetpackBannerComponent,
    BetpackFeaturepageComponent,
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class BetpackMarketModule {
  static entry = {
    BetpackBannerComponent
  };
}