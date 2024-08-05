import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Quiz} from '@app/client/private/models/quiz.model';
import {Question} from '@app/client/private/models/question.model';

@Injectable()
export class QuizService extends AbstractService<Configuration> {
  quizBaseUrl: string = 'question-engine';
  quizByBrandUrl: string = `question-engine/brand/${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getQuizzes(): Observable<HttpResponse<Quiz[]>> {
    return this.sendRequest<Quiz[]>('get', this.quizBaseUrl, null);
  }

  public getQuizzesByBrand(): Observable<HttpResponse<Quiz[]>> {
    return this.sendRequest<Quiz[]>('get', this.quizByBrandUrl, null);
  }

  public getSingleQuiz(id: string): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${id}`;
    return this.sendRequest<Quiz>('get', url, null);
  }

  public postNewQuiz(quiz: Quiz): Observable<HttpResponse<Quiz>> {
    return this.sendRequest<Quiz>('post', this.quizBaseUrl, quiz);
  }

  public putQuizChanges(id: string, quiz: Quiz): Observable<HttpResponse<Quiz>> {
    const apiUrl = `${this.quizBaseUrl}/${id}`;
    return this.sendRequest<Quiz>('put', apiUrl, quiz);
  }

  public deleteQuiz(id: string): Observable<HttpResponse<void>> {
    const url = `${this.quizBaseUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }

  public getQuestionById(quizId: string, questionId: string): Observable<HttpResponse<Question>> {
    const url = `${this.quizBaseUrl}/question/${quizId}/${questionId}`;
    return this.sendRequest<Question>('get', url, null);
  }

  public deleteFallbackImage(id: string): Observable<HttpResponse<void>> {
    const url = `${this.quizBaseUrl}/${id}/upsell/upload-fallback-image`;
    return this.sendRequest<void>('delete', url, null);
  }

  public uploadFallbackImage(id: string, file: FormData): Observable<HttpResponse<void>> {
    const url = `${this.quizBaseUrl}/${id}/upsell/upload-fallback-image`;
    return this.sendRequest<void>('post', url, file);
  }

  public uploadQuestionDetailsImages(quizId: string, questionId: string, file: FormData): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${this.brand}/question/${quizId}/${questionId}/question-details-images`;
    return this.sendRequest<Quiz>('post', url, file);
  }

  public uploadQuizLogoImage(quizId: string, file: FormData): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${this.brand}/${quizId}/quiz-logo-image`;
    return this.sendRequest<Quiz>('post', url, file);
  }

  public uploadQuizBackgroundImage(quizId: string, file: FormData): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${this.brand}/${quizId}/quiz-background-image`;
    return this.sendRequest<Quiz>('post', url, file);
  }

  public deleteQuizLogoImage(quizId: string): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${quizId}/quiz-logo-image`;
    return this.sendRequest<Quiz>('delete', url, null);
  }

  public deleteQuizBackgroundImage(quizId: string): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${quizId}/quiz-background-image`;
    return this.sendRequest<Quiz>('delete', url, null);
  }

  public uploadDefaultQuestionDetailsImage(quizId: string, file: FormData): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${this.brand}/${quizId}/default-questions-details-images`;
    return this.sendRequest<Quiz>('post', url, file);
  }

  public deleteDefaultQuestionDetailsImage(quizId: string, imageType: string): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${quizId}/default-questions-details-images/${imageType}`;
    return this.sendRequest<Quiz>('delete', url, null);
  }

  public uploadPopupIconImage(quizId: string, file: FormData, popupType: string): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${this.brand}/${quizId}/popup-icon/${popupType}`;
    return this.sendRequest<Quiz>('post', url, file);
  }

  public deletePopupIconImage(quizId: string, popupType: string): Observable<HttpResponse<Quiz>> {
    const url = `${this.quizBaseUrl}/${quizId}/popup-icon/${popupType}`;
    return this.sendRequest<Quiz>('delete', url, null);
  }

  public generateQuestionSummaryReport(quizId: string): Observable<HttpResponse<any>> {
    const url = `${this.quizBaseUrl}/${quizId}/report/questions-summary`;

    return this.sendRequest<Quiz>('get', url, null);
  }
}
