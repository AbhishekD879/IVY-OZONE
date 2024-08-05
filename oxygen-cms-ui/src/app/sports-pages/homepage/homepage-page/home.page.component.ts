import { Component, OnInit } from '@angular/core';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { AppConstants } from '@app/app.constants';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { Order } from '@app/client/private/models/order.model';

@Component({
  selector: 'home-page',
  templateUrl: './home.page.component.html',
  styleUrls: ['./home.page.component.scss']
})
export class HomePageComponent implements OnInit {
  sportModules: Array<SportsModule> = [];
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Module',
      property: 'title',
      link: {
        hrefProperty: 'href'
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Enabled',
      property: 'disabled',
      type: 'boolean',
      isReversed: true,
      width: 1
    }
  ];

  constructor(
    public snackBar: MatSnackBar,
    private sportsModulesService: SportsModulesService
  ) {
  }

  ngOnInit(): void {
    this.sportModules = [];
    this.sportsModulesService.getModulesData('sport', 0)
      .subscribe((modules: SportsModule[]) => {
        this.sportModules = modules;
      });
  }

  get homepageAmount(): ActiveInactiveExpired {
    const activeHomepages = this.sportModules && this.sportModules.filter(homepage => homepage.enabled === true);
    const activeHomepagesAmount = activeHomepages && activeHomepages.length;
    const inactivePromosAmount = this.sportModules.length - activeHomepagesAmount;

    return {
      active: activeHomepagesAmount,
      inactive: inactivePromosAmount
    };
  }

  reorderHandler(newOrder: Order): void {
    this.sportsModulesService.updateModulesOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('New Homepage Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

}
