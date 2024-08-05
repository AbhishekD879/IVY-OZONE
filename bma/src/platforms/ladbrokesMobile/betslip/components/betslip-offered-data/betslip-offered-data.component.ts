import { ChangeDetectionStrategy, Component } from '@angular/core';
import {
  BetslipOfferedDataComponent as AppBetslipOfferedDataComponent
} from '@betslip/components/betslipOfferedData/betslip-offered-data.component';

@Component({
  selector: 'betslip-offered-data',
  templateUrl: '../../../../../app/betslip/components/betslipOfferedData/betslip-offered-data.component.html',
  styleUrls: ['./betslip-offered-data.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BetslipOfferedDataComponent extends AppBetslipOfferedDataComponent {}
