import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {CampaignRoutingModule} from './campaign-routing.module';
import {CampaignListComponent} from './campaign-list/campaign-list.component';
import {CampaignCreateComponent} from './campaign-create/campaign-create.component';
import {CampaignEditComponent} from './campaign-edit/campaign-edit.component';


import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    CampaignRoutingModule
  ],
  declarations: [CampaignListComponent, CampaignCreateComponent, CampaignEditComponent],
  entryComponents: [CampaignCreateComponent],
  providers: [CampaignApiService, QuizApiService]
})
export class CampaignModule {
}
