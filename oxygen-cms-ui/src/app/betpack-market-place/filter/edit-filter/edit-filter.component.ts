import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FilterModel } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { Breadcrumb } from '@app/client/private/models';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';


@Component({
  selector: 'edit-filter',
  templateUrl: './edit-filter.component.html',
  styleUrls: ['./edit-filter.component.scss'],
  providers: [
    DialogService
  ]
})
export class EditFilterComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  public isLoading: boolean = false;
  public editFilter: FilterModel;
  public breadcrumbsData: Breadcrumb[];
  isHaveAll: boolean = false;
  isSpecialCar: boolean = false;

  constructor(public router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  public isValidForm(editFilter: FilterModel): boolean {
    const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    (editFilter.filterName === 'All') ? this.isHaveAll = true : this.isHaveAll = false;
    (specialChars.test(editFilter.filterName)) ? this.isSpecialCar = true : this.isSpecialCar = false;
    return !!(editFilter.filterName && editFilter.filterName.length > 0 && (!editFilter.isLinkedFilter||(editFilter.isLinkedFilter && editFilter.linkedFilterWarningText && editFilter.linkedFilterWarningText?.length > 0)) && !this.isHaveAll && !this.isSpecialCar);
  }

  /**
  * Save BetPack
  *  @returns - {void}
  */
  public saveChanges(): void {
    this.apiClientService.betpackService()
      .putFilter(this.editFilter)
      .subscribe((val: any) => {
        if (!val.body.filterAssociated) {
          this.dialogService.showNotificationDialog({
            title: `Filter Saving`,
            message: `Filter is Saved.`,
            closeCallback: () => {
              this.router.navigate(['betpack-market/filter']);
            }
          });
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Save Not Done',
            message: 'Filter is associated with ' + JSON.stringify(val.body.betpackNames),
            closeCallback: () => {
              this.router.navigate(['betpack-market/filter']);
            }
          });
        }
      });
  }

  /**
* To delete Betpack
* @returns - {void}
*/
  public removeFilter(): void {
    this.apiClientService.betpackService().deleteFilter(this.editFilter.filterName).subscribe((val: any) => {
      if (!val.body.filterAssociated) {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Filter is Removed.',
          closeCallback: () => {
            this.router.navigate(['betpack-market/filter']);
          }
        });
      } else {
        this.dialogService.showNotificationDialog({
          title: 'Remove Not Done',
          message: 'Filter is associated with ' + JSON.stringify(val.body.betpackNames),
          closeCallback: () => {
            this.router.navigate(['betpack-market/filter']);
          }
        });
      }
    });
  }

  /**
 * loading betpack initial data
 * @param {boolean} isLoading -;
 *  @returns - {void}
 */
  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.hideLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.betpackService().getFilterById(params['id'])
        .map((res: HttpResponse<FilterModel>) => res.body)
        .subscribe((editFilter: FilterModel) => {
          this.editFilter = editFilter;
          this.breadcrumbsData = [{
            label: 'Filters',
            url: '/betpack-market/filter'
          }, {
            label: this.editFilter.filterName,
            url: `/betpack-market/${this.editFilter.id}`
          }];
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  /**
  * to set action items remove,save and revert
  * @param {any} event -;
  * @returns - {void}
  */
  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeFilter();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.loadInitData();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
* To check the filtername have special characters
* @returns - {void}
*/
  filterCheck(filter): void {
    const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    (filter === 'All') ? this.isHaveAll = true : this.isHaveAll = false;
    (specialChars.test(filter)) ? this.isSpecialCar = true : this.isSpecialCar = false;
  }
}
