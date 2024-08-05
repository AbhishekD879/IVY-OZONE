// (no proper coverage - no file movement) TODO re-folder this module

import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { SportMainComponent } from './sport-main.component';
import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';
import { FootballTutorialOverlayComponent } from '@sbModule/components/footballTutorialOverlay/football-tutorial-overlay.component';
import { SportMatchesTabComponent } from '@sbModule/components/sportMatchesTab/sport-matches-tab.component';
import { SbModule } from '@sbModule/sb.module';

@NgModule({
  imports: [
    SharedModule,
    SbModule,
  ],
  declarations: [
    SportMainComponent,
    SportMatchesPageComponent,
    SportTabsPageComponent,
    FootballTutorialOverlayComponent,
    SportMatchesTabComponent
  ],
  providers: [],
  exports: [
    SportMainComponent,
    SportMatchesPageComponent,
    SportTabsPageComponent,
    FootballTutorialOverlayComponent,
    SportMatchesTabComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SportMainModule { }
