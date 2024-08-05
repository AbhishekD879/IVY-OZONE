import { Component } from '@angular/core';
import { CmsService } from '@ladbrokesMobile/core/services/cms/cms.service';
import { PromoLabelsComponent } from '@promotions/components/promoLabels/promo-labels.component';
@Component({
  selector: 'promo-labels',
  styleUrls: ['./promo-labels.component.scss'],
  templateUrl: 'promo-labels.component.html'
})

export class LadbrokesPromoLabelsComponent extends PromoLabelsComponent {

  constructor(
    cmsService: CmsService
  ) {
    super(cmsService);
  }
}
