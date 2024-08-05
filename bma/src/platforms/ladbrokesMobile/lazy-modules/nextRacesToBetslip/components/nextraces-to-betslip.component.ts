import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
    NextRacesToBetslipComponent as MainNextRacesToBetslipComponent
} from '@app/lazy-modules/nextRacesToBetslip/components/nextraces-to-betslip.component';

@Component({
    selector: 'nextraces-to-betslip',
    templateUrl: 'nextraces-to-betslip.component.html',
    styleUrls: ['./nextraces-to-betslip.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class NextRacesToBetslipComponent extends MainNextRacesToBetslipComponent {

}
