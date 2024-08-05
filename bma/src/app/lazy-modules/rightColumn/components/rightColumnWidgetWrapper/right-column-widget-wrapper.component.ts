import { Component, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IWidget } from '@core/services/cms/models';

@Component({
  selector: 'right-column-widget-wrapper',
  templateUrl: 'right-column-widget-wrapper.component.html'
})

export class RightColumnWidgetWrapperComponent extends AbstractOutletComponent implements OnInit {
  widgetDataStore: IWidget[] = [];

  constructor(private cms: CmsService) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.cms.getActiveWidgets().subscribe((widgetData: IWidget[]) => {
      _.each(_.keys(widgetData), key => {
        this.widgetDataStore.push(widgetData[key]);
      });
      this.hideSpinner();
    }, () => {
      this.hideSpinner();
    });
  }
}
