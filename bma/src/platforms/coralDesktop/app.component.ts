import { Component, ApplicationRef, NgZone } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import decorateTick from './../app-decorator';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router } from '@angular/router';

@Component({
  selector: 'root-app',
  templateUrl: './app.component.html'
})
export class RootComponent {
  isProduction = environment.production;

  constructor(
    private applicationRef: ApplicationRef,
    private ngZone: NgZone,
    private pubSubService: PubSubService,
    private router: Router
  ) {
    decorateTick(this.applicationRef, this.ngZone, this.pubSubService, this.router);
  }
}
