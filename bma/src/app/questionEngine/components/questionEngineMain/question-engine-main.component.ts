import { Component, OnDestroy, OnInit } from '@angular/core';
import { timeout } from 'rxjs/operators';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@core/services/locale/locale.service';

import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { IQuizHistoryModel } from '@app/questionEngine/models/quizHistory.model';
import {
  BACKEND_RESPONSE_TIMEOUT_LIMIT,
  QE_INIT_DATA_FAILURE,
} from '@app/questionEngine/constants/question-engine.constant';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';
import { rgyellow } from '@bma/constants/rg-yellow.constant';

@Component({
  selector: 'question-engine-main',
  templateUrl: './question-engine-main.component.html',
  styleUrls: ['./question-engine-main.component.scss'],
})
export class QuestionEngineMainComponent implements OnInit, OnDestroy {
  isMobile: boolean = true;
  dataLoadingError: string = this.localeService.getString('qe.dataLoadingError');
  dataLoadingErrorBtn: string = this.localeService.getString('qe.dataLoadingErrorBtn');
  public qeData: QuestionEngineModel;
  public errorMessage: string;
  protected routeChangeListener: Subscription;
  protected quizHistoryListener: Subscription;
  private readonly tag = 'QeMainComponent';

  constructor(
    protected pubSubService: PubSubService,
    protected deviceService: DeviceService,
    protected questionEngineService: QuestionEngineService,
    protected awsService: AWSFirehoseService,
    protected localeService: LocaleService,
    protected router: Router,
    protected bonusSuppressionService: BonusSuppressionService
  ) {}

  ngOnInit(): void {
    this.isMobile = this.deviceService.isMobile;
    this.isMobile && this.pubSubService.publish(this.pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, false);
    this.pubSubService.subscribe(this.tag, this.pubSubService.API.QE_FATAL_ERROR,
      (errorMessage, error) => {
        this.errorMessage = errorMessage;
        error && this.awsService.errorLog(error);
        console.error(errorMessage);
        this.awsService.addAction(`Question Engine fatal error`, {error: errorMessage});
      });

    this.initComponentData();
    this.pubSubService.subscribe(this.tag, [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
        if (!this.bonusSuppressionService.checkIfYellowFlagDisabled(rgyellow.FOOTBALL_SUPER_SERIES)) {
          this.bonusSuppressionService.navigateAwayForRGYellowCustomer();
        }
      this.initComponentData();
    });
    this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', true);
  }

  ngOnDestroy(): void {
    this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', false);
    this.isMobile && this.pubSubService.publish(this.pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, true);
    this.questionEngineService.resetCheckForAnonymousDataValue();
    this.pubSubService.unsubscribe(this.tag);
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
    this.quizHistoryListener && this.quizHistoryListener.unsubscribe();
  }

  private initComponentData(initial: boolean = false): void {
    this.quizHistoryListener = this.questionEngineService.getQuizHistory(initial)
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT))
      .subscribe((data: IQuizHistoryModel) => {

        // if no quiz live or previous game data from BE - perform default data fetch
        if (this.questionEngineService.checkGameData(data, this.initComponentData.bind(this))) {
          return;
        }

        this.qeData = this.questionEngineService.mapResponseOnComponentModel(data);
        this.questionEngineService.setQEDataUptodateStatus(true);
        this.pubSubService.publish(this.pubSubService.API.QE_HISTORY_DATA_RECEIVED);
      },
      (error) => {
        this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [QE_INIT_DATA_FAILURE, error]);
      });
  }

}
