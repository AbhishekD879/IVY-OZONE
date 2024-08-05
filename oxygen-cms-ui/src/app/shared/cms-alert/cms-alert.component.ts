import { Component, OnInit } from '@angular/core';
import { AppConstants } from '@app/app.constants';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';

@Component({
  selector: 'cms-alert',
  templateUrl: './cms-alert.component.html',
  styleUrls: ['./cms-alert.component.scss']
})
export class CmsAlertComponent implements OnInit {
  public error: string = null;
  constructor(
    private globalLoaderService: GlobalLoaderService
  ) { }

  ngOnInit() {
  }

  public closeAlert(): void {
    this.error = null;
  }

  public showError(message): void {
    this.error = 'Error: ' + message;
    this.globalLoaderService.hideLoader();
    setTimeout(() => {
      this.error = null;
    }, AppConstants.ERROR_HIDE_DURATION);
  }

}
