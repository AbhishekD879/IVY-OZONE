import { Component } from '@angular/core';
import { PromotionsListComponent } from '@app/promotions/components/promotionsList/promotions-list.component';
import { PromotionsService } from '@ladbrokesMobile/promotions/services/promotions/promotions.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'promotions-list',
  templateUrl: './promotions-list.component.html',
  styleUrls: ['promotions-list.component.scss']
})
export class LadbrokesPromotionsListComponent extends PromotionsListComponent {
  constructor(
    public promotionsService: PromotionsService,
    public pubSubService: PubSubService, public userService: UserService, protected bonusSuppressionService: BonusSuppressionService) {
    super(promotionsService, pubSubService, userService, bonusSuppressionService);
  }
}
