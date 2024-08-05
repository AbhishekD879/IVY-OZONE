import {
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { StreamBetService } from '@lazy-modules/eventVideoStream/services/streamBet/stream-bet.service';


@Component({
  selector: 'stream-bet-templates',
  templateUrl: './stream-bet-templates.component.html',
  styleUrls: ['./stream-bet-templates.component.scss']
})
export class StreamBetTemplatesComponent {
@Input() market: any; // IMarket; remove later
@Input() eventEntity: ISportEvent;
@Input() allMarkets: IMarket[];
@Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();

constructor(
  private streamBetService: StreamBetService
){}

  getMarketTemplate(currentMarket: IMarket, eventEntity: ISportEvent): string {
    return this.streamBetService.getMarketTemplate(currentMarket, eventEntity);
  }

  handleSelectionClick(market: IMarket) {
    this.selectionClickEmit.emit(market);
  }

}