import { Component } from '@angular/core';
import { RequestErrorComponent as AppRequestErrorComponent } from '@app/shared/components/requestError/request-error.component';

@Component({
  selector: 'request-error',
  templateUrl: './request-error.component.html',
  styleUrls: ['./request-error.component.scss']
})
export class RequestErrorComponent extends AppRequestErrorComponent {}
