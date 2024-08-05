import { Component, Input } from '@angular/core';
import { IShowdownCardDetails, IShowdownCardSignPostings } from '@app/fiveASideShowDown/models/showdown-card.model';

@Component({
  selector: 'fiveaside-sign-posting',
  template: ``
})
export class FiveASideSignPostingComponent {
  @Input() signPostingsInfo: IShowdownCardSignPostings;
  @Input() contestDetails: IShowdownCardDetails;
}
