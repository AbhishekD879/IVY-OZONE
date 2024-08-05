import { Component, OnInit, ViewChild } from '@angular/core';

import { Router, ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http/index';
import { PromotionsSections } from '@root/app/client/private/models/promotions-sections.model';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';
import { ActionButtonsComponent } from '../../shared/action-buttons/action-buttons.component';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '../../shared/dialog/dialog.service';

@Component({
  selector: 'app-section',
  templateUrl: './section.component.html',
  styleUrls: ['./section.component.scss']
})
export class SectionComponent implements OnInit {

  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  public promotionsSections: PromotionsSections;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadInitData();
  }

  saveChanges(): void {
    this.globalLoaderService.showLoader();
    if (this.promotionsSections.promotionIds !== null && this.promotionsSections.promotionIds.length === 0) {
      this.promotionsSections.promotionIds = null;
    }
    this.apiClientService.promotionsSectionsService()
        .edit(this.promotionsSections)
        .map((promotionsSections: HttpResponse<PromotionsSections>) => {
          return promotionsSections.body;
        })
        .subscribe((data: PromotionsSections) => {
          this.promotionsSections = data;
          this.actionButtons.extendCollection(this.promotionsSections);
          this.globalLoaderService.hideLoader();
          this.dialogService.showNotificationDialog({
            title: `Promotions Sections`,
            message: `Promotions Sections is Saved.`
          });
        });
  }

  revertChanges(): void {
    this.loadInitData(false);
  }

  removePromotionsSections(): void {
    this.apiClientService.promotionsSectionsService().remove(this.promotionsSections.id).subscribe(() => {
      this.router.navigate(['/promotions/sections']);
    });
  }

  isValidForm(promotionsSections: PromotionsSections): boolean {
    return !!(promotionsSections.name);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removePromotionsSections();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.promotionsSectionsService()
         .getById(params['id'])
         .map((promotionsSections: HttpResponse<PromotionsSections>) => {
        return promotionsSections.body;
      }).subscribe((promotionsSections: PromotionsSections) => {
        this.promotionsSections = promotionsSections;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.breadcrumbsData = [{
          label: `Promotions Sections`,
          url: `/promotions/sections`
        }, {
          label: this.promotionsSections.name,
          url: `/promotions/section/${this.promotionsSections.id}`
        }];
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }

}
