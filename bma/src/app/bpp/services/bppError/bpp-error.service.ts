import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { serverDictionary } from '../../constants/bpp-server-dictionary.constant';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { IErrorResponse, IErrorDataParsed } from './bpp-error.model';
import { BppErrorDialogComponent } from '@sharedModule/components/bppErrorDialog/bpp-error-dialog.component';

@Injectable()
export class BppErrorService {

  constructor(
    private dialogService: DialogService
  ) { }

  /**
   * Parse error and create object with debug message && code of error.
   * @param {Object} response, response from $resource.
   * @return {Object} in format {code: 'XXX', msg: 'serviceUrl + Server code + Status message'}.
   */
  errorDataParser(response: IErrorResponse): IErrorDataParsed {
    const code: string = String(response.data.code);
    const status: string = response.data.status;
    const service: string = response.config.url;
    return {
      code: code.slice(1),
      msg: `${service}\nError occured by ${serverDictionary.code[code[0]]}. Reason: ${serverDictionary.status[status] || status}`
    };
  }

  /**
   * Parse error and show it into the console.
   * @param {Object} response, response from $resource.
   */
  errorHandler(response: IErrorResponse): void {
    if (response && response.data && response.config) {
      const parsedObj = this.errorDataParser(response);
      console.error(parsedObj.msg);
    }
  }

  /**
   * Error Handling for provided cases.
   * @param {Object} response
   */
  showPopup(response: IErrorResponse | string): void {
    let errorKey;

    if (_.isString(response)) {
      errorKey = response;
    } else {
      const error = response && ((response.error && response.error.error) || (response.data && response.data.error));
      errorKey = error === 'Connection timeout' ? 'betPlacementTimeoutError' : 'betPlacementError';
    }

    this.dialogService.openDialog(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true, {
      error: errorKey
    });
  }
}
