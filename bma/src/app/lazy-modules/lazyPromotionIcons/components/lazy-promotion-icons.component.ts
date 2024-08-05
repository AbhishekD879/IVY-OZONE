import {
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output
} from '@angular/core';
import { PromotionIconComponent } from '@app/promotions/components/promotionIcon/promotion-icon.component';
import { ISystemConfig } from '@app/core/services/cms/models';
import { SECTION_TYPE } from '@promotions/constants/promotion-description';

@Component({
  selector: 'lazy-promotion-icons',
  templateUrl: './lazy-promotion-icons.component.html',
  styleUrls: ['./lazy-promotion-icons.component.scss']
})
export class LazyPromotionIconsComponent extends PromotionIconComponent implements OnInit {
  @Input() isLazyBIRSignpost: boolean = false;
  @Input() iconsCount: number = 0;
  @Output() iconCountUpdated: EventEmitter<number> = new EventEmitter();

  isDisplayBIRSignpost: boolean = false;
  isBIRAvailable: boolean = false;

  ngOnInit(): void {
    super.ngOnInit();
    if (this.showBIRSignPost && this.isLazyBIRSignpost) {
      const isMarketType = this.type && this.type.toLocaleLowerCase() === SECTION_TYPE.MARKET;
      const drillDowngTags = (isMarketType && this.eventDrillDownTags) || this.display;
      this.isBIRAvailable = this.isHeaderBIRAvailable || this.parseFlags(drillDowngTags).includes(this.BIR_FLAG);
      if (this.isBIRAvailable) {
        this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
          const isBIRCurrentMarketEnabled = isMarketType
            && config?.HorseRacingBIR?.marketsEnabled?.some((market: string) => this.marketName?.toLocaleLowerCase() === market.toLocaleLowerCase());
          this.isDisplayBIRSignpost = config?.HorseRacingBIR?.inplaySignpostEnabled
            && (isBIRCurrentMarketEnabled || !isMarketType);
          this.isDisplayBIRSignpost && this.iconCountUpdated.emit(1);
        });
      }
    }
  }
}
