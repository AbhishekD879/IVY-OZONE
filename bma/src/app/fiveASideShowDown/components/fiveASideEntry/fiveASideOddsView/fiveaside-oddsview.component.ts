import { Component, Input, OnInit, SimpleChanges, OnChanges } from '@angular/core';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Component({
    selector: 'fiveaside-oddsview',
    templateUrl: './fiveaside-oddsview.component.html'
})
export class FiveASideOddsViewComponent implements OnInit, OnChanges {
    @Input() summary: IEntrySummaryInfo;
    public odds: string;
    constructor(protected fracToDecService: FracToDecService) {
    }
    ngOnInit() {
        this.oddsFormat();
    }
    ngOnChanges(change: SimpleChanges) {
        if (change.summary) {
            this.oddsFormat();
        }
    }

    /**
     * oddsFormat to '@2/4','@8/9'
     * @returns void
     */
    protected oddsFormat(): void {
        this.odds = `@${this.fracToDecService.getFormattedValue(Number(this.summary.priceNum), Number(this.summary.priceDen))}`;
    }
}
