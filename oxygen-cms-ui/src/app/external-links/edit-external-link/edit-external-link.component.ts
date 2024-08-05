import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import {HttpResponse} from '@angular/common/http';
import {DialogService} from '../../shared/dialog/dialog.service';
import {Breadcrumb} from '../../client/private/models/breadcrumb.model';
import {ActionButtonsComponent} from '../../shared/action-buttons/action-buttons.component';
import {ExternalLink} from '../../client/private/models/externalLink.model';

@Component({
  selector: 'app-edit-external-link',
  templateUrl: './edit-external-link.component.html',
  styleUrls: ['./edit-external-link.component.scss']
})
export class EditExternalLinkComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  public externalLink: ExternalLink;
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
    this.apiClientService.externalLinks()
      .edit(this.externalLink)
      .map((externalLink: HttpResponse<ExternalLink>) => {
        return externalLink.body;
      })
      .subscribe((data: ExternalLink) => {
        this.externalLink = data;
        this.actionButtons.extendCollection(this.externalLink);
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: `External Link`,
          message: `External Link is Saved.`
        });
        this.router.navigate(['/external-links']);
      });
  }

  revertChanges(): void {
    this.loadInitData(false);
  }

  removeExternalLink(): void {
    this.apiClientService.externalLinks().remove(this.externalLink.id).subscribe(() => {
      this.router.navigate(['/external-links']);
    });
  }

  isValidForm(externalLink: ExternalLink): boolean {
    return !!(externalLink.url && externalLink.target);
  }

  shortVersion(): String {
    return this.externalLink.url.slice(0, 30) + '...';
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeExternalLink();
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
      this.apiClientService.externalLinks().getById(params['id']).map((externalLink: HttpResponse<ExternalLink>) => {
        return externalLink.body;
      }).subscribe((externalLink: ExternalLink) => {
        this.externalLink = externalLink;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.breadcrumbsData = [{
          label: `External Links`,
          url: `/external-links`
        }, {
          label: this.externalLink.url,
          url: `/external-links/${this.externalLink.id}`
        }];
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }
}
