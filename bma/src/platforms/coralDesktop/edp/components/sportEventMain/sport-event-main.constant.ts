export const SCOREBOARD_CONFIG = [
  'badminton',
  'volleyball',
  'handball',
  'beachvolleyball',
  'darts'
];

/**
 * Defines the scoreboard initialization order.
 * By default, if the Scoreboard is available, the check sequence is terminated.
 * The ~ sign in the loader id resumes/continues the aborted search chain.
 */
export const SCOREBOARDS_LOAD_ORDER = {
  default: ['OPTA', 'BG', 'BR', 'IMG', 'IMG_ARENA', 'FS', 'GP'],
  tennis: ['IMG', 'OPTA', 'BG', 'FS~', 'GP']
};
