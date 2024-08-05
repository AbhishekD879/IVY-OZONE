import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Component, OnInit, Input, Output, OnDestroy, EventEmitter } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'request-error',
  templateUrl: './request-error.component.html',
  styleUrls: ['./request-error.component.scss']
})
export class RequestErrorComponent implements OnInit, OnDestroy {
  static COMPONENT_ID: number = 0;
  @Input() loadFailed: boolean | string;
  @Input() errorMsg?: string;
  @Input() loginNeed?: boolean | string;
  @Input() insertedPlace?: string;
  @Input() reloadMethods?: string[] = ['RELOAD_COMPONENTS'];
  @Output() readonly reloadFn?: EventEmitter<{}> = new EventEmitter();

  loginPending: boolean;
  reloadPending: boolean;

  private title: string;
  private reloadTimeout: number;

  constructor(
    private pubSubService: PubSubService,
    private windowRefService: WindowRefService
  ) {}

  get isServerError(): boolean {
    return !this.loginPending && !!this.loadFailed;
  }
  set isServerError(value:boolean){}

  ngOnInit(): void {
    this.title = `RequestError_${RequestErrorComponent.COMPONENT_ID++}`;

    this.loginPending = false;
    this.loginNeed = this.loginNeed || false;
    this.loadFailed = this.loadFailed || !this.loginNeed;

    this.loginNeed && this.pubSubService.subscribe(this.title, this.pubSubService.API.LOGIN_PENDING, (status: boolean) => {
      this.loginPending = status;
    });
    this.pubSubService.subscribe(this.title, this.reloadMethods, () => this.reloadSection());
  }

  ngOnDestroy(): void {
    this.windowRefService.nativeWindow.clearTimeout(this.reloadTimeout);
    this.pubSubService.unsubscribe(this.title);
  }

  openLoginDialog(): void {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: this.insertedPlace });
  }

  reloadSection(): void {
    this.reloadPending = true;
    this.reloadTimeout = this.windowRefService.nativeWindow.setTimeout(() => {
      this.reloadPending = false;

      this.reloadFn.emit(event);
    }, 1000);
  }
}
