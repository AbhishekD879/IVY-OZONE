import { Component, OnInit } from '@angular/core';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';
import {BrandService} from '@app/client/private/services/brand.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {QEQuickLinksApiService} from '@app/quiz/service/quick-links.api.service';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {ErrorService} from '@app/client/private/services/error.service';
import {HttpErrorResponse} from '@angular/common/http';
import {QELink} from '@app/client/private/models/qeLink.model';

@Component({
  selector: 'app-quick-links-add',
  templateUrl: './quick-links-add.component.html'
})
export class QuickLinksAddComponent implements OnInit {

  public breadcrumbsData: Breadcrumb[];
  public newQEQuickLinks: QEQuickLinks;

  constructor(
    private brandService: BrandService,
    private quickLinksApi: QEQuickLinksApiService,
    private dialogService: DialogService,
    private router: Router,
    private errorService: ErrorService
  ) { }

  ngOnInit() {
    this.newQEQuickLinks = {
      id: '',
      brand: this.brandService.brand,
      createdBy: '',
      createdAt: '',
      updatedBy: '',
      updatedAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      title: '',
      links: []
    };

    this.pushLinks();

    this.breadcrumbsData = [{
      label: `Quick Links`,
      url: `/question-engine/quick-links`
    }, {
      label: 'Create Quick Links',
      url: `/question-engine/quick-links/create/`
    }];
  }

  isValidModel(): boolean {
    return this.newQEQuickLinks.title.trim().length > 0;
  }

  private pushLinks(): void {
    for (let i = 0; i < 3; i++) {
      this.newQEQuickLinks.links.push(new QELink('', '', ''));
    }
  }

  public updateText(htmlMarkup: string, index: number): void {
    this.newQEQuickLinks.links[index].description = htmlMarkup;
  }

  public saveQuickLinksChanges(): void {
    this.quickLinksApi.createQEQuickLinks(this.newQEQuickLinks).subscribe(data => {
      this.newQEQuickLinks.id = data.body.id;
      this.finishQuickLinksPageCreation();
    }, (error: HttpErrorResponse) => {

      this.errorService.emitError('There is an error occurred during page creation: ' + error.error.message);
    });
  }

  finishQuickLinksPageCreation(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Quick Links Page is Created and Stored.',
      closeCallback() {
        self.router.navigate([`question-engine/quick-links/quick-link/${self.newQEQuickLinks.id}`]);
      }
    });
  }

}
