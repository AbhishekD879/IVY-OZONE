import { Component, Input } from '@angular/core';
import { EURO_MESSAGES } from '@app/euro/constants/euro-constants';

@Component({
  selector: 'terms-and-cond',
  templateUrl: './terms-and-cond.component.html',
  styleUrls: ['./terms-and-cond.component.scss']
})
export class TermsAndCondComponent {

  @Input() public termsAndConditions: string;
  @Input() public fullTermsURI: string;
  public readonly TERMS_AND_COND: string = EURO_MESSAGES.TERMS_AND_COND;
  public readonly FULL_TERMS_AND_COND: string = EURO_MESSAGES.FULL_TERMS_AND_COND;
  constructor() { }
}
