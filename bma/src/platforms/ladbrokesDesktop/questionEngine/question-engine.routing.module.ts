import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { QuestionEngineMainComponent } from '@ladbrokesDesktop/questionEngine/components/questionEngineMain/question-engine-main.component';
import { SplashPageComponent } from '@ladbrokesDesktop/questionEngine/components/splashPage/splash-page.component';
import { ResultsPageComponent } from '@ladbrokesDesktop/questionEngine/components/resultsPage/results-page.component';
import { QuestionsPageComponent } from '@ladbrokesDesktop/questionEngine/components/questionsPage/questions-page.component';
import { InfoPageComponent } from '@ladbrokesDesktop/questionEngine/components/shared/infoPage/info-page.component';

const routes: Routes = [{
  path: '',
  component: QuestionEngineMainComponent,
  children: [
    {
      path: '',
      redirectTo: 'splash',
      pathMatch: 'full'
    }, {
      path: 'splash',
      component: SplashPageComponent,
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
          component: ResultsPageComponent,  // LatestPageComponent
          data: {
            segment: 'question-engine.after.latest'
          }
        }, {
          path: 'previous-quizes',
          component: ResultsPageComponent, // PreviousPageComponent
          data: {
            segment: 'question-engine.after.previous'
          }
        }
      ],
    },
    {
      path: 'survey-end',
      component: ResultsPageComponent,
      data: {
        segment: 'question-engine.survey-end'
      }
    },
    {
      path: 'questions',
      component: QuestionsPageComponent,
      data: {
        segment: 'question-engine.questions'
      },
    },
    {
      path: 'info/:pageId',
      component: InfoPageComponent,
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
