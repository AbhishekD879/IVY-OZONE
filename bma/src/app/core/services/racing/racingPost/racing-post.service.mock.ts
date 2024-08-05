export const STUB_OB_EVENTS = [
  { id: 0, markets: [{ outcomes: [] }] },
  { id: 1, markets: [{ }] },
  { id: 2, markets: [{ outcomes: [] }] },
  { id: 4, markets: [] },
  { id: 5 }
];

export const STUB_RP_DATA = {
  Error: false,
  document: {
    0: { raceType: 'race-0' },
    1: { raceType: 'race-1' },
    3: { raceType: 'race-3' },
    4: { raceType: 'race-4' },
    5: { raceType: 'race-5' }
  }
};

export const HORSES_DATA = [
    {
       'horseName':'Royal Advice',
    },
    {
       'horseName':'Significantly',
       'isMostTipped':true
    }
 ];

 export const NEWSPAPERS_DATA = [
   {
     'selection': 'Significantly',
     'name': 'SPOTLIGHT',
     'rpSelectionUid': 3048926,
     'tips': '11'
   },
   {
     'selection': 'Digital',
     'name': 'Daily Mail',
     'rpSelectionUid': 3048916,
     'tips': '2'
   },
   {
    'selection':'Significantly',
    'name':'RP Ratings',
    'rpSelectionUid':3048926
 },

 ];

export const HORSERACING_EVENTS = [{
  id: 1,
  racingFormEvent: { everything: 'will-change', overview: '', horses: HORSES_DATA },
  markets: [{
    outcomes: [{
      name: 'Horse-1-1',
      racingFormOutcome: { everything: 'will-change' },
      runnerNumber: '1'
    }, {
      name: 'Horse-1-2',
      racingFormOutcome: { anything: 'not-changed' },
      runnerNumber: '2',
    }, {
      name: 'Horse-1-3'
    }, {
      name: 'Horse-1-4',
      racingFormOutcome: { everything: 'will-change' },
      runnerNumber: '4',
    }]
  }]
}, {
  id: 2,
  markets: [{
    outcomes: [{
      name: 'Horse-2-1',
      racingFormOutcome: { anything: 'not-changed', },
      runnerNumber: '1',
    }, {
      name: 'Horse-2-2',
      racingFormOutcome: { anything: 'not-changed', },
      runnerNumber: '3',
    }]
  }]
}, {
  id: 3,
  racingFormEvent: { anything: 'not-changed', horses: HORSES_DATA },
  markets: [{
    outcomes: [{
      name: 'Horse-3-1',
      runnerNumber: '1',
    }, {
      name: 'Horse-3-2',
      racingFormOutcome: { anything: 'not-changed' },
      runnerNumber: '2',
    }]
  }]
}];

export const GREYHOUND_EVENTS = [{
  id: 1,
  racingFormEvent: { everything: 'will-change', horses: []},
  markets: [{
    outcomes: [{
      name: 'Hound-1-1',
      racingFormOutcome: { everything: 'will-change' },
      runnerNumber: '1'
    }, {
      name: 'Hound-1-2',
      racingFormOutcome: { anything: 'not-changed' },
      runnerNumber: '2'
    }, {
      name: 'Hound-1-3',
      racingFormOutcome: { anything: 'not-changed' }
    }]
  }]
}, {
  id: 2,
  markets: [{
    outcomes: [{
      name: 'Hound-2-1',
      racingFormOutcome: { anything: 'not-changed', },
      runnerNumber: '1'
    }, {
      name: 'Hound-2-2',
      racingFormOutcome: { anything: 'not-changed', },
      runnerNumber: '3'
    }]
  }]
}, {
  id: 3,
  racingFormEvent: { anything: 'not-changed', horses: [] },
  markets: [{
    outcomes: [{
      name: 'Hound-3-1',
      runnerNumber: '1'
    }, {
      name: 'Hound-3-2',
      racingFormOutcome: { anything: 'not-changed' },
      runnerNumber: '2'
    }]
  }]
}];

export const RACINGPOST_HR_RESPONSE = {
  Error: 'false',
  document: {
    1: {
      yards: 'yards-1',
      goingCode: 'going-1',
      raceName: 'race-1',
      raceClass: 'race-class-1',
      raceType: 'race-type-1',
      verdict: 'verdict-1',
      courseGraphicsLadbrokes: 'course-graphics-1',
      horses: [{
        horseAge: 5,
        draw: '3',
        formfigs: 'form-1-1',
        jockey: 'jockey-1-1',
        trainer: 'trianer-1-1',
        rating: 3,
        silk: 'silk-1-1.png',
        weightLbs: 90,
        spotlight: 'spotlight-1-1',
        officialRating: 0,
        courseDistanceWinner: '4',
        starRating: '',
        saddle: '1',
        form: ['form-1-1a', 'form-1-1b'],
        unmappedProp: 'unmappedProp',
        horseName: 'horseName',
        isMostTipped: 'true'
      }, {
        jockey: 'nothing',
        silk: 'applied',
        saddle: 3
      }, {
        jockey: 'jockey-1-4',
        silk: 'silk-1-4.png',
        saddle: 4,
        starRating: 4
      }],
      newspapers: [{
        name: 'newspaper-name-1-1',
        selection: 'newspaper-selection-1-1'
      }, {
        selection: 'newspaper-selection-1-2'
      }, {
        name: 'newspaper-name-1-3'
      }],
      unmappedProp: 'unmappedProp'
    },
    2: {
      yards: 'yards-2',
      goingCode: 'going-2',
      raceName: 'race-2',
      overview: 'overview-2'
    },
    4: {
      yards: 'nothing',
      verdict: 'applied',
      horses: [{
        jockey: 'nothing',
        silk: 'applied',
        saddle: 1
      }],
      newspapers: [{
        name: 'nothing',
        selection: 'applied'
      }]
    },
  }
};

export const RACINGPOST_GH_RESPONSE = {
  Error: 'false',
  document: {
    1: {
      distance: 'distance-1',
      raceType: 'race-type-1',
      postPick: 'post-pick-1',
      runners: [{
        comment: 'comment-1-1',
        last5Runs: 'last5runs-1-1',
        trap: '1',
        unmappedProp: 'unmappedProp'
      }, {
        comment: 'nothing',
        last5Runs: 'applied',
        trap: 3
      }],
      unmappedProp: 'unmappedProp'
    },
    2: {
      distance: 'distance-2',
      raceType: 'race-type-2',
      postPick: 'post-pick-2',
    },
    4: {
      distance: '3m 5y',
      raceType: 'race-type-4',
      postPick: 'post-pick-4',
      runners: [{
        comment: 'nothing',
        last5Runs: 'applied',
        trap: '1',
      }]
    },
  }
};

export const RACE_DATA = [
  {
     'id':1,
     'racingFormEvent':{
        'distance':'yards-1',
        'overview':'verdict-1',
        'going':'going-1',
        'title':'race-1',
        'class':'race-class-1',
        'newspapers':[
           {
              'name':'newspaper-name-1-1',
              'selection':'newspaper-selection-1-1'
           },
           {
              'selection':'newspaper-selection-1-2'
           },
           {
              'name':'newspaper-name-1-3'
           }
        ],
        'courseGraphics':'course-graphics-1',
        'raceType':'race-type-1',
        'horses':[
           {
              'horseAge':5,
              'draw':'3',
              'formfigs':'form-1-1',
              'jockey':'jockey-1-1',
              'trainer':'trianer-1-1',
              'rating':3,
              'silk':'silk-1-1.png',
              'weightLbs':90,
              'spotlight':'spotlight-1-1',
              'officialRating':0,
              'courseDistanceWinner':'4',
              'starRating':'',
              'saddle':'1',
              'form':[
                 'form-1-1a',
                 'form-1-1b'
              ],
              'unmappedProp':'unmappedProp',
              'horseName':'horseName',
              'isMostTipped':'true'
           },
           {
              'jockey':'nothing',
              'silk':'applied',
              'saddle':3
           },
           {
              'jockey':'jockey-1-4',
              'silk':'silk-1-4.png',
              'saddle':4,
              'starRating':4
           }
        ]
     },
     'markets':[
        {
           'outcomes':[
              {
                 'name':'Horse-1-1',
                 'racingFormOutcome':{
                    'trainer':'trianer-1-1',
                    'officialRating':'3',
                    'age':'5',
                    'jockey':'jockey-1-1',
                    'silkName':'silk-1-1.png',
                    'formGuide':'form-1-1',
                    'weight':'90',
                    'overview':'spotlight-1-1',
                    'formProviderRating':'0',
                    'draw':'3',
                    'courseDistanceWinner':'4',
                    'starRating':'',
                    'form':[
                       'form-1-1a',
                       'form-1-1b'
                    ]
                 },
                 'runnerNumber':'1'
              },
              {
                 'name':'Horse-1-2',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'2'
              },
              {
                 'name':'Horse-1-3'
              },
              {
                 'name':'Horse-1-4',
                 'racingFormOutcome':{
                    'jockey':'jockey-1-4',
                    'silkName':'silk-1-4.png',
                    'starRating':'4'
                 },
                 'runnerNumber':'4'
              }
           ]
        }
     ],
     'racingPostVerdict':{
        'starRatings':[
           {
              'name':'Horse-1-4',
              'rating':4
           }
        ],
        'tips':[
           {
              'name':'newspaper-name-1-1',
              'value':'newspaper-selection-1-1'
           },
           {
              'value':'newspaper-selection-1-2'
           },
           {
              'name':'newspaper-name-1-3'
           }
        ],
        'verdict':'verdict-1',
        'imgUrl':'course-graphics-1',
        'isFilled':true,
        'mosttipped':[
        ]
     }
  },
  {
     'id':2,
     'markets':[
        {
           'outcomes':[
              {
                 'name':'Horse-2-1',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'1'
              },
              {
                 'name':'Horse-2-2',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'3'
              }
           ]
        }
     ],
     'racingFormEvent':{
        'distance':'yards-2',
        'going':'going-2',
        'title':'race-2'
     },
     'racingPostVerdict':{
        'starRatings':[
        ],
        'tips':[
        ],
        'isFilled':false,
        'mosttipped':[

        ]
     }
  },
  {
     'id':3,
     'racingFormEvent':{
        'anything':'not-changed',
        'horses':[
           {
              'horseName':'Royal Advice'
           },
           {
              'horseName':'Significantly',
              'isMostTipped':true
           }
        ]
     },
     'markets':[
        {
           'outcomes':[
              {
                 'name':'Horse-3-1',
                 'runnerNumber':'1'
              },
              {
                 'name':'Horse-3-2',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'2'
              }
           ]
        }
     ]
  }
];

export const RACE_DATA_GH = [
  {
     'id':1,
     'racingFormEvent':{
        'distance':'distance-1',
        'raceType':'race-type-1',
        'postPick':'post-pick-1'
     },
     'markets':[
        {
           'outcomes':[
              {
                 'name':'Hound-1-1',
                 'racingFormOutcome':{
                    'overview':'comment-1-1',
                    'formGuide':'last5runs-1-1'
                 },
                 'runnerNumber':'1'
              },
              {
                 'name':'Hound-1-2',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'2'
              },
              {
                 'name':'Hound-1-3',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 }
              }
           ]
        }
     ]
  },
  {
     'id':2,
     'markets':[
        {
           'outcomes':[
              {
                 'name':'Hound-2-1',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'1'
              },
              {
                 'name':'Hound-2-2',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'3'
              }
           ]
        }
     ],
     'racingFormEvent':{
        'distance':'distance-2',
        'raceType':'race-type-2',
        'postPick':'post-pick-2'
     }
  },
  {
     'id':3,
     'racingFormEvent':{
        'anything':'not-changed',
        'horses':[
        ]
     },
     'markets':[
        {
           'outcomes':[
              {
                 'name':'Hound-3-1',
                 'runnerNumber':'1'
              },
              {
                 'name':'Hound-3-2',
                 'racingFormOutcome':{
                    'anything':'not-changed'
                 },
                 'runnerNumber':'2'
              }
           ]
        }
     ]
  }
];

export const PREPARE_VERDICT_DATA = {
   'id': 1,
   'racingFormEvent': {
       'distance': 'yards-1',
       'overview': 'verdict-1',
       'going': 'going-1',
       'title': 'race-1',
       'class': 'race-class-1',
       'newspapers': [
           {
               'name': 'newspaper-name-1-1',
               'selection': 'newspaper-selection-1-1'
           },
           {
               'selection': 'newspaper-selection-1-2'
           },
           {
               'name': 'newspaper-name-1-3'
           }
       ],
       'courseGraphics': 'course-graphics-1',
       'raceType': 'race-type-1',
       'horses': [
           {
               'horseAge': 5,
               'draw': '3',
               'formfigs': 'form-1-1',
               'jockey': 'jockey-1-1',
               'trainer': 'trianer-1-1',
               'rating': 3,
               'silk': 'silk-1-1.png',
               'weightLbs': 90,
               'spotlight': 'spotlight-1-1',
               'officialRating': 0,
               'courseDistanceWinner': '4',
               'starRating': '',
               'saddle': '1',
               'form': [
                   'form-1-1a',
                   'form-1-1b'
               ],
               'unmappedProp': 'unmappedProp',
               'horseName': 'horseName',
               'isMostTipped': 'true'
           },
           {
               'jockey': 'nothing',
               'silk': 'applied',
               'saddle': 3
           },
           {
               'jockey': 'jockey-1-4',
               'silk': 'silk-1-4.png',
               'saddle': 4,
               'starRating': 4
           }
       ]
   },
   'markets': [
       {
           'outcomes': [
               {
                   'name': 'Horse-1-1',
                   'racingFormOutcome': {
                       'trainer': 'trianer-1-1',
                       'officialRating': '3',
                       'age': '5',
                       'jockey': 'jockey-1-1',
                       'silkName': 'silk-1-1.png',
                       'formGuide': 'form-1-1',
                       'weight': '90',
                       'overview': 'spotlight-1-1',
                       'formProviderRating': '0',
                       'draw': '3',
                       'courseDistanceWinner': '4',
                       'starRating': '',
                       'form': [
                           'form-1-1a',
                           'form-1-1b'
                       ]
                   },
                   'runnerNumber': '1'
               },
               {
                   'name': 'Horse-1-2',
                   'racingFormOutcome': {
                       'anything': 'not-changed'
                   },
                   'runnerNumber': '2'
               },
               {
                   'name': 'Horse-1-3'
               },
               {
                   'name': 'Horse-1-4',
                   'racingFormOutcome': {
                       'jockey': 'jockey-1-4',
                       'silkName': 'silk-1-4.png',
                       'starRating': '4'
                   },
                   'runnerNumber': '4'
               }
           ]
       }
   ]
};
