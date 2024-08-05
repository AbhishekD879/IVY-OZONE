import {Component, Input} from '@angular/core';

@Component({
  selector: 'header-activity-badge',
  templateUrl: './activity.badge.component.html',
  styleUrls: ['./activity.badge.component.scss']
})
export class HeaderActivityBadgeComponent {
  @Input() state: boolean;

  constructor() {}

  /* tslint:disable */
  // Maksym Shturmin
  ngOnInit() {}
  /* tslint:enable */
}
