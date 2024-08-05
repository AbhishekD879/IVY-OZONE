import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { WidgetsService } from '@desktop/components/widgets/widgets.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IWidgetConfig, IWigetsConfigsData } from '@desktop/models/wigets.model';
import { ISportConfigurationTabs } from '@sb/models/sport-configuration.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';

@Component({
  selector: 'widgets',
  templateUrl: './widgets.component.html'
})
export class WidgetsComponent implements OnInit, OnDestroy, OnChanges {
  @Input() sportConfig: ISportConfigurationTabs[];
  @Input() sportActiveTab: string;
  @Input() sportName: string;
  @Input() sportDetailPage: string;
  //changed type of below property for strict mode issue
  @Input() params: any;

  isShowColumn: boolean = false;
  activeWidgets: IWidgetConfig = {};

  private widgets: IWigetsConfigsData;

  constructor(
    private widgetsService: WidgetsService,
    private pubSubService: PubSubService,
    private cms: CmsService
  ) {
  }

  ngOnInit(): void {
    this.widgets = this.widgetsService.getConfig(this.sportConfig);
    this.widgetsService.activeWidgets = {};

    this.pubSubService.subscribe('WidgetsController', this.pubSubService.API.WIDGET_VISIBILITY, widget => {
      if (widget && this.widgetsService.activeWidgets.hasOwnProperty(Object.keys(widget)[0])) {
        this.isShowColumn = this.widgetsService.getWidgetsVisibility(widget);
      }
    });

    this.cms.getSystemConfig(false).subscribe((data: ISystemConfig) => {
      this.widgets['tab-matches'] = {
        inPlay: data.DesktopWidgetsToggle && data.DesktopWidgetsToggle.inPlay ? data.DesktopWidgetsToggle.inPlay : false,
        liveStream: data.DesktopWidgetsToggle && data.DesktopWidgetsToggle.liveStream ? data.DesktopWidgetsToggle.liveStream : false
      };

      this.setWidgetsVisibility();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('WidgetsController');
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.sportActiveTab && changes.sportActiveTab.previousValue) {
      this.setWidgetsVisibility();
    }
  }

  setWidgetsVisibility(): void {
    this.activeWidgets = this.widgets[this.sportActiveTab || this.sportDetailPage];
    this.widgetsService.activeWidgets = this.activeWidgets;
    this.isShowColumn = this.widgetsService.getWidgetsVisibility(this.activeWidgets);
  }
}
