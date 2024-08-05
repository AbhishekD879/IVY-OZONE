import { finalize } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { IStaticBlock } from '@core/services/cms/models';
import { CmsService } from '@coreModule/services/cms/cms.service';

@Component({
  selector: 'contact-us',
  templateUrl: './contact-us.component.html'
})
export class ContactUsComponent extends AbstractOutletComponent implements OnInit {
  content: IStaticBlock;

  constructor(
    private cmsService: CmsService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit() {
    this.cmsService.getContactUs().pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((content: IStaticBlock) => {
        this.content = content;
      }, () => {
        this.showError();
      });
  }
}
