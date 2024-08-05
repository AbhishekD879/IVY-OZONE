import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RetailApiModule } from '@retailModule/retail-api.module';

@Injectable({
  providedIn: RetailApiModule
})
export class RecapchaService {
  document : Document

  constructor(
    private windowRef: WindowRefService
  ) {}
   addScript(): void {
    const elementId = 'retail-recaptcha-enterprise';
    if (! ((this.windowRef.document.getElementById(elementId)) || (this.windowRef.document.getElementById('recaptcha-enterprise')))) {
    const script = this.windowRef.document.createElement('script');
    script.src = `https://www.google.com/recaptcha/enterprise.js?render=${environment.GOOGLE_RECAPTCHA.ACCESS_TOKEN}`;
    script.id = elementId;
    script.async = true;
    script.defer = true;
    this.windowRef.document.body.appendChild(script);
    }
}

}
