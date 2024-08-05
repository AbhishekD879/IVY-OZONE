import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {PostRoutingModule} from './post-routing.module';
import {PostListComponent} from './post-list/post-list.component';
import {PostPreviewComponent} from './post-preview/post-preview.component';
import {PostCreateComponent} from './post-create/post-create.component';
import {PostEditComponent} from './post-edit/post-edit.component';


import {PostApiService} from '@app/timeline/service/post-api.service';
import {TemplateApiService} from '@app/timeline/service/template-api.service';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import {SpotlightComponent} from '@app/timeline/post/spotlight/spotlight.component';
import {SpotlightApiService} from '@app/timeline/service/spotlight-api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    PostRoutingModule
  ],
  exports:[SpotlightComponent],
  declarations: [PostListComponent, PostPreviewComponent, PostCreateComponent, PostEditComponent, SpotlightComponent],
  entryComponents: [PostCreateComponent],
  providers: [PostApiService, TemplateApiService, CampaignApiService, SpotlightApiService]
})
export class PostModule {
}
