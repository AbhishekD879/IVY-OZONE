import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

@Component({
  selector: 'featured-events-module',
  templateUrl: './featured-events-module.component.html',
  styleUrls: ['./featured-events-module.component.scss']
})
export class FeaturedEventsModuleComponent implements OnInit {
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;
  module: SportsModule;
  isFeaturedEventsActive: boolean;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  
  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  loadInitialData(params: Params): void {
    this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
      .subscribe((moduleData: [SportsModule, SportCategory]) => {
        this.module = moduleData[0];

        // currently featured events modules configurable only for EventHub
        this.isFeaturedEventsActive = this.module.pageType === 'eventhub';
        this.actionButtons?.extendCollection(this.module);
        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }

  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.loadInitialData(this.routeParams);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  save(): void {
    this.sportsModulesService.updateModule(this.module)
      .subscribe((module: SportsModule) => {
        this.module = module;
        this.actionButtons?.extendCollection(this.module);
        this.snackBar.open(`Sports module saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
