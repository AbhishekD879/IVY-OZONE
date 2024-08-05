import { Component, OnDestroy, OnInit } from '@angular/core';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';

@Component({
  template: '',
  selector: 'abstract-outlet'
})
export class AbstractOutletComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnDestroy {
  reloadInitiated: boolean = false;
  state: {
    loading: boolean;
    error: boolean;
  } = {
    loading: true,
    error: false
  };

  constructor() {
    super();
  }

  ngOnInit(): void {}
  ngOnDestroy(): void {}

  showSpinner(): void {
    this.hideError();
    this.state.loading = true;
  }

  hideSpinner(): void {
    this.state.loading = false;
    this.reloadInitiated = false;
  }

  showError(): void {
    this.hideSpinner();
    this.state.error = true;
  }

  hideError(): void {
    this.state.error = false;
  }

  /**
   * Reloads component
   * @protected
   */
  reloadComponent(): void {
    this.reloadInitiated = true;
    this.showSpinner();
    this.ngOnDestroy();
    this.ngOnInit();
  }
}
