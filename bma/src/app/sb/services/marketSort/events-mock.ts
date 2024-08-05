export const eventsMock = {
  'data': [
    {
      groupedByDate: [
        {
          id: 1, events: [{
            id: 1, markets: [{
              id: 1, templateMarketName: 'Match Betting', name: 'Match Betting', displayOrder: 1
            }]
          }]
        },
        {
          id: 2, events: [{
            id: 2, markets: [{
              id: 2, templateMarketName: 'Total Points', name: 'Total Points', displayOrder: 2,
              rawHandicapValue: 2, hidden: true
            }]
          }]
        }
      ]
    },
    {
      groupedByDate: [
        {
          id: 3, events: [{
            id: 3, markets: [{
              id: 3, templateMarketName: 'Match Betting', name: 'Match Betting', displayOrder: 1
            }]
          }]
        },
        {
          id: 4, events: [{
            id: 4, markets: [{
              id: 4, templateMarketName: 'To Win To Nil', name: 'To Win To Nil', displayOrder: 2
            }]
          }]
        }
      ]
    },
    {
      groupedByDate: [
        {
          id: 5, events: [{
            id: 5, markets: [
              {
                id: 5, templateMarketName: 'Total Points', name: 'Total Points', displayOrder: 1,
                rawHandicapValue: 5, hidden: false
              },
              {
                id: 6, templateMarketName: 'Total Points', name: 'Total Points', displayOrder: 2,
                rawHandicapValue: 6, hidden: true
              },
              {
                id: 7, templateMarketName: 'Total Points', name: 'Total Points', displayOrder: -1,
                rawHandicapValue: 7, hidden: true
              },
              {
                id: 8, templateMarketName: 'Total Points', name: 'Total Points', displayOrder: -1,
                rawHandicapValue: 7, hidden: true
              }
            ]
          }]
        }
      ]
    },
    {
      groupedByDate: [
        {
          id: 7, events: [{
            id: 7, markets: [{
              id: 7, templateMarketName: 'Match Betting', name: 'Match Betting', displayOrder: 1
            }]
          }]
        }
      ]
    },
    {
      groupedByDate: [
        {
          id: 8, events: [{
            id: 8, eventIsLive: true, markets: [{
              id: 8, templateMarketName: 'Current Set Winner', name: 'Current Set Winner', displayOrder: 1
            }]
          }]
        }
      ]
    },
    {
      groupedByDate: [
        {
          id: 9, events: [{
            id: 9, eventIsLive: undefined, markets: [{
              id: 9, templateMarketName: 'Current Set Winner', name: 'Current Set Winner', displayOrder: 1
            },
            {
              id: 10, templateMarketName: 'Current Set Winner', name: 'Current Set Winner', displayOrder: 1
            }
          ]
          }]
        }
      ]
    }
  ]
};
