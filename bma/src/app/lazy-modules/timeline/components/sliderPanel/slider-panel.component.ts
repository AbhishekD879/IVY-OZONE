import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  Output,
  OnInit,
  OnDestroy,
  ViewChild,
  ElementRef
} from '@angular/core';
import { IPost } from '@lazy-modules/timeline/models/timeline-post.model';
import { IScrollEvent } from '@lazy-modules/timeline/components/sliderPanel/slider-panel.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { fromEvent, from, merge, Observable, Subscription } from 'rxjs';
import { debounceTime, map, filter, mergeMap, delay, mapTo, pairwise } from 'rxjs/operators';

@Component({
  selector: 'slider-panel',
  templateUrl: './slider-panel.component.html',
  styleUrls: ['./slider-panel.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SliderPanelComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @ViewChild('sliderPanel', {static: true}) sliderPanel: ElementRef;
  @Input() isReconectedFailedMsg: boolean = false;
  @Input() showSkeleton: boolean = false;
  @Input() displayedPosts: IPost[];
  @Input() allPostsLoaded: boolean = false;
  @Input() visible: boolean;
  @Input() priceButtonClasses: { [key: string]: string };
  @Input() isBrandLadbrokes: boolean;
  @Input() gtmModuleBrandName: string;
  @Output() readonly stateChange: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly reloadTimeline: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly loadMore: EventEmitter<void> = new EventEmitter();

  bounce$: Observable<boolean>;
  private subscription: Subscription;

  constructor(
    private changeDetectorRef: ChangeDetectorRef
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    const scrollEnd$ = this.getScrollObservable().pipe(
      map(() => this.isPanelScrolledEnd())
    );
    this.subscription = scrollEnd$.pipe(
      debounceTime(400),
      filter(scrollEnd => scrollEnd && !this.allPostsLoaded)
    ).subscribe(() => {
      this.loadMore.emit();
    });
    this.bounce$ = this.getBounceObservable(scrollEnd$);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  show($event: Event, visible: boolean): void {
    $event.stopPropagation();

    this.visible = visible;
    this.stateChange.emit(visible);
    this.changeDetectorRef.markForCheck();
  }

  callToReload($event: Event): void {
    $event.stopPropagation();
    this.reloadTimeline.emit(true);
  }

  trackByPost(index: number, post: IPost): string {
    return post.id;
  }

  onStateChange(visible: boolean) {
    this.stateChange.emit(visible);
  }

  private getScrollObservable(): Observable<IScrollEvent | any> {
    const events = ['scroll', 'touchmove'];
    return from(events).pipe(mergeMap(event => fromEvent(this.sliderPanel.nativeElement, event)));
  }

  private isScrollEnd(scrollEnd: boolean): boolean {
    return scrollEnd && this.allPostsLoaded;
  }

  private isPanelScrolledEnd(): boolean {
    const { scrollHeight, scrollTop, clientHeight } = this.sliderPanel.nativeElement;
    return (scrollHeight - scrollTop - clientHeight) < 100;
  }

  private getScrollNum(): number {
    const { scrollTop, clientHeight } = this.sliderPanel.nativeElement;
    return scrollTop + clientHeight;
  }

  private getBounceObservable(scrollEnd$: Observable<boolean>): Observable<boolean> {
    const scrollEndAndPostsLoaded$ = scrollEnd$.pipe(
      filter(scrollEnd => this.isScrollEnd(scrollEnd))
    );
    const addBounceAnimation$ = scrollEndAndPostsLoaded$.pipe(
      mapTo(true)
    );
    const removeBounceAnimationAfterDelay$ = scrollEndAndPostsLoaded$.pipe(
      mapTo(false),
      delay(1200)
    );
    const removeBounceAnimationAfterScrollUp$ = scrollEndAndPostsLoaded$.pipe(
      map(() => this.getScrollNum()),
      pairwise(),
      filter(values => values[1] < values[0]),
      mapTo(false)
    );
    return merge(addBounceAnimation$, removeBounceAnimationAfterDelay$, removeBounceAnimationAfterScrollUp$);
  }
}
