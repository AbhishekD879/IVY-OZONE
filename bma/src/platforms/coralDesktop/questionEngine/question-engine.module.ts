import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { QuestionEngineRoutingModule } from './question-engine.routing.module';

import {
  DesktopQuestionEngineMainComponent
} from '@coralDesktop/questionEngine/components/questionEngineMain/question-engine-main.component';
import { DesktopSplashPageComponent } from '@coralDesktop/questionEngine/components/splashPage/splash-page.component';
import { DesktopResultsPageComponent } from '@coralDesktop/questionEngine/components/resultsPage/results-page.component';
import { DesktopUpsellComponent } from '@coralDesktop/questionEngine/components/resultsPage/upsell/upsell.component';
import { DesktopQuestionsPageComponent } from '@coralDesktop/questionEngine/components/questionsPage/questions-page.component';
import {
  DesktopQuestionsCarouselComponent
} from '@coralDesktop/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';
import { InfoDialogService } from '@core/services/infoDialogService/info-dialog.service';
import { DesktopFooterComponent } from '@coralDesktop/questionEngine/components/shared/footer/footer.component';
import { DesktopInfoPageComponent } from '@coralDesktop/questionEngine/components/shared/infoPage/info-page.component';
import {
  DesktopQuestionsInfoComponent
} from '@coralDesktop/questionEngine/components/questionsPage/questions-info/questions-info.component';
import { InfoDialogComponent } from '@coralDesktop/questionEngine/components/shared/infoDialog/info-dialog.component';
import { DesktopPreviousTabComponent } from '@coralDesktop/questionEngine/components/resultsPage/tabs/previousTab/previous-tab.component';
import { DesktopLatestTabComponent } from '@coralDesktop/questionEngine/components/resultsPage/tabs/latestTab/latest-tab.component';
import { DesktopAnswersSummaryComponent } from '@coralDesktop/questionEngine/components/shared/answersSummary/answers-summary.component';

@NgModule({
  imports: [
    SharedModule,
    QuestionEngineRoutingModule,

  ],
  declarations: [
    DesktopQuestionEngineMainComponent,
    DesktopSplashPageComponent,
    DesktopResultsPageComponent,
    DesktopUpsellComponent,
    DesktopQuestionsPageComponent,
    DesktopQuestionsCarouselComponent,
    DesktopFooterComponent,
    InfoDialogComponent,
    DesktopInfoPageComponent,
    DesktopQuestionsInfoComponent,
    DesktopPreviousTabComponent,
    DesktopLatestTabComponent,
    DesktopAnswersSummaryComponent
  ],
  providers: [
    InfoDialogService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class QuestionEngineModule {
}
