import { Component, OnInit, ViewChild } from '@angular/core';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActivatedRoute, Params } from '@angular/router';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { AppConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-highlight-carousels-module',
  templateUrl: './highlight-carousels-module.component.html'
})

export class HighlightCarouselsModuleComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  public module: SportsModule;
  public breadcrumbsData: Breadcrumb[];
  public routeParams: Params;

  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private snackBar: MatSnackBar
  ) {

  }

  public ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  public loadInitialData(params: Params): void {
    this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
      .subscribe((moduleData: [SportsModule, SportCategory]) => {
        this.module = moduleData[0];

        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }

  public save() {
    this.module.enabled = !this.module.disabled;
    this.sportsModulesService.updateModule(this.module)
      .subscribe((module: SportsModule) => {
        this.module = module;
        this.actionButtons.extendCollection(this.module);
        this.snackBar.open(`Sports module saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  public actionsHandler(event: string): void {
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
}
