import { Component } from '@angular/core';
import {FiveASideOddsViewComponent
    as AppFiveASideOddsViewComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideOddsView/fiveaside-oddsview.component';
import { FracToDecService } from '@app/core/services/fracToDec/frac-to-dec.service';

@Component({
    selector: 'fiveaside-oddsview',
    templateUrl: './fiveaside-oddsview.component.html'
})
export class FiveASideOddsViewComponent extends AppFiveASideOddsViewComponent {
    constructor(public fracToDecService: FracToDecService) {
       super(fracToDecService);
    }
}
