/**
 * Digital Sports statistics to OB markets map
 * <Digital Sport Market>: <OB/CMS name>
 *
 * On Event Detail Page in YourCall tab will display only markets listed here
 */
import { YOURCALL_DATA_PROVIDER } from './yourcall-data-provider';
import { YOURCALL_BANACH_MARKETS } from './yourcall-banach-markets';
import { YOURCALL_MARKETS_TYPES } from './yourcall-markets-types';

// TODO: move market 'type' (aka template) property to CMS mapping
export const YOURCALL_MARKETS_MAP = {
  [YOURCALL_DATA_PROVIDER.BYB]: {
    [YOURCALL_BANACH_MARKETS.CORRECT_SCORE]: {
      type: YOURCALL_MARKETS_TYPES.CORRECT_SCORE
    },
    [YOURCALL_BANACH_MARKETS.SHOWN_CARD]: {
      type: YOURCALL_MARKETS_TYPES.SWITCHER,
      multi: true
    },
    [YOURCALL_BANACH_MARKETS.ANYTIME_GOAL]: {
      type: YOURCALL_MARKETS_TYPES.SWITCHER,
      multi: true
    },
    [YOURCALL_BANACH_MARKETS.FIRST_BOOKING]: {
      type: YOURCALL_MARKETS_TYPES.SWITCHER
    },
    [YOURCALL_BANACH_MARKETS.FIRST_GOAL]: {
      type: YOURCALL_MARKETS_TYPES.SWITCHER
    },
    [YOURCALL_BANACH_MARKETS.PLAYER_2_GOALS]: {
      type: YOURCALL_MARKETS_TYPES.SWITCHER,
      multi: true
    },
    [YOURCALL_BANACH_MARKETS.PLAYER_3_GOALS]: {
      type: YOURCALL_MARKETS_TYPES.SWITCHER,
      multi: true
    },
    [YOURCALL_BANACH_MARKETS.PLAYER_BETS]: {
      type: YOURCALL_BANACH_MARKETS.PLAYER_BETS,
      multi: true
    }
  }
};
