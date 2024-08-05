import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { CmsService } from '@core/services/cms/cms.service';

@Component({
  selector: 'bog-label',
  templateUrl: './bog-label.component.html',
  styleUrls: ['./bog-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BogLabelComponent implements OnInit {
  @Input() bogLabelStyle: boolean;
  isBogEnabled: boolean;

  constructor(
    protected cmsService: CmsService
  ) {
  }

  ngOnInit(): void {
    this.cmsService.isBogFromCms().subscribe((bog: boolean) => {
      return this.isBogEnabled = bog;
    });
  }

}
