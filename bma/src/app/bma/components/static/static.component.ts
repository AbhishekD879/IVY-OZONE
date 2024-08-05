import { finalize } from 'rxjs/operators';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { Component, OnInit } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ActivatedRoute } from '@angular/router';
import { IStaticBlock } from '@core/services/cms/models';

@Component({
  selector: 'static',
  templateUrl: './static.component.html'
})
export class StaticComponent extends AbstractOutletComponent implements OnInit {
  content: IStaticBlock;

  constructor(
    private cmsService: CmsService,
    private route: ActivatedRoute,
    private routingState: RoutingState
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit() {
    const staticBlockParams: string = this.routingState.getRouteParam('static-block', this.route.snapshot);

    this.cmsService.getStaticBlock(staticBlockParams, null)
      .pipe(finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((staticBlock: IStaticBlock) => {
        this.content = staticBlock;
      }, () => {
        this.showError();
      });
  }
}
