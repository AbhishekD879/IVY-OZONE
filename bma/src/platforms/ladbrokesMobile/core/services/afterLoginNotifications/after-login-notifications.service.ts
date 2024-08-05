import { Injectable } from '@angular/core';

import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { UserService } from '@core/services/user/user.service';
import { IteratorService } from '@core/services/iterator/iterator.service';
import { Iterator } from '@core/services/iterator/iterator.class';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Location } from '@angular/common';
import {
  AfterLoginNotificationsService as AppAfterLoginNotificationsService
} from '@app/core/services/afterLoginNotifications/after-login-notifications.service';

@Injectable()
export class AfterLoginNotificationsService extends AppAfterLoginNotificationsService {
  constructor(
    freeBetsService: FreeBetsService,
    command: CommandService,
    user: UserService,
    iteratorService: IteratorService,
    pubSubService: PubSubService,
    cmsService: CmsService,
    location: Location
  ) {
    super(
      freeBetsService,
      command,
      user,
      iteratorService,
      pubSubService,
      cmsService,
      location,
    );
  }

  /**
   * Override method which skip freebet info table on successful login
   * @param {Iterator} iterator
   * @returns {void}
   */
  protected freeBetInfoShow(iterator: Iterator): void  {
      iterator.next();
  }
}
