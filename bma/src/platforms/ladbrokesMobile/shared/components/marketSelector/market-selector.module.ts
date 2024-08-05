import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { MatchesMarketSelectorComponent } from './matchesMarketSelector/matches-market-selector.component';
import { LadbrokesInplayMarketSelectorComponent } from './inplayMarketSelector/inplay-market-selector.component';
import { MarketSelectorConfigService } from '@app/shared/components/marketSelector/market-selector-config.service';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
    imports:[SharedModule],
    providers: [MarketSelectorConfigService],
    declarations: [MatchesMarketSelectorComponent,LadbrokesInplayMarketSelectorComponent],
    exports:[MatchesMarketSelectorComponent,LadbrokesInplayMarketSelectorComponent],
    schemas: [NO_ERRORS_SCHEMA]
})
export class MarketSelectorModule {
    static entry = { MatchesMarketSelectorComponent,LadbrokesInplayMarketSelectorComponent};
}
