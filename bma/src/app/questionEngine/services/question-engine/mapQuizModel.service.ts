import { Injectable } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { IQuizModel } from '@app/questionEngine/models/quiz.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { IAnswerModel, Question } from '@app/questionEngine/models/question.model';
import environment from '@environment/oxygenEnvConfig';
import { QuestionEngineSplashPageModel } from '@app/questionEngine/models/questionEngineSplashPage.model';
import { QuestionEngineResultsPageModel } from '@app/questionEngine/models/questionEngineResultsPage.model';
import { QuestionEngineQuestionDetailsModel } from '@app/questionEngine/models/questionEngineQuestionDetails.model';
import { QuizPopupModel } from '@app/questionEngine/models/quizPopup.model';
import { UpsellItemModel, IUpsellModel, IUpsellOptions } from '@app/questionEngine/models/upsell.model';

@Injectable({
  providedIn: 'root'
})
export class MapQuizModelService {
  private cmsUrl: string = this.handleCmsLink();
  private ctaButtonText: string;
  private upsellData: UpsellItemModel;

  constructor(
    private domSanitizer: DomSanitizer,
  ) {}

  // QuestionEngineQuizModel --> DTO
  public mapQuizModel(backendQuiz: IQuizModel): QuestionEngineQuizModel {
    const quiz: QuestionEngineQuizModel = new QuestionEngineQuizModel();
    const { endPage, splashPage, upsell, defaultQuestionsDetails } = backendQuiz;

    quiz.entryDeadline = new Date(backendQuiz.entryDeadline);
    quiz.firstAnsweredQuestion = backendQuiz.firstAnsweredQuestion;
    quiz.firstQuestion = backendQuiz.firstQuestion;
    quiz.id = backendQuiz.id;
    quiz.displayTo = backendQuiz.displayTo;

    quiz.sourceId = backendQuiz.sourceId;
    quiz.quizConfiguration = backendQuiz.quizConfiguration;
    quiz.questionsList = Question.flatten(backendQuiz.firstAnsweredQuestion || backendQuiz.firstQuestion);

    if (upsell) {
      this.extractUpsellData(upsell, quiz.questionsList);
    }

    if (splashPage) {
      quiz.splashPage = new QuestionEngineSplashPageModel(
        splashPage.strapLine ? this.domSanitizer.bypassSecurityTrustHtml(splashPage.strapLine) : '',
        splashPage.paragraphText1,
        splashPage.paragraphText2,
        splashPage.paragraphText3,
        splashPage.footerText,
        splashPage.footerSvgFilePath ? this.getAbsoluteCmsUrl(splashPage.footerSvgFilePath) : null,
        splashPage.footerSvgFilePath,
        splashPage.logoSvgFilePath ? this.getAbsoluteCmsUrl(splashPage.logoSvgFilePath) : null,
        splashPage.logoSvgFilePath,
        this.ctaButtonText,
        splashPage.loginToViewCTAText,
        splashPage.playForFreeCTAText,
        splashPage.seePreviousSelectionsCTAText,
        splashPage.seeYourSelectionsCTAText,
        splashPage.backgroundSvgFilePath,
        splashPage.showPreviousGamesButton
      );

      quiz.backgroundSvgUrl = this.getAbsoluteCmsUrl(backendQuiz.splashPage.backgroundSvgFilePath);
    }

    quiz.resultsPage = endPage ? new QuestionEngineResultsPageModel(endPage, this.upsellData) : null;

    if (endPage) {
      quiz.resultsPage.backgroundSvgImagePath = this.getAbsoluteCmsUrl(endPage.backgroundSvgImagePath);
    }

    quiz.quizLoginRule = backendQuiz.quizLoginRule;
    quiz.quickLinks = backendQuiz.qeQuickLinks ? backendQuiz.qeQuickLinks.links : [];

    if (defaultQuestionsDetails) {
      quiz.defaultQuestionsDetails = new QuestionEngineQuestionDetailsModel(
        backendQuiz.defaultQuestionsDetails.awayTeamName,
        this.getAbsoluteCmsUrl(backendQuiz.defaultQuestionsDetails.awayTeamSvgFilePath),
        this.getAbsoluteCmsUrl(backendQuiz.defaultQuestionsDetails.channelSvgFilePath),
        backendQuiz.defaultQuestionsDetails.description,
        backendQuiz.defaultQuestionsDetails.homeTeamName,
        this.getAbsoluteCmsUrl(backendQuiz.defaultQuestionsDetails.homeTeamSvgFilePath),
        backendQuiz.defaultQuestionsDetails.middleHeader,
        backendQuiz.defaultQuestionsDetails.signposting,
        backendQuiz.defaultQuestionsDetails.topLeftHeader,
        backendQuiz.defaultQuestionsDetails.topRightHeader,
      );
    }

    quiz.quizLogoSvgFilePath = this.getAbsoluteCmsUrl(backendQuiz.quizLogoSvgFilePath);
    quiz.quizBackgroundSvgFilePath = this.getAbsoluteCmsUrl(backendQuiz.quizBackgroundSvgFilePath);

    quiz.exitPopup = new QuizPopupModel(
      this.getAbsoluteCmsUrl(backendQuiz.exitPopup.iconSvgPath),
      backendQuiz.exitPopup.header,
      backendQuiz.exitPopup.description,
      backendQuiz.exitPopup.submitCTAText,
      backendQuiz.exitPopup.closeCTAText
    );

    quiz.submitPopup = new QuizPopupModel(
      this.getAbsoluteCmsUrl(backendQuiz.submitPopup.iconSvgPath),
      backendQuiz.submitPopup.header,
      backendQuiz.submitPopup.description,
      backendQuiz.submitPopup.submitCTAText,
      backendQuiz.submitPopup.closeCTAText
    );

    Object.keys(backendQuiz.correctAnswersPrizes).forEach(requiredCorrectAnswers => {
      const item = backendQuiz.correctAnswersPrizes[requiredCorrectAnswers];
      quiz.correctAnswersPrizes.push({
        requiredCorrectAnswers: +requiredCorrectAnswers,
        amount: +item.amount,
        currency: item.currency,
        prizeType: item.prizeType
      });
    });
    quiz.eventDetails = backendQuiz.eventDetails;
    quiz.quizConfiguration = backendQuiz.quizConfiguration;

    return quiz;
  }

  /**
   * getAbsoluteCmsUrl method for generate url
   * @return full absolute path from relative
   */
  private getAbsoluteCmsUrl(relativePath: string): string {
    return  relativePath ? `${this.cmsUrl}${relativePath}` : null;
  }

  /**
   * grab all user selected answers Ids and return combined ids
   * collection for right upsell pickup.
   * @param questionsList
   */
  private findAnswersIdsHandler(questionsList: Question[]): string[] {
    const awrsIds = [];
    questionsList.forEach((question: Question ) => {
      question.answers.forEach((answer: IAnswerModel) => {
        if (answer.userChoice) {
          awrsIds.push(answer.id);
        }
      });
    });
    return this.answersIdsCombineHandler(awrsIds);
  }

  /**
   * build combination of user selected answers
   * input ['aa11', 'aa22', 'bb11', 'bb22'] =>
   * output [ 'aa11;aa22', 'aa11;bb11', 'aa11;bb22', 'aa22;bb11', 'aa22;bb22', 'bb11;bb22' ];
   * @param awrsIds
   */
  private answersIdsCombineHandler(awrsIds: string[]): string[] {
    const upsellIds = [];

    awrsIds.forEach((answerId: string, index: number) => {
      awrsIds.forEach((comparedAnswerId: string, comparedIndex: number) => {
        if (awrsIds[comparedIndex + index] && answerId !== awrsIds[comparedIndex + index]) {
          upsellIds.push(`${answerId};${awrsIds[comparedIndex + index]}`);
        }
      });
    });
    return upsellIds;
  }

  /**
   * Find from upsells collection one with matched user
   * answered ids. Return upsell item match or nothing.
   * @param idsList
   * @param dynamicUpsells
   */
  private checkDynamicUpsell(idsList: string[], dynamicUpsells: IUpsellOptions): UpsellItemModel {
    return dynamicUpsells[idsList.find(id => !!dynamicUpsells[id])];
  }

  /**
   * method extract upsell data for results page.
   * if dynamic upsell data exist and CMS ID selections config matches to user selected
   * answers - upsellData will be populated. If no match - default CMS upsell config will be applied.
   * @param upsell
   * @param questionsList
   */
  private extractUpsellData(upsell: IUpsellModel, questionsList: Question[]): void {
    const { defaultUpsellOption, dynamicUpsellOptions, fallbackImagePath, imageUrl } = upsell;

    if (dynamicUpsellOptions && !!Object.keys(dynamicUpsellOptions).length) {
      const idsList = this.findAnswersIdsHandler(questionsList);
      this.upsellData = this.checkDynamicUpsell(idsList, dynamicUpsellOptions);
    }

    if (!this.upsellData && defaultUpsellOption && !!Object.keys(defaultUpsellOption).length) {
      this.upsellData = defaultUpsellOption;
    }
    this.upsellData = {
      ...this.upsellData,
      imageUrl,
      fallbackImagePath: this.getAbsoluteCmsUrl(fallbackImagePath)
    };
  }

  private handleCmsLink(): string {
    const cmsLink = environment.CMS_ROOT_URI;
    return cmsLink.replace(/\/$/, '');
  }
}
