import { Component } from '@angular/core';

import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { QuestionEngineMainComponent } from '@app/questionEngine/components/questionEngineMain/question-engine-main.component';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'question-engine-main',
  templateUrl: './question-engine-main.component.html',
  styleUrls: ['./question-engine-main.component.scss'],
  providers: [QuestionEngineService]
})

export class DesktopQuestionEngineMainComponent extends QuestionEngineMainComponent {

  quizName: string;

  constructor(
    protected pubSubService: PubSubService,
    protected deviceService: DeviceService,
    protected questionEngineService: QuestionEngineService,
    protected awsService: AWSFirehoseService,
    protected localeService: LocaleService,
    protected router: Router,
    protected bonusSuppressionService: BonusSuppressionService
  ) {
    super(pubSubService, deviceService, questionEngineService, awsService, localeService, router, bonusSuppressionService);
    this.quizName = this.getQuizName();
  }

  public getQuizName(): string {
    const urlParts: string[] = this.router.url.split('/').filter(e => e !== '');
    if (urlParts.length && urlParts[0] === 'footballsuperseries') {
      return urlParts[0];
    }
    if (urlParts.length > 1 && urlParts[0] === 'qe') {
      return urlParts[1];
    }
    return '';
  }
}
