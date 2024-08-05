import { Directive, HostListener, Input, OnInit, ElementRef } from '@angular/core';

@Directive({
  // eslint-disable-next-line
  selector: '[linkHref]'
})
export class LinkHrefDirective implements OnInit {

  @Input() link: string;

  constructor(
    private elementRef: ElementRef
  ) {}

  ngOnInit(): void {
    this.elementRef.nativeElement.setAttribute('href', this.link);
  }

  @HostListener('click', ['$event'])
  onclick($event: MouseEvent | TouchEvent): void {
    $event.preventDefault();
  }

}
