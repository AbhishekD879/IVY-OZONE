import { Injectable } from '@angular/core';

import { IQuickbetNotificationModel } from '@app/quickbet/models/quickbet-notification.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Subject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class QuickbetNotificationService {
  private model: IQuickbetNotificationModel = {
    msg: '',
    type: '',
    location: ''
  };

  snbMaxPayoutMsgSub: Subject<string> =  new Subject<string>();

  constructor(private pubsub: PubSubService) {}

  /**
   * Panel model
   * @returns {{msg: string, type: string, location: string}}
   */
  get config() {
    return this.model;
  }
  set config(value:any){}

  /**
   * Save error message with code
   * @param {string} message
   * @param {string} type
   * @param {string} location
   * @param {string} errorCode
   */
  saveErrorMessageWithCode(message: string, type: string = 'warning', location: string = '', errorCode: string = '') {
    this.updateModel(this.model, { msg: message, type, location, errorCode });
    this.publishQuickbetInfoPanel();
  }

  /**
   * Save error message
   * @param {string} message
   * @param {string} type
   * @param {string} location
   */
  saveErrorMessage(message: string, type: string = 'warning', location: string = ''): void {
    this.updateModel(this.model, { msg: message, type, location, errorCode: '' });
    this.publishQuickbetInfoPanel();
  }

  /**
   * Clear model
   * @param {string} location
   */
  clear(location: string = ''): void {
    this.updateModel(this.model, { msg: '', type: '', location: location, errorCode: '' });
    this.publishQuickbetInfoPanel();
  }

  private publishQuickbetInfoPanel() {
    this.pubsub.publish(this.pubsub.API.QUICKBET_INFO_PANEL, Object.assign({}, this.model));
  }

  private updateModel(model: IQuickbetNotificationModel, { msg, type, location, errorCode }: IQuickbetNotificationModel): void {
    model.type = type;
    model.msg = msg;
    model.location = location;
    model.errorCode = errorCode;
  }
}
