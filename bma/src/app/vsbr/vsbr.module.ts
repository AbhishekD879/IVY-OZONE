import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { VsbrRoutingModule } from './vsbr-routing.module';
import { EventProvider } from './services/event.provider';
import { PanelStateService } from './services/panel-state.service';
import { VirtualSportsService } from './services/virtual-sports.service';
import { LocalStorageMapperService } from './services/local-storage-mapper.service';
import { VsOddsCardComponent } from '@app/vsbr/components/vsOddsCard/vs-odds-card.component';
import { VirtualCarouselMenuComponent } from './components/virtualCarouselMenu/virtual-carousel-menu.component';
import { VirtualSportsPageComponent } from './components/virtualSportsPage/virtual-sports-page.component';
import { VirtualSportClassesComponent } from './components/virtualSportClasses/virtual-sport-classes.component';
import { VsVideoStreamComponent } from './components/vsVideoStream/vs-video-stream.component';
import { VirtualSportsMapperService } from './services/virtual-sports-mapper.service';
import { VirtualMenuDataService } from './services/virtual-menu-data.service';
import { CountdownHeaderComponent } from './components/countdownHeader/countdown-header.component';
import { VirtualCarouselSubMenuComponent } from '@app/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component';
import { VirtualHomePageComponent } from './components/virtualHomePage/virtual-home-page.component';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';
import { RacingFeaturedModule } from '../lazy-modules/racingFeatured/racing-featured.module';
import { VirtualOtherSports } from './components/virtualOtherSports/virtual-other-sports.component';
import { VirtualFeatureZoneComponent } from './components/virtualFeatureZone/virtual-feature-zone.component';
import { VirtualTopSportsComponent } from './components/virtual-top-sports/virtual-top-sports.component';
import { BannersModule } from '@app/lazy-modules/banners/banners.module';

@NgModule({
  declarations: [
    VirtualSportsPageComponent,
    VirtualSportClassesComponent,
    VirtualCarouselMenuComponent,
    VsVideoStreamComponent,
    VsOddsCardComponent,
    CountdownHeaderComponent,
    VirtualCarouselSubMenuComponent,
    VirtualHomePageComponent,
    VirtualOtherSports,
    VirtualFeatureZoneComponent,
    VirtualTopSportsComponent
  ],
  exports: [
    VirtualSportsPageComponent,
    VirtualSportClassesComponent,
    VsOddsCardComponent,
    CountdownHeaderComponent,
    VirtualCarouselSubMenuComponent,
    VirtualHomePageComponent,
    VirtualOtherSports,
    VirtualFeatureZoneComponent,
    VirtualTopSportsComponent
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
