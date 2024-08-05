import { Component, OnInit } from '@angular/core';
import { SportsModulesService } from '../../sports-modules.service';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { ActivatedRoute, Params } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';

@Component({
  selector: 'app-quick-links-module',
  templateUrl: './quick-links-module.component.html',
  styleUrls: ['./quick-links-module.component.scss']
})
export class QuickLinksModuleComponent implements OnInit {
  module: SportsModule;
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;

  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  loadInitialData(params): void {
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

  // no validation
  isValidModule(): boolean { return true; }

  actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.module.enabled = !this.module.disabled;
        this.sportsModulesService.updateModule(this.module)
          .subscribe((module: SportsModule) => {
            this.module = module;
            this.snackBar.open(`Sports module saved!`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
          });
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
