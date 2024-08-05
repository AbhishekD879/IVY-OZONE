import { ChangeDetectionStrategy, Component } from "@angular/core";
import { OnBoardingFirstBetComponent as CoralOnBoardingFirstBetComponent } from "@app/lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-placement.component";

@Component({
    selector: 'first-bet-placement',
    templateUrl: './../../../../../../app/lazy-modules/onBoardingTutorial/firstBetPlacement/components/first-bet-placement.component.html',
    styleUrls: ['./first-bet-placement.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
  })

export class LadbrokesOnBoardingFirstBetComponent extends CoralOnBoardingFirstBetComponent {

}