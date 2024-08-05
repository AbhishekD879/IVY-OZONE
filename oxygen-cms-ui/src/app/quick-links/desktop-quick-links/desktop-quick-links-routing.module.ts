import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {DesktopQuickLinksListComponent} from './desktop-quick-links-list/desktop-quick-links-list.component';
import {DesktopQuickLinksEditComponent} from './desktop-quick-links-edit/desktop-quick-links-edit.component';

const routes: Routes = [
  {
    path: 'desktop-quick-links',
    component: DesktopQuickLinksListComponent
  },
  {
    path: 'desktop-quick-links/:id', component: DesktopQuickLinksEditComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class DesktopQuickLinksRoutingModule { }
