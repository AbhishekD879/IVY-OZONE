import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {
  HttpClient,
  HttpResponse
} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {QualificationRule} from '@app/client/private/models/qualificationRule.model';

@Injectable()
export class QualificationRuleService extends AbstractService<Configuration> {
  byBrandUrl: string = `qualification-rule/brand/${this.brand}`;
  rootUrl: string = 'qualification-rule';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOneByBrand(): Observable<HttpResponse<QualificationRule>> {
    return this.sendRequest<QualificationRule>('get', this.byBrandUrl, null);
  }

  public saveRule(qualificationRule: QualificationRule): Observable<HttpResponse<QualificationRule>> {
    return this.sendRequest<QualificationRule>('post', this.rootUrl, qualificationRule);
  }

  public updateRule(qualificationRule: QualificationRule): Observable<HttpResponse<QualificationRule>> {
    return this.sendRequest<QualificationRule>('put', `${this.rootUrl}/${qualificationRule.id}`, qualificationRule);
  }

  public uploadBlacklistedUsers(file: FormData): Observable<HttpResponse<QualificationRule>> {
    const uri = `${this.rootUrl}/${this.brand}/blacklist`;
    return this.sendRequest<QualificationRule>('post', uri, file);
  }
}
