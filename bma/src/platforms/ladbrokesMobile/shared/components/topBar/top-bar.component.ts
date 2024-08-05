import { Component } from '@angular/core';

import { TopBarComponent as AppTopBarComponent } from '@shared/components/topBar/top-bar.component';

@Component({
  selector: 'top-bar',
  templateUrl: 'top-bar.component.html',
  styleUrls: ['top-bar.component.scss']
})
export class TopBarComponent extends AppTopBarComponent {}
