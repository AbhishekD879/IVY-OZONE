import { Directive, Input, ElementRef, OnDestroy, OnChanges, OnInit } from '@angular/core';
import { ServingService } from '@core/services/serving/serving.service';
import { Router, NavigationEnd, Event } from '@angular/router';
import { Subscription } from 'rxjs';

@Directive({
  // eslint-disable-next-line
  selector: '[activeLinkClass]'
})
export class ActiveLinkClassDirective implements OnInit, OnDestroy, OnChanges {

  @Input() link: string;

  private activeLinkClass: string = 'active';
  private routerSubscription: Subscription;

  constructor(
    private elementRef: ElementRef,
    private servingService: ServingService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.routerSubscription = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.updateStatus();
      }
    });
  }

  ngOnDestroy(): void {
    this.routerSubscription && this.routerSubscription.unsubscribe();
  }

  ngOnChanges(): void {
    this.updateStatus();
  }

  private updateStatus(): void {
    const isActive = this.servingService.pathStartsWith(this.link);

    if (isActive) {
      this.setClass();
    } else {
      this.removeClass();
    }
  }

  private setClass(): void {
    this.elementRef.nativeElement.classList.add(this.activeLinkClass);
  }

  private removeClass(): void {
    this.elementRef.nativeElement.classList.remove(this.activeLinkClass);
  }
}
