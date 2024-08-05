import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import { QE_COMPONENT_MISSED_DATA } from '@app/questionEngine/constants/question-engine.constant';
import { LinksModel } from '@app/questionEngine/models/links.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';

@Component({
  selector: 'qe-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})

export class FooterComponent implements OnInit {

  qeData: QuestionEngineQuizModel;
  clickedItem: number = -1;

  constructor(
    private questionEngineService: QuestionEngineService,
    private router: Router,
    private pubSubService: PubSubService,
    private windowRefService: WindowRefService
  ) {
  }

  ngOnInit(): void {
    if (this.questionEngineService.qeData && this.questionEngineService.qeData.baseQuiz) {
      this.qeData = this.questionEngineService.qeData.baseQuiz;
    } else {
      this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [QE_COMPONENT_MISSED_DATA]);
    }
  }

  redirectLink(link: LinksModel, index: number): void {
    const { sourceId } = this.questionEngineService.qeData.baseQuiz;
    this.clickedItem = index;
    this.windowRefService.nativeWindow.setTimeout(() => {
      const redirectUrl: string = `${this.questionEngineService.resolvePath(sourceId)}/info/${link.relativePath}`;
      this.router.navigateByUrl(redirectUrl);
      }, 50
    );
    this.questionEngineService.trackEventGA(link.title);
  }

  trackByFn(index: number): string {
    return `${index}`;
  }
}
