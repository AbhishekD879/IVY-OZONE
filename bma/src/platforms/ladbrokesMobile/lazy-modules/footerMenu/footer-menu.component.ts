import { Component } from '@angular/core';
import { FooterMenuComponent } from '@app/lazy-modules/footerMenu/footer-menu.component';

@Component({
  selector: 'footer-menu',
  templateUrl: '../../../../app/lazy-modules/footerMenu/footer-menu.component.html',
  styleUrls: ['footer-menu.component.scss']
})

export class LadbrokesFooterMenuComponent extends FooterMenuComponent {}
