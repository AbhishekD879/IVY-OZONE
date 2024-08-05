export interface IBYBMarket {
market: string;
active: boolean;
}
export const Tabs: Array<IBYBMarket> =[
    {market:'All Markets', active: true},
    {market:'Popular Markets', active: false},
    {market:'Player Bets', active: false},
    {market:'Team Bets', active: false},
];