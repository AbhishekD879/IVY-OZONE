import { Component } from '@angular/core';
import {
  FiveASideLiveEventOverlayComponent as AppFiveASideLiveEventOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideLiveEventOverlay/five-a-side-live-event-overlay.component';
import { GTM_EVENTS, LIVE_OVERLAY, LOBBY_OVERLAY } from '@app/fiveASideShowDown/constants/constants';

@Component({
  selector: 'five-a-side-live-event-overlay',
  templateUrl: './five-a-side-live-event-overlay.component.html',
  styleUrls: ['./five-a-side-live-event-overlay.component.scss']
})
export class FiveASideLiveEventOverlayComponent extends AppFiveASideLiveEventOverlayComponent {

  /**
   * Set dom properties for Team progress
   * @param  {string} highlightHolder
   * @param  {HTMLElement} entryEl
   */
  protected setDomPropertiesForTeamProgress(highlightHolder: string, entryEl: HTMLElement) {
    this.windowRef.nativeWindow.scrollTo(0, 0);
    const newRect: DOMRect = this.getParentContainerRect();
    if (newRect) {
      const entry: DOMRect = entryEl.getBoundingClientRect();
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${entry.top - newRect.top}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.LEFT,
        `${entry.left - newRect.left}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
        `${entry.width}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
        `${entry.height}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_MY_ENTRY_TEAM_ARROW, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${entry.height + 10}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_CARD_INFO_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${entry.height * 2}px`);
      this.unsetNativeBackgroundColor();
    }
  }

  /**
   * Set DOM properties for Entry progress
   * @param  {string} highlightHolder
   * @param  {DOMRect} legEl
   */
  protected setDomPropertiesEntryProgress(highlightHolder: string, legEl: DOMRect) {
    const newRect: DOMRect = this.getParentContainerRect();
    const entryContainer = this.windowRef.document.querySelector(LIVE_OVERLAY.ID_SUMMARY_EXPANDED);
    if (newRect && entryContainer) {
      const entryContainerRect: DOMRect = entryContainer.getBoundingClientRect();
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${legEl.top - newRect.top}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
        `${entryContainerRect.width}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
        `${legEl.height}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.LEFT,
        `${entryContainerRect.left - newRect.left}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_ARROW_ENTRY_EXPAND, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${legEl.height + 20}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_EXPAND_TEAM_PROGRESS, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${legEl.height * 3}px`);
      this.unsetNativeBackgroundColor();
    }
  }

  /**
   * Method to set DOM properties for Entry progress bar
   * @param  {string} highlightHolder
   * @param  {HTMLElement} progressBarEl
   */
  protected setDomPropertiesEntryProgressBar(highlightHolder: string, progressBarEl: HTMLElement) {
    const entry: DOMRect = progressBarEl.getBoundingClientRect();
    const newRect: DOMRect = this.getParentContainerRect();
    if (newRect) {
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${entry.top - newRect.top}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.LEFT,
        `${entry.left - newRect.left}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
        `${entry.width}px`); // - 30
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
        `${entry.height}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_ENTRY_TOP_PROGRESS_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.BOTTOM,
        `${entry.height * 2}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_PROGRESS_ARROW, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${entry.height}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_CARD_INFO_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${entry.height}px`);
      this.unsetNativeBackgroundColor();
    }
  }

  /**
   * Method to display Leaderboard entries tutorial
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showLeaderboardEntriesTutorial(highlightHolder: string): void {
    this.changeDetectorRef.detectChanges();
    this.setElementDOMProperty(LIVE_OVERLAY.ID_SUMMARY_EXPANDED, LIVE_OVERLAY.SET_STYLE, 'display',
        `unset`);
    const leaderboardItemEl = this.windowRef.document.querySelector(LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM);
    const leaderboardTitleEl = this.windowRef.document.querySelector(LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE);
    const highlightEl: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    if (!highlightEl || !leaderboardItemEl || !leaderboardTitleEl) {
      this.onClickNext('5');
      return;
    }
    const newRect: DOMRect = this.getParentContainerRect();
    if (newRect) {
      const leaderboardItem = leaderboardItemEl.getBoundingClientRect();
      const leaderboardTitleContent = leaderboardTitleEl.getBoundingClientRect();
      const calcHeight = this.calculateLeaderboardEntriesHeight(2) + leaderboardTitleContent.height + 43;
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE,
        LOBBY_OVERLAY.STYLE.TOP, `${leaderboardTitleContent.top - newRect.top - 6}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
        `${leaderboardItem.width}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
        `${calcHeight - 5}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.LEFT,
        `${leaderboardItem.left - newRect.left}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_CARD_INFO_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${calcHeight + 20}px`);
      this.unsetNativeBackgroundColor();
    }
    this.liveTutorialGATrack(GTM_EVENTS.NEXT_STEP_4_LABEL);
  }

  /**
   * Get coordianates for parent container
   * @returns DOMRect
   */
  private getParentContainerRect(): DOMRect {
    const containerEl = this.windowRef.document.querySelector(LIVE_OVERLAY.CLASS_LEADERBOARD_CONTAINER);
    let containerCorords = null;
    if (containerEl) {
      containerCorords = containerEl.getBoundingClientRect();
      return containerCorords;
    }
    return containerCorords;
  }
}
