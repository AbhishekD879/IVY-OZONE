import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {QualificationRule} from '@app/client/private/models/qualificationRule.model';

@Injectable()
export class QualificationRuleAPIService {
  constructor(private globalLoaderService: GlobalLoaderService,
              private apiClientService: ApiClientService) {
  }

  getOneByBrand(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.qualificationRuleService().getOneByBrand();

    return this.wrappedObservable(getData);
  }

  create(qualificationRule: QualificationRule) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.qualificationRuleService().saveRule(qualificationRule);
    return this.wrappedObservable(getData);
  }

  update(qualificationRule: QualificationRule) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.qualificationRuleService().updateRule(qualificationRule);
    return this.wrappedObservable(getData);
  }

  uploadBlacklistedUsers(file: File) {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('file', file);
    const data = this.apiClientService.qualificationRuleService().uploadBlacklistedUsers(formData);
    return this.wrappedObservable(data);
  }

  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
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
}
