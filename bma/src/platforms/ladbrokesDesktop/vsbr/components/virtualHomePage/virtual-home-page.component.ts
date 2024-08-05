import { Component } from "@angular/core";
import { VirtualHomePageComponent } from '@app/vsbr/components/virtualHomePage/virtual-home-page.component';

@Component({
    selector: 'virtual-home-page',
    templateUrl: './virtual-home-page.component.html',
    styleUrls: ['./virtual-home-page.component.scss']
})

export class DesktopVirtualHomePageComponent extends VirtualHomePageComponent {}