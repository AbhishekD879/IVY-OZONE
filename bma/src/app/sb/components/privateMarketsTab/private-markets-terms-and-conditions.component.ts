import { finalize } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IStaticBlock } from '@core/services/cms/models';

@Component({
  selector: 'private-markets-terms-and-conditions',
  templateUrl: './private-markets-terms-and-conditions.html'
})
export class PrivateMarketsTermsAndConditionsComponent extends AbstractOutletComponent implements OnInit {
  privateMarketsTermsAndConditionsText: IStaticBlock;

  constructor(private cms: CmsService) {
    super();
  }

  ngOnInit(): void {
    this.cms.getPrivateMarketsTermsAndConditions().pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((data: IStaticBlock) => {
        this.privateMarketsTermsAndConditionsText = data;
      }, () => {
        this.showError();
      });
  }
}
