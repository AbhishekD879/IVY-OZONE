import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { CmsService } from '@core/services/cms/cms.service';
import { BogLabelComponent } from '@shared/components/bogLabel/bog-label.component';

@Component({
  selector: 'bog-label',
  templateUrl: './bog-label.component.html',
  styleUrls: ['./bog-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesBogLabelComponent extends BogLabelComponent implements OnInit {
  constructor(
    protected cmsService: CmsService
  ) {
    super(cmsService);
  }
}
