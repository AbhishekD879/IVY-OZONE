import { NgModule } from "@angular/core";
import { RssRewardsPageComponent } from "./rss-rewards-page/rss-rewards-page.component";
import { RssRewardsRoutingModule } from "./rss-rewards-routing.module";
import { SharedModule } from "../shared/shared.module";
import { RssRewardsApiService } from "./rss-rewards.api.service";
import { BrandService } from "@app/client/private/services/brand.service";

@NgModule({
    declarations: [
        RssRewardsPageComponent
    ],
    imports: [
        RssRewardsRoutingModule,
        SharedModule,
    ],
    exports: [],
    providers: [
        RssRewardsApiService,
        BrandService
    ],
})
export class RssRewardsModule { }