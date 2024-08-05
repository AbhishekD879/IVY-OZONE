import { Component, OnInit } from '@angular/core';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { QE_COMPONENT_MISSED_DATA } from '@app/questionEngine/constants/question-engine.constant';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';

  @Component({
    selector: 'questions-info',
    templateUrl: './questions-info.component.html',
    styleUrls: ['./questions-info.component.scss'],
  })

  export class QuestionsInfoComponent implements OnInit {

    qeData: QuestionEngineQuizModel;
    isDesktop = false;
    constructor(
      private questionEngineService: QuestionEngineService,
      private pubSubService: PubSubService
    ) {}

    ngOnInit(): void  {
      if (this.questionEngineService.qeData && this.questionEngineService.qeData.baseQuiz) {
        this.qeData = this.questionEngineService.qeData.baseQuiz;
      } else {
        this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [QE_COMPONENT_MISSED_DATA]);
      }
    }
}
