import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {
  DesktopQuestionEngineMainComponent
} from '@coralDesktop/questionEngine/components/questionEngineMain/question-engine-main.component';
import { DesktopSplashPageComponent } from '@coralDesktop/questionEngine/components/splashPage/splash-page.component';
import { DesktopResultsPageComponent } from '@coralDesktop/questionEngine/components/resultsPage/results-page.component';
import { DesktopQuestionsPageComponent } from '@coralDesktop/questionEngine/components/questionsPage/questions-page.component';
import { DesktopInfoPageComponent } from '@coralDesktop/questionEngine/components/shared/infoPage/info-page.component';

const routes: Routes = [{
  path: '',
  component: DesktopQuestionEngineMainComponent,
  children: [
    {
      path: '',
      redirectTo: 'splash',
      pathMatch: 'full'
    }, {
      path: 'splash',
      component: DesktopSplashPageComponent,
      data: {
        segment: 'question-engine.splash'
      }
    },
    {
      path: 'after',
      children: [
        {
          path: '',
          redirectTo: 'latest-quiz',
          pathMatch: 'full',
          data: {
            segment: 'question-engine.after'
          }
        },
        {
          path: 'latest-quiz',
          component: DesktopResultsPageComponent,  // LatestPageComponent
          data: {
            segment: 'after.latest'
          }
        }, {
          path: 'previous-quizes',
          component: DesktopResultsPageComponent, // PreviousPageComponent
          data: {
            segment: 'after.previous'
          }
        },
        {
          path: 'previous-results',
          component: DesktopResultsPageComponent, // PreviousResultsPageComponent
          data: {
            segment: 'after.previous-results'
          }
        }
      ],
    },
    {
      path: 'survey-end',
      component: DesktopResultsPageComponent,
      data: {
        segment: 'question-engine.survey-end'
      }
    },
    {
      path: 'questions',
      component: DesktopQuestionsPageComponent,
      data: {
        segment: 'question-engine.questions'
      },
    },
    {
      path: 'info/:pageId',
      component: DesktopInfoPageComponent,
      data: {
        segment: 'question-engine.info'
      }
    }
  ]
},

];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []

})
export class QuestionEngineRoutingModule {
}
