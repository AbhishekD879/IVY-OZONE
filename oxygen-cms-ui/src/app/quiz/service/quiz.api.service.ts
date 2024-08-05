import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Quiz} from '@app/client/private/models/quiz.model';

@Injectable()
export class QuizApiService {

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate) {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }

  hideLoader() {
    this.globalLoaderService.hideLoader();
  }

  getQuizzes() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService().getQuizzes();
    return this.wrappedObservable(data);
  }

  getQuizzesByBrand() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService().getQuizzesByBrand();
    return this.wrappedObservable(data);
  }

  getQuiz(id: string) {
    const data = this.apiClientService.quizService().getSingleQuiz(id);
    return this.wrappedObservable(data);
  }

  createQuiz(quiz: Quiz) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService().postNewQuiz(quiz);
    return this.wrappedObservable(data);
  }

  updateQuiz(quiz: Quiz) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService().putQuizChanges(quiz.id, quiz);
    return this.wrappedObservable(data);
  }

  deleteQuiz(id: string) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService().deleteQuiz(id);
    return this.wrappedObservable(data);
  }

  getQuestion(quizId: string, questionId: string) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService().getQuestionById(quizId, questionId);
    return this.wrappedObservable(data);
  }


  deleteFallbackImage(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.splashPageService().deleteSplashPage(id);
    return this.wrappedObservable(data);
  }

  uploadFallbackImage(id: string, image: File): Observable<any> {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('fallback-image', image);
    const data = this.apiClientService.quizService().uploadFallbackImage(id, formData);
    return this.wrappedObservable(data);
  }

  uploadQuestionDetailsImages(quizId: string, questionId: string, home: File, away: File, channel: File) {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    if (home) {
      formData.append('home', home);
    }
    if (away) {
      formData.append('away', away);
    }
    if (channel) {
      formData.append('channel', channel);
    }
    const data = this.apiClientService.quizService().uploadQuestionDetailsImages(quizId, questionId, formData);
    return this.wrappedObservable(data);
  }

  uploadQuizLogoImage(quizId: string, quizLogo: File) {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('file', quizLogo);
    const data = this.apiClientService.quizService().uploadQuizLogoImage(quizId, formData);
    return this.wrappedObservable(data);
  }

  uploadQuizBackgroundImage(quizId: string, quizBackground: File) {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('file', quizBackground);
    const data = this.apiClientService.quizService().uploadQuizBackgroundImage(quizId, formData);
    return this.wrappedObservable(data);
  }

  deleteQuizLogoImage(quizId: string) {
    this.globalLoaderService.showLoader();

    const data = this.apiClientService.quizService().deleteQuizLogoImage(quizId);
    return this.wrappedObservable(data);
  }

  deleteQuizBackgroundImage(quizId: string) {
    this.globalLoaderService.showLoader();

    const data = this.apiClientService.quizService().deleteQuizBackgroundImage(quizId);
    return this.wrappedObservable(data);
  }

  uploadDefaultQuestionDetailsImage(quizId: string, file: File, fileType: string) {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    if (fileType === 'home') {
      formData.append('home', file);
    }
    if (fileType === 'away') {
      formData.append('away', file);
    }
    if (fileType === 'channel') {
      formData.append('channel', file);
    }
    const data = this.apiClientService.quizService().uploadDefaultQuestionDetailsImage(quizId, formData);
    return this.wrappedObservable(data);
  }

  deleteDefaultQuestionDetailsImage(quizId: string, imageType: string) {
    this.globalLoaderService.showLoader();

    const data = this.apiClientService.quizService().deleteDefaultQuestionDetailsImage(quizId, imageType);
    return this.wrappedObservable(data);
  }

  uploadPopupIconImage(quizId: string, popupIcon: File, popupType: string) {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('file', popupIcon);

    let requestPopupType = '';
    if ('submit' === popupType) {
      requestPopupType = 'submit';
    } else if ('exit' === popupType) {
      requestPopupType = 'exit';
    }
    const data = this.apiClientService.quizService().uploadPopupIconImage(quizId, formData, requestPopupType);
    return this.wrappedObservable(data);
  }

  deletePopupIconImage(quizId: string, popupType: string) {
    this.globalLoaderService.showLoader();

    let requestPopupType = '';
    if ('submit' === popupType) {
      requestPopupType = 'submit';
    } else if ('exit' === popupType) {
      requestPopupType = 'exit';
    }
    const data = this.apiClientService.quizService().deletePopupIconImage(quizId, requestPopupType);
    return this.wrappedObservable(data);
  }

  generateQuestionSummaryReport(quizId: string) {
    const data = this.apiClientService.quizService().generateQuestionSummaryReport(quizId);

    return this.wrappedObservable(data);
  }
}

