import {
  Component, Input, AfterViewInit, OnDestroy, ViewContainerRef, ComponentRef,
  ViewChild, OnChanges, SimpleChanges, Output, EventEmitter, ApplicationRef, ChangeDetectorRef
} from '@angular/core';
import * as _ from 'underscore';
import { Subscription } from 'rxjs';

import { LazyComponentFactory } from '@core/services/lazyComponentFactory/lazy-component.factory';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
  selector: 'lazy-component',
  templateUrl: 'lazy-component.component.html',
})
export class LazyComponent extends AbstractOutletComponent implements AfterViewInit, OnChanges, OnDestroy {
  
  @Input() moduleUri?: string;
  @Input() entryComponent?: string;
  @Input() inputs?: {[key: string]: any};
  @Input() outputs?: string[];
  @Input() handleError?: boolean = false;
  @Input() isLoaderEnabled?: boolean = false;

  @Output() readonly init = new EventEmitter<ComponentRef<any>>();
  @Output() readonly failed = new EventEmitter<any>();
  @Output() readonly event = new EventEmitter<{ output: string, value: any}>();

  @ViewChild('container', { read: ViewContainerRef, static: false }) container: ViewContainerRef;

  componentId: string = `LazyComponent${Math.random()}`;
  private componentRef: ComponentRef<any>;
  private outputSubs: Subscription[];
  private timeoutId: number;

  constructor(
    private lazyComponentFactory: LazyComponentFactory,
    private applicationRef: ApplicationRef,
    private windowRef: WindowRefService,
    private changeDetectRef: ChangeDetectorRef
  ) {
    super();

    this.loadComponent = this.loadComponent.bind(this);
  }

  ngAfterViewInit(): void {
    this.loadComponent();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.shouldUpdateInputs(changes)) {
      this.updateInputs();
      this.componentRef && this.componentRef.instance.ngOnChanges && this.componentRef.instance.ngOnChanges(this.formatChanges(changes));
    }
  }

  ngOnDestroy(): void {
    this.destroyComponent();
    this.windowRef.nativeWindow.clearTimeout(this.timeoutId);
  }

  reloadComponent(): void {
    super.reloadComponent();
    this.loadComponent();
  }

  private loadComponent(): void {
    this.showSpinner();

    if (this.moduleUri) {
      this.createComponentByUri();
    }
  }
  /**
   * formats data to simpleChanges type
   * @param {SimpleChanges} changes
   * @return {SimpleChanges} simpleChanges
   */
  private formatChanges(changes: SimpleChanges): SimpleChanges {
    const simpleChanges = {};
    Object.entries(changes['inputs'].currentValue).forEach(([inputName, value]) => {
      if (!_.isEqual(value, changes['inputs'].previousValue[inputName])) {
        simpleChanges[inputName] = { currentValue: value, previousValue: changes['inputs'].previousValue[inputName] };
      }
    });
    return simpleChanges;
  }

  private createComponentByUri(): void {
    this.lazyComponentFactory
      .createLazyComponent(this.moduleUri, this.container, this.entryComponent)
      .then((data: ComponentRef<any>) => {
        this.hideSpinner();
        this.componentRef = data;
        this.updateInputs();
        this.subscribeToOutputs();
        this.init.emit(this.componentRef);
        if (this.componentRef.instance['changeStrategy'] && this.componentRef.instance['changeStrategy'] === STRATEGY_TYPES.ON_PUSH) {
          this.changeDetectRef.detectChanges();
        }
        if(this.componentRef.location.nativeElement.localName == 'multi-market-template'){
          this.changeDetectRef.detectChanges();
        }
        if(this.componentRef.location.nativeElement.localName == 'tote-free-bets-toggle'){
          this.changeDetectRef.detectChanges();
        }
        // Invoke applicationRef.tick asynchroniously to avoid running process change detection when few lazy
        // load components rendering in the same time and only first component has inputs/outputs updated,
        // but all next components - not. SOMETIMES it causes issue when ngOnInit hook executed for second
        // and all next rendering components before updateInputs method for those component's instances
        // @ts-ignore
        this.timeoutId = this.windowRef.nativeWindow.setTimeout(() => this.applicationRef.tick(true));
      })
      .catch(e => {
        console.warn(e);
        this.showError();
        this.failed.emit();
      });
  }

  private destroyComponent(): void {
    _.each(this.outputSubs, sub => sub.unsubscribe());

    if (this.componentRef && this.componentRef.destroy) {
      this.componentRef.destroy();
    }
  }

  private updateInputs(): void {
    if (this.componentRef && this.inputs) {
      _.each(this.inputs, (value: any, inputName: string) => {
        this.componentRef.instance[inputName] = value;
      });
    }
  }

  private shouldUpdateInputs(changes: SimpleChanges): boolean {
    const inputs = changes['inputs'];
    return inputs && (
      inputs.firstChange || !_.isEqual(inputs.previousValue, inputs.currentValue)
    );
  }

  private subscribeToOutputs(): void {
    if (_.isEmpty(this.outputs)) {
      return;
    }

    const component = this.componentRef.instance;

    this.outputSubs = this.outputs
      .filter(outputName => component[outputName] instanceof EventEmitter)
      .map(outputName => {
        return component[outputName].subscribe(value => {
          this.event.emit({ output: outputName, value });
        });
      });
  }
}
