import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {
  HttpClient,
  HttpResponse
} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {QuizPopupConfig} from '@app/client/private/models/quizPopupConfig.model';

@Injectable()
export class QuizPopupService extends AbstractService<Configuration> {
  byBrandUrl: string = `quiz-popup-setting/brand/${this.brand}`;
  rootUrl: string = 'quiz-popup-setting';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOneByBrand(): Observable<HttpResponse<QuizPopupConfig>> {
    return this.sendRequest<QuizPopupConfig>('get', this.byBrandUrl, null);
  }

  public saveConfig(qualificationRule: QuizPopupConfig): Observable<HttpResponse<QuizPopupConfig>> {
    return this.sendRequest<QuizPopupConfig>('post', this.rootUrl, qualificationRule);
  }

  public updateConfig(qualificationRule: QuizPopupConfig): Observable<HttpResponse<QuizPopupConfig>> {
    return this.sendRequest<QuizPopupConfig>('put', `${this.rootUrl}/${qualificationRule.id}`, qualificationRule);
  }
}
