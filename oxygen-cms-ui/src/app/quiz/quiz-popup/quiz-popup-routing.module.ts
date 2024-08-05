import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {QuizPopupConfigComponent} from '@app/quiz/quiz-popup/quiz-popup-config/quiz-popup-config.component';

const optionsPopupRoutes: Routes = [
  {
    path: '',
    component: QuizPopupConfigComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(optionsPopupRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class QuizPopupRoutingModule {

}
