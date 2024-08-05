import { Component, Input, OnInit } from '@angular/core';

import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';

@Component({
  selector: 'yourcall-icon',
  templateUrl: 'your-call-icon.component.html'
})
export class YourCallIconComponent implements OnInit {
  @Input() typeId: number;
  @Input() events?: ISportEvent[];
  @Input() display?: string;

  isYcAvailable: boolean = false;
  isBybAvailable: boolean = false;

  constructor(
    private yourCallService: YourcallService,
    private promotionsService: PromotionsService,
  ) {}

  ngOnInit(): void {
    if (this.display === 'general') {
      this.yourCallService.whenYCReady('isEnabledYCIcon')
        .subscribe(() => {
          this.isBybAvailable = this.yourCallService.isBYBIconAvailable(this.typeId);
          this.isYcAvailable = this.yourCallService.isYCIconAvailable(this.events);
        });
    } else {
      this.isYcAvailable = false;
      this.isBybAvailable = false;
    }
  }

  /**
   * On click yourCall icon action
   * @param event
   */
  iconAction(event: Event): void {
    event.stopPropagation();
    this.promotionsService.openPromotionDialog('YOUR_CALL');
  }
}


