import { IMGArenaScoreboard } from '@edp/components/imgArenaScoreboard/models/img-arena-scoreboard';

export const IMG_ARENA_DEFAULT_GOLF: IMGArenaScoreboard = {
    sport: 'golf',
    targetModule: 'full',
    version: '5.x',
    language: 'en',
    targetElementSelector: '#img-arena-event-centre',
    operator: '',
    eventId: '',
    options: {
        videoPlaybackEnabled: false
    },
    initialContext: {
        view: 'GroupDetail',
        roundNo: '',
        groupNo: '',
        holeNo: ''
    }
};

export const IMG_OPERATORS = {
    CORAL: 'coral',
    LADBROKES: 'ladbrokes'
}