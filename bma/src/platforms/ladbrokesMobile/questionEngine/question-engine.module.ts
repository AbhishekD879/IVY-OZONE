import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { QuestionEngineRoutingModule } from '@ladbrokesMobile/questionEngine/question-engine.routing.module';

import { QuestionEngineMainComponent } from '@questionEngine/components/questionEngineMain/question-engine-main.component';
import { SplashPageComponent } from '@ladbrokesMobile/questionEngine/components/splashPage/splash-page.component';
import { ResultsPageComponent } from '@ladbrokesMobile/questionEngine/components/resultsPage/results-page.component';
import { QuestionsPageComponent } from '@ladbrokesMobile/questionEngine/components/questionsPage/questions-page.component';
import { LatestTabComponent } from '@ladbrokesMobile/questionEngine/components/resultsPage/tabs/latestTab/latest-tab.component';
import { PreviousTabComponent } from '@ladbrokesMobile/questionEngine/components/resultsPage/tabs/previousTab/previous-tab.component';
import {
  QuestionsCarouselComponent
} from '@ladbrokesMobile/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';

import { InfoDialogComponent } from '@ladbrokesMobile/questionEngine/components/shared/infoDialog/info-dialog.component';
import { InfoDialogService } from '@core/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FooterComponent } from '@questionEngine/components/shared/footer/footer.component';
import { InfoPageComponent } from '@ladbrokesMobile/questionEngine/components/shared/infoPage/info-page.component';
import { QuestionsInfoComponent } from '@questionEngine/components/questionsPage/questions-info/questions-info.component';
import { AnswersSummaryComponent } from '@ladbrokesMobile/questionEngine/components/shared/answersSummary/answers-summary.component';
import { UpsellComponent } from '@ladbrokesMobile/questionEngine/components/resultsPage/upsell/upsell.component';
import * as qe from '@localeModule/translations/en-US';

@NgModule({
  imports: [
    SharedModule,
    QuestionEngineRoutingModule
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
    UpsellComponent,
  ],
  providers: [
    InfoDialogService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class QuestionEngineModule {
  constructor(private localeService: LocaleService) {
    this.localeService.setLangData(qe);
  }
}


