import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { QuizDialogComponent } from '@lazy-modules/quiz/components/quiz-dialog.component';

@NgModule({
  imports: [],
  declarations: [QuizDialogComponent],
  exports: [QuizDialogComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class QuizDialogModule {
  static entry = QuizDialogComponent;
}
