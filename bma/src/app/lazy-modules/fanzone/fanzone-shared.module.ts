import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { FanzoneSharedComponent } from '@app/lazy-modules/fanzone/components/fanzone-shared.component';
import { FanzoneSycDialogComponent } from '@app/lazy-modules/fanzone/components/fanzoneSycDialog/fanzone-syc-dialog.component';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';

import { FanzoneSharedRoutingModule } from '@app/lazy-modules/fanzone/fanzone-shared-routing.module';
import { CommonModule } from '@angular/common';
import { FanzoneSelectYourTeamDialogComponent } from './components/fanzoneSelectYourTeamDialog/fanzone-select-your-team-dialog.component';
import { FanzoneCrestImageComponent } from './components/fanzoneCrestImage/fanzone-crest-image.component';
import { FanzoneNotificationComponent } from './components/fanzoneNotification/fanzone-notification.component';
import { FanzonePreferenceDialogComponent } from './components/fanzonePreferenceDialog/fanzone-preference-dialog.component';
import { FanzoneBannerComponent } from '@lazy-modules/fanzone/components/fanzonBanner/fanzone-banner-entry.component';
import { FanzoneCbOverlayComponent } from './components/fanzoneCbOverlay/fanzone-cb-overlay.component';
import { FanzoneOptinEmailDialogComponent } from './components/fanzoneOptinEmailDialog/fanzone-optin-email-dialog.component';
import { FanzoneGamesDialogComponent } from "@app/lazy-modules/fanzone/components/fanzoneGamesDialog/fanzone-games-dialog.component";
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';
import { FanzoneGameLaunchDialogComponent } from "@app/lazy-modules/fanzone/components/fanzoneGameLaunchDialog/fanzone-game-launch-dialog.component";

@NgModule({
  imports: [FanzoneSharedRoutingModule, CommonModule, SharedModule],
  declarations:
    [FanzoneSharedComponent,
      FanzoneSycDialogComponent,
      FanzoneSelectYourTeamDialogComponent,
      FanzoneCrestImageComponent,
      FanzoneNotificationComponent,
      FanzonePreferenceDialogComponent,
      FanzoneBannerComponent,
      FanzoneCbOverlayComponent,
      FanzoneOptinEmailDialogComponent,
      FanzoneGamesDialogComponent,
      FanzoneGameLaunchDialogComponent
    ],
  exports: [FanzoneBannerComponent, FanzoneSharedComponent, FanzoneSycDialogComponent, FanzoneSelectYourTeamDialogComponent, FanzoneCrestImageComponent, FanzonePreferenceDialogComponent, FanzoneBannerComponent, FanzoneCbOverlayComponent, FanzoneOptinEmailDialogComponent, FanzoneGamesDialogComponent, FanzoneGameLaunchDialogComponent],
  providers: [FanzoneSharedService, FanzoneGamesService]
})
export class FanzoneSharedModule {
  static entry = { FanzoneSharedComponent, FanzoneBannerComponent, FanzoneCbOverlayComponent };
}
