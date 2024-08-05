import {Component, EventEmitter, OnInit, ViewChild} from '@angular/core';
import {CmsAlertComponent} from '../shared/cms-alert/cms-alert.component';
import {ErrorService} from '../client/private/services/error.service';

@Component({
  selector: 'home-root',
  templateUrl: './home.component.html'
})
export class HomeComponent implements OnInit {
  private errorEmitter: EventEmitter<any>;
  constructor(errorService: ErrorService) {
    this.errorEmitter = errorService.getErrorEmitter();
  }

  @ViewChild('requestErrorBlock') private requestErrorBlock: CmsAlertComponent;

  ngOnInit() {
    const that = this;
    this.errorEmitter.subscribe(function (error) {
      that.requestErrorBlock.showError(error);
      window.scrollTo(0, 0);
    });
  }
}
