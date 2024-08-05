import {Component} from '@angular/core';
import {GlobalLoaderService} from '../loader.service';

@Component({
  selector: 'global-loader',
  templateUrl: './global-loader.component.html',
  styleUrls: ['./global-loader.component.scss']
})
export class GlobalLoaderComponent {
  constructor(private globalLoaderService: GlobalLoaderService) {}

  get isVisible() {
    return this.globalLoaderService.isVisible;
  }
}
