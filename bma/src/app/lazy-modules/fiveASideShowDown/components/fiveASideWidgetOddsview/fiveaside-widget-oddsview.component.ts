import { ChangeDetectionStrategy, Component, OnChanges, SimpleChanges } from '@angular/core';
import { FiveASideOddsViewComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideOddsView/fiveaside-oddsview.component';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Component({
  selector: 'fiveaside-widget-oddsview',
  templateUrl: './fiveaside-widget-oddsview.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveasideWidgetOddsviewComponent extends FiveASideOddsViewComponent implements OnChanges {

  constructor(protected fracToDecService: FracToDecService) {
    super(fracToDecService);
  }

  ngOnChanges(change: SimpleChanges) {
    if (change.summary) {
      this.oddsFormat();
    }
  }
}
