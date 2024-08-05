import { Component, Input } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
@Component({
    selector: 'single-markets',
    templateUrl: './single-markets.component.html',
    styleUrls : ['./single-markets.component.scss']
})
export class SingleMarketsComponent {

    @Input() eventEntity: ISportEvent;
    @Input() market: IMarket;

    getTrackById(index: number, entity: any) {
        return `${entity.id}_${index}`;
    }
    
    toggleShowAll(marketEntity: IMarket){
        marketEntity.isAllShown = !marketEntity.isAllShown;
    }
}