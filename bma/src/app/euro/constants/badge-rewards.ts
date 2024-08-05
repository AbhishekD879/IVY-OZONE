import { IBadgeRewards } from '@app/euro/models/euro.model';

export class BadgeRewards implements IBadgeRewards {
    badgeType: string = '';
    yellowHighlight: boolean = false;
    message: string[] = [];
    freeBetToken: string = '';
  }
