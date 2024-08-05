import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { VsbrRoutingModule } from '@vsbrModule/vsbr-routing.module';
import { DesktopVirtualSportsPageComponent } from '@coralDesktop/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { VirtualSportsService } from '@app/vsbr/services/virtual-sports.service';
import { LocalStorageMapperService } from '@app/vsbr/services/local-storage-mapper.service';
import { PanelStateService } from '@app/vsbr/services/panel-state.service';
import { EventProvider } from '@app/vsbr/services/event.provider';
import { VsOddsCardComponent } from '@app/vsbr/components/vsOddsCard/vs-odds-card.component';
import { VirtualSportClassesComponent } from '@app/vsbr/components/virtualSportClasses/virtual-sport-classes.component';
import { VsVideoStreamComponent } from '@app/vsbr/components/vsVideoStream/vs-video-stream.component';
import { VirtualSportsMapperService } from '@app/vsbr/services/virtual-sports-mapper.service';
import { VirtualMenuDataService } from '@app/vsbr/services/virtual-menu-data.service';
import { CountdownHeaderComponent } from '@app/vsbr/components/countdownHeader/countdown-header.component';
import { DesktopVirtualCarouselMenuComponent } from '@coralDesktop/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';
import {
  DesktopVirtualCarouselSubMenuComponent
} from '@coralDesktop/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component';
import { DesktopVirtualHomePageComponent } from '@coralDesktop/vsbr/components/virtualHomePage/virtual-home-page.component';
import { RacingFeaturedModule } from '../lazy-modules/racingFeatured/racing-featured.module';
import { DesktopVirtualOtherSports } from '@coralDesktop/vsbr/components/virtualOtherSports/virtual-other-sports.component';
import { DesktopVirtualFeatureZoneComponent } from '@coralDesktop/vsbr/components/virtualFeatureZone/virtual-feature-zone.component';
import { DesktopVirtualTopSportsComponent } from '@coralDesktop/vsbr/components/virtual-top-sports/virtual-top-sports.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { BannersModule } from '@coralDesktop/lazy-modules/banners/banners.module';

@NgModule({
  declarations: [
    VirtualSportClassesComponent,
    VsVideoStreamComponent,
    VsOddsCardComponent,
    CountdownHeaderComponent,
    // Overridden
    DesktopVirtualSportsPageComponent,
    DesktopVirtualCarouselMenuComponent,
    DesktopVirtualCarouselSubMenuComponent,
    DesktopVirtualHomePageComponent,
    DesktopVirtualOtherSports,
    DesktopVirtualFeatureZoneComponent,
    DesktopVirtualTopSportsComponent
  ],
  exports: [
    VirtualSportClassesComponent,
    VsOddsCardComponent,

    // Overridden
    DesktopVirtualSportsPageComponent,
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
