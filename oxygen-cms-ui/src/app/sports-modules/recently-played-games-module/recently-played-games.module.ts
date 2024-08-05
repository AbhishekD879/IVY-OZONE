import {NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';
import { RecentlyPlayedGamesRoutingModule } from '@app/sports-modules/recently-played-games-module/recently-played-games-routing.module';
import {
  RecentlyPlayedGamesModulePageComponent
} from '@app/sports-modules/recently-played-games-module/recently-played-games-module-page/recently-played-games-module-page.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    RecentlyPlayedGamesRoutingModule
  ],
  declarations: [
    RecentlyPlayedGamesModulePageComponent
  ],
  entryComponents: [
    RecentlyPlayedGamesModulePageComponent
  ],
  providers: [],
  exports: []
})
export class RecentlyPlayedGamesModule {
}
