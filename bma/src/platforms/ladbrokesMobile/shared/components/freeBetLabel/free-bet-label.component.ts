import { ChangeDetectionStrategy, Component } from '@angular/core';
import { FreeBetLabelComponent as AppFreeBetLabelComponent } from '@app/shared/components/freeBetLabel/free-bet-label.component';

@Component({
  selector: 'free-bet-label',
  templateUrl: '../../../../../app/shared/components/freeBetLabel/free-bet-label.component.html',
  styleUrls: ['../../../../../app/shared/components/freeBetLabel/free-bet-label.scss', './free-bet-label.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class FreeBetLabelComponent extends AppFreeBetLabelComponent {}
