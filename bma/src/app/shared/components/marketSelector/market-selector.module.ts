import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { MatchesMarketSelectorComponent } from './matchesMarketSelector/matches-market-selector.component';
import { InplayMarketSelectorComponent } from './inplayMarketSelector/inplay-market-selector.component';
import { MarketSelectorConfigService } from './market-selector-config.service';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
    imports:[SharedModule],
    providers: [MarketSelectorConfigService],
    declarations: [MatchesMarketSelectorComponent,InplayMarketSelectorComponent],
    exports:[MatchesMarketSelectorComponent,InplayMarketSelectorComponent],
    schemas: [NO_ERRORS_SCHEMA]
})
export class MarketSelectorModule {
    static entry = { MatchesMarketSelectorComponent, InplayMarketSelectorComponent };
}
