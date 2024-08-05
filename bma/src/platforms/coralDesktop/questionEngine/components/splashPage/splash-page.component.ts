import { Component } from '@angular/core';
import { SplashPageComponent } from '@app/questionEngine/components/splashPage/splash-page.component';


@Component({
  selector: 'splash-page',
  templateUrl: '../../../../../app/questionEngine/components/splashPage/splash-page.component.html',
  styleUrls: ['./splash-page.component.scss'],
})

export class DesktopSplashPageComponent extends SplashPageComponent{
isDesktop = true;
}
