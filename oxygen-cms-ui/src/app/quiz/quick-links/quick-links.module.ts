import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {QuickLinksRoutingModule} from './quick-links-routing.module';
import {QuickLinksListComponent} from './quick-links-list/quick-links-list.component';
import {QuickLinksAddComponent} from './quick-links-add/quick-links-add.component';
import {QuickLinksEditComponent} from './quick-links-edit/quick-links-edit.component';
import {QEQuickLinksApiService} from '@app/quiz/service/quick-links.api.service';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    QuickLinksRoutingModule
  ],
  declarations: [QuickLinksListComponent, QuickLinksAddComponent, QuickLinksEditComponent],
  entryComponents: [QuickLinksAddComponent],
  providers: [QEQuickLinksApiService, QuizApiService]
})
export class QuickLinksModule {
}
