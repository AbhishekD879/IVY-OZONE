import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BetpackMarketRoutingModule } from '@coralDesktop/betpackMarket/betpack-market.routing.module';
import { SharedModule } from '@sharedModule/shared.module';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { DesktopBetpackHomepageComponent } from '@coralDesktop/betpackMarket/components/betpackHomePage/betpack-homepage.component';
import { BannersModule } from '@app/lazy-modules/banners/banners.module';
import { BetpackCmsModule } from '@app/lazy-modules/betpackPage/betpack-cms.module';
import { BetpackMarketModule as AppBetpackMarketModule} from '@app/betpackMarket/betpack-market.module';
import { BetpackBannerComponent } from '@app/betpackMarket/components/betpackBanner/betpack-banner.component';

@NgModule({
  imports: [
    BetpackMarketRoutingModule,
    SharedModule,

    BannersModule,
    FormsModule,
    CommonModule,
    BetpackCmsModule,
    AppBetpackMarketModule
  ],
  declarations: [
    DesktopBetpackHomepageComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BetpackMarketModule {
  static entry =  BetpackBannerComponent;
 }