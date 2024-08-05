import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { InPlaySportTabComponent } from '@ladbrokesDesktop/lazy-modules/InPlaySportTab/in-play-sport-tab.component';
import { DesktopModule } from '@ladbrokesDesktop/desktop/desktop.module';

@NgModule({
  imports: [SharedModule, DesktopModule],
  declarations: [InPlaySportTabComponent],
  exports: [InPlaySportTabComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class InPlaySportTabModule {
  static entry = InPlaySportTabComponent;
}
