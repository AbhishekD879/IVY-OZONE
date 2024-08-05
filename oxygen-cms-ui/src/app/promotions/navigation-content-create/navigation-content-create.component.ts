import { Component, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { MatSelectChange } from '@angular/material/select';
import { ActivatedRoute, Router } from '@angular/router';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { ApiClientService } from '@app/client/private/services/http/index';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import {
    NavTypeContent,
    PromoNavContent,
    PromoNavItems,
    PromoNavItemsClass,
    PromotionsNavigationGroup
  } from '@app/client/private/models/promotions-navigation.model';
import { Leaderboards } from '@app/client/private/models/promotions-leaderboard.model';

@Component({
  selector: 'app-navigation-content',
  templateUrl: './navigation-content-create.component.html',
  styleUrls: ['./navigation-content-create.component.scss'],
})

export class NavigationContentCreateComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  @Output() navItemsList: EventEmitter<NavTypeContent> = new EventEmitter<NavTypeContent>();

  type: Leaderboards[] = [
    { id: 'url', name: 'URL' },
    { id: 'Leaderboard', name: 'Leaderboard' },
    { id: 'description', name: 'Description' },
  ]
  navTypeContent: NavTypeContent = {
    name: '',
    navType: '',
    url: null,
    leaderboardId: null,
    descriptionTxt: null,
    navigationGroupId: ''
  };

  name: FormControl;
  url: FormControl;
  navGroupId: string;
  nId: string;
  isLoading: boolean;
  navData: PromoNavContent;
  leaderboard: FormControl;
  activeLeaderboard: Leaderboards[];
  leaderboardCount: PromoNavItemsClass[];
  isLbExist : boolean;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private route: ActivatedRoute,
    private dialogService: DialogService,
    private errorService: ErrorService,
    public router: Router,
  ) {
    this.name = new FormControl('', [Validators.required]);
    this.url = new FormControl('', [Validators.required]);
    this.leaderboard = new FormControl('', [Validators.required]);
    this.isValidModel = this.isValidModel.bind(this);
  }

  ngOnInit(): void {
    this.navGroupId = this.route.snapshot.paramMap.get('id');
    this.navTypeContent.navigationGroupId = this.navGroupId;
    this.nId = this.route.snapshot.paramMap.get('nId');

    // load Active leaderboard
    this.apiClientService
      .promotionLeaderboardService()
      .getActiveLeaderboard()
      .map((data: HttpResponse<Leaderboards[]>) => data.body)
      .subscribe((leaderboard: Leaderboards[]) => {
        this.activeLeaderboard = leaderboard;
      });
    if (this.nId) {
      this.updateForm()
    }
    this.apiClientService.promotionsNavigationsService().getNavListById(this.navGroupId)
    .map((data: HttpResponse<PromotionsNavigationGroup>) => data.body)
      .subscribe((data: PromotionsNavigationGroup) => {
        this.breadcrumbsData = [{
          label: `Promotions Navigation`,
          url: `/promotions/navigations`
        },
        {
          label:`${data?.title}`,
          url: `/promotions/navigation/${this.navGroupId}`
        },
        {
          label: 'Create Navigation Content',
          url: `/navigations/navigationCreate/:id`
        },
        ];
        this.leaderboardCount = data.navItems.filter(el => {
          return (el.leaderboardId != null &&  el.leaderboardId != "none")
        });
      })
  }

  /**
   * Open the Page in Edit Form
   * @param isLoading boolean
   */
  updateForm(isLoading: boolean = true) {
    this.isLoading = isLoading;
    this.apiClientService.promotionsNavigationsService().
      getNavListById(this.navGroupId)
      .map((nav: HttpResponse<PromotionsNavigationGroup>) => nav.body)
      .subscribe((data: PromotionsNavigationGroup) => {
        this.globalLoaderService.hideLoader();
        data.navItems.filter(el => {
          if (el.id === this.nId) {
            this.navData = el;
            this.navTypeContent.name = el?.name;
            this.navTypeContent.navType = el?.navType;
            this.navTypeContent.url = el?.url;
            this.navTypeContent.descriptionTxt = el?.descriptionTxt;
            this.breadcrumbsData = [
              {
                label: `Promotions Navigation`,
                url: `/promotions/navigations`
              },
              {
                label: `${this.navData?.name}`,
                url: `/promotions/navigation/${this.navGroupId}`
              },{
                label: `Update Navigation Content`,
                url: `/navigations/navigationCreate/:id`
              }
            ];
            if (el.leaderboardStatus) {
              this.navTypeContent.leaderboardId = el?.leaderboardId;
            } else {
              if (el.navType.toLowerCase() === 'leaderboard') {
                this.navTypeContent.leaderboardId = 'none';
              }
            }
          }
        })
        this.isLoading = false;
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
  }

  /**
   * Set all chosen Leaderboard
   * @param event
   */
  setLeaderboard(event: MatSelectChange): void {
      this.isLbExist = this.leaderboardCount.find(lb => lb.leaderboardId === event.value) ? true : false
     if(this.isLbExist){
      this.dialogService.showNotificationDialog({
        title: `NavTypeLeaderboard`,
        message: `This Leaderboard is already selected`,
      });
     }
    this.navTypeContent.leaderboardId = event.value;
  }

  /**
   * Set the type of the Nav Content
   * @param event
   */
  setType(event: MatSelectChange): void {
    this.navTypeContent.url = null;
    this.navTypeContent.leaderboardId = null;
    this.navTypeContent.descriptionTxt = null;
    if (event.value.toLowerCase() === 'leaderboard' && this.leaderboardCount.length >= 2) {
      this.dialogService.showNotificationDialog({
        title: `Navigation Item `,
        message: `Max 2 leaderboards can be selected`,
      });
      this.router.navigate([`/promotions/navigation/${this.navGroupId}`]);
    }
    this.navTypeContent.navType = event.value;
  }

  /**
   * check the validaity of the form
   * @returns boolean
   */
  public isValidForm(): boolean {
    return this.navTypeContent?.name?.length > 0 && (
      (this.navTypeContent?.leaderboardId?.length > 0 && this.navTypeContent?.leaderboardId !== 'none' && !(this.leaderboardCount?.length >= 2) && !this.isLbExist) ||
      (this.navTypeContent?.url?.length > 0 && this.checkValidUrl(this.navTypeContent?.url))||
      this.navTypeContent?.descriptionTxt?.length > 0)
  }

  /**
 * check the validaity of the model
 * @returns boolean
 */
  public isValidModel(navType: NavTypeContent): boolean {
    if (navType?.name?.length > 0 && navType?.leaderboardId?.length > 0) {
      return this.navTypeContent?.leaderboardId !== 'none' &&!(this.leaderboardCount?.length > 2) && !(this.isLbExist)
    } else {
      return navType?.name?.length > 0 && (
        navType?.leaderboardId?.length > 0 ||
        navType?.url?.length > 0 ||
        navType?.descriptionTxt?.length > 0)
    }
  }

  /**
  * Action handler for the action button
  * @param {event}
  * @returns null
  */
  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeNavContent();
        break;
      case 'save':
        this.updateNavContent();
        break;
      case 'revert':
        this.revertNavContent();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
  * remove the nav content
  */
  removeNavContent() {
    this.apiClientService.promotionsNavigationsService().removeNavContent(this.navData?.id)
    .subscribe((data: any) => {
      this.dialogService.showNotificationDialog({
        title: 'Remove Completed',
        message: 'Nav Item  is Removed.'
      });
      this.router.navigate([`/promotions/navigation/${this.navGroupId}`])
    });
  }

  /**
  * make the put request to server
  */
  updateNavContent() {
    const self = this;
    this.globalLoaderService.showLoader();
    this.navData.name = this.navTypeContent?.name;
    this.navData.navType = this.navTypeContent.navType;
    this.navData.url = this.navTypeContent.url;
    this.navData.descriptionTxt = this.navTypeContent.descriptionTxt;
    this.navData.leaderboardId =this.navTypeContent.leaderboardId;
    if (this.navData.leaderboardId === 'none') {
      this.navData.leaderboardId = null;
    }
    this.apiClientService.promotionsNavigationsService().putNavContent(this.navData)
    .map((nav: HttpResponse<PromoNavItems>) => nav.body)
    .subscribe((data: PromoNavItems) => {
        this.globalLoaderService.hideLoader();
        this.navTypeContent = data;
        this.actionButtons.extendCollection(this.navTypeContent);
        this.navItemsList.emit(this.navTypeContent);
        this.dialogService.showNotificationDialog({
          title: `NavTypeContent `,
          message: `Navigation Content is Updated.`,
          closeCallback() {
            self.router.navigate([`/promotions/navigation/${self.navGroupId}`]);
          }
        });
      }, (error: HttpErrorResponse) => {
          self.router.navigate([`promotions/navigation/${self.navGroupId}`]).then(() => {
            this.errorService.emitError(error.error.message);
          });
        });
  }

  /**
  * make the post request to server
  */
  saveNavContent() {
    this.globalLoaderService.showLoader();
    this.apiClientService.promotionsNavigationsService().
      postNavContent(this.navTypeContent)
      .map((nav: HttpResponse<PromoNavContent>) => nav.body)
      .subscribe((data: PromoNavContent) => {
        this.globalLoaderService.hideLoader();
        this.navTypeContent = data;
        this.finishNavContentCreation();
      }, (error: HttpErrorResponse) => {
          this.router.navigate([`promotions/navigation/${this.navGroupId}`]).then(() => {
            this.errorService.emitError(error.error.message);
          });
      });
  }

  /**
  * show the message on saving the nav Content
  */
  finishNavContentCreation() {
    const self = this;
    this.navItemsList.emit(this.navTypeContent);
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Nav Item is Created and Stored.',
      closeCallback() {
        self.router.navigate([`/promotions/navigation/${self.navGroupId}`]);
      }
    });
  }

  /**
  * revert the nav content
  */
  revertNavContent() {
    this.updateForm(false)
  }

  /**
  * update the descriptionTxt of the navTypeContent
  */
  updateNavTypeContent(data, promotionProperty) {
    this.navTypeContent[promotionProperty] = data;
  }

  /**
   * Check URl Format
   * @param {url} string
   * @return boolean
   * 
   */
  checkValidUrl(url: string): boolean {
    const strRegex = '^s?https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+$';
    const urlRegex = new RegExp(strRegex);
    return urlRegex.test(url);
  }
}
