import { Component, Input } from '@angular/core';

@Component({
  selector: 'show-more',
  templateUrl: 'show-more.component.html'
})

export class ShowMoreComponentComponent {
  @Input() titleText: string;
  @Input() contentText: string;

  showMore: boolean = false;
}
