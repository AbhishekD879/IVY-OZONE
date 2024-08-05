import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Filename } from '@root/app/client/public/models/filename.model';
import { environment } from '@root/environments/environment';
import { BrandService } from '@app/client/private/services/brand.service';


@Component({
  selector: 'track-image-list',
  templateUrl: './track-image-list.component.html',
  styleUrls: ['./track-image-list.component.scss']
})
export class TrackImageListComponent {
  @Input()
  runnerImages: Filename[];

  @Output()
  onImageRemoving = new EventEmitter();

  constructor(private brandService: BrandService) {}

  absoluteUrl(relative: Filename) {
    return `${environment.cmsRoot[this.brandService.brand]}${relative.path}/${relative.filename}`;
  }

  removeImageClicked(image: Filename) {
    this.onImageRemoving.emit(image);
  }
}
