import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { VsbrRoutingModule } from '@vsbrModule/vsbr-routing.module';
import { VirtualSportsService } from '@app/vsbr/services/virtual-sports.service';
import { LocalStorageMapperService } from '@app/vsbr/services/local-storage-mapper.service';
import { PanelStateService } from '@app/vsbr/services/panel-state.service';
import { EventProvider } from '@app/vsbr/services/event.provider';
import { VsVideoStreamComponent } from '@app/vsbr/components/vsVideoStream/vs-video-stream.component';
import { VirtualSportClassesComponent } from '@ladbrokesMobile/vsbr/components/virtualSportClasses/virtual-sport-classes.component';
import { VsOddsCardComponent } from '@ladbrokesMobile/vsbr/components/vsOddsCard/vs-odds-card.component';

// Overriden components
import { VirtualSportsPageComponent } from '@ladbrokesDesktop/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { VirtualCarouselMenuComponent } from '@ladbrokesDesktop/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';
import { VirtualSportsMapperService } from '@app/vsbr/services/virtual-sports-mapper.service';
import { VirtualMenuDataService } from '@app/vsbr/services/virtual-menu-data.service';
import {
  VirtualCarouselSubMenuComponent
} from '@ladbrokesDesktop/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component';
import { CountdownHeaderComponent } from '@app/vsbr/components/countdownHeader/countdown-header.component';
import { DesktopVirtualHomePageComponent } from '@ladbrokesDesktop/vsbr/components/virtualHomePage/virtual-home-page.component';
import { RacingFeaturedModule } from '../lazy-modules/racingFeatured/racing-featured.module';
import { DesktopVirtualOtherSports } from '@ladbrokesDesktop/vsbr/components/virtualOtherSports/virtual-other-sports.component';
import { DesktopVirtualFeatureZoneComponent } from '@ladbrokesDesktop/vsbr/components/virtualFeatureZone/virtual-feature-zone.component';
import { DesktopVirtualTopSportsComponent} from '@ladbrokesDesktop/vsbr/components/virtual-top-sports/virtual-top-sports.component'
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { BannersModule } from '@ladbrokesDesktop/lazy-modules/banners/banners.module';


@NgModule({
  declarations: [
    VsVideoStreamComponent,
    CountdownHeaderComponent,
    // Overridden
    VirtualSportsPageComponent,
    VirtualCarouselMenuComponent,
    VirtualSportClassesComponent,
    VsOddsCardComponent,
    VirtualCarouselSubMenuComponent,
    DesktopVirtualHomePageComponent,
    DesktopVirtualOtherSports,
    DesktopVirtualFeatureZoneComponent,
    DesktopVirtualTopSportsComponent
  ],
  exports: [
    // Overridden
    VirtualSportsPageComponent,
    VirtualCarouselMenuComponent,
    VirtualSportClassesComponent,
    VsOddsCardComponent,
    VirtualCarouselSubMenuComponent,
    DesktopVirtualHomePageComponent,
    DesktopVirtualOtherSports,
    DesktopVirtualFeatureZoneComponent,
    DesktopVirtualTopSportsComponent
  ],
  imports: [
    SharedModule,
    VsbrRoutingModule,
    RacingFeaturedModule,
    BannersModule
  ],
  providers: [
    EventProvider,
    PanelStateService,
    LocalStorageMapperService,
    VirtualSportsService,
    VirtualSportsMapperService,
    VirtualMenuDataService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class VsbrModule {
  constructor( private asls: AsyncScriptLoaderService){
    this.asls.loadCssFile('assets-vsbr.css', true, true).subscribe();
  }
}
