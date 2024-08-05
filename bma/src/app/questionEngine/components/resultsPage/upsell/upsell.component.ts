import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { timeout } from 'rxjs/operators';

import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';

import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { IUpsellComponentModel } from '@app/questionEngine/models/upsellComponent.model';
import { BACKEND_RESPONSE_TIMEOUT_LIMIT } from '@app/questionEngine/constants/question-engine.constant';

@Component({
  selector: 'upsell',
  templateUrl: './upsell.component.html',
  styleUrls: ['./upsell.component.scss'],
})

export class UpsellComponent implements OnInit, OnDestroy {
  @Input() qeData: QuestionEngineModel;

  upsellData: IUpsellComponentModel;
  upsellReturn: string;
  gameStarted: boolean = false;
  processingAddToSlip: boolean = false;
  btnProcessingMsg: string = this.localeService.getString('qe.btnProcessingMsg');
  upsellTitle: string;
  private eventId: string;
  private addToSlipHandler: Subscription;

  constructor(
    protected questionEngineService: QuestionEngineService,
    protected router: Router,
    protected localeService: LocaleService,
    protected gtmService: GtmService
  ) {
  }

  ngOnInit(): void {
    const {
      eventDetails: { startTime }, resultsPage: { upsellAddToBetslipCtaText, upsellBetInPlayCtaText, upsell },
      defaultQuestionsDetails: { awayTeamSvgFilePath, homeTeamSvgFilePath, topLeftHeader, topRightHeader },
      eventDetails: { eventId, eventName }
    } = this.qeData.baseQuiz;
    const { fallbackImagePath, marketName,
      price, priceDen, priceNum, selectionId, selectionName } = upsell;

    this.eventId = eventId;
    this.upsellData = {
      awayTeamSvgFilePath,
      betNowCTA: upsellAddToBetslipCtaText,
      betInPlay: upsellBetInPlayCtaText,
      marketName,
      homeTeamSvgFilePath,
      topLeftHeader,
      topRightHeader,
      fallbackImagePath,
      price,
      priceNum,
      priceDen,
      selectionId,
      selectionName
    };
    this.calculateReturns(price);
    this.gameStarted = this.eventStarted(startTime);
    this.upsellTitle = this.gameStarted ? eventName && eventName.replace(/\|/g, '') : selectionName;
  }

  ngOnDestroy(): void {
    if (this.addToSlipHandler) {
      this.addToSlipHandler.unsubscribe();
    }
  }

  addToSlip(): void {
    this.processingAddToSlip = true;
    this.addToSlipHandler = this.questionEngineService.addToSlipHandler(this.upsellData.selectionId.toString())
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT))
      .subscribe(
        () => this.trackBetslipGA(),
        () => {
          this.processingAddToSlip = false;
          this.upsellData.betNowCTA = this.localeService.getString('qe.upsellTryAgain');
          return;
        },
        () => this.processingAddToSlip = false
    );
  }

  betInPlayHandler(): void {
    const url = `/event/${this.eventId}`;
    this.router.navigateByUrl(url);
  }

  /**
   * GA: Send tracking data to GTM
   *
   */
  public trackBetslipGA(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'Betslip',
      eventAction: 'Add to betslip',
      eventLabel: 'success',
      ecommerce: {
        add: {
          products: [{
            name: this.upsellData.selectionName, //  '<<EVENT NAME>>'
            category: '16',
            variant: '434',
            brand: this.upsellData.marketName, // '<<EVENT MARKET>>'
            dimension60: '11527917', //  '<<EVENT>>'
            dimension61: this.upsellData.selectionId.toString(), // '<<SELECTION ID>>'
            dimension62: 0,
            dimension63: 0,
            dimension64: `/${this.questionEngineService.sourceIdFromParams}/after/latest-quiz`,  // '<<LOCATION>>'
            dimension65: `/${this.questionEngineService.sourceIdFromParams}` // '<< SOURCE_ID>>'
          }]
        }
      }
    });
  }

  protected calculateReturns(price: number): void {
    // 1.431474 will return 14.31
    const returnPrice = (Math.floor(price * 1000) / 100).toFixed(2).replace('.00','');
    this.upsellReturn = `${this.localeService.getString('qe.upsellReturnInfo')}${returnPrice}`;
  }

  protected eventStarted(startTime: Date | string): boolean {
    return new Date().getTime() > new Date(startTime).getTime();
  }
}
