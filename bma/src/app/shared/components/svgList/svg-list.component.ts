import { ChangeDetectionStrategy, Component, ElementRef, Input, OnInit } from '@angular/core';

import { ISvgListTem } from '../../models/svg-list-tem';

@Component({
  selector: 'svg-list',
  templateUrl: './svg-list.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SvgListComponent implements OnInit {

  @Input() list: string | ISvgListTem[];
  @Input() keepStyles: boolean;
  @Input() keepFill?: boolean;

  constructor(private elem: ElementRef) {}

  ngOnInit() {
    let symbolsHtmlStr = Array.isArray(this.list) ? this.list
        .filter(el => el.svg)
        .map(el => el.svg)
        .join('')
      : this.list;

    if (!this.keepStyles) {
      let regexString = /(class=".*?")|(fill=".*?")|(<style>.*?<\/style>)|(<svg xmlns=".*?">)|(<\/svg>)|(<title>.*?<\/title>)/g;

      if (this.keepFill) {
        regexString = /(<svg xmlns=".*?">)|(<\/svg>)|(<title>.*?<\/title>)/g;
      }

      symbolsHtmlStr = symbolsHtmlStr ? symbolsHtmlStr.replace(regexString, '') : '';
    }

    this.elem.nativeElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">${symbolsHtmlStr}</svg>`;
  }
}
