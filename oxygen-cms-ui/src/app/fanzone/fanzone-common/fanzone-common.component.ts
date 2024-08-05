import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Fanzone } from '@app/client/private/models/fanzone.model';
import { FANZONE_DETAILS } from '@app/fanzone/constants/fanzone.constants';

@Component({
  selector: 'app-fanzone-common',
  templateUrl: './fanzone-common.component.html'
})
export class FanzoneCommonComponent {
  public readonly FANZONE_DETAILS = FANZONE_DETAILS;
  @Input() fanzone: Fanzone;
  @Input() form: FormGroup;

  constructor() { }

}
