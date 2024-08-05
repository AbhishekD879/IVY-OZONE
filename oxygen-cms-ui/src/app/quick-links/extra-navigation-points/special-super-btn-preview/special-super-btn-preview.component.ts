import { Component, Input, OnInit } from '@angular/core';
import { Brand } from '@root/app/app.constants';
import { TitleOptions } from '@root/app/client/private/models/navigationpoint.model';
import { BrandService } from '@root/app/client/private/services/brand.service';

@Component({
  selector: 'special-super-btn-preview',
  templateUrl: './special-super-btn-preview.component.html',
  styleUrls: ['./special-super-btn-preview.component.scss']
})
export class SpecialSuperBtnPreviewComponent implements OnInit {

  @Input('titleOptions') titleOptions: TitleOptions[];
  @Input('bgImage') bgImage:string;
  @Input('type') type : string;
  alignmentFromParent: string;
  titleOptionsFromParent: TitleOptions[];
  rightTopClass: string = "";
  rightBtnClass: string = "";
  defaultFormConfig: TitleOptions;
  constructor(private brandService: BrandService) { }

  isBrandLads: boolean = false;
  ngOnInit(): void {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
  }

  ngDoCheck() {
    this.titleOptionsFromParent = this.titleOptions;
    this.defaultFormConfig = this.titleOptionsFromParent.find(option => option.key === 'bgImage');

    switch (this.isBrandLads && this.bgImage && this.bgImage.length > 0) {
      case true:
        this.rightBtnClass = "bg-align-right-theme1-btn";
        this.rightTopClass = "row bg-align-right-theme1";
        break;

      default:
        this.rightBtnClass = "bg-align-right-theme1-btn";
        this.rightTopClass = "row bg-align-right-theme1";
    }
  }
}
