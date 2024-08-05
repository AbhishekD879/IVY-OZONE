import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { RssRewardsPageComponent } from './rss-rewards-page/rss-rewards-page.component';
import { PendingChangesGuard } from '@app/client/private/classes/PendingChangesGuard.class';
const rssRewardsPageRoutes: Routes = [
  {
    path: '',
    component: RssRewardsPageComponent,
    children: [],
    canDeactivate: [PendingChangesGuard]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(rssRewardsPageRoutes)
  ],
  exports: [
    RouterModule
  ],
  providers: [PendingChangesGuard]
})
export class RssRewardsRoutingModule {

}