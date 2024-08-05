import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { InplayMarketSelectorDesktopComponent } from './inplayMarketSelectorDesktop/inplay-market-selector.component';
import { MarketSelectorConfigService } from '@app/shared/components/marketSelector/market-selector-config.service';
import { DesktopMatchesMarketSelectorComponent } from './matchesMarketSelector/matches-market-selector.component';
import { WrappedMarketSelectorComponent } from './wrappedMarketSelector/wrapped-market-selector.component';
@NgModule({
    imports: [SharedModule],
    providers: [MarketSelectorConfigService],
    declarations: [InplayMarketSelectorDesktopComponent, DesktopMatchesMarketSelectorComponent,WrappedMarketSelectorComponent],
    exports: [InplayMarketSelectorDesktopComponent, DesktopMatchesMarketSelectorComponent,WrappedMarketSelectorComponent],
    schemas: [NO_ERRORS_SCHEMA]
})
export class MarketSelectorModule {
    static entry = { DesktopMatchesMarketSelectorComponent, InplayMarketSelectorDesktopComponent,WrappedMarketSelectorComponent };
}
