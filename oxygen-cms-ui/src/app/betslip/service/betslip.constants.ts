import { DataTableColumn } from "@app/client/private/models";

export const BSCONST = {
  BS_ACCA_INSURANCE: "betslip-acca-insurance",
  BS_ODDS_BOOST: "betslip-odds-boost",
  ACCA_INS_MSG : 'Acca Insurance Messages',
  ODDS_BOOST_MSG : 'Odds Boost Messages'
};
export const BS_LABELS = {
  ENABLED : 'Enabled',
  ACCA_INS_SP_AND_MSG : 'Acca Insurance Signpostings and Messages',
  ACCA_INSURANCE_ELIGIBILITY_MESSAGE: "Acca Insurance Eligibility Message",
  BETSLIP_ADDTO_QUALIFY_MESSAGE: "Betslip Add to Qualify Message",
  AVAILABLE_INSURANCE_COUNT :'Available Insurances Count Indicator',
  OB_ACCA_COUNT :  'Selections Count',
  BETSLIP_QUALIFIED_MESSAGE: "Betslip Qualified Message",
  BETSLIP_SIGNPOSTING: "Betslip Signposting",
  ACCA_BAR_SIGNPOSTING: "Acca Bar Signposting",
  PROGRESS_BAR: "Progress Bar",
  BET_RECEIPT_SIGNPOSTING: "Bet Receipt Signposting",
  MYBETS_SIGNPOSTING: "My Bets Signposting (Open & Settled)",

  POPUP_DETAILS: "Pop-up Details",
  POPUP_TITLE: "Pop-Up Title",
  POPUP_MESSGE: "Pop-Up Message",
  PRIMARY_CTA: "Primary CTA",
  SECONDARY_CTA: "Secondary CTA",

  BETSLIP_MESSAGE_AND_SIGNPOSTING: "Betslip Messages and Signpostings",
  HEADER_MESSAGES: "Header Messages",
  ODDSBOOST_SIGNPOSTING_AND_MESSAGES: "Odds Boost Signpostings And Messages",

  ICON: "Icon",
  BETSLIPBAR_HEADER: "Betslip bar header",
  BETSLIP_DESCRIPTION: "Bet Slip Description",
  INFO_ICON: "Info Icon",
  BETRECEIPT_SIGNPOSTING: "Bet Receipt Signposting",
  DISPLY_BOOSTED_PRICE: "Display Boosted Price",
  PROFIT_INDICATOR: "Profit Indicator",

  ICON_PLACEHOLDER : '{icon}',
  VALUE_PLACEHOLDER : '{value}',
//Odds Boost section//

BETSLIP_HEADER:'Betslip Header',
DISPLAY_BOOSTED_PRICE :'Display Boosted price',
ODDS_BOOST_MSG_SIGNPOSTINGS :'Odds Boost Messages and Signpostings'


};

export const dataTableColumns: Array<DataTableColumn> = [
  {
    name: "Title",
    property: "tabName",
    link: {
      hrefProperty: "href",
    },
    type: "link",
    width: 2,
  },
  {
    name: "Enabled",
    property: "enable",
    type: "boolean",
    width: 1,
  },
];
