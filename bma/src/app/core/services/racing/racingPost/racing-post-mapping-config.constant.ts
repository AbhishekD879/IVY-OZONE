import {
  IRacingPostMappingConfig, IRacingPostHRRaceData, IRacingPostGHRaceData, IRacingPostHorse, IRacingPostGreyhound
} from '@core/services/racing/racingPost/racing-post.model';

export const GREYHOUND_MAPPING_CONFIG: IRacingPostMappingConfig<IRacingPostGHRaceData, IRacingPostGreyhound> = {
  eventKeysMap: {
    distance: 'distance',
    raceType: 'raceType',
    postPick: 'postPick',
    grade: 'grade'
  },
  outcomeKeysMap: {
    comment: 'overview',
    last5Runs: 'formGuide',
    trainerName: 'trainer'
  },
  runnersKeys: {
    runnersPropName: 'runners',
    runnerNumberPropName: 'trap'
  }
};

export const HORSERACING_MAPPING_CONFIG: IRacingPostMappingConfig<IRacingPostHRRaceData, IRacingPostHorse> = {
  eventKeysMap: {
    yards: 'distance',
    verdict: 'overview',
    goingCode: 'going',
    raceName: 'title',
    raceClass: 'class', // TODO: temporary unavailable form PR API side, will be added in new API!
    newspapers: 'newspapers',
    courseGraphicsLadbrokes: 'courseGraphics',
    raceType: 'raceType',
    horses: 'horses'
  },
  outcomeKeysMap: {
    trainer: 'trainer',
    rating: 'officialRating',
    rpRating: 'rprRating',
    horseAge: 'age',
    jockey: 'jockey',
    silk: 'silkName',
    formfigs: 'formGuide',
    weightLbs: 'weight',
    spotlight: 'overview',
    officialRating: 'formProviderRating',
    draw: 'draw',
    courseDistanceWinner: 'courseDistanceWinner',
    isBeatenFavourite: 'isBeatenFavourite',
    starRating: 'starRating',
    form: 'form',
    allowance: 'allowance',
    rpHorseId: 'rprHorseId'
  },
  runnersKeys: {
    runnersPropName: 'horses',
    runnerNumberPropName: 'saddle'
  }
};
