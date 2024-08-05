import { Component, ElementRef, Input, OnInit } from '@angular/core';
import { SvgListItem } from '@app/client/private/models/svgListItem.model';


@Component({
  selector: 'svg-list',
  templateUrl: './svg-list.component.html'
})
export class SvgListComponent implements OnInit {

  @Input() list: string | SvgListItem[];

  constructor(private elem: ElementRef) {}

  ngOnInit() {
    const symbolsHtmlStr = Array.isArray(this.list) ? this.list
        .filter(el => el.svg)
        .map(el => el.svg)
        .join('')
      : this.list;

    this.elem.nativeElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">${symbolsHtmlStr}</svg>`;
  }

  public reinitSvgElement(svg) {
    this.elem.nativeElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">${svg}</svg>`;
  }
}
