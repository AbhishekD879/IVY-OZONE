import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';

@Component({
  selector: 'empty-betslip',
  templateUrl: './empty-betslip.component.html',
  styleUrls: ['./empty-betslip.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class EmptyBetslipComponent {
  @Input() showButton: boolean;

  constructor(
    private router: Router,
    private pubSubService: PubSubService,
    public serviceClosureService: ServiceClosureService
  ) {}

  goToHomePage(): void {
    this.router.navigate(['/']);
    this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
  }
}
