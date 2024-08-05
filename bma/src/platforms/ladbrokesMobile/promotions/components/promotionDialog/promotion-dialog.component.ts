import { Component } from '@angular/core';

import { PromotionDialogComponent as AppPromotionDialogComponent } from '@promotions/components/promotionDialog/promotion-dialog.component';

@Component({
  selector: 'promotion-overlay-dialog',
  templateUrl: './promotion-dialog.component.html'
})
export class PromotionDialogComponent extends AppPromotionDialogComponent {}
