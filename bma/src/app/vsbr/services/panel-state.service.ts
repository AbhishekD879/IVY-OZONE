import { Injectable } from '@angular/core';

@Injectable()
export class PanelStateService {
  private panelsStates: Object = {};

  changeStatePanel(eventId, panelId) {
    if (!this.panelsStates[eventId]) {
      this.panelsStates[eventId] = {};
    }
    this.panelsStates[eventId][panelId] = !this.panelsStates[eventId][panelId];
  }

  getPanelsStates() {
    return this.panelsStates;
  }
}
