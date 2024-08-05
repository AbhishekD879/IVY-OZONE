import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import {
  PromotionIconComponent as AppPromotionIconComponent
} from '@app/promotions/components/promotionIcon/promotion-icon.component';

@Component({
  selector: 'promotion-icon',
  templateUrl: '../../../../../app/promotions/components/promotionIcon/promotion-icon.component.html',
  styleUrls: ['./promotion-icon.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PromotionIconComponent extends AppPromotionIconComponent implements OnInit {

  ngOnInit(): void {
    this.buildYourBetAvailable = false;
    super.ngOnInit();
  }
}
