import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {CampaignListComponent} from '@app/timeline/campaign/campaign-list/campaign-list.component';
import {CampaignEditComponent} from '@app/timeline/campaign/campaign-edit/campaign-edit.component';
import {CampaignCreateComponent} from '@app/timeline/campaign/campaign-create/campaign-create.component';

const routes: Routes = [
  {
    path: '',
    component: CampaignListComponent
  },
  {
    path: 'edit/:id',
    component: CampaignEditComponent
  },
  {
    path: 'create',
    component: CampaignCreateComponent
  }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CampaignRoutingModule {
}
