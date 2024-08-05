import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import environment from '@environment/oxygenEnvConfig';
import { IMaintenancePage } from '@core/services/cms/models';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'maintenance',
  templateUrl: 'maintenance.component.html',
  styleUrls: ['maintenance.component.scss']
})
export class MaintenanceComponent implements OnInit, OnDestroy {
  CMS_ROOT_URI: string;
  buttonTarget: string;
  imagePath: string;
  data: IMaintenancePage;

  constructor(
    private activatedRoute: ActivatedRoute,
    private rendererService: RendererService,
    private navigationService: NavigationService,
    private pubSubService: PubSubService
  ) {
    this.CMS_ROOT_URI = environment.CMS_ROOT_URI;
  }

  ngOnInit(): void {
    const maintenanceData: IMaintenancePage = this.data || this.activatedRoute.snapshot.data.data;

    if (!maintenanceData) { return; }

    this.imagePath = this.CMS_ROOT_URI + maintenanceData.uriOriginal;
    this.buttonTarget = maintenanceData.targetUri || '/';

    this.addMaintenanceClass();
    this.pubSubService.subscribe('maintenance',
      this.pubSubService.API.MAINTENANCE_PAGE_DATA_CHANGED, (data: IMaintenancePage) => this.reloadData(data));
  }

  ngOnDestroy(): void {
    this.removeMaintenanceClass();
    this.pubSubService.unsubscribe('maintenance');
  }

  reloadData(data: IMaintenancePage): void {
    this.data = data;
    this.ngOnDestroy();
    this.ngOnInit();
  }

  /**
   * Delegate in-app navigation on image click to service
   */
  reloadOrNavigate(): void {
    this.navigationService.openUrl(this.buttonTarget, true);
  }

  private addMaintenanceClass() {
    this.rendererService.renderer.addClass(document.body, 'maintenance');
  }

  private removeMaintenanceClass() {
    this.rendererService.renderer.removeClass(document.body, 'maintenance');
  }
}


