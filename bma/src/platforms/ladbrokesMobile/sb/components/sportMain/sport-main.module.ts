// (no proper coverage - no file movement) TODO re-folder this module

import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { SportMainComponent } from './sport-main.component';
import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';
import { SportMatchesTabComponent } from '@sbModule/components/sportMatchesTab/sport-matches-tab.component';
import { SbModule } from '@ladbrokesMobile/sb/sb.module';

@NgModule({
  imports: [
    SharedModule,
    SbModule
  ],
  declarations: [
    SportMainComponent,
    SportMatchesPageComponent,
    SportTabsPageComponent,
    SportMatchesTabComponent
  ],
  providers: [],
  exports: [
    SportMainComponent,
    SportMatchesPageComponent,
    SportTabsPageComponent,
    SportMatchesTabComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SportMainModule { }
