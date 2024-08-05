import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {EndPageRoutingModule} from './end-page-routing.module';
import {EndPageListComponent} from './end-page-list/end-page-list.component';
import {EndPageCreateComponent} from './end-page-create/end-page-create.component';
import {EndPageEditComponent} from './end-page-edit/end-page-edit.component';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    EndPageRoutingModule
  ],
  declarations: [EndPageListComponent, EndPageCreateComponent, EndPageEditComponent],
  entryComponents: [EndPageCreateComponent],
  providers: [EndPageApiService, QuizApiService]
})
export class EndPageModule {
}
