import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {WidgetsAPIService} from '../../service/widgets.api.service';
import {Widget} from '@app/client/private/models/widget.model';
import {AppConstants} from '@app/app.constants';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '@app/client/private/models/activeInactiveExpired.model';
import {WidgetColumnTypes} from '../../widget-column.enum';
import {HttpResponse} from '@angular/common/http';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'widgets-page',
  templateUrl: './widgets.page.component.html',
  styleUrls: ['./widgets.page.component.scss']
})
export class WidgetsPageComponent implements OnInit {
  widgetsData: Array<Widget>;
  getDataError: string;
  searchField: string = '';

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Columns',
      property: 'columns'
    },
    {
      name: 'Show Expanded',
      property: 'showExpanded',
      type: 'boolean'
    },
    {
      name: 'Show On Mobile',
      property: 'showOnMobile',
      type: 'boolean'
    },
    {
      name: 'Show On Desktop',
      property: 'showOnDesktop',
      type: 'boolean'
    },
    {
      name: 'Show On Tablet',
      property: 'showOnTablet',
      type: 'boolean'
    }
  ];
  filterProperties: Array<string> = [
    'title'
  ];

  constructor(
    private widgetsAPIService: WidgetsAPIService,
    public snackBar: MatSnackBar
  ) {}

  get widgetsAmount(): ActiveInactiveExpired {
    const activeWidgets = this.widgetsData && this.widgetsData.filter(promotion => promotion.disabled === false);
    const activeWidgetsAmount = activeWidgets && activeWidgets.length;
    const inactiveWidgetsAmount = this.widgetsData.length - activeWidgetsAmount;

    return {
      active: activeWidgetsAmount,
      inactive: inactiveWidgetsAmount
    };
  }

  reorderWidgetsHandler(newOrder: Order): void {

    this.widgetsAPIService.postNewWidgetsOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('NEW WIDGET ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  ngOnInit() {
    this.widgetsAPIService.getWidgetsData()
      .map((res: HttpResponse<Widget[]>) => {
        return res.body.map((d: Widget) => {
          d.columns = WidgetColumnTypes[d.columns];
          return d;
        });
      })
      .subscribe((data: Widget[]) => {
        this.widgetsData = data;
      }, error => {
        this.getDataError = error.message;
      });
  }
}
