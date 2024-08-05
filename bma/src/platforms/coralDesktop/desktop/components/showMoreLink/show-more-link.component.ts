import { Component, Input, Output, EventEmitter } from '@angular/core';

import { Router } from '@angular/router';

@Component({
  selector: 'show-more-link',
  templateUrl: './show-more-link.component.html',
  styleUrls: ['./show-more-link.component.scss']
})
export class ShowMoreLinkComponent {
  @Input() link: string;
  @Input() title: string;
  @Output() readonly function = new EventEmitter();

  constructor(
    private router: Router,
  ) {}

  clickFn() {
    this.function && this.function.emit();
    this.router.navigateByUrl(this.link);
  }
}
