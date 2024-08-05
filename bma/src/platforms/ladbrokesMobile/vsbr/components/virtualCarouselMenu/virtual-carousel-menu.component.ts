import { Component } from '@angular/core';
import {
  VirtualCarouselMenuComponent as CoralVirtualCarouselMenuComponent
} from '@app/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';

@Component({
    selector: 'virtual-carousel-menu',
    templateUrl: 'virtual-carousel-menu.component.html',
    styleUrls: ['./virtual-carousel-menu.component.scss']
})
export class VirtualCarouselMenuComponent extends CoralVirtualCarouselMenuComponent {}
