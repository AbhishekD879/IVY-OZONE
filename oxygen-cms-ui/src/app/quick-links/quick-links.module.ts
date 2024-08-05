import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DesktopQuickLinksModule } from './desktop-quick-links/desktop-quick-links.module';
import { DesktopQuickLinksCreateComponent } from './desktop-quick-links/desktop-quick-links-create/desktop-quick-links-create.component';
import { HrQuickLinksModule } from './hr-quick-links/hr-quick-links.module';
import { HrQuickLinksCreateComponent } from './hr-quick-links/hr-quick-links-create/hr-quick-links-create.component';
import { NavigationPointsModule } from './navigation-points/navigation-points.module';
import { NavigationPointsCreateComponent } from './navigation-points/navigation-points-create/navigation-points-create.component';
import { ExtraNavigationPointsModule } from './extra-navigation-points/extra-navigation-points.module';
@NgModule({
  imports: [
    CommonModule,
    DesktopQuickLinksModule,
    HrQuickLinksModule,
    NavigationPointsModule,
    ExtraNavigationPointsModule
  ],
  entryComponents: [
    DesktopQuickLinksCreateComponent,
    HrQuickLinksCreateComponent,
    NavigationPointsCreateComponent
  ]
})
export class QuickLinksModule { }
