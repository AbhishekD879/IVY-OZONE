import {Component, OnInit, Input} from '@angular/core';
import {environment} from '@root/environments/environment';
import {Post} from '@app/client/private/models/timeline-post.model';
import {Filename} from '@root/app/client/public/models/filename.model';
import {ImageLoaderService} from '@app/client/private/services/imageLoader/image-loader-service';
import {IImageData} from '@app/image-manager/model/image-manager.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { TimelineTemplate } from '@app/client/private/models/timelineTemplate.model';
import { Brand, TimeLine } from '@app/app.constants';
@Component({
  selector: 'post-preview',
  templateUrl: './post-preview.component.html',
  styleUrls: ['./post-preview.component.scss']
})
export class PostPreviewComponent implements OnInit {
  @Input() post: Post;
  activePostIconImage: IImageData;
  activeHeaderIconImage: IImageData;
  brand: string;

  constructor(private imageLoaderService: ImageLoaderService, private brandService: BrandService) {}

  ngOnInit() {
    this.brand = this.brandService.brand;
    if (this.post.template.postIconSvgId) {
      this.imageLoaderService.getData(this.post.template.postIconSvgId)
        .subscribe(images => {
          this.activePostIconImage = images && images[0];
        });
    }

    if (this.post.template.headerIconSvgId) {
      this.imageLoaderService.getData(this.post.template.headerIconSvgId)
        .subscribe(images => {
          this.activeHeaderIconImage = images && images[0];
        });
    }
  }

  absoluteUrl(relative: Filename) {
    return `${(<any>environment).cmsRoot[this.post.brand]}${relative.path}/${relative.filename}`;
  }

  /**
   * Get css class for post preview template
   * @param template
   * @returns string
   */
  getCssClass(template: TimelineTemplate): string {
    let postPreviewClass = '';
    if(template.showLeftSideRedLine && this.brand === Brand.LADBROKES) {
      postPreviewClass += TimeLine.POST_RED_LINE;
    }

    if(template.showLeftSideBlueLine && this.brand === Brand.CORAL) {
      postPreviewClass += TimeLine.POST_BLUE_LINE;
    }

    if(this.activePostIconImage) {
      postPreviewClass += ' ' + TimeLine.POST_WITH_ICON;
    }

    return postPreviewClass;
  }
}
