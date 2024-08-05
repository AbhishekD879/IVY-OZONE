import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {QuizEngineRoutingModule} from './quiz-engine-routing.module';
import {QuizEngineListComponent} from './quiz-engine-list/quiz-engine-list.component';
import {QuizEngineEditComponent} from './quiz-engine-edit/quiz-engine-edit.component';
import {QuizEngineCreateComponent} from './quiz-engine-create/quiz-engine-create.component';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import {SortableTableService} from '@app/client/private/services/sortable.table.service';
import { MatTableModule } from '@angular/material/table';
import {UpsellComponent} from '@app/quiz/quiz-engine/upsell/upsell.component';
import {QEQuickLinksApiService} from '@app/quiz/service/quick-links.api.service';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import { FssRewardsDialogComponent } from '@app/quiz/fss-rewards-dialog/fss-rewards-dialog.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    QuizEngineRoutingModule,
    MatTableModule
  ],
  declarations: [
    QuizEngineListComponent,
    QuizEngineEditComponent,
    QuizEngineCreateComponent,
    UpsellComponent,
    FssRewardsDialogComponent
  ],
  entryComponents: [
    QuizEngineCreateComponent,
    UpsellComponent
  ],
  providers: [
    QuizApiService,
    SplashPageApiService,
    SortableTableService,
    QEQuickLinksApiService,
    EndPageApiService
  ]
})
export class QuizEngineModule {
}
