import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {PostListComponent} from '@app/timeline/post/post-list/post-list.component';
import {PostEditComponent} from '@app/timeline/post/post-edit/post-edit.component';
import {PostCreateComponent} from '@app/timeline/post/post-create/post-create.component';
import {SpotlightComponent} from '@app/timeline/post/spotlight/spotlight.component';

const routes: Routes = [
  {
    path: 'by-campaign/:campaignId',
    component: PostListComponent
  },
  {
    path: 'spotlight/by-campaign/:campaignId',
    component: SpotlightComponent
  },
  {
    path: 'by-campaign/:campaignId/edit/:id',
    component: PostEditComponent
  },
  {
    path: 'by-campaign/:campaignId/create',
    component: PostCreateComponent
  }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PostRoutingModule {
}
