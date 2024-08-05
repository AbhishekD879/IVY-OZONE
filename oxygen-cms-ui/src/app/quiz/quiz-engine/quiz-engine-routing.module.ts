import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { QuizEngineListComponent } from '@app/quiz/quiz-engine/quiz-engine-list/quiz-engine-list.component';
import { QuizEngineEditComponent } from '@app/quiz/quiz-engine/quiz-engine-edit/quiz-engine-edit.component';

const routes: Routes = [
  {
    path: '',
    component: QuizEngineListComponent
  },
  {
    path: ':id',
    component: QuizEngineEditComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class QuizEngineRoutingModule { }
