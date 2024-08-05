import {Base} from './base.model';

export interface QualificationRule extends Base {
  daysToCheckActivity: any;
  message: string;
  enabled: boolean;
  blacklistedUsersPath: string;
  recurringUsers?: { [username: string]: boolean };
  recurringUsersList?: RecurringUser[];
}

export interface RecurringUser {
  username: string;
  enabled: boolean;
}
