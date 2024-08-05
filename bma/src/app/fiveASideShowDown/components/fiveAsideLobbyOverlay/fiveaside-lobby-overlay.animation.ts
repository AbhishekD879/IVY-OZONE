import { trigger, transition, style, animate, keyframes, sequence, query } from '@angular/animations';

export const textContentNoDelay = trigger('textContent-noDelay', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate('1s', style({ opacity: 1 }))
    ])
]);
export const textContentFade = trigger('textContent-fade', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate('1s 2s', style({ opacity: 1 }))
    ])
]);
export const textButtonWelcome = trigger('textButton-Welcome', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate('0.5s 1s', style({ opacity: 1 }))
    ])
]);
export const showdownCardArrow = trigger('showdownCard-arrow', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1.4s 0.5s ease-in',
            keyframes([
                style({ opacity: 0, top: '380px', offset: 0 }),
                style({ opacity: 1, top: '245px', offset: 1 })
            ])
        )
    ])
]);
export const liveCardArrow = trigger('liveCard-arrow', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1s 1s ease-in',
            keyframes([
                style({ opacity: 0, top: '380px', offset: 0 }),
                style({ opacity: 1, top: '70px', offset: 1 }),
            ])
        )
    ])
]);
export const teamProgressDownArrow = trigger('teamProgressDown-arrow', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1s 0.5s ease-in',
            keyframes([
                style({ opacity: 0, top: '380px', offset: 0 }),
                style({ opacity: 1, top: '50px', offset: 1 }),
            ])
        )
    ])
]);
export const liveEntriesArrow = trigger('liveEntries-arrow', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1.4s 0.5s ease-in',
            keyframes([
                style({ opacity: 0, top: '380px', offset: 0 }),
                style({ opacity: 1, top: '220px', offset: 1 }),
            ])
        )
    ])
]);
export const teamProgressArrow = trigger('teamProgress-arrow', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1s 1s cubic-bezier(0.65, 0, 0.35, 1)',
            keyframes([
                style({ opacity: 0, margin: '0', offset: 0 }),
                style({ opacity: 1, margin: '0 auto 0 35%', offset: 1 }),
            ])
        )
    ])
]);
export const entryInfoArrow = trigger('entryInfo-arrow', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1s 1s cubic-bezier(0.65, 0, 0.35, 1)',
            keyframes([
                style({ opacity: 0, right: '200px', offset: 0 }),
                style({ opacity: 1, right: '100px', offset: 1 }),
            ])
        )
    ])
]);
export const entryInfoArrowMobile = trigger('entryInfo-arrow-Mobile', [
    transition('void => *', [
        style({ opacity: 0 }),
        animate(
            '1s 1s cubic-bezier(0.65, 0, 0.35, 1)',
            keyframes([
                style({ opacity: 0, top: '130px', offset: 0 }),
                style({ opacity: 1, top: '79px', offset: 1 }),
            ])
        )
    ])
]);
export const cardPrizeInfo = trigger('cardPrizeInfo', [
    transition('void => *', [
        query('#arrow-prizes', style({ opacity: 0 })),
        query('#arrow-signposting', style({ opacity: 0 })),
        query('#sign-postings', style({ opacity: 0 })),
        query('#signposting-content', style({ opacity: 0 })),
        sequence([
            query('#entry-prizes', [
                animate(
                    '1s cubic-bezier(0.65, 0, 0.35, 1)',
                    keyframes([
                        style({
                            transform: 'scale(9)',
                            'webkit-transform': 'scale(9)',
                            'box-shadow': '-409px -2020px 48px 2100px #000000cc',
                            'border-radius': '0%',
                            offset: 0
                        }),
                        style({
                            transform: 'scale(1)',
                            'box-shadow': 'inset 0 0 3px 2px #007affcc, 0 0 8px 1px #007affcc, -409px -2020px 48px 2100px #000000cc',
                            'border-radius': '50%',
                            offset: 0.8
                        }),
                        style({
                            transform: 'scale(1)',
                            'box-shadow': 'inset 0 0 3px 2px #007affcc, 0 0 8px 1px #007affcc, -409px -2020px 48px 2100px #000000cc',
                            'border-radius': '50%',
                            offset: 1
                        })
                    ])
                )
            ]),
            query('#arrow-prizes', [
                animate(
                    '1s cubic-bezier(0.65, 0, 0.35, 1)',
                    keyframes([
                        style({ opacity: 0, right: '160px', offset: 0 }),
                        style({ opacity: 1, right: '100px', offset: 1 }),
                    ])
                )
            ]),
            query('#sign-postings', [
                style({ opacity: 1 }),
                query('#signposting-content', style({ opacity: 0 })),
                animate(
                    '1s cubic-bezier(0.65, 0, 0.35, 1)',
                    keyframes([
                        style(
                            {
                                height: '400px',
                                'box-shadow': '-73px 850px 57px 916px #000000cc',
                                offset: 0
                            }
                        ),
                        style(
                            {
                                height: '53px',
                                'box-shadow': 'inset 0 0 3px 2px #007affcc, 0 0 8px 1px #007affcc, -73px 850px 57px 916px #000000cc',
                                offset: 1
                            }
                        )
                    ])
                )
            ]),
            query('#arrow-signposting', [
                // style({ opacity: 1 }),
                animate(
                    '1s 0.8s cubic-bezier(0.65, 0, 0.35, 1)',
                    keyframes([
                        style({ opacity: 0, bottom: '170px' }),
                        style({ opacity: 1, bottom: '90px' }),
                    ])
                )
            ]),
            query('#signposting-content', [
                animate(
                    '1s 1s cubic-bezier(0.65, 0, 0.35, 1)',
                    keyframes([
                        style({ opacity: 0 }),
                        style({ opacity: 1 })
                    ])
                )
            ])
        ])
    ])
]);
