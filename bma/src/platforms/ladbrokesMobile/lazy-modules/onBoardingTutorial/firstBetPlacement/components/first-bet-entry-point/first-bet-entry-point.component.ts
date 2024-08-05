import { ChangeDetectionStrategy, Component } from "@angular/core";
import { FirstBetEntryPointComponent as CoralFirstBetEntryPointComponent } from "@app/lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-entry-point/first-bet-entry-point.component";

@Component({
    selector: 'first-bet-entry-point',
    templateUrl: './../../../../../../../app/lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-entry-point/first-bet-entry-point.component.html',
    styleUrls: ['./first-bet-entry-point.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})

export class LadbrokesFirstBetEntryPointComponent extends CoralFirstBetEntryPointComponent {

}