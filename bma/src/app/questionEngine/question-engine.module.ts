import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { QuestionEngineRoutingModule } from '@app/questionEngine/question-engine.routing.module';


import { QuestionEngineMainComponent } from '@app/questionEngine/components/questionEngineMain/question-engine-main.component';
import { SplashPageComponent } from '@app/questionEngine/components/splashPage/splash-page.component';
import { ResultsPageComponent } from '@app/questionEngine/components/resultsPage/results-page.component';
import { QuestionsPageComponent } from '@app/questionEngine/components/questionsPage/questions-page.component';
import { LatestTabComponent } from '@app/questionEngine/components/resultsPage/tabs/latestTab/latest-tab.component';
import { PreviousTabComponent } from '@app/questionEngine/components/resultsPage/tabs/previousTab/previous-tab.component';
import { QuestionsCarouselComponent } from '@app/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';

import { InfoDialogService } from '@core/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FooterComponent } from '@app/questionEngine/components/shared/footer/footer.component';
import { InfoPageComponent } from '@app/questionEngine/components/shared/infoPage/info-page.component';
import { QuestionsInfoComponent } from '@app/questionEngine/components/questionsPage/questions-info/questions-info.component';
import { InfoDialogComponent } from '@app/questionEngine/components/shared/infoDialog/info-dialog.component';
import { AnswersSummaryComponent } from '@app/questionEngine/components/shared/answersSummary/answers-summary.component';
import { UpsellComponent } from '@app/questionEngine/components/resultsPage/upsell/upsell.component';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';

import * as qe from '@localeModule/translations/en-US';

@NgModule({
  imports: [
    SharedModule,
    QuestionEngineRoutingModule,

  ],
  declarations: [
    QuestionEngineMainComponent,
    SplashPageComponent,
    ResultsPageComponent,
    QuestionsPageComponent,
    QuestionsCarouselComponent,
    FooterComponent,
    InfoPageComponent,
    QuestionsInfoComponent,
    InfoDialogComponent,
    LatestTabComponent,
    PreviousTabComponent,
    AnswersSummaryComponent,
    UpsellComponent
  ],
  providers: [
    InfoDialogService,
    QuestionEngineService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class QuestionEngineModule {
  constructor(private localeService: LocaleService) {
    this.localeService.setLangData(qe);
  }
}


