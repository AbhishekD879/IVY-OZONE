import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { FiltersService } from '@core/services/filters/filters.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { DeviceService } from '@core/services/device/device.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { bs } from '@app/lazy-modules/locale/translations/en-US/bs.lang';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
@Component({
  selector: 'free-bet-label',
  templateUrl: './free-bet-label.component.html',
  styleUrls: ['./free-bet-label.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FreeBetLabelComponent {
  value: string;
  isDesktop: boolean;
  isFanzone:boolean;
  readonly betTokenName = bma.betToken.toUpperCase();
  readonly freeBetName = bma.freeBet.toUpperCase();

  @Input() plusPrefix: boolean;
  @Input() plusSuffix: boolean;
  @Input() margin: boolean;
  @Input() jump: string;
  @Input() freeBetLabelText: string;

  isStreamAndBet: boolean;

  constructor(
    private filtersService: FiltersService,
    private device: DeviceService,
    private fbService: FreeBetsService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService) {
    this.isDesktop = this.device.isDesktop;
    this.isStreamAndBet = this.eventVideoStreamProviderService.isStreamAndBet;
  }
  @Input()
  set selected(val: number|string) {
    if(this.isStreamAndBet) {
      this.value = this.setcurrency(val);
    } else {
      this.value = this.setcurrency(val) + ' ' + (this.freeBetLabelText ? this.getFreebetLabelText() : bs.freeBet);
    }
    this.isFanzone = this.fbService.isFanzone(this.freeBetLabelText);

  }
  get selected() {
    return this.value;
  }
  setcurrency(val){
     return val % 1 != 0?this.filtersService.setCurrency(val) :this.filtersService.setFreebetCurrency(val) ;

  }
   public getFreebetLabelText(): string {
    return this.fbService.isBetPack(this.freeBetLabelText) ? bs.betToken : this.fbService.isFanzone(this.freeBetLabelText) ?bs.fanZoneFreebet:this.freeBetLabelText;
  }
}
