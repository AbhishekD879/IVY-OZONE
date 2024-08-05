import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { LazyNextRacesTabRoutingModule } from '@ladbrokesMobile/lazy-modules/lazyNextRacesTab/lazyNextRacesTab-routing.module';
import {
  LadbrokesExtraPlaceHomeComponent
} from '@ladbrokesMobile/lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component';

import {
  LadbrokesNextRacesHomeTabComponent
} from '@ladbrokesMobile/lazy-modules/lazyNextRacesTab/components/nextRacesHomeTab/next-races-home-tab.component';
import { SharedModule } from '@sharedModule/shared.module';

import { NextRacesHomeComponent } from '@lazy-modules-module/lazyNextRacesTab/components/nextRacesHome/next-races-home.component';
import { NextRacesHomeService } from '@ladbrokesMobile/lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';

@NgModule({
  imports: [
    LazyNextRacesTabRoutingModule,
    SharedModule
  ],
  declarations: [
    LadbrokesExtraPlaceHomeComponent,
    LadbrokesNextRacesHomeTabComponent,
    NextRacesHomeComponent
  ],
  providers: [
    NextRacesHomeService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class LazyNextRacesTabModule {
  static entry = LadbrokesNextRacesHomeTabComponent;
}
