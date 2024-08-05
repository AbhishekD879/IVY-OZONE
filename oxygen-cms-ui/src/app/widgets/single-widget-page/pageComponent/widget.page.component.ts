import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { ApiClientService } from '@app/client/private/services/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Widget } from '@app/client/private/models/widget.model';
import { WidgetsAPIService } from '../../service/widgets.api.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { WidgetColumnTypes } from '../../widget-column.enum';

@Component({
  selector: 'widget-page',
  templateUrl: './widget.page.component.html',
  styleUrls: ['./widget.page.component.scss']
})
export class WidgetPageComponent implements OnInit {
  widget: Widget;
  columnOptions: Array<string>;
  public sportCategories: SportCategory[];
  columnsTypesEnum: any = WidgetColumnTypes;
  id: string;
  @ViewChild('actionButtons') actionButtons;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private widgetsAPIService: WidgetsAPIService,
    private apiClientService: ApiClientService
  ) {}

  /**
   * Load widget data from server.
   */
  loadInitialData() {
    // load current widget data
    this.widgetsAPIService.getSingleWidgetData(this.id)
      .subscribe((data: any) => {
        this.widget = data.body;
        this.breadcrumbsData = [{
          label: `Widgets`,
          url: `/widgets`
        }, {
          label: this.widget.title,
          url: `/widgets/${this.widget.id}`
        }];
        if (this.widget.type === 'match-centre') {
          this.apiClientService.sportCategoriesService()
              .getSportCategories()
              .map((response) => {
                return response.body;
              })
              .subscribe((categories) => {
                this.sportCategories = categories;
              });
        }
      }, error => {
        this.router.navigate(['/widgets']);
      });
  }

  /**
   * Reload widget data from server.
   */
  revertWidgetChanges() {
    this.loadInitialData();
  }

  /**
   * Make PUT request to server to update widhet data.
   */
  saveWidgetChanges() {
    this.widgetsAPIService
        .putWidgetChanges(this.widget)
        .map((response) => {
          return response.body;
        })
        .subscribe((data: any) => {
          this.widget = data;
          this.actionButtons.extendCollection(this.widget);
          this.dialogService.showNotificationDialog({
            title: 'Upload Completed',
            message: 'Widget Changes Are Saved.'
          });
        });
  }

  ngOnInit() {
    this.columnOptions = Object.keys(WidgetColumnTypes);
    this.id = this.route.snapshot.paramMap.get('id');

    this.loadInitialData();
  }

  public isValidForm(widget: Widget): boolean {
    return widget.title && widget.title.length > 0;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveWidgetChanges();
        break;
      case 'revert':
        this.revertWidgetChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
