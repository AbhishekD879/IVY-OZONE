import { Component, Input } from '@angular/core';

@Component({
  selector: 'outlet-status',
  templateUrl: 'outlet-status.component.html'
})
export class OutletStatusComponent {
  @Input() state: {
    loading: boolean;
    error: boolean;
  };
  @Input() isUsedFromWidget: boolean = false;
  @Input() skeletonType: string = 'GENERIC';
}
