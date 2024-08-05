import { NgModule } from '@angular/core';
import { QuizPopupConfigComponent } from './quiz-popup-config/quiz-popup-config.component';
import { SharedModule } from '@app/shared/shared.module';
import {QuizPopupRoutingModule} from '@app/quiz/quiz-popup/quiz-popup-routing.module';
import {FormsModule} from '@angular/forms';
import {QuizPopupApiService} from '@app/quiz/service/quiz-popup.api.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    QuizPopupRoutingModule
  ],
  providers: [
    QuizPopupApiService
  ],
  declarations: [QuizPopupConfigComponent],
  entryComponents: [
    QuizPopupConfigComponent
  ]
})
export class QuizPopupModule { }
