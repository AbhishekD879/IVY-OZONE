import { Component } from '@angular/core';
import { LoadingScreenComponent } from '@shared/components/loadingScreen/loading-screen.component';

@Component({
  selector: 'loading-screen',
  templateUrl: 'loading-screen.component.html',
  styleUrls: ['../../../../../app/shared/components/loadingScreen/fade-out-animation.scss',
    'loading-screen.component.scss']
})

export class LadbrokesLoadingScreenComponent extends LoadingScreenComponent {
}

