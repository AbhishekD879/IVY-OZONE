import { Component } from '@angular/core';
import {
  FiveASideLobbyOverlayComponent as AppFiveASideLobbyOverlayComponent
} from '@app/fiveASideShowDown/components/fiveAsideLobbyOverlay/fiveaside-lobby-overlay.component';
import { GTM_EVENTS, LOBBY_OVERLAY } from '@app/fiveASideShowDown/constants/constants';

@Component({
  selector: 'fiveaside-lobby-overlay',
  templateUrl: './fiveaside-lobby-overlay.component.html',
  styleUrls: ['./fiveaside-lobby-overlay.component.scss']
})
export class FiveASideLobbyOverlayComponent extends AppFiveASideLobbyOverlayComponent {
  /**
   * Method to show entry prizes tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showEntryPrizesTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.changeDetectorRef.detectChanges();
    let containerCorords = this.getContainerRect();
    const entryEl: HTMLElement = this.windowRef.document.querySelector(toBeHighlightEl);
    const highlightEl: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    if (!entryEl || !highlightEl || !containerCorords) {
      this.onClickNext('3');
      return;
    }
    entryEl.scrollIntoView({ block: 'center' });
    containerCorords = this.getContainerRect();
    const entry: DOMRect = entryEl.getBoundingClientRect();
    this.setElementDOMProperty(highlightHolder, 'setStyle', LOBBY_OVERLAY.STYLE.TOP,
      `${entry.top - containerCorords.top - 18}px`);
    this.setElementDOMProperty(highlightHolder, 'setStyle', LOBBY_OVERLAY.STYLE.LEFT,
      `${entry.left - containerCorords.left - 6}px`);
    this.showLobbySignPostingTutorial(entryEl);
    entryEl.scrollIntoView({ block: 'center' });
  }

  /**
   * Method to display sign posting tutorial
   * @param  {HTMLElement} entryEl
   * @returns void
   */
  protected showLobbySignPostingTutorial(entryEl: HTMLElement): void {
    const signPosting: HTMLElement = entryEl.parentElement.parentElement.parentElement.parentElement;
    if (signPosting) {
      const rectEl: HTMLElement = signPosting.querySelector(LOBBY_OVERLAY.SIGN_POST);
      if (rectEl && rectEl.parentElement) {
        const rect: DOMRect = rectEl.getBoundingClientRect();
        const parentRect = rectEl.parentElement.getBoundingClientRect();
        const rectElParentWidth = rectEl.parentElement.offsetWidth;
        const newRect = this.getContainerRect();
        if (newRect) {
          this.setElementDOMProperty(LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.TOP, `${rect.top - newRect.top - 12}px`);
          this.setElementDOMProperty(LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.LEFT,
            `${parentRect.left - newRect.left}px`);
          this.setElementDOMProperty(LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.WIDTH,
            `${rectElParentWidth}px`);
          this.unsetNativeBackgroundColor();
          this.lobbyTutorialGATrack(GTM_EVENTS.NEXT_STEP_1_LABEL);
        }
      }
    }
  }

  /**
   * Method to display show entry info tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showEntryInfoTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.changeDetectorRef.detectChanges();
    const entryEl = this.windowRef.document.querySelector(toBeHighlightEl);
    const el1: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    let containerCorords = this.getContainerRect();
    if (!entryEl || !el1 || !containerCorords) {
      this.onClickNext('4');
      return;
    }
    entryEl.scrollIntoView({ block: 'center' });
    containerCorords = this.getContainerRect();
    let entry = entryEl.getBoundingClientRect();
    entry = entryEl.getBoundingClientRect();
    const cardParentEl = entryEl.parentElement;
    if (cardParentEl) {
      this.rendererService.renderer.setStyle(el1, LOBBY_OVERLAY.STYLE.WIDTH, `${entry.width + 18}px`);
    }
    this.setElementDOMProperty(highlightHolder, 'setStyle', LOBBY_OVERLAY.STYLE.LEFT,
      `${entry.left - containerCorords.left - 11}px`);
    this.setElementDOMProperty(highlightHolder, 'setStyle', LOBBY_OVERLAY.STYLE.TOP,
      `${entry.top - containerCorords.top - 16}px`);
    this.unsetNativeBackgroundColor();
    this.lobbyTutorialGATrack(GTM_EVENTS.NEXT_STEP_2_LABEL);
  }

  /**
   * Method to display showdown card tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showShowdownCardTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.changeDetectorRef.detectChanges();
    const entryEl: HTMLElement = this.windowRef.document.querySelector(toBeHighlightEl);
    const el1: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    let containerCorords = this.getContainerRect();
    if (!entryEl || !el1 || !containerCorords) {
      this.onClickNext(LOBBY_OVERLAY.FINISH);
      return;
    }
    entryEl.scrollIntoView({ block: 'center' });
    containerCorords = this.getContainerRect();
    const entry: DOMRect = entryEl.getBoundingClientRect();
    this.setElementDOMProperty(highlightHolder, 'setStyle', LOBBY_OVERLAY.STYLE.LEFT,
      `${entry.left - containerCorords.left}px`);
    this.setElementDOMProperty(highlightHolder, 'setStyle', LOBBY_OVERLAY.STYLE.TOP,
      `${entry.top - containerCorords.top}px`);
    this.rendererService.renderer.setStyle(el1, LOBBY_OVERLAY.STYLE.HEIGHT, `${entry.height}px`);
    this.rendererService.renderer.setStyle(el1, LOBBY_OVERLAY.STYLE.WIDTH, `${entryEl.offsetWidth - 8}px`);
    this.unsetNativeBackgroundColor();
    this.lobbyTutorialGATrack(GTM_EVENTS.NEXT_STEP_3_LABEL);
  }

  /**
   * Returns container coordinates
   * @returns DOMRect
   */
  private getContainerRect(): DOMRect {
    const containerEl = this.windowRef.document.querySelector(LOBBY_OVERLAY.CLASS_LEADERBOARD_CONTAINER);
    let containerCorords = null;
    if (containerEl) {
      containerCorords = containerEl.getBoundingClientRect();
      return containerCorords;
    }
    return containerCorords;
  }
}
