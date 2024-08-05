import { UpsellItemModel } from '@app/questionEngine/models/upsell.model';
import { IResultPage } from '@app/questionEngine/models/result-page.model';

export class QuestionEngineResultsPageModel {
  backgroundSvgImagePath: string;
  gameDescription: string;
  noLatestRoundMessage: string;
  noPreviousRoundMessage: string;
  showAnswersSummary: boolean;
  showPrizes: boolean;
  showResults: boolean;
  showUpsell: boolean;
  submitMessage: string;
  title: string;
  submitCta: string;
  upsellAddToBetslipCtaText: string;
  upsellBetInPlayCtaText: string;
  upsell: UpsellItemModel;

  constructor(
    endPage: IResultPage,
    upsellData?: UpsellItemModel
  ) {
    this.backgroundSvgImagePath = endPage.backgroundSvgImagePath;
    this.gameDescription = endPage.gameDescription;
    this.noLatestRoundMessage = endPage.noLatestRoundMessage;
    this.noPreviousRoundMessage = endPage.noPreviousRoundMessage;
    this.showAnswersSummary = endPage.showAnswersSummary;
    this.showPrizes = endPage.showPrizes;
    this.showResults = endPage.showResults;
    this.showUpsell = endPage.showUpsell;
    this.submitMessage = endPage.submitMessage;
    this.title = endPage.title;
    this.submitCta = endPage.submitCta;
    this.upsellAddToBetslipCtaText = endPage.upsellAddToBetslipCtaText;
    this.upsellBetInPlayCtaText = endPage.upsellBetInPlayCtaText;
    if (upsellData) {
      this.upsell = new UpsellItemModel(upsellData);
    }
  }
}
