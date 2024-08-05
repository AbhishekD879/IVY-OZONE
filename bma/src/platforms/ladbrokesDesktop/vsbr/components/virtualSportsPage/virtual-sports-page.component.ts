import { Component } from '@angular/core';
import {
  VirtualSportsPageComponent as MobileVirtualSportsPageComponent
} from '@ladbrokesMobile/vsbr/components/virtualSportsPage/virtual-sports-page.component';

@Component({
  selector: 'virtual-sports-page',
  templateUrl: './virtual-sports-page.component.html'
})
export class VirtualSportsPageComponent extends MobileVirtualSportsPageComponent {}
