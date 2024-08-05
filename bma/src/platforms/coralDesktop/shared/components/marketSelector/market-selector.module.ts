import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { MatchesMarketSelectorComponent } from './matchesMarketSelector/matches-market-selector.component';
import { SharedModule } from '@sharedModule/shared.module';
import { InplayMarketSelectorDesktopComponent } from './inplayMarketSelectorDesktop/inplay-market-selector.component';
import { MarketSelectorConfigService } from '@app/shared/components/marketSelector/market-selector-config.service';
import { DesktopMatchesMarketCustomSelectorComponent } from './matchesMarketCustomSelector/matches-market-custom-selector.component';
@NgModule({
    imports:[SharedModule],
    providers:[MarketSelectorConfigService],
    declarations: [MatchesMarketSelectorComponent,InplayMarketSelectorDesktopComponent,DesktopMatchesMarketCustomSelectorComponent],
    exports:[MatchesMarketSelectorComponent,InplayMarketSelectorDesktopComponent,DesktopMatchesMarketCustomSelectorComponent],
    schemas: [NO_ERRORS_SCHEMA]
})
export class MarketSelectorModule {
    static entry = { MatchesMarketSelectorComponent,InplayMarketSelectorDesktopComponent,DesktopMatchesMarketCustomSelectorComponent};
}
