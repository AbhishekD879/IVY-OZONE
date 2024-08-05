import { AfterViewInit, Component } from '@angular/core';
import { BmaMainComponent } from '@app/bma/components/bmaMain/bma-main.component';

@Component({
  selector: 'bma-main',
  templateUrl: 'bma-main.component.html'
})
export class DesktopBmaMainComponent extends BmaMainComponent implements AfterViewInit { }
