import { Component, ViewEncapsulation } from '@angular/core';
import { OxygenDialogComponent } from '@shared/components/oxygenDialogs/oxygen-dialog.component';

@Component({
  selector: 'oxygen-dialog',
  templateUrl: './oxygen-dialog.component.html',
  styleUrls: ['./oxygen-dialog.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LadbrokesOxygenDialogComponent extends OxygenDialogComponent {
}
