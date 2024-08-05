import { Component } from '@angular/core';

import { OlympicsPageComponent as MobileOlympicsPageComponent } from '@app/olympics/components/olympicsPage/olympics-page.component';

@Component({
  selector: 'olympics-page',
  templateUrl: './olympics-page.component.html'
})
export class OlympicsPageComponent extends MobileOlympicsPageComponent {}
