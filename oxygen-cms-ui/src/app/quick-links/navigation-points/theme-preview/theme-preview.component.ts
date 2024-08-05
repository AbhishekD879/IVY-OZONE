import { Component, Input, OnInit } from '@angular/core';
import { Brand } from '@root/app/app.constants';
import { TitleOptions } from '@root/app/client/private/models/navigationpoint.model';
import { BrandService } from '@root/app/client/private/services/brand.service';

@Component({
  selector: 'app-theme-preview',
  templateUrl: './theme-preview.component.html',
  styleUrls: ['./theme-preview.component.scss']
})
export class ThemePreviewComponent implements OnInit {

  @Input('alignment') alignment: string;
  @Input('themeValue') themeValue: string;
  @Input('titleOptions') titleOptions: TitleOptions[];
  @Input('bgImage') bgImage:string;

  themeValueFromParent: string;
  alignmentFromParent: string;
  titleOptionsFromParent: TitleOptions[];
  rightTopClass: string = "";
  rightBtnClass: string = "";
  centerTopClass: string = "";
  centerBtnClass: string = "";
  defaultFormConfig: TitleOptions;
  constructor(private brandService: BrandService) { }

  isBrandLads: boolean = false;
  ngOnInit(): void {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
  }

  ngDoCheck() {
    this.titleOptionsFromParent = this.titleOptions;
    this.alignmentFromParent = this.alignment;
    this.themeValueFromParent = this.themeValue;
    this.defaultFormConfig = this.titleOptionsFromParent.find(option => option.key === this.alignmentFromParent);

    switch (this.isBrandLads) {
      case false:
        switch (this.alignmentFromParent) {
          case "center":
            switch (this.themeValueFromParent) {
              case "theme_1":
                this.centerBtnClass = "center-theme1-corl-btn text-center";
                this.centerTopClass = "row center-theme1-corl-top";
                break;
              case "theme_2":
                this.centerBtnClass = "center-theme2-corl-btn text-center";
                this.centerTopClass = "row center-theme2-corl-top";
                break;
              case "theme_3":
                this.centerBtnClass = "center-theme3-corl-btn text-center";
                this.centerTopClass = "row center-theme3-corl-top";
                break;
              case "theme_4":
                this.centerBtnClass = "center-theme4-corl-btn text-center";
                this.centerTopClass = "row center-theme4-corl-top";
                break;
              case "theme_5":
                this.centerBtnClass = "center-theme5-corl-btn text-center";
                this.centerTopClass = "row center-theme5-corl-top";
                break;
              case "theme_6":
                this.centerBtnClass = "center-theme6-corl-btn text-center";
                this.centerTopClass = "row center-theme6-corl-top";
                break;
              default:
                this.centerBtnClass = "center-theme1-corl-btn text-center";
                this.centerTopClass = "row center-theme1-corl-top";
                break;
            }
            break;
          case "right":
            switch (this.themeValueFromParent) {
              case "theme_1":
                this.rightBtnClass = "right-theme1-corl-btn";
                this.rightTopClass = "row right-theme1-corl-top";
                break;
              case "theme_2":
                this.rightBtnClass = "right-theme2-corl-btn";
                this.rightTopClass = "row right-theme2-corl-top";
                break;
              case "theme_3":
                this.rightBtnClass = "right-theme3-corl-btn";
                this.rightTopClass = "row right-theme3-corl-top";
                break;
              case "theme_4":
                this.rightBtnClass = "right-theme4-corl-btn";
                this.rightTopClass = "row right-theme4-corl-top";
                break;
              case "theme_5":
                this.rightBtnClass = "right-theme5-corl-btn";
                this.rightTopClass = "row right-theme5-corl-top";
                break;
              case "theme_6":
                this.rightBtnClass = "right-theme6-corl-btn";
                this.rightTopClass = "row right-theme6-corl-top";
                break;
              default:
                this.rightBtnClass = "right-theme1-corl-btn";
                this.rightTopClass = "row right-theme1-corl-top";
                break
            }
            break;
        }
        break;
      case true:
        switch (this.alignmentFromParent) {
          case "bgImage":
            switch (this.themeValueFromParent) {
              case "theme_1":
                this.rightBtnClass = "bg-align-right-theme1-btn";
                this.rightTopClass = "row bg-align-right-theme1";
                break;
              
              default:
                this.rightBtnClass = "bg-align-right-theme1-btn";;
                this.rightTopClass = "row bg-align-right-theme1";
                break;
            }
            break;
          case "center":
            switch (this.themeValueFromParent) {
              case "theme_1":
                this.centerBtnClass = "center-theme1-btn text-center";
                this.centerTopClass = "row center-theme1-top";
                break;
              case "theme_2":
                this.centerBtnClass = "center-theme2-btn text-center";
                this.centerTopClass = "row center-theme2-top";
                break;
              case "theme_3":
                this.centerBtnClass = "center-theme3-btn text-center";
                this.centerTopClass = "row center-theme3-top";
                break;
              case "theme_4":
                this.centerBtnClass = "center-theme4-btn text-center";
                this.centerTopClass = "row center-theme4-top";
                break;
              default:
                this.centerBtnClass = "center-theme1-btn text-center";
                this.centerTopClass = "row center-theme1-top";
                break;
            }
            break;
          case "right":
            switch (this.themeValueFromParent) {
              case "theme_1":
                this.rightBtnClass = "right-theme1-btn";
                this.rightTopClass = "row right-theme1-top";

                break;
              case "theme_2":
                this.rightBtnClass = "right-theme2-btn";
                this.rightTopClass = "row right-theme2-top";
                break;
              case "theme_3":
                this.rightBtnClass = "right-theme3-btn";
                this.rightTopClass = "row right-theme3-top";
                break;
              case "theme_4":
                this.rightBtnClass = "right-theme4-btn";
                this.rightTopClass = "row right-theme4-top";
                break;
              default:
                this.rightBtnClass = "right-theme1-btn";
                this.rightTopClass = "row right-theme1-top";
                break
            }
            break;
        }
        break;
      default:

        break;
    }
  }

  ngAfterViewInit() {
    this.alignmentFromParent = this.alignment;
    this.themeValueFromParent = this.themeValue;

  }

}
