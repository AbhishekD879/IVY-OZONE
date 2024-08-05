export const INPLAY_LIVESTREAM_CONFIG = {
  requestConfigLiveStream: {
    requestParams: {
      topLevelType: 'STREAM_EVENT'
    },
    socket: {
      sport: {
        emit: 'GET_SPORT',
        on(data) {
          return `IN_PLAY_SPORTS::${data.categoryId}::STREAM_EVENT`;
        }
      },
      competition: {
        emit: 'GET_TYPE',
        on(data) {
          return `IN_PLAY_SPORT_TYPE::${data.categoryId}::STREAM_EVENT::${data.typeId}`;
        }
      }
    },
    cachePrefix: 'inplaySection',
    limit: 4
  },
  requestConfigLiveEvent: {
    requestParams: {
      topLevelType: 'LIVE_EVENT'
    },
    socket: {
      sport: {
        emit: 'GET_SPORT',
        on(data) {
          return `IN_PLAY_SPORTS::${data.categoryId}::LIVE_EVENT`;
        }
      },
      competition: {
        emit: 'GET_TYPE',
        on(data) {
          return `IN_PLAY_SPORT_TYPE::${data.categoryId}::LIVE_EVENT::${data.typeId}`;
        }
      }
    },
    cachePrefix: 'inplaySection',
    limit: 4
  },
  viewByFilters: [
    'livenow',
    'livestream'
  ]
};
