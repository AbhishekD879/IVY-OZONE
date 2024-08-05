import { Directive, HostListener, Input } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Directive({
  // eslint-disable-next-line
  selector: '[trigger]'
})
export class TriggerDirective {
  @Input() triggerArgs: string | {};
  @Input() trigger: string;

  constructor(private pubSubService: PubSubService) {}

  @HostListener('click', ['$event'])
  onClick($event: MouseEvent): void {
    $event.preventDefault();

    this.pubSubService.publish(this.trigger, this.triggerArgs);
  }
}
