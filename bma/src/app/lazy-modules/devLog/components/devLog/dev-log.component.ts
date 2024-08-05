import { Component, HostListener, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import * as _ from 'underscore';
import { IConstant } from '@core/services/models/constant.model';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'dev-log',
  templateUrl: './dev-log.component.html',
  styleUrls: ['./dev-log.component.scss']
})
export class DevLogComponent implements OnInit {
  environment: any = environment;
  isOpened: boolean = false;
  data: IConstant;
  isNotProduction: boolean;

  /**
   * Query key to open devlog on Mobile Devices
   */
  consoleOpenQueryKey: string = 'qa=1';
  currentEnvironment: string;


  /**
   * Selectbox options data
   */
  environmentsList: any = {
    bma: [
      { name: 'dev0' },
      { name: 'dev1' },
      { name: 'dev2' },
      { name: 'devStage' },
      { name: 'devProduction' }
    ],
    ladbrokes: [
      { name: 'tst2' },
      { name: 'devStage' },
      { name: 'devProduction' }
    ]
  };

  private charMap: number[] = [68, 69, 86, 76, 79, 71]; //  [d, e, v, l, o, g]
  private mapCombo: number = 0;

  constructor(
    private http: HttpClient,
    private windowRefService: WindowRefService
  ) {}

  @HostListener('document:keydown', ['$event.keyCode'])
  onKeyDown(keyCode: number): void {
    if (_.indexOf(this.charMap, keyCode) === this.mapCombo) {
      if (++this.mapCombo === this.charMap.length) {
        this.mapCombo = 0;
        this.openConsole();
      }
    } else {
      this.mapCombo = 0;
    }
    if (keyCode === 27 && this.isOpened) {
      this.closeConsole();
    }
  }

  ngOnInit(): void {
    this.isNotProduction = !this.environment.production || this.environment.IS_DYNAMIC === true;

    if (this.isNotProduction && this.windowRefService.nativeWindow.location.search.indexOf(this.consoleOpenQueryKey) >= 0) {
      this.openConsole();
    }

    this.currentEnvironment = this.windowRefService.nativeWindow.localStorage.getItem('env') || 'dev0';
  }

  openConsole(): void {
    this.isOpened = true;
    this.data || this.http.get<IConstant>('buildInfo.json').subscribe(data => {
      this.data = data;
      this.windowRefService.nativeWindow.scrollTo(0, 0);
    });
  }

  closeConsole(): void {
    this.isOpened = false;
  }

  /**
   * Store chosen environment name to localStorage.
   * Reload page.
   * If devlog was opened with queryParameter, we clear search string, which will reload the page.
   * If devlog was opened with keyboard, just reload the page to apply changes.
   * @param chosenNewEnvironmentName
   */
  setNewEnvironment(chosenNewEnvironmentName: string): void {
    // clear all localstorage data exclude conflicts between environments.
    this.windowRefService.nativeWindow.localStorage.clear();
    this.windowRefService.nativeWindow.localStorage.setItem('env', chosenNewEnvironmentName);

    if (this.windowRefService.nativeWindow.location.search.indexOf(this.consoleOpenQueryKey) >= 0) {
      this.windowRefService.nativeWindow.location.search = '';
    } else {
      this.windowRefService.nativeWindow.location.reload();
    }
  }

  trackByName(option: { name: string }): string {
    return option.name;
  }
}
