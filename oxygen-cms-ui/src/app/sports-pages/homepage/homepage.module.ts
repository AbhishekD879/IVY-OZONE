import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {HomepageRoutingModule} from './homepage-routing.module';
import {SharedModule} from '@app/shared/shared.module';

import {HomePageComponent} from './homepage-page/home.page.component';

import {HrQuickLinksModule} from '@app/quick-links/hr-quick-links/hr-quick-links.module';
import {FeaturedTabModule} from '@app/featured-tab/featured-tab.module';
import {SportsModulesService} from '@app/sports-modules/sports-modules.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    HomepageRoutingModule,
    HrQuickLinksModule, // TODO: change to newly created page
    FeaturedTabModule // TODO: change to newly created page
  ],
  declarations: [
    HomePageComponent
  ],
  providers: [
    SportsModulesService
  ],
  entryComponents: [
    HomePageComponent
  ]
})
export class HomePageModule { }
