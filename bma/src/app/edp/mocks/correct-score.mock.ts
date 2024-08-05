export const eventOutcomesMock =  {outcomes: [{
  outcomeMeaningScores: '2,0',
  originalOutcomeMeaningMinorCode:'S',
  outcomeMeaningMinorCode: '1'
}, {
  outcomeMeaningScores: '0,2',
  originalOutcomeMeaningMinorCode:'S',
  outcomeMeaningMinorCode: '2'
},
{
  outcomeMeaningScores: null,
  originalOutcomeMeaningMinorCode:'H',
  outcomeMeaningMinorCode: '1'
},
{
  outcomeMeaningScores: null,
  originalOutcomeMeaningMinorCode:'D',
  outcomeMeaningMinorCode: '2'
},
{
  outcomeMeaningScores: null,
  originalOutcomeMeaningMinorCode:'A',
  outcomeMeaningMinorCode: '3'
},
{
  outcomeMeaningScores: null,
  originalOutcomeMeaningMinorCode:'O',
  outcomeMeaningMinorCode: '1'
}]}  as any;

export const groupeddata = {
  1: [{ id: 1, outcomeMeaningMinorCode: 1 }],
  2: [{ id: 2, outcomeMeaningMinorCode: 2 }],
  3: [{ id: 3, outcomeMeaningMinorCode: 3 }]
};

export const groupedOutcomes = [[{'id':1,'outcomeMeaningMinorCode':1}],
[{'id':2,'outcomeMeaningMinorCode':2}],
[{'id':3,'outcomeMeaningMinorCode':3}]] as any;

export const marketGrouped = [{
  name: 'A',
  marketMeaningMinorCode: 'CS',
  outcomes: [{name: 'A', }]
 },
 {
  name: 'A',
  marketMeaningMinorCode: 'MR',
  outcomes: [{name: 'A', }]
 }
] as any;

