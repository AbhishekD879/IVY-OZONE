import { Router } from '@angular/router';
import { of } from 'rxjs';

import { DesktopQuestionEngineMainComponent } from './question-engine-main.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';

describe('Desktop QuestionEngine Main Component', () => {
  let component: DesktopQuestionEngineMainComponent;
  let pubSubService;
  let deviceService;
  let questionEngineService;
  let awsService;
  let localeService;
  let router;
  let bonusSuppression;

  beforeEach(() => {
    const data = null;

    router = {
      url: '/footballsuperseries/splash',
      events: of({})
    };

    awsService = {
      API: {},
      addAction: jasmine.createSpy('addAction'),
      errorLog: jasmine.createSpy('errorLog')
    };

    pubSubService = {
      API: {
        TOGGLE_MOBILE_HEADER_FOOTER: 'TOGGLE_MOBILE_HEADER_FOOTER',
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy()
    };

    questionEngineService = {
      qeData: null,
      getQuizHistory: jasmine.createSpy().and.returnValue(of(data)),
      mapResponseOnComponentModel: jasmine.createSpy().and.returnValue(of(data)),
      checkGameData: jasmine.createSpy(),
      setQEDataUptodateStatus: jasmine.createSpy(),
      pipe: jasmine.createSpy(),
      error: jasmine.createSpy().and.callThrough(),
    };

    deviceService = {
      isMobile: true
    };

    localeService = {
      getString: jasmine.createSpy(),
    };

    component = new DesktopQuestionEngineMainComponent(
      pubSubService as PubSubService,
      deviceService as DeviceService,
      questionEngineService as QuestionEngineService,
      awsService as AWSFirehoseService,
      localeService as LocaleService,
      router as Router,
      bonusSuppression as BonusSuppressionService
    );
  });

  it('should create component', () => {
    component.ngOnInit();
    expect(component).toBeTruthy();

    component.getQuizName();
    expect(component.quizName).toEqual('footballsuperseries');

    router = {
      url: '/',
      events: of({})
    };
    component = new DesktopQuestionEngineMainComponent(
      pubSubService as PubSubService,
      deviceService as DeviceService,
      questionEngineService as QuestionEngineService,
      awsService as AWSFirehoseService,
      localeService as LocaleService,
      router as Router,
      bonusSuppression as BonusSuppressionService
    );
    component.getQuizName();
    expect(component.quizName).toEqual('');

    router = {
      url: '/qe/smart-money',
      events: of({})
    };
    component = new DesktopQuestionEngineMainComponent(
      pubSubService as PubSubService,
      deviceService as DeviceService,
      questionEngineService as QuestionEngineService,
      awsService as AWSFirehoseService,
      localeService as LocaleService,
      router as Router,
      bonusSuppression as BonusSuppressionService
    );
    component.getQuizName();
    expect(component.quizName).toEqual('smart-money');
  });
});
